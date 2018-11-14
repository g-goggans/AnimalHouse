# Visitors

def visitor_functionality(self, my_user):
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
    self.SearchExhibits.clicked.connect(self.search_exhibits)
    self.SearchShows.clicked.connect(self.search_shows)
    # self.SearchAnimals.clicked.connect(self.search_animals)

    self.newWindow = TableWindow()
    self.newWindow.setLayout(layout)
    self.newWindow.show()
    self.LogOut.clicked.connect(self.newWindow.close)
    self.LogOut.clicked.connect(self.close)
    layout.addWidget(self.LogOut)

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
