import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # For flash messages

# Paths for user data
USER_FILE = "data/users.txt"
PASS_FILE = "data/passwords.txt"

class User:
    def __init__(self, username, full_name, role, uni_id, section):
        self.username = username
        self.full_name = full_name
        self.role = role
        self.uni_id = uni_id
        self.section = section


def authenticate(username, password):
    """
    Authenticate user by checking against stored passwords.
    """
    try:
        with open(PASS_FILE, "r") as file:
            for line in file:
                stored_username, stored_password, role = line.strip().split(",")
                if username == stored_username and password == stored_password:
                    return role  # Return the role (admin or student)
    except FileNotFoundError:
        print("Error: passwords.txt file not found.")
    return None


def get_user_details(username):
    """
    Retrieve full name, role, uni_id, and section of a user.
    """
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                stored_username, full_name, role, uni_id, section = line.strip().split(",")
                if username == stored_username:
                    return User(username, full_name, role, uni_id, section)
    except FileNotFoundError:
        print("Error: users.txt file not found.")
    return None


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = authenticate(username, password)

        if role:
            # Successful login
            user_details = get_user_details(username)
            flash(f"Welcome {user_details.full_name} as {role}!", 'success')
            return redirect(url_for('dashboard', username=username, role=role, uni_id=user_details.uni_id, section=user_details.section))
        else:
            # Failed login
            flash("Invalid username or password. Please try again.", 'danger')
            return redirect(url_for('login'))
    
    return render_template('login.html')


from authenticator import get_student_grades  # Make sure this is at the top

from flask import Flask, render_template, request
from authenticator import get_student_grades  # Or any relevant imports for your project

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, Flask is running!'

@app.route('/dashboard')
def dashboard():
    username = request.args.get('username')
    role = request.args.get('role')
    uni_id = request.args.get('uni_id')
    section = request.args.get('section')

    grades = get_student_grades(username)
    eca = []  # Empty list for now (since no ECA file)

    return render_template(
        'dashboard.html',
        username=username,
        role=role,
        uni_id=uni_id,
        section=section,
        grades=grades,
        eca=eca
    )

if __name__ == '__main__':
    app.run(debug=True)
