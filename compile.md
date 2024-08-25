
autocore base-files bash block-mount busybox ca-bundle coremark curl dnsmasq-full dropbear ds-lite e2fsprogs fdisk firewall4 fstools grub2-bios-setup htop kmod-8139cp kmod-8139too kmod-alx kmod-amazon-ena kmod-amd-xgbe kmod-bnx2 kmod-bnx2x kmod-button-hotplug kmod-drm-amdgpu kmod-drm-i915 kmod-e1000 kmod-e1000e kmod-forcedeth kmod-fs-vfat kmod-i40e kmod-iavf kmod-igb kmod-igbvf kmod-igc kmod-ixgbe kmod-ixgbevf kmod-lib-zstd kmod-mlx4-core kmod-mlx5-core kmod-mmc kmod-pcnet32 kmod-phy-broadcom kmod-r8101 kmod-r8125 kmod-r8126 kmod-r8168 kmod-sdhci kmod-tcp-bbr kmod-tg3 kmod-tulip kmod-usb-hid kmod-vmxnet3 libc libgcc libustream-mbedtls lm-sensors-detect logd lsblk luci-app-advancedplus luci-app-autoreboot luci-app-fan luci-app-fileassistant luci-app-firewall luci-app-opkg luci-app-upnp luci-app-wizard luci-base luci-compat luci-lib-fs luci-lib-ipkg mkf2fs mtd nano netifd odhcp6c odhcpd-ipv6only openssh-sftp-server opkg partx-utils pciutils ppp ppp-mod-pppoe procd resolveip swconfig uci uclient-fetch urandom-seed urngd usbutils wget-ssl zram-swap luci-app-adguardhome luci-app-mosdns luci-app-ddns luci-app-store luci-app-argon-config

```shell
# 密码
root_password="22372901"

# root密码
if [ -n "$root_password" ]; then
  (echo "$root_password"; sleep 1; echo "$root_password") | passwd > /dev/null
fi

# wan 拨号 pppoe 协议
pppoe_username="261010087356"
pppoe_password="33848492"
# wan 其它协议
# wan_proto="dhcp"

# Wan pppoe 协议
# More options: https://openwrt.org/docs/guide-user/network/wan/wan_interface_protocols#protocol_pppoe_ppp_over_ethernet
if [ -n "$pppoe_username" -a "$pppoe_password" ]; then
  uci set network.wan.proto=pppoe
  uci set network.wan.username="$pppoe_username"
  uci set network.wan.password="$pppoe_password"
  uci commit network
fi

# WAN 其它协议
if [ -n "$wan_proto" ]; then
  uci set network.wan.proto="$wan_proto"
  uci commit network
fi

# 主机名，时区
host_name="OpenWrt-duke"
zone_name="Asia/Shanghai"
# 主机名
if [ -n "$host_name" ]; then
    uci set system.@system[0].hostname="$host_name"
    uci commit system
fi

# 时区
if [ -n "$zone_name" ]; then
    uci set system.@system[0].zonename="$zone_name"
    uci set system.@system[0].timezone='UTC-8'
    uci commit system
    /etc/init.d/system reload
fi

# lan 静态协议地址
lan_ip_address="192.168.31.1"
lan_netmask="255.255.255.0"

# lan 其它协议
#lan_proto="dhcp"

# LAN 静态协议
# More options: https://openwrt.org/docs/guide-user/base-system/basic-networking
if [ -n "$lan_ip_address" ]; then
  uci set network.lan.proto='static'
  uci set network.lan.ipaddr="$lan_ip_address"
  uci set network.lan.netmask="$lan_netmask"
  uci commit network
fi

# LAN 其它协议
# More options: https://openwrt.org/docs/guide-user/base-system/basic-networking
if [ -n "$lan_proto" ]; then
  uci set network.lan.proto="$lan_proto"
  uci commit network
fi
```