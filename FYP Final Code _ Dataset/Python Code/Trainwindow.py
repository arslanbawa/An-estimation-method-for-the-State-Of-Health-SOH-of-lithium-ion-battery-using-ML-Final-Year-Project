from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog
from chgwig import Chgwig
from dischgwig import dischgwigv
from dischgwig import dischgwigc
from mat2json import loadMat
from util import getBatteryCapacity, getDischargingValues, getDataframe, rollingAverage
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from pandas import DataFrame
import csv
import numpy
from decimal import *


class Ui_MainWindow2(object):
    def setup1(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.setWindowIcon(QtGui.QIcon('battery.png'))
        self.centralwidget.setObjectName("centralwidget")
        self.loadtdButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadtdButton.setGeometry(QtCore.QRect(10, 20, 261, 101))
        self.loadtdButton.setObjectName("loadtdButton")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 140, 261, 111))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.Train)
        self.backButton = QtWidgets.QPushButton(self.centralwidget)
        self.backButton.setGeometry(QtCore.QRect(10, 400, 261, 111))
        self.backButton.setObjectName("backButton")
        self.widget = Chgwig(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(285, 20, 500, 350))
        self.widget.setObjectName("widget")
        self.widget_2 = dischgwigv(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(285, 360, 500, 350))
        self.widget_2.setObjectName("widget_2")
        self.widget_3 = dischgwigc(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(775, 20, 720, 690))
        self.widget_3.setObjectName("widget_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 270, 261, 111))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.Test)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 520, 261, 111))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuDataset = QtWidgets.QMenu(self.menubar)
        self.menuDataset.setObjectName("menuDataset")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_Training_Dataset = QtWidgets.QAction(MainWindow)
        self.actionLoad_Training_Dataset.setObjectName("actionLoad_Training_Dataset")
        self.actionLoad_Training_Dataset.setStatusTip('Load Dataset')
        self.actionLoad_Training_Dataset.setShortcut("Ctrl+O")
        self.actionLoad_Training_Dataset.triggered.connect(self.file_open)
        self.actiongotomain = QtWidgets.QAction(MainWindow)
        self.actiongotomain.setObjectName("actiongotomain")
        self.actionexit = QtWidgets.QAction(MainWindow)
        self.actionexit.setObjectName("actionexit")
        self.actionexit.triggered.connect(self.close)
        self.menuDataset.addAction(self.actionLoad_Training_Dataset)
        self.menuDataset.addAction(self.actiongotomain)
        self.menuDataset.addAction(self.actionexit)
        self.menubar.addAction(self.menuDataset.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Prediction"))
        self.loadtdButton.setText(_translate("MainWindow", "Load Dataset"))
        self.loadtdButton.clicked.connect(self.file_open)
        self.label.setText(_translate("MainWindow", "Dataset not loaded."))
        self.pushButton.setText(_translate("MainWindow", "Train"))
        self.pushButton_2.setText(_translate("MainWindow", "Test"))
        self.backButton.setText(_translate("MainWindow", "Main Page"))
        self.menuDataset.setTitle(_translate("MainWindow", "Dataset"))
        self.actionLoad_Training_Dataset.setText(_translate("MainWindow", "Load Training Dataset"))
        self.actiongotomain.setText(_translate("MainWindow", "Goto Main"))
        self.actionexit.setText(_translate("MainWindow", "Exit"))

    path = ""
    test = False
    train = False
    presstr = False
    presst = False

    def file_open(self):
        file_name = QFileDialog.getOpenFileName(self, "Load Dataset")
        print(file_name)
        self.path = file_name[0]
        if self.path:
            if self.path.endswith('.mat'):
                self.label.setText("Dataset loaded.\nPress Train Button.")
                self.widget.canvas.axes.clear()
                self.widget.canvas.draw()
                self.widget_2.canvas.axes.clear()
                self.widget_2.canvas.draw()
                self.widget_3.canvas.axes.clear()
                self.widget_3.canvas.draw()
                self.train = True
                self.presstr = False
                self.presst = False

            elif self.path.endswith('.csv'):
                self.label.setText("Dataset loaded.\nPress Train Button.")
                self.widget.canvas.axes.clear()
                self.widget.canvas.draw()
                self.widget_2.canvas.axes.clear()
                self.widget_2.canvas.draw()
                self.widget_3.canvas.axes.clear()
                self.widget_3.canvas.draw()
                self.train = True
                self.presstr = False
                self.presst = False


            else:
                self.path = ""
                self.label.setText("Unable to load Dataset.\nInvalid File Extension")

    def Train(self):
        if self.path:
            if (not self.presst and not self.train) or (not self.presstr and self.train):
                print('')

            if self.presstr:
                self.label.setText("Training already done.")
            if self.train and not self.presstr and self.path.endswith('.mat'):
                self.B0005 = loadMat(self.path)
                B0005_capacity = getBatteryCapacity(self.B0005)
                self.widget_3.canvas.axes.clear()
                self.widget_3.canvas.axes.plot(B0005_capacity[0], B0005_capacity[1], color='blue')
                print(type(B0005_capacity))
                self.widget_3.canvas.axes.set(xlabel='Discharge cycles', title='Capacity degradation ',
                                              ylabel='Capacity/Ah')
                self.widget_3.canvas.draw()
                B0005_discharging = getDischargingValues(self.B0005, 17)
                self.widget_2.canvas.axes.clear()
                self.widget_2.canvas.axes.plot(B0005_discharging[5], B0005_discharging[1], color='orange')
                self.widget_2.canvas.axes.set(xlabel='Time in seconds', ylabel='Voltage_measured',
                                              title='Discharging performance')
                self.widget_2.canvas.draw()
                self.widget.canvas.axes.clear()
                self.widget.canvas.axes.plot(B0005_discharging[5], B0005_discharging[2], color='green')
                self.widget.canvas.axes.set(xlabel='Time in seconds', ylabel='Current_measured',
                                            title='Discharging performance')
                self.widget.canvas.draw()
                self.presstr = True
                self.label.setText("Training done.\nPress Test Button.")

            elif self.train and not self.presstr and self.path.endswith('.csv'):
                file_name = QFileDialog.getOpenFileName(self, "Load Capacity Dataset")
                print(file_name)
                self.path1 = file_name[0]
                c1 = []
                c2 = []
                c3 = []
                self.cca = []
                self.ccy = []
                if self.path1:
                    if self.path1.endswith('.csv'):
                        with open(self.path, 'r') as file:
                            reader = csv.reader(file)
                            line_count = 0
                            time = 0
                            for row in reader:
                                if line_count > 0:
                                    c1.append(float(row[0]))
                                    c2.append(float(row[1]))
                                    c3.append(time)
                                line_count += 1
                                time += 2
                        with open(self.path1, 'r') as file:
                            reader1 = csv.reader(file)
                            line_count1 = 0
                            for row in reader1:
                                if line_count1 > 0:
                                    self.ccy.append(int(row[0]))
                                    self.cca.append(float(row[1]))
                                line_count1 += 1

                        self.widget_3.canvas.axes.clear()
                        self.widget_3.canvas.axes.plot(self.ccy, self.cca, color='blue',
                                                       )
                        self.widget_3.canvas.axes.set(xlabel='Discharge cycles', title='Capacity degradation ',
                                                      ylabel='Capacity/Ah')
                        self.widget_3.canvas.draw()
                        self.widget_2.canvas.axes.clear()
                        self.widget_2.canvas.axes.plot(c3, c1, color='orange')
                        self.widget_2.canvas.axes.set(xlabel='Time in seconds', ylabel='Voltage_measured',
                                                      title='Discharging performance')
                        self.widget_2.canvas.draw()
                        self.widget.canvas.axes.clear()
                        self.widget.canvas.axes.plot(c3, c2, color='green')
                        self.widget.canvas.axes.set(xlabel='Time in seconds', ylabel='Current_measured',
                                                    title='Discharging performance')
                        self.widget.canvas.draw()
                        self.presstr = True
                        self.label.setText("Training done.\nPress Test Button.")
                    else:
                        self.label.setText("Unable to load Capacity Dataset.\nInvalid File Extension")
                else:
                    self.label.setText("Capacity Dataset not Loaded.")

            if self.test and not self.presst and self.path.endswith('.mat'):
                dfB0005 = getDataframe(self.B0005)
                X = dfB0005['cycle']
                Y = dfB0005['capacity']
                X_train, X_test1, y_train, y_test1 = train_test_split(X, Y, test_size=0.2, shuffle=False)
                lst_x, lst_y = rollingAverage(X_train, y_train)
                d = {'X_train': X_train.values, 'y_train': y_train.values}
                d = DataFrame(d)
                d = d[~d['X_train'].isin(lst_x)]
                X_train = d['X_train']
                y_train = d['y_train']
                X_train = X_train.values.reshape(-1, 1)
                y_train = y_train.values.reshape(-1, 1)
                print(type(X))
                best_svr = SVR(C=20, epsilon=0.0001, gamma=0.00001, cache_size=200, kernel='rbf', max_iter=-1,
                               shrinking=True, tol=0.001, verbose=False)
                best_svr.fit(X_train, y_train)
                pred = best_svr.predict(X.values.reshape(-1, 1))
                acc = best_svr.score(X.values.reshape(-1, 1), Y.values.reshape(-1, 1))
                print(acc)
                X = dfB0005['cycle']
                Y = dfB0005['capacity']
                ratios = [40, 30, 20, 10]
                for ratio in ratios:
                    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=ratio, shuffle=False)
                    lst_x, lst_y = rollingAverage(X_train, y_train)
                    d = {'X_train': X_train.values, 'y_train': y_train.values}
                    d = DataFrame(d)
                    d = d[~d['X_train'].isin(lst_x)]
                    X_train = d['X_train']
                    y_train = d['y_train']
                    X_train = X_train.values.reshape(-1, 1)
                    y_train = y_train.values.reshape(-1, 1)
                    best_svr = SVR(C=20, epsilon=0.0001, gamma=0.0001, cache_size=200,
                                   kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
                    best_svr.fit(X_train, y_train)
                    if ratio == 40:
                        y_pred_40 = best_svr.predict(X.values.reshape(-1, 1))
                    elif ratio == 30:
                        y_pred_30 = best_svr.predict(X.values.reshape(-1, 1))
                    elif ratio == 20:
                        y_pred_20 = best_svr.predict(X.values.reshape(-1, 1))
                    elif ratio == 10:
                        y_pred_10 = best_svr.predict(X.values.reshape(-1, 1))
                B0005_capacity = getBatteryCapacity(self.B0005)
                self.widget.canvas.axes.clear()
                self.widget.canvas.axes.plot(B0005_capacity[0], B0005_capacity[1], color='blue')
                self.widget.canvas.axes.set(xlabel='Discharge cycles', title='Capacity degradation ',
                                            ylabel='Capacity/Ah')
                self.widget.canvas.draw()
                self.widget_2.canvas.axes.clear()
                self.widget_2.canvas.axes.plot(X, pred, color='red')
                self.widget_2.canvas.axes.set(xlabel='Discharge cycles', ylabel='Capacity/Ah',
                                              title='Predicted Capacity Degradation')
                self.widget_2.canvas.draw()
                self.widget_3.canvas.axes.clear()
                self.widget_3.canvas.axes.plot(X, y_pred_40, color='black')
                self.widget_3.canvas.axes.plot(X, y_pred_30, color='orange')
                self.widget_3.canvas.axes.plot(X, y_pred_20, color='blue')
                self.widget_3.canvas.axes.plot(X, y_pred_10, color='green')
                self.widget_3.canvas.axes.set(xlabel='Discharging cycles', ylabel='Capacity/Ah',
                                              title='Predicted Battery Degradation')
                self.widget_3.canvas.axes.legend(('Prediction with train size of 60%',
                                                  'Prediction with train size of 70%',
                                                  'Prediction with train size of 80%',
                                                  'Prediction with train size of 90%'), loc='upper right')
                self.widget_3.canvas.draw()
                self.test = False
                self.presst = True
                acc1 = acc * 100
                self.label.setText("SOH Predicted.\n" + str(int(acc1)) + " % accuracy")

            if self.test and not self.presst and self.path.endswith('.csv'):
                X1 = self.ccy
                Y1 = self.cca
                X_train1, X_test11, y_train1, y_test11 = train_test_split(X1, Y1, test_size=0.05, shuffle=False)
                d = {'X_train': X_train1, 'y_train': y_train1}
                d = DataFrame(d)
                X_train1 = d['X_train']
                y_train1 = d['y_train']
                X_train1 = X_train1.values.reshape(-1, 1)
                y_train1 = y_train1.values.reshape(-1, 1)

                best_svr = SVR(C=20, epsilon=0.0001, gamma=0.0001, cache_size=200,
                               kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
                best_svr.fit(X_train1, y_train1)
                d1 = {'Xt': X1, 'yt': Y1}
                d1 = DataFrame(d1)
                Xt = d1['Xt']
                yt = d1['yt']
                Xt = Xt.values.reshape(-1, 1)
                yt = yt.values.reshape(-1, 1)
                pred1 = best_svr.predict(Xt)
                acc = best_svr.score(Xt, yt)
                self.widget.canvas.axes.clear()
                self.widget.canvas.axes.plot(self.ccy, self.cca, color='blue')
                self.widget.canvas.axes.set(xlabel='Discharge cycles', title='Capacity degradation ',
                                            ylabel='Capacity/Ah')
                self.widget.canvas.draw()
                self.widget_2.canvas.axes.clear()
                self.widget_2.canvas.axes.plot(Xt, pred1, color='red')
                self.widget_2.canvas.axes.set(xlabel='Discharge cycles', ylabel='Capacity/Ah',
                                              title='Predicted Capacity Degradation')
                self.widget_2.canvas.draw()
                X_train1, X_test11, y_train1, y_test11 = train_test_split(X1, Y1, test_size=0.3, shuffle=False)
                d = {'X_train': X_train1, 'y_train': y_train1}
                d = DataFrame(d)
                X_train1 = d['X_train']
                y_train1 = d['y_train']
                X_train1 = X_train1.values.reshape(-1, 1)
                y_train1 = y_train1.values.reshape(-1, 1)
                best_svr = SVR(C=20, epsilon=0.0001, gamma=0.0001, cache_size=200,
                               kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
                best_svr.fit(X_train1, y_train1)
                y_pred_101 = best_svr.predict(Xt)
                self.widget_3.canvas.axes.clear()
                self.widget_3.canvas.axes.plot(Xt, y_pred_101, color='green')
                self.widget_3.canvas.axes.set(xlabel='Discharging cycles', ylabel='Capacity/Ah',
                                              title='Predicted Battery Degradation')
                self.widget_3.canvas.axes.legend(('Prediction with train size of 70%',), loc='upper right')
                self.widget_3.canvas.draw()
                self.test = False
                self.presst = True
                acc1 = acc * 100
                self.label.setText("SOH Predicted.\n" + str(int(acc1)) + " % accuracy")

        else:
            self.label.setText("Dataset not Loaded.")

    def Test(self):
        if self.path:
            if self.presstr:
                if self.presst:
                    self.label.setText("Prediction already done.")
                else:
                    self.train = False
                    self.test = True
                    self.Train()
            else:
                self.label.setText("Training not done.\nPress Train Button.")


        else:
            self.label.setText("Dataset not Loaded.")
