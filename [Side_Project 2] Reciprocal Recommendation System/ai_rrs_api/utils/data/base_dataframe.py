from ..config.common import conf
from ..data.backup_userdata import getUserData
from ..data.functions import *
from datetime import datetime
import pandas as pd
import time

mate_df = pd.read_pickle(f'{conf.dataPath}mate_df.pkl')
basic_df = pd.read_pickle(f'{conf.dataPath}basic_df.pkl')
view_df = pd.read_pickle(f'{conf.dataPath}view_df.pkl')
msg_df = pd.read_pickle(f'{conf.dataPath}msg_df.pkl')


class getBaseDataFrame(getUserData) :
    def __init__(self):
        super().__init__()

    def make_base_dataframe(self):
        df = mate_df.copy()
        df['age'] = int(str(datetime.today())[:4]) - df['mem_birth_year']
        # pf view / pf viewed
        df = self.get_member_list(df, view_df, 'view_list', 'viewed_list')
        # msg sent / msg receive
        df = self.get_member_list(df, msg_df, 'sent_list', 'receive_list')

        # other features(profile)
        df = char_transform(df)
        df = food_transform(df)
        df = hobby_transform(df)


        df['mate_religion'] = df['mate_religion'].apply(religion_code)
        df['mate_job'] = df['mate_job'].apply(job_code)
        df['mate_career'] = df['mate_career'].apply(career_code)
        df['mate_car'] = df['mate_car'].apply(lambda x: 0 if x == 9 else 1)
        df['mate_ann_salary'] = df['mate_ann_salary'].apply(salary_code)
        df['possess_property'] = df['possess_property'].apply(pos_code)
        df['drink_slct'] = df['drink_slct'].apply(drink_code)
        df['health_slct'] = df['health_slct'].apply(health_code)
        df['smoke_slct'] = df['smoke_slct'].apply(lambda x: 1 if len(str(x)) > 0 and str(x)[0] == 'c' else 0)

        h_bins = [0, 150, 160, 165, 170, 175, 180, 200]
        w_bins = [0, 40, 50, 60, 70, 80, 90, 100, 180]
        df['mate_height'] = pd.cut(df['mate_height'], bins=h_bins,
                                    labels=['under_150', '150', '160', '165', '170', '175', 'over_180'])
        df['mate_weight'] = pd.cut(df['mate_weight'], bins=w_bins,
                                    labels=['under_40', '40', '50', '60','70', '80', '90', 'over_100'])

        del df['mate_charc'], df['favor_food'], df['mate_hobby']
        df = pd.merge(df, basic_df[['mem_no', 'join_cnt', 'login_cnt', 'tot_stay_time']])

        return df

    def get_member_list(self, df, df2, list_name, list_name2):
        start = time.time()

        # view/sent member list x
        df[list_name] = None
        for i in range(len(df)) :
            temp = df2[df2['mem_no']==df.loc[i, 'mem_no']]['ptr_mem_no'].values.tolist()
            df.at[i, list_name] = temp

        # viewed/receive member list x
        df[list_name2] = None
        for i in range(len(df)) :
            temp = df2[df2['ptr_mem_no']==df.loc[i, 'mem_no']]['mem_no'].values.tolist()
            df.at[i, list_name2] = temp

        # list / list len count
        # df[list_name] = df[list_name].apply(lambda x : x)
        df[f'{list_name}_count'] = df[list_name].apply(lambda x : len(x))
        # df[list_name2] = df[list_name2].apply(lambda x : x)
        df[f'{list_name2}_count'] = df[list_name2].apply(lambda x : len(x))

        print(f'List Computing Time : {time.time() - start :.2f}s')
        return df


if __name__ == '__main__' :
    bdf = getBaseDataFrame()
    # make backup files by sql query
    bdf.save_sql()
    # make base dataframe
    df = bdf.make_base_dataframe()

    # pr base dataframe
    pr_base = df[['mem_no', 'mem_sex', 'age', 'mem_loc', 'mate_slct',
                  'mate_religion', 'mate_car', 'mate_ann_salary',
                  'mate_career', 'possess_property', 'mate_height', 'mate_weight',
                  'smoke_slct', 'drink_slct', 'health_slct',
                  'join_cnt', 'login_cnt', 'tot_stay_time', 'photo_cnt', 'upd_cnt', 'conts_upd_cnt',
                  'view_list', 'viewed_list', 'view_list_count','viewed_list_count',
                  'sent_list', 'receive_list', 'sent_list_count','receive_list_count',
                  'char_type_1', 'char_type_2', 'char_type_3', 'char_type_4',
                  'hobby_type_1', 'hobby_type_2', 'hobby_type_3', 'hobby_type_4']]
    pr_base.to_pickle(f"{conf.dataPath}pr_base_df.pkl")

    # cf base dataframe
    cf_base = df[['mem_no', 'mem_sex', 'age',
                  'view_list', 'viewed_list', 'view_list_count','viewed_list_count',
                  'sent_list', 'receive_list', 'sent_list_count', 'receive_list_count']]
    cf_base.to_pickle(f"{conf.dataPath}cf_base_df.pkl")

    # explanation base dataframe
    corr_base = df[['mem_no', 'mem_sex', 'mate_religion', 'mem_loc', 'mate_car', 'mate_slct', 'mate_job',
                    'mate_ann_salary', 'mate_career', 'mate_style', 'possess_property',
                    'smoke_slct', 'drink_slct','health_slct',  'mate_height',
                    'char_type_1', 'char_type_2', 'char_type_3', 'char_type_4', 'food_type_1',
                  'food_type_2', 'food_type_3', 'food_type_4', 'food_type_5', 'food_type_6', 'food_type_7',
                  'food_type_8', 'food_type_9', 'hobby_type_1', 'hobby_type_2', 'hobby_type_3', 'hobby_type_4',
                  'view_list', 'sent_list']]
    corr_base.to_pickle(f"{conf.dataPath}corr_df.pkl")