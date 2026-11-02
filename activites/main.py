import json
import os

DATA_FILE = "school_data.json"
EMAIL_DOMAIN = "tuwaiq.edu.hub"

ADMIN_CODE = "07321098"

SUBJECTS = ["Math", "Python", "Chemistry", "English"]

STAGES = ["First Secondary", "Second Secondary", "Third Secondary"]
SECTIONS = ["Section A", "Section B", "Section C"]


def load_data():
    if not os.path.exists(DATA_FILE):
        return {
            "students": [],
            "teachers": [],
            "schedule": {},
            "next_student_number": 1
        }

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        data.setdefault("students", [])
        data.setdefault("teachers", [])
        data.setdefault("schedule", {})
        data.setdefault("next_student_number", 1)

        return data

    except (json.JSONDecodeError, OSError):
        print("Could not read the data file.")
        print("The file was not replaced to protect your data.")
        raise SystemExit(1)


def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


data = load_data()


def ask_required(message):
    while True:
        value = input(message).strip()

        if value:
            return value
        else:
            print("This field is required. Try again.")

def choose_option(title, options):
    print(f"\n--- {title} ---")

    for i, option in enumerate(options, start=1):
        print(f"{i}. {option}")

    while True:
        choice = input("Enter your choice: ").strip()

        if choice.isdigit():
            number = int(choice)

            if 1 <= number <= len(options):
                return options[number - 1]
            else:
                print("Invalid option number.")
        else:
            print("Please enter a valid number.")


def find_student(identity):
    for student in data["students"]:
        if student["identity"] == identity:
            return student

    return None


def find_teacher(number):
    for teacher in data["teachers"]:
        if teacher["number"] == number:
            return teacher

    return None


def create_student():
    print("\n=== Create a New Student Account ===")

    stage = choose_option("Choose Stage", STAGES)
    section = choose_option("Choose Section", SECTIONS)

    identity = ask_required("Student ID: ")

    if find_student(identity) is not None:
        print("This student is already registered.")
        return

    name = ask_required("Student Full Name (Two Names): ")
    guardian_phone = ask_required("Parent Phone Number: ")
    guardian_name = ask_required("Parent Name: ")

    number = data["next_student_number"]
    email = f"student{number:04d}@{EMAIL_DOMAIN}"

    student = {
        "number": number,
        "identity": identity,
        "name": name,
        "stage": stage,
        "section": section,
        "email": email,
        "guardian_name": guardian_name,
        "guardian_phone": guardian_phone,
        "grades": {},
        "attendance": [],
        "student_notes": [],
        "guardian_notes": [],
        "violations": []
    }

    data["students"].append(student)
    data["next_student_number"] += 1
    save_data()

    print("\nStudent account created successfully!")
    print(f"Student Name: {name}")
    print(f"School Email: {email}")
    print(f"Stage: {stage}")
    print(f"Section: {section}")


def show_current_students():
    print("\n=== Current Students ===")

    stage = choose_option("Choose Stage", STAGES)
    section = choose_option("Choose Section", SECTIONS)

    found = False

    for student in data["students"]:
        if (student["stage"] == stage
                and student["section"] == section):

            print(
                f'\nStudent Number: {student["number"]}'
                f'\nName: {student["name"]}'
                f'\nEmail: {student["email"]}'
            )
            found = True

    if found == False:
        print("No students found in this section.")


def show_grades(student):
    print("\n=== Grades ===")

    if student["grades"]:
        for subject, grade in student["grades"].items():
            print(f"{subject}: {grade} / 100")
    else:
        print("No grades have been added yet.")


def show_attendance(student):
    print("\n=== Attendance Record ===")

    if len(student["attendance"]) == 0:
        print("No attendance records found.")
    else:
        for record in student["attendance"]:
            print(
                f'Date: {record["date"]} | '
                f'Status: {record["status"]}'
            )


def show_notes(student, note_type):
    notes = student[note_type]

    if len(notes) == 0:
        print("No notes found.")
    else:
        for note in notes:
            print(f'- {note["teacher"]}: {note["text"]}')


