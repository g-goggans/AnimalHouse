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
