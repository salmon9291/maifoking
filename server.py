from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os
from models import db, User, Message

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    session['username'] = username
    return redirect(url_for('chat'))

@app.route('/chat')
def chat():
    if 'username' in session:
        messages = Message.query.all()
        return render_template('chat.html', username=session['username'], messages=messages)
    return redirect(url_for('index'))

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' in session:
        username = session['username']
        message_content = request.form['message']
        user = User.query.filter_by(username=username).first()
        message = Message(content=message_content, user=user)
        db.session.add(message)
        db.session.commit()
    return redirect(url_for('chat'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)