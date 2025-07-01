# 🔐 FUTURE\_CS\_03: Secure File Sharing System using Flask and AES Encryption (CBC)

A secure file sharing portal built with **Python Flask** and **AES encryption** to ensure file confidentiality during upload/download. This project simulates a **real-world secure data exchange system** used in healthcare, legal, and enterprise environments.

---

## ✅ Step-by-Step Implementation

### 🛠️ STEP 1: Project Initialization

```bash
mkdir FUTURE_CS_03 && cd FUTURE_CS_03
mkdir templates uploads temp
touch app.py encryption.py requirements.txt README.md
```

---

### 🐍 STEP 2: Set Up Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate   # For Linux/macOS
venv\Scripts\activate      # For Windows

pip install flask pycryptodome
```

Update your `requirements.txt`:

```
flask
pycryptodome
```

---

### 🔐 STEP 3: AES Encryption/Decryption Logic (`encryption.py`)

```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

KEY = b'ThisIsASecretKey'  # 16-byte key for AES-128

def pad(data):
    pad_len = AES.block_size - len(data) % AES.block_size
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt_file(data):
    iv = get_random_bytes(16)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(data))
    return iv + encrypted

def decrypt_file(encrypted):
    iv = encrypted[:16]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted[16:]))
```

---

### 🌐 STEP 4: Flask Backend Logic (`app.py`)

```python
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
    file = request.files['file']
    if file.filename == '':
        return "No file selected."
    data = file.read()
    encrypted = encrypt_file(data)
    encrypted_path = os.path.join(UPLOAD_FOLDER, file.filename + ".enc")
    with open(encrypted_path, 'wb') as f:
        f.write(encrypted)
    return f"File uploaded and encrypted as {file.filename}.enc"

@app.route('/download/<filename>')
def download(filename):
    encrypted_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(encrypted_path):
        return "File not found."
    with open(encrypted_path, 'rb') as f:
        encrypted_data = f.read()
    decrypted = decrypt_file(encrypted_data)
    temp_path = os.path.join(TEMP_FOLDER, filename.replace('.enc', ''))
    with open(temp_path, 'wb') as f:
        f.write(decrypted)
    return send_file(temp_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
```

---

### 🖼️ STEP 5: Web Interface (`templates/index.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🔐 Secure File Portal</title>
</head>
<body>
    <h2>Upload File</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <input type="submit" value="Encrypt and Upload">
    </form>

    <h2>Download File</h2>
    <form onsubmit="return redirectToDownload()">
        <input type="text" id="filename" placeholder="Enter filename.enc" required>
        <input type="submit" value="Download Decrypted File">
    </form>

    <script>
        function redirectToDownload() {
            const filename = document.getElementById("filename").value;
            window.location.href = "/download/" + filename;
            return false;
        }
    </script>
</body>
</html>
```

---

### ▶️ STEP 6: Run the Application

```bash
python app.py
```

Open in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔐 How the Encryption Works

* Uses **AES-128 (CBC mode)** with a static 16-byte key
* A **random IV (Initialization Vector)** is generated for every file
* The IV is **prepended to the ciphertext**
* During decryption, the IV is extracted and used to reconstruct the cipher

---

## 🧪 Test Scenarios

* ✅ Upload any file (e.g., `.txt`, `.pdf`, `.jpg`)
* ✅ Check `uploads/` for `.enc` encrypted files
* ✅ Download the file and confirm content accuracy
* ✅ Open the decrypted file and verify integrity

---

## 📦 Project Structure

```
FUTURE_CS_03/
├── app.py
├── encryption.py
├── templates/
│   └── index.html
├── uploads/        # Encrypted files
├── temp/           # Decrypted temp files
├── requirements.txt
└── README.md
```

---

## 📄 License

This project is developed as part of **Future Interns' internship program**. For educational use only. Commercial use without permission is prohibited.

---

Let me know if you'd like me to generate a `.env` key loader, login system, or deploy instructions for GitHub Pages + backend on Railway or Render!
