import os

os.system("""/home/ggunny/anaconda3/envs/chem_p/bin/gunicorn chemistry_main:app --config ./utils/config/gconf.py""")