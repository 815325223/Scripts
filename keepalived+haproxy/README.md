#### killall: command not found
```bash
yum install -y psmisc

#### keepalived模式切换
M和B的state类型均为BACKUP，同时设置为nopreempt不抢占模式。首先启动M，后启动B，由于M的优先级为100，B不会抢占VIP；\
M宕机时，B称为主，接着M恢复正常，由于nopreempt模式，所以M不会抢夺VIP，B继续为主，防止频繁切换VIP所在的主机。
