
### 优选ip代码
```shell
#!/usr/bin/env bash
cd /root/media/cfst
curl -o cfip.zip https://zip.baipiao.eu.org/
unzip -o cfip.zip -d cfip
# cat cfip/*8443*.txt > ip.txt
./CloudflareST -tp 8443 -tll 20 -f ip.txt -o result.csv -url https://gh.con.sh/https://github.com/AaronFeng753/Waifu2x-Extension-GUI/releases/download/v2.21.12/Waifu2x-Extension-GUI-v2.21.12-Portable.7z
# 第一行
# best_ip=`sed -n '2p' result.csv | awk -F',' '{print $1}'`
best_ip=`sed '1d' result.csv | awk -F',' '$6 > 10 { print $1 }' | tr '\n' ' '`
if [ -z "$best_ip" ]; then
    curl -X POST -d "domain:327237.xyz 172.67.3.3" http://192.168.31.1:9091/plugins/hosts/update
else
    echo $best_ip
    curl -X POST -d "domain:327237.xyz $best_ip" http://192.168.31.1:9091/plugins/hosts/update
fi
#echo $best_ip
#curl -X POST -d "domain:327237.xyz $best_ip" http://192.168.31.1:9091/plugins/hosts/update
```