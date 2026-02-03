import sys
from PyQt6.QtCore import Qt, QRegularExpression
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QStackedLayout
from clinic.gui.appointment_gui import AppointmentGUI
from clinic.controller import Controller

class GetPHNGUI(QWidget):
    def __init__(self, controller, stackedLayout, mainWindow):
        super().__init__()
        self.controller = controller
        self.stackedLayout = stackedLayout
        self.mainWindow = mainWindow
        
    def getPHNScreen(self):
        getPHNScreenWidget = QWidget()
        getPHNScreenLayout = QVBoxLayout()

        buttonOptionLayout = QHBoxLayout()
        
        patientLabel = QLabel("")
        patientLabel.hide()
        searchPatientLabel = QLabel("Please enter the PHN of the patient you want to book an appointment with.")
        searchPatientLabel.setAlignment(Qt.AlignmentFlag.AlignCenter) 
 
        PHNInput = QLineEdit(self)
        PHNInput.setPlaceholderText("PHN")

        backButton = QPushButton("Back")
        backButton.clicked.connect(lambda: self.backButtonClick(PHNInput, getPHNScreenLayout, patientLabel))

        enterButton = QPushButton("Enter")
        enterButton.clicked.connect(lambda: self.enterButtonClick(PHNInput, getPHNScreenLayout, patientLabel))

        buttonOptionLayout.addWidget(backButton)
        buttonOptionLayout.addWidget(enterButton)

        getPHNScreenLayout.addWidget(searchPatientLabel)
        getPHNScreenLayout.addWidget(PHNInput)
        getPHNScreenLayout.addLayout(buttonOptionLayout)
        getPHNScreenLayout.addWidget(patientLabel)

        getPHNScreenWidget.setLayout(getPHNScreenLayout)
        return getPHNScreenWidget
    
    # Goes back to the main menu
    def backButtonClick(self, PHNInput, searchPatientScreenLayout, patientLabel):
        PHNInput.clear()
        patientLabel.setText("")
        patientLabel.hide()
        self.stackedLayout.setCurrentIndex(2)

    # Checks the current PHN box input to see if the user exists
    def enterButtonClick(self, PHNInput, searchPatientScreenLayout, patientLabel):
        PHN = PHNInput.text().strip()
        if not PHN:
            QMessageBox.warning(self, "Invalid Input", "Please enter a PHN.")
            return

        patient = self.controller.search_patient(int(PHN))

        if patient is None:
            QMessageBox.warning(self, "Invalid PHN", "No patient with this PHN exists")
        else:
            patientString = f"\n\nPHN: {patient.phn}\nName: {patient.name}\nBirth Date: {patient.birth_date}\nPhone Number: {patient.phone}\nEmail: {patient.email}\nAddress: {patient.address}"

            # Confirm with user if the system found the correct patient
            found = QMessageBox.question(self, "Confirm", "Is this the patient you want to book an appointment with?" + patientString)

            if found == QMessageBox.StandardButton.Yes:                
                # Set current_patient to the PHN
                self.controller.set_current_patient(int(PHN))
                self.mainWindow.setWindowTitle("MEDICAL CLINIC SYSTEM - APPOINTMENT MENU")
                self.stackedLayout.setCurrentIndex(10)
            else:
                found.close()

        PHNInput.clear()
