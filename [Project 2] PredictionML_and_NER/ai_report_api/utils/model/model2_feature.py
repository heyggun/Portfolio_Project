from utils.functions import *


class Model2 :
    def __init__(self):
        pass

    def model_2_transform(self, df):
        df = self.birth_transform(df)
        df = self.food_transform(df)
        df = self.hobby_transform(df)
        df = self.loc_transform(df)
        df = self.marriage_divorce_transform(df)
        df = self.religion_transform(df)
        return df

    # mem_birth_year column (생년) / birth_gap
    def birth_transform(self, df):
        df['birth_gap'] = int(df.loc[0, 'ptr_mem_birth_year']) - int(df.loc[0, 'mem_birth_year'])
        return df

    # favor_food column (선호음식)
    def food_transform(self, df):
        df['favor_food'] = df['favor_food'].apply(lambda x: [int(i) if i.isdecimal() else 1 for i in str(x).split(',')])
        df['ptr_favor_food'] = df['ptr_favor_food'].apply(lambda x: [int(i) if i.isdecimal() else 1 for i in str(x).split(',')])

        for i in range(1, 10) :
            df['food_type_'+str(i)] = df['favor_food'].apply(lambda x : detect_type(globals()['favor_food_type']['type_'+str(i)], x))
            df['ptr_food_type_'+str(i)] = df['ptr_favor_food'].apply(lambda x : detect_type(globals()['favor_food_type']['type_'+str(i)], x))
            if i == 1 :
                df['food_like_cnt'] = df.apply(lambda x : 1 if x['food_type_'+str(i)]==1 and x['ptr_food_type_'+str(i)] else 0, axis=1)
            else :
                df['food_like_cnt'] = df.apply(lambda x : x['food_like_cnt']+1 if x['food_type_'+ str(i)]==1
                                              and x['ptr_food_type_'+str(i)]==1 else x['food_like_cnt'], axis=1)

        del df['favor_food'], df['ptr_favor_food']

        return df

    # mate_hobby column(취미)
    def hobby_transform(self, df):
        df['mate_hobby'] = df['mate_hobby'].apply(lambda x: [int(i) for i in x.split(',') if i.isdecimal()])
        df['ptr_mate_hobby'] = df['ptr_mate_hobby'].apply(lambda x: [int(i) for i in x.split(',') if i.isdecimal()])

        for i in range(1, 5):
            df['hobby_type_' + str(i)] = df['mate_hobby'].apply(
                lambda x: detect_type(globals()['hobby_type']['type_' + str(i)],x))
            df['ptr_hobby_type_' + str(i)] = df['ptr_mate_hobby'].apply(
                lambda x: detect_type(globals()['hobby_type']['type_' + str(i)], x))
            if i == 1:
                df['hobby_like_cnt'] = df.apply(
                    lambda x: 1 if x['food_type_' + str(i)] == 1 and x['ptr_hobby_type_' + str(i)] else 0, axis=1)
            else:
                df['hobby_like_cnt'] = df.apply(lambda x: x['hobby_like_cnt'] + 1 if x['hobby_type_' + str(i)] == 1
                                                 and x['ptr_hobby_type_' + str(i)] == 1 else x['hobby_like_cnt'], axis=1)

        del df['mate_hobby'], df['ptr_mate_hobby']

        return df

    # mem_loc column(지역)
    def loc_transform(self, df):
        df['mem_loc'] = df['mem_loc'].apply(lambda x : 'q' if x == 'y' else x)
        df['ptr_mem_loc'] = df['ptr_mem_loc'].apply(lambda x : 'q' if x == 'y' else x)
        df['loc_like'] = df.apply(lambda x: get_loc_score(x['mem_loc'], x['ptr_mem_loc']), axis=1)
        return df

    # mate_slct(결혼상태) / divorce year column(이혼년도)
    def marriage_divorce_transform(self, df):
        df['marriage_like'] = df.apply(lambda x : 1 if x['mate_slct'] == x['ptr_mate_slct'] else 0, axis=1)
        df['divorce_year'].fillna(0, inplace=True)
        df['ptr_divorce_year'].fillna(0, inplace=True)
        return df

    # mate_religion column(종교)
    def religion_transform(self, df):
        df['mate_religion'] = df['mate_religion'].apply(religion_code)
        df['ptr_mate_religion'] = df['ptr_mate_religion'].apply(religion_code)
        df['religion_like'] = df.apply(lambda x : 1 if x['mate_religion'] == x['ptr_mate_religion'] and x['mate_religion'] != 3
                                                       and x['ptr_mate_religion']!=3 else 0, axis=1)
        return df