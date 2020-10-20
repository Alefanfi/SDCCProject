import json

import mysql.connector as mysql

"""
Questo modulo prepara un file JSON che verrà inviato ad AWS.
I dati inviati sono:

{
    sensor_state: [0,1] che indicano rispettivamente se il parcheggio è libero o occupato
    occupated: il numero delle volte in cui un determinato posto è stato occupato
    sensor_number: numero del sensore
}
"""


def connectdb():

    config_file = open("config.json", "r")
    json_object = json.load(config_file)
    config_file.close()

    db = mysql.connect(
        host=json_object['host'],
        user=json_object['user'],
        passwd=json_object['passwd'],
        database=json_object['database']
    )

    return db


def calculate_value():

    db = connectdb()
    cursor = db.cursor()


