# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'LogView.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QHeaderView, QSizePolicy,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
import icons_rc

class Ui_LogView(object):
    def setupUi(self, LogView):
        if not LogView.objectName():
            LogView.setObjectName(u"LogView")
        LogView.resize(919, 639)
        LogView.setMinimumSize(QSize(900, 600))
        icon = QIcon()
        icon.addFile(u":/resources/icons/images/icons/files.png", QSize(), QIcon.Normal, QIcon.Off)
        LogView.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(LogView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tableWidget = QTableWidget(LogView)
        if (self.tableWidget.columnCount() < 3):
            self.tableWidget.setColumnCount(3)
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font);
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font);
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font);
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.tableWidget.rowCount() < 40):
            self.tableWidget.setRowCount(40)
        self.tableWidget.setObjectName(u"tableWidget")
        font1 = QFont()
        font1.setPointSize(11)
        self.tableWidget.setFont(font1)
        self.tableWidget.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.tableWidget.setProperty("showDropIndicator", False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setGridStyle(Qt.SolidLine)
        self.tableWidget.setRowCount(40)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(170)
        self.tableWidget.horizontalHeader().setProperty("showSortIndicator", True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tableWidget)


        self.retranslateUi(LogView)

        QMetaObject.connectSlotsByName(LogView)
    # setupUi

    def retranslateUi(self, LogView):
        LogView.setWindowTitle(QCoreApplication.translate("LogView", u"Log Viewer", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("LogView", u"Date", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("LogView", u"Level", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("LogView", u"Message", None));
    # retranslateUi

