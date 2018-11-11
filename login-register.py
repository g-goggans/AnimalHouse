#!/usr/bin/env python3

import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    qApp,
    QAction,
    QTabWidget,
    QFileDialog,
    QTableView,
    QPushButton,
    QVBoxLayout,
    QListView,
    QLineEdit,
    QGridLayout,
    QComboBox,
    QGroupBox,
    QListWidget,
    QMessageBox,
    QFormLayout,
    QDialog,
    QLayout,
    QHBoxLayout,
    QGridLayout
)
from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem
)
from PyQt5.QtCore import (
    Qt,
    QAbstractTableModel,
    QVariant
)
from PyQt5.QtSql import (
    QSqlDatabase,
    QSqlQuery,
    QSqlQueryModel
)

import PyQt5.QtGui
import pymysql

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Login")
        makewin = self.login()

    def login(self):



        self.user_line_edit = QLineEdit()
        self.password_line_edit = QLineEdit()

        self.register_button = QPushButton("Register")
        self.register_button.setEnabled(True)
        self.login_button = QPushButton("Login")
        self.login_button.setEnabled(False)

        self.register_button.clicked.connect(self.go_to_register)
        self.user_line_edit.textChanged.connect(self.enable_login_button)

        self.vbox = QVBoxLayout()
        userlbl = QLabel()
        userlbl.setText("Username")
        passlbl = QLabel()
        passlbl.setText("Password")

        self.vbox.addWidget(userlbl)
        self.vbox.addWidget(self.user_line_edit)
        self.vbox.addWidget(passlbl)
        self.vbox.addWidget(self.password_line_edit)
        self.vbox.addWidget(self.login_button)
        self.vbox.addWidget(self.register_button)
        self.setLayout(self.vbox)


    def go_to_register(self):
        # app = QApplication(sys.argv)
        # w = QWidget()
        # reg_button = QPushButton(w)
        regLayout = QGridLayout()
        # # reg_button.clicked.connect()
        # w.setWindowTitle("Registration")

        self.db = self.Connect()
        self.c = self.db.cursor()

        self.email = QLabel('Email:')
        self.wemail  = QLineEdit()
        self.user = QLabel('Username')
        self.wuser = QLineEdit()
        self.pswd = QLabel('Password:')
        self.wpswd  =QLineEdit()
        self.confirmpswd = QLabel('Confirm Password:')
        self.wconfirmpswd  = QLineEdit()

        self.RegVisitor = QPushButton('Register Visitor')
        self.RegStaff = QPushButton('Register Staff')

        regLayout = QGridLayout()
        regLayout.setColumnStretch(1,3)
        regLayout.setRowStretch(1,3)

        regLayout.addWidget(self.email,1,0)
        regLayout.addWidget(self.wemail, 1,1)
        regLayout.addWidget(self.user,2,0)
        regLayout.addWidget(self.wuser, 2,1)
        regLayout.addWidget(self.pswd,3,0)
        regLayout.addWidget(self.wpswd, 3,1)
        regLayout.addWidget(self.confirmpswd,4,0)
        regLayout.addWidget(self.wconfirmpswd, 4,1)
        regLayout.addWidget(self.RegVisitor,5,0)
        regLayout.addWidget(self.RegStaff,5,1)

        self.RegVisitor.clicked.connect(self.register_visitor)
        self.RegStaff.clicked.connect(self.register_staff)

        #w.show()
        self.go_to_register = QDialog()
        self.go_to_register.setLayout(regLayout)
        self.go_to_register.setWindowTitle('Register')
        self.go_to_register.show()



        # vbox = QWidget()
        #
        # vbox.email_line_edit = QLineEdit()
        # # self.user_line_edit = QLineEdit()
        # # self.password_line_edit = QLineEdit()
        # # self.conf_password_line_edit = QLineEdit()
        # #
        # self.vbox.setWindowTitle("Registration")
        # emaillbl = QLabel()
        # emaillbl.setText("Email")
        # # userlbl = QLabel()
        # # userlbl.setText("Username")
        # # passlbl = QLabel()
        # # passlbl.setText("Password")
        # # confpasslbl = QLabel()
        # # confpasslbl.setText("Confirm Password")
        # #
        # self.vbox.addWidget(emaillbl)
        # self.vbox.addWidget(self.email_line_edit)
        # # self.vbox.addWidget(userlbl)
        # # self.vbox.addWidget(self.user_line_edit)
        # # self.vbox.addWidget(passlbl)
        # # self.vbox.addWidget(self.password_line_edit)
        # # self.vbox.addWidget(confpasslbl)
        # # self.vbox.addWidget(self.conf_password_line_edit)
        # #
        # vbox.setWindowModality(Qt.ApplicationModal)
        # vbox.exec_()


    def register_visitor(self):

        self.email = str(self.wemail.text())
        self.user = str(self.wuser.text())
        self.pswd = str(self.wpswd.text())
        #check for confirm

        print(self.email)
        print(self.user)
        print(self.pswd)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("INSERT INTO USERS VALUES (%s,%s,%s,%s)",(self.email,self.user,self.pswd,"visitor"))
        #self.db.commit()


    def register_staff(self):

        self.email = str(self.wemail.text())
        self.user = str(self.wuser.text())
        self.pswd = str(self.wpswd.text())
        #check for confirm

        print(self.email)
        print(self.user)
        print(self.pswd)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("INSERT INTO USERS VALUES (%s,%s,%s,%s)",(self.email,self.user,self.pswd,"staff"))


    def enable_login_button(self):
        if len(self.password_line_edit.text()) < 8:
            self.login_button.setEnabled(False)
        else:
            self.login_button.setEnabled(True)

    def enable_register_button(self):
        if (len(self.password_line_edit.text()) < 8 or len(self.user_line_edit.text()) == 0):
            self.login_button.setEnabled(False)
        else:
            self.login_button.setEnabled(True)

    def Connect(self):
        try:
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_group4", passwd = "2jILwMuE", db="cs4400_group4")
            self.db = db
            db.autocommit(True)
            return db

        except:
            messagebox.showwarning("Error", "Check Internet Connection")


if __name__=='__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
