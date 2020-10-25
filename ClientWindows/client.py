import json
import threading
import time
import random
import requests
import sys, pyqtgraph, ctypes
from PyQt5 import QtGui, QtCore, QtWidgets, uic, QtSerialPort  # , QtSql
from PyQt5.QtCore import Qt, QTimer, QCoreApplication, QIODevice, QStringListModel, QSize, QPoint
from flask import request
import matplotlib.pyplot as plt

proxy_ip = "findfognode"
proxy_port = 5000

qtCreatorFile = "gui/parcheggio_gui.ui"  # Enter file
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

parcheggio_vuoto = ("QLineEdit {\n"
                    "    border: 2px solid gray;\n"
                    "    border-radius: 10px;\n"
                    "    padding: 0 8px;\n"
                    "    background-color: #33ff66;\n"
                    "}")

parcheggio_occupato = ("QLineEdit {\n"
                       "    border: 2px solid red;\n"
                       "    border-radius: 10px;\n"
                       "    padding: 0 8px;\n"
                       "    background: #cf4245;\n"
                       "}")

"""
parcheggio_prenotato = ("QLineEdit {\n"
                        "    border: 2px solid gray;\n"
                        "    border-radius: 10px;\n"
                        "    padding: 0 8px;\n"
                        "    background: #ffcd12;\n"
                        "}")
"""


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    '''GUI principale'''

    def __init__(self, rnum):

        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)

        self.rnum = rnum
        self.setupUi(self)

        self.setWindowModality(Qt.NonModal)
        self.setAttribute(Qt.WA_PendingResizeEvent)
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self.setAttribute(Qt.WA_Resized)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowState(self.windowState() | Qt.WindowActive)
        self.activateWindow()

        self.setFixedSize(self.width(), self.height())

        self.label_7.mouseDoubleClickEvent = self.getStats

    def setOccupied(self, sensors):

        if sensors.get('1', '0') == '1':
            self.p1.setStyleSheet(parcheggio_occupato)
        else:
            self.p1.setStyleSheet(parcheggio_vuoto)
        if sensors.get('2', '0') == '1':
            self.p2.setStyleSheet(parcheggio_occupato)
        else:
            self.p2.setStyleSheet(parcheggio_vuoto)
        if sensors.get('3', '0') == '1':
            self.p3.setStyleSheet(parcheggio_occupato)
        else:
            self.p3.setStyleSheet(parcheggio_vuoto)
        if sensors.get('4', '0') == '1':
            self.p4.setStyleSheet(parcheggio_occupato)
        else:
            self.p4.setStyleSheet(parcheggio_vuoto)
        if sensors.get('5', '0') == '1':
            self.p5.setStyleSheet(parcheggio_occupato)
        else:
            self.p5.setStyleSheet(parcheggio_vuoto)
        if sensors.get('6', '0') == '1':
            self.p6.setStyleSheet(parcheggio_occupato)
        else:
            self.p6.setStyleSheet(parcheggio_vuoto)
        if sensors.get('7', '0') == '1':
            self.p7.setStyleSheet(parcheggio_occupato)
        else:
            self.p7.setStyleSheet(parcheggio_vuoto)
        if sensors.get('8', '0') == '1':
            self.p8.setStyleSheet(parcheggio_occupato)
        else:
            self.p8.setStyleSheet(parcheggio_vuoto)
        if sensors.get('9', '0') == '1':
            self.p9.setStyleSheet(parcheggio_occupato)
        else:
            self.p9.setStyleSheet(parcheggio_vuoto)
        if sensors.get('10', '0') == '1':
            self.p10.setStyleSheet(parcheggio_occupato)
        else:
            self.p10.setStyleSheet(parcheggio_vuoto)
        if sensors.get('11', '0') == '1':
            self.p11.setStyleSheet(parcheggio_occupato)
        else:
            self.p11.setStyleSheet(parcheggio_vuoto)
        if sensors.get('12', '0') == '1':
            self.p12.setStyleSheet(parcheggio_occupato)
        else:
            self.p12.setStyleSheet(parcheggio_vuoto)
        if sensors.get('13', '0') == '1':
            self.p13.setStyleSheet(parcheggio_occupato)
        else:
            self.p13.setStyleSheet(parcheggio_vuoto)
        if sensors.get('14', '0') == '1':
            self.p14.setStyleSheet(parcheggio_occupato)
        else:
            self.p14.setStyleSheet(parcheggio_vuoto)
        if sensors.get('15', '0') == '1':
            self.p15.setStyleSheet(parcheggio_occupato)
        else:
            self.p15.setStyleSheet(parcheggio_vuoto)
        if sensors.get('16', '0') == '1':
            self.p16.setStyleSheet(parcheggio_occupato)
        else:
            self.p16.setStyleSheet(parcheggio_vuoto)
        if sensors.get('17', '0') == '1':
            self.p17.setStyleSheet(parcheggio_occupato)
        else:
            self.p17.setStyleSheet(parcheggio_vuoto)
        if sensors.get('18', '0') == '1':
            self.p18.setStyleSheet(parcheggio_occupato)
        else:
            self.p18.setStyleSheet(parcheggio_vuoto)
        if sensors.get('19', '0') == '1':
            self.p19.setStyleSheet(parcheggio_occupato)
        else:
            self.p19.setStyleSheet(parcheggio_vuoto)
        if sensors.get('20', '0') == '1':
            self.p20.setStyleSheet(parcheggio_occupato)
        else:
            self.p20.setStyleSheet(parcheggio_vuoto)
        if sensors.get('21', '0') == '1':
            self.p21.setStyleSheet(parcheggio_occupato)
        else:
            self.p21.setStyleSheet(parcheggio_vuoto)
        if sensors.get('22', '0') == '1':
            self.p22.setStyleSheet(parcheggio_occupato)
        else:
            self.p22.setStyleSheet(parcheggio_vuoto)
        if sensors.get('23', '0') == '1':
            self.p23.setStyleSheet(parcheggio_occupato)
        else:
            self.p23.setStyleSheet(parcheggio_vuoto)
        if sensors.get('24', '0') == '1':
            self.p24.setStyleSheet(parcheggio_occupato)
        else:
            self.p24.setStyleSheet(parcheggio_vuoto)
        if sensors.get('25', '0') == '1':
            self.p25.setStyleSheet(parcheggio_occupato)
        else:
            self.p25.setStyleSheet(parcheggio_vuoto)
        if sensors.get('26', '0') == '1':
            self.p26.setStyleSheet(parcheggio_occupato)
        else:
            self.p26.setStyleSheet(parcheggio_vuoto)
        if sensors.get('27', '0') == '1':
            self.p27.setStyleSheet(parcheggio_occupato)
        else:
            self.p27.setStyleSheet(parcheggio_vuoto)
        if sensors.get('28', '0') == '1':
            self.p28.setStyleSheet(parcheggio_occupato)
        else:
            self.p28.setStyleSheet(parcheggio_vuoto)
        if sensors.get('29', '0') == '1':
            self.p29.setStyleSheet(parcheggio_occupato)
        else:
            self.p29.setStyleSheet(parcheggio_vuoto)
        if sensors.get('30', '0') == '1':
            self.p30.setStyleSheet(parcheggio_occupato)
        else:
            self.p30.setStyleSheet(parcheggio_vuoto)
        if sensors.get('31', '0') == '1':
            self.p31.setStyleSheet(parcheggio_occupato)
        else:
            self.p31.setStyleSheet(parcheggio_vuoto)
        if sensors.get('32', '0') == '1':
            self.p32.setStyleSheet(parcheggio_occupato)
        else:
            self.p32.setStyleSheet(parcheggio_vuoto)

    def getStats(self, e):

        url = "http://" + proxy_ip + ":" + str(proxy_port) + "/stats?hash=" + str(self.rnum)
        r = requests.get(url)
        testoAnalisi = r.text

        appo = testoAnalisi.replace("}", "")
        appo = appo.replace("{", "")
        appo = appo.replace('"', "")
        appo = appo.replace("'", "")
        appo = appo.replace(",", "")
        appo = appo.replace(" ", "")
        appo_split_n = appo.split("\\n")
        orario = []
        numeroPosti = []
        new_numeroPosti = []
        for i in range(len(appo_split_n)):
            appo_split_analisi = appo_split_n[i].split(":")
            if len(appo_split_analisi) > 1:
                orario.append(int(appo_split_analisi[0]))
                numeroPosti.append(appo_split_analisi[1])
        orario_sorted = sorted(orario)
        new_orario = []
        for k in range(len(orario_sorted)):
            indice_cercare = orario_sorted[k]
            indice = orario.index(indice_cercare)
            new_numeroPosti.append(numeroPosti[indice])
            if len(str(indice_cercare)) == 1:
                ora = "{0}{1}:00".format("0", str(indice_cercare))
            else:
                ora = "{0}:00".format(str(indice_cercare))
            new_orario.append(ora)
        plt.figure(figsize=(15, 8))
        plt.plot(orario, numeroPosti)
        plt.xticks(orario)

        plt.show()


def show_parking(window):
    while True:
        url = "http://" + proxy_ip + ":" + str(proxy_port) + "/all?hash="+str(window.rnum)
        r = requests.get(url)
        print(r.text)

        data = json.loads(r.text)
        window.setOccupied(data)

        time.sleep(5)


if __name__ == "__main__":

    seedValue = random.randrange(sys.maxsize)
    random.seed(seedValue)
    num = random.randint(2000, 3000)

    ctypes.windll.shcore.SetProcessDpiAwareness()
    appo = QtGui.QApplication.instance()

    if appo is None:
        application = QtWidgets.QApplication(sys.argv)
        win = MyApp(num)

        t = threading.Thread(target=show_parking, args=(win,))
        t.daemon = True
        t.start()

        try:
            win.show()
            sys.exit(application.exec_())

        except Exception as eccezione:
            pass
