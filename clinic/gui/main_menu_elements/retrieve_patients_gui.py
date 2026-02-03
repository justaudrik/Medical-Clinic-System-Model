import sys
from PyQt6.QtCore import Qt, QRegularExpression
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableView
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QStackedLayout
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from clinic.controller import Controller

class RetrievePatientsGUI (QWidget):

    def __init__(self, controller, stackedLayout):
        super().__init__()
        self.controller = controller
        self.stackedLayout = stackedLayout
        self.patientTable = QTableView()
        self.patientModel = QStandardItemModel()

    def retrievePatientsScreen(self):
        retrievePatientsScreenWidget = QWidget()
        retrievePatientsScreenLayout = QVBoxLayout()

        buttonOptionLayout = QHBoxLayout()

        retrievePatientsLabel = QLabel("Please enter the name of the patient you want to search for.")
        retrievePatientsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter) 
 
        nameInput = QLineEdit(self)
        nameInput.setPlaceholderText("Patient name")

        backButton = QPushButton("Back")
        backButton.clicked.connect(lambda: self.backButtonClick(nameInput, retrievePatientsScreenLayout))

        enterButton = QPushButton("Enter")
        enterButton.clicked.connect(lambda: self.enterButtonClick(nameInput, retrievePatientsScreenLayout))

        buttonOptionLayout.addWidget(backButton)
        buttonOptionLayout.addWidget(enterButton)

        retrievePatientsScreenLayout.addWidget(retrievePatientsLabel)
        retrievePatientsScreenLayout.addWidget(self.patientTable)
        retrievePatientsScreenLayout.addWidget(nameInput)
        retrievePatientsScreenLayout.addLayout(buttonOptionLayout)

        retrievePatientsScreenWidget.setLayout(retrievePatientsScreenLayout)
        return retrievePatientsScreenWidget
    
    # Goes back to the main menu
    def backButtonClick(self, nameInput, retirevePatientsScreenLayout):
        nameInput.clear()
        self.patientModel.clear()
        self.stackedLayout.setCurrentIndex(2)
        
    # Checks to see if the current name matches any users in the system, and displays them if so
    def enterButtonClick(self, nameInput, retrievePatientsScreenLayout):
        name = nameInput.text().strip()
        if not name:
            QMessageBox.warning(self, "Invalid Input", "Please enter a name.")
            return

        patients = self.controller.retrieve_patients(name)

        if not patients:
            QMessageBox.warning(self, "Invalid Name", "No patients with this name exist.")
        else:
            # Clear the table before inserting new data
            self.patientModel.clear()
            self.patientTable.setModel(self.patientModel)

            # Setting up the data for each column, and adding every patients data into it
            self.patientModel.setHorizontalHeaderLabels(["PHN", "Name", "Birthday", "Phone", "Email", "Address"])
            patientInfoList = []
            for patient in patients:
                patientInfo = [str(patient.phn), patient.name, patient.birth_date, patient.phone, patient.email, patient.address]
                patientInfoList.append(patientInfo)
            
            for row in patientInfoList:
                items = [QStandardItem(field) for field in row]

                # Make table contents uneditable for user
                for item in items:
                    item.setEditable(False)
                self.patientModel.appendRow(items)

            self.patientTable.setModel(self.patientModel)
            self.patientTable.resizeColumnsToContents()
        nameInput.clear()

