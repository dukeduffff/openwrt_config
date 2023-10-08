
## 新增挂载点
```
echo "UUID=7bfecac7-338c-4460-a44b-f24a46bdb115 /volume1/data1 ext4 defaults 0 0" >> /etc/fstab

mount /dev/sdb1 /volume1/data1/
```

## dsm开机启动配置
```
# mount /dev/sdb1 /volume1/data1/
synosystemctl disable pkgctl-SynoFinder
sleep 6m && sysctl -w vm.swappiness=1
```

## dsm第三方源
```
synocommunity社区: https://packages.synocommunity.com/
我不是旷神: https://spk7.imnks.com/
```


## pve挂载视频分区
mount -t cifs //192.168.31.3/media /root/jellyfin -o username=duke,nobrl
mount -t cifs //192.168.31.3/download /root/media -o username=duke,nobrl