> 生产环境DR配置，init参数在第一次启动服务时不触发同步，新建文件及文件夹时触发
- 创建用户 SyncUser，并配置免密登陆远程主机；
- mkdir /POC
- 根据目录结构放置配置文件
- chmod +x /etc/init.d/Sync_POC && chkconfig --add Sync_POC && /etc/init.d/Sync_POC start
