#!/usr/bin/env python3

import sys
from datetime import datetime

import tkinter as tk
from tkinter import *
import tkinter.messagebox as messagebox

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from passlib.hash import pbkdf2_sha256

from PyQt5.QtGui import (
    QStandardItemModel,
    QStandardItem
)

from PyQt5.QtCore import (
    Qt,
    QAbstractTableModel,
    QVariant,
    QDate
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
        self.logged_in = False
        makewin = self.login()

    def login(self):
#Creating the first page for login information
        self.user_line_edit = QLineEdit()
        self.password_line_edit = QLineEdit()
        self.password_line_edit.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Register")
        self.register_button.setEnabled(True)
        self.login_button = QPushButton("Login")
        self.login_button.setEnabled(True)
        self.login_button.setDefault(True)

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

        self.register_button.clicked.connect(self.go_to_register)
        self.login_button.clicked.connect(self.check_user)

    def visitor_functionality(self):
    #buttons that appear on main page
        self.openPages = []
        self.SearchExhibits = QPushButton("Search Exhibits")
        self.SearchShows = QPushButton("Search Shows")
        self.SearchAnimals = QPushButton("Search for Animals")
        self.ViewExhibit = QPushButton("View Exhibit History")
        self.ViewShow = QPushButton("View Show History")
        self.LogOut = QPushButton("Log Out")

    #layout of page
        self.layout = QGridLayout()
        layout = self.layout
        layout.setColumnStretch(1,3)
        layout.setRowStretch(1,3)

    #placement layout of page
        layout.addWidget(self.SearchExhibits,1,0)
        layout.addWidget(self.ViewExhibit, 1,1)
        layout.addWidget(self.SearchShows, 2,0)
        layout.addWidget(self.ViewShow, 2,1)
        layout.addWidget(self.SearchAnimals, 3,0)
        layout.addWidget(self.LogOut, 3,1)

    #button connections
        self.SearchExhibits.clicked.connect(self.visitor_search_exhibits)
        self.ViewExhibit.clicked.connect(self.Visitor_Exhibit_History)
        self.SearchShows.clicked.connect(self.visitor_search_shows)
        self.ViewShow.clicked.connect(self.Visitor_Show_History)
        self.SearchAnimals.clicked.connect(self.visitor_search_animals)
        self.LogOut.clicked.connect(self.my_Log_Out)
        self.newWindow = TableWindow()
        self.newWindow.setLayout(layout)
        self.hide()
        self.newWindow.show()

    def my_Log_Out(self):
        for page in self.openPages:
            page.close()
        self.my_user = None
        self.logged_in = False
        self.newWindow.close()
        self.show()


    def admin_functionality(self):
    #buttons that appear on main page
        self.openPages = []
        self.ViewVisitors = QPushButton("View Visitors")
        self.ViewShows = QPushButton("View Shows")
        self.ViewStaff = QPushButton("View Staff")
        self.AddShow = QPushButton("Add Show")
        self.ViewAnimals = QPushButton("View Animals")
        self.AddAnimals = QPushButton("Add Animal")
        self.LogOut = QPushButton("Log Out")

    #layout of page
        self.layout = QGridLayout()
        layout = self.layout
        layout.setColumnStretch(1,4)
        layout.setRowStretch(1,4)

    #placement layout of page
        layout.addWidget(self.ViewVisitors,0,0)
        layout.addWidget(self.ViewStaff, 0,1)
        layout.addWidget(self.ViewShows,1,0)
        layout.addWidget(self.ViewAnimals, 1,1)
        layout.addWidget(self.AddAnimals,2,0)
        layout.addWidget(self.AddShow,2,1)
        layout.addWidget(self.LogOut, 3,1)


        self.newWindow = TableWindow()
        self.newWindow.setLayout(layout)
        self.hide()
        self.newWindow.show()
        for page in self.openPages:
            page.close()
        self.ViewShows.clicked.connect(self.admin_view_shows)
        self.ViewAnimals.clicked.connect(self.admin_view_animals)
        self.AddAnimals.clicked.connect(self.admin_add_animals)
        self.ViewStaff.clicked.connect(self.admin_view_staff)
        self.ViewVisitors.clicked.connect(self.admin_view_visitor)
        self.AddShow.clicked.connect(self.admin_add_show)
        self.LogOut.clicked.connect(self.my_Log_Out)

    def admin_add_show(self):
        SAlayout = QGridLayout()
        self.title1 = QLabel("Atlanta Zoo")
        self.name = QLabel("Name: ")
        self.wname = QLineEdit()
        self.exhibit = QLabel("Exhibit: ")
        self.exhibitDrop = QComboBox()
        self.staff = QLabel("Staff: ")
        self.staffDrop = QComboBox()
        self.date = QLabel("Date: ")
        self.calendar = QCalendarWidget()
        self.time = QLabel("Time: ")
        self.hourDrop = QComboBox()
        self.minuteDrop = QComboBox()
        self.AMPMDrop = QComboBox()
        self.back = QPushButton("Back")

        self.AddShow = QPushButton("Add Show")

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")
#exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT username FROM USERS where user_type = 'staff'")

#type drop down menu contents
        result2 = self.c.fetchall()
        stDrop = [""]
        for i in result2:
            stDrop.append(i[0])

        self.exhibitDrop.addItems(exDrop)
        self.staffDrop.addItems(stDrop)
        self.hourDrop.addItems(["hour","1","2","3","4","5","6","7","8","9","10","11","12"])
        self.AMPMDrop.addItems(["AM/PM","AM","PM"])

        minutes = ["min","00","01","02","03","04","05","06","07","08","09"]
        for i in range(10,61):
            minutes.append(str(i))
        self.minuteDrop.addItems(minutes)

        SAlayout = QGridLayout()
        SAlayout.setColumnStretch(1,6)
        SAlayout.setRowStretch(1,10)
        SAlayout.addWidget(self.title1,0,0)
        SAlayout.addWidget(self.name, 1,0)
        SAlayout.addWidget(self.wname,2,0)
        SAlayout.addWidget(self.exhibit,3,0)
        SAlayout.addWidget(self.exhibitDrop,4,0)
        SAlayout.addWidget(self.staff,5,0)
        SAlayout.addWidget(self.staffDrop,6,0)
        SAlayout.addWidget(self.date,7,0)
        SAlayout.addWidget(self.calendar, 8,0,3,3)
        SAlayout.addWidget(self.time, 11,0)
        SAlayout.addWidget(self.hourDrop,12,0)
        SAlayout.addWidget(self.minuteDrop,12,1)
        SAlayout.addWidget(self.AMPMDrop,12,2)
        SAlayout.addWidget(self.AddShow,5,4)
        SAlayout.addWidget(self.back,0,4)

        self.AddShow.clicked.connect(self.admin_add_show_button)
        self.back.clicked.connect(self.bac_button)

        self.add_shows = QDialog()
        self.add_shows.setLayout(SAlayout)
        self.add_shows.setWindowTitle('Add Show')
        self.add_shows.show()
        for page in self.openPages:
            page.close()
        self.openPages.append(self.add_shows)

    def admin_add_show_button(self):
        datestring = "Jun 1 2005  1:33PM"
        datestring = datetime.strptime(datestring, '%b %d %Y %I:%M%p')
        #momthDict =
        errorStr = ""
        count = 0
#error handling for inputs
        if (len(str(self.wname.text()))) == 0:
            errorStr += "- Enter name of show\n"
            count += 1
        if (len(str(self.exhibitDrop.currentText()))) == 0:
            errorStr += "- Select valid exhibit\n"
            count += 1
        if (len(str(self.staffDrop.currentText()))) == 0:
            errorStr += "- Select valid staff to host the show\n"
            count += 1

        if (len(str(self.hourDrop.currentText()))) > 2:
            errorStr += "- Select valid hour for show start time\n"
            count += 1
        if (len(str(self.minuteDrop.currentText()))) > 2:
            errorStr += "- Select valid minute for show start time\n"
            count += 1
        if (len(str(self.AMPMDrop.currentText()))) == 5:
            errorStr += "- Select valid AM/PM option for show start time\n"
            count += 1

        if count == 0:
#defining gui inputs to variables
            self.name = str(self.wname.text())
            self.exhibit = str(self.exhibitDrop.currentText())
            self.staff = str(self.staffDrop.currentText())
            self.showDate = str(self.calendar.selectedDate())
            self.minute = str(self.minuteDrop.currentText())
            self.AMPM = str(self.AMPMDrop.currentText())
            self.hour = str(self.hourDrop.currentText())
#converting time to correct datetime format
            if (self.AMPM == "PM") and (self.hour != "12"):
                self.hour = int(self.hourDrop.currentText()) + 12
                self.hour = str(self.hour)
            else:
                 self.hour = str(self.hourDrop.currentText())
            if (self.hour == 12) and (self.AMPM == "AM"):
                self.hour = "00"
            if len(self.hour) == 1:
                self.hour = "0" + self.hour
            if len(self.minute) == 1:
                self.minute = "0" + self.minute
#converting date to correct datetime format
            self.year = ""
            for i in range(19,23):
                self.year += self.showDate[i]

            self.month = ""
            for i in range(25,27):
                self.month += self.showDate[i]
            if "," in self.month:
                self.month += "0"
                self.month += self.month[0]
                self.month = self.month[2:]

            self.day = ""
            for i in range(28,len(self.showDate)-1):
                self.day += self.showDate[i]
            if " " in self.day:
                self.day = self.day.replace(" ","")
            if len(self.day) == 1:
                self.day += "0"
                self.day += self.day[0]
                self.day = self.day[1:]
#creating sting to represent datetime
            self.showDate = ""
            self.showDate = self.year + "-" + self.month + "-" + self.day + " " + self.hour + ":" + self.minute + ":00"
            self.showDate = datetime.strptime(self.showDate, '%Y-%m-%d %H:%M:%S')
#see if the staff is working at another show at that time
            self.c.execute("SELECT username, datetime FROM SHOWS WHERE username = (%s) and datetime = (%s)", (self.staff,self.showDate))
            staffMatch = self.c.fetchall()
            if len(staffMatch) != 0:
                errorStr += "This staff member is working another show at that time"
                count += 1
#execute insert SQL query
            if count == 0:
                self.c.execute("INSERT INTO SHOWS VALUES (%s,%s,%s,%s)",(self.name,self.showDate,self.exhibit,self.staff))
                messagebox.showwarning("Congrats", "Show has been successfully added")

        if count > 0:
            messagebox.showwarning("Error", errorStr)

        ############################################
        # - have not closed window
        # - hove not blocked shows from being added in the past present or future
        ############################################

    def admin_view_staff(self):
        SAlayout = QGridLayout()
        self.title1 = QLabel("Atlanta Zoo")
        self.RemoveStaff = QPushButton("Remove Staff Member")
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.back = QPushButton("Back")
        self.model = QStandardItemModel()
        self.model.setColumnCount(2)
        self.headerNames = ["Username", "Email"]
        self.model.setHorizontalHeaderLabels(self.headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT username, email FROM USERS")
        self.c = self.db.cursor()
        self.c.execute("SELECT username,email from USERS Where user_type = 'staff'")
        result = self.c.fetchall()
        for i in result:
            row = []
#converts item to list from tuple
            for j in i:
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)

        self.table.setModel(self.model)
        self.table.setColumnWidth(1,200)

        SAlayout = QGridLayout()
        SAlayout.setColumnStretch(1,5)
        SAlayout.setRowStretch(1,5)
        SAlayout.addWidget(self.title1,0,0)
        SAlayout.addWidget(self.table,6,0,3,9)
        SAlayout.addWidget(self.RemoveStaff,10,4)
        SAlayout.addWidget(self.back,10,0)

        self.RemoveStaff.clicked.connect(self.remove_staff)

        self.back.clicked.connect(self.bac_button)

        self.table.horizontalHeader().sectionClicked.connect(self.avs_column_sort)


        self.view_staff = QDialog()
        self.view_staff.setLayout(SAlayout)
        self.view_staff.show()
        for page in self.openPages:
            page.close()
        self.view_staff.setWindowTitle('View Staff')
        self.openPages.append(self.view_staff)

        self.table.horizontalHeader().sectionClicked.connect(self.avs_column_sort)

    def remove_staff(self):
        staff = self.table.selectionModel().selectedIndexes()
        if len(staff) == 0:
            messagebox.showwarning("Error", "Please select a staff to remove.")
        else:
            name = str(staff[0].data())
            email = str(staff[1].data())
            self.db = self.Connect()
            self.c = self.db.cursor()

            self.c.execute("DELETE FROM USERS WHERE USERS.username = (%s)",name)

            for index in sorted(staff):
                self.model.removeRow(index.row())
                break
            self.table.setModel(self.model)
            messagebox.showwarning("Staff Removed", "The staff member has been removed.")


    def admin_add_animals(self):
        SAlayout = QGridLayout()
        self.title1 = QLabel("Atlanta Zoo")
        self.name = QLabel("Name: ")
        self.wname = QLineEdit()
        self.exhibit = QLabel("Exhibit: ")
        self.exhibitDrop = QComboBox()
        self.type = QLabel("Type: ")
        self.typeDrop = QComboBox()
        self.Species = QLabel("Species: ")
        self.wSpecies = QLineEdit()
        self.Age = QLabel("Age: ")
        self.wAge = QLineEdit()
        self.AddAnimal = QPushButton("Add Animal")
        self.back = QPushButton("Back")

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")

#exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT type FROM ANIMALS")

#type drop down menu contents
        result2 = self.c.fetchall()
        typDrop = ["","Bird","Fish","Mammal","Amphibian","Reptile","Invertebrate"]
        # for i in result2:
        #     typDrop.append(i[0])

        self.exhibitDrop.addItems(exDrop)
        self.typeDrop.addItems(typDrop)

        SAlayout = QGridLayout()
        SAlayout.setColumnStretch(1,6)
        SAlayout.setRowStretch(1,10)
        SAlayout.addWidget(self.title1,0,0)
        SAlayout.addWidget(self.name, 1,0)
        SAlayout.addWidget(self.wname,2,0)
        SAlayout.addWidget(self.exhibit,3,0)
        SAlayout.addWidget(self.exhibitDrop,4,0)
        SAlayout.addWidget(self.type,5,0)
        SAlayout.addWidget(self.typeDrop,6,0)
        SAlayout.addWidget(self.Species,7,0)
        SAlayout.addWidget(self.wSpecies, 8,0)
        SAlayout.addWidget(self.Age, 9,0)
        SAlayout.addWidget(self.wAge,10,0)
        SAlayout.addWidget(self.AddAnimal,5,1)
        SAlayout.addWidget(self.back,10,1)

        self.add_animals = QDialog()
        self.add_animals.setLayout(SAlayout)
        self.add_animals.show()
        for page in self.openPages:
            page.close()
        self.add_animals.setWindowTitle('Add Animals')
        self.openPages.append(self.add_animals)

        self.AddAnimal.clicked.connect(self.admin_add_animal_button)
        self.back.clicked.connect(self.bac_button)

    def admin_add_animal_button(self):
        self.name = str(self.wname.text())
        self.exhibit = str(self.exhibitDrop.currentText())
        self.type = str(self.typeDrop.currentText())
        self.species = str(self.wSpecies.text())
        self.age = str(self.wAge.text())

        self.db = self.Connect()
        self.c = self.db.cursor()
        printstr = ""
        count = 0

#conducting checks for registration information for visitors
        if len(self.name) < 1:
            printstr += "- Name of animal not entered\n"
            count += 1
        if len(self.species) < 1:
            printstr += "- Species of animal not entered\n"
            count+=1
        if len(self.age) < 1:
            printstr += "- Age of animal is not entered\n"
        else:
            try:
                self.age = int(self.age)
            except:
                printstr += "- Age of animals must be an integer\n"
                count += 1
        if len(self.exhibit) < 1:
            printstr += "- Select a valid exhibit\n"
            count += 1
        if len(self.type) < 1:
            printstr += "- Select a valid type\n"
            count += 1
        if (len(self.name) > 0) and (len(self.species) > 0) and (len(str(self.age)) > 0) and (len(self.exhibit) > 0) and (len(self.type) > 0):
            self.c.execute("SELECT name, species FROM ANIMALS WHERE name = (%s) and species = (%s) and age = (%s)", (self.name,self.species,self.age))
            animalMatch = self.c.fetchall()
            if len(animalMatch) != 0:
                printstr += "This name already exists in the Zoo's database"
                count += 1

            if count > 0:
                messagebox.showwarning("Error", printstr)

#adding the visitor to the database
            else:
                self.name = self.name.capitalize()
                self.species = self.species
                self.c.execute("INSERT INTO ANIMALS VALUES (%s,%s,%s,%s,%s)",(self.name,self.species,self.type,self.age,self.exhibit))
                messagebox.showwarning("Congrats", "Animal has been successfully added")
        else:
            messagebox.showwarning("Error", printstr)


    def admin_view_visitor(self):
        SAlayout = QGridLayout()

        self.RemoveVisitor = QPushButton("Remove Visitor")
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.model = QStandardItemModel()
        self.model.setColumnCount(2)
        self.back = QPushButton("Back")

        atlantaZoo = QLabel()
        atlantaZoo.setText("Atlanta Zoo")

        self.headerNames = ["Username", "Email"]
        self.model.setHorizontalHeaderLabels(self.headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT username, email FROM USERS")

        self.c = self.db.cursor()
        self.c.execute("SELECT username,email from USERS Where user_type = 'visitor'")
        result = self.c.fetchall()
        for i in result:
            row = []
    #converts item to list from tuple
            for j in i:
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)

        self.table.setModel(self.model)
        self.table.setColumnWidth(1,190)

        SAlayout = QGridLayout()
        SAlayout.setColumnStretch(1,6)
        SAlayout.setRowStretch(1,2)
        SAlayout.addWidget(atlantaZoo,0,0)
        SAlayout.addWidget(self.table,6,0,3,12)
        SAlayout.addWidget(self.RemoveVisitor,10,7)
        SAlayout.addWidget(self.back,10,0)

        self.RemoveVisitor.clicked.connect(self.remove_visitor)

        self.back.clicked.connect(self.bac_button)

        self.table.horizontalHeader().sectionClicked.connect(self.avv_column_sort)


        self.view_visitors = QDialog()
        self.view_visitors.setLayout(SAlayout)
        self.view_visitors.show()
        for page in self.openPages:
            page.close()
        self.view_visitors.setWindowTitle('View Visitors')
        self.openPages.append(self.view_visitors)


        self.table.horizontalHeader().sectionClicked.connect(self.avv_column_sort)



    def avv_column_sort(self, position):
        sort_by = self.headerNames[position]
        if sort_by == "Username":
            sort_by = "username"
        else:
            sort_by = "email"
        self.c = self.db.cursor()
        self.c.execute("SELECT username,email from USERS Where user_type = 'visitor' ORDER BY " + sort_by)
        result = self.c.fetchall()
        self.model = QStandardItemModel()
        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)
        self.table.setModel(self.model)
        self.model.setHorizontalHeaderLabels(self.headerNames)

    def avs_column_sort(self, position):
        sort_by = self.headerNames[position]
        if sort_by == "Username":
            sort_by = "username"
        else:
            sort_by = "email"
        self.c = self.db.cursor()
        self.c.execute("SELECT username,email from USERS Where user_type = 'staff' ORDER BY " + sort_by)
        result = self.c.fetchall()
        self.model = QStandardItemModel()
        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)
        self.table.setModel(self.model)
        self.model.setHorizontalHeaderLabels(self.headerNames)

    def remove_visitor(self):
        visitor = self.table.selectionModel().selectedIndexes()
        if len(visitor) == 0:
            messagebox.showwarning("Error", "Please select a visitor to remove")
        else:
            name = str(visitor[0].data())
            email = str(visitor[1].data())
            self.db = self.Connect()
            self.c = self.db.cursor()

            self.c.execute("DELETE FROM USERS WHERE USERS.username = (%s)",name)
            for index in sorted(visitor):
                self.model.removeRow(index.row())
                break
            self.table.setModel(self.model)
            messagebox.showwarning("Visitor Removed", "The visitor has been removed.")


    def staff_functionality(self):

    #buttons that appear on main page
        self.openPages = []
        self.SearchAnimals = QPushButton("Search for Animals")
        self.ViewShows = QPushButton("View Show History")
        self.LogOut = QPushButton("Log Out")

    #layout of page
        self.layout = QGridLayout()
        layout = self.layout

    #placement layout of page
        layout.addWidget(self.SearchAnimals,1,0)
        layout.addWidget(self.ViewShows, 2,0)
        layout.addWidget(self.LogOut, 3,0)

        self.newWindow = TableWindow()
        self.newWindow.setLayout(layout)
        self.hide()
        self.newWindow.show()
        for page in self.openPages:
            page.close()
        self.ViewShows.clicked.connect(self.staff_view_shows)
        self.SearchAnimals.clicked.connect(self.staff_search_animals)

        self.LogOut.clicked.connect(self.newWindow.close)
        self.LogOut.clicked.connect(self.my_Log_Out)


    def visitor_search_exhibits(self):
        SElayout = QGridLayout()
        self.title1 = QLabel("Atalnta Zoo")
        self.search = QPushButton("search")
        self.name = QLabel("Name: ")
        self.wname = QLineEdit()
        self.NumAnimals = QLabel("Number of Animals")
        self.animalMin = QLabel("Min")
        self.animalMax = QLabel("Max")
        self.wanimalMin = QLineEdit()
        self.wanimalMax = QLineEdit()
        self.Size = QLabel("Size")
        self.sizeMin = QLabel("Min")
        self.sizeMax = QLabel("Max")
        self.wsizeMin = QLineEdit()
        self.wsizeMax = QLineEdit()
        self.Water = QLabel("Water Feature")
        self.waterDrop = QComboBox()
        self.back = QPushButton("Back")

        self.waterDrop.addItems(["","Yes","No"])
        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT * FROM EXHIBITS")
        result = self.c.fetchall()
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.model = QStandardItemModel()
        self.model.setColumnCount(4)
        self.headerNames = ["Exhibit Name", "Water", "Number of Animals", "Size"]
        self.model.setHorizontalHeaderLabels(self.headerNames)

        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)

        self.table.setModel(self.model)
        self.table.setColumnWidth(3,80)

        SElayout = QGridLayout()
        SElayout.setColumnStretch(1,3)
        SElayout.setRowStretch(1,3)
        SElayout.addWidget(self.title1,1,0)
        SElayout.addWidget(self.search,7,2)
        SElayout.addWidget(self.name, 2,0)
        SElayout.addWidget(self.wname,2,1)
        SElayout.addWidget(self.NumAnimals, 4,0)
        SElayout.addWidget(self.animalMin,3,1)
        SElayout.addWidget(self.animalMax,3,2)
        SElayout.addWidget(self.wanimalMin,4,1)
        SElayout.addWidget(self.wanimalMax,4,2)
        SElayout.addWidget(self.sizeMin,5,1)
        SElayout.addWidget(self.sizeMax,5,2)
        SElayout.addWidget(self.Size,6,0)
        SElayout.addWidget(self.wsizeMin,6,1)
        SElayout.addWidget(self.wsizeMax,6,2)
        SElayout.addWidget(self.Water, 7,0)
        SElayout.addWidget(self.waterDrop, 7,1)
        SElayout.addWidget(self.back,1,2)

        SElayout.addWidget(self.table,8,0,4,4.5)

        self.search_exhibits = QDialog()
        self.search_exhibits.setLayout(SElayout)
        self.search_exhibits.show()
        for page in self.openPages:
            page.close()
        self.search_exhibits.setWindowTitle('Search Exhibits')
        self.openPages.append(self.search_exhibits)

        self.search.clicked.connect(self.visitor_exhibit_search_button)
        self.back.clicked.connect(self.bac_button)
        self.table.doubleClicked.connect(self.exhibit_details)
        self.table.horizontalHeader().sectionClicked.connect(self.vse_column_sort)


        self.table.horizontalHeader().sectionClicked.connect(self.vse_column_sort)

    def bac_button(self):
        for pages in self.openPages:
            pages.close()

    def exhibit_details(self):

        self.back = QPushButton("Back")
        exhibit = self.table.selectionModel().selectedIndexes()
        self.e_name = exhibit[0].data()
        self.e_size = exhibit[3].data()
        self.e_num_animals = exhibit[2].data()
        self.waterornotwaterthatisthequestion = exhibit[1].data()

        self.setWindowTitle('Exhibit Detail')
        SElayout = QGridLayout()
        zooLabel = QLabel("Atlanta Zoo")
        emptyspace = QLabel("")
        namelbl = QLabel("Name: " + str(self.e_name))
        sizelbl = QLabel("Size: " + str(self.e_size))
        numAlbl = QLabel("Num Animals: " + str(self.e_num_animals))
        waterlbl = QLabel("Water Feature: " + str(self.waterornotwaterthatisthequestion))
        logNotesButton = QPushButton("Log Visit")
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)

        self.animalTable = QTableView()
        self.animalModel = QStandardItemModel()
        self.animalModel.setColumnCount(2)
        self.headerNames = ["Name", "Species"]
        self.animalModel.setHorizontalHeaderLabels(self.headerNames)


        self.c = self.db.cursor()
        self.c.execute("SELECT name, species FROM ANIMALS WHERE ANIMALS.exhibit_name = (%s)", (str(self.e_name)))
        result = self.c.fetchall()
        for i in result:
            row = []
#converts item to list from tuple
            for j in i:
                item = QStandardItem(str(j))
#has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.animalModel.appendRow(row)
        self.animalTable.setModel(self.animalModel)

        SElayout.addWidget(zooLabel,0,0)
        SElayout.addWidget(emptyspace, 1,0)
        SElayout.addWidget(namelbl,2,0)
        SElayout.addWidget(sizelbl, 2,1)
        SElayout.addWidget(numAlbl,2,2)
        SElayout.addWidget(waterlbl,2,3)
        SElayout.addWidget(emptyspace,2,4)
        SElayout.addWidget(logNotesButton,3,2)
        SElayout.addWidget(self.animalTable,4,2)
        SElayout.addWidget(self.back,4,0)

        self.log_exhibit = QDialog()
        self.log_exhibit.setLayout(SElayout)
        self.log_exhibit.show()
        self.log_exhibit.setWindowTitle('Log Exhibit')
        self.openPages.append(self.log_exhibit)


        logNotesButton.clicked.connect(self.log_note)
        self.back.clicked.connect(self.back_out_of_exhibit_detail)
        self.animalTable.setSelectionBehavior(QTableView.SelectRows)
        self.animalTable.setSelectionMode(QTableView.SingleSelection)
        self.animalTable.doubleClicked.connect(self.visitor_animal_view)

    def visitor_animal_view(self):
        animal = self.animalTable.selectionModel().selectedIndexes()
        aname = animal[0].data()
        aspec = animal[1].data()
        self.c = self.db.cursor()
        self.c.execute("SELECT * FROM ANIMALS WHERE name = (%s) AND species = (%s)", (aname, aspec))
        animal_info = self.c.fetchone()

        SAlayout = QGridLayout()

        exit = QPushButton("Exit")
        name = QLabel("Name: ")
        wname = QLabel(str(animal_info[0]))
        spec = QLabel("Species: ")
        wspec = QLabel(str(animal_info[1]))
        typey = QLabel("Type: ")
        wtype = QLabel(str(animal_info[2]))
        age = QLabel("Age: ")
        wage = QLabel(str(animal_info[3]))
        exhibit = QLabel("Exhibit: ")
        wexhibit = QLabel(str(animal_info[4]))

        SAlayout.addWidget(name,1,0)
        SAlayout.addWidget(wname,1,1)
        SAlayout.addWidget(spec,1,2)
        SAlayout.addWidget(wspec,1,3)
        SAlayout.addWidget(age,1,4)
        SAlayout.addWidget(wage,1,5)
        SAlayout.addWidget(name,1,0)
        SAlayout.addWidget(typey,2,0)
        SAlayout.addWidget(wtype,2,1)
        SAlayout.addWidget(exhibit,2,2)
        SAlayout.addWidget(wexhibit,2,3)
        SAlayout.addWidget(exit,2,4)

        self.animalView = QDialog()
        self.animalView.setLayout(SAlayout)
        self.animalView.setWindowTitle("Animal Details")
        self.animalView.show()
        exit.clicked.connect(self.animalView.close)

    def back_out_of_exhibit_detail(self):
        self.log_exhibit.close()
        self.search_exhibits.setFocus()

    def log_note(self):
        visitor = self.my_user[1]
        now = str(datetime.now())
        self.c.execute("INSERT INTO EXHIBIT_VISITS VALUES (%s,%s,%s)",(str(self.e_name), str(visitor), now))
        messagebox.showwarning("Thank you!", "Your visit has been logged.")

    def visitor_exhibit_search_button(self):
        self.animalMin = str(self.wanimalMin.text())
        self.animalMax = str(self.wanimalMax.text())
        self.sizeMin = str(self.wsizeMin.text())
        self.sizeMax = str(self.wsizeMax.text())
        printstr = ""
        count = 0
        count2 = 0
        count3 = 0
        count4 = 0
        fullQuery = "SELECT exhibit_name, water, number_of_animals, size FROM EXHIBITS"
        addQuery = []

        if len(self.animalMin) > 0:
            try:
                self.animalMin = int(str(self.wanimalMin.text()))
                self.animalMin = str(self.wanimalMin.text())
                addQuery.append("number_of_animals >= '{}'".format(self.animalMin))
                count2 += 1
            except:
                printstr += "- input for min animal number must be integer\n"
                count += 1
        if len(self.animalMax) > 0:
            try:
                self.animalMax = int(str(self.wanimalMax.text()))
                self.animalMax = str(self.wanimalMax.text())
                addQuery.append("number_of_animals <= '{}'".format(self.animalMax))
                count2 += 1
            except:
                printstr += "- input for max animal number must be integer\n"
                count += 1
        if count2 == 2:
            if (int(self.animalMin) > int(self.animalMax)):
                printstr += "- min animals must be less than max animals\n"
                count += 1
        if len(self.sizeMin) > 0:
            try:
                self.sizeMin = int(str(self.wsizeMin.text()))
                self.sizeMin = str(self.wsizeMin.text())
                addQuery.append("size >= '{}'".format(self.sizeMin))
                count4 += 1
            except:
                printstr += "- input for min size must be integer\n"
                count3 += 1
        if len(self.sizeMax) > 0:
            try:
                self.sizeMax = int(str(self.wsizeMax.text()))
                self.sizeMax = str(self.wsizeMax.text())
                addQuery.append("size <= '{}'".format(self.sizeMax))
                count4 += 1
            except:
                printstr += "- input for max size must be integer\n"
                count3 += 1
        if count4 == 2:
            if (int(self.sizeMin) > int(self.sizeMax)):
                printstr += "- min size must be less than max size\n"
                count3 += 1
        if len(str(self.wname.text())) > 0:
            self.name = str(self.wname.text())
            addQuery.append("exhibit_name LIKE '%{}%'".format(self.name))
        if len(str(self.waterDrop.currentText())) > 0:
            self.water = str(self.waterDrop.currentText())
            addQuery.append("water = '{}'".format(self.water))
        if ((count == 0) and (count3 == 0)):
            if len(addQuery) > 0:
                fullQuery += " WHERE "
                for i in range(0,len(addQuery)-1):
                    fullQuery = fullQuery + addQuery[i] + " AND "
                fullQuery += addQuery[len(addQuery)-1]
            self.model.clear()
            self.table.setModel(self.model)

            self.c = self.db.cursor()
            self.c.execute(fullQuery)
            result = self.c.fetchall()
            for i in result:
                row = []
    #converts item to list from tuple
                for j in i:
                    item = QStandardItem(str(j))
    #has to be converted to string in order to work
                    item.setEditable(False)
                    row.append(item)
                self.model.appendRow(row)

            self.headerNames = ["Exhibit Name", "Water", "Number of Animals", "Size"]
            self.model.setHorizontalHeaderLabels(self.headerNames)
            self.table.setModel(self.model)
        else:
            messagebox.showwarning("Error", printstr)


    def Visitor_Exhibit_History(self):
        SSlayout = QGridLayout()

        self.search = QPushButton("search")

        self.name = QLabel("Name: ")
        self.wname = QLineEdit()
        self.title1 = QLabel("Atlanta Zoo")
        self.date = QLabel("Date: ")
        self.calendar = QDateEdit() #this is wrong implementation
        self.calendar.setCalendarPopup(True)
        self.calendar.calendarWidget().installEventFilter(self)
        self.calendar.setSpecialValueText(" ")
        self.calendar.setDate(QDate.fromString( "01/01/0001", "dd/MM/yyyy" ))
        self.calendar.setMinimumDate(QDate.fromString( "01/01/2010", "dd/MM/yyyy" ))

        self.NumVisits = QLabel("Number of Visits: ")
        self.minVisits = QLineEdit()
        self.maxVisits = QLineEdit()
        self.minVisitsLabel = QLabel("Min")
        self.maxVisitsLabel = QLabel("Max")
        self.back = QPushButton("Back")

        # self.table = QTableView()
        # self.model = QStandardItemModel()
        # self.model.setColumnCount(3)
        # headerNames = ["Name", "Exhibit", "Date"]
        # self.model.setHorizontalHeaderLabels(headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT EXHIBIT_VISITS.exhibit_name, datetime, c FROM EXHIBIT_VISITS JOIN view1 WHERE username = '{}' AND EXHIBIT_VISITS.exhibit_name = view1.exhibit_name".format(self.my_user[1]))
        result = self.c.fetchall()


        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        self.headerNames = ["Exhibit Name", "Time", "Number of Visits"]
        self.model.setHorizontalHeaderLabels(self.headerNames)

        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)

            self.model.appendRow(row)

        self.table.setModel(self.model)

        SSlayout = QGridLayout()
        SSlayout.setColumnStretch(1,3)
        SSlayout.setRowStretch(1,3)
        SSlayout.addWidget(self.title1,0,0)
        SSlayout.addWidget(self.search,3,4)
        SSlayout.addWidget(self.name, 1,0)
        SSlayout.addWidget(self.wname,1,1)
        SSlayout.addWidget(self.date,2,0)
        SSlayout.addWidget(self.calendar,2,1)
        SSlayout.addWidget(self.NumVisits,1,2)
        SSlayout.addWidget(self.minVisitsLabel,0,3)
        SSlayout.addWidget(self.maxVisitsLabel,0,4)
        SSlayout.addWidget(self.maxVisits,1,4)
        SSlayout.addWidget(self.minVisits,1,3)
        SSlayout.addWidget(self.table,4,0,3,3)
        SSlayout.addWidget(self.back,7,4)

        self.search.clicked.connect(self.visitor_exhibit_history_search)
        self.back.clicked.connect(self.bac_button)
        self.table.horizontalHeader().sectionClicked.connect(self.vseh_column_sort)


        self.exhibit_history = QDialog()
        self.exhibit_history.setLayout(SSlayout)
        self.exhibit_history.show()
        for page in self.openPages:
            page.close()
        self.exhibit_history.setWindowTitle('Exhibit History')
        self.openPages.append(self.exhibit_history)


        self.table.horizontalHeader().sectionClicked.connect(self.vseh_column_sort)



    def vseh_column_sort(self, position):
        sort_by = self.headerNames[position]
        if sort_by == "Time":
            sort_by = "datetime"
        elif sort_by == "Exhibit Name":
            sort_by = "exhibit_name"
        else:
            sort_by = "view1.c"
        self.c = self.db.cursor()
        self.c.execute("SELECT EXHIBIT_VISITS.exhibit_name, datetime, c FROM EXHIBIT_VISITS JOIN view1 WHERE username = %s AND EXHIBIT_VISITS.exhibit_name = view1.exhibit_name ORDER BY " + sort_by, (self.my_user[1]))
        result = self.c.fetchall()
        self.model = QStandardItemModel()
        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)
        self.table.setModel(self.model)
        self.model.setHorizontalHeaderLabels(self.headerNames)

    def visitor_exhibit_history_search(self):
        addQuery =[]
        addQuery2 = []
        count = 0
        count2 = 0
        errorstr = ""
        if len(str(self.wname.text())) > 0:
            self.name = str(self.wname.text())
            addQuery.append("EXHIBIT_VISITS.exhibit_name LIKE '%{}%'".format(self.name))
        self.date = str(self.calendar.date())
        if self.date == "PyQt5.QtCore.QDate(2010, 1, 1)":
            self.date = ""
        else:
            self.year = ""
            for i in range(19,23):
                self.year += self.date[i]
            self.month = ""
            for i in range(25,27):
                self.month += self.date[i]
            if "," in self.month:
                self.month += "0"
                self.month += self.month[0]
                self.month = self.month[2:]
            self.day = ""
            for i in range(28,len(self.date)-1):
                self.day += self.date[i]
            if " " in self.day:
                self.day = self.day.replace(" ","")
            if len(self.day) == 1:
                self.day += "0"
                self.day += self.day[0]
                self.day = self.day[1:]

            self.date = ""
            self.date = self.year + "-" + self.month + "-" + self.day
            addQuery.append("DATE(EXHIBIT_VISITS.datetime) = '{}'".format(self.date))
        if len(self.maxVisits.text()) > 0:
            try:
                int(self.maxVisits.text())
                self.wmaxVisits = str(self.maxVisits.text())
                addQuery2.append("c <= '{}'".format(self.wmaxVisits))
                count += 1
            except:
                errorstr += "- input for max age must be an integer\n"
                count2 += 1
        if len(self.minVisits.text()) > 0:
            try:
                int(self.minVisits.text())
                self.wminVisits = str(self.minVisits.text())
                addQuery2.append("c >= '{}'".format(self.wminVisits))
                count += 1
            except:
                errorstr += "- input for min age must be an integer\n"
                count2 += 1
        if (count == 2) and (int(self.minVisits.text()) > int(self.maxVisits.text())):
                errorstr += "- max age must be greater than min age\n"
                count2 += 1
        if (count2 > 0):
            messagebox.showwarning("Error", errorstr)

        fullQuery = "SELECT EXHIBIT_VISITS.exhibit_name,datetime, c FROM EXHIBIT_VISITS JOIN view1 WHERE username = '{}' AND EXHIBIT_VISITS.exhibit_name = view1.exhibit_name".format(self.my_user[1])
        if len(addQuery) > 0:
            fullQuery += " and "
            for i in range(0,len(addQuery)-1):
                fullQuery = fullQuery + addQuery[i] + " and "
            fullQuery = fullQuery + addQuery[len(addQuery)-1] + " "
        # fullQuery += "GROUP BY exhibit_name"
        if len(addQuery2) > 0:
            fullQuery += " HAVING "
            for i in range(0,len(addQuery2)-1):
                fullQuery = fullQuery + addQuery2[i] + " and "
            fullQuery = fullQuery + addQuery2[len(addQuery)-1] + " "

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute(fullQuery)
        result = self.c.fetchall()
        self.model.clear()
        self.table.setModel(self.model)

        for i in result:
            row = []
