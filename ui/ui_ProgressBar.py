# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ProgressBar.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QProgressBar,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_ProgressBar(object):
    def setupUi(self, ProgressBar):
        if not ProgressBar.objectName():
            ProgressBar.setObjectName(u"ProgressBar")
        ProgressBar.resize(300, 85)
        ProgressBar.setMinimumSize(QSize(300, 50))
        ProgressBar.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(ProgressBar)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(ProgressBar)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignHCenter|Qt.AlignTop)
        self.label.setWordWrap(False)
        self.label.setMargin(-1)
        self.label.setTextInteractionFlags(Qt.NoTextInteraction)

        self.verticalLayout.addWidget(self.label)

        self.progressBar = QProgressBar(ProgressBar)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(0, 30))
        self.progressBar.setValue(24)

        self.verticalLayout.addWidget(self.progressBar)


        self.retranslateUi(ProgressBar)

        QMetaObject.connectSlotsByName(ProgressBar)
    # setupUi

    def retranslateUi(self, ProgressBar):
        ProgressBar.setWindowTitle("")
        self.label.setText(QCoreApplication.translate("ProgressBar", u"Saving Log Data", None))
    # retranslateUi

