import cx_Freeze
from glob import glob # riga necessaria per il packaging con pyqtGraph
import sys, os

application_title = "LoraTool" #nome del applicazione
main_python_file = "ToolIVMS2_4.py" #nome del file .py costituente il programma

base = None

if sys.platform == "win32":
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = "C:\\Anaconda\\pkgs\\python-3.6.1-2\\tcl\\tcl8.6"
os.environ["TCLLIBPATH"]= r"C:\\Anaconda\\pkgs\\python-3.6.1-2\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Anaconda\\pkgs\\python-3.6.1-2\\tcl\\tk8.6"

includes = ["atexit", "re", "os", "time",  "ctypes", "ctypes.wintypes", "csv", "sys",
            "PyQt5.QtGui", "PyQt5.QtWidgets", "PyQt5.uic", "PyQt5.QtCore", "PyQt5.QtSerialPort",
            "PyQt5.QtMultimedia", "math", "datetime", "subprocess", "platform", "pyqtgraph", "numpy",
            "cv2", "openpyxl", "OpenGL.GL"]

packages = ["serial", "serial.tools.list_ports", "xmodem", "glob", "pyqtgraph", 
            "numpy", "numpy.lib", "numpy.lib.format", "numpy.core._methods", "numpy.core", "numpy.add_newdocs",
            "pyqtgraph.debug","pyqtgraph.functions", "pyqtgraph.ThreadsafeTimer", "OpenGL"]

