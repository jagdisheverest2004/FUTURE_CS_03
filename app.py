from flask import Flask, request, render_template, send_file
from encryption import encrypt_file, decrypt_file
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
TEMP_FOLDER = "temp"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return "No file selected."

    data = uploaded_file.read()
    encrypted_data = encrypt_file(data)
    unique_filename = uploaded_file.filename + ".enc"
    encrypted_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    with open(encrypted_path, 'wb') as f:
        f.write(encrypted_data)

    return f"File uploaded and encrypted as {unique_filename}"

@app.route('/download/<filename>')
def download(filename):
    encrypted_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(encrypted_path):
        return "Encrypted file not found."

    with open(encrypted_path, 'rb') as f:
        encrypted_data = f.read()

    decrypted_data = decrypt_file(encrypted_data)

    temp_path = os.path.join(TEMP_FOLDER, filename.replace(".enc", ""))
    with open(temp_path, 'wb') as f:
        f.write(decrypted_data)

    return send_file(temp_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
