import json
import os
import re
import sys
from typing import Dict, List, Tuple

# 数据文件常量
CCF_EN_FILE = "CCF-2026-EN.md"
CCF_CN_FILE = "CCF-2025-CN.md"
ZKY_FILES = ["ZKY-2025.md", "ZKY-2023.md", "ZKY-2022.md"]
XR_FILES = ["XR-2026.md"]

# 缩写映射表
ABBREVIATIONS = {
    "TMC": "IEEE Transactions on Mobile Computing",
    "TPAMI": "IEEE Transactions on Pattern Analysis and Machine Intelligence",
    "TKDE": "IEEE Transactions on Knowledge and Data Engineering",
    "TSE": "IEEE Transactions on Software Engineering",
    "TOSEM": "ACM Transactions on Software Engineering and Methodology",
    "TIST": "ACM Transactions on Intelligent Transportation Systems",
    "TODS": "ACM Transactions on Database Systems",
    "TOPLAS": "ACM Transactions on Programming Languages and Systems",
    "TOG": "ACM Transactions on Graphics",
    "TOS": "ACM Transactions on Storage",
    "TC": "IEEE Transactions on Computers",
    "TMM": "IEEE Transactions on Multimedia",
    "TIP": "IEEE Transactions on Image Processing",
    "TNNLS": "IEEE Transactions on Neural Networks and Learning Systems",
    "TCYB": "IEEE Transactions on Cybernetics",
    "TFS": "IEEE Transactions on Fuzzy Systems",
    "TEVC": "IEEE Transactions on Evolutionary Computation",
    "TIST": "IEEE Transactions on Intelligent Transportation Systems",
    "TBD": "IEEE Transactions on Big Data",
    "TCC": "IEEE Transactions on Cloud Computing",
    "TSC": "IEEE Transactions on Services Computing",
    "TNSM": "IEEE Transactions on Network and Service Management",
    "TVT": "IEEE Transactions on Vehicular Technology",
    "TWC": "IEEE Transactions on Wireless Communications",
    "TCOM": "IEEE Transactions on Communications",
    "TSP": "IEEE Transactions on Signal Processing",
    "TIT": "IEEE Transactions on Information Theory",
    "TAC": "IEEE Transactions on Automatic Control",
    "TIE": "IEEE Transactions on Industrial Electronics",
    "TII": "IEEE Transactions on Industrial Informatics",
    "TMECH": "IEEE/ASME Transactions on Mechatronics",
    "TRO": "IEEE Transactions on Robotics",
    "TASLP": "IEEE/ACM Transactions on Audio, Speech, and Language Processing",
    "TASL": "IEEE Transactions on Audio, Speech, and Language Processing",
    "JMLR": "Journal of Machine Learning Research",
    "PAMI": "IEEE Transactions on Pattern Analysis and Machine Intelligence",
    "IJCV": "International Journal of Computer Vision",
    "CVPR": "IEEE/CVF Conference on Computer Vision and Pattern Recognition",
    "ICCV": "IEEE/CVF International Conference on Computer Vision",
    "ECCV": "European Conference on Computer Vision",
    "NeurIPS": "Neural Information Processing Systems",
    "ICML": "International Conference on Machine Learning",
    "ICLR": "International Conference on Learning Representations",
    "AAAI": "AAAI Conference on Artificial Intelligence",
    "IJCAI": "International Joint Conference on Artificial Intelligence",
    "ACL": "Annual Meeting of the Association for Computational Linguistics",
    "EMNLP": "Conference on Empirical Methods in Natural Language Processing",
    "NAACL": "North American Chapter of the Association for Computational Linguistics",
    "COLING": "International Conference on Computational Linguistics",
    "SIGIR": "ACM SIGIR Conference on Research and Development in Information Retrieval",
    "WWW": "The Web Conference",
    "KDD": "ACM SIGKDD Conference on Knowledge Discovery and Data Mining",
    "ICDE": "IEEE International Conference on Data Engineering",
    "VLDB": "International Conference on Very Large Data Bases",
    "SIGMOD": "ACM SIGMOD International Conference on Management of Data",
    "CIKM": "ACM International Conference on Information and Knowledge Management",
    "ICSE": "International Conference on Software Engineering",
    "FSE": "ACM SIGSOFT Symposium on the Foundation of Software Engineering",
    "ASE": "IEEE/ACM International Conference on Automated Software Engineering",
    "ISSTA": "ACM SIGSOFT International Symposium on Software Testing and Analysis",
    "PLDI": "ACM SIGPLAN Conference on Programming Language Design and Implementation",
    "POPL": "ACM SIGPLAN Symposium on Principles of Programming Languages",
    "OSDI": "USENIX Symposium on Operating Systems Design and Implementation",
    "SOSP": "ACM Symposium on Operating Systems Principles",
    "NSDI": "USENIX Symposium on Networked Systems Design and Implementation",
    "SIGCOMM": "ACM SIGCOMM Conference",
    "MobiCom": "ACM International Conference on Mobile Computing and Networking",
    "SenSys": "ACM Conference on Embedded Networked Sensor Systems",
    "IPSN": "ACM/IEEE International Conference on Information Processing in Sensor Networks",
    "RTSS": "IEEE Real-Time Systems Symposium",
    "CPS": "ACM/IEEE International Conference on Cyber-Physical Systems",
    "DAC": "Design Automation Conference",
    "ICCAD": "IEEE/ACM International Conference on Computer-Aided Design",
    "HPCA": "IEEE International Symposium on High-Performance Computer Architecture",
    "ISCA": "ACM/IEEE International Symposium on Computer Architecture",
    "MICRO": "IEEE/ACM International Symposium on Microarchitecture",
    "ASPLOS": "ACM International Conference on Architectural Support for Programming Languages and Operating Systems",
    "PPoPP": "ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming",
    "SC": "ACM/IEEE International Conference for High Performance Computing, Networking, Storage, and Analysis",
    "HPDC": "ACM International Symposium on High-Performance Parallel and Distributed Computing",
    "ICS": "ACM International Conference on Supercomputing",
    "SP": "IEEE Symposium on Security and Privacy",
    "CCS": "ACM Conference on Computer and Communications Security",
    "USENIX Security": "USENIX Security Symposium",
    "NDSS": "Network and Distributed System Security Symposium",
    "CRYPTO": "International Cryptology Conference",
    "EUROCRYPT": "Annual International Conference on the Theory and Applications of Cryptographic Techniques",
    "CHI": "ACM Conference on Human Factors in Computing Systems",
    "UIST": "ACM Symposium on User Interface Software and Technology",
    "UbiComp": "ACM International Joint Conference on Pervasive and Ubiquitous Computing",
    "IMWUT": "Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies",
    "VR": "IEEE Virtual Reality",
    "IEEE VR": "IEEE Virtual Reality",
    "ISMAR": "IEEE International Symposium on Mixed and Augmented Reality",
    "CGO": "IEEE/ACM International Symposium on Code Generation and Optimization",
    "EuroSys": "European Conference on Computer Systems",
    "FAST": "USENIX Conference on File and Storage Technologies",
    "ATC": "USENIX Annual Technical Conference",
    "HotOS": "USENIX Workshop on Hot Topics in Operating Systems",
    "HotNets": "ACM Workshop on Hot Topics in Networks",
    "CoNEXT": "ACM International Conference on Emerging Networking Experiments and Technologies",
    "IMC": "ACM Internet Measurement Conference",
    "INFOCOM": "IEEE International Conference on Computer Communications",
    "ICNP": "IEEE International Conference on Network Protocols",
    "IWQoS": "IEEE/ACM International Symposium on Quality of Service",
    "SECON": "IEEE International Conference on Sensing, Communication, and Networking",
    "MASS": "IEEE International Conference on Mobile Ad-hoc and Sensor Systems",
    "ICDCS": "IEEE International Conference on Distributed Computing Systems",
    "SRDS": "IEEE International Symposium on Reliable Distributed Systems",
    "DSN": "IEEE/IFIP International Conference on Dependable Systems and Networks",
    "LCTES": "ACM SIGPLAN/SIGBED International Conference on Languages, Compilers, and Tools for Embedded Systems",
    "EMSOFT": "International Conference on Embedded Software",
    "CODES": "International Conference on Hardware/Software Codesign and System Synthesis",
    "NOCS": "ACM/IEEE International Symposium on Networks-on-Chip",
    "DATE": "Design, Automation and Test in Europe Conference",
    "ICRA": "IEEE International Conference on Robotics and Automation",
    "IROS": "IEEE/RSJ International Conference on Intelligent Robots and Systems",
    "RSS": "Robotics: Science and Systems",
    "T-RO": "IEEE Transactions on Robotics",
    "T-MECH": "IEEE/ASME Transactions on Mechatronics",
    "RA-L": "IEEE Robotics and Automation Letters",
    "ICRA": "IEEE International Conference on Robotics and Automation",
    "IROS": "IEEE/RSJ International Conference on Intelligent Robots and Systems",
    "RSS": "Robotics: Science and Systems",
}


def get_data_path(filename: str) -> str:
    """获取数据文件的完整路径"""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "data", filename)


def normalize_query(query: str) -> Tuple[str, str]:
    """
    规范化查询
    返回: (规范化后的查询, 匹配类型)
    匹配类型: abbreviation | raw
    """
    q = query.strip().upper()
    
    if q in ABBREVIATIONS:
        return ABBREVIATIONS[q], "abbreviation"
    
    return query.strip(), "raw"


def clean_line(line: str) -> List[str]:
    """清理并解析 Markdown 表格行"""
    line = line.strip()
    
    if not line or line.startswith("#") or "------" in line:
        return []
    
    parts = [p.strip() for p in line.split("|")]
    return [p for p in parts if p]


def fuzzy_match(query: str, text: str) -> bool:
    """模糊匹配"""
    return query.lower() in text.lower()


def search_file(filepath: str, query: str) -> List[List[str]]:
    """在单个文件中搜索"""
    results = []
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        return results
    
    for line in lines:
        parts = clean_line(line)
        if not parts:
            continue
        
        row_text = " ".join(parts)
        if fuzzy_match(query, row_text):
            results.append(parts)
    
    return results


def parse_ccf_row(parts: List[str], source: str) -> Dict:
    """解析 CCF 数据行"""
    if len(parts) < 4:
        return None
    
    return {
        "source": source,
        "short_name": parts[0],
        "full_name": parts[1] if len(parts) > 1 else parts[0],
        "rank": parts[2] if len(parts) > 2 else "",
        "category": parts[3] if len(parts) > 3 else ""
    }


