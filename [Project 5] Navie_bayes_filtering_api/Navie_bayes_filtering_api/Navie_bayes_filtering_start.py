import os

os.system("""/home/gguny/anaconda3/envs/conts_torch/bin/gunicorn Navie_bayes_filtering_main:app --config ./utils/config/gconf.py""")