#converts item to list from tuple
            for j in i:
                item = QStandardItem(str(j))
#has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)

        self.table.setModel(self.model)
        self.headerNames = ["Exhibit Name", "Time", "Number of Visits"]
        self.model.setHorizontalHeaderLabels(self.headerNames)


    def Visitor_Show_History(self):
        SSlayout = QGridLayout()

        self.search = QPushButton("search")
        self.name = QLabel("Name: ")
        self.wname = QLineEdit()
        self.date = QLabel("Date: ")
        self.calendar = QDateEdit() #this is wrong implementation
        self.calendar.setCalendarPopup(True)
        self.calendar.calendarWidget().installEventFilter(self)
        self.calendar.setSpecialValueText(" ")
        self.calendar.setDate(QDate.fromString( "01/01/0001", "dd/MM/yyyy" ))
        self.calendar.setMinimumDate(QDate.fromString( "01/01/2010", "dd/MM/yyyy" ))

        self.exhibit_name = QLabel("Exhibit")
        self.exhibitDrop = QComboBox()
        self.back = QPushButton("Back")

        self.historyTable = QTableView()
        self.historyModel = QStandardItemModel()
        self.historyModel.setColumnCount(3)
        self.headerNames = ["Name", "Date", "Exhibit"]
        self.historyModel.setHorizontalHeaderLabels(self.headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")

#exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])
        self.exhibitDrop.addItems(exDrop)

#fill dedfault table
        self.c = self.db.cursor()
        self.c.execute("SELECT SHOWS.show_name, SHOWS.datetime, exhibit_name FROM (SHOWS JOIN SHOW_VISITS on SHOWS.show_name = SHOW_VISITS.show_name) WHERE SHOW_VISITS.username = '{}'".format(self.my_user[1]))
        result = self.c.fetchall()
        for i in result:
            row = []
#converts item to list from tuple
            for j in i:
                item = QStandardItem(str(j))
#has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.historyModel.appendRow(row)

        self.historyTable.setModel(self.historyModel)
        self.historyTable.setColumnWidth(2,95)

        SAlayout = QGridLayout()
        SAlayout.setColumnStretch(1,6)
        SAlayout.setRowStretch(1,6)
        SAlayout.addWidget(self.search,1,7)
        SAlayout.addWidget(self.name, 1,0,1,1)
        SAlayout.addWidget(self.wname,1,1)
        SAlayout.addWidget(self.date,2,0)
        SAlayout.addWidget(self.calendar,2,1,1,5)
        SAlayout.addWidget(self.exhibit_name,3,0)
        SAlayout.addWidget(self.exhibitDrop,3,1)
        SAlayout.addWidget(self.historyTable,4,0,7,8)
        SAlayout.addWidget(self.back,3,7)

        self.search.clicked.connect(self.view_show_history_search)
        self.back.clicked.connect(self.bac_button)
        self.historyTable.horizontalHeader().sectionClicked.connect(self.vsh_column_sort)

        self.show_history = QDialog()
        self.show_history.setLayout(SAlayout)
        self.show_history.show()
        for page in self.openPages:
            page.close()
        self.show_history.setWindowTitle('Show History')
        self.openPages.append(self.show_history)


        self.historyTable.horizontalHeader().sectionClicked.connect(self.vsh_column_sort)



    def vsh_column_sort(self, position):
        sort_by = self.headerNames[position]
        if sort_by == "Name":
            sort_by = "SHOWS.show_name"
        elif sort_by == "Exhibit":
            sort_by = "exhibit_name"
        else:
            sort_by = "SHOWS.datetime"
        self.c = self.db.cursor()
        self.c.execute("SELECT SHOWS.show_name, SHOWS.datetime, exhibit_name FROM (SHOWS JOIN SHOW_VISITS on SHOWS.show_name = SHOW_VISITS.show_name) WHERE SHOW_VISITS.username = (%s) ORDER BY " + sort_by, (self.my_user[1]))
        result = self.c.fetchall()
        self.historyModel = QStandardItemModel()
        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.historyModel.appendRow(row)
        self.historyTable.setModel(self.historyModel)
        self.historyModel.setHorizontalHeaderLabels(self.headerNames)

    def view_show_history_search(self):
        self.name = str(self.wname.text())
        self.exhibit = str(self.exhibitDrop.currentText())

        addQuery = []
        if len(self.exhibit) != 0:
            addQuery.append("exhibit_name = '{}'".format(self.exhibit))
        if len(self.name) != 0:
            addQuery.append("lower(SHOWS.show_name) LIKE '%{}%'".format(self.name.lower()))

        self.date = str(self.calendar.date())
        if self.date == "PyQt5.QtCore.QDate(2010, 1, 1)":
            self.date = ""
        else:
            self.year = ""
            for i in range(19,23):
                self.year += self.date[i]
            self.month = ""
            for i in range(25,27):
                self.month += self.date[i]
            if "," in self.month:
                self.month += "0"
                self.month += self.month[0]
                self.month = self.month[2:]
            self.day = ""
            for i in range(28,len(self.date)-1):
                self.day += self.date[i]
            if " " in self.day:
                self.day = self.day.replace(" ","")
            if len(self.day) == 1:
                self.day += "0"
                self.day += self.day[0]
                self.day = self.day[1:]

            self.date = ""
            self.date = self.year + "-" + self.month + "-" + self.day
            addQuery.append("DATE(SHOWS.datetime) = '{}'".format(self.date))

        fullQuery = "SELECT SHOWS.show_name, SHOWS.datetime, exhibit_name FROM (SHOWS JOIN SHOW_VISITS on SHOWS.show_name = SHOW_VISITS.show_name) WHERE SHOW_VISITS.username = '{}'".format(self.my_user[1])
        if len(addQuery) > 0:
            fullQuery += " and "
            for i in range(0,len(addQuery)-1):
                fullQuery = fullQuery + addQuery[i] + " and "
            fullQuery += addQuery[len(addQuery)-1]

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute(fullQuery)
        result = self.c.fetchall()

        self.historyModel.clear()
        self.historyTable.setModel(self.historyModel)

        self.c = self.db.cursor()
        self.c.execute(fullQuery)
        result = self.c.fetchall()
        for i in result:
            row = []
#converts item to list from tuple
            for j in i:
                item = QStandardItem(str(j))
#has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.historyModel.appendRow(row)

        self.headerNames = ["Name", "Date", "Exhibit"]
        self.historyModel.setHorizontalHeaderLabels(self.headerNames)
        self.historyTable.setModel(self.historyModel)

    def visitor_search_shows(self):
        SSlayout = QGridLayout()

        self.title1 = QLabel("Atalnta Zoo")
        self.title2 = QLabel("Shows")
        self.search = QPushButton("search")
        self.name = QLabel("Name: ")
        self.wname = QLineEdit()
        self.date = QLabel("Date: ")
        self.dateDrop = QDateEdit() #this is wrong implementation
        self.dateDrop.setCalendarPopup(True)
        self.dateDrop.calendarWidget().installEventFilter(self)
        self.dateDrop.setSpecialValueText(" ")
        self.dateDrop.setDate(QDate.fromString( "01/01/0001", "dd/MM/yyyy" ))
        self.dateDrop.setMinimumDate(QDate.fromString( "01/01/2010", "dd/MM/yyyy" ))
        self.exhibit = QLabel("Exhibit: ")
        self.exhibitDrop = QComboBox()
        self.logVisit = QPushButton("Log Visit")
        self.back = QPushButton("Back")
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        self.headerNames = ["Name", "Exhibit", "Date"]
        self.model.setHorizontalHeaderLabels(self.headerNames)
        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")

#exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])

#fill dedfault table
        self.c = self.db.cursor()
        self.c.execute("SELECT show_name, exhibit_name, datetime FROM SHOWS")
        result = self.c.fetchall()
        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)

        self.exhibitDrop.addItems(exDrop)
        self.table.setModel(self.model)

        self.table.setColumnWidth(2,180)

        self.table.horizontalHeader().sectionClicked.connect(self.vss_column_sort)


        SSlayout = QGridLayout()
        SSlayout.setColumnStretch(1,3)
        SSlayout.setRowStretch(1,3)
        SSlayout.addWidget(self.title1,1,0)
        SSlayout.addWidget(self.title2, 1,2)
        SSlayout.addWidget(self.search,3,3)
        SSlayout.addWidget(self.name, 2,0)
        SSlayout.addWidget(self.wname,2,1)
        SSlayout.addWidget(self.date,2,2)
        SSlayout.addWidget(self.dateDrop,2,3)
        SSlayout.addWidget(self.exhibit,3,0)
        SSlayout.addWidget(self.exhibitDrop,3,1)
        SSlayout.addWidget(self.table,4,0,4,6)
        SSlayout.addWidget(self.logVisit,8,3)
        SSlayout.addWidget(self.back,8,0)

        self.search.clicked.connect(self.search_shows_button)
        self.back.clicked.connect(self.bac_button)
        self.logVisit.clicked.connect(self.log_shows_button)

        self.search_shows = QDialog()
        self.search_shows.setLayout(SSlayout)
        self.search_shows.show()
        for page in self.openPages:
            page.close()
        self.search_shows.setWindowTitle('Search Shows')
        self.openPages.append(self.search_shows)


        self.table.horizontalHeader().sectionClicked.connect(self.vss_column_sort)



    def vss_column_sort(self, position):
        sort_by = self.headerNames[position]
        if sort_by == "Name":
            sort_by = "show_name"
        elif sort_by == "Exhibit":
            sort_by = "exhibit_name"
        else:
            sort_by = "datetime"
        self.c = self.db.cursor()
        self.c.execute("SELECT show_name, exhibit_name, datetime FROM SHOWS ORDER BY " + sort_by)
        result = self.c.fetchall()
        self.model = QStandardItemModel()
        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)
        self.table.setModel(self.model)
        self.model.setHorizontalHeaderLabels(self.headerNames)









