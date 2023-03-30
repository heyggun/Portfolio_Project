from utils.config.common import conf
import pandas as pd
import numpy as np

df = pd.read_pickle(f"{conf.dataPath}corr_df.pkl")


class Reciprocal_Explanation() :
    def __init__(self):
        pass

    def get_reciprocal_explanations_for_y_list(self, x, y):
        reciprocal_exp_list = list()
        reciprocal_exp = self.get_reciprocal_explanations(x, y)
        reciprocal_exp_list.append(reciprocal_exp)
        return reciprocal_exp_list

    def get_reciprocal_explanations(self, x, y):

        exp_x_r = self.get_explanation(x, y)
        exp_y_r = self.get_explanation(y, x)

        reciprocal_exp = {"exp_mem_to_ptr" : exp_x_r, "exp_ptr_to_mem" : exp_y_r}
        # {x}에게 {y}가 추천된 이유 : {exp_x_r}, {y}에게 {x}가 추천된 이유 : {exp_y_r}

        return reciprocal_exp

    def get_explanation(self, x, y, k=3):
        view_list = df[df['mem_no']==x]['view_list'].values[0]
        send_list = df[df['mem_no']==x]['sent_list'].values[0]

        try :
            # m_x
            m_x = [1 if i in send_list else 0 for i in view_list]
            a_v_df= pd.DataFrame([m_x], columns=view_list, index=[x]).T

            # S_x_a_v
            for col in df.columns :
                S_x_a_v = [df[df['mem_no']==y][col].values[0] for y in a_v_df.index]
                a_v_df[col] = S_x_a_v

            y_df = df[df['mem_no'] == y]

            del a_v_df['mem_sex'], a_v_df['view_list'], a_v_df['sent_list']
            del y_df['view_list'], y_df['sent_list'], y_df['smoke_slct']

            y_a_v = pd.get_dummies(y_df)

            for y_col in y_a_v.columns :
                if y_col in a_v_df.columns and y_a_v[y_col].values[0] != 1 :
                    a_v_df.drop(y_col, inplace=True, axis=1)

            a_v_df.drop([c for c in a_v_df.columns if c not in y_a_v.columns and c!=x], axis=1, inplace=True)

            corr_data = a_v_df.corr()[x].sort_values(ascending=False)
            corr_data = corr_data.fillna(0)
            corr_data = corr_data[corr_data>=0]
            print(f"Highest correlation features for {x} : {[corr_data.index[1]]}, Correlation value : {corr_data.values[1]}")


            if corr_data.values[1] == 0.0:
                result = 'No corr'
            else:
                result = corr_data.index[1:k + 1].tolist()

        except:
            result = 'No corr'

        return result

