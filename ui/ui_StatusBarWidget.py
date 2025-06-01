# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'StatusBarWidget.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QLCDNumber,
    QLabel, QLayout, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_StatusBarWidget(object):
    def setupUi(self, StatusBarWidget):
        if not StatusBarWidget.objectName():
            StatusBarWidget.setObjectName(u"StatusBarWidget")
        StatusBarWidget.resize(1142, 24)
        StatusBarWidget.setMaximumSize(QSize(16777215, 24))
        self.gridLayout = QGridLayout(StatusBarWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.progLcd = QLCDNumber(StatusBarWidget)
        self.progLcd.setObjectName(u"progLcd")
        self.progLcd.setMinimumSize(QSize(46, 0))
        self.progLcd.setFrameShape(QFrame.Shape.NoFrame)
        self.progLcd.setFrameShadow(QFrame.Shadow.Plain)
        self.progLcd.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)

        self.gridLayout.addWidget(self.progLcd, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(931, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 1, 1, 1)

        self.status = QLabel(StatusBarWidget)
        self.status.setObjectName(u"status")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(11)
        self.status.setFont(font)

        self.gridLayout.addWidget(self.status, 0, 0, 1, 1)

        self.lcdNumber = QLCDNumber(StatusBarWidget)
        self.lcdNumber.setObjectName(u"lcdNumber")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lcdNumber.sizePolicy().hasHeightForWidth())
        self.lcdNumber.setSizePolicy(sizePolicy1)
        self.lcdNumber.setMinimumSize(QSize(46, 0))
        self.lcdNumber.setFont(font)
        self.lcdNumber.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lcdNumber.setAutoFillBackground(False)
        self.lcdNumber.setStyleSheet(u"")
        self.lcdNumber.setFrameShape(QFrame.Shape.NoFrame)
        self.lcdNumber.setFrameShadow(QFrame.Shadow.Plain)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setDigitCount(5)
        self.lcdNumber.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.lcdNumber.setProperty(u"value", 0.000000000000000)

        self.gridLayout.addWidget(self.lcdNumber, 0, 3, 1, 1)


        self.retranslateUi(StatusBarWidget)

        QMetaObject.connectSlotsByName(StatusBarWidget)
    # setupUi

    def retranslateUi(self, StatusBarWidget):
        StatusBarWidget.setWindowTitle(QCoreApplication.translate("StatusBarWidget", u"Form", None))
#if QT_CONFIG(tooltip)
        self.progLcd.setToolTip(QCoreApplication.translate("StatusBarWidget", u"Program Counter", None))
#endif // QT_CONFIG(tooltip)
        self.status.setText(QCoreApplication.translate("StatusBarWidget", u"TextLabel", None))
#if QT_CONFIG(tooltip)
        self.lcdNumber.setToolTip(QCoreApplication.translate("StatusBarWidget", u"Test Counter", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

