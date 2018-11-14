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
