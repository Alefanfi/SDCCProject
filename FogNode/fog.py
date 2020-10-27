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

local = dict()          # Values of local sensors
total = dict()          # Values of all sensors
auto = dict()           # How many times each parking spot was used in the last hour
stats = dict()          # Statistics on the last 24 hours

server_ip = ""
server_port = 0
broadcast_port = 0


# Loads configurations from config.json file
def loadConfig():

    global server_ip
    global server_port
    global broadcast_port

    config_file = open("config.json", "r")
    json_object = json.load(config_file)
    config_file.close()

    server_ip = json_object['ec2_server_ip']
    server_port = json_object['ec2_server_port']
    broadcast_port = json_object['broadcast_port']


# Returns the values of all sensors
@app.route('/all', methods=["GET"])
def get_all():
    return jsonify(total), 200


# Returns the statistics taken from the ec2 server
@app.route('/stats', methods=["GET"])
def get_stats():
    return jsonify(stats), 200


# Updates the value of a sensor both in local and total
@app.route('/update', methods=["POST"])
def update():
    try:

        sensor_num = request.form['num']
        sensor_val = request.form['val']

        if sensor_num not in local:
            auto[sensor_num] = 1
        else:
            # If a new car has taken the parking spot it updates the dictionary auto
            if local[sensor_num] == '0' and sensor_val == '1':
                auto[sensor_num] += 1

        local.update({sensor_num: sensor_val})
        total.update({sensor_num: sensor_val})

        return json.dumps({'Done': "OK"}), 200, {'ContentType': 'application/json'}

    except Exception as e:

        return json.dumps({'Exception': e.args}), 500, {'ContentType': 'application/json'}


# Thread which sends periodically the updated values of the sensors to the other fog nodes
def sendingThread():

    fog_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    fog_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # Enable broadcasting mode
    fog_server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    fog_server.settimeout(0.2)

    while True:
        time.sleep(10)

        old_local = local.copy()
        local.clear()

        # Checks if the dictionary has updates
        if len(old_local) > 0:

            message = json.dumps(old_local).encode('utf-8')
            fog_server.sendto(message, ('<broadcast>', broadcast_port))

            old_local.clear()


# Thread which listens for updates from other nodes
def listeningThread():

    fog_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    fog_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # Enable broadcasting mode
    fog_client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    fog_client.bind(("", broadcast_port))

    while True:

        data, addr = fog_client.recvfrom(2000)
        sens = json.loads(data.decode('utf-8'))

        for key, value in sens.items():
            total.update({key: value})


# Thread which periodically sends the sensors values to the ec2 server and updates the local stats dictionary
def statsThread():
    while True:
        time.sleep(60*60)  # Update every hour

        r = requests.post("http://" + server_ip + ":" + str(server_port) + "/fog_info", data=json.dumps(auto))
        print(r, file=sys.stderr)

        auto.clear()

        r = requests.get("http://" + server_ip + ":" + str(server_port) + "/get_stat")
        print(r, file=sys.stderr)
        data = json.loads(r.text)

        for key, value in data:
            stats.update({key: value})


if __name__ == '__main__':

    loadConfig()

    st = threading.Thread(target=statsThread)
    st.daemon = True
    t = threading.Thread(target=sendingThread)
    t.daemon = True
    t1 = threading.Thread(target=listeningThread)
    t1.daemon = True

    st.start()
    t.start()
    t1.start()

    app.run(host='0.0.0.0', debug=True, port='8080')
