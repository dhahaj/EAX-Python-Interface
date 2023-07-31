# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
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
    QAction,
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
    QFrame,
    QHBoxLayout,
    QLabel,
    QLayout,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
import resource_rc
import icons_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1027, 850)
        MainWindow.setMinimumSize(QSize(1025, 850))
        font = QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)
        MainWindow.setAcceptDrops(True)
        icon = QIcon()
        icon.addFile(
            ":/resources/icons/images/icons/powershell.ico",
            QSize(),
            QIcon.Normal,
            QIcon.On,
        )
        MainWindow.setWindowIcon(icon)
        MainWindow.setIconSize(QSize(32, 32))
        self.actionConnect = QAction(MainWindow)
        self.actionConnect.setObjectName("actionConnect")
        icon1 = QIcon()
        icon1.addFile(
            ":/resources/icons/images/icons/plug.png", QSize(), QIcon.Normal, QIcon.Off
        )
        icon1.addFile(
            ":/resources/icons/images/icons/plug.png", QSize(), QIcon.Normal, QIcon.On
        )
        self.actionConnect.setIcon(icon1)
        self.actionConnect.setFont(font)
        self.actionConnect.setShortcutContext(Qt.WidgetShortcut)
        self.actionLogout = QAction(MainWindow)
        self.actionLogout.setObjectName("actionLogout")
        icon2 = QIcon()
        icon2.addFile(
            ":/resources/icons/images/icons/remove-user.png",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon2.addFile(
            ":/resources/icons/images/icons/remove-user.png",
            QSize(),
            QIcon.Normal,
            QIcon.On,
        )
        self.actionLogout.setIcon(icon2)
        self.actionLogout.setFont(font)
        self.actionExit_2 = QAction(MainWindow)
        self.actionExit_2.setObjectName("actionExit_2")
        icon3 = QIcon()
        icon3.addFile(
            ":/resources/icons/images/icons/logout2.png",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon3.addFile(
            ":/resources/icons/images/icons/logout2.png",
            QSize(),
            QIcon.Disabled,
            QIcon.Off,
        )
        self.actionExit_2.setIcon(icon3)
        self.actionExit_2.setFont(font)
        self.actionExit_2.setMenuRole(QAction.QuitRole)
        self.actionEAX300 = QAction(MainWindow)
        self.actionEAX300.setObjectName("actionEAX300")
        self.actionEAX300.setCheckable(True)
        self.actionEAX300.setFont(font)
        self.actionEAX500 = QAction(MainWindow)
        self.actionEAX500.setObjectName("actionEAX500")
        self.actionEAX500.setCheckable(True)
        self.actionEAX500.setFont(font)
        self.actionEAX503 = QAction(MainWindow)
        self.actionEAX503.setObjectName("actionEAX503")
        self.actionEAX503.setCheckable(True)
        self.actionEAX503.setFont(font)
        self.actionEAX504 = QAction(MainWindow)
        self.actionEAX504.setObjectName("actionEAX504")
        self.actionEAX504.setCheckable(True)
        self.actionEAX504.setFont(font)
        self.actionEAX505 = QAction(MainWindow)
        self.actionEAX505.setObjectName("actionEAX505")
        self.actionEAX505.setCheckable(True)
        self.actionEAX505.setFont(font)
        self.actionEAX510 = QAction(MainWindow)
        self.actionEAX510.setObjectName("actionEAX510")
        self.actionEAX510.setCheckable(True)
        self.actionEAX510.setFont(font)
        self.actionEAX513 = QAction(MainWindow)
        self.actionEAX513.setObjectName("actionEAX513")
        self.actionEAX513.setCheckable(True)
        self.actionEAX513.setFont(font)
        self.actionEAX514 = QAction(MainWindow)
        self.actionEAX514.setObjectName("actionEAX514")
        self.actionEAX514.setCheckable(True)
        self.actionEAX514.setFont(font)
        self.actionEAX515 = QAction(MainWindow)
        self.actionEAX515.setObjectName("actionEAX515")
        self.actionEAX515.setCheckable(True)
        self.actionEAX515.setFont(font)
        self.actionEAX520 = QAction(MainWindow)
        self.actionEAX520.setObjectName("actionEAX520")
        self.actionEAX520.setCheckable(True)
        self.actionEAX520.setFont(font)
        self.actionEAX523 = QAction(MainWindow)
        self.actionEAX523.setObjectName("actionEAX523")
        self.actionEAX523.setCheckable(True)
        self.actionEAX523.setFont(font)
        self.actionEAX524 = QAction(MainWindow)
        self.actionEAX524.setObjectName("actionEAX524")
        self.actionEAX524.setCheckable(True)
        self.actionEAX524.setFont(font)
        self.actionEAX525 = QAction(MainWindow)
        self.actionEAX525.setObjectName("actionEAX525")
        self.actionEAX525.setCheckable(True)
        self.actionEAX525.setFont(font)
        self.actionChange_font = QAction(MainWindow)
        self.actionChange_font.setObjectName("actionChange_font")
        icon4 = QIcon()
        icon4.addFile(
            ":/resources/icons/images/icons/size.png", QSize(), QIcon.Normal, QIcon.On
        )
        self.actionChange_font.setIcon(icon4)
        self.actionChange_font.setFont(font)
        self.actionModify_Settings = QAction(MainWindow)
        self.actionModify_Settings.setObjectName("actionModify_Settings")
        icon5 = QIcon()
        icon5.addFile(
            ":/resources/icons/images/icons/settings.ico",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.actionModify_Settings.setIcon(icon5)
        self.actionModify_Settings.setFont(font)
        self.actionAdd_User = QAction(MainWindow)
        self.actionAdd_User.setObjectName("actionAdd_User")
        icon6 = QIcon()
        icon6.addFile(
            ":/resources/icons/images/icons/follow.png",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        icon6.addFile(
            ":/resources/icons/images/icons/follow.png", QSize(), QIcon.Normal, QIcon.On
        )
        self.actionAdd_User.setIcon(icon6)
        self.actionAdd_User.setFont(font)
        self.actionRemove_User = QAction(MainWindow)
        self.actionRemove_User.setObjectName("actionRemove_User")
        icon7 = QIcon()
        icon7.addFile(
            ":/resources/icons/images/icons/remove-user.png",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.actionRemove_User.setIcon(icon7)
        self.actionRemove_User.setFont(font)
        self.actionShow_Logs = QAction(MainWindow)
        self.actionShow_Logs.setObjectName("actionShow_Logs")
        icon8 = QIcon()
        icon8.addFile(
            ":/resources/icons/images/icons/files.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.actionShow_Logs.setIcon(icon8)
        self.actionShow_Logs.setFont(font)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        icon9 = QIcon()
        icon9.addFile(
            ":/resources/icons/images/icons/information.png",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        self.actionAbout.setIcon(icon9)
        self.actionAbout.setFont(font)
        self.actionAbout.setShortcutContext(Qt.ApplicationShortcut)
        self.actionAbout.setMenuRole(QAction.AboutQtRole)
        self.actionManual_Control = QAction(MainWindow)
        self.actionManual_Control.setObjectName("actionManual_Control")
        icon10 = QIcon()
        icon10.addFile(
            ":/resources/icons/images/icons/gear.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.actionManual_Control.setIcon(icon10)
        self.actionManual_Control.setFont(font)
        self.actionChip_Select = QAction(MainWindow)
        self.actionChip_Select.setObjectName("actionChip_Select")
        icon11 = QIcon()
        icon11.addFile(
            ":/resources/icons/images/icons/chip.png", QSize(), QIcon.Normal, QIcon.Off
        )
        self.actionChip_Select.setIcon(icon11)
        self.actionChip_Select.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.text_edit = QTextEdit(self.centralwidget)
        self.text_edit.setObjectName("text_edit")
        font1 = QFont()
        font1.setFamilies(["Calibri"])
        font1.setPointSize(16)
        self.text_edit.setFont(font1)
        self.text_edit.setMouseTracking(True)
        self.text_edit.setFocusPolicy(Qt.NoFocus)
        self.text_edit.setAutoFillBackground(False)
        self.text_edit.setStyleSheet("")
        self.text_edit.setFrameShape(QFrame.StyledPanel)
        self.text_edit.setFrameShadow(QFrame.Plain)
        self.text_edit.setAutoFormatting(QTextEdit.AutoAll)
        self.text_edit.setUndoRedoEnabled(False)
        self.text_edit.setReadOnly(True)
        self.text_edit.setTextInteractionFlags(Qt.NoTextInteraction)

        self.verticalLayout.addWidget(self.text_edit)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(4, -1, 4, -1)
        self.program_button = QPushButton(self.centralwidget)
        self.program_button.setObjectName("program_button")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.program_button.sizePolicy().hasHeightForWidth()
        )
        self.program_button.setSizePolicy(sizePolicy)
        self.program_button.setMinimumSize(QSize(0, 80))
        self.program_button.setBaseSize(QSize(0, 0))
        font2 = QFont()
        font2.setPointSize(20)
        self.program_button.setFont(font2)

        self.horizontalLayout.addWidget(self.program_button)

        self.device_label = QLabel(self.centralwidget)
        self.device_label.setObjectName("device_label")
        font3 = QFont()
        font3.setPointSize(13)
        font3.setBold(True)
        self.device_label.setFont(font3)
        self.device_label.setStyleSheet("color: rgb(255, 0, 0);\nfont-weight: bold;")
        self.device_label.setFrameShape(QFrame.WinPanel)
        self.device_label.setFrameShadow(QFrame.Sunken)
        self.device_label.setTextFormat(Qt.AutoText)
        self.device_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.device_label)

        self.usb_label = QLabel(self.centralwidget)
        self.usb_label.setObjectName("usb_label")
        self.usb_label.setFont(font3)
        self.usb_label.setAutoFillBackground(False)
        self.usb_label.setStyleSheet("color: rgb(255, 0, 0);\nfont-weight: bold;")
        self.usb_label.setFrameShape(QFrame.WinPanel)
        self.usb_label.setFrameShadow(QFrame.Sunken)
        self.usb_label.setTextFormat(Qt.AutoText)
        self.usb_label.setScaledContents(False)
        self.usb_label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.usb_label)

        self.test_button = QPushButton(self.centralwidget)
        self.test_button.setObjectName("test_button")
        self.test_button.setMinimumSize(QSize(0, 80))
        font4 = QFont()
        font4.setPointSize(20)
        font4.setBold(False)
        self.test_button.setFont(font4)

        self.horizontalLayout.addWidget(self.test_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1027, 26))
        self.menubar.setFont(font)
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(False)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuDevice = QMenu(self.menubar)
        self.menuDevice.setObjectName("menuDevice")
        self.menuSetting = QMenu(self.menubar)
        self.menuSetting.setObjectName("menuSetting")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        QWidget.setTabOrder(self.program_button, self.test_button)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDevice.menuAction())
        self.menubar.addAction(self.menuSetting.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionConnect)
        self.menuFile.addAction(self.actionLogout)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit_2)
        self.menuDevice.addAction(self.actionEAX300)
        self.menuDevice.addSeparator()
        self.menuDevice.addAction(self.actionEAX500)
        self.menuDevice.addAction(self.actionEAX503)
        self.menuDevice.addAction(self.actionEAX504)
        self.menuDevice.addAction(self.actionEAX505)
        self.menuDevice.addAction(self.actionEAX510)
        self.menuDevice.addAction(self.actionEAX513)
        self.menuDevice.addAction(self.actionEAX514)
        self.menuDevice.addAction(self.actionEAX515)
        self.menuDevice.addAction(self.actionEAX520)
        self.menuDevice.addAction(self.actionEAX523)
        self.menuDevice.addAction(self.actionEAX524)
        self.menuDevice.addAction(self.actionEAX525)
        self.menuSetting.addAction(self.actionChange_font)
        self.menuSetting.addAction(self.actionModify_Settings)
        self.menuSetting.addSeparator()
        self.menuSetting.addAction(self.actionAdd_User)
        self.menuSetting.addAction(self.actionRemove_User)
        self.menuSetting.addSeparator()
        self.menuSetting.addAction(self.actionManual_Control)
        self.menuSetting.addAction(self.actionChip_Select)
        self.menuHelp.addAction(self.actionShow_Logs)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)
        self.actionExit_2.triggered.connect(MainWindow.close)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "EAX Interface", None)
        )
        self.actionConnect.setText(
            QCoreApplication.translate("MainWindow", "Connect", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionConnect.setToolTip(
            QCoreApplication.translate("MainWindow", "Connect to the fixture.", None)
        )
        # endif // QT_CONFIG(tooltip)
        self.actionLogout.setText(
            QCoreApplication.translate("MainWindow", "Logout", None)
        )
        self.actionExit_2.setText(
            QCoreApplication.translate("MainWindow", "Exit", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionExit_2.setShortcut(
            QCoreApplication.translate("MainWindow", "Esc", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionEAX300.setText(
            QCoreApplication.translate("MainWindow", "EAX300", None)
        )
        self.actionEAX500.setText(
            QCoreApplication.translate("MainWindow", "EAX500", None)
        )
        self.actionEAX503.setText(
            QCoreApplication.translate("MainWindow", "EAX503", None)
        )
        self.actionEAX504.setText(
            QCoreApplication.translate("MainWindow", "EAX504", None)
        )
        self.actionEAX505.setText(
            QCoreApplication.translate("MainWindow", "EAX505", None)
        )
        self.actionEAX510.setText(
            QCoreApplication.translate("MainWindow", "EAX510", None)
        )
        self.actionEAX513.setText(
            QCoreApplication.translate("MainWindow", "EAX513", None)
        )
        self.actionEAX514.setText(
            QCoreApplication.translate("MainWindow", "EAX514", None)
        )
        self.actionEAX515.setText(
            QCoreApplication.translate("MainWindow", "EAX515", None)
        )
        self.actionEAX520.setText(
            QCoreApplication.translate("MainWindow", "EAX520", None)
        )
        self.actionEAX523.setText(
            QCoreApplication.translate("MainWindow", "EAX523", None)
        )
        self.actionEAX524.setText(
            QCoreApplication.translate("MainWindow", "EAX524", None)
        )
        self.actionEAX525.setText(
            QCoreApplication.translate("MainWindow", "EAX525", None)
        )
        self.actionChange_font.setText(
            QCoreApplication.translate("MainWindow", "Change Font", None)
        )
        self.actionModify_Settings.setText(
            QCoreApplication.translate("MainWindow", "Modify Settings", None)
        )
        self.actionAdd_User.setText(
            QCoreApplication.translate("MainWindow", "Add User", None)
        )
        self.actionRemove_User.setText(
            QCoreApplication.translate("MainWindow", "Remove User", None)
        )
        self.actionShow_Logs.setText(
            QCoreApplication.translate("MainWindow", "Show Logs", None)
        )
        self.actionAbout.setText(
            QCoreApplication.translate("MainWindow", "About", None)
        )
        self.actionManual_Control.setText(
            QCoreApplication.translate("MainWindow", "Manual Control", None)
        )
        self.actionChip_Select.setText(
            QCoreApplication.translate("MainWindow", "Chip Select", None)
        )
        self.text_edit.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Text Area", None)
        )
        self.program_button.setText(
            QCoreApplication.translate("MainWindow", "Program", None)
        )
        self.device_label.setText(
            QCoreApplication.translate("MainWindow", "Device: Not Selected", None)
        )
        self.usb_label.setText(
            QCoreApplication.translate("MainWindow", "USB: Not Connected", None)
        )
        self.test_button.setText(QCoreApplication.translate("MainWindow", "Test", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "File", None))
        self.menuDevice.setTitle(
            QCoreApplication.translate("MainWindow", "Device", None)
        )
        self.menuSetting.setTitle(
            QCoreApplication.translate("MainWindow", "Setting", None)
        )
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "Help", None))

    # retranslateUi
