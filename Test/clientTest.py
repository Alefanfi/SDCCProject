import csv
import time
import requests


def createTestFile(func, ip, port, tag, num):
    row = dict()
    fieldnames = ['id', 'result', 'time']

    file_name = func + ".csv"
    file = open(file_name, 'w', newline='')
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for i in range(0, num):
        url = "http://" + ip + ":" + str(port) + "/" + func + "?hash=" + str(tag)

        start = time.time()
        r = requests.get(url)
        end = time.time()

        row.update({'id': i, 'time': end - start})

        if r.status_code != 200:
            row.update({'result': 'fail'})
        else:
            row.update({'result': 'ok'})

        writer.writerow(row)
        row.clear()


if __name__ == "__main__":
    proxy_ip = "findfognode"
    proxy_port = 5000
    hash_num = 1234
    repetitions = 100

    print("---------- Test client ----------\n\n")

    print("-> Testing showParking function ...\n")
    createTestFile("all", proxy_ip, proxy_port, hash_num, repetitions)

    print("-> Testing getStats function ...\n")
    createTestFile("stats", proxy_ip, proxy_port, hash_num, repetitions)

    print("END")
