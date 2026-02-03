import sys
from PyQt6.QtCore import Qt, QRegularExpression
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QStackedLayout
from clinic.controller import Controller

class AppointmentGUI(QWidget):
    def __init__(self, controller, stackedLayout, mainWindow):
        super().__init__()
        self.controller = controller
        self.stackedLayout = stackedLayout
        self.mainWindow = mainWindow
    
    def appointmentMenuScreen(self):
        appointmentMenuWidget = QWidget()
        appointmentMenuLayout = QVBoxLayout()
        
        subAppointmentMenuWidget = QWidget()
        subAppointmentMenuLayout = QGridLayout()
        
        addNoteButton = QPushButton("Add note to patient record")
        addNoteButton.clicked.connect(self.addNoteButtonClick)
        
        retrieveNotesButton = QPushButton("Retrieve notes from patient record")
        retrieveNotesButton.clicked.connect(self.retrieveNotesButtonClick)
        
        changeNoteButton = QPushButton("Change note from patient record")
        changeNoteButton.clicked.connect(self.changeNoteButtonClick)
        
        removeNoteButton = QPushButton("Remove note from patient record")
        removeNoteButton.clicked.connect(self.removeNoteButtonClick)
        
        listNotesButton = QPushButton("List full patient record")
        listNotesButton.clicked.connect(self.listNotesButtonClick)
        
        finishAppointmentButton = QPushButton("Finish appointment")
        finishAppointmentButton.clicked.connect(self.finishAppointmentButtonClick)
        
        subAppointmentMenuLayout.addWidget(addNoteButton, 0, 1)
        subAppointmentMenuLayout.addWidget(retrieveNotesButton, 0, 2)
        subAppointmentMenuLayout.addWidget(changeNoteButton, 1, 1)
        subAppointmentMenuLayout.addWidget(removeNoteButton, 1, 2)
        
        appointmentMenuLayout.addLayout(subAppointmentMenuLayout)
        
        appointmentMenuLayout.addWidget(listNotesButton)
        appointmentMenuLayout.addWidget(finishAppointmentButton)
        
        appointmentMenuWidget.setLayout(appointmentMenuLayout)
        
        return appointmentMenuWidget
    
    # All of these functions navigate to their respective screens for the button in the stackedLayout
    # Goes back to the main menu
    def finishAppointmentButtonClick(self):
        QMessageBox.information(self, " ", "Appointment finished.", QMessageBox.StandardButton.Ok)
        self.mainWindow.setWindowTitle("MEDICAL CLINIC SYSTEM")
        self.stackedLayout.setCurrentIndex(2)
        
    # Navigate to add_note_gui screen
    def addNoteButtonClick(self):
        self.stackedLayout.setCurrentIndex(11)

    # Navigate to retrieve_notes_gui screen
    def retrieveNotesButtonClick(self):
        self.stackedLayout.setCurrentIndex(15)
    
    # Navigate to change_note_gui screen
    def changeNoteButtonClick(self):
        self.stackedLayout.setCurrentIndex(12)
        
    # Navigate to remove_note_gui screen
    def removeNoteButtonClick(self):
        self.stackedLayout.setCurrentIndex(14)
        
    # Navigate to list_notes_gui screen
    def listNotesButtonClick(self):
        # Update the list of notes before loading the table
        self.mainWindow.list_notes_gui.updateNoteTable()

        self.stackedLayout.setCurrentIndex(13)
        
    

