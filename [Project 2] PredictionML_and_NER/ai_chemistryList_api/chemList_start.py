import os
os.system("""/home/gguny/anaconda3/envs/chem_list/bin/gunicorn chemList_main:app --config ./utils/config/gconf.py""")