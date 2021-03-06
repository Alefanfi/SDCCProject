import ctypes
import json
import platform
import random
import sys
import threading
import time
import matplotlib.pyplot as plt

import requests
from PyQt5 import QtGui, QtWidgets, uic  # , QtSql
from PyQt5.QtCore import Qt, QCoreApplication

proxy_ip = ""
proxy_port = 0

qtCreatorFile = "gui/parcheggio_gui.ui"  # Enter file
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


def readJSON():
    global proxy_ip
    global proxy_port
    with open('config.json') as config_file:
        data = json.load(config_file)

        proxy_ip = data['proxy_ip']
        proxy_port = data['proxy_port']

        config_file.close()


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

        self.label_7.show()
        self.label_7.mouseDoubleClickEvent = self.getStats

    def getStats(self, e):

        url = "http://" + proxy_ip + ":" + str(proxy_port) + "/stats?hash=" + str(self.rnum)

        try:
            r = requests.get(url)
            testoAnalisi = r.text
            print(r.text)
            appo = testoAnalisi.replace("}", "")
            appo = appo.replace("{", "")
            appo = appo.replace('"', "")
            appo = appo.replace("'", "")
            appo = appo.replace(",", "")
            appo = appo.replace(" ", "")
            appo_split_n = appo.split("\n")
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
            print(new_numeroPosti)
            print(new_orario)

            plt.figure(figsize=(15, 8))
            plt.plot(new_orario, new_numeroPosti)
            plt.xticks(new_orario)

            plt.show()

        except requests.ConnectionError as e:
            print(e.args, file=sys.stderr)  # Displays the error

    def setOccupied(self, sensors):

        empty = ("QLineEdit {"
                 "border: 2px solid gray;"
                 "border-radius: 10px;"
                 "padding: 0 8px;"
                 "background-color: #33ff66;"
                 "}")

        taken = ("QLineEdit {"
                 "border: 2px solid red;"
                 "border-radius: 10px;"
                 "padding: 0 8px;"
                 "background: #cf4245;"
                 "}")

        if sensors.get('1', '0') == '1':
            self.p1.setStyleSheet(taken)
        else:
            self.p1.setStyleSheet(empty)
        if sensors.get('2', '0') == '1':
            self.p2.setStyleSheet(taken)
        else:
            self.p2.setStyleSheet(empty)
        if sensors.get('3', '0') == '1':
            self.p3.setStyleSheet(taken)
        else:
            self.p3.setStyleSheet(empty)
        if sensors.get('4', '0') == '1':
            self.p4.setStyleSheet(taken)
        else:
            self.p4.setStyleSheet(empty)
        if sensors.get('5', '0') == '1':
            self.p5.setStyleSheet(taken)
        else:
            self.p5.setStyleSheet(empty)
        if sensors.get('6', '0') == '1':
            self.p6.setStyleSheet(taken)
        else:
            self.p6.setStyleSheet(empty)
        if sensors.get('7', '0') == '1':
            self.p7.setStyleSheet(taken)
        else:
            self.p7.setStyleSheet(empty)
        if sensors.get('8', '0') == '1':
            self.p8.setStyleSheet(taken)
        else:
            self.p8.setStyleSheet(empty)
        if sensors.get('9', '0') == '1':
            self.p9.setStyleSheet(taken)
        else:
            self.p9.setStyleSheet(empty)
        if sensors.get('10', '0') == '1':
            self.p10.setStyleSheet(taken)
        else:
            self.p10.setStyleSheet(empty)
        if sensors.get('11', '0') == '1':
            self.p11.setStyleSheet(taken)
        else:
            self.p11.setStyleSheet(empty)
        if sensors.get('12', '0') == '1':
            self.p12.setStyleSheet(taken)
        else:
            self.p12.setStyleSheet(empty)
        if sensors.get('13', '0') == '1':
            self.p13.setStyleSheet(taken)
        else:
            self.p13.setStyleSheet(empty)
        if sensors.get('14', '0') == '1':
            self.p14.setStyleSheet(taken)
        else:
            self.p14.setStyleSheet(empty)
        if sensors.get('15', '0') == '1':
            self.p15.setStyleSheet(taken)
        else:
            self.p15.setStyleSheet(empty)
        if sensors.get('16', '0') == '1':
            self.p16.setStyleSheet(taken)
        else:
            self.p16.setStyleSheet(empty)
        if sensors.get('17', '0') == '1':
            self.p17.setStyleSheet(taken)
        else:
            self.p17.setStyleSheet(empty)
        if sensors.get('18', '0') == '1':
            self.p18.setStyleSheet(taken)
        else:
            self.p18.setStyleSheet(empty)
        if sensors.get('19', '0') == '1':
            self.p19.setStyleSheet(taken)
        else:
            self.p19.setStyleSheet(empty)
        if sensors.get('20', '0') == '1':
            self.p20.setStyleSheet(taken)
        else:
            self.p20.setStyleSheet(empty)
        if sensors.get('21', '0') == '1':
            self.p21.setStyleSheet(taken)
        else:
            self.p21.setStyleSheet(empty)
        if sensors.get('22', '0') == '1':
            self.p22.setStyleSheet(taken)
        else:
            self.p22.setStyleSheet(empty)
        if sensors.get('23', '0') == '1':
            self.p23.setStyleSheet(taken)
        else:
            self.p23.setStyleSheet(empty)
        if sensors.get('24', '0') == '1':
            self.p24.setStyleSheet(taken)
        else:
            self.p24.setStyleSheet(empty)
        if sensors.get('25', '0') == '1':
            self.p25.setStyleSheet(taken)
        else:
            self.p25.setStyleSheet(empty)
        if sensors.get('26', '0') == '1':
            self.p26.setStyleSheet(taken)
        else:
            self.p26.setStyleSheet(empty)
        if sensors.get('27', '0') == '1':
            self.p27.setStyleSheet(taken)
        else:
            self.p27.setStyleSheet(empty)
        if sensors.get('28', '0') == '1':
            self.p28.setStyleSheet(taken)
        else:
            self.p28.setStyleSheet(empty)
        if sensors.get('29', '0') == '1':
            self.p29.setStyleSheet(taken)
        else:
            self.p29.setStyleSheet(empty)
        if sensors.get('30', '0') == '1':
            self.p30.setStyleSheet(taken)
        else:
            self.p30.setStyleSheet(empty)
        if sensors.get('31', '0') == '1':
            self.p31.setStyleSheet(taken)
        else:
            self.p31.setStyleSheet(empty)
        if sensors.get('32', '0') == '1':
            self.p32.setStyleSheet(taken)
        else:
            self.p32.setStyleSheet(empty)
        QCoreApplication.processEvents()


def show_parking(window):
    while True:
        url = "http://" + proxy_ip + ":" + str(proxy_port) + "/all?hash=" + str(window.rnum)
        try:
            r = requests.get(url)

            data = json.loads(r.text)
            window.setOccupied(data)

        except requests.ConnectionError as e:
            print(e.args, file=sys.stderr)  # Displays the error

        time.sleep(5)


if __name__ == "__main__":

    readJSON()

    seedValue = random.randrange(sys.maxsize)
    random.seed(seedValue)
    num = random.randint(2000, 3000)

    ctypes.CDLL("libc.{}".format("so.6" if platform.uname()[0] != "Darwin" else "dylib"))
    appo = QtWidgets.QApplication.instance()

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
