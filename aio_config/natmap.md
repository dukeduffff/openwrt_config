# natmap notify.sh
```
#!/bin/bash

echo "$0 $1 $2 $3 $4 $5" > /root/natmap/map_result
> /www/subscribe/shadowrocket/config.txt
python rocket_subscribe.py $1 $2 /www/subscribe/shadowrocket/config.txt
```

# 生成订阅信息
```
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