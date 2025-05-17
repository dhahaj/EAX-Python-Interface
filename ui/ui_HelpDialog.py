# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HelpDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QSizePolicy, QTabWidget, QTextBrowser, QVBoxLayout,
    QWidget)
import icons_rc
import resource_rc

class Ui_HelpDialog(object):
    def setupUi(self, HelpDialog):
        if not HelpDialog.objectName():
            HelpDialog.setObjectName(u"HelpDialog")
        HelpDialog.resize(934, 1039)
        icon = QIcon()
        icon.addFile(u":/resources/icons/images/icons/icon.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        HelpDialog.setWindowIcon(icon)
        self.verticalLayout_5 = QVBoxLayout(HelpDialog)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.tabWidget = QTabWidget(HelpDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        font = QFont()
        font.setPointSize(11)
        self.tabWidget.setFont(font)
        self.tabWidget.setDocumentMode(False)
        self.tabWidgetPage1 = QWidget()
        self.tabWidgetPage1.setObjectName(u"tabWidgetPage1")
        self.verticalLayout = QVBoxLayout(self.tabWidgetPage1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textBrowser_readme = QTextBrowser(self.tabWidgetPage1)
        self.textBrowser_readme.setObjectName(u"textBrowser_readme")
        font1 = QFont()
        font1.setPointSize(12)
        self.textBrowser_readme.setFont(font1)
        self.textBrowser_readme.setLineWrapColumnOrWidth(-5)
        self.textBrowser_readme.setReadOnly(True)
        self.textBrowser_readme.setHtml(u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<h1 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:xx-large; font-weight:700;\">EAX Device Test &amp; Programming Interface</span></h1>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This application provides a graphical user interface for testing and programming EAX hardware devices (e.g., EAX300, EAX500 series). It interacts with an Arduino-based"
                        " test fixture using the TelemetrixAIO library and allows users to execute configurable test sequences, program firmware onto target devices, and manually control I/O pins.</p>\n"
"<h2 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Table of Contents</span></h2>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#eax-device-test--programming-interface\"><span style=\" color:#7cfbfc;\">EAX Device Test &amp; Programming Interface</span></a>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#table-of-con"
                        "tents\"><span style=\" color:#7cfbfc;\">Table of Contents</span></a></li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#features\"><span style=\" color:#7cfbfc;\">Features</span></a></li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#prerequisites\"><span style=\" color:#7cfbfc;\">Prerequisites</span></a></li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#dependencies\"><span style=\" color:#7cfbfc;\">Dependencies</span></a></li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#configuration-configyaml\"><span style=\" color:#7cfbfc;\">Configuration (config.yaml)</span></a>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right"
                        ": 0px; -qt-list-indent: 3;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#testing-configuration\"><span style=\" color:#7cfbfc;\">Testing Configuration</span></a></li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#pin-configuration\"><span style=\" color:#7cfbfc;\">Pin Configuration</span></a></li></ul></li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#installation\"><span style=\" color:#7cfbfc;\">Installation</span></a></li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#modules\"><span style=\" color:#7cfbfc;\">Modules</span></a></li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-ind"
                        "ent:0px;\"><a href=\"#contributing\"><span style=\" color:#7cfbfc;\">Contributing</span></a></li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#license\"><span style=\" color:#7cfbfc;\">License</span></a></li></ul></li></ul>\n"
"<h2 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Features</span></h2>\n"
"<ul type=\"circle\" style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Graphical User Interface:</span> Built with PySide6 (Qt6) for intuitive operation.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span "
                        "style=\" font-weight:700;\">Configurable Test Sequences:</span> Define test steps, including pin manipulation, delays, user prompts, and input waiting, via a <span style=\" font-family:'Courier New'; font-size:11pt;\">config.yaml</span> file.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Hardware Interaction:</span> Controls an Arduino (via TelemetrixAIO) for digital I/O to the device under test.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Device Programming:</span> Supports programming target EAX devices using an external programmer tool (path and arguments configurable).</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Device Management:</span> Select differe"
                        "nt EAX device models, each potentially having different test sequences or firmware.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Manual Control:</span> A dialog to manually toggle output pins on the test fixture.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Asynchronous Operations:</span> Utilizes <span style=\" font-family:'Courier New'; font-size:11pt;\">asyncio</span> and <span style=\" font-family:'Courier New'; font-size:11pt;\">qasync</span> to ensure a responsive UI during I/O operations and tests.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Logging:</span> Comprehensive logging of application events and test progress.</li>\n"
"<li style=\" margin-t"
                        "op:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Settings Management:</span> Persistent application settings (COM port, programmer paths, UI preferences, etc.).</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Theming:</span> Supports dark and light themes.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Single Instance:</span> Prevents multiple instances of the application from running simultaneously.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Firmware Update:</span> Capability to update the firmware on the Arduino test fixture itself.</li>\n"
"<li style=\" margin-top:7px; mar"
                        "gin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Resource Bundling:</span> Essential configuration files and images can be bundled within the application.</li></ul>\n"
"<h2 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Prerequisites</span></h2>\n"
"<ul type=\"circle\" style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Python 3.8+</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">An Arduino board flashed with <a href=\"https://github.com/MrYsLab/Telemetrix4Arduino\"><span style=\" color:#7cfbfc;\">Telemetrix4Arduino</span></a> (or StandardFirmata for older te"
                        "st fixture firmware, if supported by configuration).</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">External programmer for the target EAX devices (e.g., ASIX PRESTO or similar).</li></ul>\n"
"<h2 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Dependencies</span></h2>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The application relies on the following Python libraries:</p>\n"
"<ul type=\"circle\" style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">PySide6</span>: For the graphical user interfa"
                        "ce (Qt6 bindings).</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">qtpy</span>: Abstraction layer for Qt bindings (though PySide6 is explicitly used).</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">qasync</span>: To integrate <span style=\" font-family:'Courier New'; font-size:11pt;\">asyncio</span> with the Qt event loop.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">telemetrix-aio</span>: For asynchronous communication with the Arduino.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font"
                        "-family:'Courier New'; font-size:11pt;\">PyYAML</span>: For loading <span style=\" font-family:'Courier New'; font-size:11pt;\">config.yaml</span>.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">qdarkstyle</span>: For dark/light theming.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">pyserial</span>: For serial port listing (dependency of Telemetrix).</li></ul>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">You can typically install these using pip:</p>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">pip install Py"
                        "Side6 qtpy qasync telemetrix-aio PyYAML qdarkstyle pyserial</span></pre>\n"
"<pre style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Courier New'; font-size:11pt;\"><br /></pre>\n"
"<h2 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Configuration (config.yaml)</span></h2>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The application uses a YAML configuration file (<span style=\" font-family:'Courier New'; font-size:11pt;\">config.yaml</span>) to define various runtime settings. This file is expected to be in the same directory as the main executable, and if not found, the application will attempt to extract a bundled version with default settings. The structure of the <span style=\" font-family:'Courier New'; "
                        "font-size:11pt;\">config.yaml</span> file is as follows:</p>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2523\u2501app_name             </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2523\u2501app_version          </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2523\u2501devices</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;"
                        " margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2523\u2501firmware_path            </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2523\u2501label_styles</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2523\u2501label_size   </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2517\u2501firmware_files           </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><spa"
                        "n style=\" font-family:'Courier New'; font-size:11pt;\">\u2503       \u2523\u2501device_name  </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503       \u2523\u2501firmware_name</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503       \u2517\u2501color     </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2523\u2501pins                 </span></pre>\n"
""
                        "<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2517\u2501&lt;function&gt;</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503       \u2517\u2501&lt;mode, number, pullup&gt;</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2523\u2501testing              </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2523\u2501cleanup          </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left"
                        ":0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2503   \u2517\u2501&lt;action, function, value&gt;       </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2517\u2501sequence         </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503       \u2517\u2501&lt;action, params...&gt;       </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-ind"
                        "ent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2523\u2501window</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2517\u2501usb_label</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503       \u2523\u2501connected_style</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503       \u2523\u2501connected_text</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503       \u2523\u2501"
                        "connecting_style</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503       \u2523\u2501disconnected_style</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503       \u2523\u2501disconnected_text</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503       \u2517\u2501text  </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px;"
                        " margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2523\u2501logging              </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2523\u2501log_file         </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2523\u2501log_level        </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2523\u2501log_format       </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" f"
                        "ont-family:'Courier New'; font-size:11pt;\">\u2503   \u2523\u2501log_rotation     </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2523\u2501log_retention    </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2517\u2501database_file    </span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2523\u2501chip_options</span></pre>\n"
"<pre style=\" m"
                        "argin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503   \u2517\u2501&lt;chip_part_number&gt;</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2503</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">\u2517\u2501programmer_config</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">    \u2523\u2501executable</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span s"
                        "tyle=\" font-family:'Courier New'; font-size:11pt;\">    \u2523\u2501programmer</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">    \u2517\u2501arguments[...]</span></pre>\n"
"<h3 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">Testing Configuration</span></h3>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The <span style=\" font-family:'Courier New'; font-size:11pt;\">testing</span> key in <span style=\" font-family:'Courier New'; font-size:11pt;\">config.yaml</span> file defines how the test is run. The testing configuration is stored in a YAML object with the following format:</p>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right"
                        ":0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">sequence:</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">  - action: message</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">    text: &gt;</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">      &lt;p&gt;</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">        \ud83d\udd37 Testing Low battery function \ud83e\udca7"
                        " The LED's blink alternately</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">      &lt;/p&gt;</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">  - action: write_pin</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">    function: low battery</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">    value: 1</span></pre>\n"
"<pre style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-rig"
                        "ht:0px; -qt-block-indent:0; text-indent:0px; font-family:'Courier New'; font-size:11pt;\"><br /></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">  - action: delay # Uses default speed if duration_ms is omitted</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">    duration_ms: 1000</span></pre>\n"
"<pre style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'Courier New'; font-size:11pt;\"><br /></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">cleanup:</span></pre>\n"
"<pre style=\" "
                        "margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">  - action: write_pin</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">    function: test_indicator</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">    value: 0</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">  - action: write_pin</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Co"
                        "urier New'; font-size:11pt;\">    function: low battery</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">    value: 0</span></pre>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The <span style=\" font-family:'Courier New'; font-size:11pt;\">sequence</span> key in the <span style=\" font-family:'Courier New'; font-size:11pt;\">config.yaml</span> file contains a sequence of actions to be performed during the testing process. The possible options for an action are:</p>\n"
"<table border=\"1\" style=\" border-collapse:collapse;\" cellpadding=\"4\">\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Action</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; mar"
                        "gin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Parameters</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Description</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">message</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">text</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The text to display.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-botto"
                        "m:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">---</p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">if_has (optional)</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Optional condition to check if the action should be executed.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">delay</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">duration_ms (optional)</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top"
                        ":0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Delay in milliseconds.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">---</p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">if_has (optional)</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Optional condition to check if the action should be executed.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">write_pin</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin"
                        "-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">function</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Write a value to the pin with the specified function.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">---</p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">value</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The value to write to the pin.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-inden"
                        "t:0; text-indent:0px;\">---</p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">if_has (optional)</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Optional condition to check if the action should be executed.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">wait_for_input</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">function</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -q"
                        "t-block-indent:0; text-indent:0px;\">Wait for input on the pin with the specified function.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">---</p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">if_has (optional)</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Optional condition to check if the action should be executed.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">---</p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier"
                        " New'; font-size:11pt;\">timeout_key</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">They key used in the settings to set the timeout.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">---</p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">message_on_pass</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The message to display on pass.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">---</p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0"
                        "px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">message_on_fail</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The message to display on fail.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">---</p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">expected_value</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The expected value. (0 or 1)</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-ind"
                        "ent:0; text-indent:0px;\">---</p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">fail_on_timeout</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Whether to fail on timeout.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">wait_for_button</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">timeout_key</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:"
                        "0px;\">The key used in the settings to set the button timeout.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">---</p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">message_on_fail</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The message to display on fail.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">---</p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">fail_on_timeout</span></p></td>\n"
""
                        "<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Whether to fail on timeout.</p></td></tr></table>\n"
"<h3 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">Pin Configuration</span></h3>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The <span style=\" font-family:'Courier New'; font-size:11pt;\">pins</span> key in the <span style=\" font-family:'Courier New'; font-size:11pt;\">config.yaml</span> file contains the pin configuration. The pin configuration is stored in a YAML object with the following format:</p>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">pins:</span></pre>\n"
"<pre style=\" margin"
                        "-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">  - function: &lt;function_name&gt;</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">    io_mode: &lt;input|output|input_pullup&gt;</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">    pin_number: &lt;pin_number&gt;</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">    pullup_enabled: &lt;true|false&gt;</span></pre>\n"
"<table border=\"1\" style=\" border-collapse:collapse;\" cellpadding=\"4\">\n"
"<tr>\n"
""
                        "<td>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Key</p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">Description</span></p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">function</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The functional name of the pin (e.g., &quot;battery&quot;, &quot;low battery&quot;).</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">io_mode</span></p"
                        "></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The I/O mode of the pin (e.g., &quot;input&quot;, &quot;output&quot;, &quot;input_pullup&quot;).</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">pin_number</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Arduino pin number associated with the function.</p></td></tr>\n"
"<tr>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New'; font-size:11pt;\">pullup_enabled</span></p></td>\n"
"<td>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-ind"
                        "ent:0; text-indent:0px;\">Whether the internal pull-up resistor is enabled (true/false).</p></td></tr></table>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The application's behavior is heavily driven by config.yaml. This file defines:</p>\n"
"<ul type=\"circle\" style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">**Pin Mappings: Maps functional names (e.g., &quot;battery&quot;, &quot;low battery&quot;) to Arduino pin numbers and I/O modes.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">**Test Sequences: A list of steps for automated testing. Each step defines an action (e.g., write_pin, delay, wait_for_input, wait_for_button, message).</li>\n"
"<li style=\" margin-top:7px;"
                        " margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">**Cleanup Sequences: Steps to run after a test to reset hardware.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">**Device Definitions: Information about supported EAX devices, including firmware paths.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">**Chip Options: List of microcontroller part numbers for the programmer.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">**Logging: Configuration for logging, including log file path, log level, and log format.</li></ul>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A default config.yaml is expected. If not found, the application may attempt to extra"
                        "ct a bundled version.</p>\n"
"<h2 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Installation</span></h2>\n"
"<ul type=\"circle\" style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Clone this repository or download the source code.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Install Python 3 if you haven't already.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Install the required dependencies (see Dependencies).</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">E"
                        "nsure your Arduino is flashed with the appropriate Telemetrix firmware.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Configure your external EAX device programmer and ensure its path is correctly set in the application settings or config.yaml.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Review and customize config.yaml for your specific hardware setup and test requirements.</li></ul>\n"
"<h2 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Modules</span></h2>\n"
"<ul type=\"circle\" style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style"
                        "=\" font-weight:700;\">main.py</span>: The main application entry point. Initializes the UI (MainWindow), handles user interactions, and orchestrates the overall application flow.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">test_controller.py</span>: Manages the execution of automated test sequences. Reads steps from config.yaml, interacts with AIODevice for hardware control, and emits signals to update the UI.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">arduino.py</span>: Provides the AIODevice class, an abstraction layer for communicating with the Arduino test fixture using TelemetrixAIO. Handles pin configuration, digital I/O, and input callbacks.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:"
                        "0px;\"><span style=\" font-weight:700;\">config_loader.py</span>: Loads and provides access to configurations from config.yaml (pin definitions, test sequences, device settings).</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">settings.py (assumed)</span>: Manages persistent application settings.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">constants.py (assumed)</span>: Defines shared constants used throughout the application.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">globals.py (assumed)</span>: Provides global instances like the logger.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-in"
                        "dent:0px;\"><span style=\" font-weight:700;\">ui/ (assumed directory)</span>: Contains UI files generated from Qt Designer (.ui files converted to .py).</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">util/ (assumed directory)</span>: Utility functions, possibly including resource management.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:700;\">device.py (assumed)</span>: Defines the Device class representing the EAX device under test.</li></ul>\n"
"<h2 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Contributing</span></h2>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Pull requests are"
                        " welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.</p>\n"
"<h2 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">License</span></h2>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">This project is licensed under the MIT License - see the <a href=\"LICENSE\"><span style=\" color:#7cfbfc;\">LICENSE</span></a> file for details.</p></body></html>")
        self.textBrowser_readme.setOverwriteMode(False)
        self.textBrowser_readme.setAcceptRichText(False)
        self.textBrowser_readme.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByKeyboard|Qt.TextInteractionFlag.TextSelectableByMouse)
        self.textBrowser_readme.setSource(QUrl(u"qrc:/README.md"))
        self.textBrowser_readme.setSearchPaths([u"images", u"resources", u"docs", u"."])
        self.textBrowser_readme.setOpenExternalLinks(True)

        self.verticalLayout.addWidget(self.textBrowser_readme)

        self.tabWidget.addTab(self.tabWidgetPage1, "")
        self.tabWidgetPage2 = QWidget()
        self.tabWidgetPage2.setObjectName(u"tabWidgetPage2")
        self.verticalLayout_3 = QVBoxLayout(self.tabWidgetPage2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.tabWidgetPage2)
        self.label.setObjectName(u"label")
        self.label.setFrameShape(QFrame.Shape.NoFrame)
        self.label.setScaledContents(False)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(False)

        self.verticalLayout_3.addWidget(self.label)

        self.tabWidget.addTab(self.tabWidgetPage2, "")
        self.tabWidgetPage3 = QWidget()
        self.tabWidgetPage3.setObjectName(u"tabWidgetPage3")
        self.horizontalLayout = QHBoxLayout(self.tabWidgetPage3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.tabWidgetPage3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_2)

        self.tabWidget.addTab(self.tabWidgetPage3, "")
        self.tabWidgetPage4 = QWidget()
        self.tabWidgetPage4.setObjectName(u"tabWidgetPage4")
        self.horizontalLayout_2 = QHBoxLayout(self.tabWidgetPage4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_3 = QLabel(self.tabWidgetPage4)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)
        self.label_3.setTextFormat(Qt.TextFormat.AutoText)
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_3)

        self.tabWidget.addTab(self.tabWidgetPage4, "")
        self.tabWidgetPage5 = QWidget()
        self.tabWidgetPage5.setObjectName(u"tabWidgetPage5")
        self.verticalLayout_2 = QVBoxLayout(self.tabWidgetPage5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.textBrowser_usage = QTextBrowser(self.tabWidgetPage5)
        self.textBrowser_usage.setObjectName(u"textBrowser_usage")
        self.textBrowser_usage.setSource(QUrl(u"qrc:/docs/USAGE.md"))

        self.verticalLayout_2.addWidget(self.textBrowser_usage)

        self.tabWidget.addTab(self.tabWidgetPage5, "")
        self.tabWidgetPage6 = QWidget()
        self.tabWidgetPage6.setObjectName(u"tabWidgetPage6")
        self.verticalLayout_4 = QVBoxLayout(self.tabWidgetPage6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.textBrowser_settings = QTextBrowser(self.tabWidgetPage6)
        self.textBrowser_settings.setObjectName(u"textBrowser_settings")
        self.textBrowser_settings.setSource(QUrl(u"qrc:/docs/Settings.md"))

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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage1), QCoreApplication.translate("HelpDialog", u"Readme", None))
        self.label.setText(QCoreApplication.translate("HelpDialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700; text-decoration: underline;\">Click To Play Movie</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage2), QCoreApplication.translate("HelpDialog", u"Firmware Update", None))
        self.label_2.setText(QCoreApplication.translate("HelpDialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700; text-decoration: underline;\">Click To Play Movie</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage3), QCoreApplication.translate("HelpDialog", u"Testing", None))
        self.label_3.setText(QCoreApplication.translate("HelpDialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700; text-decoration: underline;\">Click To Play Movie</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage4), QCoreApplication.translate("HelpDialog", u"Settings", None))
        self.textBrowser_usage.setHtml(QCoreApplication.translate("HelpDialog", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<h1 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:xx-large; font-weight:700;\">Usage</span></h1>\n"
"<h2 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Table of Contents</span></h2>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li "
                        "style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#usage\"><span style=\" color:#7cfbfc;\">Usage</span></a>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 2;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#table-of-contents\"><span style=\" color:#7cfbfc;\">Table of Contents</span></a></li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#installation\"><span style=\" color:#7cfbfc;\">Installation</span></a>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 3;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#new-features\"><span style=\" color:#7cfbfc;\""
                        ">New Features</span></a></li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#gui\"><span style=\" color:#7cfbfc;\">GUI</span></a></li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#settings\"><span style=\" color:#7cfbfc;\">Settings</span></a></li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"#firmware\"><span style=\" color:#7cfbfc;\">Firmware</span></a></li></ul></li></ul></li></ul>\n"
"<h2 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:x-large; font-weight:700;\">Installation</span></h2>\n"
"<ol style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7"
                        "px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Install the firmware to the test fixture. See the <a href=\"#firmware\"><span style=\" color:#7cfbfc;\">Firmware</span></a> section for more information.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The programming software called <span style=\" font-family:'Courier New';\">up.exe</span> provided for by <a href=\"https://www.asix.net/\"><span style=\" color:#7cfbfc;\">Asix</span></a> is required for programming.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Install Python 3.7 or later from <a href=\"https://www.python.org/\"><span style=\" color:#7cfbfc;\">Python.org</span></a>.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Run <span style=\" font-family:'Courier New';\">Start.bat</"
                        "span> from the <span style=\" font-family:'Courier New';\">Scrpts</span> directory to start the application.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Install the required Python package dependencies listed in <span style=\" font-family:'Courier New';\">requirements.txt</span> using the command <span style=\" font-family:'Courier New';\">pip install -r requirements.txt</span>.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">A standalone executable can be created using <span style=\" font-family:'Courier New';\">pyinstaller</span>. Install <span style=\" font-family:'Courier New';\">pyinstaller</span> using the command <span style=\" font-family:'Courier New';\">pip install pyinstaller</span>. (Optional)</li></ol>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The E"
                        "AX Test Interface is an improvement over the last version. The interface was written in pure Python using the <a href=\"https://doc.qt.io/qtforpython-6/\"><span style=\" color:#7cfbfc;\">Pyside6</span></a> library and <a href=\"https://www.qt.io/\"><span style=\" color:#7cfbfc;\">Qt</span></a> framwork. The improvements are listed below:</p>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Using an improved firmware for communicating with the fixture. It includes improvements to both the communication speed and allows for multiple devices to be connected to the same computer.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The <span style=\" font-family:'Courier New';\">Install.PS1</span> script can be used to automatically download and insta"
                        "ll the latest firmware. Requires an internet connection. See the <a href=\"#firmware\"><span style=\" color:#7cfbfc;\">Firmware</span></a> section for more information.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The settings are now stored in a plaint text file called <span style=\" font-family:'Courier New';\">settings.json</span>. This file contains a JSON object that represents all the runtime settings. There should not be any need to modify this file as all the settings can be changed in the application.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The pin assignments are now stored in a plain text file called <span style=\" font-family:'Courier New';\">pins.json</span>. This file contains a JSON object that represents all the pin assignments. There should not be any need to modify this file as all the pin assignments can be changed in"
                        " the application. The EAX Test Interface is an improvement over the last version. The interface was written in pure Python using the <a href=\"https://doc.qt.io/qtforpython-6/\"><span style=\" color:#7cfbfc;\">Pyside6</span></a> and Qt framwork. The improvements are listed below:</li></ul>\n"
"<h3 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">New Features</span></h3>\n"
"<ol style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Changing the serial numbers for the programmer can be done directly now in the settings menu. See the <a href=\"#settings\"><span style=\" color:#7cfbfc;\">Settings</span></a> section for more information.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:"
                        "0px; -qt-block-indent:0; text-indent:0px;\">The login process can be skipped by enabling the <span style=\" font-family:'Courier New';\">Auto Login</span> setting. Note to avoid the possibility of a user accidentally modifying the settings, a person will still be required to login as an administrator to change the settings.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The application can automatically find the correct USB port by enabling the <span style=\" font-family:'Courier New';\">Auto Find</span> setting. It will scan and test all USB ports and automatically connect to the correct one. The <span style=\" font-family:'Courier New';\">Auto Connect</span> setting will automatically connect to the fixture when the application is started.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">If for some reason two fixtures are to be connected to the"
                        " same computer, the <span style=\" font-family:'Courier New';\">arduino_instance_id</span> setting can be changed so that the application will only connect to the fixture with the matching <span style=\" font-family:'Courier New';\">arduino_instance_id</span>. Note that to do this, the firmware will need to be recompilled and uploaded to the test fixture.</li></ol>\n"
"<h3 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">GUI</span></h3>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The main window is composed of a text console, two buttons and two labels. The text console is used for displaying messages, and the buttons are used for programming and testing. The two text labels are used for displaying the status of the USB connection and the currently selected device. The menu bar contains the <span style=\" font-fa"
                        "mily:'Courier New';\">File</span>, <span style=\" font-family:'Courier New';\">Device</span>, <span style=\" font-family:'Courier New';\">Settings</span> and <span style=\" font-family:'Courier New';\">Help</span> menus. The <span style=\" font-family:'Courier New';\">File</span> menu contains items for logging in and out, connecting and disconnecting from the fixture, and exiting the application. The <span style=\" font-family:'Courier New';\">Device</span> menu contains items for selecting the device. The <span style=\" font-family:'Courier New';\">Settings</span> menu contains various items for modifying the settings. The <span style=\" font-family:'Courier New';\">Help</span> menu contains items for displaying the debugging logs and displaying the about dialog.</p>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"../images/MainWindow.png\" alt=\"alt text\" title=\"\" /></p>\n"
"<h3 style=\" margin-top:0px; margin-bottom:"
                        "0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">Settings</span></h3>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The settings can be changed by clicking on the <span style=\" font-family:'Courier New';\">Modify Settings</span> menu item. This will open up a new window as shown below. Any changes made on this window will not be applied until the <span style=\" font-family:'Courier New';\">Save</span> button is pressed. The <span style=\" font-family:'Courier New';\">Default</span> button will reset all the settings to their default values. The dial on the bottom right can be used to change the testing speed. Rotating it CW will increase the speed and CCW will decrease the speed. The exact timing is shown just above the dial, which is specified in ms. The <span style=\" font-family:'Courier New';\">Debug</span> checkbox just enables additional debug me"
                        "ssages to be printed to the console and to the log file. The <span style=\" font-family:'Courier New';\">Auto Logoff Delay</span> is the amount of time in minutes before the application will automatically logoff the current user (note that this is only valid if <span style=\" font-family:'Courier New';\">Auto Login</span> is disabled). The <span style=\" font-family:'Courier New';\">Chip</span> combobox is used to select the particular chip that is populated on the EAX board. This setting can be changed here or by selecting <span style=\" font-family:'Courier New';\">Chip Select</span> from the settings menu. All the items in the <span style=\" font-family:'Courier New';\">Advanced</span> section should not be changed unless you know what you are doing. These settings modify how the application interacts with the fixture and the firmware.</p>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"../images/SettingsMenu.png\" alt=\""
                        "alt text\" title=\"\" /></p>\n"
"<h3 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">Firmware</span></h3>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The test fixture uses an arduino library called <span style=\" font-family:'Courier New';\">Telemetrix</span>. It can easily be installed to the test fixture using the <span style=\" font-family:'Courier New';\">Arduino</span> IDE, or with the <span style=\" font-family:'Courier New';\">Install.ps1</span> or <span style=\" font-family:'Courier New';\">UpdateFirmware.ps1</span> scripts located in the <span style=\" font-family:'Courier New';\">Scripts</span> folder. To run the script from the GUI, select <span style=\" font-family:'Courier New';\">Update Firmware</span> from the <span style=\" font-family:'Courier New';\">Settings</span> menu. This will attempt to d"
                        "ownload and update the <span style=\" font-family:'Courier New';\">arduino_cli</span> tool, compile the firmware, and upload it to the test fixture. The basic steps for updating the firmware are listed below:</p>\n"
"<ol style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">An internet connection may be required if the necessary files have not already been downloaded.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Ensure that the test fixture is connected to the computer but is not connected to the application.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Open the <span style=\" font-family:'Courier New';\">Settings</span> menu and make sure that <span style=\" font-fam"
                        "ily:'Courier New';\">COM Port</span> and <span style=\" font-family:'Courier New';\">arduino_instance_id</span> are set to the correct values. These will be the values used to upload the firmware. Press <span style=\" font-family:'Courier New';\">Save</span> to save the settings.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">From the <span style=\" font-family:'Courier New';\">Settings</span> menu, select <span style=\" font-family:'Courier New';\">Update Firmware</span>. This will start the firmware update process and its progress will be displayed in the console window. (See the image below)</li></ol>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"../images/FirmwareUpdate.png\" alt=\"alt text\" title=\"\" /></p></body></html>", None))
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
"</style></head><body style=\" font-family:'Segoe UI'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<h1 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:xx-large; font-weight:700;\">Settings</span></h1>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The settings for this application are stored in the windows registry under the key <span style=\" font-family:'Courier New';\">Computer\\Hkey_Current_User\\Software\\Detex Corp\\EAX Interface</span>. Th"
                        "e settings can be modified by clicking on the settings menu item in the main window. The settings can also be edited by opening the registry editor and navigating to the key mentioned above.</p>\n"
"<h3 style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:large; font-weight:700;\">Descriptions for the settings</span></h3>\n"
"<ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\">\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">serial_port: The serial port that is connected to the device. Example: &quot;COM8&quot;.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">programmer_serial_number: The serial number of the programmer. Example: &quot;1E660&quot;.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; marg"
                        "in-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">chip_part: The part number of the chip on the device. Example: &quot;PIC16F627A&quot;.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">last_user: The last user who used the software. Example: &quot;dmh&quot;.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">testing_speed: The speed of testing in Hz. Example: 1584.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">auto_test: If set to true, the software will automatically start testing when it starts up.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">font_family: The font family used for display text. Example: &quot;Segoe UI&quot;.</li>\n"
"<li style=\" margin-top:7px;"
                        " margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">font_size: The size of the font. Example: 12.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">font_weight: The weight of the font. Example: &quot;normal&quot;.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">skip_login: If set to true, the software will not prompt for a user login.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">auto_connect: If set to true, the software will automatically attempt to connect to the device on startup.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">arduino_instance_id: The instance ID of the Arduino software. Example: 15.</li>\n"
"<li style=\" margin-top:7px; "
                        "margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">debug: If set to true, the software will log extra information for debugging purposes.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">firmware_folder: The path to the folder containing the device firmware. If empty, the software will look in the default location.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">inactivity_delay: The delay in minutes before the software will automatically log off the current user. Example: 3.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">bg_color: The background color of the software, specified as a hex color. Example: &quot;#000000&quot;.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-"
                        "indent:0; text-indent:0px;\">fg_color: The foreground color of the software, specified as a hex color. Example: &quot;#ffffff&quot;.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">arduino_wait: The time in seconds to wait for the Arduino software to start. Example: 2.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">shutdown_on_exception: If set to true, the software will automatically shut down if it encounters an exception.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">auto_find: If set to true, the software will automatically find and connect to the device on startup.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">sleep_tune: The delay in seconds to wait for tuning to complete. "
                        "Example: 1e-06.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">firmware_location: The path to the firmware file. Example: &quot;./firmware&quot;.</li>\n"
"<li style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">full_screen: If set to true, the software will start in full screen mode.</li></ul>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">{</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;serial_port&quot;: &quot;COM8&quot;,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier "
                        "New';\">    &quot;programmer_serial_number&quot;: &quot;1E660&quot;,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;chip_part&quot;: &quot;PIC16F628A&quot;,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;last_user&quot;: &quot;dmh&quot;,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;testing_speed&quot;: 0.5,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;auto_test&quot;: true,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bo"
                        "ttom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;font_family&quot;: &quot;Arial&quot;,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;font_size&quot;: 14,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;font_weight&quot;: &quot;normal&quot;,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;font_color&quot;: &quot;#000000&quot;,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'"
                        "Courier New';\">    &quot;skip_login&quot;: true,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;auto_connect&quot;: false,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;arduino_instance_id&quot;: 1,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;debug&quot;: true,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;firmware_folder&quot;: &quot;&quot;,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; mar"
                        "gin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;firmware_location&quot;: &quot;./firmware&quot;,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;shutdown_on_exception&quot;: true,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;auto_find&quot;: true,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;sleep_tune&quot;: 1e-06,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;arduino_w"
                        "ait&quot;: 2,</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">    &quot;full_screen&quot;: false</span></pre>\n"
"<pre style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Courier New';\">}</span></pre>\n"
"<p style=\" margin-top:7px; margin-bottom:7px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><img src=\"../images/SettingsMenu.png\" alt=\"alt text\" title=\"\" /></p></body></html>", None))
        self.textBrowser_settings.setSearchPaths([
            QCoreApplication.translate("HelpDialog", u"images", None),
            QCoreApplication.translate("HelpDialog", u"docs", None)])
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidgetPage6), QCoreApplication.translate("HelpDialog", u"Settings", None))
    # retranslateUi

