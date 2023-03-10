# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'setup.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogSetup(object):
    def setupUi(self, DialogSetup):
        DialogSetup.setObjectName("DialogSetup")
        DialogSetup.setWindowModality(QtCore.Qt.ApplicationModal)
        DialogSetup.resize(440, 300)
        DialogSetup.setMinimumSize(QtCore.QSize(440, 300))
        DialogSetup.setMaximumSize(QtCore.QSize(440, 300))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        DialogSetup.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icon_32x32_1x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogSetup.setWindowIcon(icon)
        DialogSetup.setModal(True)
        self.layoutWidget = QtWidgets.QWidget(DialogSetup)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 416, 285))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEditEmailAddress = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        self.lineEditEmailAddress.setFont(font)
        self.lineEditEmailAddress.setInputMethodHints(QtCore.Qt.ImhEmailCharactersOnly)
        self.lineEditEmailAddress.setInputMask("")
        self.lineEditEmailAddress.setText("")
        self.lineEditEmailAddress.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.lineEditEmailAddress.setPlaceholderText("")
        self.lineEditEmailAddress.setObjectName("lineEditEmailAddress")
        self.gridLayout.addWidget(self.lineEditEmailAddress, 2, 2, 1, 1)
        self.labelPhoneNumber = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        font.setKerning(True)
        self.labelPhoneNumber.setFont(font)
        self.labelPhoneNumber.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.labelPhoneNumber.setObjectName("labelPhoneNumber")
        self.gridLayout.addWidget(self.labelPhoneNumber, 0, 0, 1, 2)
        self.labelEmailSendingAccountPassword = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        self.labelEmailSendingAccountPassword.setFont(font)
        self.labelEmailSendingAccountPassword.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.labelEmailSendingAccountPassword.setObjectName("labelEmailSendingAccountPassword")
        self.gridLayout.addWidget(self.labelEmailSendingAccountPassword, 3, 0, 1, 2)
        self.labelNameToUseWhenTextsAreSent = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        self.labelNameToUseWhenTextsAreSent.setFont(font)
        self.labelNameToUseWhenTextsAreSent.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.labelNameToUseWhenTextsAreSent.setObjectName("labelNameToUseWhenTextsAreSent")
        self.gridLayout.addWidget(self.labelNameToUseWhenTextsAreSent, 4, 0, 1, 2)
        self.lineEditPhoneNumber = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        self.lineEditPhoneNumber.setFont(font)
        self.lineEditPhoneNumber.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.lineEditPhoneNumber.setInputMask("")
        self.lineEditPhoneNumber.setText("")
        self.lineEditPhoneNumber.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.lineEditPhoneNumber.setDragEnabled(True)
        self.lineEditPhoneNumber.setPlaceholderText("")
        self.lineEditPhoneNumber.setObjectName("lineEditPhoneNumber")
        self.gridLayout.addWidget(self.lineEditPhoneNumber, 0, 2, 1, 1)
        self.labelTimeIntervalBetweenIPChecks = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        self.labelTimeIntervalBetweenIPChecks.setFont(font)
        self.labelTimeIntervalBetweenIPChecks.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.labelTimeIntervalBetweenIPChecks.setObjectName("labelTimeIntervalBetweenIPChecks")
        self.gridLayout.addWidget(self.labelTimeIntervalBetweenIPChecks, 6, 0, 1, 2)
        self.spinBoxTimeIntervalBetweenIPChecks = QtWidgets.QSpinBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxTimeIntervalBetweenIPChecks.sizePolicy().hasHeightForWidth())
        self.spinBoxTimeIntervalBetweenIPChecks.setSizePolicy(sizePolicy)
        self.spinBoxTimeIntervalBetweenIPChecks.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBoxTimeIntervalBetweenIPChecks.setMinimum(24)
        self.spinBoxTimeIntervalBetweenIPChecks.setMaximum(168)
        self.spinBoxTimeIntervalBetweenIPChecks.setSingleStep(24)
        self.spinBoxTimeIntervalBetweenIPChecks.setObjectName("spinBoxTimeIntervalBetweenIPChecks")
        self.gridLayout.addWidget(self.spinBoxTimeIntervalBetweenIPChecks, 6, 2, 1, 1)
        self.comboBoxSelectedSMSGateway = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxSelectedSMSGateway.sizePolicy().hasHeightForWidth())
        self.comboBoxSelectedSMSGateway.setSizePolicy(sizePolicy)
        self.comboBoxSelectedSMSGateway.setMinimumSize(QtCore.QSize(120, 26))
        self.comboBoxSelectedSMSGateway.setMaximumSize(QtCore.QSize(120, 26))
        self.comboBoxSelectedSMSGateway.setObjectName("comboBoxSelectedSMSGateway")
        self.gridLayout.addWidget(self.comboBoxSelectedSMSGateway, 5, 2, 1, 1)
        self.pushButtonTest = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButtonTest.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonTest.sizePolicy().hasHeightForWidth())
        self.pushButtonTest.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        self.pushButtonTest.setFont(font)
        self.pushButtonTest.setObjectName("pushButtonTest")
        self.gridLayout.addWidget(self.pushButtonTest, 9, 0, 1, 1)
        self.lineEditEmailSendingAccountPassword = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        self.lineEditEmailSendingAccountPassword.setFont(font)
        self.lineEditEmailSendingAccountPassword.setInputMethodHints(QtCore.Qt.ImhEmailCharactersOnly|QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.lineEditEmailSendingAccountPassword.setInputMask("")
        self.lineEditEmailSendingAccountPassword.setText("")
        self.lineEditEmailSendingAccountPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEditEmailSendingAccountPassword.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.lineEditEmailSendingAccountPassword.setPlaceholderText("")
        self.lineEditEmailSendingAccountPassword.setObjectName("lineEditEmailSendingAccountPassword")
        self.gridLayout.addWidget(self.lineEditEmailSendingAccountPassword, 3, 2, 1, 1)
        self.labelSMTPServer = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        self.labelSMTPServer.setFont(font)
        self.labelSMTPServer.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.labelSMTPServer.setObjectName("labelSMTPServer")
        self.gridLayout.addWidget(self.labelSMTPServer, 1, 0, 1, 2)
        self.lineEditSMTPServer = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        self.lineEditSMTPServer.setFont(font)
        self.lineEditSMTPServer.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEditSMTPServer.setInputMask("")
        self.lineEditSMTPServer.setText("")
        self.lineEditSMTPServer.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.lineEditSMTPServer.setPlaceholderText("")
        self.lineEditSMTPServer.setObjectName("lineEditSMTPServer")
        self.gridLayout.addWidget(self.lineEditSMTPServer, 1, 2, 1, 1)
        self.labelEmailAddress = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        self.labelEmailAddress.setFont(font)
        self.labelEmailAddress.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.labelEmailAddress.setObjectName("labelEmailAddress")
        self.gridLayout.addWidget(self.labelEmailAddress, 2, 0, 1, 2)
        self.lineEditNameToUseWhenTextsAreSent = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        self.lineEditNameToUseWhenTextsAreSent.setFont(font)
        self.lineEditNameToUseWhenTextsAreSent.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEditNameToUseWhenTextsAreSent.setInputMask("")
        self.lineEditNameToUseWhenTextsAreSent.setText("")
        self.lineEditNameToUseWhenTextsAreSent.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.lineEditNameToUseWhenTextsAreSent.setPlaceholderText("")
        self.lineEditNameToUseWhenTextsAreSent.setObjectName("lineEditNameToUseWhenTextsAreSent")
        self.gridLayout.addWidget(self.lineEditNameToUseWhenTextsAreSent, 4, 2, 1, 1)
        self.labelSelectedSMSGateway = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(10)
        self.labelSelectedSMSGateway.setFont(font)
        self.labelSelectedSMSGateway.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.labelSelectedSMSGateway.setObjectName("labelSelectedSMSGateway")
        self.gridLayout.addWidget(self.labelSelectedSMSGateway, 5, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 9, 2, 1, 1)
        self.labelPhoneNumber.setBuddy(self.lineEditPhoneNumber)
        self.labelEmailSendingAccountPassword.setBuddy(self.lineEditEmailSendingAccountPassword)
        self.labelNameToUseWhenTextsAreSent.setBuddy(self.lineEditNameToUseWhenTextsAreSent)
        self.labelTimeIntervalBetweenIPChecks.setBuddy(self.spinBoxTimeIntervalBetweenIPChecks)
        self.labelSMTPServer.setBuddy(self.lineEditSMTPServer)
        self.labelEmailAddress.setBuddy(self.lineEditEmailAddress)
        self.labelSelectedSMSGateway.setBuddy(self.comboBoxSelectedSMSGateway)

        self.retranslateUi(DialogSetup)
        self.buttonBox.accepted.connect(DialogSetup.accept) # type: ignore
        self.buttonBox.rejected.connect(DialogSetup.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DialogSetup)
        DialogSetup.setTabOrder(self.lineEditPhoneNumber, self.lineEditSMTPServer)
        DialogSetup.setTabOrder(self.lineEditSMTPServer, self.lineEditEmailAddress)
        DialogSetup.setTabOrder(self.lineEditEmailAddress, self.lineEditEmailSendingAccountPassword)
        DialogSetup.setTabOrder(self.lineEditEmailSendingAccountPassword, self.lineEditNameToUseWhenTextsAreSent)
        DialogSetup.setTabOrder(self.lineEditNameToUseWhenTextsAreSent, self.comboBoxSelectedSMSGateway)
        DialogSetup.setTabOrder(self.comboBoxSelectedSMSGateway, self.spinBoxTimeIntervalBetweenIPChecks)
        DialogSetup.setTabOrder(self.spinBoxTimeIntervalBetweenIPChecks, self.pushButtonTest)

    def retranslateUi(self, DialogSetup):
        _translate = QtCore.QCoreApplication.translate
        DialogSetup.setWindowTitle(_translate("DialogSetup", "Setup"))
        self.labelPhoneNumber.setText(_translate("DialogSetup", "P&hone Number to Send Texts to:"))
        self.labelEmailSendingAccountPassword.setText(_translate("DialogSetup", "Email Sending Account &Password"))
        self.labelNameToUseWhenTextsAreSent.setText(_translate("DialogSetup", "&Name to Use When Texts Are Sent"))
        self.labelTimeIntervalBetweenIPChecks.setText(_translate("DialogSetup", "Select &Time Between IP Checks"))
        self.spinBoxTimeIntervalBetweenIPChecks.setSuffix(_translate("DialogSetup", " Hours"))
        self.pushButtonTest.setToolTip(_translate("DialogSetup", "Push to test your settings by sending a text message"))
        self.pushButtonTest.setText(_translate("DialogSetup", "Test"))
        self.labelSMTPServer.setText(_translate("DialogSetup", "&SMTP Server Address for Sending Texts"))
        self.labelEmailAddress.setText(_translate("DialogSetup", "&Email Address to Send Texts From"))
        self.labelSelectedSMSGateway.setText(_translate("DialogSetup", "Selected SMS &Gateway"))
import resources_rc
