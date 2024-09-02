#!/bin/bash

echo "$0 $1 $2 $3 $4 $5" > map_result
ipv6=`ip -f inet6 addr show dev eth1.10 | sed -n '2p' | awk -F' ' '{print $2}' | sed 's/.\{3\}$//'`
ipv4=$1
ipv4_port=$2
curl "http://192.168.31.3:3010/add_vmess?ip=${ipv4}&ps=ff-v4&port=${ipv4_port}"
curl "http://192.168.31.3:3010/add_vmess?ip=${ipv6}&ps=ff-v6&port=1071"
curl "http://192.168.31.3:3010/gen_config"