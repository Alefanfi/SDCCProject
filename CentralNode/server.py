import json
import threading
import time

from flask import Flask, request, jsonify
from flask_restful import Api
from CentralNode.dao import Dao
from CentralNode import grafici

app = Flask(__name__)
api = Api(app)

stats = dict()      # Statistics on the last 24 hours
fog = dict()        # How many times each parking spot was used in the last hour


# Updates values taken from fog nodes in the dictionary fog
@app.route('/fog_info', methods=["POST"])
def set_fog_info():
    try:

        sens = json.loads(request.data)

        for key, value in sens.items():
            fog.update({key: value})

        return json.dumps({'Done': "OK"}), 200, {'ContentType': 'application/json'}

    except Exception as e:

        return json.dumps({'Exception': e.args}), 500, {'ContentType': 'application/json'}


# Returns the statistics of the last 24 hours
@app.route('/get_stat', methods=["GET"])
def send_stats():
    return jsonify(stats), 200


# Thread which periodically creates the new stats values
def create_stats():

    # Loading database configuration
    config_file = open("config.json", "r")
    json_object = json.load(config_file)
    config_file.close()

    host = json_object['host']
    user = json_object['user']
    passwd = json_object['passwd']
    db = json_object['database']

    dao = Dao(host, user, passwd, db, "sensors")

    while True:
        time.sleep(60*60)  # Update every hour

        if not bool(fog):
            pass
        else:
            print(fog)
            dao.insertValue(fog)  # Inserts values into the database
            stats.update(dao.getLast24h())  # Updates the statistics

            """Costruisce gli array di valori che verranno ad essere utilizzati per la realizzazione dei grafici e 
            delle statistiche """
            ax = []
            ay = []
            for x in stats:
                ax.append(x)
                ay.append((stats[x]))
            grafici.createPlot24h(ax, ay)
            grafici.createPlot24h(ax, ay)
            grafici.mergePdfs()


if __name__ == "__main__":
    t = threading.Thread(target=create_stats)
    t.daemon = True
    t.start()

    app.run(host='0.0.0.0', debug=True, port='5000')