#DO NOT CHANGE THE NAME OF THIS METHOD
#STAFF AND VISITOR BOTH USE THIS METHOD TO SEARCH FOR SHOWS
    def search_shows_button(self):
        fullQuery = "SELECT show_name, exhibit_name, datetime FROM SHOWS"
        addQuery = []
        count = 0
        if len(str(self.wname.text())) > 0:
            self.name = str(self.wname.text())
            addQuery.append("lower(show_name) LIKE '%{}%'".format(self.name.lower()))
            count += 1
        if len(str(self.exhibitDrop.currentText())):
            self.exhibit = str(self.exhibitDrop.currentText())
            addQuery.append("exhibit_name = '{}'".format(self.exhibit.lower()))
            count += 1
        self.date = str(self.dateDrop.date())
        if self.date == "PyQt5.QtCore.QDate(2010, 1, 1)":
            self.date = ""
        else:
            self.year = ""
            for i in range(19,23):
                self.year += self.date[i]
            self.month = ""
            for i in range(25,27):
                self.month += self.date[i]
            if "," in self.month:
                self.month += "0"
                self.month += self.month[0]
                self.month = self.month[2:]
            self.day = ""
            for i in range(28,len(self.date)-1):
                self.day += self.date[i]
            if " " in self.day:
                self.day = self.day.replace(" ","")
            if len(self.day) == 1:
                self.day += "0"
                self.day += self.day[0]
                self.day = self.day[1:]

            self.date = ""
            self.date = self.year + "-" + self.month + "-" + self.day
            addQuery.append("DATE(datetime) = '{}'".format(self.date))
        if len(addQuery) > 0:
            fullQuery += " WHERE "
            for i in range(0,len(addQuery)-1):
                fullQuery = fullQuery + addQuery[i] + " AND "
            fullQuery += addQuery[len(addQuery)-1]

        self.model.clear()
        self.table.setModel(self.model)

        self.c = self.db.cursor()
        self.c.execute(fullQuery)
        result = self.c.fetchall()
        for i in result:
            row = []
