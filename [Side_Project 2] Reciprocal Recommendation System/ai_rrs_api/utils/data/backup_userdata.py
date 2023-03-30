from ..config.common import conf
from datetime import datetime, timedelta
import pandas as pd
import pymysql
import os


class getUserData() :
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

        # 대용량 select 시 192.168.1.141 사용
        self.today = str(datetime.today())[:10]
        self.yesterday = str(datetime.today() - timedelta(1))[:10]
        self.past = str(datetime.today() - timedelta(7))[:10]

    def save_sql(self):
        if not os.path.exists(conf.dataPath) :
            os.mkdir(conf.dataPath)
        mate_df = self.read_sql('member_m')
        basic_df = self.read_sql('member_b')
        view_df = self.read_sql('pf_view_all_log', 'ins_date')
        msg_df = self.read_sql('msg_log_back', 'ins_date')

        view_df = self.check_duplications(view_df, mate_df)
        msg_df = self.check_duplications(msg_df, mate_df)

        mate_df.to_pickle(f'{conf.dataPath}mate_df.pkl')
        basic_df.to_pickle(f'{conf.dataPath}basic_df.pkl')
        view_df.to_pickle(f'{conf.dataPath}view_df.pkl')
        msg_df.to_pickle(f'{conf.dataPath}msg_df.pkl')

    def read_sql(self, table_name, *column_name) :
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        if column_name :
            sql = f"SELECT DISTINCT mem_no, ptr_mem_no FROM database.{table_name} WHERE {column_name[0]} BETWEEN '{self.past}' AND '{self.today}'"
        else :
            sql = f"SELECT * FROM database.{table_name}"
        # print('Processed SQL Query :', sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        df = pd.DataFrame(result)
        # print(f'DataFrame ({table_name}) Length : {len(df):,}')
        return df

    def check_duplications(self, df,mate_df):
        df = df[(df['mem_no'].isin(mate_df['mem_no'].values)) & (df['ptr_mem_no'].isin(mate_df['mem_no'].values))]
        df = df.reset_index(drop=True)
        # print(f'Deduplicated DataFrame Length : {len(df):,}')
        return df

if __name__ == '__main__':
    getUser = getUserData()
    getUser.save_sql()
