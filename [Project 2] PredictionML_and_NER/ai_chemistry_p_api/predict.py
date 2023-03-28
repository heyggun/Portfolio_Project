from utils.model.model1_feature import Model1
from utils.model.model2_feature import Model2
from utils.model.model3_feature import Model3
from utils.config.common import *
from utils.functions import *
import warnings
warnings.filterwarnings('ignore')

class predictScore(Model1, Model2, Model3) :
    def __init__(self):
        super(predictScore, self).__init__()

    def get_model_scores(self, df):

        # df = self.to_numeric(df)
        model_1_df, model_2_df, model_3_df = self.data_splitter(df)

        model_1_df = self.model_1_transform(model_1_df)
        model_2_df = self.model_2_transform(model_2_df)
        model_3_df = self.model_3_transform(model_3_df)

        model_1_score = self.model_predict(model_1_df, model_1)
        model_2_score = self.model_predict(model_2_df, model_2)
        model_3_score = self.model_predict(model_3_df, model_3)

        total_score = round(((model_1_score * 0.2) + (model_2_score * 0.3) + (model_3_score * 0.5)), 1)
        return model_1_score, model_2_score, model_3_score, total_score

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

    def to_numeric (self, df):
        for c in df.columns :
            # df[c] = pd.to_numeric(df[c])
            if c in integer_cols :
                df[c] = df[c].astype(int)
            return df

    def model_predict(self, df, model):
        df = pd.get_dummies(df)
        for fname in model.feature_names_ :
            if fname not in df.columns :
                df[fname] = 0
        score = model.predict(df)[0]
        if score > 100 :
            score = 100
        return round(score, 1)