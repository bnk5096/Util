import json
from dataclasses import dataclass

@dataclass
class Vuln:
    id: str
    tags: list[int]
    util: bool


def read_vhp(path):
    with open(path) as f:
        data = json.load(f)
    return data


def main():
    results = {}
    data = read_vhp("vhp_vulns.json")
    tags = read_vhp("vhp_tags.json")
    for project in data:
        results[project] = {}
        for vulnerability in data[project]:
            tag_list = []
            for tag in vulnerability["tag_json"]:
                tag_list.append(str(tag["id"]))
        # 617
            results[project][vulnerability["cve"]] = Vuln(vulnerability["cve"], tag_list, True if '617' in tag_list else False)

    cwe_util = []
    cwe_nonu = []
    for project in results:
        for vulnerability_key in results[project]:
            # print(vulnerability_key)
            vulnerability = results[project][vulnerability_key]
            # print(vulnerability)
            for tag in vulnerability.tags:
                if tag in tags:
                    if vulnerability.util:
                        cwe_util.append(tags[tag])
                    else:
                        cwe_nonu.append(tags[tag])
    cwe_util.sort()
    cwe_nonu.sort()
    print(cwe_util)
    print(cwe_nonu)
    # print(tags)



if __name__ == '__main__':
    main()
