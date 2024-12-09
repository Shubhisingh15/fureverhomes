from flask import Flask, render_template, request, redirect, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key'

# MySQL Configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change to your MySQL username
app.config['MYSQL_PASSWORD'] = 'shu@15'  # Change to your MySQL password
app.config['MYSQL_DB'] = 'fureverhomes'

mysql = MySQL(app)

# Home Route
@app.route('/')
def home():
    return render_template("home.html")

# Adopt Page Route
@app.route('/adopt')
def adopt():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM dogs")
    dogs = cur.fetchall()
    cur.close()
    return render_template('adopt.html', dogs=dogs)

# Donate Page Route
@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        amount = request.form['donation-amount']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO donations (amount) VALUES (%s)", [amount])
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

# Login Route
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
            flash("Login successful!")
            return redirect('/')
        else:
            flash("Invalid email or password.")
            return redirect('/login')
    return render_template('login.html')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

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

# Main Function
if __name__ == '__main__':
    app.run(debug=True)
