import tkinter as tk
from PIL import Image, ImageTk
import qrcode

qr = qrcode.make("test_merchant_123")
qr.save("test_qr.png")

def show_qr():
    win = tk.Tk()
    win.title("Test QR")

    img = Image.open("test_qr.png")
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(win, image=photo)
    label.image = photo
    label.pack()

    win.mainloop()

show_qr()
