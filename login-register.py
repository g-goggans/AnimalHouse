#!/usr/bin/env python3

############################
# WORKING FUNCTIONALITIES
# - visitor search exhibits
# - visitor search shows
# - visitor search animals
# - staff search animals 
#     - issue with exhibit drop down menu (Combobox)
# - admin view visitors
# - admin view staff
# - admin view animals 
# - admin view shows 
# - admin add animal 
#       - does not exit out after animal is successfully added
# - admin add show 
#     - does not exit out after show is successfully added
############################
# NONWORKING FUNCTIONALITIES
# - a lot of the .close() implmentations for most functionalities
# - visitor view show history 
#     - idk if the search results are correct
#     - is visitor only supposed to see the shows that he/she has attended
#     - or does visitor see all shows (even ones he/she didn't visit)
# - visitor view exhibit history
#     - same issue as visitor view show history
# - staff view show history
#############################

import sys
from datetime import datetime

import tkinter as tk
from tkinter import *
import tkinter.messagebox as messagebox

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

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

        self.register_button.clicked.connect(self.go_to_register)
        self.login_button.clicked.connect(self.check_user)
        # self.login_button.clicked.connect(self.close)
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

    def visitor_functionality(self):
    #buttons that appear on main page
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

        self.newWindow = TableWindow()
        self.newWindow.setLayout(layout)
        self.newWindow.show()
        self.LogOut.clicked.connect(self.newWindow.close)
        self.LogOut.clicked.connect(self.close)
        layout.addWidget(self.LogOut)


    def admin_functionality(self):
    #buttons that appear on main page
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
        self.newWindow.show()
        self.ViewShows.clicked.connect(self.admin_view_shows)
        self.ViewAnimals.clicked.connect(self.admin_view_animals)
        self.AddAnimals.clicked.connect(self.admin_add_animals)
        self.ViewStaff.clicked.connect(self.admin_view_staff)
        self.ViewVisitors.clicked.connect(self.admin_view_visitor)
        self.AddShow.clicked.connect(self.admin_add_show)


        self.LogOut.clicked.connect(self.newWindow.close)
        self.LogOut.clicked.connect(self.close)
        layout.addWidget(self.LogOut)

    def admin_add_show(self):
        self.setWindowTitle('Add Show')
        SAlayout = QGridLayout()

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

        self.AddShow = QPushButton("Add Show")

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")
#exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])
        #print(exDrop)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT username FROM USERS where user_type = 'staff'")

#type drop down menu contents
        result2 = self.c.fetchall()
        stDrop = [""]
        for i in result2:
            stDrop.append(i[0])
        print(stDrop)

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

        self.AddShow.clicked.connect(self.admin_add_show_button)

        self.add_shows = QDialog()
        self.add_shows.setLayout(SAlayout)
        self.add_shows.show()

    def admin_add_show_button(self):
        datestring = "Jun 1 2005  1:33PM"
        datestring = datetime.strptime(datestring, '%b %d %Y %I:%M%p')
        print(datestring)
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
                print(self.hour)
            if len(self.minute) == 1:
                self.minute = "0" + self.minute
                print(self.minute)
#converting date to correct datetime format
            self.year = ""
            for i in range(19,23):
                self.year += self.showDate[i]
            print(self.year)

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
            print(self.showDate)
            print(type(self.showDate))
            print(self.staff)
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
        print("view_staff")
        self.setWindowTitle('View Staff')
        SAlayout = QGridLayout()

        self.RemoveStaff = QPushButton("Remove Staff Member")
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)

        self.model = QStandardItemModel()
        self.model.setColumnCount(2)
        headerNames = ["Username", "Email"]
        self.model.setHorizontalHeaderLabels(headerNames)

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

        SAlayout = QGridLayout()
        SAlayout.setColumnStretch(1,8)
        SAlayout.setRowStretch(1,4)
        SAlayout.addWidget(self.table,6,0,4,4)
        SAlayout.addWidget(self.RemoveStaff,10,4)

        self.RemoveStaff.clicked.connect(self.remove_staff)

        self.view_staff = QDialog()
        self.view_staff.setLayout(SAlayout)
        self.view_staff.show()

    def remove_staff(self):
        staff = self.table.selectionModel().selectedIndexes()
        name = str(staff[0].data())
        email = str(staff[1].data())
        #print(name,email)
        self.db = self.Connect()
        self.c = self.db.cursor()

        self.c.execute("DELETE FROM USERS WHERE USERS.username = (%s)",name)
        #print("Removed",name,email)
