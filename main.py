from array import array

from patient_module import Patient
from doctor_module import Doctor
from appointment_module import Appointment
from file_utils import read_lines, write_lines

PATIENTS_FILE = "data/patients.txt"
DOCTORS_FILE = "data/doctors.txt"
APPOINTMENTS_FILE = "data/appointments.txt"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def load_patients():
    lines = read_lines(PATIENTS_FILE)
    patients = []
    for line in lines:
        patients.append(Patient.from_line(line))
    return patients


def save_patients(patients):
    lines = []
    for p in patients:
        lines.append(p.to_line())
    write_lines(PATIENTS_FILE, lines)


def load_doctors():
    lines = read_lines(DOCTORS_FILE)
    doctors = []
    for line in lines:
        doctors.append(Doctor.from_line(line))
    return doctors


def save_doctors(doctors):
    lines = []
    for d in doctors:
        lines.append(d.to_line())
    write_lines(DOCTORS_FILE, lines)


def load_appointments():
    lines = read_lines(APPOINTMENTS_FILE)
    appointments = []
    for line in lines:
        appointments.append(Appointment.from_line(line))
    return appointments


def save_appointments(appointments):
    lines = []
    for a in appointments:
        lines.append(a.to_line())
    write_lines(APPOINTMENTS_FILE, lines)


def find_patient_by_id(patients, patient_id):
    for p in patients:
        if p.patient_id == patient_id:
            return p
    return None


def find_patient_by_username(patients, username):
    for p in patients:
        if p.username.lower() == username.lower():
            return p
    return None


def find_doctor_by_id(doctors, doctor_id):
    for d in doctors:
        if d.doctor_id == doctor_id:
            return d
    return None


def find_doctor_by_username(doctors, username):
    for d in doctors:
        if d.username.lower() == username.lower():
            return d
    return None


def find_appointment_by_id(appointments, appointment_id):
    for a in appointments:
        if a.appointment_id == appointment_id:
            return a
    return None


def is_slot_taken(appointments, doctor_id, day, time):
    for a in appointments:
        if a.doctor_id == doctor_id and a.day.capitalize() == day.capitalize() \
                and a.time == time and a.status == "Scheduled":
            return True
    return False


def book_appointment(patients, doctors, appointments, patient_id, doctor_id, day, time, reason):
    patient = find_patient_by_id(patients, patient_id)
    doctor = find_doctor_by_id(doctors, doctor_id)

    if patient is None:
        print("Patient not found.")
        return None
    if doctor is None:
        print("Doctor not found.")
        return None
    if not doctor.is_available_on(day):
        available_text = ", ".join(sorted(doctor.available_days))
        print(f"Dr. {doctor.name} is not available on {day.capitalize()}. Available days: {available_text}")
        return None
    if is_slot_taken(appointments, doctor_id, day, time):
        print(f"Dr. {doctor.name} already has an appointment at {day.capitalize()} {time}.")
        return None

    new_appointment = Appointment(patient.patient_id, patient.name,
                                   doctor.doctor_id, doctor.name, day, time, reason)
    appointments.append(new_appointment)
    save_appointments(appointments)
    print(f"Appointment #{new_appointment.appointment_id} booked with Dr. {doctor.name} on {new_appointment.day} at {time}.")
    return new_appointment


def average_patient_age(patients):
    if len(patients) == 0:
        return 0
    ages = array('i', [p.age for p in patients])
    total = 0
    for age in ages:
        total += age
    return total / len(ages)


def appointment_status_counts(appointments):
    counts = {}
    for a in appointments:
        if a.status in counts:
            counts[a.status] += 1
        else:
            counts[a.status] = 1
    return counts


def doctor_workload(appointments):
    workload = {}
    for a in appointments:
        if a.status == "Scheduled":
            if a.doctor_name in workload:
                workload[a.doctor_name] += 1
            else:
                workload[a.doctor_name] = 1
    return workload


