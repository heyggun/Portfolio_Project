import buffalo.data
from buffalo.algo.als import ALS, inited_CUALS
from buffalo.data.mm import MatrixMarketOptions
from utils.model.optimizer import optimizer
import os

class trainModel(optimizer) :
    def __init__(self):
        super().__init__()

    def train(self):
        self.params_opt()
        self.als_female()
        self.als_male()
        if 'dev' not in self.male_path :
            self.send_file()

    def als_female(self):
        opt_model = ALS()
        opt_model.load(f'{self.female_path}/als-best-model.bin')

        data_opt = MatrixMarketOptions().get_default_option()
        data_opt.input.main = f'{self.female_path}/main.mtx'
        data_opt.input.iid = f'{self.female_path}/iid'
        data_opt.input.uid = f'{self.female_path}/uid'
        data_opt.data.validation.p = 0.1
        data_opt.data.validation.max_samples = 10000
        data_opt.data.path = f'{self.female_path}/mm.h5py'

        data = buffalo.data.load(data_opt)
        data.create()

        model = ALS(opt_model.opt, data=data)
        model.initialize()
        model.train()
        model.save(f'{self.female_path}/als_model_female')

    def als_male(self):
        opt_model = ALS()
        opt_model.load(f'{self.male_path}/als-best-model.bin')

        data_opt = MatrixMarketOptions().get_default_option()
        data_opt.input.main = f'{self.male_path}/main.mtx'
        data_opt.input.iid = f'{self.male_path}/iid'
        data_opt.input.uid = f'{self.male_path}/uid'
        data_opt.data.validation.p = 0.1
        data_opt.data.validation.max_samples = 10000
        data_opt.data.path = f'{self.male_path}/mm.h5py'

        data = buffalo.data.load(data_opt)
        data.create()

        model = ALS(opt_model.opt, data=data)
        model.initialize()
        model.train()
        model.save(f'{self.male_path}/als_model_male')

    def send_file(self):
        # send model files to a16 (real)
        os.system('/bin/rsync -a /home/gguny/ai_data/recomm_data/female 000.000.0.00::ai_data/recomm_data')
        os.system('/bin/rsync -a /home/gguny/ai_data/recomm_data/male 000.000.0.00::ai_data/recomm_data')


if __name__ == '__main__' :
    t = trainModel()
    t.train()