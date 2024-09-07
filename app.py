from flask import Flask, render_template, request, redirect, jsonify, url_for
import sqlite3
import asyncio

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()

    # Create the 'users' table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, username TEXT, password TEXT, address TEXT, profession TEXT)''')
    conn.commit()
    conn.close()

# Route to render the signup page
@app.route('/')
def signup_page():
    return render_template('signup.html')

# Route to render the login page
@app.route('/login')
def login_page():
    return render_template('login.html')

# Route to render the doctor page
@app.route('/doctor')
def doctor_page():
    return render_template('doctor.html')

# Route to handle the signup form submission
@app.route('/signup', methods=['POST'])
def signup_user():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    address = request.form['address']
    profession = request.form['profession']
    if "@" in username:
    # Insert into the users table
        conn = sqlite3.connect('user_data.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, username, password, address, profession) VALUES (?, ?, ?, ?, ?)",
              (name, username, password, address, profession))
        conn.commit()
        conn.close()
    
        return redirect('http://127.0.0.1:5000/login')
    else:
        print("Invalid credentials")  # Debugging output
        return jsonify({"success": False, "message": "Invalid credentials"})
    
    
   

# Route to handle the login form submission asynchronously
@app.route('/login', methods=['POST'])
async def login_user():
    username = request.form['username']
    password = request.form['password']
    
    # Check credentials in the database
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("SELECT profession FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    conn.close()
 
    if result:
        profession = result[0].lower()  # Make it lowercase to handle case sensitivity
        print(f"Profession found: {profession}")  # Debugging output
        if profession == 'doctor':
            # Redirect to the 'doctor' page if the profession is 'doctor'
            return redirect(url_for('doctor_page'))
        else:
            return jsonify({"success": True, "profession": profession})
    else:
        print("Invalid credentials")  # Debugging output
        return jsonify({"success": False, "message": "Invalid credentials"})

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
