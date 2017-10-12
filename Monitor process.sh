#!/bin/bash
#author: Jay.Cheng
#date: 2015-12-17
#role: Monitor the Serv-U service
#Usage: */5 * * * * /bin/bash /root/monitor.sh >> /root/monitor.log 2>&1
##################################################
process_name="/usr/local/Serv-U/Serv-U"
process_count=1

process_number()
{
        number=`ps -ef | grep ${process_name} | grep -v grep | wc -l`
        return ${number}
}

process_number

p_num=$?

now=`date '+%Y-%m-%d %H:%M:%S'`

if [ ${p_num} -lt ${process_count} ]
then
        "/usr/local/Serv-U/Serv-U" -startservice
        echo "[$now] [ERROR] '$process_name' process_number is $p_num."
        echo "Please check the service!." | mail -s "SFTP notification" jay@example.com
else
        echo "[$now] [DEBUG] '$process_name' process_number is $p_num, status ok."