# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Settings.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDial,
    QFormLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpinBox, QWidget)
import resource_rc

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(500, 400)
        icon = QIcon()
        icon.addFile(u":/new/prefix1/images/pcb.ico", QSize(), QIcon.Normal, QIcon.Off)
        Settings.setWindowIcon(icon)
        self.formLayout_2 = QFormLayout(Settings)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_port = QLabel(Settings)
        self.label_port.setObjectName(u"label_port")
        font = QFont()
        font.setPointSize(11)
        self.label_port.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_port)

        self.lineEdit_port = QLineEdit(Settings)
        self.lineEdit_port.setObjectName(u"lineEdit_port")
        self.lineEdit_port.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_port)

        self.label_serial = QLabel(Settings)
        self.label_serial.setObjectName(u"label_serial")
        self.label_serial.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_serial)

        self.lineEdit_serial = QLineEdit(Settings)
        self.lineEdit_serial.setObjectName(u"lineEdit_serial")
        self.lineEdit_serial.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_serial)

        self.label_chip = QLabel(Settings)
        self.label_chip.setObjectName(u"label_chip")
        self.label_chip.setFont(font)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_chip)

        self.comboBox_chip = QComboBox(Settings)
        self.comboBox_chip.setObjectName(u"comboBox_chip")
        self.comboBox_chip.setFont(font)
        self.comboBox_chip.setFrame(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboBox_chip)

        self.checkBox_connect = QCheckBox(Settings)
        self.checkBox_connect.setObjectName(u"checkBox_connect")
        self.checkBox_connect.setFont(font)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.checkBox_connect)

        self.checkBox_logon = QCheckBox(Settings)
        self.checkBox_logon.setObjectName(u"checkBox_logon")
        self.checkBox_logon.setFont(font)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.checkBox_logon)

        self.checkBox_debug = QCheckBox(Settings)
        self.checkBox_debug.setObjectName(u"checkBox_debug")
        self.checkBox_debug.setFont(font)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.checkBox_debug)

        self.checkBox_test = QCheckBox(Settings)
        self.checkBox_test.setObjectName(u"checkBox_test")
        self.checkBox_test.setFont(font)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.checkBox_test)

        self.label_2 = QLabel(Settings)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_2)

        self.spinBox_arduino_id = QSpinBox(Settings)
        self.spinBox_arduino_id.setObjectName(u"spinBox_arduino_id")
        self.spinBox_arduino_id.setFont(font)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.spinBox_arduino_id)

        self.pushButton_save = QPushButton(Settings)
        self.pushButton_save.setObjectName(u"pushButton_save")
        self.pushButton_save.setFont(font)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.pushButton_save)

        self.label_speed = QLabel(Settings)
        self.label_speed.setObjectName(u"label_speed")
        self.label_speed.setFont(font)

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.label_speed)

        self.dial = QDial(Settings)
        self.dial.setObjectName(u"dial")
        self.dial.setFont(font)
        self.dial.setMinimum(10)
        self.dial.setMaximum(225)
        self.dial.setValue(50)
        self.dial.setOrientation(Qt.Horizontal)
        self.dial.setInvertedAppearance(True)
        self.dial.setInvertedControls(False)
        self.dial.setNotchesVisible(True)

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.dial)

        self.label = QLabel(Settings)
        self.label.setObjectName(u"label")
        self.label.setFont(font)

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label)


        self.formLayout_2.setLayout(0, QFormLayout.SpanningRole, self.formLayout)


        self.retranslateUi(Settings)

        self.comboBox_chip.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Modify Settings", None))
        self.label_port.setText(QCoreApplication.translate("Settings", u"SerialPort", None))
        self.label_serial.setText(QCoreApplication.translate("Settings", u"Pgmr Serial", None))
        self.label_chip.setText(QCoreApplication.translate("Settings", u"Chip", None))
        self.checkBox_connect.setText(QCoreApplication.translate("Settings", u"Auto Connect", None))
        self.checkBox_logon.setText(QCoreApplication.translate("Settings", u"Auto Login", None))
        self.checkBox_debug.setText(QCoreApplication.translate("Settings", u"Debug", None))
        self.checkBox_test.setText(QCoreApplication.translate("Settings", u"Auto Test", None))
        self.label_2.setText(QCoreApplication.translate("Settings", u"Arduino ID", None))
        self.pushButton_save.setText(QCoreApplication.translate("Settings", u"Save", None))
        self.label_speed.setText(QCoreApplication.translate("Settings", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("Settings", u"Test Speed", None))
    # retranslateUi

