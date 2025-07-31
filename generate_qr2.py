import qrcode
import hashlib
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk

SECRET = 'my_super_secret_phrase'
SERVER_URL = 'http://172.19.2.165:5000/attendance'  # ← Point this to app.py server
CODE_DURATION = 30  # seconds

def get_current_code():
    now = datetime.now()
    time_slot = int(now.timestamp() // CODE_DURATION)
    raw = f"{SECRET}-{time_slot}"
    return hashlib.sha256(raw.encode()).hexdigest()[:6].upper()

def start_qr_gui():
    root = tk.Tk()
    root.title("Live QR Code")
    label = tk.Label(root)
    label.pack(padx=10, pady=10)

    def update_qr():
        code = get_current_code()
        url = f"{SERVER_URL}?code={code}"
        img = qrcode.make(url)
        img.save("temp_qr.png")

        image = Image.open("temp_qr.png")
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo

        root.after(5000, update_qr)  # Refresh QR every 5 sec

    update_qr()
    root.mainloop()

if __name__ == '__main__':
    start_qr_gui()
