# CCF-Lookup 详细指南

## 目录结构

```
ccf-lookup/
├── SKILL.md              # Skill 主文件（AI Agent 读取）
├── README.md             # 人类可读的说明
├── scripts/              # 可执行脚本
│   └── search.py         # 搜索脚本
├── data/                 # 数据文件
│   ├── CCF.md            # CCF 国际期刊/会议列表
│   ├── CCF-2025-CN.md    # CCF 中文期刊列表
│   ├── XR-2022.md        # 中科院分区 2022
│   ├── XR-2023.md        # 中科院分区 2023
│   ├── XR-2025.md        # 中科院分区 2025
│   └── XR-2026.md        # 中科院分区 2026（默认）
└── references/           # 参考文档
    └── guide.md          # 本文档
```

## 命令行用法

### 基本语法

```bash
python scripts/search.py <query> [--mode] [year]
```

### CCF 国际期刊/会议

```bash
# 查询简称
python scripts/search.py TMC

# 查询全称
python scripts/search.py "IEEE Transactions on Mobile Computing"

# 查询会议
python scripts/search.py SC
```

### CCF 中文期刊

```bash
python scripts/search.py "计算机学报" --cn
python scripts/search.py "软件学报" --cn
```

### 中科院分区

```bash
# 默认 2026 年
python scripts/search.py TPAMI --zky

# 指定年份
python scripts/search.py TKDE --zky 2025
python scripts/search.py TVCG --zky 2023
python scripts/search.py TSE --zky 2022
```

### 支持的年份

中科院分区支持的年份：
- 2022
- 2023
- 2025
- 2026（默认）

## API 输出格式

### CCF 国际期刊/会议

```json
[
  {
    "简称": "TMC",
    "全称": "IEEE Transactions on Mobile Computing",
    "评级": "A",
    "类型": "期刊"
  }
]
```

### CCF 中文期刊

```json
[
  {
    "中文名称": "计算机学报",
    "英文名称": "-",
    "评级": "T1",
    "语种": "中文"
  }
]
```

### 中科院分区

```json
[
  {
    "期刊名称": "IEEE TRANSACTIONS ON PATTERN ANALYSIS AND MACHINE INTELLIGENCE",
    "大类分区": "1区",
    "小类分区": "1区",
    "学科范畴": "计算机：人工智能",
    "是否TOP期刊": "是",
    "年份": 2026
  }
]
```

## 数据格式说明

### CCF.md

国际期刊/会议表格格式：
```
| 简称 | 全称 | 评级 | 类型 |
|------|------|------|------|
| TMC  | IEEE Transactions on Mobile Computing | A | 期刊 |
```

### CCF-2025-CN.md

中文期刊表格格式：
```
| 期刊中文名称 | 英文名称 | 评级 | 语种 |
|-------------|---------|------|------|
| 计算机学报  | -       | T1   | 中文 |
```

### XR-{year}.md

中科院分区表格格式：
```
| 期刊名称 | 大类分区 | 小类分区 | 学科范畴 | 是否TOP期刊 |
|---------|---------|---------|---------|------------|
| TPAMI   | 1区     | 1区     | 计算机：人工智能 | 是 |
```

## 更新数据

如需更新数据：
1. 将新的 `.md` 文件放入 `data/` 目录
2. 更新 `search.py` 中的默认年份（如果需要）
3. 测试查询是否正常工作

## 常见问题

**Q: 为什么找不到某个期刊？**
A: 可能是数据文件中没有收录，或者名称不匹配。尝试使用全称或更精确的关键词。

**Q: 如何添加新的年份数据？**
A: 将新年份的分区文件命名为 `XR-{year}.md` 放入 `data/` 目录，然后在 `search.py` 中更新年份列表即可。

**Q: 支持哪些平台？**
A: 符合 Agent Skills 规范，支持 Trae、Claude Code、Cursor、GitHub Copilot、Windsurf 等平台。
