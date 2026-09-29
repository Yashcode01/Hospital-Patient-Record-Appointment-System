from person_module import Person


class Patient(Person):
    next_id = 1

    def __init__(self, name, age, gender, phone, username, password,
                 patient_id=None, history=None):
        super().__init__(name, phone)
        self.age = age
        self.gender = gender
        self.username = username
        self.password = password
        self.history = history if history is not None else []

        if patient_id is None:
            self.patient_id = Patient.next_id
            Patient.next_id += 1
        else:
            self.patient_id = patient_id
            if patient_id >= Patient.next_id:
                Patient.next_id = patient_id + 1

    def add_note(self, note):
        self.history.append(note)

    def to_line(self):
        history_text = ";".join(self.history)
        fields = [str(self.patient_id), self.name, str(self.age), self.gender,
                  self.phone, self.username, self.password, history_text]
        return "|".join(fields)

    @staticmethod
    def from_line(line):
        parts = line.split("|")
        patient_id, name, age, gender, phone, username, password, history_text = parts
        history = history_text.split(";") if history_text else []
        return Patient(name, int(age), gender, phone, username, password,
                       int(patient_id), history)

    def __str__(self):
        return f"[{self.patient_id}] {self.name}, {self.age}{self.gender[0]} - {self.phone}"
