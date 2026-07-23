# 英汉化学化工词汇表

基于《英汉化学化工词汇（第五版）》的开源化学词汇数据集。

![可视化预览](asset/images/view.gif)

## 数据来源

| 项目 | 信息 |
|------|------|
| **书名** | 英汉化学化工词汇（第五版） |
| **出版社** | 科学出版社 |
| **编者** | 科学出版社名词室 |
| **ISBN** | 978-7-03-046913-7 |
| **出版年份** | 2016年 |
| **原始收词量** | 约 17.5 万条 |
| **本数据集** | **151,337 条**去重词汇 |

> 第五版相比2000年的第四版，删除了约2万条过时/边缘词汇，同时增补了约2万条新材料、化工、药物化学、生物化学、海洋化学、分析技术方向的新词。

## 数据集特点

- **大规模**：151,337 条中英文对照词汇，覆盖化学化工全领域
- **结构化**：每条词汇包含英文、中文释义，可选领域分类标签
- **多领域标注**：16 个化学子领域、57 个细分方向
- **多格式**：提供 JSON、CSV、TXT 等格式
- **完全免费**：MIT 许可证，可自由使用

## 数据结构

```
data/
├── glossary_all.json        # 完整词汇表（含领域分类）
├── glossary.json            # 完整词汇表（仅英文+中文）
├── glossary.csv             # CSV 格式，Excel 可直接打开
├── glossary.txt             # 纯文本，Tab 分隔
├── domains/                 # 按领域+子领域拆分
├── by_domain.json           # 按领域分组
└── statistics.json          # 统计信息
```

### 文件说明

#### glossary_all.json
完整数据集，151,337 条词汇，每条包含：
```json
{
  "en": "crystal",
  "zh": "晶体",
  "domains": [
    {"domain": "physical_chemistry", "sub_domain": "crystallography", "role": "primary", "confidence": 4.5}
  ]
}
```

#### glossary.json
精简版，仅保留英文和中文：
```json
{"en": "crystal", "zh": "晶体"}
```

#### glossary.csv
CSV 格式，两列（English, Chinese），可直接用 Excel 打开。

#### glossary.txt
纯文本格式，Tab 分隔，每行一条，方便 grep/awk 处理。

#### by_domain.json
按主领域分组，结构为 `{"领域名": [{"en":"...", "zh":"..."}]}`，适合按领域批量加载。

#### statistics.json
统计数据，包含总词汇数、来源信息、各领域词汇数量分布。

#### domains/ 目录
按领域+子领域拆分的 JSON 文件，每条包含 `en`、`zh`、`role`（primary/secondary）、`confidence`（置信度分数）。

```
domains/
├── organic_chemistry/        # 有机化学
│   ├── organic_synthesis.json
│   ├── organic_compounds.json
│   ├── natural_products.json
│   └── stereochemistry.json
├── inorganic_chemistry/      # 无机化学
│   ├── coordination.json
│   ├── main_group.json
│   ├── transition_metals.json
│   └── solid_state.json
├── physical_chemistry/       # 物理化学
│   ├── thermodynamics.json
│   ├── kinetics.json
│   ├── quantum_chemistry.json
│   ├── spectroscopy.json
│   ├── electrochemistry.json
│   ├── surface_science.json
│   ├── colloid_science.json
│   └── crystallography.json
├── analytical_chemistry/     # 分析化学
├── biochemistry/             # 生物化学
├── pharmaceutical_chemistry/ # 药物化学
├── chemical_engineering/     # 化工
├── materials_science/        # 材料科学
├── polymer_science/          # 高分子科学
├── environmental_science/    # 环境科学
├── food_science/             # 食品科学
├── geological_chemistry/     # 地球化学
├── nuclear_science/          # 核科学
└── general_chemistry/        # 通用化学
```

## 领域分类字段说明

每条词汇的 `domains` 字段结构如下：

