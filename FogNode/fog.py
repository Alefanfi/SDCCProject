import json
import socket
import sys
import threading
import time
import requests

from flask import Flask, request, jsonify
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

local = dict()  # Dizionario con i sensori locali
total = dict()  # Dizionario dei sensori afferenti ad altri nodi fog

auto = dict()  # Numero di volte in cui quel parcheggio è stato preso nell'ultima ora
stats = dict()  # Dizionario con le statistiche dell'ultima settimana

server_ip = "3.232.43.204"
server_port = 5000

my_ip = socket.gethostbyname(socket.gethostname())


@app.route('/', methods=["GET"])
def use_me():
    return jsonify({'name': my_ip})


@app.route('/all', methods=["GET"])
def get_all():
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

        total.update(local)

        return {'DONE': "OK"}

    except Exception as e:

        return {'Exception': e.args}


"""
@app.route('/merge', methods=["POST"])
def merge():
    try:
        sens = json.loads(request.data)

        for key, value in sens.items():
            if key not in total:
                total[key] = value
            else:
                total.update({key: value})

        return {'DONE': "OK"}

    except Exception as e:

        app.logger.error(e.args)

        return {'Exception': e.args}
"""


def sending_thread():

    fog_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    fog_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # Enable broadcasting mode
    fog_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    fog_server.settimeout(0.2)

    while True:
        time.sleep(10)

        if len(local) > 0:

            old_local = local.copy()
            local.clear()

            print(old_local, file=sys.stderr)
            message = json.dumps(old_local).encode('utf-8')
            fog_server.sendto(message, ('<broadcast>', 8081))

            old_local.clear()

        """
        Decommentare se si vogliono vedere i valori dei duei dict mantenuti dal nodo fog

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
        r = requests.post("http://" + "fog3" + ":" + str(8080) + "/merge",
                          data=data)
        print(r, file=sys.stderr)
        """


def listen_for_updates():

    fog_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    fog_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # Enable broadcasting mode
    fog_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    fog_client.bind(("", 8081))
    while True:
        # Thanks @seym45 for a fix
        data, addr = fog_client.recvfrom(2000)
        print("received message: %s" % data, file=sys.stderr)

        sens = json.loads(data.decode('utf-8'))

        for key, value in sens.items():
            if key not in total:
                total[key] = value
            else:
                total.update({key: value})


def stats_thread():
    while True:
        time.sleep(60)  # Aggiornamento ogni ora

        r = requests.post("http://" + server_ip + ":" + str(server_port) + "/fog_info", data=json.dumps(auto))
        print(r, file=sys.stderr)

        auto.clear()


if __name__ == '__main__':

    st = threading.Thread(target=stats_thread)
    st.daemon = True
    t = threading.Thread(target=sending_thread)
    t.daemon = True
    t1 = threading.Thread(target=listen_for_updates)
    t1.daemon = True

    st.start()
    t.start()
    t1.start()

    app.run(host='0.0.0.0', debug=True, port='8080')
