import sys
from PyQt6.QtCore import Qt, QRegularExpression
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QStackedLayout
from clinic.controller import Controller

class DeletePatientGUI(QWidget):

    def __init__(self, controller, stackedLayout):
        super().__init__()
        self.controller = controller
        self.stackedLayout = stackedLayout

    def deletePatientScreen(self):
        deletePatientScreenWidget = QWidget()
        deletePatientScreenLayout = QVBoxLayout()

        buttonOptionLayout = QHBoxLayout()

        deletePatientLabel = QLabel("Please enter the PHN of the patient you want to delete.") 
        deletePatientLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        PHNInput = QLineEdit(self)
        PHNInput.setPlaceholderText("PHN")

        backButton = QPushButton("Back")
        backButton.clicked.connect(lambda: self.backButtonClick(PHNInput))

        enterButton = QPushButton("Enter")
        enterButton.clicked.connect(lambda: self.enterButtonClick(PHNInput))

        buttonOptionLayout.addWidget(backButton)
        buttonOptionLayout.addWidget(enterButton)

        deletePatientScreenLayout.addWidget(deletePatientLabel)
        deletePatientScreenLayout.addWidget(PHNInput)
        deletePatientScreenLayout.addLayout(buttonOptionLayout)

        deletePatientScreenWidget.setLayout(deletePatientScreenLayout)
        return deletePatientScreenWidget
    
    # Goes back to the main menu
    def backButtonClick(self, PHNInput):
        PHNInput.clear()
        self.stackedLayout.setCurrentIndex(2)

    # Checks if the currently inputted PHN is a valid user
    def enterButtonClick(self, PHNInput):
        PHN = PHNInput.text()
        if not PHN:
            QMessageBox.warning(self, "Invalid Input", "Please enter a PHN.")
            return

        patient = self.controller.search_patient(int(PHN))

        if patient is None:
            QMessageBox.warning(self, "Invalid PHN", "No patient exists with this PHN.")
        else:
            # Confirm with the user if they want to delete the found patient
            patientString = f"\n\nPHN: {patient.phn}\nName: {patient.name}\nBirthday: {patient.birth_date}\nPhone Number: {patient.phone}\nEmail: {patient.email}\nAddress: {patient.address}"
            confirmationBox = QMessageBox.question(self, "Confirm", "Are you sure you want to delete this patient?" + patientString)

            if confirmationBox == QMessageBox.StandardButton.Yes:
                self.controller.delete_patient(int(PHN))
                self.stackedLayout.setCurrentIndex(2)
                QMessageBox.information(self, "Success", "Patient deleted.")

        PHNInput.clear()