def admin_menu(patients, doctors, appointments):
    while True:
        print("\nAdmin Menu")
        print("1. Register New Patient")
        print("2. View All Patients")
        print("3. Add Doctor")
        print("4. View All Doctors")
        print("5. Create Doctor Login")
        print("6. View All Appointments")
        print("7. Update Appointment Status")
        print("8. Hospital Summary Report")
        print("9. Doctor Workload Report")
        print("10. Logout")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            name = input("Patient name: ").strip()
            age_text = input("Age: ").strip()
            gender = input("Gender: ").strip()
            phone = input("Phone: ").strip()
            username = input("Choose a username for this patient: ").strip()
            password = input("Choose a password: ").strip()

            if not age_text.isdigit():
                print("Age must be a whole number.")
                continue
            if find_patient_by_username(patients, username) is not None:
                print("That username is already taken.")
                continue

            new_patient = Patient(name, int(age_text), gender, phone, username, password)
            patients.append(new_patient)
            save_patients(patients)
            print(f"Patient '{name}' registered with ID {new_patient.patient_id}.")

        elif choice == "2":
            if len(patients) == 0:
                print("No patients registered yet.")
            else:
                for p in patients:
                    print(p)

        elif choice == "3":
            name = input("Doctor name: ").strip()
            phone = input("Phone: ").strip()
            specialization = input("Specialization: ").strip()
            days_text = input("Available days (comma separated, e.g. Monday,Wednesday): ").strip()
            days = [d.strip().capitalize() for d in days_text.split(",") if d.strip() != ""]
            username = input("Choose a username for this doctor: ").strip()
            password = input("Choose a password: ").strip()

            new_doctor = Doctor(name, phone, specialization, days, username, password)
            doctors.append(new_doctor)
            save_doctors(doctors)
            print(f"Dr. {name} added with ID {new_doctor.doctor_id}.")

        elif choice == "4":
            if len(doctors) == 0:
                print("No doctors on record yet.")
            else:
                for d in doctors:
                    print(d)

        elif choice == "5":
            doctor_id_text = input("Doctor ID this login belongs to: ").strip()
            if not doctor_id_text.isdigit():
                print("Invalid doctor ID.")
                continue
            doctor = find_doctor_by_id(doctors, int(doctor_id_text))
            if doctor is None:
                print("Doctor not found.")
                continue
            username = input("Choose a username: ").strip()
            password = input("Choose a password: ").strip()
            doctor.username = username
            doctor.password = password
            save_doctors(doctors)
            print(f"Login '{username}' set for Dr. {doctor.name}.")

        elif choice == "6":
            if len(appointments) == 0:
                print("No appointments yet.")
            else:
                for a in appointments:
                    print(a)

        elif choice == "7":
            appt_id_text = input("Appointment ID: ").strip()
            if not appt_id_text.isdigit():
                print("Invalid appointment ID.")
                continue
            appointment = find_appointment_by_id(appointments, int(appt_id_text))
            if appointment is None:
                print("Appointment not found.")
                continue
            print("Valid statuses:", ", ".join(Appointment.VALID_STATUSES))
            new_status = input("New status: ").strip().capitalize()
            if new_status not in Appointment.VALID_STATUSES:
                print("That is not a valid status.")
                continue
            appointment.status = new_status
            save_appointments(appointments)
            print(f"Appointment #{appointment.appointment_id} marked as '{new_status}'.")

        elif choice == "8":
            counts = appointment_status_counts(appointments)
            avg_age = average_patient_age(patients)
            print(f"Total Patients: {len(patients)}")
            print(f"Total Doctors: {len(doctors)}")
            print(f"Total Appointments: {len(appointments)}")
            print(f"Average Patient Age: {round(avg_age, 1)}")
            for status in counts:
                print(f"{status}: {counts[status]}")

        elif choice == "9":
            workload = doctor_workload(appointments)
            if len(workload) == 0:
                print("No scheduled appointments right now.")
            else:
                for doctor_name in workload:
                    print(f"Dr. {doctor_name}: {workload[doctor_name]} appointment(s)")

        elif choice == "10":
            print("Logging out.")
            break

        else:
            print("Invalid choice.")


