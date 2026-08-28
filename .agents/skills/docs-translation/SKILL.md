---
name: docs-translation
description: 开源文档翻译站点的翻译与上游同步技能：上游英文文档更新后同步中文译文、翻译新增页面、校验结构与术语一致性、把流程复用到新的文档项目。凡涉及翻译本仓库文档、同步上游更新、比对译文一致性、维护术语表或初始化新翻译项目，一律使用本技能。Use whenever translating docs in this repo, syncing translations after upstream updates, verifying translation parity, or onboarding a new docs project.
---

# docs-translation：文档翻译与上游同步

## 工作原理

本技能**完全自包含**于站点仓库的 `.agents/skills/docs-translation/`（Mintlify 自动忽略该目录，不会发布）：

```
docs-translation/
├── SKILL.md            本文件：流程与红线
├── project.json        项目事实（上游仓库、路径、扩展名映射、术语表位置等）
├── references/         rules.md 翻译规范；terminology.md 约束性术语表
├── scripts/            verify_structure.py（批量结构校验）；verify_mdx.py（单篇深查）
└── state/              batches.json 源↔译文配对清单；sync-state.json 同步基线
```

**零侵入约束**：除译文站点内容（`.mdx`、`docs.json`、`assets/`）与技能目录自身外，不修改站点仓库的任何文件（README、AGENTS.md、.mintignore、.gitignore 等一律不动）。每次会话动手前先读 `project.json`，不要凭记忆。所有命令在站点仓库根目录执行；下文命令里的具体取值均来自 `project.json`，换项目时按配置替换。

| 配置字段 | 含义 |
|---|---|
| `upstream` | 上游仓库 `repo` / 分支 `branch` / 文档目录 `docs_dir` |
| `source_cache` | 上游仓库的本地克隆位置（`/tmp` 会被清空，每次会话按步骤 0 重建） |
| `site_root` / `nav_file` | 译文站点根（相对 translation/）与导航文件 |
| `source_ext` → `target_ext` | 源/译文扩展名映射，路径一一对应 |
| `rules` / `terminology` | 翻译规范与约束性术语表（**动手前必读，对一切翻译任务双向约束**） |
| `pairs` | 源↔译文配对清单（新增/删除/改名都要登记） |
| `sync_state` | 同步基线：现有译文对应的最后上游 commit |
| `protected_assets` | 本项目自绘品牌资产，同步时不被上游同名文件覆盖 |
| `nav_tabs` | 上游导航 tab 名 → 本站译名对照 |

要点速记（详见 rules / terminology）：代码围栏与行内代码字节级保留；链接 URL 原样、链接文字翻译；JSX 组件只译标签间文本与展示型属性（`title`/`label`/`description`/`alt`）；frontmatter 只译 `title`/`description`；术语严禁现场发明，未收录且无先例的保留英文并列入「待定术语」。

## 步骤 0：准备英文源（每次会话必做）

```bash
SRC=/tmp/semantica-src   # project.json 的 source_cache
BR=main                  # project.json 的 upstream.branch
REPO=https://github.com/semantica-agi/semantica
if [ -d "$SRC/.git" ]; then
  if [ "$(git -C "$SRC" rev-parse --is-shallow-repository)" = true ]; then
    git -C "$SRC" fetch --unshallow origin "$BR" || git -C "$SRC" fetch origin "$BR"
  else
    git -C "$SRC" fetch origin "$BR"
  fi
  git -C "$SRC" reset --hard "origin/$BR"
else
  git clone "$REPO" "$SRC"
fi
```

**完整历史是硬要求**：A1 要对旧基线 commit 做 `git diff`，shallow 克隆里旧基线可能已不存在，diff 会失败。若 diff 因基线缺失报错，删掉缓存重新完整克隆（不要用 `--depth 1`）。

## 工作流 A：同步上游更新（源文档变了）

### A1. 找出变更

```bash
BASE=$(python3 -c "import json;print(json.load(open('.agents/skills/docs-translation/state/sync-state.json'))['last_synced_commit'])")
NEW=$(git -C /tmp/semantica-src rev-parse origin/main)
git -C /tmp/semantica-src diff --name-status "$BASE" "$NEW" -- docs/
```

按状态分类处理：

- `M docs/xxx.md` — 页面内容有变 → A2
- `A` — 新增页面 → 工作流 B 全量翻译，并登记进 `pairs` 与站点 `nav_file`（新批次命名 `<batch_prefix><下一序号>-sync-<yyyymmdd>`，序号接续现有批次递增，如 `B16-sync-20260828`）
- `D` — 删除页面 → 删对应译文，从 `pairs` 与 `nav_file` 移除
- `R100 docs/old.md docs/new.md` — 改名 → 移动译文，同步两处清单
- 上游 `docs/docs.json` 有变 → A3
- `docs/assets/*` 有变 → 复制到站点 `assets/`；**例外**：文件名在 `protected_assets` 里的不覆盖

