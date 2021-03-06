import json
import random
import sys
import time
import requests

from threading import Thread


proxy_ip = ""
proxy_port = 0


def readJSON():

    global proxy_ip
    global proxy_port
    with open('config.json') as config_file:
        data = json.load(config_file)

        proxy_ip = data['proxy_ip']
        proxy_port = data['proxy_port']

        config_file.close()


class Sensor(Thread):
    def __init__(self, num, server_ip, port):
        Thread.__init__(self)
        self.server_ip = server_ip
        self.port = port
        self.num = num                  # Sensors number
        self.vacant = 0                 # Initially the parking spot is vacant

    def run(self):

        print("-- Starting sensor number " + str(self.num) + " --")

        while True:
            n = random.random()

            if n < 0.5:
                self.vacant = 1
            else:
                self.vacant = 0

            try:
                r = requests.post("http://" + self.server_ip + ":" + str(self.port) + "/update?hash=" + str(self.num),
                                  data={'num': self.num, 'val': self.vacant})
            except requests.ConnectionError as e:
                print(e.args, file=sys.stderr)  # Displays the error

            time.sleep(5)


if __name__ == "__main__":

    # Loading configuration
    readJSON()

    # Creating sensors
    for i in range(1, 33):
        s = Sensor(i, proxy_ip, proxy_port)
        s.start()