#converts item to list from tuple
            for j in i:
                item = QStandardItem(str(j))
#has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)


        self.headerNames = ["Name", "Exhibit", "Date"]
        self.model.setHorizontalHeaderLabels(self.headerNames)
        self.table.setModel(self.model)
        self.table.setColumnWidth(2,180)

    def log_shows_button(self):
        show = self.table.selectionModel().selectedIndexes()
        visitor = self.my_user[1]
        if (len(show) == 0):
            messagebox.showwarning("Error", "Please Select a Show to log.")
        else:
            show_name = show[0].data()
            show_date = show[2].data()
            show_exh = show[1].data()
            self.c.execute("SELECT SHOWS.show_name, SHOWS.datetime, exhibit_name FROM (SHOWS JOIN SHOW_VISITS on SHOWS.show_name = SHOW_VISITS.show_name) WHERE SHOW_VISITS.username = '{}'".format(self.my_user[1]))
            result = self.c.fetchall()
            newResults = []
            for x in result:
                newList = [x[0], str(x[1]), x[2]]
                newResults.append(newList)
            row = [show_name, show_date, show_exh]
            if (row in newResults):
                messagebox.showwarning("Error", "That show has already been logged")
            else:
                if (datetime.strptime(show_date, "%Y-%m-%d %H:%M:%S") <= datetime.now()):
                    messagebox.showwarning("Error", "You can only log visits to shows in the past.")
                else:
                    self.c.execute("INSERT INTO SHOW_VISITS VALUES (%s,%s,%s)",(str(show_name), str(show_date), str(visitor)))
                    messagebox.showwarning("Thank you!", "Your visit has been logged.")




    def visitor_search_animals(self):
        SAlayout = QGridLayout()

        self.title1 = QLabel("Atlanta Zoo")
        self.search = QPushButton("search")
        self.name = QLabel("Name: ")
        self.wname = QLineEdit()
        self.wname = QLineEdit()
        self.age = QLabel("Age: ")
        self.minAge = QLabel("min")
        self.wminAge = QLineEdit()
        self.maxAge = QLabel("max")
        self.Species = QLabel("Species: ")
        self.wSpecies = QLineEdit()
        self.wmaxAge = QLineEdit()
        self.exhibit = QLabel("Exhibit: ")
        self.exhibitDrop = QComboBox()
        self.back = QPushButton("Back")
        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        self.headerNames = ["Name", "Species","Exhibit", "Age", "Type"]
        self.model.setHorizontalHeaderLabels(self.headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")

#exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])


#fill dedfault table
        self.c = self.db.cursor()
        self.c.execute("SELECT name,species,exhibit_name,age,type FROM ANIMALS")
        result = self.c.fetchall()
        for i in result:
            row = []
#converts item to list from tuple
            for j in i:
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)

        self.exhibitDrop.addItems(exDrop)
        self.table.setModel(self.model)

        SAlayout = QGridLayout()
        SAlayout.setColumnStretch(1,3)
        SAlayout.setRowStretch(1,2)
        SAlayout.addWidget(self.title1,1,0)
        SAlayout.addWidget(self.search,5,3)
        SAlayout.addWidget(self.name, 2,0)
        SAlayout.addWidget(self.wname,2,1)
        SAlayout.addWidget(self.Species,3,0)
        SAlayout.addWidget(self.wSpecies, 3,1)
        SAlayout.addWidget(self.age, 5,0)
        SAlayout.addWidget(self.maxAge,4,2)
        SAlayout.addWidget(self.minAge,4,1)
        SAlayout.addWidget(self.wminAge,5,1)
        SAlayout.addWidget(self.wmaxAge,5,2)
        SAlayout.addWidget(self.exhibit,3,2)
        SAlayout.addWidget(self.exhibitDrop,3,3)
        SAlayout.addWidget(self.table,6,0,4,10)
        SAlayout.addWidget(self.back,1,3.5)

        self.search.clicked.connect(self.search_animals_button)
        self.back.clicked.connect(self.bac_button)
        self.table.horizontalHeader().sectionClicked.connect(self.vsa_column_sort)

        self.search_animals = QDialog()
        self.search_animals.setLayout(SAlayout)
        self.search_animals.show()
        for page in self.openPages:
            page.close()
        self.search_animals.setWindowTitle('Search Animals')
        self.openPages.append(self.search_animals)


        self.table.horizontalHeader().sectionClicked.connect(self.vsa_column_sort)



    def vsa_column_sort(self, position):
        sort_by = self.headerNames[position]
        if sort_by == "Name":
            sort_by = "name"
        elif sort_by == "Species":
            sort_by = "species"
        elif sort_by == "Exhibit":
            sort_by = "exhibit_name"
        elif sort_by == "Age":
            sort_by = "age"
        else:
            sort_by = "type"
        self.c = self.db.cursor()
        self.c.execute("SELECT name,species,exhibit_name,age,type FROM ANIMALS ORDER BY " + sort_by)
        result = self.c.fetchall()
        self.model = QStandardItemModel()
        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)
        self.table.setModel(self.model)
        self.model.setHorizontalHeaderLabels(self.headerNames)

#DO NOT CHANGE THE NAME OF THIS METHOD
#STAFF AND VISITOR BOTH USE THIS METHOD TO SEARCH FOR ANIMALS
    def search_animals_button(self):
        errorstr = ""
        count = 0
        count2 = 0
        fullQuery = "SELECT name, species, exhibit_name, age, type FROM ANIMALS"
        addQuery = []
