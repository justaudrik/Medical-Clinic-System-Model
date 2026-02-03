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

class SearchPatientGUI(QWidget):

    def __init__(self, controller, stackedLayout):
        super().__init__()
        self.controller = controller
        self.stackedLayout = stackedLayout

    def searchPatientScreen(self):
        searchPatientScreenWidget = QWidget()
        searchPatientScreenLayout = QVBoxLayout()

        buttonOptionLayout = QHBoxLayout()
        
        patientTable = QTableView()
        patientModel = QStandardItemModel()
        patientTable.hide()
        searchPatientLabel = QLabel("Please enter the PHN of the patient you want to search for.")
        searchPatientLabel.setAlignment(Qt.AlignmentFlag.AlignCenter) 
 
        PHNInput = QLineEdit(self)
        PHNInput.setPlaceholderText("PHN")

        backButton = QPushButton("Back")
        backButton.clicked.connect(lambda: self.backButtonClick(PHNInput, searchPatientScreenLayout, patientTable, patientModel))

        enterButton = QPushButton("Enter")
        enterButton.clicked.connect(lambda: self.enterButtonClick(PHNInput, searchPatientScreenLayout, patientTable, patientModel))

        buttonOptionLayout.addWidget(backButton)
        buttonOptionLayout.addWidget(enterButton)

        searchPatientScreenLayout.addWidget(searchPatientLabel)
        searchPatientScreenLayout.addWidget(patientTable)
        searchPatientScreenLayout.addWidget(PHNInput)
        searchPatientScreenLayout.addLayout(buttonOptionLayout)

        searchPatientScreenWidget.setLayout(searchPatientScreenLayout)
        return searchPatientScreenWidget
    
    # Goes back to the main menu
    def backButtonClick(self, PHNInput, searchPatientScreenLayout, patientTable, patientModel):
        PHNInput.clear()
        patientModel.clear()
        patientTable.hide()
        self.stackedLayout.setCurrentIndex(2)

    # Checks to see if the inputted PHN exists
    def enterButtonClick(self, PHNInput, searchPatientScreenLayout, patientTable, patientModel):
        PHN = PHNInput.text().strip()
        if not PHN:
            QMessageBox.warning(self, "Invalid Input", "Please enter a PHN.")
            return

        patient = self.controller.search_patient(int(PHN))

        if patient is None:
            QMessageBox.warning(self, "Invalid PHN", "No patient with this PHN exists")
        else:
            # If a patient is found shows the table and loads the patients info into it
            patientTable.show()
            patientInfo = [str(patient.phn), patient.name, patient.birth_date, patient.phone, patient.email, patient.address]
            patientModel.clear()
            patientModel.setHorizontalHeaderLabels(["PHN", "Name", "Birthday", "Phone", "Email", "Address"])
            items = [QStandardItem(field) for field in patientInfo]

            # Make info uneditable to user
            for item in items:
                item.setEditable(False)

            patientModel.appendRow(items)
            patientTable.setModel(patientModel)
            patientTable.resizeColumnsToContents()
        PHNInput.clear()
