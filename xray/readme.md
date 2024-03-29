## 1. update_domain  更新cloudflare域名信息
```shell
#!/bin/bash
cd /root/passwall
python gfw2dnsmasq.py domain -t
# /etc/init.d/self_xray restart
```

## 2. 检查被墙域名是否可以访问
```shell
#!/bin/bash

url="https://www.google.com"
response=$(curl --write-out "%{http_code}" --silent --output /dev/null $url)

if [ $response -ne 200 ]
then
    ./root/passwall/update_domain.sh
	/etc/init.d/self_xray restart
fi
```