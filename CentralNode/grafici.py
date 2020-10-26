import json
import os
import shutil
from datetime import datetime

import matplotlib.pyplot as plt
from fpdf import FPDF
import PyPDF2

from CentralNode import s3api

FOLDER_NAME = ""
BUCKET_NAME = ""


def readJSON():

    global FOLDER_NAME, BUCKET_NAME
    with open('config.json') as config_file:
        data = json.load(config_file)

        FOLDER_NAME = data['folder_name']
        BUCKET_NAME = data['bucket_name']

        config_file.close()


def createPlot24h(times, ay):
    new_times = []
    new_ay = []
    times_sorted = sorted(times)
    for m in range(len(times_sorted)):
        indice_cercare = times_sorted[m]
        indice = times.index(indice_cercare)
        new_ay.append(ay[indice])
        new_times.append(str(indice_cercare))

    plt.figure(figsize=(11.69, 8.27))
    plt.title('Posti occupati nelle ultime 24 ore')
    plt.xlabel('Ora')
    plt.ylabel('Numero posti occupati')

    plt.plot(new_times, new_ay)
    plt.xticks(new_times)
    plt.savefig('grafico.pdf')
    shutil.move('grafico.pdf', FOLDER_NAME)
    # plt.show()


def writePdf(times, posti):

    filename = 'statistiche.pdf'
    new_times = []
    new_posti = []
    times_sorted = sorted(times)
    for m in range(len(times_sorted)):
        indice_cercare = times_sorted[m]
        indice = times.index(indice_cercare)
        new_posti.append(posti[indice])
        if len(str(indice_cercare)) == 1:
            ora = "{0}{1}:00".format("0", str(indice_cercare))
        else:
            ora = "{0}:00".format(str(indice_cercare))
        new_times.append(ora)

    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('arial', 'B', 12)
    pdf.cell(10)
    pdf.cell(60, 10, 'Ora', 0, 0, 'C')
    pdf.cell(60, 10, 'Numero posti occupati', 0, 1, 'C')

    for k in range(0, len(times)):
        pdf.cell(60, 10, '%s' % (str(new_times[k])), 0, 0, 'C')
        pdf.cell(60, 10, '%s' % (str(new_posti[k])), 0, 1, 'C')

    pdf.output(filename, 'F')
    shutil.move(filename, FOLDER_NAME)


def mergePdfs():
    readJSON()
    files = ['files3/grafico.pdf', 'files3/statistiche.pdf']
    pdf_writer = PyPDF2.PdfFileWriter()

    for path in files:
        pdf_reader = PyPDF2.PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    now = datetime.now()
    str_date = now.strftime("%Y-%m-%d %H:%M:%S")
    output = str_date + '.pdf'
    with open(output, 'wb') as out:
        pdf_writer.write(out)
        out.close()
    s3api.upload_file(output, BUCKET_NAME)
    # shutil.move(output, FOLDER_NAME)
    os.remove(output)

    for k in files:
        os.remove(k)
