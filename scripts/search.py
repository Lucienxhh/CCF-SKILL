import sys
import json
import os

def get_data_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    return os.path.join(skill_dir, "data", filename)

def search_ccf_en(query):
    ccf_file = get_data_path("CCF-2026-EN.md")

    try:
        with open(ccf_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []

    results = []
    query_lower = query.lower().strip()

    for line in lines:
        line = line.strip()
        if not line or (line.startswith('|') and '------' in line):
            continue
        if line.startswith('简称'):
            continue

        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 5:
            continue

        abbr = parts[1]
        full_name = parts[2]
        rating = parts[3]
        item_type = parts[4]

        if (query_lower in abbr.lower() or
            query_lower in full_name.lower() or
            abbr.lower() == query_lower or
            full_name.lower() == query_lower):
            results.append({
                "简称": abbr,
                "全称": full_name,
                "CCF评级": rating,
                "类型": item_type
            })

    return results

def search_ccf_cn(query):
    ccf_file = get_data_path("CCF-2025-CN.md")

    try:
        with open(ccf_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []

    results = []
    query_lower = query.lower().strip()

    for line in lines:
        line = line.strip()
        if not line or (line.startswith('|') and '------' in line):
            continue
        if line.startswith('期刊中文名称'):
            continue

        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 4:
            continue

        cn_name = parts[1]
        en_name = parts[2]
        rating = parts[3]
        language = parts[4] if len(parts) > 4 else ""

        if (query_lower in cn_name.lower() or
            query_lower in en_name.lower() or
            cn_name.lower() == query_lower or
            en_name.lower() == query_lower):
            results.append({
                "中文名称": cn_name,
                "英文名称": en_name,
                "CCF评级": rating,
                "语种": language,
                "类型": "期刊"
            })

    return results

def search_zky_or_xr(query, year=None):
    if year is None:
        file_path = get_data_path("XR-2026.md")
        year_str = "2026"
        source = "新锐分区"
    else:
        file_path = get_data_path(f"ZKY-{year}.md")
        year_str = str(year)
        source = "中科院分区"

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return []

    results = []
    query_lower = query.lower().strip()

    for line in lines:
        line = line.strip()
        if not line or (line.startswith('|') and '------' in line):
            continue
        if line.startswith('#') or line.startswith('>'):
            continue
        if '期刊名称' in line and '大类分区' in line:
            continue

        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 5:
            continue

        journal_name = parts[1]
        major_category = parts[2]
        sub_category = parts[3]
        field = parts[4]
        is_top = parts[5] if len(parts) > 5 else ""

        if query_lower in journal_name.lower() or journal_name.lower() == query_lower:
            results.append({
                "期刊名称": journal_name,
                "大类分区": major_category,
                "小类分区": sub_category,
                "学科范畴": field,
                "是否TOP期刊": is_top,
                "年份": year_str,
                "数据来源": source
            })

    return results

def search(query, year=None):
    ccfe_results = search_ccf_en(query)
    ccfc_results = search_ccf_cn(query)

    all_ccf = ccfe_results + ccfc_results

    if not all_ccf:
        return []

    results = []

    for ccf_item in all_ccf:
        item_type = ccf_item.get("类型", "")

        if "期刊" in item_type:
            abbr = ccf_item.get("简称", "")
            full_name = ccf_item.get("全称", "")

            zky_results = search_zky_or_xr(abbr, year)
            if not zky_results and full_name:
                zky_results = search_zky_or_xr(full_name, year)

            combined = {**ccf_item}
            if zky_results:
                zky = zky_results[0]
                combined["大类分区"] = zky.get("大类分区", "")
                combined["小类分区"] = zky.get("小类分区", "")
                combined["学科范畴"] = zky.get("学科范畴", "")
                combined["是否TOP期刊"] = zky.get("是否TOP期刊", "")
                combined["分区年份"] = zky.get("年份", "")
                combined["分区来源"] = zky.get("数据来源", "")
            else:
                combined["分区信息"] = "未找到"

            results.append(combined)
        else:
            results.append({**ccf_item})

    return results

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "请提供搜索关键词"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    query = sys.argv[1]
    year = None

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--zky" and i + 1 < len(sys.argv):
            year_arg = sys.argv[i + 1]
            if year_arg.isdigit():
                year = int(year_arg)
            i += 2
        else:
            i += 1

    results = search(query, year)

    if not results:
        print(json.dumps([{"期刊/会议": query, "CCF评级": "未找到", "分区信息": "未找到"}], ensure_ascii=False, indent=2))
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
