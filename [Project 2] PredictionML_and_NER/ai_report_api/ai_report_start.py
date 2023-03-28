import os

os.system("""/home/ggunny/anaconda3/envs/ai_report/bin/gunicorn ai_report_main:app --config ./utils/config/gconf.py""")