#validation checks
        if len(str(self.wname.text())) > 0:
            self.name = str(self.wname.text())
            addQuery.append("lower(name) LIKE '%{}%'".format(self.name.lower()))
        if len(str(self.wSpecies.text())) > 0:
            self.species = str(self.wSpecies.text())
            addQuery.append("lower(species) LIKE '%{}%'".format(self.species.lower()))
        if len(str(self.exhibitDrop.currentText())) > 0:
            self.exhibit = str(self.exhibitDrop.currentText())
            addQuery.append("exhibit_name = '{}'".format(self.exhibit))
        if len(self.wmaxAge.text()) > 0:
            try:
                int(self.wmaxAge.text())
                self.maxAge = str(self.wmaxAge.text())
                addQuery.append("age <= '{}'".format(self.maxAge))
                count += 1
            except:
                errorstr += "- input for max age must be an integer\n"
                count2 += 1
        if len(self.wminAge.text()) > 0:
            try:
                int(self.wminAge.text())
                self.minAge = str(self.wminAge.text())
                addQuery.append("age >= '{}'".format(self.minAge))
                count += 1
            except:
                errorstr += "- input for min age must be an integer\n"
                count2 += 1
        if (count == 2) and (int(self.minAge) > int(self.maxAge)):
                errorstr += "- max age must be greater than min age\n"
                count2 += 1
        if (count2 > 0):
            messagebox.showwarning("Error", errorstr)

#appending to the where statements for SQL query
        if count2 == 0:
            if len(addQuery) > 0:
                fullQuery += " WHERE "
                for i in range(0,len(addQuery)-1):
                    fullQuery = fullQuery + addQuery[i] + " AND "
                fullQuery += addQuery[len(addQuery)-1]

#clear current table view before repoulating
        self.model.clear()
        self.table.setModel(self.model)

        self.c = self.db.cursor()
        self.c.execute(fullQuery)
        result = self.c.fetchall()
        for i in result:
            row = []
#converts item to list from tuple
            for j in i:
                item = QStandardItem(str(j))
#has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)

        self.headerNames = ["Name", "Species", "Exhibit", "Age", "Type"]
        self.model.setHorizontalHeaderLabels(self.headerNames)
        self.table.setModel(self.model)


    def staff_search_animals(self):
        SAlayout = QGridLayout()
        self.title1 = QLabel("Atlanta Zoo")
        self.back = QPushButton("Back")
        self.name = QLabel("Name: ")
        self.wname = QLineEdit()
        self.wname = QLineEdit()
        self.search = QPushButton("search")
        self.age = QLabel("Age: ")
        self.minAge = QLabel("min")
        self.wminAge = QLineEdit()
        self.maxAge = QLabel("max")
        self.wmaxAge = QLineEdit()

        self.Species = QLabel("Species: ")
        self.wSpecies = QLineEdit()

        self.Type = QLabel("Type: ")
        self.typeDrop = QComboBox()
        typDrop = ["","Bird","Fish","Mammal","Amphibian","Reptile","Invertebrate"]
        self.typeDrop.addItems(typDrop)

        self.exhibit = QLabel("Exhibit: ")
        self.exhibitDrop = QComboBox()
        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT distinct(exhibit_name) FROM EXHIBITS")
#exhibit drop down menu contents
        result = self.c.fetchall()

        exDrop = ["","Birds","Pacific","Mountainous","Jungle","Sahara"]
        self.exhibitDrop.addItems(exDrop)

        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        self.headerNames = ["Name", "Species","Exhibit", "Age", "Type"]
        self.model.setHorizontalHeaderLabels(self.headerNames)


#fill dedfault table
        self.c = self.db.cursor()
        self.c.execute("SELECT name,species,exhibit_name,age,type FROM ANIMALS")
        result = self.c.fetchall()
        for i in result:
            row = []
#converts item to list from tuple
            for j in i:
                item = QStandardItem(str(j))
#has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)

        #self.exhibitDrop.addItems(exDrop)
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.doubleClicked.connect(self.staff_animal_care)

        SAlayout = QGridLayout()
        SAlayout.setColumnStretch(1,4)
        SAlayout.setRowStretch(1,2)
        SAlayout.addWidget(self.title1,1,0)
        SAlayout.addWidget(self.name, 2,0)
        SAlayout.addWidget(self.wname,2,1)
        SAlayout.addWidget(self.Species,3,0)
        SAlayout.addWidget(self.wSpecies, 3,1)
        SAlayout.addWidget(self.Type,4,3)
        SAlayout.addWidget(self.typeDrop,5,3)
        SAlayout.addWidget(self.age, 5,0)
        SAlayout.addWidget(self.maxAge,4,2)
        SAlayout.addWidget(self.minAge,4,1)
        SAlayout.addWidget(self.wminAge,5,1)
        SAlayout.addWidget(self.wmaxAge,5,2)
        SAlayout.addWidget(self.exhibit,3,2)
        SAlayout.addWidget(self.exhibitDrop,3,3)
        SAlayout.addWidget(self.table,7,0,4,11)
        SAlayout.addWidget(self.search,2,2)
        SAlayout.addWidget(self.back,2,3)

        self.search.clicked.connect(self.staff_search_animals_button)

        self.back.clicked.connect(self.bac_button)

        self.table.horizontalHeader().sectionClicked.connect(self.ssa_column_sort)


        self.search_animals = QDialog()
        self.search_animals.setLayout(SAlayout)
        self.search_animals.show()
        for page in self.openPages:
            page.close()
        self.search_animals.setWindowTitle('Search Animals')
        self.openPages.append(self.search_animals)


        self.table.horizontalHeader().sectionClicked.connect(self.ssa_column_sort)



    def ssa_column_sort(self, position):
        sort_by = self.headerNames[position]
        if sort_by == "Name":
            sort_by = "name"
        elif sort_by == "Exhibit":
            sort_by = "exhibit_name"
        elif sort_by == "Species":
            sort_by = "species"
        elif sort_by == "Age":
            sort_by = "age"
        elif sort_by == "Type":
            sort_by = "type"
        else:
            sort_by = "datetime"
        self.c = self.db.cursor()
        self.c.execute("SELECT name,species,exhibit_name,age,type FROM ANIMALS ORDER BY " + sort_by)
        result = self.c.fetchall()
        self.model = QStandardItemModel()
        for i in result:
            row = []
            for j in i:
                item = QStandardItem(str(j))
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)
        self.table.setModel(self.model)
        self.model.setHorizontalHeaderLabels(self.headerNames)

    def staff_search_animals_button(self):
        errorstr = ""
        count = 0
        count2 = 0
        fullQuery = "SELECT name, species, exhibit_name, age, type FROM ANIMALS"
        addQuery = []
#validation checks
        if len(str(self.wname.text())) > 0:
            self.name = str(self.wname.text())
            addQuery.append("lower(name) LIKE '%{}%'".format(self.name.lower()))
        if len(str(self.wSpecies.text())) > 0:
            self.species = str(self.wSpecies.text())
            addQuery.append("lower(species) LIKE '%{}%'".format(self.species.lower()))
        if len(str(self.exhibitDrop.currentText())) > 0:
            self.exhibit = str(self.exhibitDrop.currentText())
            addQuery.append("exhibit_name = '{}'".format(self.exhibit))
        if len(str(self.typeDrop.currentText())) > 0:
            self.type = str(self.typeDrop.currentText())
            addQuery.append("type = '{}'".format(self.type))
        if len(self.wmaxAge.text()) > 0:
            try:
                int(self.wmaxAge.text())
                self.maxAge = str(self.wmaxAge.text())
                addQuery.append("age <= '{}'".format(self.maxAge))
                count += 1
            except:
                errorstr += "- input for max age must be an integer\n"
                count2 += 1
        if len(self.wminAge.text()) > 0:
            try:
                int(self.wminAge.text())
                self.minAge = str(self.wminAge.text())
                addQuery.append("age >= '{}'".format(self.minAge))
                count += 1
            except:
                errorstr += "- input for min age must be an integer\n"
                count2 += 1
        if (count == 2) and (int(self.minAge) > int(self.maxAge)):
            errorstr += "- max age must be greater than min age\n"
            count2 += 1
        if (count2 > 0):
            messagebox.showwarning("Error", errorstr)

#appending to the where statements for SQL query
        if count2 == 0:
            if len(addQuery) > 0:
                fullQuery += " WHERE "
                for i in range(0,len(addQuery)-1):
                    fullQuery = fullQuery + addQuery[i] + " AND "
                fullQuery += addQuery[len(addQuery)-1]

#clear current table view before repoulating
        self.model.clear()
        self.table.setModel(self.model)

        self.c = self.db.cursor()
        self.c.execute(fullQuery)
        result = self.c.fetchall()
        for i in result:
            row = []
#converts item to list from tuple
            for j in i:
                item = QStandardItem(str(j))
