#!/usr/bin/env python3

import sys

import tkinter as tk
from tkinter import *
import tkinter.messagebox as messagebox

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

import pymysql
#stops annoyting tkinter pop ups
root = Tk()
root.withdraw()

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Login")
        makewin = self.login()

    def login(self):
#Creating the first page for login information
        self.user_line_edit = QLineEdit()
        self.password_line_edit = QLineEdit()

        self.register_button = QPushButton("Register")
        self.register_button.setEnabled(True)
        self.login_button = QPushButton("Login")
        self.login_button.setEnabled(True)

        self.register_button.clicked.connect(self.go_to_register)
        self.login_button.clicked.connect(self.check_user)
        # self.user_line_edit.textChanged.connect(self.enable_login_button)

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

    # check_user currently can only display the tuple from our database from which we query the row that matches the user and the password
    def check_user(self):
        user = str(self.user_line_edit.text())
        pswd = str(self.password_line_edit.text())

        self.db = self.Connect()
        self.c = self.db.cursor()

        # tuple for logged in user
        self.c.execute("SELECT * FROM USERS AS U WHERE U.username=%s AND U.password=%s",(user,pswd))
        if (self.c.fetchall()):

            currentuser = QLabel() # this will display the tuple of the sql statement
            mystr = "" # turns the tuple into a string for printing
            for i in self.c.fetchall():
                mystr += str(i)
            currentuser.setText(mystr)
            vbox = QVBoxLayout()
            vbox.addStretch(1)
            vbox.addWidget(currentuser)
            self.newWindow = TableWindow()
            self.newWindow.setLayout(vbox)
            self.newWindow.show()
            ok = QPushButton("Ok")
            ok.clicked.connect(self.newWindow.close)
            vbox.addWidget(ok)

        else:
            messagebox.showwarning("Error", "Username or password incorrect")


    def go_to_register(self):
#creating the registration page

        regLayout = QGridLayout()

        self.db = self.Connect()
        self.c = self.db.cursor()

#Labels for registration information
        self.email = QLabel('Email:')
        self.wemail  = QLineEdit()
        self.user = QLabel('Username')
        self.wuser = QLineEdit()
        self.pswd = QLabel('Password:')
        self.wpswd  =QLineEdit()
        self.confirmpswd = QLabel('Confirm Password:')
        self.wconfirmpswd  = QLineEdit()

#Creating the buttons for registering staff or visitors
        self.RegVisitor = QPushButton('Register Visitor')
        self.RegStaff = QPushButton('Register Staff')

        regLayout = QGridLayout()
        regLayout.setColumnStretch(1,3)
        regLayout.setRowStretch(1,3)

#Boxes for registration information
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

#Using the register_visitor and register_staff functions to upload/check the info into the database
        self.RegVisitor.clicked.connect(self.register_visitor)
        self.RegStaff.clicked.connect(self.register_staff)

        self.go_to_register = QDialog()
        self.go_to_register.setLayout(regLayout)
        self.go_to_register.setWindowTitle('Register')
        self.go_to_register.show()


    def register_visitor(self):
#getting data from the registration page
        self.email = str(self.wemail.text())
        self.user = str(self.wuser.text())
        self.pswd = str(self.wpswd.text())
        self.confirmpswd = str(self.wconfirmpswd.text())

        self.db = self.Connect()
        self.c = self.db.cursor()
        printstr = ""
        count = 0

#conducting checks for registration information for visitors
        if len(self.pswd) < 8:
            #print("Password needs to be more than 8 characters")
            printstr += "Password needs to be more than 8 characters\n"
            count+=1

        if self.confirmpswd != self.pswd:
            #print("Password must match Confirm Password")
            printstr += "Password must match Confirm Password\n"
            count+=1

        if "@" not in self.email or "." not in self.email:
            #print("Email must meet email format with @ and . symbols")
            printstr += "Email must meet email format with @ and . symbols\n"
            count+=1

        if count > 0:
            messagebox.showwarning("Error", printstr)

#adding the visitor to the database
        else:
            self.c.execute("INSERT INTO USERS VALUES (%s,%s,%s,%s)",(self.email,self.user,self.pswd,"visitor"))

        self.go_to_register.close()


    def register_staff(self):
#getting information from the registration page for staff registration
        self.email = str(self.wemail.text())
        self.user = str(self.wuser.text())
        self.pswd = str(self.wpswd.text())
        self.confirmpswd = str(self.wconfirmpswd.text())
        #check for confirm

        self.db = self.Connect()
        self.c = self.db.cursor()
        printstr = ""
        count = 0

