#!/bin/bash

echo "$0 $1 $2 $3 $4 $5" > map_result
tel_ipv6=`ip -f inet6 addr show dev pppoe-wan | sed -n '2p' | awk -F' ' '{print $2}' | sed 's/.\{3\}$//'`
cm_ipv6=`ip -f inet6 addr show dev pppoe-wan2 | sed -n '2p' | awk -F' ' '{print $2}' | sed 's/.\{3\}$//'`
tel_ipv4=`ip -f inet addr show dev pppoe-wan | sed -n '2p' | awk -F' ' '{print $2}' | sed 's/.\{0\}$//'`
ipv4=$1
ipv4_port=$2
curl "http://192.168.31.3:3010/add_vmess?ip=${tel_ipv4}&ps=tel-v4&port=1071"
curl "http://192.168.31.3:3010/add_vmess?ip=${ipv4}&ps=cm-v4&port=${ipv4_port}"
curl "http://192.168.31.3:3010/add_vmess?ip=${tel_ipv6}&ps=tel-v6&port=1071"
curl "http://192.168.31.3:3010/add_vmess?ip=${cm_ipv6}&ps=cm-v6&port=1071"
curl "http://192.168.31.3:3010/gen_config"
curl 'http://192.168.31.3:3010/send_message?title=网络变更&msg=网络变更，已更新配置'