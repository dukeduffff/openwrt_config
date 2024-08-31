## 1. update_domain  更新cloudflare域名信息
```shell
#!/bin/bash
cd /root/passwall
python gfw2dnsmasq.py domain -t
# /etc/init.d/self_xray restart
```

## 2. check_passwall.sh 检查被墙域名是否可以访问
```shell
#!/bin/bash

url="https://www.google.com"
response=$(curl --write-out "%{http_code}" --connect-timeout 10 --silent --output /dev/null $url)
# 第一次检测仅重启
if [ $response -ne 200 ]
then
	/etc/init.d/self_xray restart
	python /root/passwall/tool_kit.py msg --title 网络连接 --msg 连接谷歌出现问题,重启服务
else
	echo '检查通过'
	exit 0
fi

response=$(curl --write-out "%{http_code}" --connect-timeout 10 --silent --output /dev/null $url)
# 第二次检测, 重新获取域名解析并重启
if [ $response -ne 200 ]
then
	python /root/passwall/tool_kit.py msg --title 网络连接 --msg 连接谷歌出现问题,请手动处理
fii
```

```shell
table inet dnsmasq {
    chain prerouting {
        type nat hook prerouting priority dstnat - 5; policy accept;
        meta nfproto { ipv4, ipv6 } udp dport 53 counter packets 430 bytes 34012 redirect to :53 comment "DNSMASQ HIJACK"
    }
}
```