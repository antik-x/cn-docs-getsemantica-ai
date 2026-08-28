# Semantica 中文文档

Semantica 官方文档（[docs.getsemantica.ai](https://docs.getsemantica.ai/)）的简体中文版，基于 [Mintlify](https://mintlify.com) 构建，与英文源站结构、URL 一一对应。

- **英文源**：[semantica-agi/semantica](https://github.com/semantica-agi/semantica) 仓库 `docs/` 目录（MIT License）
- **覆盖范围**：全部 82 篇文档 —— 线上发布的 79 篇，外加仓库中 3 篇未发布的隐藏页（`changelog`、`storage-backends`、`migration/kg-provenance-tracker`）
- **翻译原则**：信达雅；结构与源文逐项锁定（标题层级、列表、表格、JSX 组件）；代码块（含注释）字节级原样保留；术语遵循统一术语表

## 本地开发

```bash
npm i -g mint
mint dev        # 本地预览 http://localhost:3000
```

## 校验

```bash
cd ..
python3 translation/verify_structure.py   # 与英文源逐篇比对结构一致性
```

## 目录约定

- 页面为 `.mdx`（MDX），路径与英文源 `.md` 一一对应（如 `docs/guides/graphrag.md` → `guides/graphrag.mdx`）
- 导航、分组与 Tab 结构见 `docs.json`（已译为中文）
- 品牌资产（logo、示意图、custom.css）复刻自官方站点 `assets/`

## 翻译工程文件

位于仓库上层的 `../translation/`：

- `terminology.md` —— 术语表（约束性，含保留英文清单与首现对照规则）
- `rules.md` —— 翻译规则摘要
- `batches.json` —— 翻译批次清单
- `verify_structure.py` —— 结构一致性校验器

## License

文档内容遵循上游项目的 [MIT License](LICENSE)。
