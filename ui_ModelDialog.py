# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ModelDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QGroupBox, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_ModelDialog(object):
    def setupUi(self, ModelDialog):
        if not ModelDialog.objectName():
            ModelDialog.setObjectName(u"ModelDialog")
        ModelDialog.resize(349, 140)
        ModelDialog.setMaximumSize(QSize(350, 140))
        self.verticalLayout_2 = QVBoxLayout(ModelDialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox = QGroupBox(ModelDialog)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(150, 0))
        self.comboBox.setFont(font)

        self.verticalLayout.addWidget(self.comboBox)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.buttonBox = QDialogButtonBox(ModelDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout_2.addWidget(self.buttonBox)


        self.retranslateUi(ModelDialog)
        self.buttonBox.accepted.connect(ModelDialog.accept)
        self.buttonBox.rejected.connect(ModelDialog.reject)

        QMetaObject.connectSlotsByName(ModelDialog)
    # setupUi

    def retranslateUi(self, ModelDialog):
        ModelDialog.setWindowTitle(QCoreApplication.translate("ModelDialog", u"Select Model", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("ModelDialog", u"Select an option", None))
    # retranslateUi

