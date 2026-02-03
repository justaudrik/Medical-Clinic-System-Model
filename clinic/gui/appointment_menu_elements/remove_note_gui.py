import sys
from PyQt6.QtCore import Qt, QRegularExpression
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QStackedLayout
from clinic.controller import Controller

class RemoveNoteGUI(QWidget):
    def __init__(self, controller, stackedLayout):
        super().__init__()
        self.controller = controller
        self.stackedLayout = stackedLayout
    
    def removeNoteScreen(self):
        removeNoteWidget = QWidget()
        removeNoteLayout = QVBoxLayout()

        buttonOptionsLayout = QHBoxLayout()
        
        labelText = QLabel("Please enter the code of the note you want to delete.")
        labelText.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center aligning the text
        
        noteInput = QLineEdit(self)
        
        goBackButton = QPushButton("Back")
        goBackButton.clicked.connect(lambda: self.goBackButtonClick(noteInput))
        
        enterButton = QPushButton("Enter")
        enterButton.clicked.connect(lambda: self.enterButtonClick(noteInput))
        
        removeNoteLayout.addWidget(labelText)
        removeNoteLayout.addWidget(noteInput)
        
        buttonOptionsLayout.addWidget(goBackButton)
        buttonOptionsLayout.addWidget(enterButton)
        
        removeNoteLayout.addLayout(buttonOptionsLayout)
        removeNoteWidget.setLayout(removeNoteLayout)
        
        return removeNoteWidget
    
    # Go back to the appointment menu
    def goBackButtonClick(self, noteInput):
        noteInput.clear()
        self.stackedLayout.setCurrentIndex(10)
        
    # If clicked, remove the note corresponding with the user's inputted code inside noteInput
    def enterButtonClick(self, noteInput):
        code = noteInput.text()
        if not code:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid code.")
            return
        
        note = self.controller.search_note(int(code))
        
        if note is None:
            QMessageBox.warning(self, "Invalid Code", "There is no note that exists with this code.")
        else:
            # Confirm with the user if they want to delete the note
            noteString = f"\n\nCode: {note.code}\nText: {note.text}\nTimestamp: {note.timestamp}"
            confirmationBox = QMessageBox.question(self, "Confirm?", "Are you sure you want to delete this note?" + noteString)
            
            if confirmationBox == QMessageBox.StandardButton.Yes:
                self.controller.delete_note(int(code))
                QMessageBox.information(self, "Success", "Note has been deleted.")
                
        noteInput.clear()