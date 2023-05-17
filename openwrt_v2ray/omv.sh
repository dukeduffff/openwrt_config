docker run -d --restart=always --name vaultwarden  \
-v /root/bitwarden:/data/  \
-p 8081:80 \
-p 3012:3012 \
-e SIGNUPS_ALLOWED=false \
-e WEBSOCKET_ENABLED=true \
vaultwarden/server:latest


https://bitwarden.openmv.dynv6.net:1234/