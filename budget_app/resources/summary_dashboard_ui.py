# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'summary_dashboard.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(933, 750)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.BalanceFrame = QFrame(self.widget)
        self.BalanceFrame.setObjectName(u"BalanceFrame")
        self.BalanceFrame.setFrameShape(QFrame.StyledPanel)
        self.BalanceFrame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.BalanceFrame)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.balanceChartFrame = QFrame(self.BalanceFrame)
        self.balanceChartFrame.setObjectName(u"balanceChartFrame")
        self.balanceChartFrame.setFrameShape(QFrame.StyledPanel)
        self.balanceChartFrame.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.balanceChartFrame, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.BalanceFrame)

        self.MonthlyExpenseFrame = QFrame(self.widget)
        self.MonthlyExpenseFrame.setObjectName(u"MonthlyExpenseFrame")
        self.MonthlyExpenseFrame.setFrameShape(QFrame.StyledPanel)
        self.MonthlyExpenseFrame.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.MonthlyExpenseFrame)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi

