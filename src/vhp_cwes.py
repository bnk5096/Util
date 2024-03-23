import json
import requests

def main():
    resp = requests.get("http://vulnerabilityhistory.org/api/tags")
    tags = resp.json()
    tag_dict = {}
    for entry in tags:
        if "cwe" in entry['shortname'].lower():
            tag_dict[entry['id']] = entry['name']
    # print(tag_dict)
    with open("vhp_tags.json", 'w+') as f:
        json.dump(tag_dict, f)


if __name__ == '__main__':
    main()