#has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)

        self.headerNames = ["Name", "Species", "Exhibit", "Age", "Type"]
        self.model.setHorizontalHeaderLabels(self.headerNames)
        self.table.setModel(self.model)


    def staff_animal_care(self):
        animal = self.table.selectionModel().selectedIndexes()
        self.a_name = animal[0].data()
        self.a_spec = animal[1].data()
        e_name = animal[2].data()
        a_age = animal[3].data()
        a_type = animal[4].data()
        self.back= QPushButton("Back")

        SAlayout = QGridLayout()
        zooLabel = QLabel("Atlanta Zoo")
        emptyspace = QLabel("")
        namelbl = QLabel("Name: " + str(self.a_name))
        agelbl = QLabel("Age: " + str(a_age))
        specieslbl = QLabel("Species: " + str(self.a_spec))
        typelbl = QLabel("Type: " + str(a_type))
        exhibitlbl = QLabel("Exhibit: " + str(e_name))
        self.acNote = QLineEdit()
        logNotesButton = QPushButton("Log Note")


        self.notesTable = QTableView()
        self.notesModel = QStandardItemModel()
        self.notesModel.setColumnCount(3)
        self.headerNames = ["Staff Member", "Note","Time"]
        self.notesModel.setHorizontalHeaderLabels(self.headerNames)

        #need a method here to get only the notes for this animal

        self.notesTable.setModel(self.notesModel)
        self.notesTable.setColumnWidth(2,200)
        SAlayout = QGridLayout()
        SAlayout.setColumnStretch(1,6)
        SAlayout.setRowStretch(1,2)
        SAlayout.addWidget(zooLabel, 0,0)
        SAlayout.addWidget(emptyspace, 1,0)
        SAlayout.addWidget(namelbl, 2,0)
        SAlayout.addWidget(specieslbl,2,1)
        SAlayout.addWidget(emptyspace,2,2)
        SAlayout.addWidget(typelbl,3,1)
        SAlayout.addWidget(agelbl, 2,3)
        SAlayout.addWidget(exhibitlbl,3,0)
        SAlayout.addWidget(self.acNote,4,0)
        SAlayout.addWidget(logNotesButton,4,6)
        SAlayout.addWidget(self.notesTable,6,0,4,8)
        SAlayout.addWidget(self.back,0,6)
        self.db = self.Connect()
        self.c = self.db.cursor()

        self.c = self.db.cursor()
        self.c.execute("SELECT username, note, datetime FROM ANIMAL_CARE WHERE ANIMAL_CARE.name = (%s) and ANIMAL_CARE.species = (%s)", (self.a_name, self.a_spec))
        result = self.c.fetchall()
        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)

            self.notesModel.appendRow(row)

        logNotesButton.clicked.connect(self.add_ac_note)
        self.back.clicked.connect(self.back_out_of_animal_care)

        self.animal_care = QDialog()
        self.animal_care.setLayout(SAlayout)
        self.animal_care.show()
        self.animal_care.setWindowTitle('Animal Care')
        self.openPages.append(self.animal_care)

    def back_out_of_animal_care(self):
        self.animal_care.close()
        self.search_animals.setFocus()

    def add_ac_note(self):
        user = QStandardItem(str(self.my_user[1]))
        user.setEditable(False)
        note = QStandardItem(str(self.acNote.text()))
        note.setEditable(False)
        now = QStandardItem(str(datetime.now()))
        now.setEditable(False)
        self.c.execute("INSERT INTO ANIMAL_CARE VALUES (%s,%s,%s,%s,%s)",(str(self.a_name), str(self.a_spec), str(self.my_user[1]), str(str(datetime.now())), str(self.acNote.text())))
        row = [user,note,now]
        self.notesModel.appendRow(row)
        self.notesTable.setModel(self.notesModel)


    def admin_view_shows(self):
        SSlayout = QGridLayout()
        self.title1 = QLabel("Atlanta Zoo")
        self.search = QPushButton("Search")
        self.name = QLabel("Name: ")
        self.wname = QLineEdit()
        self.date = QLabel("Date: ")
        self.date = QLabel("Date: ")
        self.dateDrop = QDateEdit() #this is wrong implementation
        self.dateDrop.setCalendarPopup(True)
        self.dateDrop.calendarWidget().installEventFilter(self)
        self.dateDrop.setSpecialValueText(" ")
        self.dateDrop.setDate(QDate.fromString( "01/01/0001", "dd/MM/yyyy" ))
        self.dateDrop.setMinimumDate(QDate.fromString( "01/01/2010", "dd/MM/yyyy" ))
        self.back = QPushButton("Back")
        self.exhibit = QLabel("Exhibit: ")
        self.exhibitDrop = QComboBox()
        self.RemoveShow = QPushButton("Remove Show")
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        self.headerNames = ["Name", "Exhibit", "Date"]
        self.model.setHorizontalHeaderLabels(self.headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")

    #exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])

    #fill dedfault table
        self.c = self.db.cursor()
        self.c.execute("SELECT show_name, exhibit_name, datetime FROM SHOWS")
        result = self.c.fetchall()
        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)

            self.model.appendRow(row)

        self.exhibitDrop.addItems(exDrop)
        self.table.setModel(self.model)
        self.table.setColumnWidth(2,150)

        SSlayout = QGridLayout()
        SSlayout.setColumnStretch(1,3)
        SSlayout.setRowStretch(1,3)
        SSlayout.addWidget(self.title1,1,0)
        SSlayout.addWidget(self.search,3,3)
        SSlayout.addWidget(self.name, 2,0)
        SSlayout.addWidget(self.wname,2,1)
        SSlayout.addWidget(self.date,2,2)
        SSlayout.addWidget(self.dateDrop,2,3)
        SSlayout.addWidget(self.exhibit,3,0)
        SSlayout.addWidget(self.exhibitDrop,3,1)
        SSlayout.addWidget(self.table,4,0,4,6)
        SSlayout.addWidget(self.RemoveShow,8,3)
        SSlayout.addWidget(self.back,8,0)

        self.RemoveShow.clicked.connect(self.remove_show)
        self.search.clicked.connect(self.search_shows_button)

        self.back.clicked.connect(self.bac_button)

        self.table.horizontalHeader().sectionClicked.connect(self.vss_column_sort)

        self.view_shows = QDialog()
        self.view_shows.setLayout(SSlayout)
        self.view_shows.setWindowTitle('View Shows')
        self.view_shows.show()
        for page in self.openPages:
            page.close()
        self.openPages.append(self.view_shows)


        self.table.horizontalHeader().sectionClicked.connect(self.avshow_column_sort)



    def avshow_column_sort(self, position):
        sort_by = self.headerNames[position]
        if sort_by == "Name":
            sort_by = "show_name"
        elif sort_by == "Exhibit":
            sort_by = "exhibit_name"
        else:
            sort_by = "datetime"
        self.c = self.db.cursor()
        self.c.execute("SELECT show_name, exhibit_name, datetime FROM SHOWS ORDER BY " + sort_by)
        result = self.c.fetchall()
        self.model = QStandardItemModel()
        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)
        self.table.setModel(self.model)
        self.model.setHorizontalHeaderLabels(self.headerNames)

    def remove_show(self):

        show = self.table.selectionModel().selectedIndexes()
        if len(show) == 0:
            messagebox.showwarning("Error", "Please select a show to remove.")
        else:
            name = str(show[0].data())
            exhibit = str(show[1].data())
            time = str(show[2].data())
            self.db = self.Connect()
            self.c = self.db.cursor()
            self.c.execute("DELETE FROM SHOWS WHERE show_name = (%s) and datetime = (%s) and exhibit_name = (%s)", (name,time,exhibit))


            for index in sorted(show):

                self.model.removeRow(index.row())
                break
            self.table.setModel(self.model)
            messagebox.showwarning("Show Removed", "The show has been removed.")

    def admin_view_animals(self):
        SAlayout = QGridLayout()
        self.title1 = QLabel("Atlanta Zoo")
        self.search = QPushButton("search")
        self.name = QLabel("Name: ")
        self.wname = QLineEdit()
        self.wname = QLineEdit()
        self.age = QLabel("Age: ")
        self.minAge = QLabel("max")
        self.wminAge = QLineEdit()
        self.maxAge = QLabel("min")
        self.Species = QLabel("Species: ")
        self.wSpecies = QLineEdit()
        self.wmaxAge = QLineEdit()
        self.exhibit = QLabel("Exhibit: ")
        self.exhibitDrop = QComboBox()
        self.RemoveAnimal = QPushButton("Remove Animal")
        self.back = QPushButton("Back")

        self.table = QTableView()

        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        self.headerNames = ["Name", "Species","Exhibit", "Age", "Type"]
        self.model.setHorizontalHeaderLabels(self.headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")

#exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])

#fill dedfault table
        self.c = self.db.cursor()
        self.c.execute("SELECT name,species,exhibit_name,age,type FROM ANIMALS")
        result = self.c.fetchall()
        for i in result:
            row = []
#converts item to list from tuple
            for j in i:
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)

        self.exhibitDrop.addItems(exDrop)
        self.table.setModel(self.model)
        self.table.setColumnWidth(4,100)

        SAlayout = QGridLayout()
        SAlayout.setColumnStretch(1,5)
        SAlayout.setRowStretch(1,5)
        SAlayout.addWidget(self.title1,1,0)
        SAlayout.addWidget(self.search,2,3)
        SAlayout.addWidget(self.name, 2,0)
        SAlayout.addWidget(self.wname,2,1)
        SAlayout.addWidget(self.Species,3,0)
        SAlayout.addWidget(self.wSpecies, 3,1)
        SAlayout.addWidget(self.age, 5,0)
        SAlayout.addWidget(self.maxAge,4,1)
        SAlayout.addWidget(self.minAge,4,2)
        SAlayout.addWidget(self.wminAge,5,1)
        SAlayout.addWidget(self.wmaxAge,5,2)
        SAlayout.addWidget(self.exhibit,3,2)
        SAlayout.addWidget(self.exhibitDrop,3,3)
        SAlayout.addWidget(self.table,6,0,3,10)
        SAlayout.addWidget(self.RemoveAnimal,10,3)
        SAlayout.addWidget(self.back,10,0)

        self.RemoveAnimal.clicked.connect(self.remove_animals)
        self.search.clicked.connect(self.search_animals_button)

        self.back.clicked.connect(self.bac_button)
#found in line 1025, written after visitor_search_animals function

        self.table.horizontalHeader().sectionClicked.connect(self.ava_column_sort)
