import json
import sys
import threading
import time
import requests
from flask import Flask, request, jsonify
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

local = dict()  # Dizionario con i sensori locali
other = dict()  # Dizionario dei sensori afferenti ad altri nodi fog

auto = dict()   # Numero di volte in cui quel parcheggio è stato preso nell'ultima ora
stats = dict()  # Dizionario con le statistiche dell'ultima settimana

server_ip = "3.232.43.204"
server_port = 5000


@app.route('/', methods=["GET"])
def usage():
    return {'Welcome to the progetto ammazzata!': 'bah'}


@app.route('/all', methods=["GET"])
def get_all():
    total = other.copy()
    total.update(local)

    return jsonify(total)


@app.route('/stats', methods=["GET"])
def get_stats():
    r = requests.get("http://" + server_ip + ":" + str(server_port) + "/get_stat")
    print(r, file=sys.stderr)

    data = json.loads(r.text)

    return jsonify(data)


@app.route('/update', methods=["POST"])
def update():

    try:

        sensor_num = request.form['num']
        sensor_val = request.form['val']

        if sensor_num not in local:
            local[sensor_num] = sensor_val
            auto[sensor_num] = 1
        else:
            if local[sensor_num] == '0' and sensor_val == '1':
                auto[sensor_num] += 1

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
        time.sleep(30)

        """
        Decommentare se si vogliono vedere i valori dei duei dict mantenuti dal nodo fog

        print(local, file=sys.stderr)
        print(other, file=sys.stderr)

        """

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
        r = requests.post("http://" + "fog3" + ":" + str(8080) + "/merge",
                          data=data)
        print(r, file=sys.stderr)


def stats_thread():
    while True:

        time.sleep(60)  # Aggiornamento ogni ora

        r = requests.post("http://" + server_ip + ":" + str(server_port) + "/fog_info", data=json.dumps(auto))
        print(r, file=sys.stderr)

        auto.clear()


if __name__ == '__main__':
    st = threading.Thread(target=stats_thread)
    t = threading.Thread(target=sending_thread)

    st.start()
    t.start()

    app.run(host='0.0.0.0', debug=True, port='8080')
