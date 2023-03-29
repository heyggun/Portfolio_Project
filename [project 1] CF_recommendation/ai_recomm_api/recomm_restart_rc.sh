#!/bin/sh
# Buffalo Recommendation api auto restart process

DIR="/var/run/gguny"
DATE=`date +'%Y-%m-%d-%H:%M:%S'`
OPT=$1

case $1 in
	test|TEST)
		MODE="DEV TEST"
		PID_FILE="$DIR/ai_recomm_dev_test.pid"
		RESULT="/home/gguny/LOGS_devel/ai_recomm_api/ai_recomm_restart_test.log"
		;;
	dev|DEV)
		MODE="DEV"
		PID_FILE="$DIR/ai_recomm_dev.pid"
		RESULT="/home/gguny/LOGS_devel/ai_recomm_api/ai_recomm_restart.log"
		;;
	real|REAL)
		MODE="REAL"
		PID_FILE="$DIR/ai_recomm.pid"
		RESULT="/home/gguny/LOGS/ai_recomm_api/ai_recomm_restart.log"
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

#
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

# log
echo "[${DATE}] AI Recomm API  Process Restart Success ! " | tee -a $RESULT


