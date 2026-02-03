import sys
from PyQt6.QtCore import Qt, QRegularExpression
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QStackedLayout
from clinic.controller import Controller

class ChangeNoteGUI(QWidget):
    def __init__(self, controller, stackedLayout):
        super().__init__()
        self.controller = controller
        self.stackedLayout = stackedLayout
    
    def changeNoteScreen(self):
        changeNoteWidget = QWidget()
        changeNoteLayout = QVBoxLayout()
        
        buttonOptionsLayout = QHBoxLayout()

        self.labelText = QLabel("Please enter the code number of the note you would like to change.")
        self.labelText.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center aligning the text
        
        noteInput = QLineEdit(self) # Re-use for updating text
        
        goBackButton = QPushButton("Back")
        goBackButton.clicked.connect(lambda: self.goBackButtonClick(noteInput, clearButton, updateButton, enterButton))
        
        enterButton = QPushButton("Enter")
        enterButton.clicked.connect(lambda: self.enterButtonClick(noteInput, clearButton, updateButton, enterButton))
        
        clearButton = QPushButton("Clear")
        clearButton.clicked.connect(lambda: self.clearButtonClick(noteInput))
        clearButton.hide()
        
        updateButton = QPushButton("Update")
        updateButton.clicked.connect(lambda: self.updateButtonClick(noteInput, clearButton, updateButton, enterButton))
        updateButton.hide()
        
        changeNoteLayout.addWidget(self.labelText)
        changeNoteLayout.addWidget(noteInput)
        
        buttonOptionsLayout.addWidget(goBackButton)
        buttonOptionsLayout.addWidget(enterButton)
        buttonOptionsLayout.addWidget(clearButton)
        buttonOptionsLayout.addWidget(updateButton)
        
        changeNoteLayout.addLayout(buttonOptionsLayout)
        changeNoteWidget.setLayout(changeNoteLayout)
        
        return changeNoteWidget
    
    # Go back to initial GUI state before going back to appointment menu
    def goBackButtonClick(self, noteInput, clearButton, updateButton, enterButton):
        noteInput.clear()
        clearButton.hide()
        updateButton.hide()
        enterButton.show()
        self.labelText.setText("Please enter the code of the note you would like to change.")
        self.stackedLayout.setCurrentIndex(10)
        
    # If clicked, update the note corresponding with the inputted code
    def enterButtonClick(self, noteInput, clearButton, updateButton, enterButton):
        code = noteInput.text().strip()
        if not code:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid code.")
            noteInput.clear()
            return
        
        try:
            self.note_code = int(code)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid code.")
            noteInput.clear()
            return

        note = self.controller.search_note(self.note_code)
        
        if note is None:
            QMessageBox.warning(self, "Invalid Code", "There is no note that exists with this code.")
            noteInput.clear()
        else:
            # Show required fields for updating the note
            self.labelText.setText("Update the note's text to your liking.")
            enterButton.hide()
            clearButton.show()
            updateButton.show()
            
            noteInput.setText(note.text)
            
    def clearButtonClick(self, noteInput):
        noteInput.clear()
        
    # Update the note and reset to initial GUI state
    # If clicked, we know that code is valid and exists
    def updateButtonClick(self, noteInput, clearButton, updateButton, enterButton):
        self.controller.update_note(self.note_code, noteInput.text())
        noteInput.clear()
        clearButton.hide()
        updateButton.hide()
        enterButton.show()
        self.labelText.setText("Please enter the code of the note you would like to change.")
        QMessageBox.information(self, "Success", "Note has been updated.")