from utils.config.common import NavieModel
from utils.config.common import Vectorizer
import warnings
warnings.filterwarnings('ignore')

class predictModel():
    def __init__(self):
        # self.NavieModel = NavieModel
        # self.Vectorizer = Vecorizer
        pass

    def predict_sentence(self, sent):
        prediction= int(''.join(map(str, NavieModel.predict(Vectorizer.transform([sent])))))
        prediction_proba = round(NavieModel.predict_proba(Vectorizer.transform([sent]))[0][1]*100,2)

        if (prediction==1) & (prediction_proba >= 99):
            result = 1
        else:
            result = 0

        return result