#deletes item selected
        for index in sorted(staff):
            self.model.removeRow(index.row())
            break 
        self.table.setModel(self.model)
        #print("Updated table")

    def admin_add_animals(self):
        self.setWindowTitle('Add Animal')
        SAlayout = QGridLayout()

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

        self.add_animals = QDialog()
        self.add_animals.setLayout(SAlayout)
        self.add_animals.show()

        self.AddAnimal.clicked.connect(self.admin_add_animal_button)
        self.AddAnimal.clicked.connect(self.close)

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
            messagebox.showwarning("Congrats", "Animals has been successfully added")
            ########################################
            # I don't know how to close this
            ######################################### 
            self.close()
            

    def admin_view_visitor(self):
        self.setWindowTitle('View Visitors')
        SAlayout = QGridLayout()

        self.RemoveVisitor = QPushButton("Remove Visitor")
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.model = QStandardItemModel()
        self.model.setColumnCount(2)

        atlantaZoo = QLabel()
        atlantaZoo.setText("Atlanta Zoo")
        viewVisitors = QLabel()
        viewVisitors.setText("Staff - View Visitors")

        headerNames = ["Username", "Email"]
        self.model.setHorizontalHeaderLabels(headerNames)

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

        SAlayout = QGridLayout()
        SAlayout.setColumnStretch(1,8)
        SAlayout.setRowStretch(1,4)
        SAlayout.addWidget(atlantaZoo,0,0)
        SAlayout.addWidget(viewVisitors,0,1)
        SAlayout.addWidget(self.table,6,0,4,4)
        SAlayout.addWidget(self.RemoveVisitor,10,4)

        self.RemoveVisitor.clicked.connect(self.remove_visitor)

        self.view_visitors = QDialog()
        self.view_visitors.setLayout(SAlayout)
        self.view_visitors.show()

    def remove_visitor(self):
        visitor = self.table.selectionModel().selectedIndexes()
        name = str(visitor[0].data())
        email = str(visitor[1].data())
        #print(name,email)
        self.db = self.Connect()
        self.c = self.db.cursor()

        self.c.execute("DELETE FROM USERS WHERE USERS.username = (%s)",name)

        #print("Removed",name,email)
