# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'RemoveUserDialog.ui'
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
    QLabel,
    QSizePolicy,
    QWidget,
)
import resource_rc
import icons_rc


class Ui_RemoveUserDialog(object):
    def setupUi(self, RemoveUserDialog):
        if not RemoveUserDialog.objectName():
            RemoveUserDialog.setObjectName("RemoveUserDialog")
        RemoveUserDialog.resize(390, 134)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(RemoveUserDialog.sizePolicy().hasHeightForWidth())
        RemoveUserDialog.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(
            ":/resources/icons/images/icons/logout.png",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        RemoveUserDialog.setWindowIcon(icon)
        self.buttonBox = QDialogButtonBox(RemoveUserDialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setGeometry(QRect(220, 80, 156, 28))
        font = QFont()
        font.setPointSize(11)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.label = QLabel(RemoveUserDialog)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(30, 30, 67, 20))
        self.label.setFont(font)
        self.comboBox = QComboBox(RemoveUserDialog)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setGeometry(QRect(117, 30, 261, 21))
        self.comboBox.setFont(font)

        self.retranslateUi(RemoveUserDialog)
        self.buttonBox.accepted.connect(RemoveUserDialog.accept)
        self.buttonBox.rejected.connect(RemoveUserDialog.reject)

        QMetaObject.connectSlotsByName(RemoveUserDialog)

    # setupUi

    def retranslateUi(self, RemoveUserDialog):
        RemoveUserDialog.setWindowTitle(
            QCoreApplication.translate("RemoveUserDialog", "Dialog", None)
        )
        self.label.setText(
            QCoreApplication.translate("RemoveUserDialog", "Username", None)
        )

    # retranslateUi
