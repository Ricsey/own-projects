# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'categories_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTableView, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(737, 874)
        Form.setStyleSheet(u"	#Form QLabel {\n"
"		color: white;\n"
"	}\n"
"\n"
"	/* style for QPushButton */\n"
"	#Form QPushButton {\n"
"		border:none;\n"
"		border-radius: 3px;\n"
"		text-align: left;\n"
"		padding: 8px 0 8px 15px;\n"
"		color: #788596;\n"
"	}\n"
"\n"
"	#Form QPushButton:hover {\n"
"		background-color: rgba( 86, 101, 115, 0.5);\n"
"	}\n"
"\n"
"	#Form QPushButton:checked {\n"
"		background-color: rgba( 86, 101, 115, 0.5);\n"
"		color: #fff;\n"
"	}\n"
"\n"
"QTableView {\n"
"	color: white;\n"
"	background-color: #313a46;\n"
"}\n"
"\n"
"QTableView::Item {\n"
"	border-bottom: 2px solid #222b31;\n"
"	color: white;\n"
"	padding-left: 3px;\n"
"}\n"
"\n"
"")
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_5)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.comboBox = QComboBox(self.frame_5)
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout_2.addWidget(self.comboBox)


        self.verticalLayout.addWidget(self.frame_5)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_4)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(0)
        self.gridLayout.setVerticalSpacing(2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.categorysum_label = QLabel(self.frame_4)
        self.categorysum_label.setObjectName(u"categorysum_label")

        self.gridLayout.addWidget(self.categorysum_label, 1, 0, 1, 1)

        self.categoryname_label = QLabel(self.frame_4)
        self.categoryname_label.setObjectName(u"categoryname_label")

        self.gridLayout.addWidget(self.categoryname_label, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.frame_4)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_10 = QFrame(self.frame_3)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(50, 0))
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_10)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tableView = QTableView(self.frame_10)
        self.tableView.setObjectName(u"tableView")

        self.gridLayout_2.addWidget(self.tableView, 0, 0, 1, 1)


        self.horizontalLayout_3.addWidget(self.frame_10)

        self.frame_9 = QFrame(self.frame_3)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(0, 0))
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_9)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.pushButton = QPushButton(self.frame_9)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QSize(0, 0))
        icon = QIcon()
        icon.addFile(u":/icons/icons/download-2-32.ico", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(12, 12))

        self.verticalLayout_5.addWidget(self.pushButton, 0, Qt.AlignLeft)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)


        self.horizontalLayout_3.addWidget(self.frame_9)


        self.verticalLayout.addWidget(self.frame_3)

        self.frame_8 = QFrame(self.frame)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_8)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.frame_8)
        self.label_5.setObjectName(u"label_5")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label_5.setFont(font)

        self.verticalLayout_3.addWidget(self.label_5)


        self.verticalLayout.addWidget(self.frame_8)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_7 = QFrame(self.frame_2)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setSpacing(2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_7)
        self.label.setObjectName(u"label")

        self.verticalLayout_6.addWidget(self.label)

        self.label_2 = QLabel(self.frame_7)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_6.addWidget(self.label_2)

        self.label_3 = QLabel(self.frame_7)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_6.addWidget(self.label_3)

        self.label_4 = QLabel(self.frame_7)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_6.addWidget(self.label_4)


        self.horizontalLayout.addWidget(self.frame_7)

        self.frame_6 = QFrame(self.frame_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_6)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tran_type = QLabel(self.frame_6)
        self.tran_type.setObjectName(u"tran_type")

        self.verticalLayout_4.addWidget(self.tran_type)

        self.tran_date = QLabel(self.frame_6)
        self.tran_date.setObjectName(u"tran_date")

        self.verticalLayout_4.addWidget(self.tran_date)

        self.tran_amount = QLabel(self.frame_6)
        self.tran_amount.setObjectName(u"tran_amount")

        self.verticalLayout_4.addWidget(self.tran_amount)

        self.tran_name = QLabel(self.frame_6)
        self.tran_name.setObjectName(u"tran_name")

        self.verticalLayout_4.addWidget(self.tran_name)


        self.horizontalLayout.addWidget(self.frame_6)


        self.verticalLayout.addWidget(self.frame_2, 0, Qt.AlignLeft)


        self.horizontalLayout_2.addWidget(self.frame)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.categorysum_label.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.categoryname_label.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"Import    ", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Tranzakci\u00f3", None))
        self.label.setText(QCoreApplication.translate("Form", u"N\u00e9v:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"D\u00e1tum:", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u00d6sszeg:", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"T\u00edpus:", None))
        self.tran_type.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.tran_date.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.tran_amount.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.tran_name.setText(QCoreApplication.translate("Form", u"TextLabel", None))
    # retranslateUi

