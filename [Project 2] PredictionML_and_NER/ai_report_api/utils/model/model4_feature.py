from utils.functions import *
from utils.config.common import *
import pandas as pd
import numpy as np
from konlpy.tag import Mecab
import warnings
warnings.filterwarnings('ignore')

class Model4 :
    def __init__(self):
        pass

    def model_4_transform(self, df):
        df['tokens'] = df['mate_conts'].apply(mecab_tokenize)
        df['ptr_tokens'] = df['ptr_mate_conts'].apply(mecab_tokenize)

        ner, keywords = self.get_keywords(df['tokens'].values[0])
        ptr_ner, ptr_keywords = self.get_keywords(df['ptr_tokens'].values[0])

        df['ptr_ners'], df['ners'] = '', ''
        df['ptr_keywords'], df['keywords'] = '', ''
        df.loc[:, 'ners'].loc[0] = ner
        df.loc[:, 'keywords'].loc[0] = keywords
        df.loc[:, 'ptr_ners'].loc[0] = ptr_ner
        df.loc[:, 'ptr_keywords'].loc[0] = ptr_keywords

        return df

    def get_keywords(self, tokens):
        ner_dict = model_4.set_index('text').to_dict()['ner']

        try:
            ners = list()
            ner_lst = list()
            pos_lst = list()
            keywords = list()

            if len(tokens) != 0:
                for token in tokens:
                    if token in ner_dict.keys():
                        NER = ner_dict[token]
                        ners.append(NER)
                        ner_lst.append(token)
                    else:
                        pos_lst.append(token)

                total_lst = ner_lst + pos_lst
                keywords.append(total_lst)
            else:
                keywords.append([None])
        except:
            keywords.append([None])

        return list(set(ners)), list(set(keywords[0]))

