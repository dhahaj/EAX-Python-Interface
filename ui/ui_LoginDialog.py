# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoginDialog.ui'
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
    QDialogButtonBox, QGridLayout, QLabel, QLineEdit,
    QSizePolicy, QWidget)
import resource_rc
import icons_rc

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        if not LoginDialog.objectName():
            LoginDialog.setObjectName(u"LoginDialog")
        LoginDialog.setWindowModality(Qt.ApplicationModal)
        LoginDialog.resize(350, 140)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoginDialog.sizePolicy().hasHeightForWidth())
        LoginDialog.setSizePolicy(sizePolicy)
        LoginDialog.setMinimumSize(QSize(350, 140))
        LoginDialog.setMaximumSize(QSize(350, 140))
        LoginDialog.setContextMenuPolicy(Qt.ActionsContextMenu)
        icon = QIcon()
        icon.addFile(u":/resources/icons/images/icons/windows.ico", QSize(), QIcon.Normal, QIcon.Off)
        LoginDialog.setWindowIcon(icon)
        LoginDialog.setModal(True)
        self.gridLayout = QGridLayout(LoginDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(LoginDialog)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.comboBox = QComboBox(LoginDialog)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(0, 30))
        self.comboBox.setFont(font)

        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)

        self.label_2 = QLabel(LoginDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_password = QLineEdit(LoginDialog)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setMinimumSize(QSize(0, 30))
        self.lineEdit_password.setFont(font)
        self.lineEdit_password.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.lineEdit_password.setEchoMode(QLineEdit.Password)

        self.gridLayout.addWidget(self.lineEdit_password, 1, 1, 1, 1)

        self.buttonBox = QDialogButtonBox(LoginDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMinimumSize(QSize(0, 35))
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.comboBox)
        self.label_2.setBuddy(self.lineEdit_password)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.lineEdit_password, self.comboBox)

        self.retranslateUi(LoginDialog)
        self.buttonBox.accepted.connect(LoginDialog.accept)
        self.buttonBox.rejected.connect(LoginDialog.reject)

        QMetaObject.connectSlotsByName(LoginDialog)
    # setupUi

    def retranslateUi(self, LoginDialog):
        LoginDialog.setWindowTitle(QCoreApplication.translate("LoginDialog", u"Login", None))
        self.label.setText(QCoreApplication.translate("LoginDialog", u"Username", None))
        self.label_2.setText(QCoreApplication.translate("LoginDialog", u"Password", None))
    # retranslateUi

