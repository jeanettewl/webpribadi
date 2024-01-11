from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DATABASE = 'users.db'

def create_table():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pengguna (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                full name TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()

def insert_user(username, password):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        hashed_password = generate_password_hash(password, method='sha256')
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()

def get_user(username):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return cursor.fetchone()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        insert_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if user and check_password_hash(user[2], password):
            # Implement session management or other login logic here
            return "Login Successful!"
        else:
            return "Login Failed. Please check your username and password."
    return render_template('login.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
def home():
    # Simulasi daftar produk
    products = [
        {'id': 1, 'name': 'Product 1', 'price': 20.0},
        {'id': 2, 'name': 'Product 2', 'price': 30.0},
        {'id': 3, 'name': 'Product 3', 'price': 25.0},
    ]
    return render_template('home.html', products=products)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
