from flask import Flask, render_template, request, redirect, url_for, send_file, flash, abort
from crypto.file_crypto import encrypt_file, decrypt_file
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import os, uuid, json
from datetime import datetime

app = Flask(__name__)
app.secret_key = "InterneeSecureFileKey2026"

STORAGE_DIR = "storage/encrypted_files"
METADATA_FILE = "storage/metadata.json"
SIGNED_URL_SECRET = "SignedURLSecret2026"
serializer = URLSafeTimedSerializer(SIGNED_URL_SECRET)

# Load/save metadata
def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_metadata(data):
    with open(METADATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        flash("No file selected!", "danger")
        return redirect(url_for("index"))
    file = request.files["file"]
    if file.filename == "":
        flash("No file selected!", "danger")
        return redirect(url_for("index"))

    # Generate unique file ID
    file_id = str(uuid.uuid4())
    original_name = file.filename
    file_data = file.read()

    # Encrypt the file
    encrypted_data = encrypt_file(file_data)
    encrypted_path = os.path.join(STORAGE_DIR, file_id + ".enc")
    with open(encrypted_path, "wb") as f:
        f.write(encrypted_data)

    # Save metadata
    metadata = load_metadata()
    metadata[file_id] = {
        "original_name": original_name,
        "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "size": len(file_data),
        "encrypted": True
    }
    save_metadata(metadata)

    flash(f"File '{original_name}' uploaded and encrypted successfully!", "success")
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    metadata = load_metadata()
    return render_template("dashboard.html", files=metadata)

@app.route("/generate-link/<file_id>")
def generate_link(file_id):
    metadata = load_metadata()
    if file_id not in metadata:
        abort(404)
    # Generate signed URL (expires in 1 hour)
    token = serializer.dumps(file_id)
    signed_url = url_for("secure_download", token=token, _external=True)
    return render_template("download.html",
                           signed_url=signed_url,
                           filename=metadata[file_id]["original_name"])

@app.route("/download/<token>")
def secure_download(token):
    try:
        file_id = serializer.loads(token, max_age=3600)  # 1 hour expiry
    except SignatureExpired:
        abort(403, description="Link has expired!")
    except BadSignature:
        abort(403, description="Invalid link!")

    metadata = load_metadata()
    if file_id not in metadata:
        abort(404)

    encrypted_path = os.path.join(STORAGE_DIR, file_id + ".enc")
    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()

    # Decrypt file
    decrypted_data = decrypt_file(encrypted_data)
    original_name = metadata[file_id]["original_name"]

    # Save temp decrypted file
    temp_path = os.path.join(STORAGE_DIR, "temp_" + original_name)
    with open(temp_path, "wb") as f:
        f.write(decrypted_data)

    return send_file(temp_path, as_attachment=True, download_name=original_name)

if __name__ == "__main__":
    app.run(debug=True)