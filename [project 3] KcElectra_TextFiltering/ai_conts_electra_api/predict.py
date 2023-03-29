import torch
from transformers import AutoTokenizer
import torch.nn.functional as F
import numpy as np
from preprocessing import Preprocessing


class predictModel():

    def __init__(self, model_path):
        # load model
        self.model_path = model_path
        self.model = torch.load(model_path)
        # set device
        self.device = torch.device('cpu')
        # load tokenizer
        model_name = 'beomi/KcELECTRA-base'
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

    def predict_sentence(self, sent):
        self.model.eval()
        Pr = Preprocessing(sent)

        if 'call' in str(self.model_path):
            sent = Pr.f_clean_sentence()

        else:
            sent = Pr.clean_sentence()

        # tokenizing
        tokenized_sent = self.tokenizer(
            sent,
            return_tensors='pt',
            truncation=True,
            add_special_tokens=True,
            max_length=512
        )
        tokenized_sent.to(self.device)

        # prediction
        with torch.no_grad():
            outputs = self.model(
                input_ids=tokenized_sent['input_ids'],
                attention_mask=tokenized_sent['attention_mask'],
                token_type_ids=tokenized_sent['token_type_ids']
            )

        # result
        per = int(str(np.array(F.softmax(outputs[0][0], dim=0).detach().cpu())[1] * 100).split('.')[0])

        if len(sent) == 0:
            return 1

        # result percent 99 upper
        if int(per) >= 97:
            return 1

        else:
            return 0