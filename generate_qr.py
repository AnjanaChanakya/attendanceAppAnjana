import qrcode, hashlib
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
import time

SECRET = 'my_super_secret_phrase'
SERVER_URL = 'https://your-render-app-url.onrender.com'  # Replace this

def get_current_code():
    slot = int(datetime.now().timestamp() // 30)
    raw = f"{SECRET}-{slot}"
    return hashlib.sha256(raw.encode()).hexdigest()[:6].upper()

def start_qr_gui():
    root = tk.Tk()
    root.title("Live QR Code")
    label = tk.Label(root)
    label.pack(padx=10, pady=10)

    def update_qr():
        code = get_current_code()
        url = f"{SERVER_URL}/attendance?code={code}"
        img = qrcode.make(url)
        img.save("temp_qr.png")
        image = Image.open("temp_qr.png")
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo
        root.after(5000, update_qr)

    update_qr()
    root.mainloop()

if __name__ == "__main__":
    start_qr_gui()
