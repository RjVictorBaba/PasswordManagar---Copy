from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from encryption import encrypt_password, decrypt_password
from models import db, User, SavedPassword  # ✅ Models import karein

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)  
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# 🔹 Database ko initialize karein
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    saved_passwords = SavedPassword.query.filter_by(user_id=user_id).all()

    if request.method == 'POST':
        website = request.form['website']
        username = request.form['username']
        password = request.form['password']
        encrypted_password = encrypt_password(password)
        
        new_entry = SavedPassword(
            user_id=user_id,
            website=website,
            username=username,
            encrypted_password=encrypted_password
        )
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('dashboard'))

    for entry in saved_passwords:
        entry.encrypted_password = decrypt_password(entry.encrypted_password)

    return render_template('dashboard.html', passwords=saved_passwords)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
