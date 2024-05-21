
## 定时更新gfw脚本
```shell
10 * * * * bash /root/passwall/update.sh

#!/bin/bash
cd /root/passwall
python gfw2dnsmasq.py ipset_gfw
cp /root/passwall/gfwlist.conf /tmp/dnsmasq.d/
/etc/init.d/dnsmasq restart
```

## 定时更新自定义ipset
```shell
*/10 * * * * bash /root/passwall/update_custom.sh

#!/bin/bash
cd /root/passwall
python gfw2dnsmasq.py ipset_custom
cp /root/passwall/gfw_custom.conf /tmp/dnsmasq.d/
/etc/init.d/dnsmasq restart
/etc/init.d/xray restart
```

## 定时更新xray配置
```shell
*/10 * * * * bash /root/passwall/update_xray.sh

cd /root/passwall
python gfw2dnsmasq.py xray -tpl /root/passwall/template.json -td /root/passwall/xray/config.json -url https://www.google.com
if [ $? -eq 1 ]; then
    /etc/init.d/xray restart
fi
```


## 检查json