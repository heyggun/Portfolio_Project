from utils.model.model1_feature import Model1
from utils.model.model2_feature import Model2
from utils.model.model3_feature import Model3
from utils.config.common import model_1, model_2, model_3
from utils.functions import *
import warnings
warnings.filterwarnings('ignore')

class predictScore(Model1, Model2, Model3) :
    def __init__(self):
        super(predictScore, self).__init__()

    def set_model_type(self, df, model_type, is_callable):
        if not is_callable :
            if model_type == 'gscore':
                df = self.total_predict(df, 'gscore')
            elif model_type == 'cscore':
                df = self.total_predict(df, 'cscore')
            elif model_type == 'mscore':
                df = self.total_predict(df, 'mscore')
        else :
            if model_type == 'gscore':
                df = self.model_1_predict(df)
            elif model_type == 'cscore':
                df = self.model_2_predict(df)
            elif model_type == 'mscore':
                df = self.model_3_predict(df)
        return df

    def get_df(self, my_info, mem_no, mem_sex):
        df = df_merge(my_info, mem_no, mem_sex)
        return df

    def model_1_predict(self, df):
        model_1_df = df[['mem_birth_year', 'mate_charc', 'smoke_slct', 'drink_slct', 'health_slct', 'wed_plan',
                         'ptr_mem_birth_year', 'ptr_mate_charc', 'ptr_drink_slct', 'ptr_health_slct', 'ptr_wed_plan']]
        model_1_df = self.model_1_transform(model_1_df)
        df['gscore'] = list(map(lambda x : round(x, 1) if x < 100 else 100, self.model_predict(model_1_df, model_1)))
        return df[['mem_no','ptr_mem_no','gscore']]

    def model_2_predict(self, df):
        model_2_df = df[['mem_birth_year', 'ptr_mem_birth_year', 'mem_loc', 'mate_slct', 'divorce_year',
                         'parents_slct', 'mate_religion', 'mate_hobby', 'favor_food', 'ptr_mem_loc', 'ptr_mate_slct',
                         'ptr_divorce_year', 'ptr_parents_slct', 'ptr_mate_religion', 'ptr_mate_hobby',
                         'ptr_favor_food']]
        model_2_df = self.model_2_transform(model_2_df)
        df['cscore'] = list(map(lambda x : round(x, 1) if x < 100 else 100, self.model_predict(model_2_df, model_2)))
        return df[['mem_no', 'ptr_mem_no', 'cscore']]

    def model_3_predict(self, df):
        model_3_df = df[['mem_birth_year', 'ptr_mem_birth_year','mate_job','ptr_mate_job',
                         'mate_career', 'ptr_mate_career','mate_weight', 'ptr_mate_weight', 'mate_height',
                         'ptr_mate_height', 'mate_car', 'ptr_mate_car','mate_ann_salary', 'ptr_mate_ann_salary',
                         'possess_property', 'ptr_possess_property']]
        model_3_df = self.model_3_transform(model_3_df)
        df['mscore'] = list(map(lambda x : round(x, 1) if x < 100 else 100, self.model_predict(model_3_df, model_3)))
        return df[['mem_no', 'ptr_mem_no', 'mscore']]

    def total_predict(self, df, model_type):
        model_1_df, model_2_df, model_3_df = self.data_splitter(df)

        model_1_df = self.model_1_transform(model_1_df)
        df['gscore'] = list(map(lambda x : round(x, 1) if x < 100 else 100, self.model_predict(model_1_df, model_1)))
        model_2_df = self.model_2_transform(model_2_df)
        df['cscore'] = list(map(lambda x : round(x, 1) if x < 100 else 100, self.model_predict(model_2_df, model_2)))
        model_3_df = self.model_3_transform(model_3_df)
        df['mscore'] = list(map(lambda x: round(x, 1) if x < 100 else 100, self.model_predict(model_3_df, model_3)))

        df['total_score'] = round(((df['gscore'] * 0.2) + (df['cscore'] * 0.3) + (df['mscore'] * 0.5)), 1)

        return df[['mem_no', 'ptr_mem_no', 'total_score', model_type]]

    def data_splitter(self, df):
        model_1_df = df[['mem_birth_year', 'mate_charc', 'smoke_slct', 'drink_slct', 'health_slct', 'wed_plan','ptr_mem_birth_year',
                         'ptr_mate_charc','ptr_drink_slct', 'ptr_health_slct', 'ptr_wed_plan']]
        model_2_df = df[['mem_birth_year', 'ptr_mem_birth_year','mem_loc', 'mate_slct', 'divorce_year',
                         'parents_slct','mate_religion', 'mate_hobby', 'favor_food','ptr_mem_loc', 'ptr_mate_slct',
                         'ptr_divorce_year', 'ptr_parents_slct','ptr_mate_religion', 'ptr_mate_hobby', 'ptr_favor_food']]
        model_3_df = df[['mem_birth_year', 'ptr_mem_birth_year','mate_job','ptr_mate_job',
                         'mate_career', 'ptr_mate_career','mate_weight', 'ptr_mate_weight', 'mate_height',
                         'ptr_mate_height', 'mate_car', 'ptr_mate_car','mate_ann_salary', 'ptr_mate_ann_salary',
                         'possess_property', 'ptr_possess_property']]
        return model_1_df, model_2_df, model_3_df

    # def to_numeric(self, df):
    #     for c in df.columns :
    #         df[c] = pd.to_numeric(df[c])
    #         df[c] = df[c].astype(int)
    #         return df

    def model_predict(self, df, model):
        df = pd.get_dummies(df)
        for fname in model.feature_names_ :
            if fname not in df.columns :
                df[fname] = 0
        return model.predict(df)