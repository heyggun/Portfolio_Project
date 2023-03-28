import pymysql
import os
import pandas as pd
from datetime import datetime
from utils.config.common import conf
import argparse

dataPath = conf.dataPath

parser = argparse.ArgumentParser()
parser.add_argument('--server', required=True, help='<real/dev>')

args = parser.parse_args()

if args.server == 'real' :
    try:
        conn = pymysql.connect(
            user='gguny',  # 유저 이름
            passwd='gguny',  # 패스워드
            host='000.000.000.000',  # 호스트
            db='ggunny',  # 데이터베이스
            charset='utf8',  # 인코딩
            port=1234  # 포트 번호(''없이 사용)
        )

        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "CALL p_ai_mytype_mem_data_list()"
        cursor.execute(sql)
        mem_list = cursor.fetchall()
        cursor.close()
        # update backupfiles
        mem_list = pd.DataFrame(mem_list)['mem_no']

        conn = pymysql.connect(
            # mysql ai db server connection
            user='gguny',  # 유저 이름
            passwd='gguny',  # 패스워드
            host='000.000.000.000',  # 호스트
            db='ggunny',  # 데이터베이스
            charset='utf8',  # 인코딩
            port=1234  # 포트 번호(''없이 사용)
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select * from database_name"
        cursor.execute(sql)
        member_mate = cursor.fetchall()
        cursor.close()
        member_mate = pd.DataFrame(member_mate)
        member_mate = member_mate[member_mate['mem_no'].isin(mem_list)].reset_index(drop=True)
        member_mate.to_csv(f'{dataPath}/member_mate.csv', escapechar='|')
        os.system(f'/bin/rsync -a {dataPath}/member_mate.csv 000.000.0.00::ai_data/chemistry_renew_data')
        print(f'[{str(datetime.today())[:16]}]BackData Update Success')

    except Exception as e:
        print(e)

elif args.server == 'dev' : # 개발서버
    try :
        conn = pymysql.connect(
            user='ggunny',  # 유저 이름
            passwd='ggunny',  # 패스워드
            host='000.000.000.000',  # 호스트
            db='ggunny',  # 데이터베이스
            charset='utf8',  # 인코딩
            port=1234  # 포트 번호(''없이 사용)
        )
        # start = time.time()  # 시작 시간 저장
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select * from database_name"
        cursor.execute(sql)
        member_mate = cursor.fetchall()
        cursor.close()
        # update backupfiles
        member_mate = pd.DataFrame(member_mate)
        member_mate.to_csv(f'{dataPath}/member_mate_dev.csv', index=False)
        os.system(f'/bin/rsync -a {dataPath}/member_mate_dev.csv 000.000.0.00::ai_data/chemistry_renew_data')
        print(f'[{str(datetime.today())[:16]}]BackData Update Success')

    except Exception as e:
        print(e)