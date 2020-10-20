import json
import threading
import time
from datetime import datetime

import mysql.connector as mysql
from flask import Flask, request, jsonify
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

stats = dict()  # Dizionario con le statistiche dell'ultima settimana
fog = dict()  # Dizionario con i valori dell'ultima ora dei nodi fog


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


@app.route('/get_stat', methods=["GET"])
def send_stats():
    return jsonify(stats)


def create_stats():

    while True:

        time.sleep(60)

        insert_value(db)

        print(fog)

        # Da fare ancora tutte le statistiche :)


def createDB():

    config_file = open("config.json", "r")
    json_object = json.load(config_file)
    config_file.close()

    db = mysql.connect(
        host=json_object['host'],
        user=json_object['user'],
        passwd=json_object['passwd'],
    )

    mycursor = db.cursor()

    mycursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
    mycursor.execute("USE mydatabase")
    mycursor.execute("CREATE TABLE IF NOT EXISTS sensors (sensor VARCHAR(255), state VARCHAR(255), date DATE)")

    return db


def insert_value(db):

    mycursor = db.cursor()

    sql = "INSERT INTO sensors (sensor, state, date) VALUES (%s, %s, datetime.now())"
    for k in fog:
        val = (k.key, k.value, datetime.now())
        mycursor.execute(sql, val)

    db.commit()

    print(mycursor.rowcount, "record inserted.")


if __name__ == "__main__":

    t = threading.Thread(target=create_stats)
    t.start()
    db = createDB()

    app.run(host='0.0.0.0', debug=True, port='5000')


"""

    def create_server():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (socket.gethostbyname(socket.gethostname()), 10000)
    print('starting up on ' + str(server_address), sys.stderr)
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)

    while True:
        # Wait for a connection
        print('waiting for a connection', sys.stderr)
        connection, client_address = sock.accept()

        try:
            print('connection from ' + str(client_address), sys.stderr)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(16)
                print('received ' + str(data), sys.stderr)
                if data:
                    print('sending data back to the client', sys.stderr)
                    connection.sendall(data)
                else:
                    print('no more data from' + str(client_address), sys.stderr)
                    break

        finally:
            # Clean up the connection
            connection.close()

"""