#conducting checks for registration information for staff
        if len(self.pswd) < 8:
            #print("Password needs to be more than 8 characters")
            printstr += "Password needs to be more than 8 characters\n"
            count+=1

        if self.confirmpswd != self.pswd:
            #print("Password must match Confirm Password")
            printstr += "Password must match Confirm Password\n"
            count+=1

        if "@" not in self.email or "." not in self.email:
            #print("Email must meet email format with @ and . symbols")
            printstr += "Email must meet email format with @ and . symbols\n"
            count+=1

        if count > 0:
            messagebox.showwarning("Error", printstr)

#adding the staff to the database
        else:
            self.c.execute("INSERT INTO USERS VALUES (%s,%s,%s,%s)",(self.email,self.user,self.pswd,"staff"))

        self.go_to_register.close()


    def Connect(self):
#Connecting to the database, function used in multiple other areas around the code
        try:
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_group4", passwd = "2jILwMuE", db="cs4400_group4")
            self.db = db
            db.autocommit(True)
            return db

        except:
            messagebox.showwarning("Error", "Check Internet Connection")

class TableWindow(QWidget):
    def __init__(self):
        super(TableWindow, self).__init__()
        self.setWindowTitle('Table Data')
        self.vbox = QVBoxLayout()

if __name__=='__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
    
    
#import sqlite3
# import sys
# import tkinter as tk
# from tkinter import *
# import tkinter.messagebox as messagebox

# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *
# from PyQt5.QtSql import *

# import PyQt5.QtGui
# import pymysql
# #stops annoyting tkinter pop ups
# root = Tk()
# root.withdraw()

# class MainWindow(QWidget):

#     def __init__(self):
#         super(MainWindow, self).__init__()
#         self.setWindowTitle('Atlanta Zoo')
#         makewin = self.visitor_functionality()
       

#     def visitor_functionality(self):
# #buttons that appear on main page
#         self.SearchExhibits = QPushButton("Seach Exhibits")
#         self.SearchShows = QPushButton("Seach Shows")
#         self.SearchAnimals = QPushButton("Search for Animals")
#         self.ViewExhibit = QPushButton("View Exhibit History")
#         self.ViewShow = QPushButton("View Show History")
#         self.LogOut = QPushButton("Log Out")

# #layout of page
#         layout = QGridLayout()
#         layout.setColumnStretch(1,3)
#         layout.setRowStretch(1,3)

# #placement layout of page
#         layout.addWidget(self.SearchExhibits,1,0)
#         layout.addWidget(self.ViewExhibit, 1,1)
#         layout.addWidget(self.SearchShows,2,0)
#         layout.addWidget(self.ViewShow, 2,1)
#         layout.addWidget(self.SearchAnimals,3,0)
#         layout.addWidget(self.LogOut, 3,1)

# #button connections
#         self.SearchExhibits.clicked.connect(self.search_exhibits)
#         self.SearchShows.clicked.connect(self.search_shows)
#         self.SearchAnimals.clicked.connect(self.search_animals)

#         self.setLayout(layout)
#         self.show()

        

#     def search_exhibits(self):
#         self.setWindowTitle('Exhibits')
#         SElayout = QGridLayout()

#         self.search = QPushButton("search")
#         self.name = QLabel("Name: ")
#         self.wname = QLineEdit()
#         self.NumAnimals = QLabel("Number of Animals")
#         self.animalMin = QLabel("Min")
#         self.animalMax = QLabel("Max")
#         self.wanimalMin = QLineEdit()
#         self.wanimalMax = QLineEdit()
#         self.Size = QLabel("Size")
#         self.sizeMin = QLabel("Min")
#         self.sizeMax = QLabel("Max")
#         self.wsizeMin = QLineEdit()
#         self.wsizeMax = QLineEdit()
#         self.Water = QLabel("Water Feature")
#         self.waterDrop = QComboBox()
        
#         self.waterDrop.addItems(["","Yes","No"])
#         self.db = self.Connect()
#         self.c = self.db.cursor()
#         self.c.execute("SELECT * FROM EXHIBITS")
#         result = self.c.fetchall()
#         #print(result)

#         self.table = QTableView()
#         self.model = QStandardItemModel()
#         self.model.setColumnCount(4)
#         headerNames = ["Exhibit Name", "Water", "Number of Animals", "Size"]
#         self.model.setHorizontalHeaderLabels(headerNames)

#         for i in result:
#             row = []
#             for j in i:  #converts item to list from tuple
#                 item = QStandardItem(str(j)) #has to be converted to string in order to work
#                 item.setEditable(False)
#                 row.append(item)
#                 #print(row)
#             self.model.appendRow(row)

