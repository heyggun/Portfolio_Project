#!/bin/sh

DIR="/home/gguny"
get_time() {
        TIME=`date '+%Y/%m/%d %H:%M:%S'`
}

OPT=$1

case $1 in
	dev|DEV)
		MODE="DEV"
		BASE_DIR="$DIR/API_devel/ai_recomm_api"
		RESULT="$DIR/LOGS_devel/ai_recomm_api/ai_recomm_train_result.log"
		;;
	real|REAL)
		MODE="REAL"
		BASE_DIR="$DIR/API/ai_recomm_api"
		RESULT="$DIR/LOGS/ai_recomm_api/ai_recomm_train_result.log"
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

msg "[START   ] AI Recomm Train Started!"

conda_act

cd $BASE_DIR

~/anaconda3/envs/recom/bin/python train.py

EndTime=$(date +%s)

msg "[END     ] AI Recomm Train End!"
msg "[RUN-TIME] Total Spent time : $(($EndTime - $StartTime)) Second"
