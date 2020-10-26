import json
import random
import sys
import time
import requests

from threading import Thread


proxy_ip = "findfognode"
proxy_port = 5000


class Sensor(Thread):
    def __init__(self, num, server_ip, port, hashnum):
        Thread.__init__(self)
        self.server_ip = server_ip
        self.port = port
        self.num = num                  # Sensors number
        self.vacant = 0                 # Initially the parking spot is vacant
        self.hashnum = hashnum          # Hash used by the nginx proxy for session persistence

    def run(self):

        print("-- Starting sensor number " + str(self.num) + " --")

        while True:
            n = random.random()

            if n < 0.5:
                self.vacant = 1
            else:
                self.vacant = 0

            """
            Uncomment this to see the values used by the sensors
            
            print("Sensor" + str(self.num) + " - " + str(self.vacant))
            
            """

            r = requests.post("http://" + self.server_ip + ":" + str(self.port) + "/update?hash="+str(self.hashnum),
                              data={'num': self.num, 'val': self.vacant})

            if r.status_code != 200:
                print(r.text, file=sys.stderr)  # Displays the error

            time.sleep(5)


if __name__ == "__main__":

    # Creating sensors
    for i in range(1, 9):
        s = Sensor(i, proxy_ip, proxy_port, 1)
        s.start()

    for i in range(9, 17):
        s = Sensor(i, proxy_ip, proxy_port, 2)
        s.start()

    for i in range(17, 25):
        s = Sensor(i, proxy_ip, proxy_port, 3)
        s.start()

    for i in range(25, 33):
        s = Sensor(i, proxy_ip, proxy_port, 4)
        s.start()
