import sys
import json
import os

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
    filepath = get_data_path("CCF-2026-EN.md")
    return search_in_file(filepath, query)

def search_ccf_cn(query):
    filepath = get_data_path("CCF-2025-CN.md")
    return search_in_file(filepath, query)

def search_zky(query, year=None):
    if year:
        filepath = get_data_path(f"ZKY-{year}.md")
    else:
        filepath = get_data_path("XR-2026.md")
    return search_in_file(filepath, query)

def is_journal(ccf_result):
    if not ccf_result:
        return False
    for item in ccf_result:
        if len(item) > 4 and "期刊" in item[4]:
            return True
    return False

def add_zky_results(results, query):
    results["zky_2026"] = search_zky(query, None)
    results["zky_2025"] = search_zky(query, 2025)
    results["zky_2023"] = search_zky(query, 2023)
    results["zky_2022"] = search_zky(query, 2022)

def search(query):
    results = {}

    ccf_en = search_ccf_en(query)
    if ccf_en:
        results["ccf_en"] = ccf_en
        if is_journal(ccf_en):
            add_zky_results(results, query)
        return results

    ccf_cn = search_ccf_cn(query)
    if ccf_cn:
        results["ccf_cn"] = ccf_cn
        add_zky_results(results, query)
        return results

    add_zky_results(results, query)
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