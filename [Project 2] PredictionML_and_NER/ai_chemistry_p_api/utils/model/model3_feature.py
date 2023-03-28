from utils.functions import *
import warnings
warnings.filterwarnings('ignore')

#
class Model3 :
    def __init__(self):
        pass

    def model_3_transform(self, df):
        df = self.birth_transform(df)
        df = self.job_transform(df)
        df = self.height_weight_transform(df)
        df = self.career_transform(df)
        df = self.car_transform(df)
        df = self.salary_transform(df)
        df = self.possess_transform(df)
        return df

    # mem_birth_year column (생년) / birth_gap
    def birth_transform(self, df):
        df['birth_gap'] = int(df.loc[0, 'ptr_mem_birth_year']) - int(df.loc[0, 'mem_birth_year'])
        return df

    # mate_job column (직업)
    def job_transform(self, df):
        df['mate_job'] = df['mate_job'].apply(job_code)
        df['ptr_mate_job'] = df['ptr_mate_job'].apply(job_code)
        df['job_like'] = df.apply(lambda x: 1 if x['mate_job'] == x['ptr_mate_job'] else 0, axis=1)
        return df

    # mate_height / mate_weight column (키, 몸무게)
    def height_weight_transform(self, df):
        df['height_gap'] = df['mate_height'] - df['ptr_mate_height']
        df['mate_bmi'] = df['mate_weight'] / ((df['mate_height'] * 0.01)) ** 2
        df['ptr_mate_bmi'] = df['ptr_mate_weight'] / ((df['ptr_mate_height'] * 0.01)) ** 2
        return df

    # mate_career column (학력)
    def career_transform(self, df):
        df['mate_career'] = df['mate_career'].apply(career_code)
        df['ptr_mate_career'] = df['ptr_mate_career'].apply(career_code)
        return df

    # mate_car column (차량)
    def car_transform(self, df):
        df['mate_car'] = df['mate_car'].apply(lambda x: 0 if x == 9 else 1)
        df['ptr_mate_car'] = df['ptr_mate_car'].apply(lambda x: 0 if x == 9 else 1)
        return df

    # mate_salary column (연봉)
    def salary_transform(self, df):
        df['mate_ann_salary'] = df['mate_ann_salary'].apply(salary_code)
        df['ptr_mate_ann_salary'] = df['ptr_mate_ann_salary'].apply(salary_code)
        df['sal_like'] = df.apply(lambda x: 1 if x['mate_ann_salary'] == x['ptr_mate_ann_salary'] else 0, axis=1)
        df['sal_gap'] = df['mate_ann_salary'] - df['ptr_mate_ann_salary']
        return df

    # possess_property column (재산)
    def possess_transform(self, df):
        df['possess_property'] = df['possess_property'].apply(pos_code)
        df['ptr_possess_property'] = df['ptr_possess_property'].apply(pos_code)
        df['possess_like'] = df.apply(lambda x: 1 if x['possess_property'] == x['ptr_possess_property'] else 0, axis=1)
        df['pos_gap'] = df['possess_property'] - df['ptr_possess_property']
        return df

