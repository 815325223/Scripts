#!/bin/bash

#
# config file defines variables, mail template and kill_log_mail()
# assumes config file in same directory as process_monitor.sh
#
COMMAND_PATH=$(cd `dirname $0` && pwd)
. ${COMMAND_PATH}/process_monitor.config

#
# make BASE_DIR if doesn't exist
#
if [ ! -d "${BASE_DIR}" ]; then
    mkdir ${BASE_DIR}
    [ "$?" != "0" ] && echo "Exiting: Could not create ${BASE_DIR}" && exit 1
else
    touch ${HISTFILE} || { echo "Exiting: Could not touch ${HISTFILE} history file"; exit 1;}
    touch ${TEMPFILE} || { echo "Exiting: Could not touch ${TEMPFILE} temporary file"; exit 1;}

fi

#
# test log file
#
touch ${LOGFILE} || { echo "Exiting: Could not touch ${LOGFILE} log file"; exit 1;}

#
# ps output once per run into TEMPFILE
#
ps -e -o pid,uid,%cpu,%mem,comm | sed -e 's/^ *//g' | sed -e 's/ \+/:/g' > $TEMPFILE
touch $HISTFILE

#
# check every user within UID range
#
for USER in $(getent passwd | cut -d ":" -f 3 );do

    if [ "$USER" -ge "$USER_UID_MIN" ] && [ "$USER" -le "$USER_UID_MAX" ]; then

	# all processes for this user
	PIDS=$(grep :$USER: $TEMPFILE  | cut -f 1 -d ":")

	for PID in $(echo $PIDS);do
	    HISTORY=""
	    CPU=$( grep  "^${PID}:" $TEMPFILE | cut -f 3 -d ":" ) 
	    MEMORY=$( grep "^${PID}:" $TEMPFILE | cut -f 4 -d ":" ) 
		
	    #echo "User $USER using $CPU %cpu and $MEMORY %memory $HISTORY $PID."

	    # if above cpu or memory limit
	    if [ "${CPU%\.*}" -ge "$MAX_CPU" ] || [ "${MEMORY%\.*}" -ge "$MAX_MEMORY" ]; then

		#number of times PID listed in history file
		HISTORY=$(grep ${PID} $HISTFILE | wc | awk '{print $1}')

		if [ "$HISTORY" -eq 0 ];then
                    #first time detected add to history
		    echo ${PID} >> $HISTFILE
		elif [ "$HISTORY" -eq 1 ];then
		    #second time detected add and alert
		    echo ${PID} >> $HISTFILE
		    kill_log_mail
		fi
	    fi
	 done
    fi
done

#
# if no longer running, remove from history
#
for D in $(cat $HISTFILE);do
    if [ ! -d /proc/$D ];then
	grep -v $D $HISTFILE > $TEMPFILE
	mv $TEMPFILE $HISTFILE
    fi
done
