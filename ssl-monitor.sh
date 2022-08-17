#!/bin/bash
WebName=$1
Port="443"

Cert_END_Time=$(echo | openssl s_client -servername ${WebName} -connect ${WebName}:${Port} 2> /dev/null | openssl x509 -noout -dates | grep 'After' | awk -F '=' '{print $2}' | awk '{print $1,$2,$4}')
Cert_NED_TimeStamp=$(date +%s -d "$Cert_END_Time")
Create_TimeStamp=$(date +%s)
Rest_Time=$(expr $(expr $Cert_NED_TimeStamp - $Create_TimeStamp) / 86400)
echo "$WebName SSL certificate has $Rest_Time days left to expire." > ./ssl-monitor.txt
if [ $Rest_Time -lt 30 ];then
  WebHook='webhook incoming'
  curl "${WebHook}" -H 'Content-Type: application/json' -d '
  {
    "text": "'"$(cat ./ssl-monitor.txt)"'"
  }' &> /dev/null
fi
