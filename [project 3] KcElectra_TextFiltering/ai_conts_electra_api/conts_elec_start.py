import os

os.system("""/home/gguny/anaconda3/envs/conts_torch/bin/gunicorn conts_elec_main:app --config ./utils/config/gconf.py""")