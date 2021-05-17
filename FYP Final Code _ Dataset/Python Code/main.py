# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 00:17:49 2020

@author: SaadNafees
"""
import os
import sys
from PyQt5 import QtWidgets
from Mainwindow import Ui_MainWindow
from Trainwindow import Ui_MainWindow2
from batterystatwindow import Ui_MainWindow3
from createdataset import Ui_MainWindow4


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)


class statwind(QtWidgets.QMainWindow, Ui_MainWindow3):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setup2(self)


class trainwind(QtWidgets.QMainWindow, Ui_MainWindow2):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setup1(self)


class cdatasetwindow(QtWidgets.QMainWindow, Ui_MainWindow4):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setup3(self)


def changeWindow(w1, w2):
    w1.hide()
    w2.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    stat = statwind()
    train = trainwind()
    cdata = cdatasetwindow()

    main.Button.clicked.connect(lambda: changeWindow(main, stat))
    main.inputButton.clicked.connect(lambda: changeWindow(main, cdata))
    main.trainButton.clicked.connect(lambda: changeWindow(main, train))
    stat.actiongotomain.triggered.connect(lambda: changeWindow(stat, main))
    stat.pushButton2.clicked.connect(lambda: changeWindow(stat, main))
    cdata.actiongotomain.triggered.connect(lambda: changeWindow(cdata, main))
    cdata.pushButton2.clicked.connect(lambda: changeWindow(cdata, main))
    train.backButton.clicked.connect(lambda: changeWindow(train, main))
    train.actiongotomain.triggered.connect(lambda: changeWindow(train, main))
    main.show()
    sys.exit(app.exec_())
