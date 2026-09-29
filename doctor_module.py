from person_module import Person


class Doctor(Person):
    next_id = 1

    def __init__(self, name, phone, specialization, available_days,
                 username, password, doctor_id=None):
        super().__init__(name, phone)
        self.specialization = specialization
        self.available_days = set(available_days)
        self.username = username
        self.password = password

        if doctor_id is None:
            self.doctor_id = Doctor.next_id
            Doctor.next_id += 1
        else:
            self.doctor_id = doctor_id
            if doctor_id >= Doctor.next_id:
                Doctor.next_id = doctor_id + 1

    def is_available_on(self, day):
        return day.capitalize() in self.available_days

    def to_line(self):
        days_text = ",".join(sorted(self.available_days))
        fields = [str(self.doctor_id), self.name, self.phone, self.specialization,
                  days_text, self.username, self.password]
        return "|".join(fields)

    @staticmethod
    def from_line(line):
        parts = line.split("|")
        doctor_id, name, phone, specialization, days_text, username, password = parts
        days = days_text.split(",") if days_text else []
        return Doctor(name, phone, specialization, days, username, password, int(doctor_id))

    def __str__(self):
        days = ", ".join(sorted(self.available_days)) if self.available_days else "Not scheduled"
        return f"[{self.doctor_id}] Dr. {self.name} ({self.specialization}) - Available: {days}"
