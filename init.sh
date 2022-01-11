#!/bin/sh
#variable
export VERSION=19.03

function menu()
{
cat << EOF
-----------------------------------------
|************Menu Home Page ************|
-----------------------------------------
`echo -e "\033[35m 1) Modify NIC\033[0m"`
`echo -e "\033[35m 2) Disable ipv6\033[0m"`
`echo -e "\033[35m 3) Initialize\033[0m"`
`echo -e "\033[35m 4) online Docker\033[0m"`
`echo -e "\033[35m 5) offline Docker\033[0m"`
`echo -e "\033[35m 6) Quit\033[0m"`
EOF

read -p "Please input your number: " num

case $num in
1)
mv /etc/sysconfig/network-scripts/ifcfg-ens33 /etc/sysconfig/network-scripts/ifcfg-eth0
sed -i "s/ens33/eth0/g" /etc/sysconfig/network-scripts/ifcfg-eth0
sed -i '6{s/rhgb/rhgb net.ifnames=0 biosdevname=0/}' /etc/default/grub
grub2-mkconfig -o /boot/grub2/grub.cfg
reboot
;;
2)
echo "net.ipv6.conf.all.disable_ipv6=1" > /etc/sysctl.d/ipv6.conf
sysctl --system
echo "NETWORKING_IPV6=no" >> /etc/sysconfig/network
sed -i "s/IPV6INIT=\"yes\"/IPV6INIT=\"no\"/" /etc/sysconfig/network-scripts/ifcfg-eth0
systemctl restart NetworkManager.service
;;
3)
firewall-cmd --set-default-zone=trusted
firewall-cmd --complete-reload
setenforce 0
sed --follow-symlinks -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
sed -i 's/#UseDNS yes/UseDNS no/g' /etc/ssh/sshd_config
sed -i 's/GSSAPIAuthentication yes/GSSAPIAuthentication no/g' /etc/ssh/sshd_config
cat > /etc/sysctl.d/docker.conf << EOF
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
EOF
cat > /etc/security/limits.d/custom.conf << EOF
*       soft    nproc   131072
*       hard    nproc   131072
*       soft    nofile  131072
*       hard    nofile  131072
EOF
tuned-adm profile throughput-performance
grubby --args="user_namespace.enable=1" --update-kernel="$(grubby --default-kernel)"
reboot
;;
4)
curl -fsSL "https://get.docker.com/" | bash -s -- --mirror Aliyun
mkdir -p /etc/docker
cat > /etc/docker/daemon.json << EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "registry-mirrors": ["https://zmtsbovs.mirror.aliyuncs.com"],
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  }
}
EOF
systemctl enable --now docker.service
cp /usr/share/bash-completion/completions/docker /etc/bash_completion.d/
curl -L https://get.daocloud.io/docker/compose/releases/download/v2.2.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
;;
5)
tar xzvf docker-$VERSION.*.tgz
cp docker/* /usr/bin/
groupadd docker
mkdir -p /etc/docker
cat > /etc/docker/daemon.json << EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "registry-mirrors": ["https://zmtsbovs.mirror.aliyuncs.com"],
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m",
    "max-file": "3"
  }
}
EOF
cat > /etc/systemd/system/docker.service << EOF
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target

[Service]
Type=notify
ExecStart=/usr/bin/dockerd
ExecReload=/bin/kill -s HUP $MAINPID
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
TimeoutStartSec=0
Delegate=yes
KillMode=process
Restart=on-failure
StartLimitBurst=3
StartLimitInterval=60s

[Install]
WantedBy=multi-user.target
EOF
systemctl enable --now docker.service
curl -L https://get.daocloud.io/docker/compose/releases/download/v2.2.2/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
;;
6)
  exit 0
;;
*)
  echo 'Input error, please again!'
  exit 1
;;
esac
}

menu
