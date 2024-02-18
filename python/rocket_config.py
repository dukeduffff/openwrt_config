import base64

# https://github.com/GMOogway/shadowrocket-rules?tab=readme-ov-file
import requests

gfw_url = "https://cdn.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/gfw.txt"

ad_url_list = [
    "https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt",
    "https://anti-ad.net/easylist.txt",
    "https://mirror.ghproxy.com/https://raw.githubusercontent.com/217heidai/adblockfilters/main/rules/AdGuard_Base_filter.txt"
]


DOMAIN_SUFFIX = "DOMAIN_SUFFIX"
PROXY_COMMAND = "Proxy"
REJECT_COMMAND = "Reject"


def line_format(type, content, command):
    return f"{type},{content},{command}"


def header():
    return [
        # "[General]",
        "# 默认关闭 ipv6 支持，如果需要请手动开启",
        "ipv6 = false",
        "bypass-system = true",
        "skip-proxy = 192.168.0.0/16, 10.0.0.0/8, 172.16.0.0/12, localhost, *.local, e.crashlytics.com, captive.apple.com, sequoia.apple.com, seed-sequoia.siri.apple.com",
        "bypass-tun = 10.0.0.0/8,100.64.0.0/10,127.0.0.0/8,169.254.0.0/16,172.16.0.0/12,192.0.0.0/24,192.0.2.0/24,192.88.99.0/24,192.168.0.0/16,198.18.0.0/15,198.51.100.0/24,203.0.113.0/24,224.0.0.0/4,255.255.255.255/32",
        # "dns-server = https://1.12.12.12/dns-query, https://223.5.5.5/dns-query",
    ]


def gfw():
    # [Rule]
    gfw_rules = []
    # 添加telegram
    gfw_rules.extend([
        "IP-CIDR,91.108.56.0/22,Proxy",
        "IP-CIDR,91.108.4.0/22,Proxy",
        "IP-CIDR,91.108.8.0/22,Proxy",
        "IP-CIDR,91.108.16.0/22,Proxy",
        "IP-CIDR,91.108.12.0/22,Proxy",
        "IP-CIDR,149.154.160.0/20,Proxy",
        "IP-CIDR,91.105.192.0/23,Proxy",
        "IP-CIDR,91.108.20.0/22,Proxy",
        "IP-CIDR,185.76.151.0/24,Proxy",
        "IP-CIDR,2001:b28:f23d::/48,Proxy",
        "IP-CIDR,2001:b28:f23f::/48,Proxy",
        "IP-CIDR,2001:67c:4e8::/48,Proxy",
        "IP-CIDR,2001:b28:f23c::/48,Proxy",
        "IP-CIDR,2a0a:f280::/32,Proxy",
    ])
    resp = requests.get(gfw_url, timeout=5)
    content = resp.content.decode("utf-8")
    for line in content.strip().split("\n"):
        line = line.strip()
        gfw_rules.append(line_format(DOMAIN_SUFFIX, line, PROXY_COMMAND))
    return gfw_rules


def ad():
    rules = []
    for url in ad_url_list:
        resp = requests.get(url, timeout=5)
        content = resp.content.decode("utf-8")
        for line in content.strip().split("\n"):
            line = line.strip()
            if not line.startswith("||"):
                continue
            line = line.replace("^", "")
            rules.append(line_format(DOMAIN_SUFFIX, line, REJECT_COMMAND))
    return rules


def tail():
    pass


def entrance():
    pass


if __name__ == '__main__':
    print(gfw())
