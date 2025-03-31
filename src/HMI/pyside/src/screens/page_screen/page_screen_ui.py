# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'page_screen.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(821, 668)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.border_left = QWidget(Form)
        self.border_left.setObjectName(u"border_left")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.border_left.sizePolicy().hasHeightForWidth())
        self.border_left.setSizePolicy(sizePolicy)
        self.border_left.setStyleSheet(u"background-color: rgb(121, 111, 111);")

        self.horizontalLayout.addWidget(self.border_left)

        self.page_container = QWidget(Form)
        self.page_container.setObjectName(u"page_container")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(4)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.page_container.sizePolicy().hasHeightForWidth())
        self.page_container.setSizePolicy(sizePolicy1)
        self.page_container.setStyleSheet(u"background-color: rgb(255, 243, 243);")
        self.horizontalLayout_2 = QHBoxLayout(self.page_container)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.horizontalLayout.addWidget(self.page_container)

        self.border_right = QWidget(Form)
        self.border_right.setObjectName(u"border_right")
        sizePolicy.setHeightForWidth(self.border_right.sizePolicy().hasHeightForWidth())
        self.border_right.setSizePolicy(sizePolicy)
        self.border_right.setStyleSheet(u"background-color: rgb(121, 111, 111);")

        self.horizontalLayout.addWidget(self.border_right)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi

