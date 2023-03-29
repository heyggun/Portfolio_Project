from utils.train.train_data_processor import trainDataProcessor
from utils.config.common import conf
from buffalo.algo.als import ALS , inited_CUALS
from buffalo.algo.options import ALSOption
from buffalo.misc import aux
from buffalo.data.mm import MatrixMarketOptions
import numpy as np
from scipy.io import mmwrite
import scipy.sparse as sp
import pandas as pd
# from logger import *
import os

dataPath = conf.dataPath

class optimizer(trainDataProcessor) :
    def __init__(self):
        super().__init__()
        self.female_path = conf.dataPath + '/female'
        self.male_path = conf.dataPath + '/male'

    def params_opt(self):
        self.total_score_gen()
        df = pd.read_pickle(f'{dataPath}/female_score.pkl')
        self.optimizer(df, self.female_path)
        df = pd.read_pickle(f'{dataPath}/male_score.pkl')
        self.optimizer(df, self.male_path)

    def optimizer(self, df, path):
        user_items, uid_to_idx, idx_to_uid, mid_to_idx, idx_to_mid = self.df_to_matrix(df, 'mem_no', 'ptr_mem_no')
        if not os.path.exists(path) :
            os.mkdir(path)
        mmwrite(f'{path}/main.mtx', user_items)
        iid = list(idx_to_mid.values())
        uid = list(idx_to_uid.values())
        with open(f"{path}/uid", "w") as f:
            for val in uid:
                print(val, file=f)
        f.close()
        with open(f"{path}/iid", "w") as f:
            for val in iid:
                print(val, file=f)
        f.close()
        opt = ALSOption().get_default_option()
        opt.num_workers = 6
        opt.num_iters = 20
        opt.evaluation_period = 20
        opt.evaluation_on_learning = True
        opt.save_best = True
        opt.accelerator = True

        data_opt = MatrixMarketOptions().get_default_option()
        data_opt.input.main = f'{path}/main.mtx'
        data_opt.input.iid = f'{path}/iid'
        data_opt.input.uid = f'{path}/uid'
        data_opt.data.path = f'{path}/mm.h5py'
        data_opt.data.validation.p = 0.1
        data_opt.data.validation.max_samples = 5000

        opt.validation = aux.Option({'topk': 10})
        opt.tensorboard = aux.Option({'root': f'{path}/als-validation', 'name': 'als-new'})

        opt.optimize = aux.Option({
            'loss': 'val_ndcg',
            'max_trials': 100,
            'deployment': True,
            'start_with_default_parameters': False,
            'space': {
                'd': ['randint', ['d', 10, 128]],
                'reg_u': ['uniform', ['reg_u', 0.1, 1.0]],
                'reg_i': ['uniform', ['reg_i', 0.1, 1.0]],
                'alpha': ['randint', ['alpha', 1, 10]]
            }
        })
        # train_log('--------*')
        # train_log(opt)
        # train_log('--------*')
        als = ALS(opt, data_opt=data_opt)
        als.initialize()

        als.opt.model_path = f"{path}/als-best-model.bin"
        als.optimize()
        als.get_optimization_data()
        del als


    def get_df_matrix_mappings(self, df, row_name, col_name):
        rid_to_idx = {}
        idx_to_rid = {}
        for (idx, rid) in enumerate(df[row_name].unique().tolist()):
            rid_to_idx[rid] = idx
            idx_to_rid[idx] = rid

        cid_to_idx = {}
        idx_to_cid = {}
        for (idx, cid) in enumerate(df[col_name].unique().tolist()):
            cid_to_idx[cid] = idx
            idx_to_cid[idx] = cid

        return rid_to_idx, idx_to_rid, cid_to_idx, idx_to_cid

    def df_to_matrix(self, df, row_name, col_name):

        rid_to_idx, idx_to_rid, cid_to_idx, idx_to_cid = self.get_df_matrix_mappings(df, row_name, col_name)

        def map_ids(row, mapper):
            return mapper[row]

        I = df[row_name].apply(map_ids, args=[rid_to_idx]).to_numpy()
        J = df[col_name].apply(map_ids, args=[cid_to_idx]).to_numpy()
        V = np.ones(I.shape[0])
        interactions = sp.coo_matrix((V, (I, J)), dtype=np.float64)
        interactions = interactions.tocsr()

        return interactions, rid_to_idx, idx_to_rid, cid_to_idx, idx_to_cid