无变更则直接结束（仍建议跑一次步骤 3 的全量校验）。

### A2. 逐页更新（最小改动原则）

对每个 `M` 页面：

1. `git -C /tmp/semantica-src diff "$BASE" "$NEW" -- docs/xxx.md` 找出源文变更的段落、列表项、代码块、表格。
2. 只修改译文中语义对应的部分：新增句子翻译后插入对应位置，删除句子从译文删掉，改写段落重译。**源文未动的段落，译文一字不动**——不做全文重译，不做风格回炉。
3. **大改版出口**：diff 显示整页约三分之一以上段落被重写时，逐段拼接得不偿失——放弃 A2，改按工作流 B 整篇重译。
4. 变更后的代码围栏、行内代码从新源文逐字节复制；新增 JSX 组件按规则只译人类语言文本。
5. 标题层级、列表项数、表格行列、JSX 数量随源文变化同步调整，保持一一对应。

### A3. 同步导航

站点 `docs.json` 与上游导航结构一一对应：`pages` 路径跟随上游；tab 名按 `nav_tabs` 对照翻译；group 名按术语表翻译；页面在导航中的标题与该页 frontmatter `title` 一致。改完导航跑 `npx -y mint@latest broken-links` 查死链。

## 工作流 B：翻译新页面

逐文件循环（可按 `pairs` 的批次推进）：

1. 读 `rules` 与 `terminology` 指向的文件（每次都读，术语表可能已增量更新）。
2. 读源文整篇，理解后再动笔；以中文技术作者口吻重述，**不增删任何信息**。
3. 译文写入站点对应路径（`.mdx`，路径与源文一一对应）。
4. 自检（每篇必做，见 rules 流程节）：数标题层级与数量、比对代码围栏、数列表项/表格行列/链接/JSX 标签、通读成稿去翻译腔。
5. 单篇深查：`python3 .agents/skills/docs-translation/scripts/verify_mdx.py <源.md> <译文.mdx>`（逐项比对行内代码，并检查 MDX 不安全字符）。

## 工作流 C：接入新项目（复用本技能）

把整个技能目录复制到新文档仓库的 `.agents/skills/docs-translation/`，然后：

1. 编辑 `project.json`：填上游仓库/分支/文档目录、`site_root`（技能目录到站点仓库根的相对路径）、语言、扩展名映射，以及（如有）品牌资产例外与导航 tab 对照。
2. 在 `references/` 新建约束性 `terminology.md`（先写「保留英文」清单）与 `rules.md`（可从本项目改写），在 `state/` 新建空的 `batches.json`。
3. 首次翻译按工作流 B 全量或分批推进（每批约 9–12K 词，`pairs` 登记全部 src→dst）；完成后把所对的上游 commit 写入 `state/sync-state.json`。

## 步骤 3：全量校验（A/B 收尾必做）

```bash
python3 .agents/skills/docs-translation/scripts/verify_structure.py
```

自动从 `project.json` 取路径（可用环境变量 `SRC_DIR` / `DST_DIR` / `PAIRS_FILE` 覆盖）。比对每一对源/译文：frontmatter 键、各级标题数、代码围栏逐字节内容、列表项数、表格行数、JSX 标签数、链接目标、行内代码数。**必须全绿（exit 0）才算完成**，FAIL 逐条修到绿。结构校验抓不住散文措辞漂移——那要靠 A1 的基线 diff，所以 `state/sync-state.json` 是权威，不能跳过 A1。

## 步骤 4：收尾

1. 更新 `state/sync-state.json`：`last_synced_commit` 取 `NEW`，更新 `last_synced_date`。
2. 新增/删除/改名页面已登记进 `pairs` 与 `nav_file`。
3. **自动提交**：`git add -A && git commit`，把「校验绿 + 基线已更新」固化成一个原子提交。**不 push**——推送是对外动作，由用户决定。
4. 报告格式：每文件一行 `OK <路径>`；结尾列「待定术语」与不确定之处；不贴译文全文。

## 红线

- 术语表双向约束，**严禁现场发明译法**。
- 代码围栏（含注释）与行内代码**逐字节保留**，永不翻译、永不「顺手修正」。
- 译文不得引入裸 `{ } < >`（MDX 编译失败）；源文的 `\{`、`&lt;` 等转义原样保留。
- 同步时最小改动；翻译时不增删信息、不改结构。
- 未跑全量校验、或校验未全绿，不得宣布完成；完成后必须更新同步基线。
- 零侵入：不碰站点仓库中译文内容与技能目录以外的任何文件。
- 新项目必须先有 `project.json` + 术语表 + 规则，才能开始翻译。
