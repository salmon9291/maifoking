from flask import Flask, send_from_directory, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/styles.css')
def styles():
    return send_from_directory(os.getcwd(), 'styles.css')

@app.route('/scripts.js')
def scripts():
    return send_from_directory(os.getcwd(), 'scripts.js')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)