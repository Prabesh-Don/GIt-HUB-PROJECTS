import os

DATA_DIR = "data"
USER_FILE = os.path.join(DATA_DIR, "users.txt")
PASS_FILE = os.path.join(DATA_DIR, "passwords.txt")
GRADES_FILE = os.path.join(DATA_DIR, "grades.txt")
ECA_FILE = os.path.join(DATA_DIR, "eca.txt")

class User:
    def __init__(self, username, full_name, role):
        self.username = username
        self.full_name = full_name
        self.role = role


def read_file_lines(filepath):
    try:
        with open(filepath, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
    return []


def write_file_lines(filepath, lines):
    try:
        with open(filepath, "w") as file:
            file.writelines(lines)
        return True
    except Exception as e:
        print(f"Error writing to {filepath}: {e}")
        return False


def authenticate(username, password):
    """
    Authenticate a user and return their role if credentials match.
    """
    lines = read_file_lines(PASS_FILE)
    for line in lines:
        stored_username, stored_password, role = line.strip().split(",")
        if username == stored_username and password == stored_password:
            return role
    return None


def get_user_details(username):
    """
    Retrieve full name and role of a user.
    """
    lines = read_file_lines(USER_FILE)
    for line in lines:
        stored_username, full_name, role = line.strip().split(",")
        if username == stored_username:
            return User(username, full_name, role)
    return None


def add_user(username, full_name, password, role):
    """
    Add a new user to the system if the username doesn't already exist.
    """
    existing_users = read_file_lines(USER_FILE)
    if any(line.startswith(f"{username},") for line in existing_users):
        return False  # User exists

    try:
        with open(USER_FILE, "a") as ufile:
            ufile.write(f"{username},{full_name},{role}\n")
        with open(PASS_FILE, "a") as pfile:
            pfile.write(f"{username},{password},{role}\n")
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        return False


def delete_user(username):
    """
    Remove user from users.txt and passwords.txt.
    """
    def filter_lines(lines):
        return [line for line in lines if not line.startswith(f"{username},")]

    users = filter_lines(read_file_lines(USER_FILE))
    passwords = filter_lines(read_file_lines(PASS_FILE))

    return write_file_lines(USER_FILE, users) and write_file_lines(PASS_FILE, passwords)


def get_student_grades(username):
    """
    Return a list of grades for the student.
    """
    lines = read_file_lines(GRADES_FILE)
    for line in lines:
        stored_username, *grades = line.strip().split(",")
        if stored_username == username:
            return grades
    return None


def get_student_eca(username):
    """
    Return a list of extracurricular activities for the student.
    """
    lines = read_file_lines(ECA_FILE)
    for line in lines:
        stored_username, *activities = line.strip().split(",")
        if stored_username == username:
            return activities
    return None


def update_student_profile(username, new_full_name):
    """
    Update full name of a student in users.txt.
    """
    updated_lines = []
    updated = False

    for line in read_file_lines(USER_FILE):
        stored_username, _, role = line.strip().split(",")
        if stored_username == username:
            updated_lines.append(f"{username},{new_full_name},{role}\n")
            updated = True
        else:
            updated_lines.append(line)

    if updated:
        return write_file_lines(USER_FILE, updated_lines)
    return False
