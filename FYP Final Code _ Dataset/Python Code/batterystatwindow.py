
from PyQt5 import QtCore, QtGui, QtWidgets
import serial
import serial.tools.list_ports


class Ui_MainWindow3(object):

    def setup2(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.setWindowIcon(QtGui.QIcon('battery.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 70 , 241, 45))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.refresh)
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(40, 20, 241, 45))
        self.pushButton1.setObjectName("pushButton")
        self.pushButton1.clicked.connect(self.aduconn)
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(40, 120, 241, 45))
        self.pushButton2.setObjectName("pushButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(400, 195, 350, 30))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setStyleSheet(
            "QProgressBar { text-align: center; color: white ;} QProgressBar::chunk { border-radius: 5px  ;background-color: red ; width: 83px; margin: 2px;}")
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(400, 10, 300, 62))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(400, 260, 351, 91))
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber_2.setGeometry(QtCore.QRect(400, 390, 351, 91))
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(50, 269, 301, 81))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 399, 311, 71))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(50, 185, 291, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionRefresh_States = QtWidgets.QAction(MainWindow)
        self.actionRefresh_States.setObjectName("actionRefresh_States")
        self.actionRefresh_States.triggered.connect(self.refresh)
        self.actionRefresh_States.setShortcut("Ctrl+R")
        self.actiongotomain = QtWidgets.QAction(MainWindow)
        self.actiongotomain.setObjectName("actiongotomain")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.triggered.connect(self.close)
        self.menuFile.addAction(self.actionRefresh_States)
        self.menuFile.addAction(self.actiongotomain)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BatteryStatus"))
        self.pushButton.setText(_translate("MainWindow", "Get Stats"))
        self.pushButton1.setText(_translate("MainWindow", "Connect HW"))
        self.pushButton2.setText(_translate("MainWindow", "Goto Main"))
        self.label.setText(_translate("MainWindow", "No Arduino connected."))
        self.label_2.setText(_translate("MainWindow", "Battery Volt (V)"))
        self.label_3.setText(_translate("MainWindow", "Battery Current (mAh)"))
        self.label_4.setText(_translate("MainWindow", "Battery Bar: "))
        self.menuFile.setTitle(_translate("MainWindow", "Options"))
        self.actionRefresh_States.setText(_translate("MainWindow", "Get Stats"))
        self.actiongotomain.setText(_translate("MainWindow", "Goto Main"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

    def portcheck(self):
        arduino_ports = [  # automatically searches for an Arduino and selects the port it's on
            p.device
            for p in serial.tools.list_ports.comports()
            if 'Arduino' in p.description
        ]
        return arduino_ports

    conn = False

    def aduconn(self):
        ports = self.portcheck()
        if not ports:
            self.label.setText("No Arduino HW found - is it plugged in?\nIf so, restart computer.")
        elif len(ports) > 1:
            self.label.setText('Multiple Arduino HWs found\n using the first.')
        else:
            self.label.setText('Arduino HW is plugged in and connected.')
            self.conn = True
            return True


    def refresh(self):
        if self.conn:
            conn1 = self.aduconn()
            if conn1:
                ports = self.portcheck()
                ser = serial.Serial(ports[0], 9600, dsrdtr=True)
                arduinoData = ser.readline().decode('ascii')
                bcheck = str(arduinoData)
                bcheck = bcheck.strip()
                if bcheck != "low" and bcheck != "high":
                    data = arduinoData.split(",")
                    if float(data[0]) <= 3.3:
                        self.progressBar.setProperty("value", 0)
                    elif float(data[0]) > 3.9:
                        self.progressBar.setProperty("value", 100)
                        self.progressBar.setStyleSheet(
                            "QProgressBar::chunk { background-color: green ; border-radius: 5px  ; width: 83px; margin: 2px}")
                    elif float(data[0]) > 3.7:
                        self.progressBar.setProperty("value", 60)
                        self.progressBar.setStyleSheet(
                            "QProgressBar::chunk { background-color: yellow ; border-radius: 5px  ; width: 83px; margin: 2px}")
                    elif float(data[0]) > 3.5:
                        self.progressBar.setProperty("value", 40)
                        self.progressBar.setStyleSheet(
                            "QProgressBar::chunk { background-color: orange ; border-radius: 5px  ; width: 83px; margin: 2px}")
                    elif float(data[0]) > 3.39:
                        self.progressBar.setProperty("value", 25)
                        self.progressBar.setStyleSheet(
                            "QProgressBar::chunk { background-color: red ; border-radius: 5px ; width: 83px; margin: 2px}")

                    self.lcdNumber.display(float(data[0]))
                    self.lcdNumber_2.display(float(data[1]))
                    ser.reset_input_buffer()
                    ser.flushInput()
                    ser.flushOutput()
                    ser.close()
                else:
                    self.label.setText('Battery is not charged or is not connected')
            else:
                self.conn = False
        else:
            self.label.setText('Arduino HW is not connected.\nClick Connect HW')
