# Admin
def admin_functionality(self, my_user):
#buttons that appear on main page
    self.ViewVisitors = QPushButton("View Visitors")
    self.ViewShows = QPushButton("View Shows")
    self.ViewStaff = QPushButton("View Staff")
    self.AddShow = QPushButton("Add Show")
    self.ViewAnimals = QPushButton("View Animals")


    self.LogOut = QPushButton("Log Out")

#layout of page
    self.layout = QGridLayout()
    layout = self.layout
    layout.setColumnStretch(1,3)
    layout.setRowStretch(1,3)

#placement layout of page
    layout.addWidget(self.ViewVisitors,1,0)
    layout.addWidget(self.ViewStaff, 1,1)
    layout.addWidget(self.ViewShows,2,0)
    layout.addWidget(self.ViewAnimals, 2,1)
    layout.addWidget(self.AddShow,3,0)
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

def admin_view_shows(self):
    self.setWindowTitle('Shows')
    SSlayout = QGridLayout()

    self.search = QPushButton("Search")
    self.name = QLabel("Name: ")
    self.wname = QLineEdit()
    self.date = QLabel("Date: ")
    self.dateDrop = QComboBox() #this is wrong implementation
    self.exhibit = QLabel("Exhibit: ")
    self.exhibitDrop = QComboBox()
    self.RemoveShow = QPushButton("Remove Show")
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
    SSlayout.addWidget(self.search,3,3)
    SSlayout.addWidget(self.name, 2,0)
    SSlayout.addWidget(self.wname,2,1)
    SSlayout.addWidget(self.date,2,2)
    SSlayout.addWidget(self.dateDrop,2,3)
    SSlayout.addWidget(self.exhibit,3,0)
    SSlayout.addWidget(self.exhibitDrop,3,1)
    SSlayout.addWidget(self.table,4,0,4,4)
    SSlayout.addWidget(self.RemoveShow,8,3)

    self.search_exhibits = QDialog()
    self.search_exhibits.setLayout(SSlayout)
    self.search_exhibits.show()

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

    self.search_exhibits = QDialog()
    self.search_exhibits.setLayout(SAlayout)
    self.search_exhibits.show()
