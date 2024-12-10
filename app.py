from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import MySQLdb.cursors
import os
import dotenv

dotenv.load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = SECRET_KEY

app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB

mysql = MySQL(app)

class User(UserMixin):
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def get_id(self):
        return self.email
    
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM users WHERE email = %s", [user_id])
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user['name'], user['email'], user['password'])
    return None

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/adopt', methods=['GET', 'POST'])
def adopt():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM adopt WHERE email = %s", [email])
        user = cur.fetchone()
        if user:
            try:
                cur.execute("INSERT INTO adopt (name, phone, address, email) VALUES (%s, %s, %s, %s)", (name, phone, address, email))      
                mysql.connection.commit()
                cur.close()
                flash("Thank you for your interest in adopting a pet!")
                return redirect('/adopt')
            except:
                flash("Sorry, we could not process your request. Please try again.")
                return redirect('/adopt')
        else:
            flash("User Not Found! Please register first.")
            return redirect('/register')
    return render_template('adopt.html')

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        amount = request.form['donation-amount']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO donations (email, amount) VALUES (%s, %s)", (current_user.email, amount))
        mysql.connection.commit()
        cur.close()
        flash("Thank you for your donation!")
        return redirect('/donate')
    return render_template('donate.html')

# Contact Page Route
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        purpose = request.form['purpose']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contact (name, email, purpose) VALUES (%s, %s, %s)", (name, email, purpose))
        mysql.connection.commit()
        cur.close()
        flash("Your message has been sent!")
        return redirect('/contact')
    return render_template('contact.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/dashboard')
@login_required
def dashboard():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM feedback where email = %s", [current_user.email])
    feedback = cur.fetchall()
    cur.execute("SELECT * FROM adopt where email = %s", [current_user.email])
    adopt = cur.fetchall()
    cur.execute("SELECT * FROM donations where email = %s", [current_user.email])
    donations = cur.fetchall()
    cur.execute("SELECT * FROM contact where email = %s", [current_user.email])
    contact = cur.fetchall()
    cur.close()
    return render_template('dashboard.html', feedback=feedback, adopt=adopt, donations=donations, contact=contact)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        if user:
            user = User(user['name'], user['email'], user['password'])
            login_user(user)
            return redirect('/')
        elif password != user['password']:
            flash("Invalid password!")
            return redirect('/login')
        else:
            flash("Invalid email!")
            return redirect('/login')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        user = cur.fetchone()
        if user:
            flash("User already exists! Please log in.")
            return redirect('/login')
        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect('/register')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
        mysql.connection.commit()
        cur.close()
        flash("Registration successful! Please log in.")
        return redirect('/login')
    return render_template('register.html')

# Feedback Route
@app.route('/feedback', methods=['POST'])
def feedback():
    name = request.form['name']
    email = request.form['email']
    feedback = request.form['feedback']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO feedback (name, email, feedback) VALUES (%s, %s, %s)", (name, email, feedback))
    mysql.connection.commit()
    cur.close()
    flash("Thank you for your feedback!")
    return redirect('/')

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        email = current_user.email
        new_password = request.form['new-password']
        confirm_password = request.form['confirm-password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        if new_password != confirm_password:
            flash("Passwords do not match!")
            return redirect('/change-password')
        cur.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, email))
        mysql.connection.commit()
        cur.close()
        flash("Password changed successfully!")
        return redirect('/dashboard')
    return render_template('change_password.html')

@app.route('/create')
def create_tables():
    cur = mysql.connection.cursor()
    cur.execute("SHOW TABLES")
    tables = cur.fetchall()
    table_names = [table[0] for table in tables]
    if 'feedback' not in table_names:
        cur.execute("CREATE TABLE feedback (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), feedback TEXT)")
    if 'adopt' not in table_names:
        cur.execute("CREATE TABLE adopt (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), phone VARCHAR(255), address VARCHAR(255), email VARCHAR(255)")
    if 'donations' not in table_names:
        cur.execute("CREATE TABLE donations (id INT AUTO_INCREMENT PRIMARY KEY, email VARCHAR(255), amount FLOAT)")
    if 'contact' not in table_names:
        cur.execute("CREATE TABLE contact (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), purpose TEXT)")
    if 'users' not in table_names:
        cur.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255), password VARCHAR(255))")
    mysql.connection.commit()
    cur.close()
    flash("Tables created successfully!")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)