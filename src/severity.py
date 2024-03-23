import json
from dataclasses import dataclass
import scipy
import statistics


@dataclass
class CVSS2:
    AV: int
    AC: int
    Au: int
    C: int
    I: int
    A: int
    score: float

@dataclass
class CVSS3:
    AV: int
    AC: int
    PR: int
    UI: int
    S: int
    C: int
    I: int
    A: int
    score: float

@dataclass
class CVE:
    cve: str
    v2: "CVSS2"
    v3: "CVSS3"
    v31: "CVSS3"
    util: bool
    cwe: str

CVSS2_LOOKUP = {
    "AV": {
        "L": 1,
        "A": 2,
        "N": 3
    },
    "AC": {
        "H": 1,
        "M": 2,
        "L": 3
    },
    "Au": {
        "M": 1,
        "S": 2,
        "N": 3
    },
    "C": {
        "N": 1,
        "P": 2,
        "C": 3
    },
    "I": {
        "N": 1,
        "P": 2,
        "C": 3
    },
    "A": {
        "N": 1,
        "P": 2,
        "C": 3
    }
}   

CVSS3_LOOKUP = {
    "AV": {
        "P": 1,
        "L": 2,
        "A": 3,
        "N": 4
    },
    "AC": {
        "L": 1,
        "H": 2
    },
    "PR": {
        "N": 1,
        "L": 2,
        "H": 3
    },
    "UI": {
        "N": 1,
        "R": 2
    },
    "S": {
        "U": 1,
        "C": 2
    },
    "C": {
        "N": 1,
        "L": 2,
        "H": 3
    },
    "I": {
        "N": 1,
        "L": 2,
        "H": 3
    },
    "A": {
        "N": 1,
        "L": 2,
        "H": 3
    }
}


def managev2(vs, baseScore):
    temp_data = []
    for segment in vs.split("/"):
        parts = segment.split(":")
        key1 = parts[0]
        key2 = parts[1]
        try:
            temp_data.append(CVSS2_LOOKUP[key1][key2])
        except:
            continue
    temp_data.append(baseScore)
    return CVSS2(*temp_data)

def managev3(vs, baseScore):
    temp_data = []
    splits = vs.split("/")
    for segment in splits[1:]:
        parts = segment.split(":")
        key1 = parts[0]
        key2 = parts[1]
        try:
            temp_data.append(CVSS3_LOOKUP[key1][key2])
        except:
            continue
    temp_data.append(baseScore)
    return CVSS3(*temp_data)



def read_vhp(path):
    with open(path) as f:
        data = json.load(f)
    return data


def lookup_cve(number, path):
    splits = number.split("-")
    year = splits[1]
    folder = splits[2][:-3] + "xxx"
    file = number + ".json"
    with open(path + "/" + year + "/" + folder + "/" + file) as f:
        res = json.load(f)
    return res


