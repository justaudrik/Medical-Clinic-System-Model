import json
import hashlib
from clinic.patient import Patient
from clinic.patient_record import PatientRecord
from clinic.note import Note
from clinic.dao.patient_dao_json import PatientDAOJSON
from clinic.dao.note_dao_pickle import NoteDAOPickle
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

# Main controller object
class Controller:
	# <<< EXCEPTION DEFINITIONS >>>
	# Invalid login = InvalidLoginException
	# Trying to log in while logged in = DuplicateLoginException
	# Trying to log out while not logged in = InvalidLogoutException
	# Adding patient with pre-existing phn, or deleting a patient with a phn that does not exist = IllegalOperationException
	# Performing an action while not logged in, setting non-existent patient as current_patient, or trying to update/delete current_patient = IllegalAccessException
	# Performing an action without setting current_patient = NoCurrentPatientException

	def __init__(self, autosave=False) -> None:
		self.loggedin = False
		self.autosave = autosave
		self.pdj = PatientDAOJSON(autosave)
		self.current_patient = None

		self.filename = 'clinic/users.txt'

		if autosave:
			self.user_system = self.load_user_system()
		else:
			# In-memory test: Set the login information to match users.txt
			self.user_system = {
				'user':'8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92',
				'ali':'6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810',
				'kala':'e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e'
			}

	# HELPER METHOD: Return a dict of username:password pairs, loaded from 'users.txt'
	def load_user_system(self) -> dict:
		users = {}
		with open(self.filename, 'r') as file:
			for line in file:
				entry = line.strip().split(",")
				username = entry[0]
				password = entry[1]
				users[username] = password
		return users

	# Converts the provided password into the encoded version to compare with whats inside user_system
	def get_password_hash(self, password) -> str:
		encoded_password = password.encode('utf-8') # Convert the password to bytes
		hash_object = hashlib.sha256(encoded_password) # Choose a hashing algorithm (e.g., SHA-256)
		hex_dig = hash_object.hexdigest() # Get the hexadecimal digest of the hashed password
		return hex_dig

	# Logs the user into the system depending on if their username/password matches that defined in users.txt
	def login(self, username, password) -> bool:
		if self.loggedin:
			raise DuplicateLoginException()

		if username in self.user_system:
			password_hash = self.get_password_hash(password)
			if self.user_system.get(username) == password_hash:
				self.loggedin = True
				return True
			
			# If reached, then password is not entered in user_system
			raise InvalidLoginException()
			
		# If reached, then username is not entered in user_system
		raise InvalidLoginException()
	
	# If someone is logged in, log them out
	def logout(self) -> bool:
		if self.loggedin:
			self.loggedin = False
			return True
		
		# If reached, user is already logged out, so call to logout is invalid
		raise InvalidLogoutException()
	
	# Creates a patient using the inputted parameters
	def create_patient(self, phn, name, birth_date, phone, email, address) -> Patient:
		new_patient = Patient(phn, name, birth_date, phone, email, address, self.autosave)

		# If user is not logged in
		if self.loggedin == False:
			raise IllegalAccessException()
		
		# If there already exists a patient with the same phn, we cannot create a new_patient, so return None
		if self.search_patient(phn) != None:
			raise IllegalOperationException()

		# Dumps to patient_collection.json file using pdj (PatientDAOJSON)
		return self.pdj.create_patient(new_patient)
	
	# Searches for a specific patient based on inputted phn
	def search_patient(self, phn) -> Patient:
		if self.loggedin == False:
			raise IllegalAccessException()

		return self.pdj.search_patients(phn)

	# Searches for specific patients based on the inputted name
	def retrieve_patients(self, name) -> list[Patient]:
		if self.loggedin == False:
			raise IllegalAccessException()
		
		return self.pdj.retrieve_patients(name)
	
	# Updates the patient with old_phn to have the following parameters
	def update_patient(self, old_phn, new_phn, new_name, new_birth_date, new_phone, new_email, new_address) -> bool:
		if self.loggedin == False:
			raise IllegalAccessException()

		# the_patient = the patient we are going to update
		the_patient = self.search_patient(old_phn)
		
        # If the_patient was not found
		if the_patient == None:
			raise IllegalOperationException()

		# If the patient to update is the current patient
		if the_patient == self.current_patient:
			raise IllegalOperationException()

		# If new_phn != old_phn, there might exist another patient with a matching phn in pdj
		if new_phn != old_phn:
			if self.search_patient(new_phn) != None:
				raise IllegalOperationException()

		the_patient = Patient(new_phn, new_name, new_birth_date, new_phone, new_email, new_address)
		self.pdj.update_patient(old_phn, the_patient)
		return True

	# Deletes the patient (along with their patient record and notes) with the matching phn
	def delete_patient(self, phn) -> bool:
		if self.loggedin == False:
			raise IllegalAccessException()

		# the_patient = the patient we are going to delete
		the_patient = self.search_patient(phn)

		if the_patient == None:
			raise IllegalOperationException()

		if the_patient == self.current_patient:
			raise IllegalOperationException()
		
		self.pdj.delete_patient(phn)
		return True

	# Returns a list of all patients that have been created and stored in patient_collection
	def list_patients(self) -> list[Patient]:
		if self.loggedin:
			return self.pdj.list_patients()
		
		# If reached, user is not logged in, so return None
		raise IllegalAccessException()

	# Sets one patient to current_patient based on inputted phn
	def set_current_patient(self, phn) -> bool:
		if self.loggedin == False:
			raise IllegalAccessException()

		# the_patient = the patient we will set as current_patient
		the_patient = self.search_patient(phn)

		if the_patient == None:
			raise IllegalOperationException()

		self.current_patient = the_patient
		return True
	
	# Unsets the current_patient to None
	def unset_current_patient(self) -> bool:
		if self.loggedin == False or self.current_patient == None:
			raise IllegalAccessException()

		self.current_patient = None
		return True
	
	# Returns current_patient (assuming there is one)
	def get_current_patient(self) -> Patient:
		if self.loggedin == False:
			raise IllegalAccessException()
		
		return self.current_patient
	
	# Create a note for current_patient; returns the newly created note
	def create_note(self, msg) -> Note:
		if self.loggedin == False:
			raise IllegalAccessException()
		
		if self.current_patient == None:
			raise NoCurrentPatientException()

		return self.current_patient.record.create_note(msg)

	# Searches for a specific note based on inputted code; returns the note
	def search_note(self, code) -> Note:
		if self.loggedin == False:
			raise IllegalAccessException()
		
		if self.current_patient == None:
			raise NoCurrentPatientException()
		
		return self.current_patient.record.search_note(code)

	# Returns a list of notes that have the inputted msg in each note, correlating to current_patient's patient record
	def retrieve_notes(self, msg) -> None:
		if self.loggedin == False:
			raise IllegalAccessException()
		
		if self.current_patient == None:
			raise NoCurrentPatientException()
		
		return self.current_patient.record.retrieve_notes(msg)

	# Deletes a specific note from current_patient's patient_record based on the inputted code
	def delete_note(self, code) -> bool:
		if self.loggedin == False:
			raise IllegalAccessException()
		
		if self.current_patient == None:
			raise NoCurrentPatientException()
		
		return self.current_patient.record.delete_note(code)

	# Updates a specific note from current_patient's patient_record that matches the inputted code
	# Replaces the note's old message with the inputted msg
	def update_note(self, code, msg) -> bool:
		if self.loggedin == False:
			raise IllegalAccessException()
		
		if self.current_patient == None:
			raise NoCurrentPatientException()
		
		return self.current_patient.record.update_note(code, msg)

	# Returns a list of all the notes located inside current_patient's patient record
	def list_notes(self) -> list[Note]:
		if self.loggedin == False:
			raise IllegalAccessException()
		
		if self.current_patient == None:
			raise NoCurrentPatientException()
		
		return self.current_patient.record.list_notes()