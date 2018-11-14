# Visitors


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


# #fill dedfault table
#         self.c = self.db.cursor()
#         self.c.execute("SELECT exhibit_name, datetime, (SELECT COUNT()) FROM EXHIBITS")
#         result = self.c.fetchall()
#         for i in result:
#             row = []
# #converts item to list from tuple
#             for j in i:  
#                 item = QStandardItem(str(j)) 
# #has to be converted to string in order to work
#                 item.setEditable(False)
#                 row.append(item)
#             self.model.appendRow(row)

#         self.table.setModel(self.model)

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
    self.dateDrop = QComboBox() #this is wrong implementation
    
    self.exhibit_name = QLabel("Exhibit")
    self.exhibitDrop = QComboBox()

    self.table = QTableView()
    self.model = QStandardItemModel()
    self.model.setColumnCount(3)
    headerNames = ["Name", "Exhibit", "Date"]
    self.model.setHorizontalHeaderLabels(headerNames)

    self.db = self.Connect()
    self.c = self.db.cursor()
    self.c.execute("SELECT exhibit_name FROM EXHIBITS")


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

    SSlayout = QGridLayout()
    SSlayout.setColumnStretch(1,3)
    SSlayout.setRowStretch(1,3)
    SSlayout.addWidget(self.search,3,3)
    SSlayout.addWidget(self.name, 1,0)
    SSlayout.addWidget(self.wname,1,1)
    SSlayout.addWidget(self.date,2,0)
    SSlayout.addWidget(self.dateDrop,2,1)
    SSlayout.addWidget(self.exhibit_name,1,2)
    SSlayout.addWidget(self.exhibitDrop,1,3)
    SSlayout.addWidget(self.table,4,0,4,4)

    self.search_exhibits = QDialog()
    self.search_exhibits.setLayout(SSlayout)
    self.search_exhibits.show()







def visitor_search_shows(self):
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
    SAlayout.addWidget(self.title1,1,0)
    SAlayout.addWidget(self.title2, 1,2)
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

    self.search_exhibits = QDialog()
    self.search_exhibits.setLayout(SAlayout)
    self.search_exhibits.show()
