import json
import sys
import threading
import time
import requests
from flask import Flask, request
from flask_restful import Api


app = Flask(__name__)
api = Api(app)

local = dict()  # Dizionario con i sensori locali
other = dict()  # Dizionario dei sensori afferenti ad altri nodi fog


@app.route('/', methods=["GET"])
def usage():
    return {'Welcome to the progetto ammazzata!': 'bah'}


@app.route('/all', methods=["GET"])
def get_all():
    total = other.copy()
    total.update(local)

    return {'sensors': total}


@app.route('/update', methods=["POST"])
def update():
    try:

        sensor_num = request.form['num']
        sensor_val = request.form['val']

        if sensor_num not in local:
            local[sensor_num] = sensor_val
        else:
            local.update({sensor_num: sensor_val})

        return {'DONE': "OK"}

    except Exception as e:

        return {'Exception': e.args}


@app.route('/merge', methods=["POST"])
def merge():
    try:

        sens = json.loads(request.data)

        for key, value in sens.items():
            if key not in other:
                other[key] = value
            else:
                other.update({key: value})

        return {'DONE': "OK"}

    except Exception as e:

        app.logger.error(e.args)

        return {'Exception': e.args}


def sending_thread():
    while True:
        time.sleep(5)

        print(local, file=sys.stderr)
        print(other, file=sys.stderr)

        data = json.dumps(local)

        r = requests.post("http://" + "fog0" + ":" + str(8080) + "/merge",
                          data=data)
        print(r, file=sys.stderr)
        r = requests.post("http://" + "fog1" + ":" + str(8080) + "/merge",
                          data=data)
        print(r, file=sys.stderr)
        r = requests.post("http://" + "fog2" + ":" + str(8080) + "/merge",
                          data=data)
        print(r, file=sys.stderr)


if __name__ == '__main__':

    t = threading.Thread(target=sending_thread)
    t.start()
    app.run(host='0.0.0.0', debug=True, port='8080')
