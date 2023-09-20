import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QTabWidget, QWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtGui import QAction
import random

class LocationResults(QtWidgets.QWidget):

    locationClicked = QtCore.pyqtSignal(str, float)

    def __init__(self, matching_locations):
        super().__init__()
        self.setWindowTitle("Location Results")
        self.setGeometry(100, 100, 400, 300)

        self.list_widget = QtWidgets.QListWidget(self)
        self.list_widget.setGeometry(QtCore.QRect(50, 50, 300, 200))

        for location in matching_locations:
            item = QtWidgets.QListWidgetItem(location)
            self.list_widget.addItem(item)

        self.list_widget.itemClicked.connect(self.emitLocationClicked)

    def emitLocationClicked(self, item):
        location_name = item.text()
        location_index = UserInfo.locations.index(location_name)
        if location_index < len(UserInfo.distances):
            distance = UserInfo.distances[location_index]
            self.locationClicked.emit(location_name, distance)

class UserInfo(QtWidgets.QWidget):
    def __init__(self, username):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("User Information")
        self.resize(529, 342)
        
        #Name Display
        self.label_username = QtWidgets.QLabel(self)
        self.label_username.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_username.resize(300,50)
        self.label_username.move(100,20)
        self.label_username.setFont(QtGui.QFont("Arial", 16))
        self.label_username.setText(f"Welcome: {username}")
        self.label_username.setStyleSheet("color: white; font-weight: bold;")


        self.btn_search = QtWidgets.QPushButton("Search", self)
        self.btn_search.setGeometry(200, 150, 100, 40)
        self.btn_search.clicked.connect(self.search)
        self.btn_search.setStyleSheet("color: white; background-color: blue; font-weight: bold;")

        self.text_input = QtWidgets.QLineEdit(self)
        self.text_input.setGeometry(100, 100, 300, 30)
        self.text_input.setPlaceholderText("Enter destination")
        self.text_input.setStyleSheet("color: white;")

        #Login Button
        self.btn_logout = QtWidgets.QPushButton("Logout", self)
        self.btn_logout.resize(100,40)
        self.btn_logout.clicked.connect(self.logout)
        self.btn_logout.setStyleSheet("color: white;")
        self.btn_logout.setStyleSheet("background-color: white;")
        self.btn_logout.setStyleSheet("color: black; background-color: white; font-weight: bold; border: 2px solid red;")

        #StyleSheet

        self.setStyleSheet("background-color: black;")

        self.location_results = None
        self.open_tabs = []
        self.current_tab = None

    locations = ["Uberland Central Mall", "Grand Uber Mall", "Tim Hortons", "Starbucks", "Uber Cafe", "Uber Highschool", 
                 "Uber State University", "Uberland Insititute of Technology", "Uberland Park", "Uberland Zoo", "Uberland Airport", "Uberland Train Station",
                 "Uberland Bus Station", "Uberland City Hall", "Uberland Police Station", "Uberland Fire Station", "Uberland Hospital",
                 "Uberland Post Office", "Uber Public Library", "Uberland Museum", "Uberland Stadium", "Uberland Movie Theater",
                 "Uber Bowling Alley", "Uberland Arcade", "Uberland Gym", "Uber Swimming Pool", "Uber Golf Course", "Uber Recreational Centre", 
                 "Cactus Club Restaurant", "Uber Bay Beach", "Uber Gas Station", "Uber Car Wash", "Uber Elementary School", "Uber Middle School", 
                 "Uber Supermarket", "Uberland Pharmacy", "Uber Central Bank", "Grand Uber Hotel"]
    
    distances = [3.2,5.1,13.1,14.0,2.2,3.0,7.3,8.9,4.5,10.6,11.2,1.1,1.5,2.7,4.2,5.3,6.5,7.7,6.4,9.2,5.7,22.5,16.6,14.6,19.2,8.7,2.9,1.9,4.5,16.3,21.1,23.0,25.6,11.2,7.0,9.9,32.1,5.2,9.0,13.7]
    traffic = ["Heavy", "Medium", "Light"]
    
    def calculate_ride_cost(self, distance):
        flat_fee = 5.0
        per_increment_cost = 0.197
        increment_size = 0.1

        #Calculate the number of 0.1 increments in the given distance
        increments = distance / increment_size

        # Calculate the cost based on the flat fee and per increment cost
        total_cost = flat_fee + increments * per_increment_cost

        return total_cost


    def search(self):
        search_text = self.text_input.text()
        matching_locations = [location for location in self.locations if search_text.lower() in location.lower()]
        if matching_locations:
            self.location_results = LocationResults(matching_locations)
            self.location_results.locationClicked.connect(self.openNewTab)
            self.location_results.show()
        else:
            QtWidgets.QMessageBox.information(self, "No Matches", "No matching locations found.")
        print("Searching for:", search_text)


    def openNewTab(self, location_name, distance):
        # Create and open a new tab with the selected location
        traffic_level = random.choice(self.traffic)
        if self.current_tab:
            self.current_tab.close()
        
        if self.location_results:
            new_tab = QtWidgets.QWidget()
            new_tab.setWindowTitle(location_name)
            self.current_tab = new_tab
            location_index = self.locations.index(location_name)
            if location_index < len(self.distances):
                distance_km = self.distances[location_index]
                cost = self.calculate_ride_cost(distance)

                layout = QVBoxLayout(new_tab)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

                table_widget = QtWidgets.QTableWidget(3, 2, new_tab)
                table_widget.setHorizontalHeaderLabels(["Description", "Value"])
                table_widget.setRowHeight(2, 20)

                table_widget.setItem(0, 0, QtWidgets.QTableWidgetItem("Distance (KM)"))
                table_widget.setItem(0, 1, QtWidgets.QTableWidgetItem(f"{distance_km:.2f}"))
                table_widget.setItem(1, 0, QtWidgets.QTableWidgetItem("Cost ($)"))
                table_widget.setItem(1, 1, QtWidgets.QTableWidgetItem(f"${cost:.2f}"))
                table_widget.setItem(2, 0, QtWidgets.QTableWidgetItem("Traffic Level"))
                table_widget.setItem(2, 1, QtWidgets.QTableWidgetItem(traffic_level))
                

                table_widget.setStyleSheet("QTableWidget { background-color: white; }")
                table_widget.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: lightblue; }")
                table_widget.verticalHeader().setStyleSheet("QHeaderView::section { background-color: lightblue; }")
                

                table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                layout.addWidget(table_widget)
                new_tab.setStyleSheet("background-color: lightgray;")
                table_widget.setStyleSheet("QTableWidget { background-color: white; }")

            # Add any widgets or content you want for the new tab here
            new_tab.show()
            self.open_tabs.append(new_tab)

    def logout(self):
        self.close()

