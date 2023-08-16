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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QProgressBar,
    QSizePolicy, QWidget)

class Ui_ProgressBar(object):
    def setupUi(self, ProgressBar):
        if not ProgressBar.objectName():
            ProgressBar.setObjectName(u"ProgressBar")
        ProgressBar.resize(300, 50)
        ProgressBar.setMinimumSize(QSize(300, 50))
        ProgressBar.setMaximumSize(QSize(300, 50))
        self.horizontalLayout = QHBoxLayout(ProgressBar)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.progressBar = QProgressBar(ProgressBar)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(0, 30))
        self.progressBar.setValue(24)

        self.horizontalLayout.addWidget(self.progressBar)


        self.retranslateUi(ProgressBar)

        QMetaObject.connectSlotsByName(ProgressBar)
    # setupUi

    def retranslateUi(self, ProgressBar):
        ProgressBar.setWindowTitle("")
    # retranslateUi

