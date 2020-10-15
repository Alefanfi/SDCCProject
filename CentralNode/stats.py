import json

from threading import Thread
import time
import numpy as np

"""
    ROBA UTILE PER FARE LE QUERY IN S3


def get_by_date(bucket_name, file_name):

    resp = s3.select_object_content(
        Bucket='s3select-demo',
        Key='sample_data.csv',
        ExpressionType='SQL',
        Expression="SELECT * FROM s3object s where s.\"Name\" = 'Jane'",
        InputSerialization={'CSV': {"FileHeaderInfo": "Use"}, 'CompressionType': 'NONE'},
        OutputSerialization={'CSV': {}},
    )

    for event in resp['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            print(records)
        elif 'Stats' in event:
            statsDetails = event['Stats']['Details']
            print("Stats details bytesScanned: ")
            print(statsDetails['BytesScanned'])
            print("Stats details bytesProcessed: ")
            print(statsDetails['BytesProcessed'])
            print("Stats details bytesReturned: ")
            print(statsDetails['BytesReturned'])
"""

BUCKET_NAME = ""


class StatsThread(Thread):
    def __init__(self, nome, time):
        Thread.__init__(self)
        self.nome = nome
        self.time = time

    def run(self):
        while True:
            print("Thread '" + self.name + "' avviato")

            time.sleep(self.time)

            # Prendi i file di dati da s3

            global BUCKET_NAME
            with open('config.json') as config_file:
                data = json.load(config_file)

                BUCKET_NAME = data['bucket_name']

                config_file.close()

            # Lista dei file presenti nel bucket
            # list_of_files = s3api.list_object(BUCKET_NAME)

            # Crea le statistiche aggiornate

            # Put the file to S3

            print("Thread '" + self.name + "' terminato")


class Stats:
    def __init__(self):
        self.hours = [0] * 24

    # Indice corrispondente al valore massimo nell'array self.hours
    def peak(self):
        return np.argmax(self.hours)

    # Indice corrispondente al valore minimo nell'array self.hours
    def mininum(self):
        return np.argmin(self.hours)


if __name__ == '__main__':
    stats = Stats()
    thread = StatsThread("ciao", 10)
    thread.start()
