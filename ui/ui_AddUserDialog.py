# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddUserDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QLabel, QLayout,
    QLineEdit, QSizePolicy, QWidget)
import resource_rc
import icons_rc

class Ui_AddUserDialog(object):
    def setupUi(self, AddUserDialog):
        if not AddUserDialog.objectName():
            AddUserDialog.setObjectName(u"AddUserDialog")
        AddUserDialog.resize(360, 135)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddUserDialog.sizePolicy().hasHeightForWidth())
        AddUserDialog.setSizePolicy(sizePolicy)
        AddUserDialog.setMinimumSize(QSize(360, 135))
        AddUserDialog.setMaximumSize(QSize(360, 135))
        icon = QIcon()
        icon.addFile(u":/resources/icons/images/icons/follow.png", QSize(), QIcon.Normal, QIcon.Off)
        AddUserDialog.setWindowIcon(icon)
        self.formLayout = QFormLayout(AddUserDialog)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.formLayout.setLabelAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.formLayout.setVerticalSpacing(12)
        self.label = QLabel(AddUserDialog)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(30, 0))
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.lineEdit_username = QLineEdit(AddUserDialog)
        self.lineEdit_username.setObjectName(u"lineEdit_username")
        self.lineEdit_username.setMinimumSize(QSize(0, 30))
        self.lineEdit_username.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_username)

        self.label_2 = QLabel(AddUserDialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 30))
        self.label_2.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.lineEdit_password = QLineEdit(AddUserDialog)
        self.lineEdit_password.setObjectName(u"lineEdit_password")
        self.lineEdit_password.setMinimumSize(QSize(0, 30))
        self.lineEdit_password.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_password)

        self.checkBox = QCheckBox(AddUserDialog)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setMinimumSize(QSize(0, 30))
        self.checkBox.setFont(font)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.checkBox)

        self.buttonBox = QDialogButtonBox(AddUserDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setMinimumSize(QSize(0, 30))
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.buttonBox)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.lineEdit_username)
        self.label_2.setBuddy(self.lineEdit_password)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(AddUserDialog)
        self.buttonBox.accepted.connect(AddUserDialog.accept)
        self.buttonBox.rejected.connect(AddUserDialog.reject)

        QMetaObject.connectSlotsByName(AddUserDialog)
    # setupUi

    def retranslateUi(self, AddUserDialog):
        AddUserDialog.setWindowTitle(QCoreApplication.translate("AddUserDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("AddUserDialog", u"Username", None))
        self.label_2.setText(QCoreApplication.translate("AddUserDialog", u"Password", None))
        self.checkBox.setText(QCoreApplication.translate("AddUserDialog", u"Admin", None))
    # retranslateUi

