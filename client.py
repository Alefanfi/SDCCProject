import sys
import requests


def sensor_info(server_ip, server_port):

    url = "http://" + server_ip + ":" + str(server_port) + "/all"
    r = requests.get(url)
    print(r.text)


def stats_info(server_ip, server_port):

    url = "http://" + server_ip + ":" + str(server_port) + "/stats"
    r = requests.get(url)
    print(r.text)


if __name__ == "__main__":

    host = "localhost"
    port = 8080

    print("---- WELCOME ----\n\n"
          "park - Shows in the parking lot which places are taken\n"
          "stats - Shows the statistics on the last week\n"
          "quit - Quit")

    while True:
        text = input("--> ")

        if text == "park":
            sensor_info(host, port)

        elif text == "stats":
            stats_info(host, port)

        elif text == "quit":
            sys.exit()
