# 文档项目说明（中文版）

- 本项目是 Semantica 官方文档的简体中文版，基于 [Mintlify](https://mintlify.com) 构建
- 页面为 MDX 文件（YAML frontmatter + 正文），配置在 `docs.json`
- 英文源：`github.com/semantica-agi/semantica` 仓库 `docs/` 目录；文件路径一一对应（源 `.md` → 本站 `.mdx`）

## 术语

术语表是唯一权威：见 `../translation/terminology.md`。要点：

- 保留英文：Semantica、模块名（Ingest、ContextGraph…）、类/函数/参数、已成标准的技术词（GraphRAG、MCP、SHACL、pgvector、LLM、RAG…）
- 核心概念在正文首次出现用「中文（English）」，标题不加对照
- reasoning → 推理，inference → 推断；Cookbook → 实战手册；runbook → 运行手册；fail closed → 失败关闭
- 未收录且无中文社区先例的术语保留英文

## 风格约定

- 第二人称「你」，主动语态，一句一个意思
- 全角标点（，。；：？！）；中文与英文/数字之间加一个空格
- 粗体用于 UI 元素与关键概念：点击 **Settings**
- 文件名、命令、路径、代码标识一律行内代码

## 内容边界（翻译时）

- 忠实源文：不增删信息、不改结构（标题层级/列表/表格/JSX 组件数量必须与源文一致）
- 代码块（含注释）字节级保留；链接 URL/锚点原样，链接文字翻译
- 修改译文后运行 `python3 ../translation/verify_structure.py` 校验
