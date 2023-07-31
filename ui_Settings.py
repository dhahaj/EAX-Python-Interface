# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Settings.ui'
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
    QCheckBox,
    QComboBox,
    QCommandLinkButton,
    QDial,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLCDNumber,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)
import resource_rc
import icons_rc


class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName("Settings")
        Settings.resize(475, 466)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Settings.sizePolicy().hasHeightForWidth())
        Settings.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(
            ":/resources/icons/images/icons/settings3.png",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        Settings.setWindowIcon(icon)
        self.groupBox = QGroupBox(Settings)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setGeometry(QRect(8, 8, 220, 50))
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QSize(220, 50))
        self.groupBox.setMaximumSize(QSize(220, 50))
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_port = QLabel(self.groupBox)
        self.label_port.setObjectName("label_port")
        font = QFont()
        font.setPointSize(11)
        self.label_port.setFont(font)

        self.horizontalLayout.addWidget(self.label_port)

        self.comboBox_com_port = QComboBox(self.groupBox)
        self.comboBox_com_port.setObjectName("comboBox_com_port")
        sizePolicy.setHeightForWidth(
            self.comboBox_com_port.sizePolicy().hasHeightForWidth()
        )
        self.comboBox_com_port.setSizePolicy(sizePolicy)
        self.comboBox_com_port.setMinimumSize(QSize(130, 0))
        self.comboBox_com_port.setFont(font)
        self.comboBox_com_port.setEditable(True)

        self.horizontalLayout.addWidget(self.comboBox_com_port)

        self.groupBox_2 = QGroupBox(Settings)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 118, 220, 50))
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
        self.groupBox_2.setMinimumSize(QSize(220, 50))
        self.groupBox_2.setMaximumSize(QSize(220, 50))
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_serial = QLabel(self.groupBox_2)
        self.label_serial.setObjectName("label_serial")
        self.label_serial.setFont(font)

        self.horizontalLayout_2.addWidget(self.label_serial)

        self.lineEdit_serial = QLineEdit(self.groupBox_2)
        self.lineEdit_serial.setObjectName("lineEdit_serial")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(
            self.lineEdit_serial.sizePolicy().hasHeightForWidth()
        )
        self.lineEdit_serial.setSizePolicy(sizePolicy2)
        self.lineEdit_serial.setMinimumSize(QSize(100, 0))
        self.lineEdit_serial.setFont(font)

        self.horizontalLayout_2.addWidget(self.lineEdit_serial)

        self.groupBox_3 = QGroupBox(Settings)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 62, 220, 50))
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QSize(220, 50))
        self.groupBox_3.setMaximumSize(QSize(220, 50))
        self.horizontalLayout_3 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_chip = QLabel(self.groupBox_3)
        self.label_chip.setObjectName("label_chip")
        self.label_chip.setFont(font)

        self.horizontalLayout_3.addWidget(self.label_chip)

        self.comboBox_chip = QComboBox(self.groupBox_3)
        self.comboBox_chip.setObjectName("comboBox_chip")
        self.comboBox_chip.setMinimumSize(QSize(150, 0))
        self.comboBox_chip.setFont(font)
        self.comboBox_chip.setEditable(False)
        self.comboBox_chip.setFrame(True)

        self.horizontalLayout_3.addWidget(self.comboBox_chip)

        self.groupBox_7 = QGroupBox(Settings)
        self.groupBox_7.setObjectName("groupBox_7")
        self.groupBox_7.setGeometry(QRect(10, 174, 215, 48))
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox_7)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QLabel(self.groupBox_7)
        self.label_4.setObjectName("label_4")
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.label_4.setMargin(4)

        self.horizontalLayout_4.addWidget(self.label_4)

        self.spinBox_autologoff_delay = QSpinBox(self.groupBox_7)
        self.spinBox_autologoff_delay.setObjectName("spinBox_autologoff_delay")
        self.spinBox_autologoff_delay.setMinimumSize(QSize(50, 0))
        self.spinBox_autologoff_delay.setMaximumSize(QSize(50, 16777215))
        self.spinBox_autologoff_delay.setFont(font)
        self.spinBox_autologoff_delay.setProperty("showGroupSeparator", False)
        self.spinBox_autologoff_delay.setMinimum(1)

        self.horizontalLayout_4.addWidget(self.spinBox_autologoff_delay)

        self.groupBox_4 = QGroupBox(Settings)
        self.groupBox_4.setObjectName("groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 226, 175, 50))
        self.label_2 = QLabel(self.groupBox_4)
        self.label_2.setObjectName("label_2")
        self.label_2.setGeometry(QRect(10, 10, 85, 30))
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)
        self.label_2.setMargin(5)
        self.spinBox_arduino_id = QSpinBox(self.groupBox_4)
        self.spinBox_arduino_id.setObjectName("spinBox_arduino_id")
        self.spinBox_arduino_id.setGeometry(QRect(101, 12, 60, 25))
        self.spinBox_arduino_id.setMinimumSize(QSize(60, 0))
        self.spinBox_arduino_id.setMaximumSize(QSize(50, 16777215))
        self.spinBox_arduino_id.setFont(font)
        self.spinBox_arduino_id.setFocusPolicy(Qt.ClickFocus)
        self.spinBox_arduino_id.setMinimum(1)
        self.groupBox_6 = QGroupBox(Settings)
        self.groupBox_6.setObjectName("groupBox_6")
        self.groupBox_6.setGeometry(QRect(250, 14, 194, 174))
        self.verticalLayout = QVBoxLayout(self.groupBox_6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox_auto_find = QCheckBox(self.groupBox_6)
        self.checkBox_auto_find.setObjectName("checkBox_auto_find")
        self.checkBox_auto_find.setFocusPolicy(Qt.NoFocus)
        self.checkBox_auto_find.setChecked(True)

        self.verticalLayout.addWidget(self.checkBox_auto_find)

        self.checkBox_shutdown_on_exception = QCheckBox(self.groupBox_6)
        self.checkBox_shutdown_on_exception.setObjectName(
            "checkBox_shutdown_on_exception"
        )
        self.checkBox_shutdown_on_exception.setFocusPolicy(Qt.NoFocus)
        self.checkBox_shutdown_on_exception.setChecked(True)

        self.verticalLayout.addWidget(self.checkBox_shutdown_on_exception)

        self.groupBox_9 = QGroupBox(self.groupBox_6)
        self.groupBox_9.setObjectName("groupBox_9")
        self.groupBox_9.setMinimumSize(QSize(0, 40))
        self.groupBox_9.setMaximumSize(QSize(200, 40))
        self.horizontalLayout_5 = QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lineEdit_serial_sleep_tune = QLineEdit(self.groupBox_9)
        self.lineEdit_serial_sleep_tune.setObjectName("lineEdit_serial_sleep_tune")
        sizePolicy2.setHeightForWidth(
            self.lineEdit_serial_sleep_tune.sizePolicy().hasHeightForWidth()
        )
        self.lineEdit_serial_sleep_tune.setSizePolicy(sizePolicy2)
        self.lineEdit_serial_sleep_tune.setMinimumSize(QSize(50, 0))
        self.lineEdit_serial_sleep_tune.setMaximumSize(QSize(70, 150))
        self.lineEdit_serial_sleep_tune.setFont(font)

        self.horizontalLayout_5.addWidget(self.lineEdit_serial_sleep_tune)

        self.label_6 = QLabel(self.groupBox_9)
        self.label_6.setObjectName("label_6")
        self.label_6.setMargin(5)

        self.horizontalLayout_5.addWidget(self.label_6)

        self.verticalLayout.addWidget(self.groupBox_9)

        self.groupBox_8 = QGroupBox(self.groupBox_6)
        self.groupBox_8.setObjectName("groupBox_8")
        self.groupBox_8.setMinimumSize(QSize(0, 40))
        self.groupBox_8.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_8)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.spinBox_wait_time = QSpinBox(self.groupBox_8)
        self.spinBox_wait_time.setObjectName("spinBox_wait_time")
        sizePolicy1.setHeightForWidth(
            self.spinBox_wait_time.sizePolicy().hasHeightForWidth()
        )
        self.spinBox_wait_time.setSizePolicy(sizePolicy1)
        self.spinBox_wait_time.setMinimumSize(QSize(34, 25))
        self.spinBox_wait_time.setMaximumSize(QSize(65, 25))
        self.spinBox_wait_time.setFocusPolicy(Qt.ClickFocus)
        self.spinBox_wait_time.setMinimum(1)
        self.spinBox_wait_time.setMaximum(15)
        self.spinBox_wait_time.setValue(4)

        self.horizontalLayout_6.addWidget(self.spinBox_wait_time)

        self.label_5 = QLabel(self.groupBox_8)
        self.label_5.setObjectName("label_5")
        self.label_5.setMargin(5)

        self.horizontalLayout_6.addWidget(self.label_5)

        self.verticalLayout.addWidget(self.groupBox_8)

        self.commandLinkButton_select_color = QCommandLinkButton(Settings)
        self.commandLinkButton_select_color.setObjectName(
            "commandLinkButton_select_color"
        )
        self.commandLinkButton_select_color.setGeometry(QRect(250, 198, 201, 45))
        icon1 = QIcon()
        icon1.addFile(
            ":/resources/icons/images/icons/foreground-color.png",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.commandLinkButton_select_color.setIcon(icon1)
        self.commandLinkButton_select_color.setIconSize(QSize(20, 20))
        self.commandLinkButton_bg_color = QCommandLinkButton(Settings)
        self.commandLinkButton_bg_color.setObjectName("commandLinkButton_bg_color")
        self.commandLinkButton_bg_color.setGeometry(QRect(250, 248, 205, 49))
        font1 = QFont()
        font1.setFamilies(["Segoe UI"])
        font1.setPointSize(11)
        self.commandLinkButton_bg_color.setFont(font1)
        icon2 = QIcon()
        icon2.addFile(
            ":/resources/icons/images/icons/background-color.png",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.commandLinkButton_bg_color.setIcon(icon2)
        self.commandLinkButton_bg_color.setIconSize(QSize(20, 20))
        self.lcdNumber = QLCDNumber(Settings)
        self.lcdNumber.setObjectName("lcdNumber")
        self.lcdNumber.setGeometry(QRect(10, 288, 126, 56))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(255, 0, 0, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush1)
        brush2 = QBrush(QColor(255, 127, 127, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Light, brush2)
        brush3 = QBrush(QColor(255, 63, 63, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Active, QPalette.Dark, brush1)
        brush4 = QBrush(QColor(170, 0, 0, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Mid, brush4)
        palette.setBrush(QPalette.Active, QPalette.Text, brush)
        brush5 = QBrush(QColor(255, 255, 255, 255))
        brush5.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.BrightText, brush5)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush5)
        palette.setBrush(QPalette.Active, QPalette.Window, brush1)
        palette.setBrush(QPalette.Active, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Active, QPalette.AlternateBase, brush2)
        brush6 = QBrush(QColor(255, 255, 220, 255))
        brush6.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ToolTipBase, brush6)
        palette.setBrush(QPalette.Active, QPalette.ToolTipText, brush)
        brush7 = QBrush(QColor(0, 0, 0, 127))
        brush7.setStyle(Qt.SolidPattern)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Active, QPalette.PlaceholderText, brush7)
        # endif
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Light, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Inactive, QPalette.Dark, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Mid, brush4)
        palette.setBrush(QPalette.Inactive, QPalette.Text, brush)
        palette.setBrush(QPalette.Inactive, QPalette.BrightText, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush5)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush1)
        palette.setBrush(QPalette.Inactive, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Inactive, QPalette.AlternateBase, brush2)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipBase, brush6)
        palette.setBrush(QPalette.Inactive, QPalette.ToolTipText, brush)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Inactive, QPalette.PlaceholderText, brush7)
        # endif
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Light, brush2)
        palette.setBrush(QPalette.Disabled, QPalette.Midlight, brush3)
        palette.setBrush(QPalette.Disabled, QPalette.Dark, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Mid, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.BrightText, brush5)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Shadow, brush)
        palette.setBrush(QPalette.Disabled, QPalette.AlternateBase, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipBase, brush6)
        palette.setBrush(QPalette.Disabled, QPalette.ToolTipText, brush)
        brush8 = QBrush(QColor(127, 0, 0, 127))
        brush8.setStyle(Qt.SolidPattern)
        # if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.Disabled, QPalette.PlaceholderText, brush8)
        # endif
        self.lcdNumber.setPalette(palette)
        self.lcdNumber.setFrameShape(QFrame.Box)
        self.lcdNumber.setFrameShadow(QFrame.Raised)
        self.lcdNumber.setSmallDecimalPoint(True)
        self.lcdNumber.setDigitCount(4)
        self.lcdNumber.setSegmentStyle(QLCDNumber.Filled)
        self.lcdNumber.setProperty("value", 2240.000000000000000)
        self.lcdNumber.setProperty("intValue", 2240)
        self.dial = QDial(Settings)
        self.dial.setObjectName("dial")
        self.dial.setGeometry(QRect(22, 356, 116, 101))
        sizePolicy1.setHeightForWidth(self.dial.sizePolicy().hasHeightForWidth())
        self.dial.setSizePolicy(sizePolicy1)
        self.dial.setMinimumSize(QSize(50, 50))
        self.dial.setMaximumSize(QSize(120, 120))
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.Dark, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Dark, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Dark, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        self.dial.setPalette(palette1)
        self.dial.setFont(font)
        self.dial.setFocusPolicy(Qt.ClickFocus)
        self.dial.setMinimum(750)
        self.dial.setMaximum(5000)
        self.dial.setSingleStep(10)
        self.dial.setPageStep(10)
        self.dial.setValue(1700)
        self.dial.setSliderPosition(1700)
        self.dial.setOrientation(Qt.Horizontal)
        self.dial.setInvertedAppearance(True)
        self.dial.setInvertedControls(False)
        self.dial.setWrapping(False)
        self.dial.setNotchTarget(3.700000000000000)
        self.dial.setNotchesVisible(True)
        self.pushButton_save = QPushButton(Settings)
        self.pushButton_save.setObjectName("pushButton_save")
        self.pushButton_save.setGeometry(QRect(284, 410, 175, 49))
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.pushButton_save.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_save.setSizePolicy(sizePolicy3)
        self.pushButton_save.setMinimumSize(QSize(100, 0))
        self.pushButton_save.setFont(font)
        self.pushButton_save.setAutoDefault(True)
        self.groupBox_5 = QGroupBox(Settings)
        self.groupBox_5.setObjectName("groupBox_5")
        self.groupBox_5.setGeometry(QRect(228, 302, 229, 89))
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy4)
        self.groupBox_5.setMinimumSize(QSize(0, 74))
        self.groupBox_5.setLayoutDirection(Qt.LeftToRight)
        self.groupBox_5.setFlat(False)
        self.gridLayout = QGridLayout(self.groupBox_5)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_logon = QCheckBox(self.groupBox_5)
        self.checkBox_logon.setObjectName("checkBox_logon")
        self.checkBox_logon.setMinimumSize(QSize(0, 26))
        self.checkBox_logon.setFont(font)
        # if QT_CONFIG(tooltip)
        self.checkBox_logon.setToolTip("This disables logging in")
        # endif // QT_CONFIG(tooltip)

        self.gridLayout.addWidget(self.checkBox_logon, 0, 0, 1, 1)

        self.checkBox_debug = QCheckBox(self.groupBox_5)
        self.checkBox_debug.setObjectName("checkBox_debug")
        self.checkBox_debug.setMinimumSize(QSize(0, 26))
        self.checkBox_debug.setFont(font)

        self.gridLayout.addWidget(self.checkBox_debug, 0, 1, 1, 1)

        self.checkBox_connect = QCheckBox(self.groupBox_5)
        self.checkBox_connect.setObjectName("checkBox_connect")
        self.checkBox_connect.setMinimumSize(QSize(0, 26))
        self.checkBox_connect.setFont(font)

        self.gridLayout.addWidget(self.checkBox_connect, 1, 0, 1, 1)

        self.checkBox_test = QCheckBox(self.groupBox_5)
        self.checkBox_test.setObjectName("checkBox_test")
        self.checkBox_test.setMinimumSize(QSize(0, 25))
        self.checkBox_test.setFont(font)
        self.checkBox_test.setIconSize(QSize(20, 20))
        self.checkBox_test.setChecked(True)
        self.checkBox_test.setTristate(False)

        self.gridLayout.addWidget(self.checkBox_test, 1, 1, 1, 1)

        self.label = QLabel(Settings)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(140, 320, 49, 23))
        palette2 = QPalette()
        palette2.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        palette2.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        self.label.setPalette(palette2)
        font2 = QFont()
        font2.setPointSize(14)
        self.label.setFont(font2)
        self.label.setScaledContents(True)
        self.pushButton_default = QPushButton(Settings)
        self.pushButton_default.setObjectName("pushButton_default")
        self.pushButton_default.setGeometry(QRect(166, 420, 100, 37))
        sizePolicy3.setHeightForWidth(
            self.pushButton_default.sizePolicy().hasHeightForWidth()
        )
        self.pushButton_default.setSizePolicy(sizePolicy3)
        self.pushButton_default.setMinimumSize(QSize(100, 0))
        self.pushButton_default.setFont(font)
        self.pushButton_default.setFocusPolicy(Qt.NoFocus)
        # if QT_CONFIG(shortcut)
        self.label_port.setBuddy(self.comboBox_com_port)
        self.label_serial.setBuddy(self.lineEdit_serial)
        self.label_chip.setBuddy(self.comboBox_chip)
        self.label_4.setBuddy(self.spinBox_autologoff_delay)
        self.label_2.setBuddy(self.spinBox_arduino_id)
        self.label_6.setBuddy(self.spinBox_wait_time)
        self.label_5.setBuddy(self.spinBox_wait_time)
        # endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.pushButton_save, self.checkBox_test)
        QWidget.setTabOrder(self.checkBox_test, self.checkBox_debug)
        QWidget.setTabOrder(self.checkBox_debug, self.checkBox_connect)
        QWidget.setTabOrder(self.checkBox_connect, self.checkBox_logon)
        QWidget.setTabOrder(self.checkBox_logon, self.commandLinkButton_bg_color)
        QWidget.setTabOrder(
            self.commandLinkButton_bg_color, self.commandLinkButton_select_color
        )
        QWidget.setTabOrder(
            self.commandLinkButton_select_color, self.spinBox_autologoff_delay
        )
        QWidget.setTabOrder(self.spinBox_autologoff_delay, self.lineEdit_serial)
        QWidget.setTabOrder(self.lineEdit_serial, self.comboBox_chip)
        QWidget.setTabOrder(self.comboBox_chip, self.comboBox_com_port)

        self.retranslateUi(Settings)
        self.dial.valueChanged.connect(self.lcdNumber.display)

        self.comboBox_chip.setCurrentIndex(-1)
        self.pushButton_save.setDefault(True)

        QMetaObject.connectSlotsByName(Settings)

    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(
            QCoreApplication.translate("Settings", "Settings", None)
        )
        # if QT_CONFIG(tooltip)
        self.groupBox.setToolTip(
            QCoreApplication.translate(
                "Settings",
                "The USB Serial Port. It should auto populate when opening this window",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.groupBox.setTitle("")
        self.label_port.setText(
            QCoreApplication.translate("Settings", "COM Port", None)
        )
        # if QT_CONFIG(tooltip)
        self.comboBox_com_port.setToolTip(
            QCoreApplication.translate(
                "Settings",
                "The USB Serial Port. It should auto populate when opening this window",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.comboBox_com_port.setCurrentText(
            QCoreApplication.translate("Settings", "COM8", None)
        )
        # if QT_CONFIG(tooltip)
        self.groupBox_2.setToolTip(
            QCoreApplication.translate(
                "Settings",
                "The serial # of the programmer (find it using up.exe)",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.groupBox_2.setTitle("")
        self.label_serial.setText(
            QCoreApplication.translate("Settings", "Pgmr Serial", None)
        )
        # if QT_CONFIG(tooltip)
        self.groupBox_3.setToolTip(
            QCoreApplication.translate(
                "Settings", "Select the correct chip for the batch", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.groupBox_3.setTitle("")
        self.label_chip.setText(QCoreApplication.translate("Settings", "Chip", None))
        self.comboBox_chip.setCurrentText("")
        # if QT_CONFIG(tooltip)
        self.groupBox_7.setToolTip(
            QCoreApplication.translate(
                "Settings", "In minutes. (Turning on Auto Login disables this)", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.groupBox_7.setTitle("")
        self.label_4.setText(
            QCoreApplication.translate("Settings", "Auto Logoff Delay:", None)
        )
        self.spinBox_autologoff_delay.setSpecialValueText("")
        self.spinBox_autologoff_delay.setSuffix(
            QCoreApplication.translate("Settings", "m", None)
        )
        # if QT_CONFIG(tooltip)
        self.groupBox_4.setToolTip(
            QCoreApplication.translate(
                "Settings", "Allows multiple fixtures to connect to one computer", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.groupBox_4.setTitle("")
        # if QT_CONFIG(tooltip)
        self.label_2.setToolTip(
            QCoreApplication.translate(
                "Settings", "Allows multiple fixtures to connect to one computer", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_2.setText(
            QCoreApplication.translate("Settings", "Arduino ID:", None)
        )
        # if QT_CONFIG(tooltip)
        self.spinBox_arduino_id.setToolTip(
            QCoreApplication.translate(
                "Settings", "Allows multiple fixtures to connect to one computer", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.groupBox_6.setToolTip(
            QCoreApplication.translate(
                "Settings",
                "Advanced Settings. Should normally not need to adjust these.",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.groupBox_6.setTitle(
            QCoreApplication.translate("Settings", "Advanced", None)
        )
        self.checkBox_auto_find.setText(
            QCoreApplication.translate("Settings", "Auto FInd", None)
        )
        self.checkBox_shutdown_on_exception.setText(
            QCoreApplication.translate("Settings", "Shutdown on Exception", None)
        )
        # if QT_CONFIG(tooltip)
        self.groupBox_9.setToolTip(
            QCoreApplication.translate(
                "Settings", "Fine adjust the sleep tuning parameter.", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.groupBox_9.setTitle("")
        self.lineEdit_serial_sleep_tune.setText(
            QCoreApplication.translate("Settings", "0.000001", None)
        )
        self.label_6.setText(QCoreApplication.translate("Settings", "Sleep Tune", None))
        # if QT_CONFIG(tooltip)
        self.groupBox_8.setToolTip(
            QCoreApplication.translate(
                "Settings",
                "This is the delay to allow the micro to reset itself upon connection",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.groupBox_8.setTitle("")
        self.spinBox_wait_time.setSuffix(
            QCoreApplication.translate("Settings", "s", None)
        )
        self.label_5.setText(
            QCoreApplication.translate("Settings", "Arduino Wait Time", None)
        )
        # if QT_CONFIG(tooltip)
        self.commandLinkButton_select_color.setToolTip(
            QCoreApplication.translate(
                "Settings", "Change the foreground color of the text area", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.commandLinkButton_select_color.setText(
            QCoreApplication.translate("Settings", "Select Text Color", None)
        )
        # if QT_CONFIG(tooltip)
        self.commandLinkButton_bg_color.setToolTip(
            QCoreApplication.translate(
                "Settings", "Change the background color of the text area", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.commandLinkButton_bg_color.setText(
            QCoreApplication.translate("Settings", "Select Background Color", None)
        )
        self.commandLinkButton_bg_color.setDescription("")
        # if QT_CONFIG(tooltip)
        self.lcdNumber.setToolTip(
            QCoreApplication.translate(
                "Settings",
                "This is the # of sec that will be applied between testing steps",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.dial.setToolTip(
            QCoreApplication.translate(
                "Settings", "Rotate CW for faster testing, CCW for slower testing", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.pushButton_save.setToolTip(
            QCoreApplication.translate("Settings", "Save and close this window.", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.pushButton_save.setText(
            QCoreApplication.translate("Settings", "Save", None)
        )
        # if QT_CONFIG(shortcut)
        self.pushButton_save.setShortcut(
            QCoreApplication.translate("Settings", "Ctrl+S", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.groupBox_5.setTitle("")
        self.checkBox_logon.setText(
            QCoreApplication.translate("Settings", "Auto Login", None)
        )
        # if QT_CONFIG(tooltip)
        self.checkBox_debug.setToolTip(
            QCoreApplication.translate(
                "Settings",
                "The application will print out more info to the terminal",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.checkBox_debug.setText(
            QCoreApplication.translate("Settings", "Debug", None)
        )
        # if QT_CONFIG(tooltip)
        self.checkBox_connect.setToolTip(
            QCoreApplication.translate(
                "Settings", "The application will try connecting on startup", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.checkBox_connect.setText(
            QCoreApplication.translate("Settings", "Auto Connect", None)
        )
        # if QT_CONFIG(tooltip)
        self.checkBox_test.setToolTip(
            QCoreApplication.translate(
                "Settings", "Automatically start testing after programming", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.checkBox_test.setText(
            QCoreApplication.translate("Settings", "Auto Test", None)
        )
        self.label.setText(QCoreApplication.translate("Settings", "ms", None))
        # if QT_CONFIG(tooltip)
        self.pushButton_default.setToolTip(
            QCoreApplication.translate(
                "Settings",
                (
                    "Apply defaults to this window. Does not save until you press the"
                    " save button."
                ),
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pushButton_default.setText(
            QCoreApplication.translate("Settings", "Defaults", None)
        )
        # if QT_CONFIG(shortcut)
        self.pushButton_default.setShortcut(
            QCoreApplication.translate("Settings", "Ctrl+D", None)
        )


# endif // QT_CONFIG(shortcut)
# retranslateUi
