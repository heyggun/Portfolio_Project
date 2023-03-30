#!/bin/sh

DIR="/var/run/gguny"
DATE=`date +'%Y-%m-%d-%H:%M:%S'`

OPT=$1

case $1 in
	test|TEST)
		MODE="DEV TEST"
		PID_FILE="$DIR/ai_chatbot_dev_test.pid"
		RESULT="/home/gguny/LOGS_devel/ai_chatbot_api/ai_chatbot_restart_test.log"
		;;
	dev|DEV)
		MODE="DEV"
		PID_FILE="$DIR/ai_chatbot_dev.pid"
		RESULT="/home/gguny/LOGS_devel/ai_chatbot_api/ai_chatbot_restart.log"
		;;
	real|REAL)
		MODE="REAL"
		PID_FILE="$DIR/ai_chatbot.pid"
		RESULT="/home/gguny/LOGS/ai_chatbot_api/ai_chatbot_restart.log"
		;;
	*)
		echo "$0 <test|dev|real>"
		exit
		;;
esac

# debug
echo "- RERUN $MODE API"
echo "- PID FILE : $PID_FILE"
echo "- LOG FILE : $RESULT"

if [ ! -f $PID_FILE ]; then
	echo "$PID_FILE file does not exist."
	exit
fi
PID=`cat $PID_FILE`

if [ "$PID" = "" ]; then
	echo "[${DATE}] Process Not Found ! " | tee -a $RESULT	
	exit
fi

# send signal
kill -HUP $PID


#write log
echo "[${DATE} AI chatbot Process Restart Success ! " | tee -a $RESULT
