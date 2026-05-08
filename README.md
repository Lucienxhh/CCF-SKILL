# CCF Skill

查询 CCF 推荐期刊/会议等级，以及中科院和新锐分区。

## 项目结构

```
.
├── data/                      # 数据文件
│   ├── CCF-2026-EN.md        # CCF 国际期刊/会议推荐列表
│   ├── CCF-2025-CN.md        # CCF 中文期刊推荐列表
│   ├── ZKY-2025.md           # 中科院分区 2025
│   ├── ZKY-2023.md           # 中科院分区 2023
│   ├── ZKY-2022.md           # 中科院分区 2022
│   └── XR-2026.md            # 新锐分区 2026
├── scripts/
│   └── search.py             # 查询脚本
├── SKILL.md                  # Agent Runtime Policy（LLM 指令）
└── README.md                 # 开发者文档
```

## 快速开始

### 安装依赖

无需额外依赖，仅使用 Python 标准库。

### 运行查询

```bash
python scripts/search.py "TMC"
```

### 输出格式

```json
{
  "query": "TMC",
  "normalized_query": "IEEE Transactions on Mobile Computing",
  "match_type": "abbreviation",
  "found": true,
  "results": {
    "ccf": [...],
    "partition": [...]
  }
}
```

## 数据文件格式

所有数据文件均为 Markdown 表格格式，位于 `data/` 目录。

### CCF 数据格式

| 简称 | 全称 | 等级 | 类型 |
|------|------|------|------|
| TMC | IEEE Transactions on Mobile Computing | A | 期刊 |

### 分区数据格式

| 期刊名称 | 大类分区 | 小类分区 | 学科范畴 | 是否TOP |
|----------|----------|----------|----------|---------|
| IEEE Transactions on Mobile Computing | 1区 | 1区 | 计算机：信息系统 | 是 |

## 开发指南

### 添加新的缩写映射

编辑 `search.py` 中的 `ABBREVIATIONS` 字典：

```python
ABBREVIATIONS = {
    "TMC": "IEEE Transactions on Mobile Computing",
    # 添加新的缩写
}
```

### 添加新的数据文件

1. 将文件放入 `data/` 目录
2. 更新 `search.py` 中的文件常量：
   - `ZKY_FILES` 用于中科院分区
   - `XR_FILES` 用于新锐分区

### 修改输出 Schema

`search.py` 返回的 JSON Schema 定义如下：

```python
{
    "query": str,                    # 原始查询
    "normalized_query": str,         # 规范化后的查询
    "match_type": str,               # 匹配类型: abbreviation/raw
    "found": bool,                   # 是否找到结果
    "results": {
        "ccf": List[Dict],           # CCF 结果列表
        "partition": List[Dict]      # 分区结果列表
    }
}
```

## 数据来源

- CCF 推荐列表：https://www.ccf.org.cn/
- 中科院分区：https://www.fenqubiao.com/

## 协议

MIT
