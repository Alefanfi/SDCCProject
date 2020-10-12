"""import socket
import sys"""
import time

import requests


def create_client(server_ip, port):

    while True:
        url = "http://" + server_ip + ":" + str(port) + "/all"
        r = requests.get(url)
        print(r.text)

        time.sleep(10)

"""
    # Create a TCP/IP socket
    sock = socket.create_connection(('54.159.110.76', 10000))

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print('connecting to' + str(server_address), sys.stderr)

    try:

        # Send data
        message = 'This is the message.  It will be repeated.'
        print('sending: ' + message, sys.stderr)
        sock.sendall(message.encode())

        # Look for the response
        amount_received = 0
        amount_expected = len(message)

        while amount_received < amount_expected:
            data = sock.recv(16).decode()
            amount_received += len(data)
            print('received: ' + str(data), sys.stderr)

    finally:
        print('closing socket', sys.stderr)
        sock.close()
"""

if __name__ == "__main__":
    create_client("localhost", 8080)
