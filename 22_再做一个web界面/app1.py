from flask import Flask, request
from flask import render_template
from flask import jsonify
import decimal
import flask.json
import json,time
from datetime import timedelta

class MyJSONEncoder(flask.json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)


app = Flask(__name__)
app.json_encoder = MyJSONEncoder
app.config['DEBUG']=True
app.config['SEND_FILE_MAX_AGE_DEFAULT']=timedelta(seconds=1)

@app.route('/')
def main():
    return render_template("main.html")


@app.route('/time')
def get_time():
    str_time = time.strftime("%Y{}%m{}%d{} %X")
    return str_time.format("年", "月", "日")

@app.route('/hmm')
def hmm():
    import akshare as ak
    bond_df = ak.bond_spot_deal()
    print(dict(bond_df))
    return 'aaa'
    # return jsonify(bond_df)

if __name__ == '__main__':
    app.run()
