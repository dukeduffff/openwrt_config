#!/bin/bash

cd /root/cftest/
./CloudflareST -f 4ip.txt -url https://gh.con.sh/https://github.com/AaronFeng753/Waifu2x-Extension-GUI/releases/download/v2.21.12/Waifu2x-Extension-GUI-v2.21.12-Portable.7z
BEST_IP=`cat result.csv | tail -n +2 | head -n 1 | awk -F ',' '{print $1}'`
PING_TIME=`cat result.csv | tail -n +2 | head -n 1 | awk -F ',' '{print $5}'`
PING_TIME=`echo $PING_TIME | awk -F '.' '{print $1}'`
if [ $PING_TIME -le 100 ]; then
    echo "$BEST_IP/32" >> 4ip.txt
fi

cd /root/passwall/xray/
sed "s/BEST_IP/$BEST_IP/g" config.template > config.json
ps | grep xray | grep -v grep | awk '{print $1}' | xargs kill -9
/etc/init.d/xray start


# 21 * * * * bash /root/cftest/cf_best.sh >> /root/cftest/cron.log 2>&1