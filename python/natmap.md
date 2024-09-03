# natmap notify.sh
```shell
#!/bin/bash

echo "$0 $1 $2 $3 $4 $5" > map_result
ipv6=`ip -f inet6 addr show dev eth1.10 | sed -n '2p' | awk -F' ' '{print $2}' | sed 's/.\{3\}$//'`
ipv4=$1
ipv4_port=$2
curl "http://192.168.31.3:3010/add_vmess?ip=${ipv4}&ps=ff-v4&port=${ipv4_port}"
curl "http://192.168.31.3:3010/add_vmess?ip=${ipv6}&ps=ff-v6&port=1071"
curl "http://192.168.31.3:3010/gen_config"
```

# 生成订阅信息
```python
import argparse
import base64


def gen_config(outer_ip, outer_port, fp):
    vmess_uri = f"none:1f8f05a1-1a29-4862-a91a-ecb2a4a5e272@{outer_ip}:{outer_port}"
    b64_vmess_uri = base64.b64encode(vmess_uri.encode("utf-8")).decode("utf-8")
    vmess_url = f"vmess://{b64_vmess_uri}?remarks=ff-v4&path=/home&obfs=none&tfo=1&mux=1&alterId=0"
    fd = open(fp, "w")
    b64_vmess_url = base64.b64encode(vmess_url.encode("utf-8")).decode("utf-8")
    fd.write(b64_vmess_url + "\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="外部ip")
    parser.add_argument("port", type=int, help="外部端口")
    parser.add_argument("fp", help="写入文件地址")
    args = parser.parse_args()
    gen_config(outer_ip=args.ip, outer_port=args.port, fp=args.fp)

```