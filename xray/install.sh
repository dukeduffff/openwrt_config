#!/bin/bash
echo_self () {
  echo -ne "\r $1"
}

check_pkg_and_install() {
  if ! command -v "$1" > /dev/null 2>&1 ; then
    echo_self "install $1"
    opkg install "$1"
  fi
  return $?
}

run_without_output() {
#  "$@" > /dev/null 2>&1
  "$@"
}

current_dir=$(pwd)
echo_self "opkg更新"
#run_without_output opkg update

#check_pkg_and_install unzip
#check_pkg_and_install wget

TMP_DOWNLOAD="/tmp/xray_install"
INSTALL_PATH="/root/passwall"
#XRAY_URL="https://github.com/XTLS/Xray-core/releases/download/v1.8.23/Xray-linux-64.zip"
XRAY_URL="https://gh-proxy.com/https://github.com/XTLS/Xray-core/releases/download/v24.12.31/Xray-linux-64.zip"
# https://github.com/Loyalsoldier/v2ray-rules-dat
GFW_URL="https://cdn.jsdelivr.net/gh/Loyalsoldier/v2ray-rules-dat@release/gfw.txt"
# ip cn 列表
GEO_IP_URL = 'https://github.com/mayaxcn/china-ip-list'

rm -rf ${TMP_DOWNLOAD}/*
rm -rf ${INSTALL_PATH}/*

if [ ! -d "$TMP_DOWNLOAD" ];then
  echo_self "创建临时目录"
  run_without_output mkdir -p "$TMP_DOWNLOAD"
fi

if [ ! -d "$INSTALL_PATH" ];then
  echo_self "创建安装目录"
  run_without_output mkdir -p "$INSTALL_PATH"
fi

cd ${TMP_DOWNLOAD}

echo_self "下载xray"
run_without_output wget -O xray.zip ${XRAY_URL}
run_without_output unzip xray.zip -d ./xray
run_without_output cp -r ./xray/* ${INSTALL_PATH}

cd "${current_dir}"
chmod +x ./xray_autoboot.sh
run_without_output cp ./config.json ./xray_autoboot.sh ./notify.sh ./99-xray.nft ${INSTALL_PATH}
run_without_output cp ./direct.txt ${INSTALL_PATH}
chmod +x ./xray
run_without_output cp ./xray /etc/init.d/
run_without_output /etc/init.d/xray enable  # 开机自启xray进程

#sed -i "/exit(0);/r bash ${INSTALL_PATH}/xray_autoboot.sh" /etc/rc.local

cd ${INSTALL_PATH}
#wget -O gfw.txt ${GFW_URL}
bash ./xray_autoboot.sh

/etc/init.d/xray start