class Ui_Outsecure(object):
    """
    LOGIN PAGE
    """
    def setupUi(self, Outsecure):


        Outsecure.setObjectName("Outsecure")
        Outsecure.resize(529, 342)
        Outsecure.setMouseTracking(True)
        Outsecure.setStyleSheet("background-color: rgb(8, 8, 8);")
        self.line = QtWidgets.QFrame(Outsecure)
        self.line.setGeometry(QtCore.QRect(10, 80, 591, 20))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.l_title = QtWidgets.QLabel(Outsecure)
        self.l_title.setGeometry(QtCore.QRect(170, 20, 231, 41))
        self.l_title.setStyleSheet("color: rgb(242, 247, 247);\n"
                                   "font: 30pt \".SF NS Text\";")
        self.l_title.setObjectName("l_title")
        self.btn_Submit = QtWidgets.QPushButton(Outsecure)
        self.btn_Submit.setGeometry(QtCore.QRect(180, 200, 161, 31))
        self.btn_Submit.setStyleSheet("color: rgb(250, 255, 255);\n"
                                      "background-color: rgb(73, 199, 41);\n"
                                      "border-style:outset;\n"
                                      "border-radius:10px;\n"
                                      "font: 14pt \"Arial\";")
        self.btn_Submit.setObjectName("btn_Submit")
        self.btn_newuser = QtWidgets.QPushButton(Outsecure)
        self.btn_newuser.setGeometry(QtCore.QRect(180, 240, 161, 31))
        self.btn_newuser.setStyleSheet("color: rgb(250, 255, 255);\n"
                                       "background-color: rgb(73, 199, 41);\n"
                                       "border-style:outset;\n"
                                       "border-radius:10px;\n"
                                       "font: 14pt \"Arial\";")
        self.btn_newuser.setObjectName("btn_newuser")
        self.l_copyright = QtWidgets.QLabel(Outsecure)
        self.l_copyright.setGeometry(QtCore.QRect(150, 310, 261, 21))
        self.l_copyright.setStyleSheet("color: rgb(252, 0, 28);")
        self.l_copyright.setObjectName("l_copyright")
        self.txt_username = QtWidgets.QLineEdit(Outsecure)
        self.txt_username.setGeometry(QtCore.QRect(130, 100, 275, 31))
        self.txt_username.setStyleSheet("background-color: rgb(207, 211, 211);\n"
                                        "border-style:outset;\n"
                                        "border-radius:10px;\n"
                                        "font: 14pt \"Arial\";")
        self.txt_username.setObjectName("txt_username")
        self.txt_password = QtWidgets.QLineEdit(Outsecure)
        self.txt_password.setGeometry(QtCore.QRect(130, 150, 271, 31))
        self.txt_password.setStyleSheet("background-color: rgb(207, 211, 211);\n"
                                        "border-style:outset;\n"
                                        "border-radius:10px;\n"
                                        "font: 14pt \"Arial\";")
        self.txt_password.setObjectName("txt_password")

        self.retranslateUi(Outsecure)
        QtCore.QMetaObject.connectSlotsByName(Outsecure)

         # Create a QLabel for the image

        image_path = "UberHackathon/images/hero-image1.jpg"
        self.image_label = QtWidgets.QLabel(Outsecure)
        self.image_label.setGeometry(QtCore.QRect(0, 0, 100, 75)) 
        pixmap = QtGui.QPixmap(image_path)  
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def retranslateUi(self, Outsecure):
        _translate = QtCore.QCoreApplication.translate
        Outsecure.setWindowTitle(_translate("Outsecure", "Form"))
        self.l_title.setText(_translate("Outsecure", "Login Page"))
        self.btn_Submit.setText(_translate("Outsecure", "Submit"))
        self.btn_newuser.setText(_translate("Outsecure", "New User"))
        self.txt_username.setPlaceholderText(_translate("Outsecure", "Enter UserName"))
        self.txt_password.setPlaceholderText(_translate("Outsecure", "Enter Password"))

