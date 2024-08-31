# 设置策略路由
ip rule add fwmark 1 table 100
ip route add local 0.0.0.0/0 dev lo table 100

#nft add table inet xray
#
## 创建set
#nft add set inet xray gfwlist { type ipv4_addr\; timeout 1h\; flags interval\; }
#nft add element inet xray gfwlist { 198.18.0.0/15 timeout 10000h }
#nft add element inet xray gfwlist { 91.108.4.0/22 timeout 10000h }
#nft add element inet xray gfwlist { 91.108.8.0/22 timeout 10000h }
#nft add element inet xray gfwlist { 91.108.12.0/22 timeout 10000h }
#nft add element inet xray gfwlist { 91.108.20.0/22 timeout 10000h }
#nft add element inet xray gfwlist { 91.108.36.0/23 timeout 10000h }
#nft add element inet xray gfwlist { 91.108.38.0/23 timeout 10000h }
#nft add element inet xray gfwlist { 91.108.56.0/22 timeout 10000h }
#nft add element inet xray gfwlist { 149.154.160.0/20 timeout 10000h }
#nft add element inet xray gfwlist { 185.76.151.0/24 timeout 10000h }
#nft add set inet xray gfwlist6 { type ipv6_addr\; timeout 1h\; flags interval\; }
#nft add element inet xray gfwlist6 { 2001:b28:f23d::/48 timeout 10000h }
#nft add element inet xray gfwlist6 { 2001:b28:f23f::/48 timeout 10000h }
#nft add element inet xray gfwlist6 { 2001:67c:4e8::/48 timeout 10000h }
#nft add element inet xray gfwlist6 { 2001:b28:f23c::/48 timeout 10000h }
#nft add element inet xray gfwlist6 { 2a0a:f280::/32 timeout 10000h }
#
## 代理局域网设备
#nft add chain inet xray prerouting { type filter hook prerouting priority 0 \; }
#nft add rule inet xray prerouting mark 0xff return # 直连 0xff 流量
#nft add rule inet xray prerouting ip daddr != @gfwlist return  # 返回
#nft add rule inet xray prerouting ip6 daddr != @gfwlist6 return  # 返回
#nft add rule inet xray prerouting meta l4proto {tcp, udp} mark set 1 tproxy to :1070 accept # 转发至 xray 12345 端口
#
## 代理网关本机
#nft add chain inet xray output { type route hook output priority 0 \; }
#nft add rule inet xray output mark 0xff return # 直连 0xff 流量
#nft add rule inet xray output ip daddr != @gfwlist return
#nft add rule inet xray output ip6 daddr != @gfwlist6 return
#nft add rule inet xray output meta l4proto {tcp, udp} mark set 1 accept # 重路由至 prerouting
#
## DIVERT 规则
#nft add table inet filter
#nft add chain inet filter divert { type filter hook prerouting priority -150 \; }
#nft add rule inet filter divert meta l4proto tcp socket transparent 1 meta mark set 1 accept