```json
{
  "domain": "physical_chemistry",
  "sub_domain": "crystallography",
  "role": "primary",
  "confidence": 4.5
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `domain` | string | 一级领域，共 16 个（如 `organic_chemistry`、`chemical_engineering`） |
| `sub_domain` | string | 二级子领域，共 57 个（如 `crystallography`、`organic_synthesis`） |
| `role` | string | `primary` = 主要领域，`secondary` = 相关领域。一个词汇可同时属于多个领域 |
| `confidence` | number | 置信度分数，越高表示匹配越精确。阈值 ≥ 1.5 才会被收录 |

### 多领域映射示例

词汇 "catalyst"（催化剂）同时属于：
```json
[
  {"domain": "physical_chemistry", "sub_domain": "kinetics", "role": "primary"},
  {"domain": "catalysis", "sub_domain": "heterogeneous_catalysis", "role": "secondary"}
]
```

词汇 "polymer"（聚合物）同时属于：
```json
[
  {"domain": "polymer_science", "sub_domain": "polymer_synthesis", "role": "primary"},
  {"domain": "materials_science", "sub_domain": "composite_materials", "role": "secondary"},
  {"domain": "organic_chemistry", "sub_domain": "organic_synthesis", "role": "secondary"}
]
```

## 分类方法

本项目使用**基于化学领域本体库的关键词规则分类**。

### 分类流程

```
原始词汇 → 关键词匹配 → 正则模式匹配 → 部分匹配 → 置信度评分 → 多领域映射
```

### 三级匹配策略

1. **精确匹配**（+2.0 分）：词汇直接命中领域关键词库
   - 例：`crystallography` 命中 `crystallography` 关键词

2. **正则模式匹配**（+1.5 分）：识别化学术语特征模式
   - 例：`-ase` 后缀 → 酶类（biochemistry/enzymes）
   - 例：`-ene` 后缀 → 烯烃（organic_chemistry/organic_compounds）
   - 例：`Fe²⁺` → 过渡金属配合物（inorganic_chemistry/transition_metals）

3. **部分匹配**（+1.0 分）：词汇包含领域关键词
   - 例：`crystal` 包含在 `crystallization` 中

### 评分规则

- 每个 (domain, sub_domain) 组合独立计分
- 总分 ≥ 1.5 才会被收录到该领域
- 得分最高的标记为 `primary`，其余为 `secondary`
- 最多返回 3 个领域，按分数排序
- 无任何匹配的词汇归入 `general_chemistry`

### 本体库规模

| 指标 | 数值 |
|------|------|
| 覆盖领域 | 16 个一级领域 |
| 细分方向 | 57 个子领域 |
| 关键词总数 | ~2,000+ 个 |
| 正则模式 | ~150+ 条 |
| 分类速度 | 151K 条 / 68 秒 |

## 领域分布

| 领域 | 英文 | 词汇数量 |
|------|------|----------|
| 有机化学 | organic_chemistry | 17,342 |
| 无机化学 | inorganic_chemistry | 20,312 |
| 物理化学 | physical_chemistry | 15,865 |
| 分析化学 | analytical_chemistry | 6,914 |
| 生物化学 | biochemistry | 3,170 |
| 药物化学 | pharmaceutical_chemistry | 4,322 |
| 化工 | chemical_engineering | 9,386 |
| 材料科学 | materials_science | 6,661 |
| 高分子科学 | polymer_science | 4,400 |
| 环境科学 | environmental_science | 21,266 |
| 食品科学 | food_science | 2,072 |
| 地球化学 | geological_chemistry | 3,817 |
| 核科学 | nuclear_science | 548 |
| 染料颜料 | dye_pigment | 925 |
| 催化 | catalysis | 613 |
| 通用化学 | general_chemistry | 93,393 |

## 可视化查词典

项目内置一个可视化页面，支持搜索过滤、领域筛选、动画效果。

### 启动方式

```bash
cd chemical-glossary
python scripts_internal/run.py
```

自动打开浏览器访问 http://localhost:7888 ，按 `Ctrl+C` 停止。

> 端口 7888 被占用时会自动切换到下一个可用端口。

### 功能

- 搜索框输入英文或中文实时过滤词汇
- 点击领域标签按化学子领域筛选
- 悬停词条查看领域分类信息
- 滚动加载，支持 151K 条流畅浏览

## 使用场景

- NLP/机器学习：化学领域词嵌入、命名实体识别训练数据
- 翻译工具：化学术语翻译参考
- 搜索引擎：化学词汇检索增强
- 教育工具：化学词汇学习应用
- 知识图谱：构建化学领域知识图谱的实体库
- LLM 增强：化学领域 RAG 知识库

## 许可证

MIT License - 可自由使用、修改和分发。

## 致谢

数据来源于《英汉化学化工词汇（第五版）》（科学出版社，2016），本项目仅用于学术研究和教育目的。
