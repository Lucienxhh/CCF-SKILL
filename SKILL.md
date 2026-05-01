---
name: CCF
description: 查询 CCF 推荐期刊/会议评级(A/B/C 或 T1/T2/T3)和中科院/新锐分区(1-4区/TOP)。当用户询问期刊/会议的评级、分区或排名时调用。
---

# CCF

查询 CCF 推荐期刊/会议评级和中科院分区的 Skill。

## When to Use

当用户询问以下问题时使用此 skill：
- "TMC 是 CCF 什么级别？"
- "计算机学报是 CCF 什么级别？"
- "TPAMI 的中科院分区是多少？"
- "TKDE 2025 年的分区是几区？"
- 查询某个期刊/会议的 CCF 评级
- 查询某个期刊的中科院分区或 TOP 状态
- 用户提供了论文引用，需要查询其 CCF 评级

## 引用解析规则

### 提取顺序

从引用中**按顺序**尝试提取以下信息：

1. **会议名称缩写**（常见格式：`in: 2019 IEEE International Conference on Software Maintenance and Evolution (ICSME)`）
   - 提取括号中的会议缩写（如 `ICSME`）
   - 提取 `International Conference on` 或类似关键词前的会议全称

2. **期刊名称**（常见格式：`IEEE Robot. Autom. Lett.`、`Expert Syst. Appl.`）
   - 提取期刊缩写或全称
   - 注意：带点缩写如 `Robot. Autom. Lett.` 需识别为 `IEEE Robotics and Automation Letters`

3. **年份**
   - 优先提取明确的年份（如 `2019`、`2021`）
   - **如果年份未知或无法确定，默认使用 2026 年**

### 典型引用格式解析示例

#### 会议引用
```
[1] A. Barbez, F. Khomh, Y.-G. Guéhéneuc, Deep learning anti-patterns from code metrics history,
in: 2019 IEEE International Conference on Software Maintenance and Evolution (ICSME), 2019, pp. 114–124.
```
- **会议缩写**：`ICSME`
- **会议全称**：`IEEE International Conference on Software Maintenance and Evolution`
- **年份**：`2019`

#### 期刊引用（带 DOI）
```
[2] D. Bobkov, S. Chen, R. Jian, M.Z. Iqbal, E. Steinbach, Noise-resistant deep learning for object
classification in three-dimensional point clouds using a point pair descriptor, IEEE Robot. Autom. Lett.
3 (2018) 865–872, https://doi.org/10.1109/LRA.2018.2792681.
```
- **期刊缩写**：`IEEE Robot. Autom. Lett.` → `IEEE Robotics and Automation Letters`
- **期刊全称**：`IEEE Robotics and Automation Letters`
- **年份**：`2018`

```
[4] S. Boutaib, S. Bechikh, F. Palomba, M. Elarbi, M. Makhlouf, L.B. Said, Code smell detection and
identification in imbalanced environments, Expert Syst. Appl. 166 (2021) 114076.
```
- **期刊缩写**：`Expert Syst. Appl.` → `Expert Systems with Applications`
- **年份**：`2021`

#### 书籍章节引用
```
[3] M. Boussaa, W. Kessentini, M. Kessentini, S. Bechikh, S. Ben Chikha, Competitive coevolutionary
code-smells detection, in: G. Ruhe, Y. Zhang (Eds.), Search Based Software Engineering,
Springer Berlin Heidelberg, Berlin, Heidelberg, 2013, pp. 50–65.
```
- **出版社/会议**：`Springer`（书籍章节，非 CCF 评级对象）
- **年份**：`2013`

### 默认值规则

| 字段 | 默认值 | 触发条件 |
|------|--------|----------|
| 年份 | **2026** | 无法从引用中确定具体年份时 |

## 查询逻辑

| 类型 | 查询方式 | 返回信息 |
|------|----------|----------|
| 期刊 | `search.py <简称>` | CCF 评级 + 中科院/新锐分区 |
| 会议 | `search.py <简称>` | CCF 评级 |
| 引用解析 | LLM 提取 venue/year，再用 `search.py` 查询 | CCF 评级和分区 |

## Instructions

### 步骤一：解析引用

从引用文本中提取：
- **venue**：会议缩写或期刊缩写/全称
- **year**：年份（未知时使用默认值 2026）

### 步骤二：查询 CCF 评级

```bash
# 用 venue 查询（无年份）
python scripts/search.py <venue>

# 用 venue 查询（指定年份）
python scripts/search.py <venue> --zky <year>
```

### 步骤三：返回结果

返回该期刊/会议的：
- CCF 评级（A/B/C 或 T1/T2/T3）
- 中科院分区（1-4区/TOP，2026年新锐分区）
