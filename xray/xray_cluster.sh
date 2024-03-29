#!/bin/sh /etc/rc.common

USE_PROCD=1
START=95
STOP=15
#STOP_CMD="cat /var/run/xray.pid | xargs kill -9"
START_CMD="/root/passwall/xray/xray run -config /root/passwall/xray/config_cluster.json"

start_service() {
    echo "start xray"
    procd_open_instance xray_cluster # 给服务实例定义一个名称
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
    procd_set_param pidfile /var/run/xray_cluster.pid # 在服务启动时写入一个 pid 文件，在停止服务时删除此 pid 文件
    procd_close_instance # 结束服务实例配置
}

stop_service() {
    echo "stop xray"
    cat /var/run/xray_cluster.pid | xargs kill -9
}

restart_service() {
    stop
    start
}