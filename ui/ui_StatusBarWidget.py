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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLCDNumber,
    QLabel, QLayout, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_StatusBarWidget(object):
    def setupUi(self, StatusBarWidget):
        if not StatusBarWidget.objectName():
            StatusBarWidget.setObjectName(u"StatusBarWidget")
        StatusBarWidget.resize(1100, 24)
        StatusBarWidget.setMaximumSize(QSize(16777215, 24))
        self.horizontalLayout = QHBoxLayout(StatusBarWidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetNoConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
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

        self.horizontalLayout.addWidget(self.status)

        self.horizontalSpacer = QSpacerItem(931, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.label = QLabel(StatusBarWidget)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label.setMargin(2)

        self.horizontalLayout.addWidget(self.label)

        self.lcdNumber = QLCDNumber(StatusBarWidget)
        self.lcdNumber.setObjectName(u"lcdNumber")
        sizePolicy1.setHeightForWidth(self.lcdNumber.sizePolicy().hasHeightForWidth())
        self.lcdNumber.setSizePolicy(sizePolicy1)
        self.lcdNumber.setMinimumSize(QSize(46, 0))
        self.lcdNumber.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.lcdNumber.setAutoFillBackground(False)
        self.lcdNumber.setStyleSheet(u"")
        self.lcdNumber.setFrameShape(QFrame.Shape.NoFrame)
        self.lcdNumber.setDigitCount(3)
        self.lcdNumber.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.lcdNumber.setProperty(u"intValue", 0)

        self.horizontalLayout.addWidget(self.lcdNumber)


        self.retranslateUi(StatusBarWidget)

        QMetaObject.connectSlotsByName(StatusBarWidget)
    # setupUi

    def retranslateUi(self, StatusBarWidget):
        StatusBarWidget.setWindowTitle(QCoreApplication.translate("StatusBarWidget", u"Form", None))
        self.status.setText(QCoreApplication.translate("StatusBarWidget", u"TextLabel", None))
        self.label.setText(QCoreApplication.translate("StatusBarWidget", u"Counter", None))
    # retranslateUi

