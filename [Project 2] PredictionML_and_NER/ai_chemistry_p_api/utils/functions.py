import pandas as pd

column_keys = {'memNo' : 'mem_no', 'memBirthYear' : 'mem_birth_year', 'memLoc' :  'mem_loc',
               'mateAnnSalary' : 'mate_ann_salary', 'mateCharc' :'mate_charc','smokeSlct': 'smoke_slct',
               'drinkSlct' : 'drink_slct', 'healthSlct' : 'health_slct', 'wedPlan' : 'wed_plan',
               'mateSlct' : 'mate_slct', 'divorceYear' : 'divorce_year', 'parentsSlct' :  'parents_slct',
               'mateReligion' : 'mate_religion', 'mateHobby' : 'mate_hobby', 'favorFood' :  'favor_food',
               'mateJob': 'mate_job', 'mateCareer' : 'mate_career', 'mateHeight' : 'mate_height',
                'mateWeight': 'mate_weight', 'mateCar' : 'mate_car', 'possessProperty' : 'possess_property'}
column_keys_f = {}
for i, j in zip(column_keys.keys(), column_keys.values()) :
    column_keys_f[i] = 'ptr_' + j

integer_cols = ['mem_no', 'ptr_mem_no', 'mem_birth_year', 'ptr_mem_birth_year',
                'mate_job', 'ptr_mate_job', 'mate_ann_salary', 'ptr_mate_ann_salary',
                'mate_religion', 'ptr_mate_religion', 'mate_car', 'ptr_mate_car', 'mate_career', 'ptr_mate_career',
                'divorce_year', 'ptr_divorce_year', 'mate_height', 'mate_weight']

