import os
os.system("""/home/gguny/anaconda3/envs/recom/bin/gunicorn rrs_main:app --config utils/config/gconf.py""")