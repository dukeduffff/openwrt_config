# 更新pve源
echo "deb https://mirrors.ustc.edu.cn/proxmox/debian/pve bullseye pve-no-subscription" > /etc/apt/sources.list.d/pve-no-subscription.list
# 删除之前
sed -i.bak "s#ftp.debian.org/debian#mirrors.aliyun.com/debian#g" /etc/apt/sources.list
sed -i "s#security.debian.org#mirrors.aliyun.com/debian-security#g" /etc/apt/sources.list

# 直通
/etc/default/grub
GRUB_CMDLINE_LINUX_DEFAULT="quiet intel_iommu=on"
sed -i 's/quiet/quiet intel_iommu=on/g' /etc/default/grub
echo -e 'vfio\nvfio_iommu_type1\nvfio_pci\nvfio_virqfd' >> /etc/modules

update-grub
update-initramfs -u -k all

# lxc安装
lxc.apparmor.profile: unconfined  
lxc.cgroup.devices.allow: a  
lxc.cap.drop:
lxc.cgroup2.devices.allow: c 226:0 rwm
lxc.cgroup2.devices.allow: c 226:128 rwm
lxc.mount.entry: /dev/dri/card0 dev/dri/card0 none bind,optional,create=file
lxc.mount.entry: /dev/dri/renderD128 dev/dri/renderD128 none bind,optional,create=file

apt install docker.io
docker pull nyanmisaka/jellyfin:latest
# 参考： https://www.bilibili.com/read/cv14514123?msource=smzdm_937_0_184__276a8519ee7f1660

sudo docker run -d --name=Jellyfin -p 8096:8096 \  # --name=Jellyfin 将容器名定义为 Jellyfin 
	-p 8920:8920 -p 7359:7359/udp -p 1900:1900/udp #这三个端口为可选项 \
	-v /root/jellyfin/config:/config -v /root/jellyfin/cache:/cache -v /root/media:/media \
	-e TZ=Asia/Shanghai -e PUID=0 -e PGID=0 \	#将容器的时区设为上海,使用窗口在运行时使用root权限
	--device=/dev/dri:/dev/dri \	#直通显卡给 Docker 容器，用于硬解
	--add-host=api.themoviedb.org:13.224.161.90 \	#为容器增加 host 指向，加速海报与影视元数据的搜刮
	--add-host=api.themoviedb.org:13.35.8.65 \
	--add-host=api.themoviedb.org:13.35.8.93 \
	--add-host=api.themoviedb.org:13.35.8.6 \
	--add-host=api.themoviedb.org:13.35.8.54 \
	--add-host=image.tmdb.org:138.199.37.230 \
	--add-host=image.tmdb.org:108.138.246.49 \
	--add-host=api.thetvdb.org:13.225.89.239 \
	--add-host=api.thetvdb.org:192.241.234.54 \
	--restart unless-stopped \
	nyanmisaka/jellyfin:latest

	#如果使用 linuxserver/jellyfin 镜像，就把最后一行替换为下行
	lscr.io/linuxserver/jellyfin:latest
	#如果使用 nyanmisaka/jellyfin  镜像，最把最后一行替换为下行
	nyanmisaka/jellyfin:latest

docker run -d --name=Jellyfin -p 8096:8096 \
	-p 8920:8920 -p 7359:7359/udp -p 1900:1900/udp \
	-v /root/jellyfin/config:/config -v /root/jellyfin/cache:/cache -v /root/media:/media \
	-e TZ=Asia/Shanghai -e PUID=0 -e PGID=0 \
	--device=/dev/dri:/dev/dri \
	--add-host=api.themoviedb.org:13.224.161.90 \
	--add-host=api.themoviedb.org:13.35.8.65 \
	--add-host=api.themoviedb.org:13.35.8.93 \
	--add-host=api.themoviedb.org:13.35.8.6 \
	--add-host=api.themoviedb.org:13.35.8.54 \
	--add-host=image.tmdb.org:138.199.37.230 \
	--add-host=image.tmdb.org:108.138.246.49 \
	--add-host=api.thetvdb.org:13.225.89.239 \
	--add-host=api.thetvdb.org:192.241.234.54 \
	--restart unless-stopped \
	nyanmisaka/jellyfin:latest
# 挂载smb
apt install cifs-utils
mount -t cifs //192.168.31.3/download /root/media -o username=duke,nobrl
mount -t cifs //192.168.31.3/media /root/jellyfin -o username=duke,nobrl