def doctor_menu(doctor, patients, appointments):
    while True:
        print(f"\nDoctor Menu - Dr. {doctor.name}")
        print("1. View My Schedule")
        print("2. Mark Appointment as Completed")
        print("3. View a Patient's Medical History")
        print("4. Add Medical Note for a Patient")
        print("5. Logout")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            my_appointments = [a for a in appointments if a.doctor_id == doctor.doctor_id]
            if len(my_appointments) == 0:
                print("No appointments found.")
            else:
                for a in my_appointments:
                    print(a)

        elif choice == "2":
            appt_id_text = input("Appointment ID to mark completed: ").strip()
            if not appt_id_text.isdigit():
                print("Invalid appointment ID.")
                continue
            appointment = find_appointment_by_id(appointments, int(appt_id_text))
            if appointment is None:
                print("Appointment not found.")
                continue
            appointment.status = "Completed"
            save_appointments(appointments)
            print(f"Appointment #{appointment.appointment_id} marked as Completed.")

        elif choice == "3":
            patient_id_text = input("Patient ID: ").strip()
            if not patient_id_text.isdigit():
                print("Invalid patient ID.")
                continue
            patient = find_patient_by_id(patients, int(patient_id_text))
            if patient is None:
                print("Patient not found.")
                continue
            if len(patient.history) == 0:
                print("No medical history recorded yet.")
            else:
                count = 1
                for note in patient.history:
                    print(f"{count}. {note}")
                    count += 1

        elif choice == "4":
            patient_id_text = input("Patient ID: ").strip()
            note = input("Note (diagnosis/prescription/remarks): ").strip()
            if not patient_id_text.isdigit() or note == "":
                print("Patient ID and note are both required.")
                continue
            patient = find_patient_by_id(patients, int(patient_id_text))
            if patient is None:
                print("Patient not found.")
                continue
            patient.add_note(note)
            save_patients(patients)
            print("Note added to patient history.")

        elif choice == "5":
            print("Logging out.")
            break

        else:
            print("Invalid choice.")


def patient_menu(patient, doctors, patients, appointments):
    while True:
        print(f"\nPatient Menu - {patient.name}")
        print("1. View Available Doctors")
        print("2. Book Appointment")
        print("3. View My Appointments")
        print("4. Cancel Appointment")
        print("5. View My Medical History")
        print("6. Logout")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            if len(doctors) == 0:
                print("No doctors on record yet.")
            else:
                for d in doctors:
                    print(d)

        elif choice == "2":
            for d in doctors:
                print(d)
            doctor_id_text = input("Doctor ID: ").strip()
            day = input("Day (e.g. Monday): ").strip()
            time = input("Time (e.g. 10:00): ").strip()
            reason = input("Reason for visit: ").strip()
            if not doctor_id_text.isdigit():
                print("Invalid doctor ID.")
                continue
            book_appointment(patients, doctors, appointments, patient.patient_id,
                             int(doctor_id_text), day, time, reason)

        elif choice == "3":
            my_appointments = [a for a in appointments if a.patient_id == patient.patient_id]
            if len(my_appointments) == 0:
                print("No appointments found.")
            else:
                for a in my_appointments:
                    print(a)

        elif choice == "4":
            appt_id_text = input("Appointment ID to cancel: ").strip()
            if not appt_id_text.isdigit():
                print("Invalid appointment ID.")
                continue
            appointment = find_appointment_by_id(appointments, int(appt_id_text))
            if appointment is None or appointment.patient_id != patient.patient_id:
                print("Appointment not found.")
                continue
            appointment.status = "Cancelled"
            save_appointments(appointments)
            print(f"Appointment #{appointment.appointment_id} cancelled.")

        elif choice == "5":
            if len(patient.history) == 0:
                print("No medical history recorded yet.")
            else:
                count = 1
                for note in patient.history:
                    print(f"{count}. {note}")
                    count += 1

        elif choice == "6":
            print("Logging out.")
            break

        else:
            print("Invalid choice.")


def main():
    patients = load_patients()
    doctors = load_doctors()
    appointments = load_appointments()

    print("Hospital Patient Record and Appointment System")

    while True:
        print("\n1. Login")
        print("2. Register as Patient")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                print("Welcome, admin.")
                admin_menu(patients, doctors, appointments)
                continue

            patient = find_patient_by_username(patients, username)
            if patient is not None and patient.password == password:
                print(f"Welcome, {patient.name}.")
                patient_menu(patient, doctors, patients, appointments)
                continue

            doctor = find_doctor_by_username(doctors, username)
            if doctor is not None and doctor.password == password:
                print(f"Welcome, Dr. {doctor.name}.")
                doctor_menu(doctor, patients, appointments)
                continue

            print("Invalid username or password.")

        elif choice == "2":
            name = input("Full name: ").strip()
            age_text = input("Age: ").strip()
            gender = input("Gender: ").strip()
            phone = input("Phone: ").strip()
            username = input("Choose a username: ").strip()
            password = input("Choose a password: ").strip()

            if not age_text.isdigit():
                print("Age must be a whole number.")
                continue
            if find_patient_by_username(patients, username) is not None:
                print("That username is already taken.")
                continue

            new_patient = Patient(name, int(age_text), gender, phone, username, password)
            patients.append(new_patient)
            save_patients(patients)
            print(f"Patient '{name}' registered with ID {new_patient.patient_id}. You can now log in.")

        elif choice == "3":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
