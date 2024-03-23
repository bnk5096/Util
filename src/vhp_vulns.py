import requests
import json


def main():
    projects = {}
    resp = requests.get("http://vulnerabilityhistory.org/api/vulnerabilities")
    data = resp.json()
    for entry in data:
        if entry['project_name'] not in projects:
            projects[entry['project_name']] = []
        projects[entry['project_name']].append(entry)
    with open("vhp_vulns.json", 'w+') as f:
        json.dump(projects, f)

if __name__ == '__main__':
    main()
