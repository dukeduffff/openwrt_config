# !/usr/bin/env python
# coding=utf-8
#
# Generate a list of dnsmasq rules with ipset for gfwlist
#
# Copyright (C) 2014 http://www.shuyz.com
# Ref https://code.google.com/p/autoproxy-gfwlist/wiki/Rules
# https://gist.github.com/lanceliao/85cd3fcf1303dba2498c
import datetime
import sys
import typing

import requests

mydnsip = '127.0.0.1'
mydnsport = '5153'
ipset_name = "gfwlist"
ipset6_name = "gfwlist6"

# the url of gfwlist
baseurl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
# match comments/title/whitelist/ip address
comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'
gfw_url = "https://cdn.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/gfw.txt"
# do not write to router internal flash directly

#
# def gfwlist_run():
#     fs = open("./gfwlist.conf", "w")
#     fs.write('# gfw list ipset rules for dnsmasq\n')
#     fs.write('# updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
#     fs.write('#\n')
#
#     http = urllib3.PoolManager()
#
#     print('fetching list...')
#     content = http.request("GET", baseurl).data
#     content = base64.b64decode(content).decode("utf-8")
#
#     # write the decoded content to file then read line by line
#     tfs = open("./gfwlist.txt", 'w')
#     tfs.write(content)
#     tfs.close()
#     tfs = open("./gfwlist.txt", 'r')
#
#     print('page content fetched, analysis...')
#
#     # remember all blocked domains, in case of duplicate records
#     domainlist = []
#
#     for line in tfs.readlines():
#         if re.findall(comment_pattern, line):
#             print('this is a comment line: ' + line)
#         # fs.write('#' + line)
#         else:
#             domain = re.findall(domain_pattern, line)
#             if domain:
#                 try:
#                     found = domainlist.index(domain[0])
#                     print(domain[0] + ' exists.')
#                 except ValueError:
#                     print('saving ' + domain[0])
#                     domainlist.append(domain[0])
#                     fs.write(f"server=/{domain[0]}/{mydnsip}#{mydnsport}\n")
#                     fs.write(f"ipset=/{domain[0]}/{ipset_name},{ipset6_name}\n")
#                     # fs.write('ipset=/.%s/gfwlist\n' % domain[0])
#             else:
#                 print('no valid domain in this line: ' + line)
#
#     tfs.close()
#     fs.close()


