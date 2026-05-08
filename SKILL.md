---
name: CCF
summary: 查询 CCF 推荐期刊/会议等级，以及中科院和新锐分区。
description: 查询期刊或会议的 CCF 等级（A/B/C/T1/T2/T3）与中科院/新锐分区（1-4区/TOP）。支持缩写、全称、中文名称和论文引用解析。
---

# Purpose

本 skill 用于查询：

- CCF 国际会议/期刊等级
- CCF 中文期刊等级
- 中科院分区
- 新锐分区

支持：

- 缩写查询
- 全称查询
- 中文名称查询
- 论文引用解析

---

# When To Use

当用户：

- 询问期刊或会议级别
- 询问中科院分区
- 询问"几区"
- 询问"TOP 吗"
- 提供论文引用并询问等级

时使用本 skill。

---

# Workflow

严格按以下流程执行：

1. 提取 venue 名称
2. 判断是：
   - 期刊
   - 会议
3. 调用 search.py
4. 解析 JSON
5. 格式化结果
6. 返回最终答案

如果输入是论文引用：

1. 提取 venue
2. 提取年份（可选）
3. 再执行搜索

---

# Command

```bash
python scripts/search.py "<query>"
```

query 可以是：

- 缩写
- 全称
- 中文名称
- 论文引用

---

# Tool Contract

search.py 返回 JSON：

```json
{
  "query": "TMC",
  "normalized_query": "IEEE Transactions on Mobile Computing",
  "match_type": "abbreviation",
  "found": true,
  "results": {
    "ccf": [],
    "partition": []
  }
}
```

---

# Result Interpretation

## ccf

```json
{
  "source": "CCF-2026-EN",
  "short_name": "TMC",
  "full_name": "IEEE Transactions on Mobile Computing",
  "rank": "A",
  "category": "期刊"
}
```

## partition

```json
{
  "source": "ZKY-2025",
  "name": "IEEE Transactions on Mobile Computing",
  "zone": "1区",
  "top": true,
  "field": "计算机科学"
}
```

---

# Response Policy

直接返回简洁结果。

示例：

```text
TMC (IEEE Transactions on Mobile Computing)

- CCF：A
- 类型：期刊
- 中科院分区：1区 TOP（2025）
```

会议不要返回分区。

---

# Failure Policy

如果 found=false：

按以下顺序重试：

1. 去掉标点
2. 尝试缩写
3. 尝试全称
4. 尝试引用解析

若仍失败：

```text
未找到相关期刊或会议信息，请提供更完整名称或论文引用。
```

不要编造结果。

---

# Constraints

- 会议没有中科院分区
- 默认优先使用最新分区数据
- search.py 只负责字符串匹配
- 不要假设模糊匹配一定正确
- 多结果时优先完全匹配
- 不要返回未经确认的结果

---

# Examples

## Query

```text
TPAMI 是什么级别？
```

## Response

```text
TPAMI (IEEE Transactions on Pattern Analysis and Machine Intelligence)

- CCF：A
- 类型：期刊
- 中科院分区：1区 TOP（2025）
```
