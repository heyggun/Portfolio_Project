import pymysql
from datetime import datetime, timedelta
import os
import pandas as pd
from utils.config.common import conf
from utils.config.logger import LogConfig
dataPath = conf.dataPath
port = conf.port

class DBConnector :
    def __init__(self):
        self.conn = pymysql.connect(
                user='gguny',  # 유저 이름
                passwd='gguny',  # 패스워드
                host='000.000.000.000',  # 호스트
                db='database',  # 데이터베이스
                charset='utf8',  # 인코딩
                port=1234  # 포트 번호(''없이 사용)
            )

        self.dev_conn = pymysql.connect(
                user='gguny',  # 유저 이름
                passwd='gguny',  # 패스워드
                host='000.000.000.000',  # 호스트
                db='database',  # 데이터베이스
                charset='utf8',  # 인코딩
                port=1234  # 포트 번호(''없이 사용)
            )

        self.today = datetime.today()
        self.path = dataPath

    # db connection
    def connector(self, tablename, dcname):
        if str(port).startswith('00') :
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            sql = f"SELECT * FROM database.{tablename} WHERE {dcname} BETWEEN '{str(self.today - timedelta(days=+7))[:10]+ ' 00:00:00'}' and '{str(self.today - timedelta(days=+1))[:10]+ ' 23:59:59'}';"
            cursor.execute(sql)
        else :
            cursor = self.dev_conn.cursor(pymysql.cursors.DictCursor)
            sql = f"SELECT * FROM database.{tablename} order by {dcname} desc limit 2000000;"
            cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(result)
        # train_log(f'[DBCONNECTION SUCCEED] TABLE NAME : {tablename} and TABLE SIZE : {len(df)}')
        return df

    def save_data(self):
        if not os.path.exists(self.path) :
            os.mkdir(self.path)
        self.call_visit_log()
        self.call_concn_log()
        self.call_member_mate()

    def call_visit_log(self,dcname='open_date'):
        df = self.connector('view_all_log',dcname)
        df = df.astype(str)
        df = df.rename(columns={'ptr_mem_no': 'ptr_mem_no'})
        df.to_pickle(f'{dataPath}/visit_log.pkl')

    def call_concn_log(self,dcname='ins_date'):
        df = self.connector('concn_hist',dcname)
        df = df.astype(str)
        df.to_pickle(f'{dataPath}/concn_log.pkl')

    def call_member_mate(self):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT user_no, user_sex FROM database.usertable"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(result)
        df = df.astype(str)
        df.to_pickle(f'{dataPath}/member_mate.pkl')
        # train_log(f'[DBCONNECTION SUCCEED] TABLE NAME : member_mate')
