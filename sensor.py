import random
import time

from threading import Thread

import requests


class Sensor(Thread):
    def __init__(self, num, server_ip, port):
        Thread.__init__(self)
        self.server_ip = server_ip  # ip del server
        self.port = port            # porta a cui collegarsi
        self.num = num              # numero del sensore
        self.vacant = 0             # posto auto inizialmente considerato libero

    def run(self):

        print("-- Starting sensor number " + str(self.num) + " --")

        while True:
            n = random.random()

            if n < 0.5:
                self.vacant = 1
            else:
                self.vacant = 0

            # Decommentare se si vuole vedere cosa fa il sensore
            # print("Sensor" + str(self.num) + " - " + str(self.vacant))

            r = requests.post("http://" + self.server_ip + ":" + str(self.port) + "/update",
                              data={'num': self.num, 'val': self.vacant})

            if r.status_code != 200:

                print(r.text)  # displays the error

            time.sleep(5)


if __name__ == "__main__":

    # creaiamo un insieme di sensori che inviino i dati ai diversi nodi fog
    for i in range(1, 9):
        s = Sensor(i, "localhost", 8080)
        s.start()

    for i in range(9, 17):
        s = Sensor(i, "localhost", 8081)
        s.start()

    for i in range(17, 25):
        s = Sensor(i, "localhost", 8082)
        s.start()

    for i in range(25, 33):
        s = Sensor(i, "localhost", 8083)
        s.start()