from flask import Flask, render_template, request
from datetime import datetime
import csv, os, hashlib

app = Flask(__name__)

CSV_FILE = 'attendance.csv'
SECRET = 'my_super_secret_phrase'

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Time', 'Name', 'Student ID', 'IP Address'])

def get_current_code():
    from time import time
    slot = int(time() // 30)
    raw = f"{SECRET}-{slot}"
    return hashlib.sha256(raw.encode()).hexdigest()[:6].upper()

@app.route('/attendance')
def attendance_form():
    code = request.args.get('code')
    if code != get_current_code():
        return "Invalid or expired QR code.", 403
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    student_id = request.form.get('student_id')
    ip = request.remote_addr
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')

    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date_str, time_str, name, student_id, ip])

    return f"Thank you, {name}. Your attendance has been recorded."

if __name__ == '__main__':
    app.run()
