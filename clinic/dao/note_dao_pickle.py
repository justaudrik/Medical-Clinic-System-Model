import pickle
from clinic.note import Note
from clinic.dao.note_dao import NoteDAO

class NoteDAOPickle:
    def __init__(self, phn, autosave=False):
        self.autosave = autosave
        self.phn = phn
        self.filename = './clinic/records/' + str(self.phn) + '.dat' # patient record file

        try:
            self.note_collection = self.load_note_collection()
        except:
            # If reached, then <patient.phn>.dat file was not found
            self.note_collection = []

        # Stores the number of notes being stored in note_collection
        self.autocounter = len(self.note_collection)
       
    # HELPER METHOD: Loads note_collection with pre-existing notes from a previously created .dat file corresponding with the patient's phn
    def load_note_collection(self) -> list[Note]:
        notes = []
        with open(self.filename, 'rb') as file:
            notes = pickle.load(file)
        return notes
    
    # HELPER METHOD: Create a new OR Update <patient.phn>.dat file to store the newest version of note_collection
    def save_file(self) -> None:
        with open(self.filename, 'wb') as file:
            pickle.dump(self.note_collection, file)
            
    # Searches for and returns the note with the inputted key (code)
    def search_note(self, key) -> Note:
        for note in self.note_collection:
            if note.code == key:
                return note
        
        # If reached, note was not found
        return None

    # Creates and returns a new note with the inputted text and incremented autocounter as its code
    # If autosave = True, it updates <patient.phn>.dat to contain the newly created note
    def create_note(self, text) -> Note:
        self.autocounter += 1
        new_note = Note(self.autocounter, text)
        self.note_collection.append(new_note)
        
        if self.autosave:
            self.save_file()
        
        return new_note

    # Compiles and returns a list of notes that contain search_string in their text
    def retrieve_notes(self, search_string) -> list[Note]:
        retrieved_list = []
        for note in self.note_collection:
            if search_string in note.text:
                retrieved_list.append(note)
        return retrieved_list

    # Updates the note with the inputted key, and change its text to the inputted text
    # If autosave = True, it updates <patient.phn>.dat to contain the newly updated note
    def update_note(self, key, text) -> bool: # True = Successfully updated the note; False = Could not update the note; note was not found
        # the_note = the note we are going to update
        the_note = self.search_note(key)
        if the_note == None:
            return False
        
        the_note.update(text)

        if self.autosave:
            self.save_file()

        return True

    # Deletes the note with the inputted key (code)
    # If autosave = True, it updates <patient.phn>.dat to lose the deleted note
    def delete_note(self, key) -> bool: # True = Successfully updated the note; False = Could not update the note; note was not found
        the_note = self.search_note(key)
        if the_note == None:
            return False
        
        # If reached, the note was found
        self.note_collection.remove(the_note)
        self.autocounter -= 1

        if self.autosave:
            self.save_file()

        return True

    # Returns a list of all the patient's notes in the order: recent -> old
    def list_notes(self) -> list[Note]:
        return list(reversed(self.note_collection))