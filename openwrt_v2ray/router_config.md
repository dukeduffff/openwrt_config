echo 0 > /proc/sys/net/bridge/bridge-nf-call-iptables
echo 0 > /proc/sys/net/bridge/bridge-nf-call-ip6tables
echo 0 > /proc/sys/net/bridge/bridge-nf-call-arptables
echo 0 > /proc/sys/net/bridge/bridge-nf-call-custom

### 1. v2ray启动

```
#!/bin/sh /etc/rc.common

USE_PROCD=1
START=95
STOP=15

start_service() {
    procd_open_instance v2ray # 给服务实例定义一个名称
    procd_set_param command /root/passwall/v2ray/v2ray run -config /root/passwall/v2ray/config.json # 需要在前台被执行的服务
    # procd_append_param command -bar 42 # 给以上命令附加的指令参数

    # 如果服务意外中止了，定义 redpawn 可以自动重启它，如果服务命令的确只需要运行一次，需要谨慎设定这里
    # 如果进程在 respawn_threshold 定义的时间内结束了，则判定为进程崩溃并尝试重启它，尝试5次后会停止重启
    procd_set_param respawn ${respawn_threshold:-3600} ${respawn_timeout:-5} ${respawn_retry:-5}

    procd_set_param env SOME_VARIABLE=funtimes  # 给进程传递环境变量
    procd_set_param limits core="unlimited"  # If you need to set ulimit for your process
    # procd_set_param file /var/etc/your_service.conf # 如果此处定义的文件发生了变化，则会触发 /etc/init.d/your_service reload 重启进程
    procd_set_param netdev dev # likewise, except if dev's ifindex changes.
    procd_set_param data name=value ... # likewise, except if this data changes.
    procd_set_param stdout 1 # 转发 stdout 输出到 logd
    procd_set_param stderr 1 # same for stderr
    procd_set_param user root # 以 nobody 用户运行服务
    procd_set_param pidfile /var/run/somefile.pid # 在服务启动时写入一个 pid 文件，在停止服务时删除此 pid 文件
    procd_close_instance # 结束服务实例配置
}
stop_service() {
    ps | grep v2ray | grep -v grep | awk '{print $1}' | xargs kill -9
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

ipset create gfwlist hash:net
ipset add gfwlist 198.18.0.0/15
ipset add gfwlist 91.108.4.0/22
ipset add gfwlist 91.108.8.0/22
ipset add gfwlist 91.108.12.0/22
ipset add gfwlist 91.108.20.0/22
ipset add gfwlist 91.108.36.0/23
ipset add gfwlist 91.108.38.0/23
ipset add gfwlist 91.108.56.0/22
ipset add gfwlist 149.154.160.0/20
ipset add gfwlist 149.154.164.0/22
ipset add gfwlist 149.154.172.0/22

iptables -t nat -A PREROUTING -p tcp -m set --match-set gfwlist dst -j REDIRECT --to-port 1070
iptables -t nat -A OUTPUT -p tcp -m set --match-set gfwlist dst -j REDIRECT --to-port 1070
```