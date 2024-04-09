
# cloudflared配置
```shell
#!/bin/sh /etc/rc.common

START=99

USE_PROCD=1
NAME=cloudflared
PROG=/usr/bin/cloudflared

start_service() {
        procd_open_instance
        procd_set_param command "$PROG" --no-autoupdate --edge-ip-version 6 tunnel run --protocol http2 --token eyJhIjoiYzIyMzc0YmNmYjUwNzE3Y2ZlZDhlZDZiZGM4NTJiNTciLCJ0IjoiZThlMjMzOTEtY2QwNi00ZDQ5LTkxZmItMjVjZTU3ZGJhZDM0IiwicyI6Ik9UTmtPVGRqTWpVdE5HWTBNeTAwWm1ZMUxXSmxZMkV0Tm1aa1pHSmhPVGhtTkRrNCJ9
        procd_set_param respawn
        procd_set_param stdout 1
        procd_set_param stderr 1
        procd_set_param pidfile /var/run/cloudflared.pid
        procd_close_instance
}
```