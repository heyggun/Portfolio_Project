from ..config.logger import LogConfig
from ..config.common import conf
from collections import Counter
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import auc, f1_score, roc_curve
from catboost import CatBoostClassifier

import pandas as pd
import joblib


smote = SMOTE()
model = CatBoostClassifier(random_state=0, silent=True)


df = pd.read_pickle(f'{conf.dataPath}pr_base_df.pkl')
msg_df = pd.read_pickle(f'{conf.dataPath}msg_df.pkl')
ptr_df = df.copy()
ptr_df.columns = ['ptr_' + col for col in ptr_df.columns]


class TrainPRModel() :
    def __init__(self):
        pass

    def save_model(self):
        X, y = self.generate_train_dataset()
        X_train, X_test, y_train, y_test = self.data_splitter(X, y)
        model = self.training_model(X_train, X_test, y_train, y_test)
        print('Train Succeed ! ')
        return model

    def training_model(self, X_train, X_test, y_train, y_test):
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        pred_proba = model.predict_proba(X_test)
        fpr, tpr, threshold = roc_curve(y_test, pred_proba[:, 1])
        # log.Log(f"[PR score model AUD Score  : {auc(fpr, tpr):.3f} - f1 score : {f1_score(y_test, pred):.3f}")
        joblib.dump(model, f"{conf.dataPath}pr_score_model.pkl")
        return model

    def data_splitter(self, X, y ):
        X_res, y_res = smote.fit_resample(X, y)
        X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.2)
        # print(f"Oversampled Dataset Result : {Counter(y_res)}")
        return X_train, X_test, y_train, y_test

    def generate_train_dataset(self):
        # Detect positive response message
        bi_temp = pd.DataFrame()
        cnt = 0
        msg_temp = msg_df.copy()[['mem_no', 'ptr_mem_no']]
        msg_temp2 = msg_temp.rename(columns={"mem_no" : "ptr_mem_no", "ptr_mem_no" : "mem_no"})
        for i in range(len(msg_temp)) :
            both_msg = msg_temp[(msg_temp['mem_no']==msg_temp2.loc[i, 'mem_no']) & (msg_temp['ptr_mem_no']==msg_temp2.loc[i, 'ptr_mem_no'])]
            if len(both_msg) >= 1 :
                cnt += 1
                bi_temp = pd.concat([bi_temp, both_msg])

        bi_temp['positive_response'] = 1
        msg_temp = msg_temp.drop(bi_temp.index)
        msg_temp['positive_response'] = 0

        response_df = pd.concat([bi_temp, msg_temp])

        total_pr_df = pd.merge(response_df, df)
        total_data = pd.merge(total_pr_df, ptr_df)

        male_data = total_data[total_data['mem_sex']=='m'].reset_index(drop=True)
        female_data = total_data[total_data['mem_sex']=='f'].reset_index(drop=True)

        female_data.columns = [f_col.replace('ptr_', '') if 'ptr_' in f_col or f_col =='positive_response' else 'ptr_' + f_col
                               for f_col in female_data.columns]

        data = pd.concat([male_data, female_data])
        data = data.drop(['mem_no', 'ptr_mem_no', 'mem_sex', 'ptr_mem_sex', 'view_list', 'viewed_list',
                          'sent_list', 'receive_list', 'ptr_view_list', 'ptr_viewed_list',
                          'ptr_sent_list', 'ptr_receive_list'], axis=1)
        data['age_gap'] = data['age'] - data['ptr_age']
        data['loc_like'] = data.apply(lambda x: 1 if x['mem_loc'] == x['ptr_mem_loc'] else 0, axis=1)
        data['marriage_like'] = data.apply(lambda x: 1 if x['mate_slct'] == x['ptr_mate_slct'] else 0, axis=1)
        data.drop(['mem_loc', 'mate_slct', 'ptr_mem_loc', 'ptr_mate_slct', 'ptr_smoke_slct'], axis=1, inplace=True)


        X = pd.get_dummies(data.drop('positive_response', axis=1))
        y = data['positive_response']

        del msg_temp, msg_temp2, bi_temp, response_df, total_pr_df, total_data, male_data, female_data, data

        return X, y