favor_food_type = {'type_1': [5, 12, 13, 15, 92, 93, 96, 97, 98],
                   'type_2': [72, 73, 74, 75, 76, 77, 82, 83],
                   'type_3': [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46],
                   'type_4': [47, 49, 50, 52, 54, 48, 57, 63, 64, 70, 71, 94, 95, 99],
                   'type_5': [6, 16, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                   'type_6': [8, 9, 10, 14, 17],
                   'type_7': [51, 53, 55, 56, 59, 60, 61, 62, 65],
                   'type_8': [1, 2, 3, 4, 7, 18, 80, 100],
                   'type_9': [11, 31, 58, 66, 67, 68, 69, 79, 81, 84, 85, 86, 87, 88]}

hobby_type = {'type_1': [11, 12, 18, 40, 41, 42, 43, 44],
              'type_2': [8, 15, 16, 19],
              'type_3': [1, 3, 4, 6, 13, 14, 21, 24, 25, 26, 27, 30, 32, 33, 34, 35, 39],
              'type_4': [5, 7, 17, 28, 29]}

male_char_type = {'type_1': [3, 5, 9, 13],
                  'type_2': [1, 10, 11, 17, 19],
                  'type_3': [4, 6, 8],
                  'type_4': [2, 12, 14, 15, 16, 18]}

female_char_type = {'type_1': [1, 10, 11, 17, 19],
                    'type_2': [1, 2, 11, 12, 20, 22],
                    'type_3': [4, 5, 7, 14, 9],
                    'type_4': [16, 17, 18, 19, 21, 13]}

drink_key = {'a' : 0 ,'b' : 1, 'c' : 2, 'd' : 3}
health_key = {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3}
wed_plan_key = {'a': 0, '3m': 1, '6m': 2, '1y': 3}
job_key = {1: 'c', 2: 'c', 3: 'l', 4: 'l', 5: 'n', 6: 'i', 7: 'i', 8: 'i', 9: 'j', 10: 'd', 11: 'k', 12: 'k', 13: 'n',
            14: 'h', 15: 'h', 16: 'a', 17: 'a', 18: 'g', 19: 'b', 20: 'm', 21: 'o', 22: 'f', 23: 'k', 24: 'n', 25: 'e',
            26: 'e', 27: 'n', 28: 'e', 29: 'e', 0: 'e', 30: 'o', 31: 'o', 32: 'o', 33: 'j', 34: 'o', 35: 'l', 36: 'l',
            37: 'j', 38: 'n', 39: 'j', 40: 'j', 41: 'j', 42: 'j', 43: 'n', 44: 'k', 45: 'k', 46: 'c', 47: 'j', 48: 'b',
            49: 'h', 50: 'c', 51: 'c', 52: 'c', 53: 'j', 54: 'j', 55: 'j', 56: 'j', 57: 'k', 58: 'j', 59: 'i', 60: 'i',
            61: 'i', 62: 'i', 63: 'i', 64: 'i', 65: 'i', 66: 'i', 67: 'i', 68: 'g', 69: 'g', 70: 'k', 71: 'k', 72: 'h',
            73: 'g', 74: 'h', 75: 'h', 76: 'h', 77: 'h', 78: 'h', 79: 'h', 80: 'g', 81: 'a', 82: 'a', 83: 'i', 84: 'i',
            85: 'i', 86: 'a', 87: 'n', 88: 'i', 89: 'i', 90: 'i', 91: 'i', 92: 'n', 93: 'b', 94: 'b', 95: 'b', 96: 'm',
            97: 'n', 98: 'f', 99: 'f', 100: 'f', 101: 'f', 102: 'a', 103: 'f'}
career_key = {0 : 1, 1: 1, 2: 1, 3 : 3, 4: 4, 5: 4, 6 : 2,7 : 2, 8 : 2, 9 : 4, 10 : 4, 11 : 4, 12 : 2}
salary_key = {1 : 1,2 : 1,3: 1,4 : 2,5: 2,6 : 3,7 : 3,8 : 3, 9 : 3,10 : 4, 13 : 5, 14 : 6,15 : 7,16 :7, 17:7, 12 : 1}
possess_key = {'b' : 1, 'c' : 1, 'd' : 1, 'e' : 2, 'f' : 3, 'g' : 4, 'h' : 5 ,'m' : 6, 'i' : 7,'j' : 7, 'k' : 7, 'l' : 7, 'n' : 7}


def make_base_dataframe(male, female) :
    mate_male = pd.DataFrame([male])
    mate_male = mate_male.rename(columns=column_keys)
    mate_female = pd.DataFrame([female])
    mate_female = mate_female.rename(columns=column_keys_f)
    df = pd.concat([mate_male, mate_female], axis=1)

    return df

def detect_type(type_li, a_type):
    for i in type_li:
        if i in a_type:
            return 1
    else:
        return 0

def drink_code(drink) :
    result = 0
    if len(str(drink)) == 0 :
        return result

    if str(drink)[0].isalpha() and str(drink)[0] in drink_key.keys() :
        result = drink_key[str(drink)[0]]
    return result

def health_code(health) :
    result = 0
    if len(str(health)) == 0 :
        return result

    if str(health)[0].isalpha() and str(health)[0] in health_key.keys() :
        result = health_key[str(health)[0]]
    return result

def wed_plan_code(wed):
    result = 0
    if wed in wed_plan_key.keys():
        result = wed_plan_key[wed]
    return result

def get_loc_score(x, y):
    if x == y :
        return 2
    # 세종
    elif x in ['g', 'o', 'z'] and y in ['g', 'o', 'z']:
        return 1
    # 경기
    elif x == 'b' and y in ['i', 'k']:
        return 1
    # 광주 / 전남
    elif x in ['e', 'l'] and y in ['e', 'l']:
        return 1
    # 전남 / 전북
    elif x in ['l', 'n'] and y in ['l', 'n']:
        return 1
    # 충남 / 충북
    elif x in ['o', 'p'] and y in ['o', 'p']:
        return 1
    # 경남 / 경북
    elif x in ['c', 'd'] and y in ['c', 'd']:
        return 1
    # 경남 / 부산
    elif x in ['c', 'h'] and y in ['c', 'h']:
        return 1
    # 경남 / 울산
    elif x in ['c', 'j'] and y in ['c', 'j']:
        return 1
    # 경북 / 대구
    elif x in ['d', 'f'] and y in ['d', 'f']:
        return 1
    # 충남 / 대전
    elif x in ['o', 'g'] and y in ['o', 'g']:
        return 1

    else:
        return 0

def religion_code(x) :
    if str(x).isdecimal() :
        if int(x) == 5 :
            return str(0)
        elif int(x) != 2 and int(x) != 1 :
            return str(3)
        else :
            return str(x)
    else :
        return str(0)

def job_code(my_job):
    if str(my_job).isnumeric() and int(my_job) in job_key.keys():
        result = job_key[int(my_job)]
    else:
        result = job_key[1]
    return result

def career_code(c) :
    if str(c).isdecimal() and int(c) in career_key.keys():
        result = career_key[int(c)]
    else :
        result = 3
    return result

def salary_code(sal) :
    if str(sal).isdecimal() and int(sal) in salary_key.keys() :
        result = salary_key[int(sal)]
    else :
        result = 1
    return result

def pos_code(pos) :
    if str(pos).isalpha() and pos in possess_key.keys() :
        result = possess_key[pos]
    else :
        result = 1
    return result