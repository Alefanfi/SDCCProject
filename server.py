import json

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


"""def create_server():
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port='5000')