#found in line 1025, written after visitor_search_animals

        self.view_animals = QDialog()
        self.view_animals.setLayout(SAlayout)
        self.view_animals.setWindowTitle('View Animals')
        self.view_animals.show()
        for page in self.openPages:
            page.close()
        self.openPages.append(self.view_animals)


        self.table.horizontalHeader().sectionClicked.connect(self.ava_column_sort)


    def ava_column_sort(self, position):
        sort_by = self.headerNames[position]
        if sort_by == "Name":
            sort_by = "name"
        elif sort_by == "Species":
            sort_by = "species"
        elif sort_by == "Exhibit":
            sort_by = "exhibit_name"
        elif sort_by == "Age":
            sort_by = "age"
        else:
            sort_by = "type"
        self.c = self.db.cursor()
        self.c.execute("SELECT name,species,exhibit_name,age,type FROM ANIMALS ORDER BY " + sort_by)
        result = self.c.fetchall()
        self.model = QStandardItemModel()
        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)
        self.table.setModel(self.model)
        self.model.setHorizontalHeaderLabels(self.headerNames)

    def remove_animals(self):
        animal = self.table.selectionModel().selectedIndexes()
        if len(animal) == 0:
            messagebox.showwarning("Error", " Please select an animal to remove.")
        else:
            name = str(animal[0].data())
            species = str(animal[1].data())
            self.db = self.Connect()
            self.c = self.db.cursor()

            self.c.execute("DELETE FROM ANIMALS WHERE name = (%s) and species = (%s)", (name,species))
            for index in sorted(animal):
                self.model.removeRow(index.row())
                break
            self.table.setModel(self.model)
            messagebox.showwarning("Animal Removed", "The animal has been removed.")

    def staff_view_shows(self):

        atlantaZoo = QLabel()
        atlantaZoo.setText("Atlanta Zoo")
        showHistory = QLabel()
        self.back = QPushButton("Back")

        SSlayout = QGridLayout()
        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        self.headerNames = ["Name", "Time", "Exhibit"]
        self.model.setHorizontalHeaderLabels(self.headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT show_name, datetime, exhibit_name FROM SHOWS WHERE SHOWS.username=%s",(self.my_user[1]))
        result = self.c.fetchall()
        for i in result:
            row = []
            for j in i: #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)

        self.table.setModel(self.model)

        self.table.setColumnWidth(1,200)
        self.table.setColumnWidth(2,100)

        self.table.horizontalHeader().sectionClicked.connect(self.svs_column_sort)

        SSlayout = QGridLayout()
        SSlayout.setColumnStretch(1,2)
        SSlayout.setRowStretch(1,2)
        SSlayout.addWidget(atlantaZoo,0,0)
        SSlayout.addWidget(self.table,2,0,2,28)
        SSlayout.addWidget(self.back,8,8)

        self.view_shows = QDialog()
        self.view_shows.setLayout(SSlayout)
        self.view_shows.setWindowTitle('View Shows')
        self.view_shows.show()
        for page in self.openPages:
            page.close()
        self.openPages.append(self.view_shows)

        self.back.clicked.connect(self.bac_button)

        self.table.horizontalHeader().sectionClicked.connect(self.svs_column_sort)


    def svs_column_sort(self, position):
        sort_by = self.headerNames[position]
        if sort_by == "Name":
            sort_by = "show_name"
        elif sort_by == "Exhibit":
            sort_by = "exhibit_name"
        else:
            sort_by = "datetime"
        self.c = self.db.cursor()
        self.c.execute("SELECT show_name, datetime, exhibit_name FROM SHOWS WHERE SHOWS.username=%s ORDER BY " + sort_by, (self.my_user[1]))
        result = self.c.fetchall()
        self.model = QStandardItemModel()
        for i in result:
            row = []
            for j in i:
                item = QStandardItem(str(j))
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)
        self.table.setModel(self.model)
        self.model.setHorizontalHeaderLabels(self.headerNames)


    def svs_column_sort(self, position):
        sort_by = self.headerNames[position]
        if sort_by == "Name":
            sort_by = "show_name"
        elif sort_by == "Exhibit":
            sort_by = "exhibit_name"
        else:
            sort_by = "datetime"
        self.c = self.db.cursor()
        self.c.execute("SELECT show_name, datetime, exhibit_name FROM SHOWS WHERE SHOWS.username=%s ORDER BY " + sort_by, (self.my_user[1]))
        result = self.c.fetchall()
        self.model = QStandardItemModel()
        for i in result:
            row = []
            for j in i:
                item = QStandardItem(str(j))
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)
        self.table.setModel(self.model)
        self.model.setHorizontalHeaderLabels(self.headerNames)


    def search_exhibits(self):
        SElayout = QGridLayout()

        self.search = QPushButton("search")
        self.name = QLabel("Name: ")
        self.wname = QLineEdit()
        self.NumAnimals = QLabel("Number of Animals")
        self.animalMin = QLabel("Min")
        self.animalMax = QLabel("Max")
        self.wanimalMin = QLineEdit()
        self.wanimalMax = QLineEdit()
        self.Size = QLabel("Size")
        self.sizeMin = QLabel("Min")
        self.sizeMax = QLabel("Max")
        self.wsizeMin = QLineEdit()
        self.wsizeMax = QLineEdit()
        self.Water = QLabel("Water Feature")
        self.waterDrop = QComboBox()

        self.waterDrop.addItems(["","Yes","No"])
        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT * FROM EXHIBITS")
        result = self.c.fetchall()


        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(4)
        self.headerNames = ["Exhibit Name", "Water", "Number of Animals", "Size"]
        self.model.setHorizontalHeaderLabels(self.headerNames)

        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)

            self.model.appendRow(row)

        self.table.setModel(self.model)

        SElayout = QGridLayout()
        SElayout.setColumnStretch(1,3)
        SElayout.setRowStretch(1,3)

        SElayout.addWidget(self.search,1,3)
        SElayout.addWidget(self.name, 2,0)
        SElayout.addWidget(self.wname,2,1)
        SElayout.addWidget(self.NumAnimals, 4,0)
        SElayout.addWidget(self.animalMin,3,1)
        SElayout.addWidget(self.animalMax,3,2)
        SElayout.addWidget(self.wanimalMin,4,1)
        SElayout.addWidget(self.wanimalMax,4,2)
        SElayout.addWidget(self.sizeMin,5,1)
        SElayout.addWidget(self.sizeMax,5,2)
        SElayout.addWidget(self.Size,6,0)
        SElayout.addWidget(self.wsizeMin,6,1)
        SElayout.addWidget(self.wsizeMax,6,2)
        SElayout.addWidget(self.Water, 7,0)
        SElayout.addWidget(self.waterDrop, 7,1)

        SElayout.addWidget(self.table,8,0,4,4)

        self.search_exhibits = QDialog()
        self.search_exhibits.setLayout(SElayout)
        self.search_exhibits.setWindowTitle('Search Exhibits')
        self.search_exhibits.show()
        for page in self.openPages:
            page.close()

        self.search.clicked.connect(self.exhibitSearch)

    def vse_column_sort(self, position):
        sort_by = self.headerNames[position]
        if sort_by == "Exhibit Name":
            sort_by = "exhibit_name"
        elif sort_by == "Water":
            sort_by = "water"
        elif sort_by == "Number of Animals":
            sort_by = "number_of_animals"
        else:
            sort_by = "size"
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name, water, number_of_animals, size FROM EXHIBITS ORDER BY " + sort_by)
        result = self.c.fetchall()
        self.model = QStandardItemModel()
        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
            self.model.appendRow(row)
        self.table.setModel(self.model)
        self.model.setHorizontalHeaderLabels(self.headerNames)

    def exhibitSearch(ds):
        self.animalMin = str(self.wanimalMin.text())
        self.animalMax = str(self.wanimalMax.text())
        self.sizeMin = str(self.wsizeMin.text())
        self.sizeMax = str(self.wsizeMax.text())
        printstr = ""
        count = 0
        count2 = 0

        try:
            self.animalMin = int(str(self.wanimalMin.text()))
        except:
            printstr += "- input for min animal number must be integer\n"
            count += 1
        try:
            self.animalMax = int(str(self.wanimalMax.text()))
        except:
            printstr += "- input for max animal number must be integer\n"
            count += 1
        if count == 0:
            if (self.animalMin > self.animalMax):
                printstr += "- min animals must be less than max animals\n"
                count += 1
        try:
            self.sizeMin = int(str(self.wsizeMin.text()))
        except:
            printstr += "- input for min size must be integer\n"
            count2 += 1
        try:
            self.sizeMax = int(str(self.wsizeMax.text()))
        except:
            printstr += "- input for max size must be integer\n"
            count2 += 1
        if count2 == 0:
            if (self.sizeMin > self.sizeMax):
                printstr += "- min size must be less than max size\n"
                count2 += 1
        if ((count == 0) and (count2 == 0)):
            pass
        else:
            messagebox.showwarning("Error", printstr)


    def search_shows(self):
        self.setWindowTitle('Shows')
        SSlayout = QGridLayout()

        self.title1 = QLabel("Atalnta Zoo")
        self.title2 = QLabel("Shows")
        self.search = QPushButton("search")
        self.name = QLabel("Name: ")
        self.wname = QLineEdit()
        self.date = QLabel("Date: ")
        self.dateDrop = QComboBox() #this is wrong implementation
        self.exhibit = QLabel("Exhibit: ")
        self.exhibitDrop = QComboBox()
        self.logVisit = QPushButton("Log Visit")
        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        self.headerNames = ["Name", "Exhibit", "Date"]
        self.model.setHorizontalHeaderLabels(self.headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")

        #exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])

        #fill dedfault table
        self.c = self.db.cursor()
        self.c.execute("SELECT show_name, exhibit_name, datetime FROM SHOWS")
        result = self.c.fetchall()
        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)

            self.model.appendRow(row)

        self.exhibitDrop.addItems(exDrop)
        self.table.setModel(self.model)

        SSlayout = QGridLayout()
        SSlayout.setColumnStretch(1,3)
        SSlayout.setRowStretch(1,3)
        SSlayout.addWidget(self.title1,1,0)
        SSlayout.addWidget(self.title2, 1,2)
        SSlayout.addWidget(self.search,3,3)
        SSlayout.addWidget(self.name, 2,0)
        SSlayout.addWidget(self.wname,2,1)
        SSlayout.addWidget(self.date,2,2)
        SSlayout.addWidget(self.dateDrop,2,3)
        SSlayout.addWidget(self.exhibit,3,0)
        SSlayout.addWidget(self.exhibitDrop,3,1)
        SSlayout.addWidget(self.table,4,0,4,4)
        SSlayout.addWidget(self.logVisit,8,3)

        self.search_exhibits = QDialog()
        self.search_exhibits.setLayout(SSlayout)
        self.search_exhibits.show()
        for page in self.openPages:
            page.close()

    def try_again(self):
        self.password_line_edit.clear()

    def check_user(self):
        user = str(self.user_line_edit.text())
        pswd = str(self.password_line_edit.text())
        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT password FROM USERS AS U WHERE U.username=%s",(user))
        passhashtuple = self.c.fetchone()

        if (passhashtuple != None):
            passhash = passhashtuple[0]
            self.db = self.Connect()
            self.c = self.db.cursor()
            if pbkdf2_sha256.verify(pswd, passhash):
                self.c.execute("SELECT * FROM USERS AS U WHERE U.username=%s",(user))
                self.my_user = self.c.fetchone()
                if (self.my_user[3] == 'visitor'):
                    self.visitor_functionality()
                    self.logged_in = True
                    self.password_line_edit.clear()
                    self.user_line_edit.clear()
                    self.user_line_edit.setFocus()
                elif (self.my_user[3] == 'admin'):
                    self.admin_functionality()
                    self.logged_in = True
                    self.password_line_edit.clear()
                    self.user_line_edit.clear()
                    self.user_line_edit.setFocus()
                elif (self.my_user[3] == 'staff'):
                    self.staff_functionality()
                    self.logged_in = True
                    self.password_line_edit.clear()
                    self.user_line_edit.clear()
                    self.user_line_edit.setFocus()
                else:
                    messagebox.showwarning("Error", "Unrecognized account type.\nCheck database.")
            else:
                messagebox.showwarning("Error", "Username or password incorrect. \n Please try again.")
                self.try_again()
        else:
            messagebox.showwarning("Error", "Username or password incorrect. \n Please try again.")
            self.try_again()



    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Return):
            if (self.logged_in):
                pass
            else:
                self.check_user()


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
        self.wpswd.setEchoMode(QLineEdit.Password)
        self.wconfirmpswd.setEchoMode(QLineEdit.Password)

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

            printstr += "Password needs to be more than 8 characters\n"
            count += 1

        if self.confirmpswd != self.pswd:

            printstr += "Password must match Confirm Password\n"
            count+=1

        if not re.match(r"^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$",self.email):
            printstr += "Please use a valid email address."
            count+=1

        if len(self.user) == 0:
            printstr += "Username input needed \n"
            count+=1

        self.c.execute("SELECT email FROM USERS WHERE email = (%s)",self.email)
        emailFound = self.c.fetchall()
        if len(emailFound) != 0:
            printstr += "Email belongs to another a user\n"
            count += 1

        self.c.execute("SELECT email FROM USERS WHERE username = (%s)",self.user)
        username_found = self.c.fetchall()
        if len(username_found) != 0:
            printstr += "Username belongs to another a user\n"
            count += 1

        if count > 0:
            messagebox.showwarning("Error", printstr)


#adding the visitor to the database
        else:
            passwd = str(pbkdf2_sha256.hash(self.pswd))
            self.c.execute("INSERT INTO USERS VALUES (%s,%s,%s,%s)",(self.email, self.user, passwd, "visitor"))
            messagebox.showwarning("Registered", "Visitor account has been registered")
            self.go_to_register.close()



    def register_staff(self):
#getting information from the registration page for staff registration
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

            printstr += "Password needs to be more than 8 characters\n"
            count += 1

        if self.confirmpswd != self.pswd:

            printstr += "Password must match Confirm Password\n"
            count+=1

        if not re.match(r"^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$",self.email):
            printstr += "Please use a valid email address."
            count+=1

        if len(self.user) == 0:
            printstr += "Username input needed \n"
            count+=1

        self.c.execute("SELECT email FROM USERS WHERE email = (%s)",self.email)
        emailFound = self.c.fetchall()
        if len(emailFound) != 0:
            printstr += "Email belongs to another a user\n"
            count += 1

        self.c.execute("SELECT email FROM USERS WHERE username = (%s)",self.user)
        username_found = self.c.fetchall()
        if len(username_found) != 0:
            printstr += "Username belongs to another a user\n"
            count += 1

        if count > 0:
            messagebox.showwarning("Error", printstr)


#adding the visitor to the database
        else:
            passwd = str(pbkdf2_sha256.hash(self.pswd))
            self.c.execute("INSERT INTO USERS VALUES (%s,%s,%s,%s)",(self.email, self.user, passwd, "staff"))
            messagebox.showwarning("Registered", "Staff account has been registered")
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
        self.setWindowTitle('Atlanta Zoo')
        self.vbox = QVBoxLayout()

if __name__=='__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
