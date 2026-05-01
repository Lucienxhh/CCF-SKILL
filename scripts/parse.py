"""
parse.py

引用解析工具，供 LLM 在处理复杂引用时调用。
仅支持两种标准格式的解析：GB/T 7714 和 BibTeX。
其他非标准格式，由 LLM 通过语义理解能力自行提取。

Usage:
    from parse import parse_citation

    result = parse_citation(text)  # 返回字典，包含 venue/name/year/format/success
    if result['success']:
        venue = result['venue']
        year = result['year']
"""

import re

def extract_year(text):
    """从文本中提取年份（4位数字）"""
    patterns = [
        r'\b(20\d{2}|19\d{2})\b',
        r'\((20\d{2}|19\d{2})\)',
        r',\s*(20\d{2}|19\d{2})\s*[,(]',
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)

    return None

def detect_format(text):
    """
    检测引用格式类型。

    Returns:
        str: 格式名称 ('bibtex', 'gb7714', 'unknown')
    """
    text_lower = text.lower().strip()

    if text_lower.startswith('@'):
        return 'bibtex'
    elif re.search(r'\[C\]|\[J\]', text):
        return 'gb7714'

    return 'unknown'

def get_format_name(text):
    """
    获取格式的中文名称。
    """
    fmt = detect_format(text)
    format_names = {
        'bibtex': 'BibTeX',
        'gb7714': 'GB/T 7714',
        'unknown': '未知格式'
    }
    return format_names.get(fmt, '未知格式')

def parse_bibtex(text):
    """解析 BibTeX 格式，提取会议/期刊缩写"""
    venue = None
    name = None

    patterns = [
        r'booktitle\s*=\s*\{([^}]+)\}',
        r'journal\s*=\s*\{([^}]+)\}',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            break

    if name:
        acronym_match = re.search(r'\(([A-Z]{2,})\)(?:\s*\d|,|$)', name)
        if acronym_match:
            venue = acronym_match.group(1)

    return venue, name

def parse_gb7714(text):
    """解析 GB/T 7714 格式，提取会议/期刊缩写"""
    venue = None
    name = None

    match = re.search(r'\[C\]\s*//\s*[^\[]+\s+([A-Z][^\[,]+?)\s*\(([A-Z]{2,})\)', text)
    if match:
        name = match.group(1).strip()
        venue = match.group(2).strip()
        return venue, name

    match = re.search(r'\(([A-Z]{2,})\)\.\s*\d+[,]\s*\d+', text)
    if match:
        venue = match.group(1).strip()
        return venue, name

    return venue, name

def parse_citation(citation):
    """
    解析引用文本，提取会议/期刊信息。

    Args:
        citation: 引用文本（仅支持 GB/T 7714 和 BibTeX 格式）

    Returns:
        dict: 包含以下键的字典：
            - venue: 会议/期刊缩写（用于搜索），可能为 None
            - name: 完整名称，可能为 None
            - year: 年份，可能为 None
            - format: 引用格式类型
            - success: 是否成功提取

    Example:
        >>> parse_citation("[C]// Proceedings of the IEEE International Conference on Software Analysis (SANER). 2016.")
        {'venue': 'SANER', 'name': None, 'year': '2016', 'format': 'GB/T 7714', 'success': True}

        >>> parse_citation("@inproceedings{SANER2016, booktitle={2016 IEEE... (ICSE)}}")
        {'venue': 'ICSE', 'name': None, 'year': None, 'format': 'BibTeX', 'success': True}
    """
    citation = citation.strip()

    fmt = detect_format(citation)
    year = extract_year(citation)

    if fmt == 'bibtex':
        venue, name = parse_bibtex(citation)
    elif fmt == 'gb7714':
        venue, name = parse_gb7714(citation)
    else:
        venue, name = None, None

    success = (venue is not None) or (name is not None)

    return {
        'venue': venue,
        'name': name,
        'year': year,
        'format': get_format_name(citation),
        'success': success
    }
