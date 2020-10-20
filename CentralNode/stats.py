import json
import os
import shutil
from operator import attrgetter
from threading import Thread
import time
import numpy as np
from CentralNode import s3api

BUCKET_NAME = ""
FOLDER_NAME = ""


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

            global BUCKET_NAME, FOLDER_NAME
            with open('config.json') as config_file:
                data = json.load(config_file)

                BUCKET_NAME = data['bucket_name']
                FOLDER_NAME = data['folder_name']

                config_file.close()

            # Lista dei file presenti nel bucket
            list_of_files = s3api.list_objects(BUCKET_NAME)

            for k in list_of_files:
                print("File:", k.key)

            # Prendo l'ultimo file modificato o ne crea uno nuovo nel caso in cui il bucket sia vuoto

            # Creare un nuovo file per le statistiche
            # il file verrà usato o come primo file che verrà poi ad essere inserito in s3 o come file che riporterà
            # le statistiche aggiornate

            pathfile = "Statistiche.txt"

            if os.path.exists(pathfile):
                append_write = 'a'  # append if already exists
            else:
                append_write = 'w'  # make a new file if not

            f = open(pathfile, append_write)
            shutil.move(pathfile, FOLDER_NAME) # lo inserisco nella cartella fileS3
            f.close()

            if not list_of_files:

                print("Il bucket è vuoto")

                # Calcolo statistiche iniziali

            else:

                sorted_list = sorted(list_of_files, key=attrgetter('last_modified'))

                latest = sorted_list.pop()

                print(latest.key)

                # Crea le statistiche aggiornate

            # Put the file to S3
            s3api.upload_file(pathfile, BUCKET_NAME)
            os.remove(pathfile)

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
