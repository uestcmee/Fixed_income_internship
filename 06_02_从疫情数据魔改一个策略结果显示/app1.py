from flask import Flask, request
from flask import render_template
from flask import jsonify
import utils
import decimal
import flask.json
import json
from datetime import timedelta

class MyJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


app = Flask(__name__)
app.json_encoder = MyJSONEncoder
app.config['DEBUG']=True
app.config['SEND_FILE_MAX_AGE_DEFAULT']=timedelta(seconds=1)

@app.route('/')
def main():
    return render_template("main.html")


@app.route('/lookback',methods=['GET','POST'])
def fetch_lookback_data():
    lf,sf,lm,sm=0,0,0,0
    if request.method=='POST':
        data=request.get_data()
        json_obj=json.loads(data)
        print(json_obj)
        lm=json_obj['lm']
        sm=json_obj['sm']
        lf=json_obj['lf']
        sf=json_obj['sf']
    else:
        print('not request')
    data = utils.fetch_lookback_data(float(lf),float(sf),int(lm),int(sm))
    [day,stg_r, idx_r] = data
    return jsonify({'day': day, 'stg_r': stg_r, 'idx_r': idx_r})



@app.route('/time')
def get_time():
    return utils.get_time()


if __name__ == '__main__':
    app.run()
