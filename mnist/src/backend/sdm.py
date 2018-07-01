from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os, uuid, base62

import numpy as np
np.set_printoptions(precision=5)

import pandas as pd
pd.set_option('display.max_rows', None) 
pd.set_option('display.max_columns', None) 
pd.set_option('display.max_colwidth', -1)
pd.options.display.float_format = '{:,.5f}'.format

import io, sys, logging, imp, json
import time, pickle, requests, json
from datetime import datetime, timedelta
from os import listdir
from os.path import isfile, join

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

sys.path.append('..')
from utils import *

# Data Model
dim_x = 784
img_rows, img_cols = 28, 28
input_shape = (img_rows, img_cols, 1)
n_class = 10
sdate = get_env_sdate(default = "2018070108")
path_data = get_env_path_date(default = "/root/mnt/dfs/data/mnist")

# GPU 설정
import tensorflow as tf
from keras import backend as k

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
k.tensorflow_backend.set_session(sess)
        
# 모델 로드
from fdm_model import *

dm_dnn = create_dnn(n_input = dim_x, n_class = n_class)
dm_dnn.summary()

dm_cnn = create_cnn(input_shape = input_shape, n_class=n_class)
dm_cnn.summary()

# weight 로드
path_fdm = os.path.join(path_data, "fdm")
path_fdm_sdate = os.path.join(path_fdm, sdate)
path_dm_dnn = os.path.join(path_fdm_sdate, "dnn-best.hdf5")
dm_dnn.load_weights(path_dm_dnn)

path_dm_cnn = os.path.join(path_fdm_sdate, "cnn-best.hdf5")
dm_cnn.load_weights(path_dm_cnn)

# scaler 로드
from sklearn.externals import joblib 

path_etl = os.path.join(path_data, "etl")
path_etl_sdate = os.path.join(path_etl, sdate)

path_scaler_dnn = os.path.join(path_etl_sdate, "dnn-scaler.pkl")
scaler_dnn = joblib.load(path_scaler_dnn)

path_scaler_cnn = os.path.join(path_etl_sdate, "cnn-scaler.pkl")
scaler_cnn = joblib.load(path_scaler_cnn)

# Flask
app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET"]

app.config['JWT_SECRET_KEY'] = os.environ["FLASK_SECRET"]

jwt = JWTManager(app)
api = Api(app)

@app.route("/")
def index():
    return "flask-skp-mnist"

from sdm_dnn import DNN
from sdm_cnn import CNN

api.add_resource(DNN, '/v1/dnn', 
                 resource_class_kwargs={'sess': sess, 'scaler': scaler_dnn, 'dm': dm_dnn, 'dim_x' : dim_x})
api.add_resource(CNN, '/v1/cnn', 
                 resource_class_kwargs={'sess': sess, 'scaler': scaler_cnn, 'dm': dm_cnn, 'input_shape' : input_shape})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, use_reloader=True, threaded=True)
