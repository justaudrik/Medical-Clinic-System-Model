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

class UpdatePatientGUI(QWidget):

    def __init__(self, controller, stackedLayout):
        super().__init__()
        self.controller = controller
        self.stackedLayout = stackedLayout

    def updatePatientScreen(self):
        updateWidget = QWidget()
        updateLayout = QVBoxLayout()

        buttonOptionLayout = QHBoxLayout()

        self.updateLabel = QLabel("Please enter a patient's PHN to update their info.")
        self.updateLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        currentPHNInput = QLineEdit(self)
        currentPHNInput.setPlaceholderText("Current PHN")
        newPHNInput = QLineEdit(self)
        newPHNInput.setPlaceholderText("PHN")
        nameInput = QLineEdit(self)
        nameInput.setPlaceholderText("Patient Name")
        birthDateInput = QLineEdit(self)
        birthDateInput.setPlaceholderText("Patient Birthday")
        phoneInput = QLineEdit(self)
        phoneInput.setPlaceholderText("Patient Phone Number")
        emailInput = QLineEdit(self)
        emailInput.setPlaceholderText("Patient Email")
        addressInput = QLineEdit(self)
        addressInput.setPlaceholderText("Patient Address")

        newPHNInput.hide()
        nameInput.hide()
        birthDateInput.hide()
        phoneInput.hide()
        emailInput.hide()
        addressInput.hide()

        backButton = QPushButton("Back")
        backButton.clicked.connect(lambda: self.backButtonClick(saveButton, searchButton, clearButton, currentPHNInput, newPHNInput, nameInput, birthDateInput, phoneInput, emailInput, addressInput))

        clearButton = QPushButton("Clear")
        clearButton.hide()
        clearButton.clicked.connect(lambda: self.clearButtonClick(saveButton, searchButton, clearButton, currentPHNInput, newPHNInput, nameInput, birthDateInput, phoneInput, emailInput, addressInput))

        saveButton = QPushButton("Save")
        saveButton.hide()
        saveButton.clicked.connect(lambda: self.saveButtonClick(saveButton, searchButton, clearButton, currentPHNInput, newPHNInput, nameInput, birthDateInput, phoneInput, emailInput, addressInput))
 
        searchButton = QPushButton("Enter")
        searchButton.clicked.connect(lambda: self.searchButtonClick(saveButton, searchButton, clearButton, currentPHNInput, newPHNInput, nameInput, birthDateInput, phoneInput, emailInput, addressInput))

        buttonOptionLayout.addWidget(backButton)
        buttonOptionLayout.addWidget(clearButton)
        buttonOptionLayout.addWidget(saveButton)
        buttonOptionLayout.addWidget(searchButton)

        updateLayout.addWidget(self.updateLabel)
        updateLayout.addWidget(currentPHNInput)
        updateLayout.addWidget(newPHNInput)
        updateLayout.addWidget(nameInput)
        updateLayout.addWidget(birthDateInput)
        updateLayout.addWidget(phoneInput)
        updateLayout.addWidget(emailInput)
        updateLayout.addWidget(addressInput)

        updateLayout.addLayout(buttonOptionLayout)
        updateWidget.setLayout(updateLayout)

        return updateWidget
    
    # Checks to see if the inputted PHN is a valid user and if so loads their info
    def searchButtonClick(self, saveButton, searchButton, clearButton, currentPHNInput, newPHNInput, nameInput, birthDateInput, phoneInput, emailInput, addressInput):
        PHN = currentPHNInput.text().strip()
        if not PHN:
            QMessageBox.warning(self, "Invalid Input", "Please enter a PHN.")
            return

        patient = self.controller.search_patient(int(PHN))

        if patient is None:
            QMessageBox.warning(self, "Invalid PHN", "No patient with this PHN exists.")
            currentPHNInput.setText("")
        else:
            # Updating the buttons so save and clear only show when a patient is found, and search when
            # A patient has not yet been found
            saveButton.show()
            clearButton.show()
            searchButton.hide()
            
            currentPHNInput.hide()
            newPHNInput.show()
            nameInput.show()
            birthDateInput.show()
            phoneInput.show()
            emailInput.show()
            addressInput.show()

            # Loading a patients current data into the text boxes to be edited by the user
            newPHNInput.setText(str(patient.phn))
            nameInput.setText(patient.name)
            birthDateInput.setText(patient.birth_date)
            phoneInput.setText(patient.phone)
            emailInput.setText(patient.email)
            addressInput.setText(patient.address)

            # Update label text
            self.updateLabel.setText("Update the following patient fields.")

    # Saves the users new info and overwrites what was there before
    def saveButtonClick(self, saveButton, searchButton, clearButton, currentPHNInput, newPHNInput, nameInput, birthDateInput, phoneInput, emailInput, addressInput):
        # Updates the patients info in the controller and clears and hides all the update boxes
        PHN = newPHNInput.text().strip()
        if not PHN:
            QMessageBox.warning(self, "Invalid Input", "Please enter a PHN.")
            return

        self.controller.update_patient(int(currentPHNInput.text()), int(newPHNInput.text()), nameInput.text(), birthDateInput.text(), phoneInput.text(), emailInput.text(), addressInput.text())
       
        # Reset to initial GUI state
        currentPHNInput.setText("")
        currentPHNInput.show()
        newPHNInput.setText("")
        nameInput.setText("")
        birthDateInput.setText("")
        phoneInput.setText("")
        emailInput.setText("")
        addressInput.setText("")

        newPHNInput.hide()
        nameInput.hide()
        birthDateInput.hide()
        phoneInput.hide()
        emailInput.hide()
        addressInput.hide()

        saveButton.hide()
        clearButton.hide()
        searchButton.show()
        self.updateLabel.setText("Please enter a patient's PHN to update their info.")
        QMessageBox.information(self, "Success", "Patient information updated.")

        # Go back to the main menu
        self.stackedLayout.setCurrentIndex(2)

    # Clears the currently loaded user's info
    def clearButtonClick(self, saveButton, searchButton, clearButton, currentPHNInput, newPHNInput, nameInput, birthDateInput, phoneInput, emailInput, addressInput):
        currentPHNInput.setText("")
        newPHNInput.setText("")
        nameInput.setText("")
        birthDateInput.setText("")
        phoneInput.setText("")
        emailInput.setText("")
        addressInput.setText("")

        currentPHNInput.show()
        newPHNInput.hide()
        nameInput.hide()
        birthDateInput.hide()
        phoneInput.hide()
        emailInput.hide()
        addressInput.hide()

        saveButton.hide()
        clearButton.hide()
        searchButton.show()

        self.updateLabel.setText("Please enter a patient's PHN to update their info.")
    # Goes back to the main menu
    def backButtonClick(self, saveButton, searchButton, clearButton, currentPHNInput, newPHNInput, nameInput, birthDateInput, phoneInput, emailInput, addressInput):
        currentPHNInput.setText("")
        newPHNInput.setText("")
        nameInput.setText("")
        birthDateInput.setText("")
        phoneInput.setText("")
        emailInput.setText("")
        addressInput.setText("")

        currentPHNInput.show()
        newPHNInput.hide()
        nameInput.hide()
        birthDateInput.hide()
        phoneInput.hide()
        emailInput.hide()
        addressInput.hide()

        saveButton.hide()
        clearButton.hide()
        searchButton.show()
        self.updateLabel.setText("Please enter a patient's PHN to update their info.")
        self.stackedLayout.setCurrentIndex(2)