#         self.table.setModel(self.model)

#         SElayout = QGridLayout()
#         SElayout.setColumnStretch(1,3)
#         SElayout.setRowStretch(1,3)

#         SElayout.addWidget(self.search,1,3)
#         SElayout.addWidget(self.name, 2,0)
#         SElayout.addWidget(self.wname,2,1)
#         SElayout.addWidget(self.NumAnimals, 4,0)
#         SElayout.addWidget(self.animalMin,3,1)
#         SElayout.addWidget(self.animalMax,3,2)
#         SElayout.addWidget(self.wanimalMin,4,1)
#         SElayout.addWidget(self.wanimalMax,4,2)
#         SElayout.addWidget(self.sizeMin,5,1)
#         SElayout.addWidget(self.sizeMax,5,2)
#         SElayout.addWidget(self.Size,6,0)
#         SElayout.addWidget(self.wsizeMin,6,1)
#         SElayout.addWidget(self.wsizeMax,6,2)
#         SElayout.addWidget(self.Water, 7,0)
#         SElayout.addWidget(self.waterDrop, 7,1)

#         SElayout.addWidget(self.table,8,0,4,4)

#         self.search_exhibits = QDialog()
#         self.search_exhibits.setLayout(SElayout)
#         self.search_exhibits.show()

#         self.search.clicked.connect(self.exhibitSearch)

#     def exhibitSearch(self):
#         self.animalMin = str(self.wanimalMin.text())
#         self.animalMax = str(self.wanimalMax.text())
#         self.sizeMin = str(self.wsizeMin.text())
#         self.sizeMax = str(self.wsizeMax.text())
#         printstr = ""
#         count = 0
#         count2 = 0

#         try:
#             self.animalMin = int(str(self.wanimalMin.text()))
#         except:
#             printstr += "- input for min animal number must be integer\n"
#             count += 1
#         try:
#             self.animalMax = int(str(self.wanimalMax.text()))
#         except:
#             printstr += "- input for max animal number must be integer\n"
#             count += 1
#         if count == 0:
#             if (self.animalMin > self.animalMax):
#                 printstr += "- min animals must be less than max animals\n"
#                 count += 1
#         try:
#             self.sizeMin = int(str(self.wsizeMin.text()))
#         except:
#             printstr += "- input for min size must be integer\n"
#             count2 += 1
#         try:
#             self.sizeMax = int(str(self.wsizeMax.text()))
#         except:
#             printstr += "- input for max size must be integer\n"
#             count2 += 1
#         if count2 == 0:
#             if (self.sizeMin > self.sizeMax):
#                 printstr += "- min size must be less than max size\n"
#                 count2 += 1
#         if ((count == 0) and (count2 == 0)):
#             print("here")
#         else: 
#             messagebox.showwarning("Error", printstr)
#             #print(printstr)

#     def search_shows(self):
#         self.setWindowTitle('Shows')
#         SSlayout = QGridLayout()

#         self.title1 = QLabel("Atalnta Zoo")
#         self.title2 = QLabel("Shows")       
#         self.search = QPushButton("search")
#         self.name = QLabel("Name: ")
#         self.wname = QLineEdit()
#         self.date = QLabel("Date: ")
#         self.dateDrop = QComboBox() #this is wrong implementation
#         self.exhibit = QLabel("Exhibit: ")
#         self.exhibitDrop = QComboBox()
#         self.logVisit = QPushButton("Log Visit")
#         self.table = QTableView()
#         self.model = QStandardItemModel()
#         self.model.setColumnCount(3)
#         headerNames = ["Name", "Exhibit", "Date"]
#         self.model.setHorizontalHeaderLabels(headerNames)

#         self.db = self.Connect()
#         self.c = self.db.cursor()
#         self.c.execute("SELECT exhibit_name FROM EXHIBITS")
        
#         #exhibit drop down menu contents
#         result = self.c.fetchall()
#         exDrop = [""]
#         for i in result:
#             exDrop.append(i[0])
#         print(exDrop)

#         #fill dedfault table
#         self.c = self.db.cursor()
#         self.c.execute("SELECT show_name, exhibit_name, datetime FROM SHOWS")
#         result = self.c.fetchall()
#         for i in result:
#             row = []
#             for j in i:  #converts item to list from tuple
#                 item = QStandardItem(str(j)) #has to be converted to string in order to work
#                 item.setEditable(False)
#                 row.append(item)
#                 #print(row)
#             self.model.appendRow(row)

#         self.exhibitDrop.addItems(exDrop)
#         self.table.setModel(self.model)

