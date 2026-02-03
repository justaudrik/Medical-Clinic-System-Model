import sys
from PyQt6.QtCore import Qt, QRegularExpression
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableView, QPlainTextEdit
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QStackedLayout
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from clinic.controller import Controller

class RetrieveNotesGUI(QWidget):
    def __init__(self, controller, stackedLayout):
        super().__init__()
        self.controller = controller
        self.stackedLayout = stackedLayout
        self.noteText = QPlainTextEdit()
    
    def retrieveNotesScreen(self):
        retrieveNotesScreenWidget = QWidget()
        retrieveNotesScreenLayout = QVBoxLayout()
        
        buttonOptionsLayout = QHBoxLayout()

        labelText = QLabel("Retrieve notes by searching for their text.")
        labelText.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center aligning the text
        
        noteInput = QLineEdit(self)
        
        goBackButton = QPushButton("Back")
        goBackButton.clicked.connect(lambda: self.goBackButtonClick(noteInput))
        
        enterButton = QPushButton("Enter")
        enterButton.clicked.connect(lambda: self.enterButtonClick(noteInput))
        
        buttonOptionsLayout.addWidget(goBackButton)
        buttonOptionsLayout.addWidget(enterButton)
        
        self.noteText.setReadOnly(True)
        retrieveNotesScreenLayout.addWidget(labelText)
        retrieveNotesScreenLayout.addWidget(self.noteText)
        retrieveNotesScreenLayout.addWidget(noteInput)
        retrieveNotesScreenLayout.addLayout(buttonOptionsLayout)
        retrieveNotesScreenWidget.setLayout(retrieveNotesScreenLayout)
        
        return retrieveNotesScreenWidget
    
    # Goes back to the appointment menu
    def goBackButtonClick(self, noteInput):
        noteInput.clear()
        self.noteText.clear()
        self.stackedLayout.setCurrentIndex(10)
        
    # If clicked, retrieve and display all notes that contain note_substring in their text
    def enterButtonClick(self, noteInput):
        note_substring = noteInput.text().strip()
        notes = self.controller.retrieve_notes(note_substring)
        if not notes:
            QMessageBox.warning(self, "Invalid text", "No notes with this text exist.", QMessageBox.StandardButton.Ok)
        else:
            x = "" # Holds current note
            y = "" # Holds all notes
            for note in notes:
                x = f"Code: {note.code}, Text: {note.text}, Timestamp: {note.timestamp}\n"
                y += x
            self.noteText.setPlainText(y)
        noteInput.clear()