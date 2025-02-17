from flask import Flask, render_template, request, redirect, url_for, session
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Lista para almacenar mensajes de chat
messages = []

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    session['username'] = username
    return redirect(url_for('chat'))

@app.route('/chat')
def chat():
    if 'username' in session:
        return render_template('chat.html', username=session['username'], messages=messages)
    return redirect(url_for('index'))

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' in session:
        username = session['username']
        message = request.form['message']
        messages.append({'username': username, 'message': message})
    return redirect(url_for('chat'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)