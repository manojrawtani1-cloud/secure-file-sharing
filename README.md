# 📁 Secure File Sharing System
### Internee.pk Cybersecurity Internship - Task 04

## 📌 Objective
Ensure secure file exchanges between Internee.pk and external parties.

## ✅ Features Implemented
- **AES-256 Encryption** — Files encrypted before storage
- **Signed URLs** — Time-limited secure download links (1-hour expiry)
- **Secure Upload & Download** — End-to-end encrypted file transfer
- **File Management Dashboard** — Track all uploaded encrypted files

## 🛠️ Tools & Technologies
| Tool | Purpose |
|------|---------|
| Python + Flask | Web framework |
| PyCryptodome | AES-256 file encryption |
| itsdangerous | Signed URL generation |
| Kaggle Datasets | Test data source |

## 📁 Project Structure
secure-file-sharing/

├── app.py                      # Main Flask application

├── crypto/

│   └── file_crypto.py          # AES-256 encryption/decryption

├── storage/

│   └── encrypted_files/        # Encrypted file storage

├── templates/

│   ├── index.html              # Upload page

│   ├── dashboard.html          # File management dashboard

│   └── download.html           # Secure download page

└── README.md

## 🚀 How to Run
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate`
4. Install dependencies: `pip install flask pycryptodome itsdangerous`
5. Run: `python app.py`
6. Open browser: `http://127.0.0.1:5000`

## 🔐 Security Implementation Details
- Files encrypted using AES-256-CBC before being stored on disk
- Signed URLs generated using HMAC-based token signing
- Download links expire after 1 hour automatically
- Files decrypted only at the moment of download

## 📸 Screenshots
See `/screenshots` folder for system demonstration.

## 👨‍💻 Author
**Manoj** - Telecommunication Engineering Student
Mehran University of Engineering & Technology (MUET)
Internee.pk Cybersecurity Internship - 2026
