from utils.functions import *
import warnings
warnings.filterwarnings('ignore')

class Model1 :
    def __init__(self):
        pass

    def model_1_transform(self, df):
        df = self.birth_transform(df)
        df = self.char_transform(df)
        df = self.drink_transform(df)
        df = self.health_transform(df)
        df = self.wed_plan_transform(df)
        return df

    # mem_birth_year column (생년) / birth_gap
    def birth_transform(self, df):
        df['birth_gap'] = df['ptr_mem_birth_year'].astype(int) - df['mem_birth_year'].astype(int)
        return df

    # mate_charc column(성격)
    def char_transform(self ,df):
        df['mate_charc'] = df['mate_charc'].apply(lambda x: [int(x) for x in x.split(',') if x.isdecimal()])
        df['ptr_mate_charc'] = df['ptr_mate_charc'].apply(lambda x: [int(x) for x in x.split(',') if x.isdecimal()])

        for i in range(1, 5) :
            df['char_type_'+str(i)] = df['mate_charc'].apply(lambda x : detect_type(globals()['male_char_type']['type_'+str(i)], x))
            df['ptr_char_type_'+str(i)] = df['ptr_mate_charc'].apply(lambda x : detect_type(globals()['female_char_type']['type_'+str(i)],x))

        del df['mate_charc'], df['ptr_mate_charc']

        return df

    # drink_slct column(음주빈도) + smoke_slct column(흡연유무)
    def drink_transform(self, df):
        df['drink_slct'] = df['drink_slct'].apply(drink_code)
        df['ptr_drink_slct'] = df['ptr_drink_slct'].apply(drink_code)
        df['smoke_slct'] = df['smoke_slct'].apply(lambda x: 1 if len(str(x)) > 0 and str(x)[0] == 'c' else 0)
        return df

    # health_slct column(건강관리)
    def health_transform(self, df):
        df['health_slct'] = df['health_slct'].apply(health_code)
        df['ptr_health_slct'] = df['ptr_health_slct'].apply(health_code)
        return df

    # wed_plan column(결혼 계획)
    def wed_plan_transform(self, df):
        df['wed_plan'] = df['wed_plan'].apply(wed_plan_code)
        df['ptr_wed_plan'] = df['ptr_wed_plan'].apply(wed_plan_code)
        # wed_plan_like
        df['wed_plan_like'] = df.apply(lambda x: 1 if x['wed_plan'] == x['ptr_wed_plan'] or x['wed_plan'] == 0
                                                      or x['ptr_wed_plan'] == 0 else 0, axis=1)
        return df