include_files = [ "testIVMS.ui", "ui_descrizioneIVMS1_5.py", "ui_ricerca_proesys.py", "ui_loginIVMS.py",
                 "ui_anagraficaIVMS.py", "ui_configurazioni_proesys.py", "fotocamera.jpg", 
                 "LoRa-Alliance.jpg", "Apparato.png", "aggiorna.png", "AntennaRossa.png", 
                 "AntennaGialla.png", "AntennaVerde.png", "connect.png", "delete.png", "fileopen.png", 
                 "closeMenu.png", "monitor.png", "pin_ciano.png", "status_02.png", "status_03.png", "status_04.png",
                 "88551.gif", "warning.png", "TEST.xlsx", "AnagraficaIVMS.xlsx",
                 "MultiLanguage.xlsx", "progressBarAnim.gif", "msvcrt.dll", 
                 "AntennaGrigia.png", "libEGL.dll", "libGLESv2.dll",
                 "LibrerieUtili\Include","LibrerieUtili\lib2to3", "LibrerieUtili\PyQt5", "LibrerieUtili\_ctypes.pyd",
                 "LibrerieUtili\_hashlib.pyd", "LibrerieUtili\_multiprocessing.pyd", "LibrerieUtili\\api-ms-win-crt-conio-l1-1-0.dll",
                 "LibrerieUtili\\api-ms-win-crt-convert-l1-1-0.dll", "LibrerieUtili\\api-ms-win-crt-environment-l1-1-0.dll",
                 "LibrerieUtili\\api-ms-win-crt-filesystem-l1-1-0.dll", "LibrerieUtili\\api-ms-win-crt-heap-l1-1-0.dll",
                 "LibrerieUtili\\api-ms-win-crt-locale-l1-1-0.dll", "LibrerieUtili\\api-ms-win-crt-math-l1-1-0.dll",
                 "LibrerieUtili\\api-ms-win-crt-multibyte-l1-1-0.dll", "LibrerieUtili\\api-ms-win-crt-process-l1-1-0.dll",
                 "LibrerieUtili\\api-ms-win-crt-runtime-l1-1-0.dll", "LibrerieUtili\\api-ms-win-crt-stdio-l1-1-0.dll",
                 "LibrerieUtili\\api-ms-win-crt-string-l1-1-0.dll", "LibrerieUtili\\api-ms-win-crt-time-l1-1-0.dll",
                 "LibrerieUtili\\api-ms-win-crt-utility-l1-1-0.dll", "LibrerieUtili\\freetype.dll", "LibrerieUtili\hdf5.dll",
                 "LibrerieUtili\hdf5_hl.dll", "LibrerieUtili\icudt58.dll", "LibrerieUtili\icuuc58.dll", "LibrerieUtili\LIBEAY32.dll",
                 "LibrerieUtili\libifcoremd.dll", "LibrerieUtili\libiomp5md.dll", "LibrerieUtili\libjpeg.dll",
                 "LibrerieUtili\libmmd.dll", "LibrerieUtili\libpng16.dll", "LibrerieUtili\mkl_core.dll", "LibrerieUtili\mkl_def.dll",
                 "LibrerieUtili\mkl_intel_thread.dll", "LibrerieUtili\MSVCP140.dll", "LibrerieUtili\pyexpat.pyd",
                 "LibrerieUtili\PyQt5.Qt.pyd", "LibrerieUtili\PyQt5.QtCore.pyd", "LibrerieUtili\PyQt5.QtGui.pyd", "LibrerieUtili\PyQt5.QtMultimedia.pyd",
                 "LibrerieUtili\PyQt5.QtNetwork.pyd", "LibrerieUtili\PyQt5.QtOpenGL.pyd", "LibrerieUtili\PyQt5.QtPrintSupport.pyd",
                 "LibrerieUtili\PyQt5.QtSerialPort.pyd", "LibrerieUtili\PyQt5.QtSvg.pyd", "LibrerieUtili\PyQt5.QtTest.pyd",
                 "LibrerieUtili\PyQt5.QtWidgets.pyd", "LibrerieUtili\python36.dll", "LibrerieUtili\pythoncom36.dll",
                 "LibrerieUtili\pywintypes36.dll", "LibrerieUtili\Qt5Core.dll", "LibrerieUtili\Qt5Gui.dll",
                 "LibrerieUtili\Qt5Multimedia.dll", "LibrerieUtili\Qt5Network.dll", "LibrerieUtili\Qt5OpenGL.dll",
                 "LibrerieUtili\Qt5PrintSupport.dll", "LibrerieUtili\Qt5SerialPort.dll", "LibrerieUtili\Qt5Svg.dll",
                 "LibrerieUtili\Qt5Test.dll", "LibrerieUtili\Qt5Widgets.dll", "LibrerieUtili\\sip.pyd",
                 "LibrerieUtili\\sqlite3.dll", "LibrerieUtili\\SSLEAY32.dll", "LibrerieUtili\\tcl86t.dll", "LibrerieUtili\\tk86t.dll",
                 "LibrerieUtili\VCRUNTIME140.dll", "LibrerieUtili\zlib.dll",
                 r"C:\Anaconda\Library\plugins\imageformats",
                 r"C:\Anaconda\Library\plugins\platforms",
                 r"C:\Anaconda\Library\plugins\mediaservice",
                 "Acc2Csv.exe", "Heatshrink.exe",
                 "libiconv.dll", "libzbar-64.dll", "opencv_ffmpeg320_64.dll",
                 "check.jpg", "serial.ini", "download.png", "modifica.png", "status_05.png",
                 "STM32FLASH.exe", "Update_Firmware.bat", "icona_tool_ivms.ico", "icona_tool_ivms.png",
                 "IVMS_password_default.txt"]
 
excludes = ["_gtkagg", "_tkagg", "bsddb", "curses", "pywin.debugger", "pywin.debugger.dbgcon", "pywin.dialogs", "tcl",
            "Tkconstants", "Tkinter", "distutils"]

icona = "icona_tool_ivms.ico"

cx_Freeze.setup(
        name = application_title,
        version = "2.4",
        author = "ProEsys",
        description = "LoRa Tool per gestione IVMS",
        options = {"build_exe": {"include_files" : include_files,
                                 "packages": packages,
                                 "includes": includes,
                                 "excludes" : excludes,
                                 "include_msvcr": True,
                                 }
                  },
        executables = [cx_Freeze.Executable(main_python_file, base = base, icon = icona)])