#         SSlayout = QGridLayout()
#         SSlayout.setColumnStretch(1,3)
#         SSlayout.setRowStretch(1,3)
#         SSlayout.addWidget(self.title1,1,0)
#         SSlayout.addWidget(self.title2, 1,2)        
#         SSlayout.addWidget(self.search,3,3)
#         SSlayout.addWidget(self.name, 2,0)
#         SSlayout.addWidget(self.wname,2,1)
#         SSlayout.addWidget(self.date,2,2)
#         SSlayout.addWidget(self.dateDrop,2,3)
#         SSlayout.addWidget(self.exhibit,3,0)
#         SSlayout.addWidget(self.exhibitDrop,3,1)
#         SSlayout.addWidget(self.table,4,0,4,4)
#         SSlayout.addWidget(self.logVisit,8,3)

#         self.search_exhibits = QDialog()
#         self.search_exhibits.setLayout(SSlayout)
#         self.search_exhibits.show()

#     def search_animals(self):
#         self.setWindowTitle('Shows')
#         SAlayout = QGridLayout()

#         self.title1 = QLabel("Atalnta Zoo")
#         self.title2 = QLabel("Animals")       
#         self.search = QPushButton("search")
#         self.name = QLabel("Name: ")
#         self.wname = QLineEdit()
#         self.wname = QLineEdit()
#         self.age = QLabel("Age: ")
#         self.minAge = QLabel("min")        
#         self.wminAge = QLineEdit()
#         self.maxAge = QLabel("max")
#         self.Species = QLabel("Species: ")
#         self.wSpecies = QLineEdit()
#         self.wmaxAge = QLineEdit()        
#         self.exhibit = QLabel("Exhibit: ")
#         self.exhibitDrop = QComboBox()
#         self.table = QTableView()
#         self.model = QStandardItemModel()
#         self.model.setColumnCount(3)
#         headerNames = ["Name", "Species","Exhibit", "Age", "Type"]
#         self.model.setHorizontalHeaderLabels(headerNames)

#         self.db = self.Connect()
#         self.c = self.db.cursor()
#         self.c.execute("SELECT exhibit_name FROM EXHIBITS")
        
#         #exhibit drop down menu contents
#         result = self.c.fetchall()
#         exDrop = [""]
#         for i in result:
#             exDrop.append(i[0])
#         print(exDrop)

#         #fill dedfault table
#         self.c = self.db.cursor()
#         self.c.execute("SELECT name,species,exhibit_name,age,type FROM ANIMALS")
#         result = self.c.fetchall()
#         for i in result:
#             row = []
#             for j in i:  #converts item to list from tuple
#                 item = QStandardItem(str(j)) #has to be converted to string in order to work
#                 item.setEditable(False)
#                 row.append(item)
#                 #print(row)
#             self.model.appendRow(row)

#         self.exhibitDrop.addItems(exDrop)
#         self.table.setModel(self.model)

#         SAlayout = QGridLayout()
#         SAlayout.setColumnStretch(1,3)
#         SAlayout.setRowStretch(1,2)
#         SAlayout.addWidget(self.title1,1,0)
#         SAlayout.addWidget(self.title2, 1,2)        
#         SAlayout.addWidget(self.search,2,3)
#         SAlayout.addWidget(self.name, 2,0)
#         SAlayout.addWidget(self.wname,2,1)
#         SAlayout.addWidget(self.Species,3,0)
#         SAlayout.addWidget(self.wSpecies, 3,1)
#         SAlayout.addWidget(self.age, 5,0)
#         SAlayout.addWidget(self.maxAge,4,1)
#         SAlayout.addWidget(self.minAge,4,2)
#         SAlayout.addWidget(self.wminAge,5,1)
#         SAlayout.addWidget(self.wmaxAge,5,2)
#         SAlayout.addWidget(self.exhibit,3,2)
#         SAlayout.addWidget(self.exhibitDrop,3,3)
#         SAlayout.addWidget(self.table,6,0,4,4)

#         self.search_exhibits = QDialog()
#         self.search_exhibits.setLayout(SAlayout)
#         self.search_exhibits.show()

#     def Connect(self):
# #Connecting to the database, function used in multiple other areas around the code
#         try:
#             db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_group4", passwd = "2jILwMuE", db="cs4400_group4")
#             self.db = db
#             db.autocommit(True)
#             return db
#         except:
#             messagebox.showwarning("Error", "Check Internet Connection")
       
        
        




# if __name__=='__main__':
#     app = QApplication(sys.argv)
#     main = MainWindow()
#     main.show()
#     sys.exit(app.exec_())
