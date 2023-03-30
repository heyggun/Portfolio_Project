#!/bin/sh

DIR="/home/gguny"
get_time() {
        TIME=`date '+%Y/%m/%d %H:%M:%S'`
}

OPT=$1

case $1 in
	dev|DEV)
		MODE="DEV"
		BASE_DIR="$DIR/API_devel/ai_rrs_api/utils/"
		RESULT="$DIR/LOGS_devel/ai_rrs_api/ai_rrs_pr_train_result.log"
		;;
	real|REAL)
		MODE="REAL"
		BASE_DIR="$DIR/API/ai_rrs_api/utils/"
		RESULT="$DIR/LOGS/ai_rrs_api/ai_rrs_pr_train_result.log"
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

conda_act() {
	source /home/gguny/anaconda3/etc/profile.d/conda.sh
	source /home/gguny/anaconda3/bin/activate recom
}

msg "[START   ] AI RRS PR model Train Started!"

conda_act

cd $BASE_DIR

~/anaconda3/envs/recom/bin/python train_pr_model.py

EndTime=$(date +%s)

msg "[END     ] AI RRS PR model Train End!"
msg "[RUN-TIME] Total Spent time : $(($EndTime - $StartTime)) Second"
