from json import loads, dumps
from clinic.patient import Patient
from clinic.dao.patient_dao import PatientDAO
from clinic.dao.patient_encoder import PatientEncoder
from clinic.dao.patient_decoder import PatientDecoder

class PatientDAOJSON:
    def __init__(self, autosave) -> None:
        self.filename = './clinic/patients.json'
        self.autosave = autosave

        try:
            self.patient_collection = self.load_patient_collection()
        except FileNotFoundError:
            # If reached, then patients.json file was not found
            self.patient_collection = []

    # HELPER METHOD: Loads patient_collection with pre-existing patients from a previously created patients.json file
    def load_patient_collection(self) -> list[Patient]:
        patients = []
        with open(self.filename, 'r') as file:
            for patient_json in file:
                patient = loads(patient_json, cls=PatientDecoder) # Decodes patient_json into python dict for patient
                patients.append(patient)
        return patients
    
    # HELPER METHOD: Create a new OR Update patients.json to store newest version of patient_collection
    def save_file(self) -> None:
        with open(self.filename, 'w') as file:
            for patient in self.patient_collection:
                patient_json = dumps(patient, cls=PatientEncoder)
                file.write("%s\n" % patient_json)
                
    # Searches for and returns the patient with the corresponding key (phn)
    def search_patients(self, key) -> Patient:
        for patient in self.patient_collection:
            if patient.phn == key:
                return patient
            
        # If reached, then patient was not found
        return None
    
    # Appends the newly created patient to patient_collection
    # If autosave = True, it updates patients.json to contain the newly created patient
    def create_patient(self, patient) -> Patient:
        self.patient_collection.append(patient)

        if self.autosave:
            self.save_file()

        return patient
    
    # Return a list of all patients whose names contain the inputted search_string
    def retrieve_patients(self, search_string) -> list[Patient]:
        patient_list = []
        # Grab all patients whose names contain at least a substring equal to the inputted name
        for patient in self.patient_collection:
            if search_string in patient.name:
                patient_list.append(patient)
        return patient_list
    
    # Updates the patient with the corresponding key (phn) to contain the details of the inputted patient
    # If autosave = True, it updates patients.json to contain the newly updated patient
    def update_patient(self, key, patient) -> None:
        # Find patient to be changed
        patient_tbu = self.search_patients(key) # patient to be updated

        # Change patient to new patient
        index = self.patient_collection.index(patient_tbu)
        self.patient_collection[index] = patient
        
        if self.autosave:
            self.save_file()

    # Deletes the patient with the corresponding key (phn) from patient_collection
    # If autosave = True, it updates patients.json to lose the deleted patient
    def delete_patient(self, key) -> None:
        patient_tbd = self.search_patients(key) # patient to be deleted
        self.patient_collection.remove(patient_tbd)

        if self.autosave:
            self.save_file()

    # Returns a list of all patients that have been created and stored in patient_collection
    def list_patients(self) -> list[Patient]:
        return self.patient_collection