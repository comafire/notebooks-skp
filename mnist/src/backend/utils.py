import os, sys, time
from datetime import datetime, timedelta

def print_response(obj, res):
    print("\n[TEST CASE] {}.{}(), STATUS_CODE: {}, JSON: {}\n".format(obj.__class__.__name__, sys._getframe(1).f_code.co_name, res.status_code, res.json))

def pretty_json(data):
    return json.dumps(data, indent=2, sort_keys=True)

def get_env_sdate(default):
    try:
        return datetime.strptime(os.environ["SDATE"], "%Y-%m-%d %H:%M:%S").strftime("%Y%m%d%H")
    except:
        return default

def get_env_path_base(default):
    try:
        return os.environ["PATH_BASE"]
    except:
        return default

def get_env_path_date(default):
    try:
        return os.environ["PATH_DATA"]
    except:
        return default
