from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os
from models import db, User, Message
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
app.config['ALLOWED_EXTENSIONS'] = set(os.getenv('ALLOWED_EXTENSIONS').split(','))

db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)  # Agregar esta línea

with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if 'profile_pic' not in request.files:
            return "No file part"
        file = request.files['profile_pic']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(username=username, password=hashed_password, profile_pic=filename)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' in session:
        return render_template('chat.html', username=session['username'])
    return redirect(url_for('index'))

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'username' in session:
        username = session['username']
        message_content = request.form['message']
        user = User.query.filter_by(username=username).first()
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                message = Message(content=filename, user=user, is_file=True)
            else:
                return "File not allowed"
        else:
            message = Message(content=message_content, user=user)
        db.session.add(message)
        db.session.commit()
    return '', 204

@app.route('/get_messages')
def get_messages():
    messages = Message.query.all()
    messages_list = [{'username': message.user.username, 'content': message.content, 'is_file': message.is_file} for message in messages]
    return jsonify(messages_list)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)