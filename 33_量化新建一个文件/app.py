# coding:utf-8
import datetime

import json
import os
import threading
import traceback
import numpy as np
# import flask.json
import pandas as pd
from flask import Flask, render_template
from flask import jsonify
from flask import request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('result_show.html')



def gen_rand(lenght=100):
    genr = np.random.rand(lenght, 2) / 10 - 0.049
    df_rr = pd.DataFrame(genr)
    df_cum_r = (df_rr + 1).cumprod()
    return {'x_lable':df_cum_r.index.tolist(),
            's1':df_cum_r[0].tolist(),
            's2':df_cum_r[1].tolist()}


@app.route('/result_data')
def result_data():
    return jsonify(gen_rand(200))


if __name__ == '__main__':
    app.run()

