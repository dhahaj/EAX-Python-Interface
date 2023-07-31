# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LoginDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractButton,
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
import resource_rc
import icons_rc


class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        if not LoginDialog.objectName():
            LoginDialog.setObjectName("LoginDialog")
        LoginDialog.setWindowModality(Qt.ApplicationModal)
        LoginDialog.resize(395, 150)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoginDialog.sizePolicy().hasHeightForWidth())
        LoginDialog.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(
            ":/resources/icons/images/icons/windows.ico",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        LoginDialog.setWindowIcon(icon)
        LoginDialog.setModal(True)
        self.verticalLayout = QVBoxLayout(LoginDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setVerticalSpacing(20)
        self.gridLayout.setContentsMargins(-1, 10, -1, -1)
        self.lineEdit_password = QLineEdit(LoginDialog)
        self.lineEdit_password.setObjectName("lineEdit_password")
        font = QFont()
        font.setPointSize(11)
        self.lineEdit_password.setFont(font)

        self.gridLayout.addWidget(self.lineEdit_password, 1, 1, 1, 1)

        self.label_2 = QLabel(LoginDialog)
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.label = QLabel(LoginDialog)
        self.label.setObjectName("label")
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.comboBox = QComboBox(LoginDialog)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setFont(font)

        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.buttonBox = QDialogButtonBox(LoginDialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox, 0, Qt.AlignBottom)

        self.retranslateUi(LoginDialog)
        self.buttonBox.accepted.connect(LoginDialog.accept)
        self.buttonBox.rejected.connect(LoginDialog.reject)

        QMetaObject.connectSlotsByName(LoginDialog)

    # setupUi

    def retranslateUi(self, LoginDialog):
        LoginDialog.setWindowTitle(
            QCoreApplication.translate("LoginDialog", "Login", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("LoginDialog", "Password", None)
        )
        self.label.setText(QCoreApplication.translate("LoginDialog", "Username", None))

    # retranslateUi
