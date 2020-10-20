import platform
import sys
import ctypes
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt

qtCreatorFile = "parcheggio_gui.ui"  # Enter file
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

parcheggio_prenotato = ("QLineEdit {\n"
                        "    border: 2px solid gray;\n"
                        "    border-radius: 10px;\n"
                        "    padding: 0 8px;\n"
                        "    background: #ffcd12;\n"
                        "}")


def show_parking(sensors):
    """ctypes.windll.shcore.SetProcessDpiAwareness()
    appoo = QtGui.QApplication.instance()"""
    ctypes.CDLL("libc.{}".format("so.6" if platform.uname()[0] != "Darwin" else "dylib"))

    appoo = QtWidgets.QApplication.instance()
    if appoo is None:
        application = QtWidgets.QApplication(sys.argv)
        win = MyApp()
        win.setOccupied(sensors)
        try:
            win.show()
            sys.exit(application.exec_())
        except Exception as eccezione:
            pass


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    '''GUI principale'''

    def __init__(self):

        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.setWindowModality(Qt.NonModal)
        self.setAttribute(Qt.WA_PendingResizeEvent)
        self.setAttribute(Qt.WA_AcceptTouchEvents)
        self.setAttribute(Qt.WA_Resized)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowState(self.windowState() | Qt.WindowActive)
        self.activateWindow()

        self.setFixedSize(self.width(), self.height())

        self.p1.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p2.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p3.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p4.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p5.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p6.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p7.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p8.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p9.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p10.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p11.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p12.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p13.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p14.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p15.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p16.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p17.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p18.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p19.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p20.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p21.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p22.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p23.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p24.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p25.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p26.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p27.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p28.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p29.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p30.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p31.mouseDoubleClickEvent = self.prenotaParcheggio
        self.p32.mouseDoubleClickEvent = self.prenotaParcheggio

    def setOccupied(self, sensors):

        if sensors.get('1', '0') == '1':
            self.p1.setStyleSheet(parcheggio_occupato)
        if sensors.get('2', '0') == '1':
            self.p2.setStyleSheet(parcheggio_occupato)
        if sensors.get('3', '0') == '1':
            self.p3.setStyleSheet(parcheggio_occupato)
        if sensors.get('4', '0') == '1':
            self.p4.setStyleSheet(parcheggio_occupato)
        if sensors.get('5', '0') == '1':
            self.p5.setStyleSheet(parcheggio_occupato)
        if sensors.get('6', '0') == '1':
            self.p6.setStyleSheet(parcheggio_occupato)
        if sensors.get('7', '0') == '1':
            self.p7.setStyleSheet(parcheggio_occupato)
        if sensors.get('8', '0') == '1':
            self.p8.setStyleSheet(parcheggio_occupato)
        if sensors.get('9', '0') == '1':
            self.p9.setStyleSheet(parcheggio_occupato)
        if sensors.get('10', '0') == '1':
            self.p10.setStyleSheet(parcheggio_occupato)
        if sensors.get('11', '0') == '1':
            self.p11.setStyleSheet(parcheggio_occupato)
        if sensors.get('12', '0') == '1':
            self.p12.setStyleSheet(parcheggio_occupato)
        if sensors.get('13', '0') == '1':
            self.p13.setStyleSheet(parcheggio_occupato)
        if sensors.get('14', '0') == '1':
            self.p14.setStyleSheet(parcheggio_occupato)
        if sensors.get('15', '0') == '1':
            self.p15.setStyleSheet(parcheggio_occupato)
        if sensors.get('16', '0') == '1':
            self.p16.setStyleSheet(parcheggio_occupato)
        if sensors.get('17', '0') == '1':
            self.p17.setStyleSheet(parcheggio_occupato)
        if sensors.get('18', '0') == '1':
            self.p18.setStyleSheet(parcheggio_occupato)
        if sensors.get('19', '0') == '1':
            self.p19.setStyleSheet(parcheggio_occupato)
        if sensors.get('20', '0') == '1':
            self.p20.setStyleSheet(parcheggio_occupato)
        if sensors.get('21', '0') == '1':
            self.p21.setStyleSheet(parcheggio_occupato)
        if sensors.get('22', '0') == '1':
            self.p22.setStyleSheet(parcheggio_occupato)
        if sensors.get('23', '0') == '1':
            self.p23.setStyleSheet(parcheggio_occupato)
        if sensors.get('24', '0') == '1':
            self.p24.setStyleSheet(parcheggio_occupato)
        if sensors.get('25', '0') == '1':
            self.p25.setStyleSheet(parcheggio_occupato)
        if sensors.get('26', '0') == '1':
            self.p26.setStyleSheet(parcheggio_occupato)
        if sensors.get('27', '0') == '1':
            self.p27.setStyleSheet(parcheggio_occupato)
        if sensors.get('28', '0') == '1':
            self.p28.setStyleSheet(parcheggio_occupato)
        if sensors.get('29', '0') == '1':
            self.p29.setStyleSheet(parcheggio_occupato)
        if sensors.get('30', '0') == '1':
            self.p30.setStyleSheet(parcheggio_occupato)
        if sensors.get('31', '0') == '1':
            self.p31.setStyleSheet(parcheggio_occupato)
        if sensors.get('32', '0') == '1':
            self.p32.setStyleSheet(parcheggio_occupato)

    def prenotaParcheggio(self, e):

        global parcheggio_prenotato

        try:
            if "#33ff66" in self.p1.styleSheet() and self.p1.hasFocus():
                self.p1.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p2.styleSheet() and self.p2.hasFocus():
                self.p2.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p3.styleSheet() and self.p3.hasFocus():
                self.p3.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p4.styleSheet() and self.p4.hasFocus():
                self.p4.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p5.styleSheet() and self.p5.hasFocus():
                self.p5.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p6.styleSheet() and self.p6.hasFocus():
                self.p6.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p7.styleSheet() and self.p7.hasFocus():
                self.p7.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p8.styleSheet() and self.p8.hasFocus():
                self.p8.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p9.styleSheet() and self.p9.hasFocus():
                self.p9.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p10.styleSheet() and self.p10.hasFocus():
                self.p10.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p11.styleSheet() and self.p11.hasFocus():
                self.p11.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p12.styleSheet() and self.p12.hasFocus():
                self.p12.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p13.styleSheet() and self.p13.hasFocus():
                self.p13.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p14.styleSheet() and self.p14.hasFocus():
                self.p14.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p15.styleSheet() and self.p15.hasFocus():
                self.p15.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p16.styleSheet() and self.p16.hasFocus():
                self.p16.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p17.styleSheet() and self.p17.hasFocus():
                self.p17.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p18.styleSheet() and self.p18.hasFocus():
                self.p18.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p19.styleSheet() and self.p19.hasFocus():
                self.p19.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p20.styleSheet() and self.p20.hasFocus():
                self.p20.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p21.styleSheet() and self.p21.hasFocus():
                self.p21.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p22.styleSheet() and self.p22.hasFocus():
                self.p22.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p23.styleSheet() and self.p23.hasFocus():
                self.p23.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p24.styleSheet() and self.p24.hasFocus():
                self.p24.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p25.styleSheet() and self.p25.hasFocus():
                self.p25.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p26.styleSheet() and self.p26.hasFocus():
                self.p26.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p27.styleSheet() and self.p27.hasFocus():
                self.p27.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p28.styleSheet() and self.p28.hasFocus():
                self.p28.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p29.styleSheet() and self.p29.hasFocus():
                self.p29.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p30.styleSheet() and self.p30.hasFocus():
                self.p30.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p31.styleSheet() and self.p31.hasFocus():
                self.p31.setStyleSheet(parcheggio_prenotato)
            if "#33ff66" in self.p32.styleSheet() and self.p32.hasFocus():
                self.p32.setStyleSheet(parcheggio_prenotato)
        except:
            pass


##############################


if __name__ == "__main__":
    show_parking()
