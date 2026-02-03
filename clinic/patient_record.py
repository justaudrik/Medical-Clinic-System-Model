from clinic.note import Note
from clinic.dao.note_dao_pickle import NoteDAOPickle

class PatientRecord:
	def __init__(self, phn, autosave=False):
		self.autosave = autosave
		self.ndp = NoteDAOPickle(phn, autosave)

	# Creates a new note and adds it to ndp
	def create_note(self, msg) -> Note:
		return self.ndp.create_note(msg)

	# Searches for the note with matching code in ndp
	def search_note(self, code) -> Note:
		return self.ndp.search_note(code)

	# Searches for and returns all notes that contain a substring equal to the inputted msg
	def retrieve_notes(self, msg) -> list[Note]:
		return self.ndp.retrieve_notes(msg)
	
	# Deletes the note with the matching code in ndp
	def delete_note(self, code) -> bool:
		return self.ndp.delete_note(code)
	
	# Updates the note that matches the code to have the inputted msg
	def update_note(self, code, msg) -> bool:
		return self.ndp.update_note(code, msg)

	# Lists all notes stored in ndp
	# Returns the list in the order: recent -> old
	def list_notes(self) -> list[Note]:
		return self.ndp.list_notes()
