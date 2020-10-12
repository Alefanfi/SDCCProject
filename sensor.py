import random
import time

from threading import Thread

import requests


class Sensor(Thread):
    def __init__(self, num, server_ip, port):
        Thread.__init__(self)
        self.server_ip = server_ip  # ip del server
        self.port = port  # porta a cui collegarsi
        self.num = num  # numero del sensore
        self.vacant = 0  # posto auto inizialmente considerato libero

    def run(self):
        while True:
            n = random.random()

            if n < 0.5:
                self.vacant = 1
            else:
                self.vacant = 0

            print("Sensor" + str(self.num) + " - " + str(self.vacant))
            # Logica per inviarlo al server
            r = requests.post("http://" + self.server_ip + ":" + str(self.port) + "/update",
                              data={'num': self.num, 'val': self.vacant})
            # And done.
            print(r.text)  # displays the result body.

            time.sleep(5)


if __name__ == "__main__":

    # creaiamo un insieme di sensori che inviino i dati al server
    for i in range(6):
        s = Sensor(i, "localhost", 8081)
        s.start()
