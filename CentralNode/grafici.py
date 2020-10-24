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


def create_plot_24h(times, ay):
    new_times = []
    new_ay = []
    times_sorted = sorted(times)
    for m in range(len(times_sorted)):
        indice_cercare = times_sorted[m]
        indice = times.index(indice_cercare)
        new_ay.append(ay[indice])
        new_times.append(str(indice_cercare))

    plt.figure(figsize=(11.69, 8.27))

    plt.plot(new_times, new_ay)
    plt.xticks(new_times)
    plt.savefig('grafico.pdf')
    shutil.move('grafico.pdf', FOLDER_NAME)
    # plt.show()

    """plt.title('Posti occupati nelle ultime 24 ore')
    plt.xlabel('Orario')
    plt.ylabel('Num posti occupati')"""


def write_pdf(ax, ay):

    filename = 'statistiche.pdf'

    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_xy(0, 0)
    pdf.set_font('arial', 'B', 13.0)

    pdf.cell(ln=0, h=5.0, align='L', w=0, txt='', border=0)

    for k in range(0, len(ax), 1):
        pdf.cell(ln=k, h=5.0, align='L', w=0, txt='alle '+str(ax[k])+' il numero di posti occupati è '+str(ay[k]), border=0)

    pdf.output(filename, 'F')
    shutil.move(filename, FOLDER_NAME)


def merge_pdfs():
    readJSON()
    files=['files3/grafico.pdf', 'files3/statistiche.pdf']
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
