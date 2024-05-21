
### 1. v2ray启动

```
#!/bin/sh /etc/rc.common

USE_PROCD=1
START=95
STOP=15
#STOP_CMD="cat /var/run/xray.pid | xargs kill -9"
START_CMD="/root/passwall/xray/xray run -config /root/passwall/xray/config.json"

start_service() {
    echo "start xray"
    procd_open_instance xray # 给服务实例定义一个名称
    procd_set_param command $START_CMD # 需要在前台被执行的服务
    # procd_append_param command -bar 42 # 给以上命令附加的指令参数

    # 如果服务意外中止了，定义 redpawn 可以自动重启它，如果服务命令的确只需要运行一次，需要谨慎设定这里
    # 如果进程在 respawn_threshold 定义的时间内结束了，则判定为进程崩溃并尝试重启它，尝试5次后会停止重启
    procd_set_param respawn ${respawn_threshold:-3600} ${respawn_timeout:-5} ${respawn_retry:-5}

    procd_set_param env SOME_VARIABLE=funtimes  # 给进程传递环境变量
    # procd_set_param limits core="unlimited"  # If you need to set ulimit for your process
    # procd_set_param file /var/etc/your_service.conf # 如果此处定义的文件发生了变化，则会触发 /etc/init.d/your_service reload 重启进程
    # procd_set_param netdev dev # likewise, except if dev's ifindex changes.
    # procd_set_param data name=value ... # likewise, except if this data changes.
    procd_set_param stdout 1 # 转发 stdout 输出到 logd
    procd_set_param stderr 1 # same for stderr
    procd_set_param user root # 以 nobody 用户运行服务
    procd_set_param pidfile /var/run/xray.pid # 在服务启动时写入一个 pid 文件，在停止服务时删除此 pid 文件
    procd_close_instance # 结束服务实例配置
}

stop_service() {
    echo "stop xray"
    cat /var/run/xray.pid | xargs kill -9
}

restart_service() {
    stop
    start
}
```

### 2. 启动命令
```
cp /root/passwall/gfw_custom.conf /tmp/dnsmasq.d/
cp /root/passwall/gfwlist.conf /tmp/dnsmasq.d/

/etc/init.d/dnsmasq restart

ipset create gfwlist hash:net timeout 3600 hashsize 10000 maxelem 100000
# ipset add gfwlist 198.18.0.0/15
ipset add gfwlist 91.108.4.0/22 timeout 0
ipset add gfwlist 91.108.8.0/22 timeout 0
ipset add gfwlist 91.108.12.0/22 timeout 0
ipset add gfwlist 91.108.20.0/22 timeout 0
ipset add gfwlist 91.108.36.0/23 timeout 0
ipset add gfwlist 91.108.38.0/23 timeout 0
ipset add gfwlist 91.108.56.0/22 timeout 0
ipset add gfwlist 149.154.160.0/20 timeout 0
ipset add gfwlist 149.154.164.0/22 timeout 0
ipset add gfwlist 149.154.172.0/22 timeout 0
ipset add gfwlist 185.76.151.0/24 timeout 0

iptables -t nat -N V2RAY
iptables -t nat -A V2RAY -j RETURN -m mark --mark 0xff
iptables -t nat -A V2RAY -p tcp -m set --match-set gfwlist dst -j REDIRECT --to-port 1070
iptables -t nat -A PREROUTING -j V2RAY


iptables -t nat -N V2RAY_MASK
iptables -t nat -A V2RAY_MASK -j RETURN -m mark --mark 0xff
iptables -t nat -A V2RAY_MASK -p tcp -m set --match-set gfwlist dst -j REDIRECT --to-port 1070
iptables -t nat -A OUTPUT -j V2RAY_MASK

ipset create gfwlist6 hash:net family inet6 timeout 3600 hashsize 10000 maxelem 100000
ipset add gfwlist6 2001:b28:f23d::/48 timeout 0
ipset add gfwlist6 2001:b28:f23f::/48 timeout 0
ipset add gfwlist6 2001:67c:4e8::/48 timeout 0
ipset add gfwlist6 2001:b28:f23c::/48 timeout 0
ipset add gfwlist6 2a0a:f280::/32 timeout 0

ip6tables -t nat -N V2RAY6
ip6tables -t nat -A V2RAY6 -j RETURN -m mark --mark 0xff
ip6tables -t nat -A V2RAY6 -p tcp -m set --match-set gfwlist6 dst -j REDIRECT --to-port 1070
ip6tables -t nat -A PREROUTING -j V2RAY6


ip6tables -t nat -N V2RAY_MASK6
ip6tables -t nat -A V2RAY_MASK6 -j RETURN -m mark --mark 0xff
ip6tables -t nat -A V2RAY_MASK6 -p tcp -m set --match-set gfwlist6 dst -j REDIRECT --to-port 1070
ip6tables -t nat -A OUTPUT -j V2RAY_MASK6

/etc/init.d/ddns restart
/etc/init.d/nlbwmon restart

```

### 3. 小米路由器旁路由配置
```
echo 0 > /proc/sys/net/bridge/bridge-nf-call-iptables
echo 0 > /proc/sys/net/bridge/bridge-nf-call-ip6tables
echo 0 > /proc/sys/net/bridge/bridge-nf-call-arptables
echo 0 > /proc/sys/net/bridge/bridge-nf-call-custom
```

### 4. 重装流程
#### 1. 备份
1. 宽带账号密码
261010087356
33848492
2. v2ray配置
#### 2. 安装
1. 替换镜像, 然后恢复出厂


### 5. warp安装说明
```
https://github.com/fscarmen/warp
https://github.com/pufferffish/wireproxy

warp优选:
https://blog.misaka.rest/2023/03/12/cf-warp-yxip/

workers创建vless协议
https://jdssl.top/index.php/2023/07/21/2023vpn/?__cf_chl_tk=5b2rH74paFlUZYNMmBiBRT515ghCbt7DgdtGGjYzoOg-1693450307-0-gaNycGzNCvs
```

### gfw定时更新
```
```

### 测速地址
```shell
https://gh.con.sh/https://github.com/AaronFeng753/Waifu2x-Extension-GUI/releases/download/v2.21.12/Waifu2x-Extension-GUI-v2.21.12-Portable.7z
https://gh.api.99988866.xyz/https://github.com/AaronFeng753/Waifu2x-Extension-GUI/releases/download/v2.21.12/Waifu2x-Extension-GUI-v2.21.12-Portable.7z
http://gh.msx.workers.dev/https://github.com/AaronFeng753/Waifu2x-Extension-GUI/releases/download/v2.21.12/Waifu2x-Extension-GUI-v2.21.12-Portable.7z
https://github.91chifun.workers.dev/https://github.com/AaronFeng753/Waifu2x-Extension-GUI/releases/download/v2.21.12/Waifu2x-Extension-GUI-v2.21.12-Portable.7z
https://gh-proxy.henryjiu.workers.dev/https://github.com/AaronFeng753/Waifu2x-Extension-GUI/releases/download/v2.21.12/Waifu2x-Extension-GUI-v2.21.12-Portable.7z

```