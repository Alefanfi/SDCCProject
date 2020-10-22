import json
import threading
import time

from flask import Flask, request, jsonify
from flask_restful import Api
from CentralNode.dao import Dao

from CentralNode import grafici

app = Flask(__name__)
api = Api(app)

stats = dict()  # Dizionario con le statistiche delle ultime 24h
fog = dict()  # Dizionario con i valori dell'ultima ora dei nodi fog


# Aggiorna i valori raccolti dai sensori nel dizionario fog
@app.route('/fog_info', methods=["POST"])
def set_fog_info():
    try:

        sens = json.loads(request.data)

        for key, value in sens.items():
            if key not in fog:
                fog[key] = value
            else:
                fog.update({key: value})

        return {'DONE': "OK"}

    except Exception as e:

        app.logger.error(e.args)

        return {'Exception': e.args}


# Ritorna le statistiche contenute nel dizionario stats
@app.route('/get_stat', methods=["GET"])
def send_stats():
    return jsonify(stats)


# Thread function che si occupa della creazione delle statistiche
def create_stats():

    # Creazione del database
    config_file = open("config.json", "r")
    json_object = json.load(config_file)
    config_file.close()

    host = json_object['host']
    user = json_object['user']
    passwd = json_object['passwd']
    db = json_object['database']

    dao = Dao(host, user, passwd, db, "sensors")

    while True:
        time.sleep(60)  # Ogni ora

        print(fog)
        dao.insert_value(fog)  # Inserisce nel database i valori raccolti
        stats.update(dao.get_last_24h())  # Recupera dal database le statistiche aggiornate sulle ultime 24h

        ax = []
        ay = []
        for x in stats:
            ax.append(x)
            ay.append((stats[x]))
        grafici.create_plot_24h(ax, ay)
        grafici.create_plot_24h(ax, ay)
        grafici.merge_pdfs()


if __name__ == "__main__":
    t = threading.Thread(target=create_stats)
    t.daemon = True
    t.start()

    app.run(host='0.0.0.0', debug=True, port='5000')
