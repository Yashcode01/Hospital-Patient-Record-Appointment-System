class Appointment:
    VALID_STATUSES = ("Scheduled", "Completed", "Cancelled")
    next_id = 5001

    def __init__(self, patient_id, patient_name, doctor_id, doctor_name,
                 day, time, reason, status="Scheduled", appointment_id=None):
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.doctor_id = doctor_id
        self.doctor_name = doctor_name
        self.day = day.capitalize()
        self.time = time
        self.reason = reason
        self.status = status

        if appointment_id is None:
            self.appointment_id = Appointment.next_id
            Appointment.next_id += 1
        else:
            self.appointment_id = appointment_id
            if appointment_id >= Appointment.next_id:
                Appointment.next_id = appointment_id + 1

    def to_line(self):
        fields = [str(self.appointment_id), str(self.patient_id), self.patient_name,
                  str(self.doctor_id), self.doctor_name, self.day, self.time,
                  self.status, self.reason]
        return "|".join(fields)

    @staticmethod
    def from_line(line):
        parts = line.split("|")
        appt_id, pid, pname, did, dname, day, time, status, reason = parts
        return Appointment(int(pid), pname, int(did), dname, day, time,
                           reason, status, int(appt_id))

    def __str__(self):
        return (f"Appt#{self.appointment_id} {self.day} {self.time} "
                f"{self.patient_name} -> Dr. {self.doctor_name} {self.status}")