def student_portal():
    print("\n=== Student Portal ===")

    name = ask_required("Student Name: ")
    identity = ask_required("Student ID: ")

    student = find_student(identity)

    if student is None or student["name"] != name:
        print("Student verification failed.")
        return

    while True:
        print(f"\nWelcome, {student['name']}!")

        choice = choose_option(
            "Student Services",
            [
                "View Grades",
                "View Attendance",
                "View Teacher Notes",
                "View Timetable",
                "Return to Main Menu"
            ]
        )

        if choice == "View Grades":
            show_grades(student)

        elif choice == "View Attendance":
            show_attendance(student)

        elif choice == "View Teacher Notes":
            show_notes(student, "student_notes")

        elif choice == "View Timetable":
            print(
                data["schedule"].get(
                    f'{student["stage"]}|{student["section"]}',
                    "No timetable has been added for this section."
                )
            )

        else:
            break


def guardian_portal():
    print("\n=== Parent Portal ===")

    phone = ask_required("Parent Phone Number: ")
    name = ask_required("Student Name: ")
    identity = ask_required("Student ID: ")

    student = find_student(identity)

    if (student is None
            or student["name"] != name
            or student["guardian_phone"] != phone):
        print("Parent verification failed.")
        return

    while True:
        choice = choose_option(
            "Parent Services",
            [
                "View Grades",
                "View Attendance",
                "View Teacher Notes",
                "View Violations",
                "Return to Main Menu"
            ]
        )

        if choice == "View Grades":
            show_grades(student)

        elif choice == "View Attendance":
            show_attendance(student)

        elif choice == "View Teacher Notes":
            show_notes(student, "guardian_notes")

        elif choice == "View Violations":
            if student["violations"]:
                for violation in student["violations"]:
                    print(f"- {violation}")
            else:
                print("No violations recorded.")

        else:
            break


def teacher_portal():
    print("\n=== Teacher Portal ===")

    number = ask_required("Teacher Number: ")
    code = ask_required("Teacher Access Code: ")

    teacher = find_teacher(number)

    if teacher is None or teacher["code"] != code:
        print("Invalid teacher credentials.")
        return

    print(f'\nWelcome, {teacher["name"]}!')
    print(f'Subject: {teacher["subject"]}')

    while True:
        choice = choose_option(
            "Teacher Services",
            [
                "View My Students",
                "View Student Grades",
                "Add or Update Grade",
                "Add Student Note",
                "Add Parent Note",
                "Record Violation",
                "Record Attendance",
                "Return to Main Menu"
            ]
        )

        if choice == "View My Students":
            for student in data["students"]:
                classroom = (
                    f'{student["stage"]}|{student["section"]}'
                )

                if classroom in teacher["classes"]:
                    print(
                        f'{student["name"]} - '
                        f'{student["stage"]} - '
                        f'{student["section"]}'
                    )

        elif choice == "View Student Grades":
            student = teacher_find_student(teacher)

            if student is not None:
                show_grades(student)

        elif choice == "Add or Update Grade":
            student = teacher_find_student(teacher)

            if student is not None:
                grade_text = ask_required("Grade (0-100): ")

                try:
                    grade = float(grade_text)

                    if 0 <= grade <= 100:
                        student["grades"][teacher["subject"]] = grade
                        save_data()
                        print("Grade saved successfully.")
                    else:
                        print("Grade must be between 0 and 100.")

                except ValueError:
                    print("Please enter a valid numeric grade.")

        elif choice == "Add Student Note":
            student = teacher_find_student(teacher)

            if student is not None:
                note = ask_required("Enter student note: ")

                student["student_notes"].append({
                    "teacher": teacher["name"],
                    "text": note
                })

                save_data()
                print("Student note saved.")

        elif choice == "Add Parent Note":
            student = teacher_find_student(teacher)

            if student is not None:
                note = ask_required("Enter parent note: ")

                student["guardian_notes"].append({
                    "teacher": teacher["name"],
                    "text": note
                })

                save_data()
                print("Parent note saved.")

        elif choice == "Record Violation":
            student = teacher_find_student(teacher)

            if student is not None:
                violation = ask_required("Describe the violation: ")

                student["violations"].append(
                    f'{teacher["name"]}: {violation}'
                )

                save_data()
                print("Violation recorded.")

        elif choice == "Record Attendance":
            student = teacher_find_student(teacher)

            if student is not None:
                date = ask_required(
                    "Date (e.g. 2026-10-27): "
                )

                status = choose_option(
                    "Attendance Status",
                    ["Present", "Absent", "Late", "Excused"]
                )

                student["attendance"].append({
                    "date": date,
                    "status": status
                })

                save_data()
                print("Attendance saved.")

        else:
            break