def parse_partition_row(parts: List[str], source: str) -> Dict:
    """解析分区数据行"""
    if len(parts) < 5:
        return None
    
    return {
        "source": source,
        "name": parts[0],
        "zone": parts[1],
        "sub_zone": parts[2] if len(parts) > 2 else "",
        "field": parts[3] if len(parts) > 3 else "",
        "top": parts[4] == "是" if len(parts) > 4 else False
    }


def is_journal(ccf_result: List[Dict]) -> bool:
    """判断是否为期刊"""
    if not ccf_result:
        return False
    for item in ccf_result:
        if "期刊" in item.get("category", ""):
            return True
    return False


def search_ccf(query: str) -> List[Dict]:
    """搜索 CCF 数据"""
    results = []
    
    # 搜索英文 CCF
    for row in search_file(get_data_path(CCF_EN_FILE), query):
        parsed = parse_ccf_row(row, "CCF-2026-EN")
        if parsed:
            results.append(parsed)
    
    # 搜索中文 CCF
    for row in search_file(get_data_path(CCF_CN_FILE), query):
        parsed = parse_ccf_row(row, "CCF-2025-CN")
        if parsed:
            results.append(parsed)
    
    return results


def search_partition(query: str) -> List[Dict]:
    """搜索分区数据（中科院 + 新锐）"""
    results = []
    
    # 搜索新锐分区
    for filename in XR_FILES:
        for row in search_file(get_data_path(filename), query):
            parsed = parse_partition_row(row, filename.replace(".md", ""))
            if parsed:
                results.append(parsed)
    
    # 搜索中科院分区
    for filename in ZKY_FILES:
        for row in search_file(get_data_path(filename), query):
            parsed = parse_partition_row(row, filename.replace(".md", ""))
            if parsed:
                results.append(parsed)
    
    return results


def search(query: str) -> Dict:
    """
    主搜索函数
    返回标准 JSON Schema
    """
    # 规范化查询
    normalized_query, match_type = normalize_query(query)
    
    # 搜索 CCF
    ccf_results = search_ccf(normalized_query)
    
    # 构建结果
    result = {
        "query": query,
        "normalized_query": normalized_query,
        "match_type": match_type,
        "found": False,
        "results": {
            "ccf": ccf_results,
            "partition": []
        }
    }
    
    # 如果找到 CCF 结果
    if ccf_results:
        result["found"] = True
        # 只有期刊才搜索分区
        if is_journal(ccf_results):
            result["results"]["partition"] = search_partition(normalized_query)
    else:
        # 未找到 CCF，尝试搜索分区
        partition_results = search_partition(normalized_query)
        if partition_results:
            result["found"] = True
            result["results"]["partition"] = partition_results
    
    return result


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "Usage: python search.py <query>",
            "query": "",
            "normalized_query": "",
            "match_type": "",
            "found": False,
            "results": {"ccf": [], "partition": []}
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    
    query = sys.argv[1]
    result = search(query)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
