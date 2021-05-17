

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    
  
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 450)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.setWindowIcon(QtGui.QIcon('battery.png'))
        self.centralwidget.setObjectName("centralwidget")
        self.inputButton = QtWidgets.QPushButton(self.centralwidget)
        self.inputButton.setGeometry(QtCore.QRect(320, 110, 250, 51))
        self.inputButton.setObjectName("inputButton")
        self.trainButton = QtWidgets.QPushButton(self.centralwidget)
        self.trainButton.setGeometry(QtCore.QRect(320, 180, 250, 51))
        self.trainButton.setObjectName("trainButton")
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(320, 320, 250, 51))
        self.exitButton.clicked.connect(self.close)
        self.exitButton.setObjectName("testButton")
        self.Button = QtWidgets.QPushButton(self.centralwidget)
        self.Button.setGeometry(QtCore.QRect(320, 252, 250, 51))
        self.Button.setObjectName("Button")
        self.mainlabel = QtWidgets.QLabel(self.centralwidget)
        self.mainlabel.setGeometry(QtCore.QRect(10, 12, 550, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.mainlabel.setFont(font)
        self.mainlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mainlabel.setObjectName("mainlabel")
        self.mainlabel1 = QtWidgets.QLabel(self.centralwidget)
        self.mainlabel1.setGeometry(QtCore.QRect(30, 100, 256, 256))
        self.mainlabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.mainlabel1.setObjectName("mainlabel1")
        self.mainlabel1.setPixmap(QtGui.QPixmap("battery.png"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 523, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.inputButton.setText(_translate("MainWindow", "Create Dataset"))
        self.trainButton.setText(_translate("MainWindow", "Prediction"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))
        self.Button.setText(_translate("MainWindow", "Battery Status"))
        self.mainlabel.setText(_translate("MainWindow", "State of Health(SOH) Estimation of Lithium-Ion Batteries"))

