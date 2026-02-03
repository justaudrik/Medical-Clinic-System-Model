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

class ListNotesGUI(QWidget): 
    def __init__(self, controller, stackedLayout):
        super().__init__()
        self.controller = controller
        self.stackedLayout = stackedLayout
        self.noteText = QPlainTextEdit()
    
    def listNotesScreen(self):
        listNotesScreenWidget = QWidget()
        listNotesScreenLayout = QVBoxLayout()
        
        goBackButton = QPushButton("Back")
        goBackButton.clicked.connect(self.goBackButtonClick)
        
        self.noteText.setReadOnly(True)
        listNotesScreenLayout.addWidget(self.noteText)
        listNotesScreenLayout.addWidget(goBackButton)
        
        listNotesScreenWidget.setLayout(listNotesScreenLayout)
        return listNotesScreenWidget
    
    # Refresh the contents inside noteTable
    def updateNoteTable(self):
        notes = self.controller.list_notes()
        x = "" # Holds current note
        y = "" # Holds all notes
        for note in notes:
            x = f"Code: {note.code}, Text: {note.text}, Timestamp: {note.timestamp}\n"
            y += x
        self.noteText.setPlainText(y)

    # Goes back to the appointment menu
    def goBackButtonClick(self):
        self.stackedLayout.setCurrentIndex(10)