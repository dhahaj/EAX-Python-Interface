# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HelpDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QSizePolicy, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)
import icons_rc

class Ui_HelpDialog(object):
    def setupUi(self, HelpDialog):
        if not HelpDialog.objectName():
            HelpDialog.setObjectName(u"HelpDialog")
        HelpDialog.resize(929, 817)
        icon = QIcon()
        icon.addFile(u":/resources/icons/images/icons/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        HelpDialog.setWindowIcon(icon)
        self.verticalLayout_5 = QVBoxLayout(HelpDialog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tabWidget = QTabWidget(HelpDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setDocumentMode(False)
        self.tabWidgetPage1 = QWidget()
        self.tabWidgetPage1.setObjectName(u"tabWidgetPage1")
        self.verticalLayout = QVBoxLayout(self.tabWidgetPage1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textBrowser_readme = QTextBrowser(self.tabWidgetPage1)
        self.textBrowser_readme.setObjectName(u"textBrowser_readme")
        self.textBrowser_readme.setTextInteractionFlags(Qt.LinksAccessibleByKeyboard|Qt.LinksAccessibleByMouse|Qt.TextBrowserInteraction|Qt.TextSelectableByKeyboard|Qt.TextSelectableByMouse)
        self.textBrowser_readme.setSource(QUrl(u"qrc:/resources/README.html"))
        self.textBrowser_readme.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.textBrowser_readme)

        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.tabWidgetPage2 = QWidget()
        self.tabWidgetPage2.setObjectName(u"tabWidgetPage2")
        self.verticalLayout_3 = QVBoxLayout(self.tabWidgetPage2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.tabWidgetPage2)
        self.label.setObjectName(u"label")
        self.label.setFrameShape(QFrame.NoFrame)
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(False)

        self.verticalLayout_3.addWidget(self.label)

        self.tabWidget.addTab(self.tabWidgetPage2, "")
        self.tabWidgetPage3 = QWidget()
        self.tabWidgetPage3.setObjectName(u"tabWidgetPage3")
        self.horizontalLayout = QHBoxLayout(self.tabWidgetPage3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.tabWidgetPage3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_2)

        self.tabWidget.addTab(self.tabWidgetPage3, "")
        self.tabWidgetPage4 = QWidget()
        self.tabWidgetPage4.setObjectName(u"tabWidgetPage4")
        self.horizontalLayout_2 = QHBoxLayout(self.tabWidgetPage4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.tabWidgetPage4)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setTextFormat(Qt.AutoText)
        self.label_3.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.tabWidget.addTab(self.tabWidgetPage4, "")
        self.tabWidgetPage5 = QWidget()
        self.tabWidgetPage5.setObjectName(u"tabWidgetPage5")
        self.verticalLayout_2 = QVBoxLayout(self.tabWidgetPage5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textBrowser_usage = QTextBrowser(self.tabWidgetPage5)
        self.textBrowser_usage.setObjectName(u"textBrowser_usage")
        self.textBrowser_usage.setSource(QUrl(u"qrc:/resources/docs/USAGE.html"))

        self.verticalLayout_2.addWidget(self.textBrowser_usage)

        self.tabWidget.addTab(self.tabWidgetPage5, "")
        self.tabWidgetPage6 = QWidget()
        self.tabWidgetPage6.setObjectName(u"tabWidgetPage6")
        self.verticalLayout_4 = QVBoxLayout(self.tabWidgetPage6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.textBrowser_settings = QTextBrowser(self.tabWidgetPage6)
        self.textBrowser_settings.setObjectName(u"textBrowser_settings")
        self.textBrowser_settings.setSource(QUrl(u"qrc:/resources/docs/Settings.html"))

        self.verticalLayout_4.addWidget(self.textBrowser_settings)

        self.tabWidget.addTab(self.tabWidgetPage6, "")

        self.verticalLayout_5.addWidget(self.tabWidget)

        QWidget.setTabOrder(self.textBrowser_readme, self.textBrowser_usage)

        self.retranslateUi(HelpDialog)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(HelpDialog)
    # setupUi

    def retranslateUi(self, HelpDialog):
        HelpDialog.setWindowTitle(QCoreApplication.translate("HelpDialog", u"Help", None))
        self.textBrowser_readme.setSearchPaths([
            QCoreApplication.translate("HelpDialog", u"images", None),
            QCoreApplication.translate("HelpDialog", u"docs", None)])
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), QCoreApplication.translate("HelpDialog", u"Readme", None))
        self.label.setText(QCoreApplication.translate("HelpDialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700; text-decoration: underline;\">Click To Play Movie</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage2), QCoreApplication.translate("HelpDialog", u"Firmware Update", None))
        self.label_2.setText(QCoreApplication.translate("HelpDialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700; text-decoration: underline;\">Click To Play Movie</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage3), QCoreApplication.translate("HelpDialog", u"Testing", None))
        self.label_3.setText(QCoreApplication.translate("HelpDialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700; text-decoration: underline;\">Click To Play Movie</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage4), QCoreApplication.translate("HelpDialog", u"Settings", None))
        self.textBrowser_usage.setSearchPaths([
            QCoreApplication.translate("HelpDialog", u"docs", None),
            QCoreApplication.translate("HelpDialog", u"images", None)])
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage5), QCoreApplication.translate("HelpDialog", u"Usage", None))
        self.textBrowser_settings.setHtml(QCoreApplication.translate("HelpDialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.textBrowser_settings.setSearchPaths([
            QCoreApplication.translate("HelpDialog", u"images", None),
            QCoreApplication.translate("HelpDialog", u"docs", None)])
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage6), QCoreApplication.translate("HelpDialog", u"Settings", None))
    # retranslateUi

