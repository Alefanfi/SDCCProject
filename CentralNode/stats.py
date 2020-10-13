import glob
import json
import logging
import os

import boto3
from threading import Thread
import time
import numpy as np
from botocore.config import Config

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

AWS_KEY_ID = ""
AWS_SECRET_KEY = ""
BUCKET_NAME = ""
FOLDER_NAME = ""


# Read the .json file to get the config.
def readJson():
    global AWS_KEY_ID, AWS_SECRET_KEY, BUCKET_NAME, FOLDER_NAME
    with open('config.json') as config_file:
        data = json.load(config_file)
        AWS_KEY_ID = data['aws_key_id']
        AWS_SECRET_KEY = data['aws_secret_key']
        BUCKET_NAME = data['bucket_name']
        FOLDER_NAME = data['folder_name']
        config_file.close()


################################################################


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

            s3 = boto3.resource(
                's3',
                aws_access_key_id=AWS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_KEY,
                config=Config(signature_version='s3v4')
            )

            # List all the file in the folder
            list_of_files = glob.glob('dump/*')

            # Get the most recent file (using timestamp)
            latest_file = max(list_of_files, key=os.path.getctime)
            try:
                data = open(latest_file, 'rb')
            except IOError as e:
                logging.warning("Errore nell'apertura del file.")
                exit(-1)

            # Crea le statistiche aggiornate

            # Put the file to S3
            s3.Bucket(BUCKET_NAME).put_object(Key=FOLDER_NAME + '/' + latest_file, Body=data)

            # Dopo l'upload elimino il file per non occupare inutilmente spazio
            # os.remove(latest_file)

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
    readJson()
    stats = Stats()
    thread = StatsThread("ciao", 10)
    thread.start()
