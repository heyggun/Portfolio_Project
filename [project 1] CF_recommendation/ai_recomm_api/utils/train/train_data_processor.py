import pandas as pd
from utils.train.dbconnector import DBConnector
from utils.config.common import conf
dataPath = conf.dataPath

class trainDataProcessor(DBConnector) :
    def __init__(self):
        super().__init__()

    def total_score_gen(self):
        self.save_data()
        visit_score = self.visit_log_preprocessor()
        concn_score = self.concn_log_preprocessor()
        tot_score = pd.concat([visit_score, concn_score])
        tot_score = tot_score.groupby(['mem_no','ptr_mem_no']).sum().reset_index()[['mem_no','ptr_mem_no','score']]
        mem_sex = pd.read_pickle(f'{self.path}/member_mate.pkl')
        ptr_mem_sex = mem_sex.rename(columns={'mem_no':'ptr_mem_no', 'mem_sex' : 'ptr_mem_sex'})

        tot_score_df = pd.merge(mem_sex, tot_score)
        tot_score = pd.merge(ptr_mem_sex, tot_score_df)
        female_score = tot_score[tot_score['mem_sex']=='f']
        female_score = female_score[female_score['mem_sex'] != female_score['ptr_mem_sex']]
        female_score.drop(['mem_sex','ptr_mem_sex'], axis=1, inplace=True)
        male_score = tot_score[tot_score['mem_sex']=='m']
        male_score = male_score[male_score['mem_sex'] != male_score['ptr_mem_sex']]
        male_score.drop(['mem_sex','ptr_mem_sex'], axis=1, inplace=True)
        pd.to_pickle(female_score, f'{dataPath}/female_score.pkl')
        pd.to_pickle(male_score, f'{dataPath}/male_score.pkl')

    # 1. 프로필 기본열람 & 2. 프로필 전체열람
    def visit_log_preprocessor(self):
        df = pd.read_pickle(f'{dataPath}/visit_log.pkl')
        visit_cnt = df.groupby(['mem_no', 'ptr_mem_no', 'open_slct']).count().reset_index()
        visit_score = visit_cnt.rename(columns={'auto_no': 'score'})
        visit_score['score'] = visit_score['score'].apply(lambda x : 5 if x > 5 else x)
        visit_score['score'] = visit_score.apply(lambda x : 2*x['score'] if x['open_slct']!='v' else x['score'] ,axis=1)
        visit_score = visit_score.groupby(['mem_no','ptr_mem_no']).sum().reset_index()
        return visit_score

    # 2. 관심있어요
    def concn_log_preprocessor(self):
        df = pd.read_pickle(f'{dataPath}/concn_log.pkl')
        concn_cnt = df.groupby(['mem_no', 'ptr_mem_no']).count()[['auto_no']].reset_index()
        concn_score = concn_cnt.rename(columns={'auto_no': 'score'})
        concn_score['score'] = concn_score['score'].apply(lambda x: 5 if x > 5 else x)
        return concn_score
