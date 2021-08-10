#!/bin/bash
# test program to inuce 100% cpu load and trigger a kill from the cpu monitor

trap "echo 'got term'" TERM 
while true ; do
true
done
