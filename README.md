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

#### HPC_monitor
- 创建工作目录/opt/ProcessMonitor
- 在配置文件中添加 REPLY_EMAIL 的值；邮件模版；添加发件用户及收件箱邮箱后缀
- namelist 以 username=example 字典形式存放
- sh stress_cpu.sh 运行测试脚本

#### Cleandata
- 创建空目录/opt/blank，利用 rsync 比对目录删除数据
- 替换变量 file
