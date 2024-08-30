from flask import Flask, render_template, request, redirect
import sqlite3

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

# Route to handle the signup form submission
@app.route('/signup', methods=['POST'])
def signup_user():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    address = request.form['address']
    profession = request.form['profession']
    
    # Insert into the users table
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, username, password, address, profession) VALUES (?, ?, ?, ?, ?)",
              (name, username, password, address, profession))
    conn.commit()
    conn.close()
    
    return redirect('/')

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