def common_gfw_txt_to_conf():
    response = requests.get(gfw_url)
    content = response.content.decode("utf-8")
    if not content:
        return

    fs = open("./gfwlist.conf", "w")
    fs.write('# gfw list ipset rules for dnsmasq\n')
    fs.write('# updated on ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    fs.write('#\n')

    for domain in content.split("\n"):
        domain = domain.strip()
        if not domain:
            continue
        fs.write(f"server=/{domain}/{mydnsip}#{mydnsport}\n")
        fs.write(f"ipset=/{domain}/{ipset_name},{ipset6_name}\n")
    fs.close()
    print("generate gfwlist common config success!")


class HostScore(object):
    def __init__(self, host, avg=0.0, loss_rate=0.0, speed=0.0):
        self.host = host
        self.avg = avg
        self.loss_rate = loss_rate
        self.speed = speed

    @property
    def score(self):
        return self.avg + self.loss_rate * 2000 + (100 - self.speed)


def get_domain_ip_v4(domain):
    hosts = dns_resolver(domain, A)
    hosts.append("172.67.171.3")
    scores = []
    for host in hosts:
        avg, loss = ping_shell(host, 5)
        scores.append(HostScore(host, avg, loss))
    return scores


def ping_shell(host, cnt):
    import subprocess
    import re
    ping_command = ['ping', '-c', f"{cnt}", host]  # 在Linux和UNIX系统中使用'-c'参数，表示发送4个ICMP回显请求
    ping_process = subprocess.Popen(ping_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ping_output, ping_error = ping_process.communicate()
    ping_output = ping_output.decode('utf-8')

    # 解析ping结果，获取平均延迟和丢包率
    avg_time = 1000
    loss_rate = 1.00
    avg_time_match1 = re.search(r'min/avg/max/mdev = [\d.]+/([\d.]+)/', ping_output)
    avg_time_match2 = re.search(r'min/avg/max = [\d.]+/([\d.]+)/', ping_output)
    loss_rate_match = re.search(r'(\d+)% packet loss', ping_output)

    if avg_time_match1:
        avg_time = float(avg_time_match1.group(1))
    elif avg_time_match2:
        avg_time = float(avg_time_match2.group(1))
    if loss_rate_match:
        loss_rate = float(loss_rate_match.group(1))

    return avg_time, loss_rate


def get_cfnode_hosts():
    hosts: typing.List[HostScore] = []
    try:
        res = requests.get("https://cfnode.eu.org/api/ajax/get_opt_v4", timeout=10)
    except Exception:
        return hosts
    if res.status_code != 200:
        return hosts
    res_json = res.json()
    if not res_json.get("status", False):
        return hosts
    res_list = res_json.get("data", [])
    for h in res_list:
        address = h.get("address", "")
        speed = h.get("speed", 0)
        loc = h.get("device_name", "")
        if loc != "广东移动":
            continue
        hosts.append(HostScore(host=address, speed=speed / 100))
    # 添加默认比较稳定的机器
    hosts.append(HostScore(host="172.67.171.3", speed=80))
    for host in hosts:
        avg, loss = ping_shell(host.host, 5)
        host.avg = avg
        host.loss_rate = loss
    return hosts


def chose_best_host(domains=None):
    hour = datetime.datetime.now().hour
    # 每天18点到次日凌晨1点,使用该ip,目前测试下来最快的
    # if hour >= 18 or hour <= 1:
    #     return "172.67.171.3"
    # 其他时间选择domains的时间最快的ip
    hosts = []
    if not domains:
        hosts.extend(get_cfnode_hosts())
    else:
        for domain in domains:
            hosts.extend(get_domain_ip_v4(domain))
    if not hosts:
        return None
    hosts.sort(key=lambda a: a.score)
    return hosts[0].host


A = 1
AAAA = 28


def dns_resolver(domain, ip_type=A):
    response = requests.get(f"https://dns.alidns.com/resolve?name={domain}&type={ip_type}")
    if response.status_code != 200:
        print(response.text)
    dns_res = response.json()
    status = dns_res.get("Status")
    if status != 0:
        print(response.text)
    ans_list = dns_res.get("Answer")
    hosts = []
    for ans in ans_list:
        ip = ans.get("data")
        if not ip:
            continue
        hosts.append(ip)
    return hosts


def custom_gfw_to_conf():
    fs = open("./gfw_custom.conf", "w")
    # 写入静态文件
    fs.write("""
# gfw server\n""")
    # 写入出国最优ip
    best_host = chose_best_host()
    if not best_host:
        best_host = "172.67.171.3"
    fs.write(f"address=/cntest2022.cf/{best_host}\n")
    fs.write(f"address=/cntest2022.cf/::\n")  # 禁止ipv6解析
    fs.write("""

# gfw custom
server=/supes.top/127.0.0.1#5153
ipset=/supes.top/gfwlist
server=/openwrt.ai/127.0.0.1#5153
ipset=/openwrt.ai/gfwlist
server=/369369.xyz/127.0.0.1#5153
ipset=/369369.xyz/gfwlist
server=/69shu.com/127.0.0.1#5153
ipset=/69shu.com/gfwlist\n""")
    print("generate gfwlist custom config success!")


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        arg = args[1]
        if arg == "common":
            common_gfw_txt_to_conf()
        elif arg == "custom":
            custom_gfw_to_conf()
    else:
        common_gfw_txt_to_conf()
        custom_gfw_to_conf()
