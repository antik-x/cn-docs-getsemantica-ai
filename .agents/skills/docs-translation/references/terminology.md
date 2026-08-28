# Semantica 中文文档术语表（约束性）

> 本表对所有翻译任务**双向约束**：表中词出现时必须按指定译法渲染；表中没有、且无可引用的中文技术社区先例的术语，保留英文并在任务报告中列入「待定术语」。**严禁现场发明译法。**

## 1. 保留英文（永不翻译）

- **产品与品牌**：Semantica、Knowledge Explorer（首次出现标注「Knowledge Explorer（知识探索器）」，后文可直接用「知识探索器」）、Semantica CLI
- **公司/生态产品**：OpenAI、Anthropic、Groq、HuggingFace、Novita AI、LiteLLM、LangChain、LlamaIndex、CrewAI、Agno、Docling、Snowflake、Databricks、pgvector、Apache AGE、PostgreSQL、Kafka、RSS、Git、GitHub、Discord、Jupyter、Docker、PyPI、pip、uv
- **技术缩写**（首次出现按第 3 节标注中文）：LLM、RAG、GraphRAG、MCP、NER、RDF、OWL、SHACL、SPARQL、JSON、YAML、CSV、XML、API、CLI、SDK、URL、CRUD、CVE、MIT、REST
- **代码身份**：一切类名（ContextGraph、VectorStore、ProvenanceManager、NERExtractor、RelationExtractor、GraphBuilder、TemporalVersionManager…）、函数/方法名、参数名、模块名、包名、文件路径、命令行、环境变量、配置键——**逐字节保留**
- **Schema** 一词保留英文（作普通名词时也保留，不译作「模式」）
- Token、Embedding 在代码/参数语境保留原文

## 2. 术语对照（EN → 简中）

| English | 中文 |
|---|---|
| accountability | 问责 |
| accuracy | 准确率 |
| agent | 智能体 |
| agent memory | 智能体记忆 |
| analytics | 分析 |
| anchor (entity) | 锚点实体 |
| approach / methodology | 方法 |
| audit trail | 审计追踪 |
| backend | 后端 |
| cache | 缓存 |
| change management | 变更管理 |
| chunk / chunking | 分块 / 文本块（chunk 作名词指「文本块」，chunking 指「分块」） |
| confidence | 置信度 |
| conflict detection & resolution | 冲突检测与解决 |
| context graph | 上下文图谱 |
| context window | 上下文窗口 |
| coreference resolution | 指代消解 |
| data lineage | 数据血缘 |
| decision intelligence | 决策智能 |
| deduplication | 去重 |
| dependency | 依赖 |
| edge | 边 |
| embedding | 嵌入（Embedding） |
| entity | 实体 |
| entity merging | 实体合并 |
| entity resolution | 实体消解 |
| evaluation / evals | 评估 |
| explainability | 可解释性 |
| export & serialization | 导出与序列化 |
| extraction / extract | 抽取 / 抽取 |
| fact | 事实 |
| feed | 订阅源 |
| graph analytics | 图分析 |
| graph store | 图存储 |
| ground truth | 基准真值 |
| ingestion / ingest | 摄取 |
| ingestion pipeline | 摄取流水线 |
| inference | 推断（与 reasoning「推理」区分；「Reasoning & Inference」译「推理与推断」） |
| knowledge graph | 知识图谱 |
| lazy loading | 懒加载 |
| lifecycle | 生命周期 |
| metadata | 元数据 |
| module | 模块 |
| multi-agent system | 多智能体系统 |
| node | 节点 |
| normalization / normalize | 规范化 |
| observability | 可观测性 |
| ontology | 本体 |
| open source | 开源 |
| parse | 解析 |
| pipeline | 流水线 |
| plugin | 插件 |
| policy engine | 策略引擎 |
| production | 生产环境 |
| prompt | 提示词 |
| property | 属性 |
| provenance | 溯源 |
| quad | 四元组 |
| query | 查询 |
| RAG / retrieval-augmented generation | 检索增强生成（RAG） |
| reasoning | 推理 |
| relation | 关系 |
| relation extraction | 关系抽取 |
| retrieve / retrieval | 检索 |
| rule | 规则 |
| schema | Schema（保留） |
| seed data | 种子数据 |
| semantic extraction | 语义抽取 |
| semantic layer | 语义层 |
| split | 切分 |
| stream / streaming | 流 / 流式 |
| temporal | 时序 |
| temporal intelligence | 时序智能 |
| threat actor | 威胁行为者 |
| threat intelligence | 威胁情报 |
| tool | 工具 |
| triplet / triple | 三元组 |
| triplet store | 三元组存储 |
| trust | 信任 |
| use case | 使用场景 |
| validation | 校验 |
| versioning | 版本管理 |
| visualization | 可视化 |
| workflow | 工作流 |
| zero trust | 零信任 |
| access control | 访问控制 |
| vector store | 向量存储 |
| vector database | 向量数据库 |
| distance intelligence | 距离智能 |
| knowledge explorer | 知识探索器（Knowledge Explorer） |
| store (n.) | 存储 |
| framework | 框架 |
| limit | 上限 |
| overhead | 开销 |
| precision | 精确率 |
| recall | 召回率 |
| F1 (score) | F1（保留） |
| reification | 具体化（Reification） |
| named graph | 具名图 |
| fail closed | 失败关闭（fail closed） |
| air-gapped | 物理隔离（air-gapped） |
| runbook | 运行手册（runbook） |
| gated (model) | 受限（gated） |
| CTI | CTI（网络威胁情报，缩写保留；首现可写「网络威胁情报（CTI）」） |
| ego(-mode) | Ego（保留，如「Ego 模式」） |
| blocking (record linkage) | Blocking（保留，记录连接术语，勿与 chunking 混译） |
| Cookbook（页面名） | 实战手册（全站统一：导航 Tab、页面标题、链接文字均用「实战手册」） |

## 3. 首次出现中英对照（first occurrence）

核心概念术语**在每篇文档首次出现时**采用「中文（English）」格式，其后用纯中文：

- 溯源（Provenance）、知识图谱（Knowledge Graph）、上下文图谱（Context Graph）、本体（Ontology）、三元组（Triplet）、嵌入（Embedding）、检索增强生成（RAG）、大语言模型（LLM）、模型上下文协议（MCP）、命名实体识别（NER）、图增强检索（GraphRAG，可仅首次释为「GraphRAG（Graph-Augmented Retrieval，图增强检索）」）

标题（H1-H3、frontmatter title、导航名）中**不加**英文对照（保持简短）；正文首现才加。

## 4. 品牌标语（全站统一）

- "The Accountability and Context Layer for AI: Context Graphs · Decision Intelligence · Full Provenance"
  → 「面向 AI 的问责与上下文层：上下文图谱 · 决策智能 · 全链路溯源」

## 5. 模块名处理

Semantica 的模块（Ingest、Parse、Split、Normalize、Embeddings、ContextGraph、KnowledgeGraph、Temporal、Distance、SemanticExtract、Reasoning、Ontology、VectorStore、GraphStore、TripletStore、Deduplication、Conflicts、Provenance、ChangeManagement、Export、Visualization、Explorer、LLMs、Seed、Evals、Utils、Core、MCP Server）是**代码身份**：行内代码与代码块中逐字节保留；行文中模块名保留英文（如「Ingest 模块」），模块的**功能描述**用中文（如「摄取模块负责……」可写作「Ingest 模块负责……」）。
