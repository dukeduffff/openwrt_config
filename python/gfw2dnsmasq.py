# !/usr/bin/env python
# coding=utf-8
#
# Generate a list of dnsmasq rules with ipset for gfwlist
#
# Copyright (C) 2014 http://www.shuyz.com
# Ref https://code.google.com/p/autoproxy-gfwlist/wiki/Rules
# https://gist.github.com/lanceliao/85cd3fcf1303dba2498c
import argparse
import json
import re
import typing
from datetime import datetime

import dns.resolver
import requests

mydnsip = '127.0.0.1'
mydnsport = '5153'
ipset_name = "gfwlist"
ipset6_name = "gfwlist6"
best_ip_domain = "8.889288.xyz"

# the url of gfwlist
baseurl = 'https://raw.githubusercontent.com/gfwlist/gfwlist/master/gfwlist.txt'
# match comments/title/whitelist/ip address
comment_pattern = '^\!|\[|^@@|^\d+\.\d+\.\d+\.\d+'
domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'
gfw_url = "https://cdn.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/gfw.txt"
default_ipv4 = "172.67.3.3"
self_domain = "327237.xyz"
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

    fs = open("./proxy_list.txt", "w")
    fs.write('# gfw list ipset rules for dnsmasq\n')
    fs.write('# updated on ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '\n')
    fs.write('#\n')

    for domain in content.split("\n"):
        domain = domain.strip()
        if not domain:
            continue
        fs.write(f"domain:{domain}\n")
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


ping_cnt = 10
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
    ans_list = dns_res.get("Answer", [])
    hosts = []
    for ans in ans_list:
        ip = ans.get("data")
        if not ip:
            continue
        hosts.append(ip)
    return hosts


def sys_dns_resolver(domain, ip_type=A):
    resp = dns.resolver.resolve(domain, "A" if ip_type == A else "AAAA")
    hosts = [r.address for r in resp]
    return hosts


def get_domain_ip_by_dns(domain, with_ipv4=True, with_ipv6=False, dr=dns_resolver):
    scores = []
    if with_ipv4:
        hosts = dr(domain, A)
        for host in hosts:
            scores.append(HostScore(host, speed=60))
    if with_ipv6:
        hosts = dr(domain, AAAA)
        for host in hosts:
            scores.append(HostScore(host, speed=60))
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


def tcping_shell(host, cnt, port=8443):
    # github开源地址:https://github.com/cloverstd/tcping/releases
    import subprocess
    import re
    if ":" in host:
        host = f"[{host}]"
    ping_command = ['/root/tcping/tcping', '-c', f"{cnt}", host, f"{port}"]
    ping_process = subprocess.Popen(ping_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ping_output, ping_error = ping_process.communicate()
    ping_output = ping_output.decode('utf-8')

    # 解析ping结果，获取平均延迟和丢包率
    avg_time = 1000
    success_match_cnt = 1
    fail_match_cnt = 0
    # 获取成功次数和失败次数
    success_match = re.search(r"(\d+) successful", ping_output)
    failure_match = re.search(r"(\d+) failed", ping_output)
    average_match = re.search(r"Average = (\d+)\.\d+ms", ping_output)

    if success_match:
        success_match_cnt = float(success_match.group(1))
    if failure_match:
        fail_match_cnt = float(failure_match.group(1))
    if average_match:
        avg_time = float(average_match.group(1))
    loss_rate = fail_match_cnt / (fail_match_cnt + success_match_cnt)

    return avg_time, loss_rate


def parse_html(html_str: str):
    html_split = html_str.split("<tr>")
    hosts = []
    for s in html_split:
        tags: typing.List[str] = s.split("\n")
        if len(tags) < 5:
            continue
        i = 0
        host = ""
        carrier = ""
        speed = 0
        for tag in tags:
            if "td" not in tag:
                continue
            result: str = re.findall("<td>(.*?)</td>", tag)
            if not result:
                continue
            result = result[0]
            # 字段赋值
            if i == 0:
                carrier = result
            elif i == 1:
                host = result
            elif i == 2:
                speed = int(result.replace("MB", "").strip())
            i = i + 1
        if carrier != "移动":
            continue
        hosts.append(HostScore(host, speed=speed))
    return hosts


ipv4_url = "https://monitor.gacjie.cn/page/cloudflare/ipv4.html"
ipv6_url = "https://monitor.gacjie.cn/page/cloudflare/ipv6.html"


def get_cfnode_hosts(get_remote=True, url=ipv4_url):
    hosts = []
    if not get_remote:
        return hosts
    try:
        res = requests.get(url, timeout=10)
    except Exception:
        return hosts
    if res.status_code != 200:
        return hosts
    html_content = res.content.decode("utf-8")
    html_content = html_content[html_content.index("<tbody>"):html_content.index("</tbody>")]
    hosts: typing.List[HostScore] = parse_html(html_content.replace(" ", "").replace("<tbody>\n", ""))
    return hosts


def get_random_ipv4():
    hosts: typing.List[HostScore] = []
    try:
        res = requests.get("https://cloudflare.vmshop.org/ipv4.php", timeout=10)
    except Exception:
        return hosts
    if res.status_code != 200:
        return hosts
    content = res.content.decode("utf-8")
    ips = content.split("<br>")
    for ip in ips:
        if not ip:
            continue
        hosts.append(HostScore(
            host=ip,
            speed=100
        ))
    return hosts


def get_ipv6_cfnode_hosts():
    hosts: typing.List[HostScore] = []
    try:
        res = requests.get("https://monitor.gacjie.cn/api/ajax/get_cloud_flare_v6?page=1&limit=100", timeout=10)
    except Exception:
        return hosts
    if res.status_code != 200:
        return hosts
    res_json = res.json()
    if not res_json.get("status", False):
        return hosts
    ips = res_json.get("data", [])
    for ip in ips:
        if ip.get("device_name") != "山东移动":
            continue
        hosts.append(HostScore(
            host=ip.get("address"),
            speed=ip.get("speed", 0) / 100
        ))
    return hosts


def chose_best_host(domains=None, ipv6=False) -> typing.Tuple[str, bool]:
    hour = datetime.now().hour
    # 每天18点到次日凌晨1点,使用该ip,目前测试下来最快的
    # if hour >= 18 or hour <= 1:
    #     return "172.67.171.3"
    # 其他时间选择domains的时间最快的ip
    hosts: typing.List[HostScore] = []
    is_ipv6 = False
    if ipv6:
        hosts.extend(get_ipv6_cfnode_hosts())
        is_ipv6 = True if hosts else False
    elif not hosts:
        if not domains:
            hosts.extend(get_ipv4_cfnode_hosts())
        else:
            for domain in domains:
                hosts.extend(get_domain_ip_by_dns(domain))
    # 若为空必须返回一个值
    if not hosts:
        return default_ipv4, False
    # ping的方式选择最优
    for host in hosts:
        avg, loss = ping_shell(host.host, ping_cnt)
        host.avg = avg
        host.loss_rate = loss
    hosts.sort(key=lambda a: a.score)
    best_host = hosts[0].host if hosts[0].host else default_ipv4
    return best_host, is_ipv6


def get_one_best_host_tcping(func: typing.Callable, **kwargs) -> typing.Tuple[str, bool]:
    if not kwargs:
        hosts = func()
    else:
        hosts = func(**kwargs)
    for host in hosts:
        print(host.host)
        host.avg, host.loss_rate = tcping_shell(host.host, ping_cnt)
    hosts = [host for host in hosts if host.loss_rate < 0.2 and host.avg < 250]
    if hosts:
        hosts.sort(key=lambda a: a.score)
        return hosts[0].host, ":" in hosts[0].host
    return "", False


def chose_best_hosts_both_46() -> typing.Tuple[str, bool]:
    hosts: typing.List[HostScore] = []
    hour = datetime.now().hour
    # 每天18点到次日凌晨1点,使用该ip,目前测试下来最快的
    # if hour >= 18 or hour <= 1:
    #     return "172.67.171.3"
    # hosts.extend(get_random_ipv4())
    # for host in hosts:
    #     host.avg, host.loss_rate = tcping_shell(host.host, ping_cnt)
    # hosts = [host for host in hosts if host.loss_rate < 0.2 and host.avg <= 180]
    # if hosts:
    #     hosts.sort(key=lambda a: a.score)
    #     return hosts[0].host, False
    # 1. 尝试获取接口数据
    # if hour < 18 or hour > 19:
    #     # 这个时间段内尝试使用ipv4
    #     host, is_ipv6 = get_one_best_host_tcping(get_cfnode_hosts, url=ipv4_url)
    #     if host:
    #         return host, is_ipv6
    host, is_ipv6 = get_one_best_host_tcping(get_cfnode_hosts, url=ipv4_url)
    if host:
        return host, is_ipv6
    # 2. 读取ipv6
    host, is_ipv6 = get_one_best_host_tcping(get_cfnode_hosts, url=ipv6_url)
    if host:
        return host, is_ipv6
    # 3. 走dns查询
    host, is_ipv6 = get_one_best_host_tcping(
        get_domain_ip_by_dns, domain=best_ip_domain, with_ipv4=True, with_ipv6=False,
        dr=sys_dns_resolver)
    if host:
        return host, is_ipv6
    return default_ipv4, False


def replace_template(from_dir, to_dir, chose_ipv6, url, tcping):
    minute = datetime.now().minute
    if minute % 10 != 0:
        if url and check_gfw(url=url):
            exit(0)
    if not tcping:
        best_host, is_ipv6 = chose_best_host(ipv6=chose_ipv6)
    else:
        best_host, is_ipv6 = chose_best_hosts_both_46()
    lines = open(from_dir, "r")
    to_file = open(to_dir, "w")
    for line in lines:
        to_file.write(line.replace("{CF_IP}", best_host))
    to_file.close()
    exit(1)


def get_outbound_config(config_dict, tag):
    for c in config_dict.get("outbounds", []):
        if c.get("tag") == tag:
            return c
    return None


def copy_json(origin_dict):
    return json.loads(json.dumps(origin_dict))


def replace_cluster_template(from_dir, to_dir, chose_ipv6, tcping, concurrent):
    if not concurrent:
        concurrent = 8
    concurrent = int(concurrent)
    data = open(from_dir).read()
    config_dict = json.loads(data)
    if not config_dict.get("outbounds"):
        config_dict["outbounds"] = []
    tag_name_prefix = "proxy_grpc"
    outbound = get_outbound_config(config_dict, tag_name_prefix)
    if not outbound:
        return
    origin_tag = outbound.get("tag", "")
    for i in range(concurrent):
        o = copy_json(outbound)
        tag_name = f"{origin_tag}_{i}"
        o["tag"] = tag_name
        config_dict.get("outbounds").append(o)
    balancers = config_dict.get("routing", {}).get("balancers", [])
    if balancers:
        balancers[0]["selector"] = [tag_name_prefix]
    config_str = json.dumps(config_dict, ensure_ascii=False, indent=4)
    if not tcping:
        best_host, is_ipv6 = chose_best_host(ipv6=chose_ipv6)
    else:
        best_host, is_ipv6 = chose_best_hosts_both_46()
    config_str = config_str.replace("{CF_IP}", best_host)
    to_file = open(to_dir, "w")
    # print(config_str)
    to_file.write(config_str)
    to_file.close()
    exit(1)


def check_gfw(url):
    try:
        requests.get(url, timeout=5)
    except Exception:
        return False
    return True


def custom_gfw_to_conf(chose_ipv6):
    fs = open("./gfw_custom.conf", "w")
    # 写入静态文件
    fs.write("""
# gfw server\n""")
    # 写入出国最优ip
    best_host, is_ipv6 = chose_best_host(ipv6=chose_ipv6)
    fs.write(f"address=/cntest2022.cf/{'0.0.0.0' if is_ipv6 else best_host}\n")
    fs.write(f"address=/cntest2022.cf/{best_host if is_ipv6 else '::'}\n")  # 禁止ipv6解析
    fs.write("""
# gfw dns

# gfw custom
server=/supes.top/127.0.0.1#5153
server=/openwrt.ai/127.0.0.1#5153
server=/369369.xyz/127.0.0.1#5153
server=/adguard.com/127.0.0.1#5153
server=/69shu.com/127.0.0.1#5153\n""")
    fs.close()
    print("generate gfwlist custom config success!")


def update_domain(chose_ipv6, tcping):
    url = "http://192.168.31.1:9091/plugins/hosts/update"
    if not tcping:
        best_host, _ = chose_best_host(ipv6=chose_ipv6)
    else:
        best_host, _ = chose_best_hosts_both_46()
    resp = requests.post(url, f"domain:{self_domain} {best_host}", timeout=10)
    print(resp.content)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("type", help="执行类型", choices=["ipset_gfw", "ipset_custom", "xray", "check", "test", "xray_cluster", "domain"])
    parser.add_argument("-tpl", "--template", help="模版路径, only for xray")
    parser.add_argument("-td", "--target", help="配置写入路径, only for xray")
    parser.add_argument("-6", "--ipv6", action="store_true", help="生成ipv6, 否则生成ipv4")
    parser.add_argument("-t", "--tcping", action="store_true", help="使用是否tcping检测")
    parser.add_argument("-url", "--url", help="测试url, only for check")
    parser.add_argument("-c", "--concurrent", help="集群并发度, only for xray_cluster")

    args = parser.parse_args()

    if args.type == "ipset_gfw":
        common_gfw_txt_to_conf()
    elif args.type == "ipset_custom":
        custom_gfw_to_conf(args.ipv6)
    elif args.type == "xray":
        replace_template(args.template, args.target, args.ipv6, args.url, args.tcping)
    elif args.type == "xray_cluster":
        replace_cluster_template(args.template, args.target, args.ipv6, args.tcping, args.concurrent)
    elif args.type == "domain":
        update_domain(args.ipv6, args.tcping)
    elif args.type == "test":
        print(get_cfnode_hosts())


if __name__ == '__main__':
    parse_args()