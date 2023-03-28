from predict import *
import warnings
warnings.filterwarnings('ignore')

class getRank(predictScore) :
    def __init__(self, my_info, is_callable, search_type):
        super(getRank, self).__init__()
        self.my_info = my_info
        self.mem_no = my_info.loc[0,'memNo']
        self.mem_sex = my_info.loc[0,'memSex']
        self.is_callable = is_callable
        self.search_type = search_type

    def get_rank(self):
        model_type = detect_model_type(self.search_type)
        model_result = self.model_rank(model_type)
        return model_result

    def model_rank(self,  model_type):
        df = self.get_df(self.my_info, self.mem_no, self.mem_sex)
        df = self.set_model_type(df, model_type, self.is_callable)
        top_n_result = df.sort_values(by=model_type, ascending=False).reset_index(drop=True).head(30).to_dict('index')
        if 'total_score' in df.columns :
            total_top_n_result = df.sort_values(by='total_score', ascending=False).reset_index(drop=True).head(30).to_dict('index')
            result = {'searchTypeScoreList' : top_n_result, 'totalScoreList' : total_top_n_result}
            log_cnt = (len(top_n_result), len(total_top_n_result))
        else :
            result = {'searchTypeScoreList' : top_n_result, 'totalScoreList' : {}}
            log_cnt = (len(top_n_result), 0)
        return result, log_cnt