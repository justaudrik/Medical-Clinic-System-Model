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

class ListPatientsGUI(QWidget):

    def __init__(self, controller, stackedLayout):
        super().__init__()
        self.controller = controller
        self.stackedLayout = stackedLayout
        self.patientTable = QTableView()
        self.patientModel = QStandardItemModel()
        self.noPatientLabel = QLabel("No patients found")
        self.noPatientLabel.hide()

    def listPatientsScreen(self):
        listPatientsScreenWidget = QWidget()
        listPatientsScreenLayout = QVBoxLayout()

        backButton = QPushButton("Back")
        backButton.clicked.connect(self.backButtonClick)

        listPatientsScreenLayout.addWidget(self.patientTable)
        listPatientsScreenLayout.addWidget(self.noPatientLabel)
        listPatientsScreenLayout.addWidget(backButton)

        listPatientsScreenWidget.setLayout(listPatientsScreenLayout)
        return listPatientsScreenWidget
    
    # Unique update function to ensure that the list of patients always remains up to dat
    # This is called everytime the screen is loaded
    def updatePatientTable(self):
        patients = self.controller.list_patients()
        patientInfoList = []
        if patients:
            self.patientTable.show()
            self.noPatientLabel.hide()
            for patient in patients:
                patientInfo = [str(patient.phn), patient.name, patient.birth_date, patient.phone, patient.email, patient.address]
                patientInfoList.append(patientInfo)
            self.patientModel.clear()
            self.patientModel.setHorizontalHeaderLabels(["PHN", "Name", "Birthday", "Phone", "Email", "Address"])
            for row in patientInfoList:
                items = [QStandardItem(field) for field in row]

                # Make info uneditable to user
                for item in items:
                    item.setEditable(False)

                self.patientModel.appendRow(items)
            self.patientTable.setModel(self.patientModel)
            self.patientTable.resizeColumnsToContents()
        else:
            self.patientTable.hide()
            self.noPatientLabel.show()
            self.noPatientLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Goes back to the main menu
    def backButtonClick(self):
        self.stackedLayout.setCurrentIndex(2)