def teacher_find_student(teacher):
    identity = ask_required("Student ID: ")
    student = find_student(identity)

    if student is None:
        print("Student not found.")
        return None

    classroom = f'{student["stage"]}|{student["section"]}'

    if classroom not in teacher["classes"]:
        print("This student is outside your authorized classes.")
        return None

    return student


def add_teacher():
    print("\n=== Add a New Teacher ===")

    admin_code = ask_required("Administrator Code: ")

    if admin_code != ADMIN_CODE:
        print("You are not authorized to add teachers.")
        return

    name = ask_required("Teacher Name: ")
    number = ask_required("Teacher Number: ")

    if find_teacher(number) is not None:
        print("This teacher number is already registered.")
        return

    subject = choose_option("Choose Subject", SUBJECTS)

    print("\nSelect the classes this teacher teaches.")

    classes = []

    for stage in STAGES:
        print(f"\n{stage}")

        for section in SECTIONS:
            answer = input(
                f"Does the teacher teach {section}? (yes/no): "
            ).strip().lower()

            if answer == "yes":
                classes.append(f"{stage}|{section}")

            elif answer == "no":
                pass

            else:
                print("Invalid answer. This section was skipped.")

    if len(classes) == 0:
        print("No classes were selected.")
        return

    teacher_code = ask_required("Create a teacher access code: ")

    teacher = {
        "name": name,
        "number": number,
        "subject": subject,
        "classes": classes,
        "code": teacher_code
    }

    data["teachers"].append(teacher)
    save_data()

    print("\nTeacher added successfully!")
    print(f"Name: {name}")
    print(f"Teacher Number: {number}")
    print(f"Subject: {subject}")
    print(f"Classes: {', '.join(classes)}")
def add_timetable():
    print("\n=== Add Class Timetable ===")

    admin_code = ask_required("Administrator Code: ")

    if admin_code != ADMIN_CODE:
        print("Access denied.")
        return

    stage = choose_option("Choose Stage", STAGES)
    section = choose_option("Choose Section", SECTIONS)

    classroom = f"{stage}|{section}"

    days = [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday"
    ]

    timetable = []

    for day in days:
        print(f"\n--- {day} ---")

        subjects = []

        for period in range(1, 8):
            subject = input(
                f"Period {period} (Enter to skip): "
            ).strip()

            if subject:
                subjects.append(
                    f"Period {period}: {subject}"
                )

        timetable.append(
            f"{day}\n" + "\n".join(subjects)
        )

    data["schedule"][classroom] = "\n\n".join(timetable)

    save_data()

    print("\nTimetable saved successfully!")  

def main():
    while True:
        print("\n" + "=" * 35)
        print("       TUWAIQ EDU HUB")
        print("=" * 35)

        choice = choose_option(
            "Main Menu",
            [
                "Create New Student Account",
                "View Current Students",
                "Student Information",
                "Add New Teacher",
                "Add Class Timetable",
                "Exit"
            ]
        )

        if choice == "Create New Student Account":
            create_student()

        elif choice == "View Current Students":
            show_current_students()

        elif choice == "Student Information":
            portal = choose_option(
                "Select Account Type",
                [
                    "Teacher",
                    "Student",
                    "Parent",
                    "Return"
                ]
            )

            if portal == "Teacher":
                teacher_portal()
            elif portal == "Student":
                student_portal()
            elif portal == "Parent":
                guardian_portal()

        elif choice == "Add New Teacher":
            add_teacher()

        elif choice == "Add Class Timetable":
            add_timetable()
        elif choice == "Exit":
            print("Tuwaiq Edu Hub has been closed.")
            break


if __name__ == "__main__":
    main()