import csv
import subprocess
import threading
import time
import requests

proxy_ip = "findfognode"
proxy_port = 5000
hash_num = 1234


# Creates a new csv file with the results of the test, num specifies the number of repetitions
def createTestFile(file_name, test_url, num):
    row = dict()
    fieldnames = ['id', 'result', 'time']

    file = open(file_name, 'w', newline='')
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(0, num):

        start = time.time()
        r = requests.get(test_url)
        end = time.time()

        row.update({'id': i, 'time': end - start})

        if r.status_code != 200:
            row.update({'result': 'fail'})
        else:
            row.update({'result': 'ok'})

        writer.writerow(row)
        row.clear()


# Starts the fog nodes and the proxy
def startFog(nodes):
    subprocess.Popen(['sh', 'startFog.sh', str(nodes)],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     universal_newlines=True).communicate()


# Stops all the containers and removes them
def stopFog():
    subprocess.Popen(['sh', 'stopFog.sh'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT,
                     universal_newlines=True).communicate()


# Launches the tests for a specific function func
def runTest(num_fog, num, func):

    print("Testing function " + func + " on " + str(num_fog) + " fog nodes\n")

    # Creating the fog nodes and the proxy server
    t = threading.Thread(target=startFog, args=(num_fog,))
    t.daemon = True
    t.start()

    time.sleep(5)  # Sleep for a few seconds to give to docker-compose

    url = "http://" + proxy_ip + ":" + str(proxy_port) + "/" + func + "?hash=" + str(hash_num)
    name = func + "_fog_" + str(num_fog) + ".csv"

    createTestFile(name, url, num)

    stopFog()   # Stops the fog nodes


if __name__ == "__main__":
    repetitions = 100

    print("---------- Test client ----------\n\n")

    for i in range(1, 6):
        runTest(i, repetitions, "all")
        runTest(i, repetitions, "stats")

    print("END")

