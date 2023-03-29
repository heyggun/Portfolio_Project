import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


class ChatbotModel():
    def __init__(self):
        pass

    def Load(self):
        self.data = pd.DataFrame(np.load('./utils/data/chatbot_embedding.npy', allow_pickle=True), columns= ['question','answer','embedding'])
        self.model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')

        return self.data, self.model
