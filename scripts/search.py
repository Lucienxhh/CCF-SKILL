import sys
import json
import os

# 数据文件常量
CCF_EN_FILE = "CCF-2026-EN.md"
CCF_CN_FILE = "CCF-2025-CN.md"
ZKY_FILES = ["ZKY-2025.md", "ZKY-2023.md", "ZKY-2022.md"]
XR_FILES = ["XR-2026.md"]

def get_data_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    return os.path.join(skill_dir, "data", filename)

def search_in_file(filepath, query):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []

    results = []
    query_lower = query.lower().strip()

    for line in lines:
        line = line.strip()
        if not line or '------' in line or line.startswith('#'):
            continue

        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 3:
            continue

        row_text = ' '.join(parts).lower()
        if query_lower in row_text or query_lower in parts[0].lower():
            results.append(parts)

    return results

def search_ccf_en(query):
    filepath = get_data_path(CCF_EN_FILE)
    return search_in_file(filepath, query)

def search_ccf_cn(query):
    filepath = get_data_path(CCF_CN_FILE)
    return search_in_file(filepath, query)

def search_fq(query):
    results = {}

    # 搜索新锐分区
    for filename in XR_FILES:
        filepath = get_data_path(filename)
        key = filename.replace(".md", "").lower()
        results[key] = search_in_file(filepath, query)

    # 搜索中科院分区
    for filename in ZKY_FILES:
        filepath = get_data_path(filename)
        key = filename.replace(".md", "").lower()
        results[key] = search_in_file(filepath, query)

    return results

def is_journal(ccf_result):
    if not ccf_result:
        return False
    for item in ccf_result:
        if len(item) > 4 and "期刊" in item[4]:
            return True
    return False

def search(query):
    results = {}

    ccf_en = search_ccf_en(query)
    if ccf_en:
        results["ccf_en"] = ccf_en
        if is_journal(ccf_en):
            results.update(search_fq(query))
        return results

    ccf_cn = search_ccf_cn(query)
    if ccf_cn:
        results["ccf_cn"] = ccf_cn
        results.update(search_fq(query))
        return results

    results.update(search_fq(query))
    return results

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: python search.py <query>"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    query = sys.argv[1]
    results = search(query)

    if not any(results.values()):
        print(json.dumps({"query": query, "results": {}, "found": False}, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({"query": query, "results": results, "found": True}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