class Ui_NewUser(object):
    """
    NEW USERS
    """
    def setupUi(self, NewUser):
        NewUser.setObjectName("NewUser")
        NewUser.resize(555, 372)
        NewUser.setStyleSheet("background-color: rgb(14, 14, 14);")
        self.l_newuser = QtWidgets.QLabel(NewUser)
        self.l_newuser.setGeometry(QtCore.QRect(180, 10, 181, 31))
        self.l_newuser.setStyleSheet("font: 24pt \".SF NS Text\";\n"
                                     "color: rgb(234, 239, 238);\n"
                                     "")
        self.l_newuser.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.l_newuser.setObjectName("l_newuser")
        self.line = QtWidgets.QFrame(NewUser)
        self.line.setGeometry(QtCore.QRect(10, 50, 591, 20))
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.txt_firstname = QtWidgets.QLineEdit(NewUser)
        self.txt_firstname.setEnabled(True)
        self.txt_firstname.setGeometry(QtCore.QRect(30, 80, 230, 41))
        self.txt_firstname.setStyleSheet("background-color: rgb(207, 211, 211);\n"
                                         "border-style:outset;\n"
                                         "border-radius:10px;\n"
                                         "font: 14pt \"Arial\";")
        self.txt_firstname.setText("")
        self.txt_firstname.setObjectName("txt_firstname")
        self.txt_lastname = QtWidgets.QLineEdit(NewUser)
        self.txt_lastname.setGeometry(QtCore.QRect(290, 80, 229, 41))
        self.txt_lastname.setStyleSheet("background-color: rgb(207, 211, 211);\n"
                                        "border-style:outset;\n"
                                        "border-radius:10px;\n"
                                        "font: 14pt \"Arial\";")
        self.txt_lastname.setObjectName("txt_lastname")
        self.txt_phone = QtWidgets.QLineEdit(NewUser)
        self.txt_phone.setGeometry(QtCore.QRect(30, 140, 230, 41))
        self.txt_phone.setStyleSheet("background-color: rgb(207, 211, 211);\n"
                                     "border-style:outset;\n"
                                     "border-radius:10px;\n"
                                     "font: 14pt \"Arial\";")
        self.txt_phone.setObjectName("txt_phone")
        self.txt_email = QtWidgets.QLineEdit(NewUser)
        self.txt_email.setGeometry(QtCore.QRect(290, 140, 229, 41))
        self.txt_email.setStyleSheet("background-color: rgb(207, 211, 211);\n"
                                     "border-style:outset;\n"
                                     "border-radius:10px;\n"
                                     "font: 14pt \"Arial\";")
        self.txt_email.setObjectName("txt_email")
        self.txt_username = QtWidgets.QLineEdit(NewUser)
        self.txt_username.setGeometry(QtCore.QRect(30, 200, 230, 41))
        self.txt_username.setStyleSheet("background-color: rgb(207, 211, 211);\n"
                                        "border-style:outset;\n"
                                        "border-radius:10px;\n"
                                        "font: 14pt \"Arial\";")
        self.txt_username.setObjectName("txt_username")
        self.lineEdit = QtWidgets.QLineEdit(NewUser)
        self.lineEdit.setGeometry(QtCore.QRect(290, 200, 231, 41))
        self.lineEdit.setStyleSheet("background-color: rgb(207, 211, 211);\n"
                                    "border-style:outset;\n"
                                    "border-radius:10px;\n"
                                    "font: 14pt \"Arial\";")
        self.lineEdit.setObjectName("lineEdit")
        self.btn_submit = QtWidgets.QPushButton(NewUser)
        self.btn_submit.setGeometry(QtCore.QRect(190, 270, 159, 31))
        self.btn_submit.setStyleSheet("color: rgb(250, 255, 255);\n"
                                      "background-color: rgb(73, 199, 41);\n"
                                      "border-style:outset;\n"
                                      "border-radius:10px;\n"
                                      "font: 14pt \"Arial\";")
        self.btn_submit.setObjectName("btn_submit")
        self.Back = QtWidgets.QPushButton(NewUser)
        self.Back.setGeometry(QtCore.QRect(190, 320, 159, 31))
        self.Back.setStyleSheet("color: rgb(250, 255, 255);\n"
                                "background-color: rgb(73, 199, 41);\n"
                                "border-style:outset;\n"
                                "border-radius:10px;\n"
                                "font: 14pt \"Arial\";")
        self.Back.setObjectName("Back")

        self.retranslateUi(NewUser)
        QtCore.QMetaObject.connectSlotsByName(NewUser)

    def retranslateUi(self, NewUser):
        _translate = QtCore.QCoreApplication.translate
        NewUser.setWindowTitle(_translate("NewUser", "Form"))
        self.l_newuser.setText(_translate("NewUser", "New User"))
        self.txt_firstname.setPlaceholderText(_translate("NewUser", "Enter your First Name"))
        self.txt_lastname.setPlaceholderText(_translate("NewUser", "Enter your Last Name"))
        self.txt_phone.setPlaceholderText(_translate("NewUser", "Enter your Phone Number "))
        self.txt_email.setPlaceholderText(_translate("NewUser", "Enter your Email Address "))
        self.txt_username.setPlaceholderText(_translate("NewUser", "Enter Username"))
        self.lineEdit.setPlaceholderText(_translate("NewUser", "Enter Password"))
        self.btn_submit.setText(_translate("NewUser", "Submit"))
        self.Back.setText(_translate("NewUser", "Back"))

