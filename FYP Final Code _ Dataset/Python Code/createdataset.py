from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
import serial
import serial.tools.list_ports
from decimal import *
import csv
import time as time


class Ui_MainWindow4(object):

    def setup3(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.setWindowIcon(QtGui.QIcon('battery.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 120, 241, 45))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.createdt)
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton1.setGeometry(QtCore.QRect(40, 20, 241, 45))
        self.pushButton1.setObjectName("pushButton")
        self.pushButton1.clicked.connect(self.aduconn)
        self.pushButton3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton3.setGeometry(QtCore.QRect(40, 70, 241, 45))
        self.pushButton3.setObjectName("pushButton3")
        self.pushButton3.clicked.connect(self.getpath)
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2.setGeometry(QtCore.QRect(40, 170, 241, 45))
        self.pushButton2.setObjectName("pushButton2")
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
        self.actiongotomain = QtWidgets.QAction(MainWindow)
        self.actiongotomain.setObjectName("actiongotomain")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.triggered.connect(self.close)
        self.menuFile.addAction(self.actiongotomain)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Create Dataset"))
        self.pushButton.setText(_translate("MainWindow", "Create Dataset"))
        self.pushButton1.setText(_translate("MainWindow", "Connect HW"))
        self.pushButton2.setText(_translate("MainWindow", "Goto Main"))
        self.pushButton3.setText(_translate("MainWindow", "Set Path"))
        self.label.setText(_translate("MainWindow", "No Arduino connected."))
        self.label_2.setText(_translate("MainWindow", "Battery Volt (V)"))
        self.label_3.setText(_translate("MainWindow", "Battery Current (mAh)"))
        self.menuFile.setTitle(_translate("MainWindow", "Options"))
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

    pp =False

    def getpath(self):
        if self.conn:
            conn1 = self.aduconn()
            if conn1:
                self.path_name = QFileDialog.getExistingDirectory(self, "Select Path")
                if self.path_name:
                    self.path = self.path_name + '/data.csv'
                    print(self.path)
                    self.label.setText('Path Selected.Click Create Dataset')
                    self.pp = True
                else:
                    self.label.setText('Path Not Selected.')
            else:
                self.conn = False
        else:
            self.label.setText('Arduino HW is not connected.\nClick Connect HW')

    loopcheck = False

    def createdt(self):
        self.input_data = '0'
        if self.conn:
            if self.pp:
                conn1 = self.aduconn()
                if conn1:
                    if self.input_data == '0' and not self.loopcheck:
                        ports = self.portcheck()
                        ser = serial.Serial(ports[0], 9600)
                        time.sleep(2)
                        arduinoData = ser.readline().decode('ascii')
                        bcheck = str(arduinoData)
                        bcheck = bcheck.strip()
                        if bcheck != "low" and bcheck != "high":
                            self.input_data = '1'
                            ser.write(self.input_data.encode())
                            print("Mosfet ON")
                            with open(self.path, 'w', newline='') as myfile:
                                thewriter = csv.writer(myfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                                thewriter.writerow(['volt', 'current','capacity'])
                                i = 0
                                arduinoData = ser.readline().decode('ascii')
                                data = arduinoData.split(",")
                                d = float(data[0])
                                print(d)
                                self.loopcheck = True
                                while d > 3.90:
                                    print(d)
                                    QtCore.QCoreApplication.processEvents()
                                    ser.flushInput()
                                    arduinoData = ser.readline().decode('ascii')
                                    print(arduinoData)
                                    data = arduinoData.split(",")
                                    d = Decimal(data[0])
                                    d1 = Decimal(data[1])
                                    d2 = Decimal(data[2])
                                    thewriter.writerow([d, d1, d2])
                                    self.lcdNumber.display(float(data[0]))
                                    self.lcdNumber_2.display(float(data[1]))
                                    time.sleep(2)
                                    i = i+1

                            time.sleep(10)
                            self.input_data = '0'
                            ser.write(self.input_data.encode())
                            self.label.setText('Dataset Created.')
                            self.loopcheck = False
                        else:
                            self.label.setText('Battery is not charged or is not connected')

                    else:
                        self.label.setText('Creating dataset.')

                else:
                    self.conn = False

            else:
                self.label.setText('Path not set.\nClick Set Path')

        else:
            self.label.setText('Arduino HW is not connected.\nClick Connect HW')



    def refresh(self):
        if self.conn:
            conn1 = self.aduconn()
            if conn1:
                ports = self.portcheck()
                ser = serial.Serial(ports[0], 9600, dsrdtr=True)
                arduinoData = ser.readline().decode('ascii')
                print(arduinoData)
                data = arduinoData.split(",")
                self.lcdNumber.display(float(data[0]))
                self.lcdNumber_2.display(float(data[1]))
                ser.reset_input_buffer()
                ser.flushInput()
                ser.flushOutput()
                ser.close()
            else:
                self.conn = False
        else:
            self.label.setText('Arduino HW is not connected.\nClick Connect HW')
