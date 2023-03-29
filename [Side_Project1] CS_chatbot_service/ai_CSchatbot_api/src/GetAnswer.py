import pandas as pd
from numpy import dot
from numpy.linalg import norm
from utils.model.model import SentenceTransformer
from sentence_transformers import SentenceTransformer

class getAnswer():
    def __init__(self, model, data):
        self.model = model
        self.data = data


    def cos_sim(self, a,b):
        return dot(a,b) / (norm(a)*norm(b))

    def return_answer(self, question):
        embedding = self.model.encode(question)
        self.data['score'] = self.data.apply(lambda x: self.cos_sim(x['embedding'], embedding), axis=1)
        return self.data.loc[self.data['score'].idxmax()]['answer']