# ----------------------------------------------


class Login(QtWidgets.QWidget,Ui_Outsecure):
    switch_window = QtCore.pyqtSignal()
    switch_window1 = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)

        self.btn_newuser.clicked.connect(self.btn_newuser_handler)
        self.btn_Submit.clicked.connect(self.btn_submit_handler)

    def pop_message(self,text=""):
        msg = QtWidgets.QMessageBox()
        msg.setText("{}".format(text))
        msg.exec()

    def bool_check_username(self):
        if len(self.txt_password.text()) <= 1:
            self.pop_message(text='Enter Valid Username and Password !')
        else:
            username = self.txt_username.text()
            password = self.txt_password.text()
            conn = sqlite3.connect('Data.db')
            cursor = conn.cursor()
            cursor.execute("SELECT username,password FROM credentials")
            val = cursor.fetchall()
            if len(val) >= 1:

                for x in val:
                    if username in x[0] and password in x[1]:
                        return True
                    else:
                        pass
            else:
                self.pop_message(text="No users Found ")
                return False

    def btn_submit_handler(self):
        val = self.bool_check_username()

        if (val):
            username = self.txt_username.text()
            self.user_info = UserInfo(username)
            self.user_info.show()
            self.close()

        else:
            self.pop_message("Invalid username or password ")

    def btn_newuser_handler(self):
        self.switch_window.emit()

