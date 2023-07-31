# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ManualControlDialog.ui'
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
    QApplication,
    QDialog,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
import resource_rc
import icons_rc


class Ui_ManualControlDialog(object):
    def setupUi(self, ManualControlDialog):
        if not ManualControlDialog.objectName():
            ManualControlDialog.setObjectName("ManualControlDialog")
        ManualControlDialog.resize(316, 466)
        icon = QIcon()
        icon.addFile(
            ":/resources/icons/images/icons/plug.png", QSize(), QIcon.Normal, QIcon.Off
        )
        ManualControlDialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(ManualControlDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.battery_button = QPushButton(ManualControlDialog)
        self.battery_button.setObjectName("battery_button")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(
            self.battery_button.sizePolicy().hasHeightForWidth()
        )
        self.battery_button.setSizePolicy(sizePolicy)
        self.battery_button.setMinimumSize(QSize(10, 10))
        font = QFont()
        font.setPointSize(16)
        self.battery_button.setFont(font)
        self.battery_button.setCheckable(True)
        self.battery_button.setChecked(False)
        self.battery_button.setAutoExclusive(False)
        self.battery_button.setFlat(False)

        self.verticalLayout.addWidget(self.battery_button)

        self.low_battery_button = QPushButton(ManualControlDialog)
        self.low_battery_button.setObjectName("low_battery_button")
        sizePolicy.setHeightForWidth(
            self.low_battery_button.sizePolicy().hasHeightForWidth()
        )
        self.low_battery_button.setSizePolicy(sizePolicy)
        self.low_battery_button.setMinimumSize(QSize(10, 10))
        self.low_battery_button.setFont(font)
        self.low_battery_button.setCheckable(True)
        self.low_battery_button.setChecked(False)
        self.low_battery_button.setAutoExclusive(False)
        self.low_battery_button.setFlat(False)

        self.verticalLayout.addWidget(self.low_battery_button)

        self.test_indicator_button = QPushButton(ManualControlDialog)
        self.test_indicator_button.setObjectName("test_indicator_button")
        sizePolicy.setHeightForWidth(
            self.test_indicator_button.sizePolicy().hasHeightForWidth()
        )
        self.test_indicator_button.setSizePolicy(sizePolicy)
        self.test_indicator_button.setMinimumSize(QSize(10, 10))
        self.test_indicator_button.setFont(font)
        self.test_indicator_button.setCheckable(True)
        self.test_indicator_button.setChecked(False)
        self.test_indicator_button.setAutoExclusive(False)
        self.test_indicator_button.setFlat(False)

        self.verticalLayout.addWidget(self.test_indicator_button)

        self.indicator_button = QPushButton(ManualControlDialog)
        self.indicator_button.setObjectName("indicator_button")
        sizePolicy.setHeightForWidth(
            self.indicator_button.sizePolicy().hasHeightForWidth()
        )
        self.indicator_button.setSizePolicy(sizePolicy)
        self.indicator_button.setMinimumSize(QSize(10, 10))
        self.indicator_button.setFont(font)
        self.indicator_button.setCheckable(True)
        self.indicator_button.setChecked(False)
        self.indicator_button.setAutoExclusive(False)
        self.indicator_button.setFlat(False)

        self.verticalLayout.addWidget(self.indicator_button)

        self.retranslateUi(ManualControlDialog)

        self.battery_button.setDefault(False)
        self.low_battery_button.setDefault(False)
        self.test_indicator_button.setDefault(False)
        self.indicator_button.setDefault(False)

        QMetaObject.connectSlotsByName(ManualControlDialog)

    # setupUi

    def retranslateUi(self, ManualControlDialog):
        ManualControlDialog.setWindowTitle(
            QCoreApplication.translate("ManualControlDialog", "Manual Control", None)
        )
        self.battery_button.setText(
            QCoreApplication.translate("ManualControlDialog", "Battery", None)
        )
        self.low_battery_button.setText(
            QCoreApplication.translate("ManualControlDialog", "Low Battery", None)
        )
        self.test_indicator_button.setText(
            QCoreApplication.translate("ManualControlDialog", "Test Indicator", None)
        )
        self.indicator_button.setText(
            QCoreApplication.translate("ManualControlDialog", "Indicator", None)
        )

    # retranslateUi
