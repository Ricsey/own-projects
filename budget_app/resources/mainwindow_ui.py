# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet(u"#MainWindow {\n"
"	background-color: #313a46;\n"
"}\n"
"\n"
"	#MainWindow QPushButton, QLabel {\n"
"		height:32px;\n"
"		border:none;\n"
"		/* border-bottom: 1px solid #b0b0b0; */\n"
"		color: rgb(182, 182, 182)\n"
"	}\n"
"\n"
"	#MainWindow QPushButton:hover {\n"
"		background-color: rgba( 86, 101, 115, 0.5);\n"
"		color: #fff;\n"
"	}\n"
"\n"
"	#MainWindow QPushButton:checked {\n"
"		background-color: rgba( 86, 101, 115, 0.5);\n"
"		color: #fff;\n"
"	}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(150, 16777215))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.summary_button = QPushButton(self.frame)
        self.summary_button.setObjectName(u"summary_button")
        self.summary_button.setCheckable(True)
        self.summary_button.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.summary_button)

        self.ricsi_transactions_button = QPushButton(self.frame)
        self.ricsi_transactions_button.setObjectName(u"ricsi_transactions_button")
        self.ricsi_transactions_button.setCheckable(True)
        self.ricsi_transactions_button.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.ricsi_transactions_button)

        self.eszti_transactions_button = QPushButton(self.frame)
        self.eszti_transactions_button.setObjectName(u"eszti_transactions_button")
        self.eszti_transactions_button.setCheckable(True)
        self.eszti_transactions_button.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.eszti_transactions_button)

        self.category_manager_button = QPushButton(self.frame)
        self.category_manager_button.setObjectName(u"category_manager_button")
        self.category_manager_button.setCheckable(True)
        self.category_manager_button.setAutoExclusive(True)

        self.verticalLayout.addWidget(self.category_manager_button)

        self.verticalSpacer = QSpacerItem(20, 387, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.stackedWidget = QStackedWidget(self.frame_2)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.horizontalLayout_2.addWidget(self.stackedWidget)


        self.horizontalLayout.addWidget(self.frame_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setEnabled(False)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.summary_button.setText(QCoreApplication.translate("MainWindow", u"Summary", None))
        self.ricsi_transactions_button.setText(QCoreApplication.translate("MainWindow", u"Ricsi transactions", None))
        self.eszti_transactions_button.setText(QCoreApplication.translate("MainWindow", u"Eszti transactions", None))
        self.category_manager_button.setText(QCoreApplication.translate("MainWindow", u"Categories", None))
    # retranslateUi

