---
name: CCF
description: 查询 CCF 推荐期刊/会议评级(A/B/C/T1/T2/T3)和中科院/新锐分区(1-4区/TOP)。当用户询问期刊/会议的评级、分区或排名时调用。
---

# CCF Skill

当用户询问以下问题时使用此 skill：
- 查询期刊/会议的 CCF 评级
- 查询期刊的中科院分区或新锐分区
- 查询某期刊/会议属于几区、什么级别
- 用户提供了论文引用，需要判断其级别

## 数据源

| 数据源 | 说明 |
|--------|------|
| CCF-2026-EN.md | CCF 国际期刊/会议（A/B/C 级） |
| CCF-2025-CN.md | CCF 中文期刊（T1/T2/T3 级） |
| ZKY-*.md | 中科院分区（2022/2023/2025） |
| XR-2026.md | 新锐分区（2026） |

## 搜索命令

```bash
python scripts/search.py <关键词>
```

**一次查完，LLM 自行过滤：**
- 会议 → 忽略 zky_* 结果（会议没有分区）
- 期刊 → 使用 zky_* 结果

## LLM 理解职责

**search.py 只做简单字符串匹配，语义理解由 LLM 负责：**

### 1. 名称理解与转换

LLM 应能理解以下等价形式：

| 用户输入 | 应查询的关键词 |
|----------|----------------|
| TMC | TMC |
| IEEE Transactions on Mobile Computing | Mobile Computing |
| 移动计算 | Mobile Computing |
| 计算机学报 | 计算机学报 |
| TPAMI | TPAMI |
| Pattern Analysis and Machine Intelligence | Pattern Analysis |

**常用期刊缩写映射（LLM 应掌握）：**

| 缩写 | 全称 |
|------|------|
| TMC | IEEE Transactions on Mobile Computing |
| TPAMI | IEEE Transactions on Pattern Analysis and Machine Intelligence |
| TKDE | IEEE Transactions on Knowledge and Data Engineering |
| TSE | IEEE Transactions on Software Engineering |
| TOS | ACM Transactions on Storage |
| TOCS | ACM Transactions on Computer Systems |
| TOSEM | ACM Transactions on Software Engineering and Methodology |
| ICSE | International Conference on Software Engineering |
| FSE | ACM SIGSOFT International Symposium on the Foundations of Software Engineering |
| ASE | IEEE/ACM International Conference on Automated Software Engineering |
| ISSTA | International Symposium on Software Testing and Analysis |

### 2. 引用解析

从论文引用中提取期刊/会议信息：

**会议引用特征：**
- `in: ... Conference ... (XXX)`
- `Proceedings of the ... (XXX)`
- `XXX 2023, pp.`（XXX 是会议缩写）

**期刊引用特征：**
- `IEEE Robot. Autom. Lett.`
- `Expert Syst. Appl.`
- 卷号+年份：`166 (2021)`

**提取步骤：**
1. 识别是会议还是期刊
2. 提取缩写或全称
3. 提取年份（可选）
4. 用提取的关键词调用 search.py

### 3. 返回结果解读

search.py 返回格式示例：

```json
{
  "query": "TMC",
  "results": {
    "ccf_en": [["", "TMC", "IEEE Transactions on Mobile Computing", "A", "期刊"]],
    "ccf_cn": [],
    "zky_2026": [["", "IEEE Transactions on Mobile Computing", "1区", "TOP", "计算机科学"]]
  },
  "found": true
}
```

**LLM 应解读为：**
- CCF 评级：A
- 类型：期刊
- 新锐分区：1区 TOP
- 完整名称：IEEE Transactions on Mobile Computing

### 4. 响应格式

直接向用户返回简洁结论：

```
TMC (IEEE Transactions on Mobile Computing)
- CCF 评级：A
- 类型：期刊
- 新锐分区：1区 TOP（2026）
```

如果未找到结果：
```
未找到相关期刊/会议信息。请确认名称是否正确，或提供论文引用以便提取信息。
```

## 注意事项

1. **搜索是模糊的**：search.py 使用包含匹配，查询 "Mobile" 会匹配 "IEEE Transactions on Mobile Computing"
2. **分区仅适用于期刊**：会议没有中科院/新锐分区
3. **年份默认 2026**：分区查询默认使用最新年份
4. **中文期刊独立数据源**：中文期刊（如计算机学报）需查询 CCF-2025-CN.md

## 命令行测试

```bash
# 查询国际期刊
python scripts/search.py TMC
python scripts/search.py "Pattern Analysis"

# 查询中文期刊
python scripts/search.py 计算机学报
python scripts/search.py 软件学报

# 查询会议
python scripts/search.py ICSE
python scripts/search.py FSE
```