#deletes item selected
        for index in sorted(visitor):
            self.model.removeRow(index.row()) 
            break
        self.table.setModel(self.model)
        #print("Updated table")


    def staff_functionality(self):

    #buttons that appear on main page
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
        self.newWindow.show()
        self.ViewShows.clicked.connect(self.staff_view_shows)
        self.SearchAnimals.clicked.connect(self.staff_search_animals)

        self.LogOut.clicked.connect(self.newWindow.close)

        self.LogOut.clicked.connect(self.close)
        layout.addWidget(self.LogOut)


    def visitor_search_exhibits(self):
        self.setWindowTitle('Exhibits')
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
        #print(result)

        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(4)
        headerNames = ["Exhibit Name", "Water", "Number of Animals", "Size"]
        self.model.setHorizontalHeaderLabels(headerNames)

        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
                #print(row)
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
        self.search_exhibits.show()

        self.search.clicked.connect(self.visitor_exhibit_search_button)

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
                addQuery.append("number_of_animals > '{}'".format(self.animalMin))
                count2 += 1
            except:
                printstr += "- input for min animal number must be integer\n"
                count += 1
        if len(self.animalMax) > 0:
            try:
                self.animalMax = int(str(self.wanimalMax.text()))
                self.animalMax = str(self.wanimalMax.text())
                addQuery.append("number_of_animals < '{}'".format(self.animalMax))
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
                addQuery.append("size > '{}'".format(self.sizeMin))
                count4 += 1
            except:
                printstr += "- input for min size must be integer\n"
                count3 += 1
        if len(self.sizeMax) > 0:
            try:
                self.sizeMax = int(str(self.wsizeMax.text()))
                self.sizeMax = str(self.wsizeMax.text())
                addQuery.append("size < '{}'".format(self.sizeMax))
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
            print("execute query")
            #print(addQuery)
            if len(addQuery) > 0:
                fullQuery += " WHERE "
                for i in range(0,len(addQuery)-1):
                    fullQuery = fullQuery + addQuery[i] + " AND "
                fullQuery += addQuery[len(addQuery)-1]
            print(fullQuery)
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

            headerNames = ["Exhibit_Name", "Water", "Number of Animals", "Size"]
            self.model.setHorizontalHeaderLabels(headerNames)
            self.table.setModel(self.model)
            self.table.resizeColumnsToContents()
        else:
            messagebox.showwarning("Error", printstr)
            #print(printstr)

    def Visitor_Exhibit_History(self):
        self.setWindowTitle('Exhibit History')
        SSlayout = QGridLayout()

        self.search = QPushButton("search")

        self.name = QLabel("Name: ")
        self.wname = QLineEdit()

        self.date = QLabel("Date: ")
        self.dateDrop = QComboBox() #this is wrong implementation

        self.NumVisits = QLabel("Number of Visits: ")
        self.minVisits = QLineEdit()
        self.maxVisits = QLineEdit()
        self.minVisitsLabel = QLabel("Min")
        self.maxVisitsLabel = QLabel("Max")

        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        headerNames = ["Name", "Exhibit", "Date"]
        self.model.setHorizontalHeaderLabels(headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")

        SSlayout = QGridLayout()
        SSlayout.setColumnStretch(1,3)
        SSlayout.setRowStretch(1,3)
        SSlayout.addWidget(self.search,3,3)
        SSlayout.addWidget(self.name, 1,0)
        SSlayout.addWidget(self.wname,1,1)
        SSlayout.addWidget(self.date,2,0)
        SSlayout.addWidget(self.dateDrop,2,1)
        SSlayout.addWidget(self.NumVisits,1,2)
        SSlayout.addWidget(self.minVisitsLabel,0,3)
        SSlayout.addWidget(self.maxVisitsLabel,0,4)
        SSlayout.addWidget(self.maxVisits,1,4)
        SSlayout.addWidget(self.minVisits,1,3)
        SSlayout.addWidget(self.table,4,0,4,4)

        self.search_exhibits = QDialog()
        self.search_exhibits.setLayout(SSlayout)
        self.search_exhibits.show()

    def Visitor_Show_History(self):
        self.setWindowTitle('Show History')
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

        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        headerNames = ["Name", "Date", "Exhibit"]
        self.model.setHorizontalHeaderLabels(headerNames)

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
        self.c.execute("SELECT show_name, datetime, exhibit_name FROM SHOWS")
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

        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

        SSlayout = QGridLayout()
        SSlayout.setColumnStretch(1,5)
        SSlayout.setRowStretch(1,5)
        SSlayout.addWidget(self.search,3,7)
        SSlayout.addWidget(self.name, 1,0,1,1)
        SSlayout.addWidget(self.wname,1,1)
        SSlayout.addWidget(self.date,2,0)
        SSlayout.addWidget(self.calendar,2,1,1,5)
        SSlayout.addWidget(self.exhibit_name,3,0)
        SSlayout.addWidget(self.exhibitDrop,3 ,1)
        SSlayout.addWidget(self.table,4,0,6,6)

        self.search.clicked.connect(self.view_show_history_search)

        self.search_exhibits = QDialog()
        self.search_exhibits.setLayout(SSlayout)
        self.search_exhibits.show()

    def view_show_history_search(self):
        self.name = str(self.wname.text())
        self.exhibit = str(self.exhibitDrop.currentText())

        addQuery = []
        if len(self.exhibit) != 0:
            addQuery.append("exhibit_name = '{}'".format(self.exhibit))
        if len(self.name) != 0:
            addQuery.append("lower(show_name) LIKE '%{}%'".format(self.name.lower()))
        #######################################################
        # need to figure out how to set up no default date
        #######################################################
        self.date = str(self.calendar.date())
        if self.date == "PyQt5.QtCore.QDate(2010, 1, 1)":
            self.date = ""
        else:
            self.year = ""
            for i in range(19,23):
                self.year += self.date[i]
            print(self.year)
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
            print(self.date)
            addQuery.append("DATE(datetime) = '{}'".format(self.date))

        fullQuery = "SELECT show_name, datetime, exhibit_name FROM SHOWS"
        if len(addQuery) > 0:
            fullQuery += " WHERE "
            for i in range(0,len(addQuery)-1):
                fullQuery = fullQuery + addQuery[i] + " and "
            fullQuery += addQuery[len(addQuery)-1]

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute(fullQuery)
        result = self.c.fetchall()

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

        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

    def visitor_search_shows(self):
        self.setWindowTitle('Shows')
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
        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        headerNames = ["Name", "Exhibit", "Date"]
        self.model.setHorizontalHeaderLabels(headerNames)

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

        self.search.clicked.connect(self.search_shows_button)

        self.search_exhibits = QDialog()
        self.search_exhibits.setLayout(SSlayout)
        self.search_exhibits.show()

#DO NOT CHANGE THE NAME OF THIS METHOD
#STAFF AND VISITOR BOTH USE THIS METHOD TO SEARCH FOR SHOWS
    def search_shows_button(self):
        fullQuery = "SELECT show_name, datetime, exhibit_name FROM SHOWS"
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

        headerNames = ["Name", "Exhibit", "Date"]
        self.model.setHorizontalHeaderLabels(headerNames)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

    def visitor_search_animals(self):
        self.setWindowTitle('Shows')
        SAlayout = QGridLayout()

        self.title1 = QLabel("Atalnta Zoo")
        self.title2 = QLabel("Animals")
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
        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        headerNames = ["Name", "Species","Exhibit", "Age", "Type"]
        self.model.setHorizontalHeaderLabels(headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")

#exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])
        #print(exDrop)

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
        SAlayout.addWidget(self.title2, 1,2)
        SAlayout.addWidget(self.search,2,3)
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
        SAlayout.addWidget(self.table,6,0,4,4)

        self.search.clicked.connect(self.search_animals_button)

        self.search_exhibits = QDialog()
        self.search_exhibits.setLayout(SAlayout)
        self.search_exhibits.show()

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
                addQuery.append("age < '{}'".format(self.maxAge))
                count += 1 
            except:
                errorstr += "- input for max age must be an integer\n"
                count2 += 1
        if len(self.wminAge.text()) > 0:
            try:
                int(self.wminAge.text())
                self.minAge = str(self.wminAge.text())
                addQuery.append("age > '{}'".format(self.minAge))
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

        headerNames = ["Name", "Species", "Exhibit", "Age", "Type"]
        self.model.setHorizontalHeaderLabels(headerNames)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()


    def staff_search_animals(self):
        self.setWindowTitle('Animals')
        SAlayout = QGridLayout()

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
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")
#exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])
        self.exhibitDrop.addItems(exDrop)

        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        headerNames = ["Name", "Species","Exhibit", "Age", "Type"]
        self.model.setHorizontalHeaderLabels(headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")

#exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])
        #print(exDrop)

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

        self.exhibitDrop.addItems(exDrop)
        self.table.setModel(self.model)
        self.table.doubleClicked.connect(self.staff_animal_care)

        SAlayout = QGridLayout()
        SAlayout.setColumnStretch(1,3)
        SAlayout.setRowStretch(1,2)
        SAlayout.addWidget(self.name, 2,0)
        SAlayout.addWidget(self.wname,2,1)
        SAlayout.addWidget(self.Species,3,0)
        SAlayout.addWidget(self.wSpecies, 3,1)
        SAlayout.addWidget(self.Type,5,3)
        SAlayout.addWidget(self.typeDrop,5,4)
        SAlayout.addWidget(self.age, 5,0)
        SAlayout.addWidget(self.maxAge,4,2)
        SAlayout.addWidget(self.minAge,4,1)
        SAlayout.addWidget(self.wminAge,5,1)
        SAlayout.addWidget(self.wmaxAge,5,2)
        SAlayout.addWidget(self.exhibit,3,2)
        SAlayout.addWidget(self.exhibitDrop,3,3)
        SAlayout.addWidget(self.table,7,0,4,4)
        SAlayout.addWidget(self.search,2,4)

        self.search.clicked.connect(self.staff_search_animals_button)

        self.search_exhibits = QDialog()
        self.search_exhibits.setLayout(SAlayout)
        self.search_exhibits.show()

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
                addQuery.append("age < '{}'".format(self.maxAge))
                count += 1 
            except:
                errorstr += "- input for max age must be an integer\n"
                count2 += 1
        if len(self.wminAge.text()) > 0:
            try:
                int(self.wminAge.text())
                self.minAge = str(self.wminAge.text())
                addQuery.append("age > '{}'".format(self.minAge))
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

        headerNames = ["Name", "Species", "Exhibit", "Age", "Type"]
        self.model.setHorizontalHeaderLabels(headerNames)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()


    def staff_animal_care(self):

        #This block helps us get the information from the row that was clicked in the animal search page
        # row - signal.row()
        # column = signal.column()
        # cell_dict = self.model.item.Data(signal)
        # cell_value = cell_dict.get(0)

        a_name = str("Nemo")
        a_spec = str("Clownfish")
        a_age = str("1 month")
        e_name = str("Pacific")
        a_type = str("Fish")

        self.setWindowTitle('Animal Detail')
        SAlayout = QGridLayout()

        self.name = QLabel("Name: " + a_name)

        self.age = QLabel("Age: " + a_age)

        self.Species = QLabel("Species: " + a_spec)

        self.Type = QLabel("Type: " + a_type)

        self.exhibit = QLabel("Exhibit: " + e_name)


        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        headerNames = ["Staff Member", "Note","Time"]
        self.model.setHorizontalHeaderLabels(headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")

#exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])
        #print(exDrop)

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

        self.exhibitDrop.addItems(exDrop)
        self.table.setModel(self.model)

        SAlayout = QGridLayout()
        SAlayout.setColumnStretch(1,3)
        SAlayout.setRowStretch(1,2)
        SAlayout.addWidget(self.name, 2,0)
        SAlayout.addWidget(self.Species,3,0)
        SAlayout.addWidget(self.Type,5,3)
        SAlayout.addWidget(self.age, 5,0)
        SAlayout.addWidget(self.exhibit,3,2)
        SAlayout.addWidget(self.table,6,0,4,4)

        self.search_exhibits = QDialog()
        self.search_exhibits.setLayout(SAlayout)
        self.search_exhibits.show()


    def admin_view_shows(self):
        self.setWindowTitle('Shows')
        SSlayout = QGridLayout()

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
        self.exhibit = QLabel("Exhibit: ")
        self.exhibitDrop = QComboBox()
        self.RemoveShow = QPushButton("Remove Show")
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        headerNames = ["Name", "Exhibit", "Date"]
        self.model.setHorizontalHeaderLabels(headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")

    #exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])
        print(exDrop)

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
                #print(row)
            self.model.appendRow(row)

        self.exhibitDrop.addItems(exDrop)
        self.table.setModel(self.model)

        SSlayout = QGridLayout()
        SSlayout.setColumnStretch(1,3)
        SSlayout.setRowStretch(1,3)
        SSlayout.addWidget(self.search,3,3)
        SSlayout.addWidget(self.name, 2,0)
        SSlayout.addWidget(self.wname,2,1)
        SSlayout.addWidget(self.date,2,2)
        SSlayout.addWidget(self.dateDrop,2,3)
        SSlayout.addWidget(self.exhibit,3,0)
        SSlayout.addWidget(self.exhibitDrop,3,1)
        SSlayout.addWidget(self.table,4,0,4,4)
        SSlayout.addWidget(self.RemoveShow,8,3)

        self.RemoveShow.clicked.connect(self.remove_show)
        self.search.clicked.connect(self.search_shows_button)

        self.search_exhibits = QDialog()
        self.search_exhibits.setLayout(SSlayout)
        self.search_exhibits.show()

    def remove_show(self):

        show = self.table.selectionModel().selectedIndexes()
        name = str(show[0].data())
        exhibit = str(show[1].data())
        time = str(show[2].data())
        print(name,time,exhibit)
        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("DELETE FROM SHOWS WHERE show_name = (%s) and datetime = (%s) and exhibit_name = (%s)", (name,time,exhibit))
        print("Removed",name,time,exhibit)

        for index in sorted(show):
            #print(index)
            self.model.removeRow(index.row())
            break
        self.table.setModel(self.model)
        print("Updated table")

    def admin_view_animals(self):
        self.setWindowTitle('Shows')
        SAlayout = QGridLayout()

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
        self.RemoveAnimal = QPushButton("Remove Animal")

        self.table = QTableView()

        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        headerNames = ["Name", "Species","Exhibit", "Age", "Type"]
        self.model.setHorizontalHeaderLabels(headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")

#exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])
        print(exDrop)

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
        SAlayout.addWidget(self.table,6,0,4,4)
        SAlayout.addWidget(self.RemoveAnimal,10,4)

        self.RemoveAnimal.clicked.connect(self.remove_animals)
        self.search.clicked.connect(self.search_animals_button) 
#found in line 1025, written after visitor_search_animals function
        self.search_exhibits = QDialog()
        self.search_exhibits.setLayout(SAlayout)
        self.search_exhibits.show()

    def remove_animals(self):
        animal = self.table.selectionModel().selectedIndexes()
        name = str(animal[0].data())
        species = str(animal[1].data())
        self.db = self.Connect()
        self.c = self.db.cursor()

        self.c.execute("DELETE FROM ANIMALS WHERE name = (%s) and species = (%s)", (name,species))
#deletes item selected
        for index in sorted(animal):
            self.model.removeRow(index.row())
            break 
        self.table.setModel(self.model)
        print("Updated table")

    def staff_view_shows(self):
        self.setWindowTitle('Shows')

        atlantaZoo = QLabel()
        atlantaZoo.setText("Atlanta Zoo")
        showHistory = QLabel()
        showHistory.setText("Staff - Show History")

        SSlayout = QGridLayout()
        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(3)
        headerNames = ["Name", "Time", "Exhibit"]
        self.model.setHorizontalHeaderLabels(headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT show_name, exhibit_name, datetime FROM SHOWS WHERE SHOWS.username=%s",(self.my_user[1]))
        result = self.c.fetchall()
        for i in result:
            row = []
            for j in i: #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
                print(row)
            self.model.appendRow(row)

        self.table.setModel(self.model)

        SSlayout = QGridLayout()
        SSlayout.setColumnStretch(1,3)
        SSlayout.setRowStretch(1,3)
        SSlayout.addWidget(atlantaZoo,0,0)
        SSlayout.addWidget(showHistory)
        SSlayout.addWidget(self.table,4,0,4,4)

        self.search_exhibits = QDialog()
        self.search_exhibits.setLayout(SSlayout)
        self.search_exhibits.show()


    def search_exhibits(self):
        self.setWindowTitle('Exhibits')
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
        #print(result)

        self.table = QTableView()
        self.model = QStandardItemModel()
        self.model.setColumnCount(4)
        headerNames = ["Exhibit Name", "Water", "Number of Animals", "Size"]
        self.model.setHorizontalHeaderLabels(headerNames)

        for i in result:
            row = []
            for j in i:  #converts item to list from tuple
                item = QStandardItem(str(j)) #has to be converted to string in order to work
                item.setEditable(False)
                row.append(item)
                #print(row)
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
        self.search_exhibits.show()

        self.search.clicked.connect(self.exhibitSearch)

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
            print("here")
        else:
            messagebox.showwarning("Error", printstr)
            #print(printstr)

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
        headerNames = ["Name", "Exhibit", "Date"]
        self.model.setHorizontalHeaderLabels(headerNames)

        self.db = self.Connect()
        self.c = self.db.cursor()
        self.c.execute("SELECT exhibit_name FROM EXHIBITS")

        #exhibit drop down menu contents
        result = self.c.fetchall()
        exDrop = [""]
        for i in result:
            exDrop.append(i[0])
        print(exDrop)

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
                #print(row)
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

    def try_again(self):
        self.login_button.clicked.connect(self.check_user)

    # check_user currently can only display the tuple from our database from which we query the row that matches the user and the password
    def check_user(self):
        user = str(self.user_line_edit.text())
        pswd = str(self.password_line_edit.text())

        self.db = self.Connect()
        self.c = self.db.cursor()

        # tuple for logged in user
        self.c.execute("SELECT * FROM USERS AS U WHERE U.username=%s AND U.password=%s",(user,pswd))
        self.my_user = self.c.fetchone()
        if (self.my_user == None):
            messagebox.showwarning("Error", "Username or password incorrect. \n Please try again.")
            self.try_again()

        elif (self.my_user[3] == 'visitor'):
            self.login_button.clicked.connect(self.close)
            self.visitor_functionality()
        elif (self.my_user[3] == 'admin'):
            self.login_button.clicked.connect(self.close)
            self.admin_functionality()
        elif (self.my_user[3] == 'staff'):
            self.login_button.clicked.connect(self.close)
            self.staff_functionality()

        else:
            messagebox.showwarning("Error", "Unrecognized account type.\nCheck database.")





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
            #print("Password needs to be more than 8 characters")
            printstr += "Password needs to be more than 8 characters\n"
            count += 1

        if self.confirmpswd != self.pswd:
            #print("Password must match Confirm Password")
            printstr += "Password must match Confirm Password\n"
            count+=1

        if "@" not in self.email or "." not in self.email:
            #print("Email must meet email format with @ and . symbols")
            printstr += "Email must meet email format with @ and . symbols\n"
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
            self.c.execute("INSERT INTO USERS VALUES (%s,%s,%s,%s)",(self.email,self.user,self.pswd,"visitor"))
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
            #print("Password needs to be more than 8 characters")
            printstr += "Password needs to be more than 8 characters\n"
            count += 1

        if self.confirmpswd != self.pswd:
            #print("Password must match Confirm Password")
            printstr += "Password must match Confirm Password\n"
            count+=1

        if "@" not in self.email or "." not in self.email:
            #print("Email must meet email format with @ and . symbols")
            printstr += "Email must meet email format with @ and . symbols\n"
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
        self.setWindowTitle('Atlanta Zoo')
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

#     def exhibitSearch(ds):
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
