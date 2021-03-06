# -*- coding: utf-8 -*-
import os
import re
import json
import base64


def read_file(filename):
    with open(filename, 'rb') as f:
        return base64.b64decode(f.read()).decode('utf-8').strip()


def read_rules(category, rule_set, rule_files):
    rules = ""
    for file in rule_files:
        if len(file) > 0:
            filename = os.path.join('extensions',
                                    category.strip().lower(),
                                    rule_set.strip().lower(),
                                    file.lower().strip() + ".conf")
            try:
                rules += "\n// {}\n{}\n".format(file.capitalize(), read_file(filename))
                print("Success: {}".format(filename))
            except:
                print("Error occurs while reading {}".format(filename))
    return rules


def main():
    cfg_file_path = 'Customize.example.json'
    if os.path.exists('Customize.json'):
        cfg_file_path = 'Customize.json'

    with open(cfg_file_path, 'r') as f:
        cfg = json.load(f)

    data = read_file("extensions/Base.conf")

    # 节点信息
    if len(cfg["config"]["node"]) >= 2:
        data = re.sub(r'\[Proxy\][\s\S]+?\[Rule\]',
                      "\n".join(cfg["config"]["node"]) + "\n[Rule]",
                      data)

    # 规则信息
    for category in cfg['config']["category"]:
        for rule_set in cfg[category].keys():
            data = data.replace('{}_{}_RULES_HERE'.format(category.upper(), rule_set.upper()),
                                read_rules(category, rule_set, cfg[category][rule_set]))

    with open("Surge_Customize.conf", 'w') as ff:
        ff.write(data)


if "__main__" == __name__:
    print("Building Customize Rules...")
    main()
    print("Success")
