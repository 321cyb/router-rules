#!/usr/bin/env python3

import re
import json

def convert_geoip_cn(txt_path):
    """
    Convert a geoip text file to JSON format.
    each input line has the following format: IP-CIDR,1.0.32.0/19,no-resolve
    output json has following format:
    {
      "version": 2,
      "rules": [
        {
          "ip_cidr": [
          ],
          "invert": true
        }
      ]
    }
    """
    cn_ip_list = []
    with open(txt_path) as f:
        for line in f:
            ip_matcher = re.compile(r'(IP-CIDR6?,)(.+)(,no-resolve)')
            match_result = ip_matcher.search(line.strip())
            if match_result:
                cn_ip_list.append(match_result.group(2))
            else:
                print("Invalid line: " + line.strip())
                exit(1)
    non_cn_ips_rule = {
        "version": 2,
        "rules": [
             {
                 "ip_cidr": cn_ip_list,
                 "invert": True,
             }
        ] 
    }
    with open('noncn.json', 'w') as f:
        json.dump(non_cn_ips_rule, f, indent = 2, ensure_ascii=False)
            
def convert_geosite_gfwlist(txt_path):
    """
    Convert a geoip text file to JSON format.
    each input line contains one blocked domain suffix in China,
    output json has following format:
    {
      "version": 2,
      "rules": [
        {
          "domain_suffix": [
          ]
        }
      ]
    }
    """
    gfw_domain_list = []
    with open(txt_path) as f:
        for line in f:
            gfw_domain_list.append(line.strip())
    gfw_sites_rule = {
        "version": 2,
        "rules": [
             {
                 "domain_suffix": gfw_domain_list,
             }
        ] 
    }
    with open('gfw.json', 'w') as f:
        json.dump(gfw_sites_rule, f, indent = 2, ensure_ascii=False)
            
            
if __name__ == "__main__":            
    convert_geoip_cn("cn.txt")
    convert_geosite_gfwlist("gfw.txt")
