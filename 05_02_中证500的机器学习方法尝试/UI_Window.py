# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_Window.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from qt_model import Model


class Ui_Dialog(object):# object什么意思
    send_value = pyqtSignal()  # 创建槽信号,str指定接收参数为str类型(字符串类型)
    # def __init__(self,Dialog):
    #     self.setupUi( Dialog)
    def setupUi(self,Dialog):# 这里的Dialog什么意思
        Dialog.setObjectName("Dialog")
        Dialog.resize(819, 929)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(160, 190, 501, 351))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_4 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.gridLayout.addWidget(self.comboBox_4, 2, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        # 选择数据文件
        self.comboBox_3 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_3.setObjectName("comboBox_3")
        for index,filename in enumerate(os.listdir('./data')):
            self.comboBox_3.addItem("")

        self.gridLayout.addWidget(self.comboBox_3, 1, 1, 1, 1)

        # 输入的模型名称
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.comboBox_5 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.gridLayout.addWidget(self.comboBox_5, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 4, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(670, 210, 81, 46))
        self.pushButton.setObjectName("pushButton")

        self.pushButton.clicked.connect(self.find_model)

        self.title = QtWidgets.QLabel(Dialog)
        self.title.setGeometry(QtCore.QRect(330, 50, 141, 41))
        self.title.setObjectName("title")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(160, 600, 501, 161))
        self.textBrowser.setObjectName("textBrowser")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(170, 560, 108, 24))
        self.label_7.setObjectName("label_7")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setEnabled(True)
        self.checkBox.setGeometry(QtCore.QRect(460, 120, 231, 28))
        self.checkBox.setObjectName("checkBox")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(590, 810, 150, 46))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.submit)

        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(400, 810, 150, 46))
        self.pushButton_3.setObjectName("pushButton_2")
        self.pushButton_3.clicked.connect(self.stop)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def stop(self):
        print('中止程序')
        sys.exit(app.exec_())

    def submit(self):
        self.model_name=self.lineEdit.text()
        self.data_file=self.comboBox_3.currentText()
        self.loss=self.comboBox_5.currentText()
        self.epoch=int(self.comboBox.currentText())
        self.optimizer=self.comboBox_4.currentText()
        self.train_flag=self.checkBox.isChecked()
        Faclist=[self.train_flag,self.model_name,self.data_file,self.optimizer,self.loss,self.epoch]
        # self.send_value.emit(Faclist)
        print(Faclist)

        Model(Faclist)


    def find_model(self):
        self.model_name=self.lineEdit.text()+'.h5'
        if self.model_name in os.listdir('./model_file'):
            self.pushButton.setText('存在')
        else:
            self.pushButton.setText('不存在')

    def printf(self, mypstr):

        self.textBrowser.append(mypstr)  # 在指定的区域显示提示信息
        self.cursor = self.textBrowser.textCursor()
        self.textBrowser.moveCursor(self.cursor.End)  # 光标移到最后，这样就会自动显示出来
        QtWidgets.QApplication.processEvents()  # 一定加上这个功能，不然有卡顿


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        for index,filename in enumerate(os.listdir('./data')):
            self.comboBox_3.setItemText(index, _translate("Dialog", filename))
        self.comboBox_4.setItemText(0, _translate("Dialog", "Adam"))
        self.comboBox_4.setItemText(1, _translate("Dialog", "RMSprop"))
        self.comboBox_4.setItemText(2, _translate("Dialog", "Adagrad"))
        self.comboBox_4.setItemText(3, _translate("Dialog", "Adadelta"))
        self.comboBox_4.setItemText(4, _translate("Dialog", "SGD"))
        self.comboBox_4.setItemText(5, _translate("Dialog", "Adamax"))
        self.comboBox_4.setItemText(6, _translate("Dialog", "Nadam"))
        self.label_6.setText(_translate("Dialog", "损失函数"))
        self.label_4.setText(_translate("Dialog", "选择数据文件"))
        self.label_5.setText(_translate("Dialog", "优化器"))
        self.label.setText(_translate("Dialog", "模型名称"))
        self.lineEdit.setText(_translate("Dialog", "my_model0"))
        self.comboBox_5.setItemText(0, _translate("Dialog", "mean_squared_error"))
        self.comboBox_5.setItemText(1, _translate("Dialog", "mean_absolute_error"))
        self.comboBox_5.setItemText(2, _translate("Dialog", "mean_absolute_percentage_error"))
        self.comboBox_5.setItemText(3, _translate("Dialog", "mean_squared_logarithmic_error"))
        self.comboBox_5.setItemText(4, _translate("Dialog", "squared_hinge"))
        self.comboBox_5.setItemText(5, _translate("Dialog", "hinge"))
        self.comboBox_5.setItemText(6, _translate("Dialog", "categorical_hinge"))
        self.comboBox_5.setItemText(7, _translate("Dialog", "logcosh"))
        self.label_3.setText(_translate("Dialog", "训练次数"))
        self.comboBox.setItemText(0, _translate("Dialog", "5000"))
        self.comboBox.setItemText(1, _translate("Dialog", "10000"))
        self.comboBox.setItemText(2, _translate("Dialog", "20000"))
        self.comboBox.setItemText(3, _translate("Dialog", "50000"))
        self.pushButton.setText(_translate("Dialog", "检测"))
        self.title.setText(_translate("Dialog", "LSTM模型"))
        self.label_7.setText(_translate("Dialog", "程序输出"))
        self.checkBox.setText(_translate("Dialog", "训练新的模型"))
        self.pushButton_2.setText(_translate("Dialog", "开始训练"))
        self.pushButton_3.setText(_translate("Dialog", "取消"))

class MyWindow(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        # self.ex=Ui_Dialog
        self.setupUi(self)
        print('加载完毕')

        # 由于UI_window的结构的特殊，参数传不出来，很气
        # 没有__init__函数
        # self.ex.send_value.connect(self.rec_data)

    def rec_data(self,Fac_list):
        print('a====',Fac_list)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())