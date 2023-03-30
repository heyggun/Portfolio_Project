import joblib
import pandas as pd
from utils.config.common import conf

df = pd.read_pickle(f"{conf.dataPath}pr_base_df.pkl")
pr_model = joblib.load(f"{conf.dataPath}pr_score_model.pkl")


class PR_score():
    def __init__(self):
        pass

    def predict_positive_reply(self, x, top_k=30):

        try:
            x_info_df = df[df['mem_no']==x].reset_index(drop=True)
            x_age = x_info_df.loc[0, 'age']
            x_gender = x_info_df.loc[0, 'mem_sex']
            x_view = x_info_df.loc[0, 'view_list']
            x_sent = x_info_df.loc[0, 'sent_list']

            # 나이 정책 및 상대 성별에 맞는 상대 회원 범위(y_range)
            y_range = df[(abs(x_age - df['age']) <= 5) & (df['mem_sex']!=x_gender)].mem_no.values
            y_range = [y for y in y_range if y not in x_view and y not in x_sent]
            y_info_df = df[df['mem_no'].isin(y_range)].reset_index(drop=True)

            if x_gender == 'm' :
                y_info_df.columns = ['ptr_' + col for col in y_info_df.columns]
                y_info_df['mem_no'] = x
            else :
                x_info_df.columns = ['ptr_' + col for col in x_info_df.columns]
                y_info_df['ptr_mem_no'] = x

            x_y_info_df = pd.merge(x_info_df, y_info_df)
            x_y_info_df.drop(['mem_no', 'ptr_mem_no', 'mem_sex', 'ptr_mem_sex'], axis=1, inplace=True)
            x_y_info_df['age_gap'] = x_y_info_df['age'] - x_y_info_df['ptr_age']
            x_y_info_df['loc_like'] = x_y_info_df.apply(lambda x : 1 if x['mem_loc'] == x['ptr_mem_loc'] else 0, axis =1)
            x_y_info_df['marriage_like'] = x_y_info_df.apply(lambda x : 1 if x['mem_loc'] == x['ptr_mem_loc'] else 0, axis =1)
            x_y_info_df.drop(['mem_loc', 'mate_slct', 'ptr_mem_loc', 'ptr_mate_slct', 'view_list', 'viewed_list',
                           'sent_list', 'receive_list', 'ptr_view_list', 'ptr_viewed_list', 'ptr_sent_list',
                           'ptr_receive_list','ptr_smoke_slct'], axis=1, inplace=True)

            x_y_info_df = pd.get_dummies(x_y_info_df)
            for col in pr_model.feature_names_ :
                if col not in x_y_info_df.columns :
                    x_y_info_df[col] = 0

            pred = pr_model.predict_proba(x_y_info_df)
            pred_result = pd.DataFrame(pred[:, 1], columns=['score'], index=y_range)
            pred_result = pred_result.sort_values('score', ascending=False).head(top_k)

        except :
            pred_result = None

        del x_info_df, y_info_df, x_y_info_df, pred

        return pred_result