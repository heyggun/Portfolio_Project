#!/bin/sh
# rrs auto making backdata & rrs base dataframe process

DIR="/home/gguny"
get_time() {
        TIME=`date '+%Y/%m/%d %H:%M:%S'`
}

OPT=$1

case $1 in
	dev|DEV)
		MODE="DEV"
		BASE_DIR="$DIR/API_devel/ai_rrs_api/utils/data/"
		RESULT="$DIR/LOGS_devel/ai_rrs_api/ai_rrs_backdata_result.log"
		;;
	real|REAL)
		MODE="REAL"
		BASE_DIR="$DIR/API/ai_rrs_api/utils/data/"
		RESULT="$DIR/LOGS/ai_rrs_api/ai_rrs_backdata_result.log"
		;;
	*)
		echo "$0 <dev|real>"
		exit
		;;
esac

StartTime=$(date +%s)


msg() {
	get_time
	echo "[$TIME] $*" | tee -a $RESULT
}

# debug
echo "- RERUN $MODE API"
echo "- PID FILE : $PID_FILE"
echo "- LOG FILE : $RESULT"


conda_act() {
	source /home/gguny/anaconda3/etc/profile.d/conda.sh
	source /home/gguny/anaconda3/bin/activate recom
}
msg "[START   ] AI rrs backup_data Started!"

conda_act

cd $BASE_DIR

~/anaconda3/envs/recom/bin/python backup_userdata.py
~/anaconda3/envs/recom/bin/python base_dataframe.py

EndTime=$(date +%s)

msg "[END     ] AI rrs backup_data, base_dataframe Making End!"
msg "[RUN-TIME] Total Spent time : $(($EndTime - $StartTime)) Second"
