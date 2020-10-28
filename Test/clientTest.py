import csv
import json
import subprocess
import sys
import threading
import time
import requests
import random

seedValue = random.randrange(sys.maxsize)
random.seed(seedValue)


# Creates a new csv file with the results of the test, num specifies the number of repetitions
def createTestFile(file_name, test_url, num):
    row = dict()
    fieldnames = ['id', 'result', 'time']

    file = open(file_name, 'w', newline='')
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(0, num):

        start = time.time()
        try:
            r = requests.get(test_url)
        except requests.ConnectionError as e:
            print(e.args, file=sys.stderr)  # Displays the error
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


# Kills random fog node to test fault tolerance
def killFogNode():
    while True:

        time.sleep(2 * 60)

        result = subprocess.Popen(['sh', 'getContainers.sh'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  universal_newlines=True).communicate()

        names = result[0].split("\n")

        if len(names) > 3:
            num = random.randint(1, len(names) - 1)

            subprocess.Popen(['sh', 'killContainer.sh', names[num]],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             universal_newlines=True).communicate()


# Creates a new client
def createClient(ip, port):

    hash_num = random.randint(2000, 3000)
    url = "http://" + ip + ":" + str(port) + "/" + "all?hash=" + str(hash_num)

    while True:

        time.sleep(10)
        
        try:
            r = requests.get(url)
        except requests.ConnectionError as e:
            print(e.args, file=sys.stderr)  # Displays the error


# Launches the tests for a specific function func
def runTest(num_fog, ip, port, num, func, failure):
    print("Testing function " + func + " on " + str(num_fog) + " fog nodes\n")

    # Creating the fog nodes and the proxy server
    t = threading.Thread(target=startFog, args=(num_fog,))
    t.daemon = True
    t.start()

    time.sleep(5)  # Sleep for a few seconds to give to docker-compose

    hash_num = random.randint(2000, 3000)

    url = "http://" + ip + ":" + str(port) + "/" + func + "?hash=" + str(hash_num)

    # Changes the file name based on the type of test
    if failure:
        name = func + "_fog_" + str(num_fog) + "_fail" + ".csv"
    else:
        name = func + "_fog_" + str(num_fog) + "_no_fail" + ".csv"

    createTestFile(name, url, num)

    stopFog()  # Stops the fog nodes


# Test with increasing number of fog nodes
def incFogNodesTest(ip, port, repetitions):
    print("---------- Test client without failures - incFogNodesTest ----------\n\n")

    for i in range(1, 10):
        runTest(i, ip, port, repetitions, "all", 0)
        runTest(i, ip, port, repetitions, "stats", 0)

    print("\n---------- Test client with failures - incFogNodesTest ----------\n\n")

    t = threading.Thread(target=killFogNode)
    t.daemon = True
    t.start()

    for i in range(3, 10):
        runTest(i, ip, port, repetitions, "all", 1)
        runTest(i, ip, port, repetitions, "stats", 1)

    print("\nEND")


# Test with increasing number of clients
def incClientsTest(ip, port, repetitions, failure):
    if failure:

        print("\n---------- Test client with failures - incClientsTest ----------\n\n")

        t = threading.Thread(target=killFogNode)
        t.daemon = True
        t.start()

        for i in range(1, 5):
            tc = threading.Thread(target=createClient, args=(ip, port,))
            tc.daemon = True
            tc.start()

            runTest(5, ip, port, repetitions, "all", "all_client_" + str(i) + "_fail.csv")
            runTest(5, ip, port, repetitions, "stats", "stats_client_" + str(i) + "_fail.csv")

    else:

        print("---------- Test client without failures - incClientsTest ----------\n\n")

        for i in range(1, 5):
            tc = threading.Thread(target=createClient, args=(ip, port,))
            tc.daemon = True
            tc.start()

            runTest(5, ip, port, repetitions, "all", "all_client_" + str(i) + "_nofail.csv")
            runTest(5, ip, port, repetitions, "stats", "stats_client_" + str(i) + "_nofail.csv")

    print("\nEND")


if __name__ == "__main__":
    # Loading configuration from config.json
    config_file = open("config.json", "r")
    json_object = json.load(config_file)
    config_file.close()

    proxy_ip = json_object['proxy_ip']
    proxy_port = json_object['proxy_port']
    repetitions = json_object['repetitions']

    # incFogNodesTest(proxy_ip, proxy_port, repetitions)

    incClientsTest(proxy_ip, proxy_port, repetitions, 0)

    # incClientsTest(proxy_ip, proxy_port, repetitions, 1)
