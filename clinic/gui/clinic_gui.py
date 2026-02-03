import sys
from PyQt6.QtCore import Qt
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QHBoxLayout, QStackedLayout
from clinic.gui.main_menu_gui import MainMenuGUI
from clinic.gui.main_menu_elements.add_new_patient_gui import AddNewPatientGUI
from clinic.gui.main_menu_elements.search_patient_gui import SearchPatientGUI
from clinic.gui.main_menu_elements.delete_patient_gui import DeletePatientGUI
from clinic.gui.main_menu_elements.retrieve_patients_gui import RetrievePatientsGUI
from clinic.gui.main_menu_elements.list_patients_gui import ListPatientsGUI
from clinic.gui.main_menu_elements.update_patient_gui import UpdatePatientGUI
from clinic.gui.main_menu_elements.get_phn_gui import GetPHNGUI
from clinic.gui.appointment_gui import AppointmentGUI
from clinic.gui.appointment_menu_elements.add_note_gui import AddNoteGUI
from clinic.gui.appointment_menu_elements.change_note_gui import ChangeNoteGUI
from clinic.gui.appointment_menu_elements.list_notes_gui import ListNotesGUI
from clinic.gui.appointment_menu_elements.remove_note_gui import RemoveNoteGUI
from clinic.gui.appointment_menu_elements.retrieve_notes_gui import RetrieveNotesGUI
from clinic.controller import Controller 

class ClinicGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = Controller(autosave=True)
        self.setWindowTitle("MEDICAL CLINIC SYSTEM")
        self.stackedLayout = QStackedLayout()
        
        # Initializing all of the screens
        self.list_patients_gui = ListPatientsGUI(self.controller, self.stackedLayout)
        self.main_menu_gui = MainMenuGUI(self.controller, self.stackedLayout, self.list_patients_gui)
        self.add_new_patient_gui = AddNewPatientGUI(self.controller, self.stackedLayout)
        self.search_patient_gui = SearchPatientGUI(self.controller, self.stackedLayout)
        self.delete_patient_gui = DeletePatientGUI(self.controller, self.stackedLayout)
        self.retrieve_patients_gui = RetrievePatientsGUI(self.controller, self.stackedLayout)
        self.update_patient_gui = UpdatePatientGUI(self.controller, self.stackedLayout)
        self.list_notes_gui = ListNotesGUI(self.controller, self.stackedLayout)
        self.appointment_menu_gui = AppointmentGUI(self.controller, self.stackedLayout, self)
        self.get_phn_gui = GetPHNGUI(self.controller, self.stackedLayout, self)
        self.add_note_gui = AddNoteGUI(self.controller, self.stackedLayout)
        self.change_note_gui = ChangeNoteGUI(self.controller, self.stackedLayout)
        self.remove_note_gui = RemoveNoteGUI(self.controller, self.stackedLayout)
        self.retrieve_note_gui = RetrieveNotesGUI(self.controller, self.stackedLayout)
        
        # Add the screens to the main layout | stackedLayout Index:
        self.stackedLayout.addWidget(self.homeScreen()) # 0
        self.stackedLayout.addWidget(self.loginScreen()) # 1
        
        self.stackedLayout.addWidget(self.main_menu_gui.mainMenu()) # 2
        self.stackedLayout.addWidget(self.add_new_patient_gui.addNewScreen()) # 3
        self.stackedLayout.addWidget(self.search_patient_gui.searchPatientScreen()) # 4
        self.stackedLayout.addWidget(self.delete_patient_gui.deletePatientScreen()) # 5
        self.stackedLayout.addWidget(self.retrieve_patients_gui.retrievePatientsScreen()) # 6
        self.stackedLayout.addWidget(self.list_patients_gui.listPatientsScreen()) # 7
        self.stackedLayout.addWidget(self.update_patient_gui.updatePatientScreen()) # 8
        
        self.stackedLayout.addWidget(self.get_phn_gui.getPHNScreen()) # 9
        self.stackedLayout.addWidget(self.appointment_menu_gui.appointmentMenuScreen()) # 10
        self.stackedLayout.addWidget(self.add_note_gui.addNoteScreen()) # 11
        self.stackedLayout.addWidget(self.change_note_gui.changeNoteScreen()) # 12
        self.stackedLayout.addWidget(self.list_notes_gui.listNotesScreen()) # 13
        self.stackedLayout.addWidget(self.remove_note_gui.removeNoteScreen()) # 14
        self.stackedLayout.addWidget(self.retrieve_note_gui.retrieveNotesScreen()) # 15
 
        # Setting up the main widget for the screen and setting the main layout to it
        widget = QWidget()
        widget.setLayout(self.stackedLayout)
        self.setCentralWidget(widget)
    
    # Opening Screen for logging in or quitting
    def homeScreen(self):
        homeScreenWidget = QWidget()
        homeScreenOptions = QVBoxLayout()

        welcomeText = QLabel("Welcome to the Medical Clinic System.")
        welcomeText.setAlignment(Qt.AlignmentFlag.AlignCenter) # Center aligning the text
 
        loginButton = QPushButton("Login")
        loginButton.clicked.connect(self.loginButtonClick)

        quitButton = QPushButton("Quit")
        quitButton.clicked.connect(self.quitButtonClick)

        homeScreenOptions.addWidget(welcomeText)
        homeScreenOptions.addWidget(loginButton)
        homeScreenOptions.addWidget(quitButton)

        homeScreenWidget.setLayout(homeScreenOptions)
        return homeScreenWidget

    # Function to move to the signin screen
    def loginButtonClick(self):
        self.stackedLayout.setCurrentIndex(1)
    
    # Close the app
    def quitButtonClick(self):
        sys.exit()

    # Screen for inputing username and pass
    def loginScreen(self):

        loginScreenWidget = QWidget()
        loginScreenLayout = QVBoxLayout()

        welcomeText = QLabel("Please enter your details to continue.")  
        welcomeText.setAlignment(Qt.AlignmentFlag.AlignCenter)

        userInput = QLineEdit(self)
        userInput.setPlaceholderText("Username")
        
        passInput = QLineEdit(self)
        passInput.setPlaceholderText("Password")
        passInput.setEchoMode(QLineEdit.EchoMode.Password)

        buttonOptionLayout = QHBoxLayout()

        backButton = QPushButton("Back")
        backButton.clicked.connect(lambda: self.backButtonClick(userInput, passInput)) #Lambda function so function
                                                                                       #is not called when connecting
        enterButton = QPushButton("Enter")
        enterButton.clicked.connect(lambda: self.enterButtonClick(userInput, passInput))

        buttonOptionLayout.addWidget(backButton)
        buttonOptionLayout.addWidget(enterButton)

        loginScreenLayout.addWidget(welcomeText)
        loginScreenLayout.addWidget(userInput)
        loginScreenLayout.addWidget(passInput)
        loginScreenLayout.addLayout(buttonOptionLayout)

        loginScreenWidget.setLayout(loginScreenLayout)
        return loginScreenWidget
    
    # Go back to the home screen
    def backButtonClick(self, userInput, passInput):
        self.stackedLayout.setCurrentIndex(0)
        userInput.clear() #Resetting text for next time user enters login screen
        passInput.clear()

    # Enter the current user and pass fields
    def enterButtonClick(self, userInput, passInput):
        try:
           username = userInput.text()
           password = passInput.text()
           self.controller.login(username, password)
           userInput.clear()
           passInput.clear()
           self.stackedLayout.setCurrentIndex(2)
        except InvalidLoginException:
           QMessageBox.warning(self, "Invalid Login", "Please try again.")
           userInput.clear()
           passInput.clear()


# Setting up the main window
def main():
    app = QApplication(sys.argv)
    window = ClinicGUI()
    window.setMinimumSize(600, 500)
    window.show()
    app.exec()

if __name__ == '__main__':
    main()
