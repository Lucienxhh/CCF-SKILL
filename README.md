# CCF

查询 CCF 推荐期刊/会议评级和中科院分区的 Agent Skill。符合 [Agent Skills Specification](https://agentskills.io) 标准，兼容 Trae、Claude Code、Cursor、GitHub Copilot、Windsurf 等平台。

## 功能

| 类别 | 年份 | 说明 |
|------|------|------|
| CCF 国际期刊 | 2026 | A/B/C 评级 + 新锐分区 |
| CCF 中文期刊 | 2025 | T1/T2/T3 评级 |
| 中科院分区 | 2022, 2023, 2025 | 1-4 区 + TOP |
| 新锐分区 | 2026 | 1-4 区 + TOP |

**查询逻辑**：自动判断类型 → 期刊返回 CCF + 分区，会议仅返回 CCF

**引用解析**：自动从引用中提取期刊/会议名称和年份，年份未知时默认使用 2026

## 安装

将 `CCF` 文件夹复制到你的技能目录：

| 平台 | 项目级目录 | 用户级目录 |
|------|-----------|-----------|
| Trae | `.trae/skills/` | `~/.trae/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |
| GitHub Copilot | `.github/skills/` | `~/.copilot/skills/` |
| Windsurf | `.windsurf/skills/` | `~/.windsurf/skills/` |

## 使用

在支持的平台中，直接询问相关问题：

```
"TMC 是 CCF 什么级别？"
"计算机学报是 CCF 什么级别？"
"TPAMI 的中科院分区是多少？"
"TKDE 2025 年的分区是几区？"
"这篇论文是什么级别？[引用格式]..."
```

## 引用解析规则

当用户提供论文引用时，LLM 会自动提取：

1. **会议名称缩写**：从括号中提取（如 `ICSME`）或 `International Conference on` 前的会议全称
2. **期刊名称**：提取期刊缩写（如 `IEEE Robot. Autom. Lett.` → `IEEE Robotics and Automation Letters`）
3. **年份**：优先提取明确年份，**未知时默认 2026**

### 示例

| 引用来源 | 提取的 venue | 年份 |
|---------|-------------|------|
| `...IEEE International Conference on Software Maintenance and Evolution (ICSME), 2019...` | ICSME | 2019 |
| `...IEEE Robot. Autom. Lett. 3 (2018)...` | IEEE Robotics and Automation Letters | 2018 |
| `...Expert Syst. Appl. 166 (2021)...` | Expert Systems with Applications | 2021 |

## 命令行测试

```bash
# 通用查询（期刊返回 CCF + 分区）
python scripts/search.py TMC
python scripts/search.py TPAMI

# 指定年份的中科院分区
python scripts/search.py TKDE --zky 2025

# CCF 中文期刊
python scripts/search.py 计算机学报

# 引用解析
python scripts/search.py "[1] A. Barbez, et al. Deep learning anti-patterns, in: 2019 IEEE ICSME, 2019, pp. 114-124."
```

## 目录结构

```
CCF/
├── SKILL.md         # Skill 主文件
├── README.md        # 本文档
├── scripts/
│   ├── search.py    # 搜索脚本
│   └── parse.py     # 引用解析模块
├── data/
│   ├── CCF-2026-EN.md  # CCF 国际期刊/会议
│   ├── CCF-2025-CN.md  # CCF 中文期刊
│   ├── ZKY-2022.md     # 中科院分区 2022
│   ├── ZKY-2023.md     # 中科院分区 2023
│   ├── ZKY-2025.md     # 中科院分区 2025
│   └── XR-2026.md      # 新锐分区 2026
└── references/
    └── guide.md          # 详细使用指南
```

## 详细文档

详见 [references/guide.md](references/guide.md)。

## 许可证

本项目包含的数据来自公共来源。脚本代码可自由使用。