if __name__ == '__main__' :

    # Train Model and save pickle file
    tpr = TrainPRModel()
    model = tpr.save_model()
    print(model.feature_names_)
    #
    # ['age', 'mate_car', 'smoke_slct', 'join_cnt', 'login_cnt', 'tot_stay_time', 'photo_cnt', 'upd_cnt', 'conts_upd_cnt',
    #  'view_list_count', 'viewed_list_count', 'sent_list_count', 'receive_list_count', 'char_type_1', 'char_type_2',
    #  'char_type_3', 'char_type_4', 'hobby_type_1', 'hobby_type_2', 'hobby_type_3', 'hobby_type_4', 'ptr_age',
    #  'ptr_mate_car', 'ptr_join_cnt', 'ptr_login_cnt', 'ptr_tot_stay_time', 'ptr_photo_cnt', 'ptr_upd_cnt',
    #  'ptr_conts_upd_cnt', 'ptr_view_list_count', 'ptr_viewed_list_count', 'ptr_sent_list_count',
    #  'ptr_receive_list_count', 'ptr_char_type_1', 'ptr_char_type_2', 'ptr_char_type_3', 'ptr_char_type_4',
    #  'ptr_hobby_type_1', 'ptr_hobby_type_2', 'ptr_hobby_type_3', 'ptr_hobby_type_4', 'age_gap', 'loc_like',
    #  'marriage_like', 'mate_religion_0', 'mate_religion_1', 'mate_religion_2', 'mate_religion_3', 'mate_ann_salary_1',
    #  'mate_ann_salary_2', 'mate_ann_salary_3', 'mate_ann_salary_4', 'mate_ann_salary_5', 'mate_ann_salary_6',
    #  'mate_ann_salary_7', 'mate_career_1', 'mate_career_2', 'mate_career_3', 'mate_career_4', 'possess_property_1',
    #  'possess_property_2', 'possess_property_3', 'possess_property_4', 'possess_property_5', 'possess_property_6',
    #  'possess_property_7', 'mate_height_under_150', 'mate_height_150', 'mate_height_160', 'mate_height_165',
    #  'mate_height_170', 'mate_height_175', 'mate_height_over_180', 'mate_weight_under_40', 'mate_weight_40',
    #  'mate_weight_50', 'mate_weight_60', 'mate_weight_70', 'mate_weight_80', 'mate_weight_90', 'mate_weight_over_100',
    #  'drink_slct_0', 'drink_slct_1', 'drink_slct_2', 'drink_slct_3', 'health_slct_0', 'health_slct_1', 'health_slct_2',
    #  'health_slct_3', 'ptr_mate_religion_0', 'ptr_mate_religion_1', 'ptr_mate_religion_2', 'ptr_mate_religion_3',
    #  'ptr_mate_ann_salary_1', 'ptr_mate_ann_salary_2', 'ptr_mate_ann_salary_3', 'ptr_mate_ann_salary_4',
    #  'ptr_mate_ann_salary_5', 'ptr_mate_ann_salary_6', 'ptr_mate_ann_salary_7', 'ptr_mate_career_1',
    #  'ptr_mate_career_2', 'ptr_mate_career_3', 'ptr_mate_career_4', 'ptr_possess_property_1', 'ptr_possess_property_2',
    #  'ptr_possess_property_3', 'ptr_possess_property_4', 'ptr_possess_property_5', 'ptr_possess_property_6',
    #  'ptr_possess_property_7', 'ptr_mate_height_under_150', 'ptr_mate_height_150', 'ptr_mate_height_160',
    #  'ptr_mate_height_165', 'ptr_mate_height_170', 'ptr_mate_height_175', 'ptr_mate_height_over_180',
    #  'ptr_mate_weight_under_40', 'ptr_mate_weight_40', 'ptr_mate_weight_50', 'ptr_mate_weight_60', 'ptr_mate_weight_70',
    #  'ptr_mate_weight_80', 'ptr_mate_weight_90', 'ptr_mate_weight_over_100', 'ptr_drink_slct_0', 'ptr_drink_slct_1',
    #  'ptr_drink_slct_2', 'ptr_drink_slct_3', 'ptr_health_slct_0', 'ptr_health_slct_1', 'ptr_health_slct_2',
    #  'ptr_health_slct_3']


