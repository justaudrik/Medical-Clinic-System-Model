import sys
from PyQt6.QtCore import Qt, QRegularExpression
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QStackedLayout
from clinic.controller import Controller

class AddNoteGUI(QWidget):
    def __init__(self, controller, stackedLayout):
        super().__init__()
        self.controller = controller
        self.stackedLayout = stackedLayout
    
    def addNoteScreen(self):
        addNoteWidget = QWidget()
        addNoteLayout = QVBoxLayout()
        
        buttonOptionLayout = QHBoxLayout()

        addNoteText = QLabel("Please enter what you would like to write in the note.")
        addNoteText.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center aligning the text
        
        noteInput = QLineEdit(self)

        goBackButton = QPushButton("Back")
        goBackButton.clicked.connect(lambda: self.goBackButtonClick(noteInput))
        
        enterButton = QPushButton("Enter")
        enterButton.clicked.connect(lambda: self.enterButtonClick(noteInput))
        
        addNoteLayout.addWidget(addNoteText)
        addNoteLayout.addWidget(noteInput)
        
        buttonOptionLayout.addWidget(goBackButton)
        buttonOptionLayout.addWidget(enterButton)
        
        addNoteLayout.addLayout(buttonOptionLayout)
        addNoteWidget.setLayout(addNoteLayout)
        
        return addNoteWidget
    
    # Goes back to the appointment menu
    def goBackButtonClick(self, noteText):
        noteText.clear()
        self.stackedLayout.setCurrentIndex(10)
        
    # Create's the note through the controller
    def enterButtonClick(self, noteInput):
        note = noteInput.text()
        patient = self.controller.get_current_patient()
        patient.record.create_note(note)
        QMessageBox.information(self, "Success", "Note has been created", QMessageBox.StandardButton.Ok)
        
        noteInput.clear()