def main():
    results = {}
    data = read_vhp("vhp_vulns.json")
    for entry in data:
        results[entry] = {}
        for item in data[entry]:
            tags = []
            for tag in item["tag_json"]:
                tags.append(tag["id"])
            # print(tags)
            results[entry][item["cve"]] = CVE(item["cve"], None, None, None, True if 617 in tags else False, None)
    
    # Populate records
    for project in results:
        for vulnerability in results[project]:
            entry = results[project][vulnerability]
            try:
                report = lookup_cve(vulnerability, "cves")
            except:
                continue
            try:
                entry.cwe = report["containers"]["cna"]["problemTypes"][0]["descriptions"][0]["cweId"]
            except:
                pass
            if "metrics" in report["containers"]["cna"]:
                for metric in report["containers"]["cna"]["metrics"]:
                    if "cvssV3_1" in metric:
                        entry.v31 = managev3(metric["cvssV3_1"]["vectorString"], metric["cvssV3_1"]["baseScore"])
                    if "cvssV3_0" in metric:
                        entry.v3 = managev3(metric["cvssV3_0"]["vectorString"], metric["cvssV3_0"]["baseScore"])
                    if "cvssV2_0" in metric:
                        entry.v2 = managev2(metric["cvssV2_0"]["vectorString"], metric["cvssV2_0"]["baseScore"])
    
    nodes = {
        # CVSS V2.0
        "AV2" : {True: [], False: []},
        "AC2" : {True: [], False: []},
        "Au2" : {True: [], False: []},
        "C2" : {True: [], False: []},
        "I2" : {True: [], False: []},
        "A2" : {True: [], False: []},
        "score2" : {True: [], False: []},
    
        # CVSS V3.0
        "AV3" : {True: [], False: []},
        "AC3" : {True: [], False: []},
        "PR3" : {True: [], False: []},
        "UI3" : {True: [], False: []},
        "S3" : {True: [], False: []},
        "C3" : {True: [], False: []},
        "I3" : {True: [], False: []},
        "A3" : {True: [], False: []},
        "score3" : {True: [], False: []},
    
        # CVSS V3.1
        "AV31" : {True: [], False: []},
        "AC31" : {True: [], False: []},
        "PR31" : {True: [], False: []},
        "UI31" : {True: [], False: []},
        "S31" : {True: [], False: []},
        "C31" : {True: [], False: []},
        "I31" : {True: [], False: []},
        "A31" : {True: [], False: []},
        "score31" : {True: [], False: []}
    }
    cwe = {True: [], False: []}

    for project in results:

        t_nodes = {
            # CVSS V2.0
            "AV2" : {True: [], False: []},
            "AC2" : {True: [], False: []},
            "Au2" : {True: [], False: []},
            "C2" : {True: [], False: []},
            "I2" : {True: [], False: []},
            "A2" : {True: [], False: []},
            "score2" : {True: [], False: []},
        
            # CVSS V3.0
            "AV3" : {True: [], False: []},
            "AC3" : {True: [], False: []},
            "PR3" : {True: [], False: []},
            "UI3" : {True: [], False: []},
            "S3" : {True: [], False: []},
            "C3" : {True: [], False: []},
            "I3" : {True: [], False: []},
            "A3" : {True: [], False: []},
            "score3" : {True: [], False: []},
        
            # CVSS V3.1
            "AV31" : {True: [], False: []},
            "AC31" : {True: [], False: []},
            "PR31" : {True: [], False: []},
            "UI31" : {True: [], False: []},
            "S31" : {True: [], False: []},
            "C31" : {True: [], False: []},
            "I31" : {True: [], False: []},
            "A31" : {True: [], False: []},
            "score31" : {True: [], False: []}
        }

        t_cwe = {True: [], False: []}

        for vulnerability in results[project]:
            record = results[project][vulnerability]
            status = record.util
            if record.cwe is not None:
                cwe[status].append(record.cwe)
                t_cwe[status].append(record.cwe)
            if record.v2 is not None:
                nodes["AV2"][status].append(record.v2.AV)
                nodes["AC2"][status].append(record.v2.AC)
                nodes["Au2"][status].append(record.v2.Au)
                nodes["C2"][status].append(record.v2.C)
                nodes["I2"][status].append(record.v2.I)
                nodes["A2"][status].append(record.v2.A)
                nodes["score2"][status].append(record.v2.score)

                t_nodes["AV2"][status].append(record.v2.AV)
                t_nodes["AC2"][status].append(record.v2.AC)
                t_nodes["Au2"][status].append(record.v2.Au)
                t_nodes["C2"][status].append(record.v2.C)
                t_nodes["I2"][status].append(record.v2.I)
                t_nodes["A2"][status].append(record.v2.A)
                t_nodes["score2"][status].append(record.v2.score)
                
            if record.v3 is not None:
                nodes["AV3"][status].append(record.v3.AV)
                nodes["AC3"][status].append(record.v3.AC)
                nodes["PR3"][status].append(record.v3.PR)
                nodes["UI3"][status].append(record.v3.UI)
                nodes["S3"][status].append(record.v3.S)
                nodes["C3"][status].append(record.v3.C)
                nodes["I3"][status].append(record.v3.I)
                nodes["A3"][status].append(record.v3.A)
                nodes["score3"][status].append(record.v3.score)

                t_nodes["AV3"][status].append(record.v3.AV)
                t_nodes["AC3"][status].append(record.v3.AC)
                t_nodes["PR3"][status].append(record.v3.PR)
                t_nodes["UI3"][status].append(record.v3.UI)
                t_nodes["S3"][status].append(record.v3.S)
                t_nodes["C3"][status].append(record.v3.C)
                t_nodes["I3"][status].append(record.v3.I)
                t_nodes["A3"][status].append(record.v3.A)
                t_nodes["score3"][status].append(record.v3.score)

            if record.v31 is not None:
                nodes["AV31"][status].append(record.v31.AV)
                nodes["AC31"][status].append(record.v31.AC)
                nodes["PR31"][status].append(record.v31.PR)
                nodes["UI31"][status].append(record.v31.UI)
                nodes["S31"][status].append(record.v31.S)
                nodes["C31"][status].append(record.v31.C)
                nodes["I31"][status].append(record.v31.I)
                nodes["A31"][status].append(record.v31.A)
                nodes["score31"][status].append(record.v31.score)

                t_nodes["AV31"][status].append(record.v31.AV)
                t_nodes["AC31"][status].append(record.v31.AC)
                t_nodes["PR31"][status].append(record.v31.PR)
                t_nodes["UI31"][status].append(record.v31.UI)
                t_nodes["S31"][status].append(record.v31.S)
                t_nodes["C31"][status].append(record.v31.C)
                t_nodes["I31"][status].append(record.v31.I)
                t_nodes["A31"][status].append(record.v31.A)
                t_nodes["score31"][status].append(record.v31.score)
        
        print("Project:",project)
        print("\n -- CVSS V2.0 -- ")
        flag = False
        done = False
        for key in t_nodes:
            print(key + ":")
            print("Count Util: " + str(len(t_nodes[key][True])) + "\t Count Non: " + str(len(t_nodes[key][False])))
            if len(t_nodes[key][True]) != 0:
                print("Util Median:", statistics.median(t_nodes[key][True]))
            if  len(t_nodes[key][False]) != 0:
                print("NonU Median:", statistics.median(t_nodes[key][False]))
            if len(t_nodes[key][True]) == 0 or len(t_nodes[key][False]) == 0:
                print("Data not available")
            else:
                print(scipy.stats.mannwhitneyu(t_nodes[key][True], t_nodes[key][False]))
            if "score" in key and not flag:
                print("\n -- CVSS V3.0 -- ")
                flag = True
            elif "score" in key and flag and not done:
                print("\n -- CVSS V3.1 -- ")
                done = True
        print("\nCWEs")
        print(t_cwe)
        print("\n\n")

    print("Overall:")
    flag = False
    done = False
    for key in nodes:
        print(key + ":")
        print("Count Util: " + str(len(nodes[key][True])) + "\t Count Non: " + str(len(nodes[key][False])))
        if len(nodes[key][True]) != 0:
            print("Util Median:", statistics.median(nodes[key][True]))
        if len(nodes[key][False]) != 0:
            print("NonU Median:", statistics.median(nodes[key][False]))
        if len(nodes[key][True]) == 0 or len(nodes[key][False]) == 0:
            print("Data not available for signifiance testing")
        else:
            print(scipy.stats.mannwhitneyu(nodes[key][True], nodes[key][False]))
        if "score" in key and not flag:
            print("\n -- CVSS V3.0 -- ")
            flag = True
        elif "score" in key and flag and not done:
            print("\n -- CVSS V3.1 -- ")
            done = True
    print("\nCWEs")
    print(cwe)


if __name__ == '__main__':
    main()
