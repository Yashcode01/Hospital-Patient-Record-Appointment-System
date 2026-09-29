# Hospital Patient Record & Appointment System

A console-based hospital management system written in Python. It supports
three types of users — admin, doctor, and patient — and stores all data in
plain text files.

# Repo link
https://github.com/Yashcode01/Hospital-Patient-Record-Appointment-System

## Features

- Patient registration and login
- Doctor records with specialization and weekly availability
- Appointment booking with availability and double-booking checks
- Appointment status tracking (Scheduled, Completed, Cancelled)
- Medical history notes per patient
- Admin reports: patient/doctor/appointment counts, average patient age,
  doctor workload

## Requirements

- Python 3.8 or higher
- No external libraries or installations needed

## Project Structure

```
hospital_plain/
├── main.py
├── person_module.py
├── patient_module.py
├── doctor_module.py
├── appointment_module.py
├── file_utils.py
└── data/
    ├── doctors.txt
    ├── patients.txt
    └── appointments.txt
```

## How to Run

1. Open the project folder in VS Code (or any terminal).
2. Run:
   ```
   python main.py
   ```

## Login Details

- Admin: username `admin`, password `admin123`
- Doctors are set up by the admin (Admin Menu → Create Doctor Login)
- Patients register themselves from the main menu

## Data Storage

All data is saved as plain text files in the `data/` folder, using `|` as a
field separator. No database or external file format is used.

- `patients.txt` — patient records and login details
- `doctors.txt` — doctor records and login details
- `appointments.txt` — booked appointments

These files are created automatically the first time data is saved.

## Known Limitations

- Passwords are stored as plain text, not hashed.
- Appointment days are entered as weekday names (e.g. "Monday") rather than
  calendar dates.
- If a name or note contains a `|` or `;` character, it will break the file
  format, since those characters are used as separators.

## Possible Improvements

- Add real calendar date support
- Add password hashing
- Move from text file storage to a database
