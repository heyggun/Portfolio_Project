from utils.config.common import m_model, f_model

# m_model = ALS()
# m_model.load(f'{MALE_PATH}/als_model_male')
#
# f_model = ALS()
# f_model.load(f'{FEMALE_PATH}/als_model_female')

class ALS :
    def __init__(self, mem_no, mem_sex, ptr_mem_no, isCallable):
        self.mem_no = str(mem_no)
        self.mem_sex = mem_sex
        self.ptr_mem_no = str(ptr_mem_no)
        self.isCallable = isCallable

    def get_recomm(self):
        sim = self.get_sim()
        topk = self.get_topk()
        recomm = {'topK' : topk, 'Sim' : sim}
        return recomm

    def get_sim(self):
        if self.isCallable:
            sim = m_model.most_similar(self.ptr_mem_no, 140) if self.mem_sex == 'm' else f_model.most_similar(
                self.ptr_mem_no, 140)
            try:
                sim = sim[70:]
            except:
                sim = []
        else:
            sim = m_model.most_similar(self.ptr_mem_no, 70) if self.mem_sex == 'm' else f_model.most_similar(
                self.ptr_mem_no, 70)

        sim_list = []
        if type(sim) == list and len(sim) > 0:
            sim_list = [int(s[0]) for s in sim]
        return sim_list

    def get_topk(self) :
        if self.isCallable :
            topk = m_model.topk_recommendation(self.mem_no, 140) if self.mem_sex == 'm' else f_model.topk_recommendation(
                self.mem_no, 140)
            try:
                topk = topk[70:]
            except:
                topk = []
        else :
            topk = m_model.topk_recommendation(self.mem_no, 70) if self.mem_sex == 'm' else f_model.topk_recommendation(
                self.mem_no, 70)

        topk_list = []
        if type(topk) == list and len(topk) > 0:
            topk_list = [int(s) for s in topk]
        return topk_list