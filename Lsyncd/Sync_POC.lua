settings {
    logfile = "/var/log/Sync_POC/Sync_POC.log",
    statusFile = "/var/log/Sync_POC/Sync_POC-status.log",
    statusInterval = 10
}

sync {
    default.rsync,
    source = "/POC",
    target = "client.devops.com:/POC",
    init = false,
    rsync = {
        compress = true,
        acls = true,
        verbose = true,
        rsh = "/usr/bin/ssh -p 22 -o StrictHostKeyChecking=no -i /home/SyncUser/.ssh/id_rsa -l SyncUser" }
}