class Newuser(QtWidgets.QWidget, Ui_NewUser):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.Back.clicked.connect(self.back_handler)
        self.btn_submit.clicked.connect(self.btn_submit_handler)

    def pop_message(self,text=""):
        msg = QtWidgets.QMessageBox()
        msg.setText("{}".format(text))
        msg.exec()


    def btn_submit_handler(self):
        self.create_db_newuser()

    def back_handler(self):
        self.close()
        self.switch_window.emit()

    def create_db_newuser(self):

        txt_firstname_v = self.txt_firstname.text()
        txt_lastname_v = self.txt_lastname.text()
        txt_phone_v = self.txt_phone.text()
        txt_emailid_v = self.txt_email.text()
        txt_username_v =self.txt_username.text()
        txt_password_v =self.lineEdit.text()

        if (len(txt_firstname_v) <= 1
                and len(txt_lastname_v) <= 1 and
        len(txt_phone_v) <= 9  and
        len(txt_emailid_v) <= 1  and
        len(txt_username_v) <= 1  and
        len(txt_password_v) <=1):

            """
            Logic to see if users Enter all Feilds Correctly 
            """
            self.pop_message(text = "Please Enter All Feilds ")

        else:

            conn=sqlite3.connect('Data.db')
            cursor = conn.cursor()

            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS credentials 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    fname TEXT, 
                    lname TEXT, 
                    Phone TEXT, 
                    email TEXT,
                    username TEXT, 
                    password TEXT)""")

            cursor.execute(""" INSERT INTO credentials 
                    (fname,
                    lname,
                    Phone,
                    email,
                    username, 
                    password)
                    
                VALUES 
                (?,?,?,?,?,?)
                """,(txt_firstname_v, txt_lastname_v, txt_phone_v, txt_emailid_v,txt_username_v,txt_password_v))

            conn.commit()
            cursor.close()
            conn.close()
            self.pop_message(text="Added to Database ! ")


class Controller:

    def __init__(self):
        pass

    def show_login_page(self):
        self.login = Login()
        self.login.switch_window.connect(self.show_newuser_page)
        self.login.show()

    def show_newuser_page(self):
        self.newuser = Newuser()
        self.newuser.switch_window.connect(self.show_login_page)
        self.login.close()
        self.newuser.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_login_page()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()