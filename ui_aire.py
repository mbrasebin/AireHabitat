# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Aire_dialog_base.ui'
#
# Created: Wed Apr 26 11:39:56 2017
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_AirehabitatDialogBase(object):
    def setupUi(self, AirehabitatDialogBase):
        AirehabitatDialogBase.setObjectName(_fromUtf8("AirehabitatDialogBase"))
        AirehabitatDialogBase.resize(400, 300)
        self.button_box = QtGui.QDialogButtonBox(AirehabitatDialogBase)
        self.button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box.setObjectName(_fromUtf8("button_box"))
        self.couche = QtGui.QComboBox(AirehabitatDialogBase)
        self.couche.setGeometry(QtCore.QRect(100, 80, 141, 22))
        self.couche.setObjectName(_fromUtf8("couche"))
        self.operation = QtGui.QComboBox(AirehabitatDialogBase)
        self.operation.setGeometry(QtCore.QRect(100, 170, 141, 22))
        self.operation.setObjectName(_fromUtf8("operation"))
        self.label = QtGui.QLabel(AirehabitatDialogBase)
        self.label.setGeometry(QtCore.QRect(80, 50, 41, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(AirehabitatDialogBase)
        self.label_2.setGeometry(QtCore.QRect(80, 140, 61, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(AirehabitatDialogBase)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), AirehabitatDialogBase.accept)
        QtCore.QObject.connect(self.button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), AirehabitatDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(AirehabitatDialogBase)

    def retranslateUi(self, AirehabitatDialogBase):
        AirehabitatDialogBase.setWindowTitle(_translate("AirehabitatDialogBase", "Aire habitat", None))
        self.label.setText(_translate("AirehabitatDialogBase", "Couche", None))
        self.label_2.setText(_translate("AirehabitatDialogBase", "Opération", None))

