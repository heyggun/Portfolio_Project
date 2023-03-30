from utils.config.common import Model
from utils.config.common import Embedding
from numpy.linalg import norm
from numpy import dot
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import os

class ChatModel() :
    def __init__(self):
        # self.model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
        # self.edata = pd.DataFrame(np.load("utils/model/chatEmbedding.npy", allow_pickle=True),
        #                               columns=['question', 'answer', 'embedding'])
        pass

    def getAnser(self, question):
        def cos_sim(a, b):
            return dot(a, b) / (norm(a) * norm(b))
        
        embedding = Model.encode(question)
        Embedding['score'] = Embedding.apply(lambda x: cos_sim(x['embedding'], embedding), axis=1)
        return Embedding.loc[Embedding['score'].idxmax()]['answer']