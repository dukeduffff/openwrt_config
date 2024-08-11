# 设置策略路由
ip rule add fwmark 1 table 100
ip route add local 0.0.0.0/0 dev lo table 100

#代理局域网设备
nft add table v2ray

# 创建set
nft add set inet v2ray gfwlist { type addr\; timeout 1h\; }
nft add element inet v2ray gfwlist { 198.18.0.0/15 timeout 0 }
nft add element inet v2ray gfwlist { 91.108.4.0/22 timeout 0 }
nft add element inet v2ray gfwlist { 91.108.8.0/22 timeout 0 }
nft add element inet v2ray gfwlist { 91.108.12.0/22 timeout 0 }
nft add element inet v2ray gfwlist { 91.108.20.0/22 timeout 0 }
nft add element inet v2ray gfwlist { 91.108.36.0/23 timeout 0 }
nft add element inet v2ray gfwlist { 91.108.38.0/23 timeout 0 }
nft add element inet v2ray gfwlist { 91.108.56.0/22 timeout 0 }
nft add element inet v2ray gfwlist { 149.154.160.0/20 timeout 0 }
nft add element inet v2ray gfwlist { 149.154.164.0/22 timeout 0 }
nft add element inet v2ray gfwlist { 149.154.172.0/22 timeout 0 }
nft add element inet v2ray gfwlist { 185.76.151.0/24 timeout 0 }
nft add element inet v2ray gfwlist { 2001:b28:f23d::/48 timeout 0 }
nft add element inet v2ray gfwlist { 2001:b28:f23f::/48 timeout 0 }
nft add element inet v2ray gfwlist { 2001:67c:4e8::/48 timeout 0 }
nft add element inet v2ray gfwlist { 2001:b28:f23c::/48 timeout 0 }
nft add element inet v2ray gfwlist { 2a0a:f280::/32 timeout 0 }

# 代理局域网设备
nft add chain v2ray prerouting { type filter hook prerouting priority 0 \; }
nft add rule v2ray prerouting mark 0xff return # 直连 0xff 流量
nft add rule v2ray prerouting ip daddr not in @gfwlist return  # 返回
nft add rule v2ray prerouting meta l4proto {tcp, udp} mark set 1 tproxy to 127.0.0.1:1070 accept # 转发至 V2Ray 12345 端口

# 代理网关本机
nft add chain v2ray output { type route hook output priority 0 \; }
nft add rule v2ray output mark 0xff return # 直连 0xff 流量
nft add rule v2ray output ip daddr not in @gfwlist
nft add rule v2ray output meta l4proto {tcp, udp} mark set 1 accept # 重路由至 prerouting

# DIVERT 规则
nft add table filter
nft add chain filter divert { type filter hook prerouting priority -150 \; }
nft add rule filter divert meta l4proto tcp socket transparent 1 meta mark set 1 accept