# 挂载webdav
apt install davfs2
mount -t davfs http://dsm.openmv.dynv6.net:5005/download /root/media

# 核显直通 9500T

args: -device vfio-pci,host=00:02.0,addr=0x02,x-pci-device-id=0x3E92





261010087356
33848492


qm set 101 -sata1 /dev/disk/by-id/ata-ST2000DM005-2CW102_ZFM0G0QB

/var/lib/vz/template/iso/openwrt.img

qm importdisk 100 /var/lib/vz/template/iso/openwrt.img local-lvm
qm importdisk 100 /var/lib/vz/template/iso/openwrt-05.09.2023-x86-64-generic-squashfs-combined-efi.img local-lvm
qm importdisk 100 /var/lib/vz/template/iso/openwrt.img local-lvm


ip=`curl 6.ipw.cn`; curl "http://dynv6.com/api/update?hostname=openmv.dynv6.net&token=HBsK6jctuYNRDd2pAYaC3-k_CtvxC7&ipv6=$ip"



http://dynv6.com/api/update?hostname=openmv.dynv6.net&token=HBsK6jctuYNRDd2pAYaC3-k_CtvxC7&ipv6=2409:8a00:5469:5bd0:7680:8956:7f7a:74a7

acme.sh --issue --dns dns_dynv6 -d openmv.dynv6.net -d *.openmv.dynv6.net

acme.sh --install-cert -d openmv.dynv6.net \
--key-file       /root/cert/key.pem  \
--fullchain-file /root/cert/cert.pem \
--reloadcmd     "service nginx force-reload"


acme.sh  --remove  -d openmv.dynv6.net

wget -O - https://github.com/OpenMediaVault-Plugin-Developers/packages/raw/master/install | bash


docker run --name webdav --restart always -v /root/webdav:/var/lib/dav -e AUTH_TYPE=Digest -e USERNAME=dujian -e PASSWORD=22372901 --publish 8972:80 -d bytemark/webdav




server {
    # 服务器端口使用443，开启ssl, 这里ssl就是上面安装的ssl模块
    listen       *:443 ssl;
    listen       [::]:1234 ssl;
    # 域名，多个以空格分开
    server_name  openmv.dynv6.net;
    
    # ssl证书地址
    ssl_certificate      /root/cert/cert.pem;  # pem文件的路径
    ssl_certificate_key  /root/cert/key.pem; # key文件的路径
    
    # ssl验证相关配置
    ssl_session_timeout  5m;    #缓存有效期
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE:ECDH:AES:HIGH:!NULL:!aNULL:!MD5:!ADH:!RC4;    #加密算法
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;    #安全链接可选的加密协议
    ssl_prefer_server_ciphers on;   #使用服务器端的首选算法

    location /openwrt {
        proxy_http_version 1.1; #代理使用的http协议
        proxy_set_header Host $host; #header添加请求host信息
        proxy_set_header X-Real-IP $remote_addr; # header增加请求来源IP信息
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; # 增加代理记录
        proxy_pass http://192.168.31.1; #服务A访问地址
    }
}
server {
    listen       80; #监听端口
    server_name  openmv.dynv6.net; #请求域名
    return      301 https://$host:1234$request_uri; #重定向至https访问。
}

docker run -d --name=webdav --restart=always -v /path/config.yml:/config.yml -p 8080:8080 stilleshan/webdav


docker run --name some-sftpgo \
    -p 8080:8080 \
    -p 2022:2022 \
    -p 8972:8972 \
    --mount type=bind,source=/root/webdav,target=/srv/sftpgo \
    -e SFTPGO_WEBDAVD__BINDINGS__0__PORT=8972 \
    -d "drakkan/sftpgo"

https://omv.openmv.dynv6.net:1234/


docker run --name webdav \
  --restart=unless-stopped \
  -p 8972:80 \
  -v /root/webdav/dav:/media \
  -e USERNAME=dujian \
  -e PASSWORD=22372901 \
  -e TZ=Asia/Shanghai  \
  -e UDI=1000 \
  -e GID=1000 \
  -d  ugeek/webdav:amd64



0:0:0:0:0:ffff:c0a8:1f05

0000:0000:0000:0000:0000:0000:c0a8:1f05
0:0:0:0:0:0:c0a8:1f05
