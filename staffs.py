# Staff
def staff_functionality(self, my_user):

#buttons that appear on main page
    self.SearchExhibits = QPushButton("Seach Exhibits")
    self.SearchShows = QPushButton("Seach Shows")
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
    layout.addWidget(self.SearchShows,2,0)
    layout.addWidget(self.ViewShow, 2,1)
    layout.addWidget(self.SearchAnimals,3,0)
    layout.addWidget(self.LogOut, 3,1)

# #button connections
#         self.SearchExhibits.clicked.connect(self.search_exhibits)
#         self.SearchShows.clicked.connect(self.search_shows)
#         self.SearchAnimals.clicked.connect(self.search_animals)

    self.newWindow = TableWindow()
    self.newWindow.setLayout(layout)
    self.newWindow.show()
    self.LogOut.clicked.connect(self.newWindow.close)
    self.LogOut.clicked.connect(self.close)
    layout.addWidget(self.LogOut)






def staff_search_animals(self):
    self.setWindowTitle('Animals')
    SAlayout = QGridLayout()


    self.name = QLabel("Name: ")
    self.wname = QLineEdit()
    self.wname = QLineEdit()
    
    self.age = QLabel("Age: ")
    self.minAge = QLabel("min")
    self.wminAge = QLineEdit()
    self.maxAge = QLabel("max")
    self.wmaxAge = QLineEdit()
    
    self.Species = QLabel("Species: ")
    self.wSpecies = QLineEdit()

    self.Type = QLabel("Type: ")
    self.typeDrop = QComboBox()

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
    print(exDrop)

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
