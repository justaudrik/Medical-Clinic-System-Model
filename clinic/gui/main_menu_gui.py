import sys
from PyQt6.QtCore import Qt, QRegularExpression
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QStackedLayout
from clinic.controller import Controller
from clinic.gui.main_menu_elements.list_patients_gui import ListPatientsGUI
from clinic.gui.appointment_gui import AppointmentGUI

class MainMenuGUI(QWidget):
    def __init__(self, controller, stackedLayout, listPatientsGUI):
        super().__init__()
        self.controller = controller
        self.stackedLayout = stackedLayout # Importing the stackedLayout to navigate through main menu screens
        self.listPatientsGUI = listPatientsGUI # Importing list patients to deal with the way the screen is updated (refer to list_patients_gui.py in main_menu_elements)

    def mainMenu(self):
        mainMenuWidget = QWidget()
        mainMenuLayout = QVBoxLayout()

        subMainMenuWidget = QWidget()
        subMainMenuLayout = QGridLayout()

        addNewButton = QPushButton("Add a new patient")
        addNewButton.setCheckable(True)
        addNewButton.clicked.connect(self.addNewButtonClick)
       
        searchPatientButton = QPushButton("Search patient by PHN")
        searchPatientButton.clicked.connect(self.searchPatientButtonClick)

        retrievePatientsButton = QPushButton("Retrieve patients by name")
        retrievePatientsButton.clicked.connect(self.retrievePatientsButtonClick)

        changePatientButton = QPushButton("Update patient data")
        changePatientButton.clicked.connect(self.updatePatientButtonClick)

        removePatientButton = QPushButton("Remove patient")
        removePatientButton.clicked.connect(self.removePatientButtonClick)

        listAllButton = QPushButton("List all patients")
        listAllButton.clicked.connect(self.listPatientsButtonClick)
        
        startAppointmentButton = QPushButton("Start appointment with patient")
        startAppointmentButton.clicked.connect(self.startAppointmentButtonClick)

        logOutButton = QPushButton("Logout")
        logOutButton.clicked.connect(self.logOutButtonClick)
   
        mainMenuLayout.addWidget(startAppointmentButton)
  
        # Adding all of the option buttons to a grid in the main menu
        subMainMenuLayout.addWidget(addNewButton, 0, 1)
        subMainMenuLayout.addWidget(searchPatientButton, 0, 2)
        subMainMenuLayout.addWidget(retrievePatientsButton, 1, 1)
        subMainMenuLayout.addWidget(changePatientButton, 1, 2)
        subMainMenuLayout.addWidget(removePatientButton, 2, 1)
        subMainMenuLayout.addWidget(listAllButton, 2, 2)
  
        mainMenuLayout.addLayout(subMainMenuLayout)

        mainMenuLayout.addWidget(logOutButton)

        mainMenuWidget.setLayout(mainMenuLayout)
        return mainMenuWidget

    # All of these functions navigate to their respective screens for the button in the stackedLayout
    def logOutButtonClick(self):
        self.controller.logout()
        self.stackedLayout.setCurrentIndex(0)
       
    def addNewButtonClick(self):
        self.stackedLayout.setCurrentIndex(3)

    def searchPatientButtonClick(self):
        self.stackedLayout.setCurrentIndex(4)

    def removePatientButtonClick(self):
        self.stackedLayout.setCurrentIndex(5)
  
    def retrievePatientsButtonClick(self):
        self.stackedLayout.setCurrentIndex(6)

    def listPatientsButtonClick(self):
        # Sets the list patient table to update upon entry
        self.listPatientsGUI.updatePatientTable()

        self.stackedLayout.setCurrentIndex(7)

    def updatePatientButtonClick(self):
        self.stackedLayout.setCurrentIndex(8)

    def startAppointmentButtonClick(self):
        self.stackedLayout.setCurrentIndex(9)
