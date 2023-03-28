#!/bin/sh
# member data backup creation for chemistry list


MONTH=`date +'%Y%m'`
OPT=$1

case $1 in
	dev|DEV)
		MODE="DEV"
		BASE_DIR="/home/gguny/API_devel/ai_chemistryList_api"
		RESULT="/home/gguny/LOGS_devel/ai_chemistryList_api/backdata_gen_${MONTH}.log"
		ARGS="dev"
		;;
	real|REAL)
		MODE="REAL"
		BASE_DIR="/home/gguny/API/ai_chemistryList_api"
		RESULT="/home/gguny/LOGS/ai_chemistryList_api/backdata_gen_${MONTH}.log"
		ARGS="real"
		;;
	*)
		echo "$0 <dev|real>"
		exit
		;;
esac


# conda init
source /home/gguny/anaconda3/etc/profile.d/conda.sh
source /home/gguny/anaconda3/bin/activate chem_list
cd $BASE_DIR

python backdata_gen.py --server ${ARGS} | tee -a /home/gguny/LOGS_devel/ai_chemistryList_api/backdata_gen_${MONTH}.log
