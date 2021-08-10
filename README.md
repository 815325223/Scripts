# Scripts
存放日常工作中的脚本

#### Harbor
- 如果是 https 协议，必须在机器上导入证书
``` bash
yum -y install ca-certificates && update-ca-trust enable
cp harbor.example.com.crt /etc/pki/ca-trust/source/anchors/
update-ca-trust extract && systemctl restart docker
```
#### Zabbix
- pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pyzabbix requests
- 配置告警邮箱和 Zabbix API
- 测试命令 python mail_with_graph.py example@qq.com 'Title' 'This is just a test mail.' withgraph
- 指定告警脚本路径和设置正确的权限
- 配置 media type 和 action
