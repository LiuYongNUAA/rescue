# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'planeposition.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_planeposition(object):
    def setupUi(self, planeposition):
        planeposition.setObjectName(_fromUtf8("planeposition"))
        planeposition.resize(300, 239)
        planeposition.setMaximumSize(QtCore.QSize(300, 239))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/新前缀/resource/point_128px_1176459_easyicon.net.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        planeposition.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(planeposition)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_15 = QtGui.QLabel(planeposition)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.horizontalLayout_2.addWidget(self.label_15)
        self.ppweidu1spinBox = QtGui.QSpinBox(planeposition)
        self.ppweidu1spinBox.setMinimumSize(QtCore.QSize(56, 0))
        self.ppweidu1spinBox.setMaximum(89)
        self.ppweidu1spinBox.setObjectName(_fromUtf8("ppweidu1spinBox"))
        self.horizontalLayout_2.addWidget(self.ppweidu1spinBox)
        self.ppweidu2spinBox = QtGui.QSpinBox(planeposition)
        self.ppweidu2spinBox.setMaximum(59)
        self.ppweidu2spinBox.setObjectName(_fromUtf8("ppweidu2spinBox"))
        self.horizontalLayout_2.addWidget(self.ppweidu2spinBox)
        self.ppweidu3spinBox = QtGui.QDoubleSpinBox(planeposition)
        self.ppweidu3spinBox.setMinimumSize(QtCore.QSize(70, 0))
        self.ppweidu3spinBox.setPrefix(_fromUtf8(""))
        self.ppweidu3spinBox.setDecimals(2)
        self.ppweidu3spinBox.setMaximum(60.0)
        self.ppweidu3spinBox.setObjectName(_fromUtf8("ppweidu3spinBox"))
        self.horizontalLayout_2.addWidget(self.ppweidu3spinBox)
        self.ppweiducomboBox = QtGui.QComboBox(planeposition)
        self.ppweiducomboBox.setObjectName(_fromUtf8("ppweiducomboBox"))
        self.ppweiducomboBox.addItem(_fromUtf8(""))
        self.ppweiducomboBox.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.ppweiducomboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_16 = QtGui.QHBoxLayout()
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.label_16 = QtGui.QLabel(planeposition)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.horizontalLayout_16.addWidget(self.label_16)
        self.ppweidudoubleSpinBox = QtGui.QDoubleSpinBox(planeposition)
        self.ppweidudoubleSpinBox.setPrefix(_fromUtf8(""))
        self.ppweidudoubleSpinBox.setDecimals(5)
        self.ppweidudoubleSpinBox.setMaximum(90.0)
        self.ppweidudoubleSpinBox.setSingleStep(1e-05)
        self.ppweidudoubleSpinBox.setObjectName(_fromUtf8("ppweidudoubleSpinBox"))
        self.horizontalLayout_16.addWidget(self.ppweidudoubleSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_16)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_13 = QtGui.QLabel(planeposition)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout.addWidget(self.label_13)
        self.ppjindu1spinBox = QtGui.QSpinBox(planeposition)
        self.ppjindu1spinBox.setMinimumSize(QtCore.QSize(56, 0))
        self.ppjindu1spinBox.setMaximum(179)
        self.ppjindu1spinBox.setObjectName(_fromUtf8("ppjindu1spinBox"))
        self.horizontalLayout.addWidget(self.ppjindu1spinBox)
        self.ppjindu2spinBox = QtGui.QSpinBox(planeposition)
        self.ppjindu2spinBox.setMaximum(59)
        self.ppjindu2spinBox.setObjectName(_fromUtf8("ppjindu2spinBox"))
        self.horizontalLayout.addWidget(self.ppjindu2spinBox)
        self.ppjindu3spinBox = QtGui.QDoubleSpinBox(planeposition)
        self.ppjindu3spinBox.setMinimumSize(QtCore.QSize(70, 0))
        self.ppjindu3spinBox.setPrefix(_fromUtf8(""))
        self.ppjindu3spinBox.setDecimals(2)
        self.ppjindu3spinBox.setMaximum(60.0)
        self.ppjindu3spinBox.setObjectName(_fromUtf8("ppjindu3spinBox"))
        self.horizontalLayout.addWidget(self.ppjindu3spinBox)
        self.ppjinducomboBox = QtGui.QComboBox(planeposition)
        self.ppjinducomboBox.setObjectName(_fromUtf8("ppjinducomboBox"))
        self.ppjinducomboBox.addItem(_fromUtf8(""))
        self.ppjinducomboBox.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.ppjinducomboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.label_14 = QtGui.QLabel(planeposition)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.horizontalLayout_14.addWidget(self.label_14)
        self.ppjindudoubleSpinBox = QtGui.QDoubleSpinBox(planeposition)
        self.ppjindudoubleSpinBox.setPrefix(_fromUtf8(""))
        self.ppjindudoubleSpinBox.setDecimals(5)
        self.ppjindudoubleSpinBox.setMaximum(180.0)
        self.ppjindudoubleSpinBox.setSingleStep(1e-05)
        self.ppjindudoubleSpinBox.setObjectName(_fromUtf8("ppjindudoubleSpinBox"))
        self.horizontalLayout_14.addWidget(self.ppjindudoubleSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_17 = QtGui.QHBoxLayout()
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        self.ppokpushButton = QtGui.QPushButton(planeposition)
        self.ppokpushButton.setObjectName(_fromUtf8("ppokpushButton"))
        self.horizontalLayout_17.addWidget(self.ppokpushButton)
        self.ppcancelpushButton = QtGui.QPushButton(planeposition)
        self.ppcancelpushButton.setObjectName(_fromUtf8("ppcancelpushButton"))
        self.horizontalLayout_17.addWidget(self.ppcancelpushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_17)

        self.retranslateUi(planeposition)
        QtCore.QMetaObject.connectSlotsByName(planeposition)

    def retranslateUi(self, planeposition):
        planeposition.setWindowTitle(_translate("planeposition", "遇难位置", None))
        self.label_15.setText(_translate("planeposition", "纬度：", None))
        self.ppweidu1spinBox.setSuffix(_translate("planeposition", "°", None))
        self.ppweidu2spinBox.setSuffix(_translate("planeposition", "\'", None))
        self.ppweidu3spinBox.setSuffix(_translate("planeposition", "\'\'", None))
        self.ppweiducomboBox.setItemText(0, _translate("planeposition", "N", None))
        self.ppweiducomboBox.setItemText(1, _translate("planeposition", "S", None))
        self.label_16.setText(_translate("planeposition", "或为四位小数：", None))
        self.ppweidudoubleSpinBox.setSuffix(_translate("planeposition", "°", None))
        self.label_13.setText(_translate("planeposition", "经度：", None))
        self.ppjindu1spinBox.setSuffix(_translate("planeposition", "°", None))
        self.ppjindu2spinBox.setSuffix(_translate("planeposition", "\'", None))
        self.ppjindu3spinBox.setSuffix(_translate("planeposition", "\'\'", None))
        self.ppjinducomboBox.setItemText(0, _translate("planeposition", "E", None))
        self.ppjinducomboBox.setItemText(1, _translate("planeposition", "W", None))
        self.label_14.setText(_translate("planeposition", "或为四位小数：", None))
        self.ppjindudoubleSpinBox.setSuffix(_translate("planeposition", "°", None))
        self.ppokpushButton.setText(_translate("planeposition", "确定", None))
        self.ppcancelpushButton.setText(_translate("planeposition", "取消", None))

import tubiao_rc
