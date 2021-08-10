# Scripts
存放日常工作中的脚本

#### Harbor
- 如果是 https 协议，必须在机器上导入证书
``` bash
yum -y install ca-certificates && update-ca-trust enable
cp harbor.example.com.crt /etc/pki/ca-trust/source/anchors/
update-ca-trust extract && systemctl restart docker
