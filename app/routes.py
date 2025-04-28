from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, current_app, send_from_directory, session
)
import os
from werkzeug.utils import secure_filename
from web3 import Web3

from models import insert_history, fetch_history
from app.utils import process_image
from model.federated_model import predict_image

main = Blueprint('main', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(fn: str) -> bool:
    return '.' in fn and fn.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/', methods=['GET', 'POST'])
def index():
    if 'wallet' not in session:
        flash("Please login to continue.", "error")
        return redirect(url_for("main.login"))

    if request.method == 'POST' and 'image' in request.files:
        file = request.files['image']
        image_type = request.form.get('image_type')
        print("📤 Uploaded file:", file.filename)

        if file.filename == '' or not allowed_file(file.filename):
            flash('Select a valid image file (png/jpg/jpeg)', 'error')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        patient_addr = request.form.get('patient_address') or "0x0000000000000000000000000000000000000000"
        patient_addr = Web3.toChecksumAddress(patient_addr)

        try:
            image_tensor = process_image(filepath, patient_addr)
            prediction, confidence = predict_image(image_tensor, image_type)

            wallet_address = session.get("wallet")
            insert_history(filename, prediction, confidence, wallet_address, image_type)

            return render_template(
                'index.html',
                prediction=prediction,
                confidence=confidence,
                filename=filename,
                image_type=image_type
            )
        except Exception as e:
            print("❌ Prediction failed:", str(e))
            flash("Error during prediction. Please try again.", "error")
            return redirect(url_for("main.index"))

    return render_template('index.html')

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main.route("/history")
def history():
    wallet = session.get("wallet")
    if not wallet:
        flash("Please login to view history.", "error")
        return redirect(url_for("main.login"))

    rows = fetch_history(wallet)
    history_logs = [
        {
            "timestamp": row[0],
            "filename": row[1],
            "prediction": row[2],
            "confidence": row[3],
            "image_type": row[4] if len(row) > 4 else "Unknown"
        } for row in rows
    ]
    return render_template("history.html", history_logs=history_logs)

@main.route("/project")
def project():
    return render_template("project.html")

# ✅ Updated login route to accept POST for MetaMask connect
@main.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        wallet = request.form.get("wallet_address")
        if wallet:
            session["wallet"] = wallet
            flash("Wallet connected successfully!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Wallet connection failed.", "error")
    return render_template("login.html")

@main.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        org_name = request.form.get("org_name")
        wallet = request.form.get("wallet_address")

        if org_name and wallet:
            session["org_name"] = org_name
            session["wallet"] = wallet
            flash("Successfully signed up!", "success")
            return redirect(url_for("main.index"))
        else:
            flash("Please provide all required fields.", "error")

    return render_template("signup.html")


@main.route("/logout")
def logout():
    session.pop("wallet", None)
    session.pop("org_name", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("main.login"))

@main.route("/download/report")
def download_report():
    return send_from_directory(directory="static", path="project_report.pdf", as_attachment=True)
