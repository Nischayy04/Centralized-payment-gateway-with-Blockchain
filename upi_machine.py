# import socket
# import threading
# import qrcode
# from PIL import Image, ImageTk
# import tkinter as tk
# import os

# # --- Merchant Setup ---
# merchant_id = "MERCHANT12345"

# qr_window = None
# qr_filename = "merchant_qr.png"

# def generate_qr(mid):
#     global qr_window
#     qr = qrcode.QRCode(version=1, box_size=10, border=5)
#     qr.add_data(mid)
#     qr.make(fit=True)
#     img = qr.make_image(fill="black", back_color="white")
#     img.save(qr_filename)
#     print("[QR] Merchant QR code generated and saved as 'merchant_qr.png'.")

#     # Display QR in a centered window
#     def show_qr():
#         global qr_window
#         qr_window = tk.Tk()
#         qr_window.title("Merchant QR Code")

#         image = Image.open(qr_filename)
#         photo = ImageTk.PhotoImage(image)

#         w, h = image.size
#         sw = qr_window.winfo_screenwidth()
#         sh = qr_window.winfo_screenheight()
#         x = (sw - w) // 2
#         y = (sh - h) // 2
#         qr_window.geometry(f"{w}x{h}+{x}+{y}")

#         label = tk.Label(qr_window, image=photo)
#         label.image = photo  # Keep reference
#         label.pack()

#         qr_window.mainloop()

#     threading.Thread(target=show_qr, daemon=True).start()

# # --- Server Setup ---
# HOST = '0.0.0.0'
# PORT = 5000
# BANK_IP = '192.168.137.30'  # Replace with actual bank IP
# BANK_PORT = 6000

# def handle_client(conn, addr):
#     global qr_window
#     print(f"[+] New connection from {addr}")
#     data = conn.recv(4096).decode()
#     print(f"[DATA from {addr}] {data}")

#     if data.startswith("USER:"):
#         generate_qr(merchant_id)
#         \
#         try:
#             bank_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             bank_socket.connect((BANK_IP, BANK_PORT))
#             bank_socket.send(data.encode())
#             response = bank_socket.recv(4096).decode()
#             conn.send(response.encode())
#             bank_socket.close()

#             # Close QR window and delete image
#             if qr_window is not None:
#                 qr_window.quit()
#                 qr_window = None
#             if os.path.exists(qr_filename):
#                 os.remove(qr_filename)
#                 print("[QR] QR code window closed and image deleted.")

#         except Exception as e:
#             print("[ERROR] Bank connection failed:", e)
#             conn.send(b"ERROR: Unable to connect to bank.")
#     conn.close()

# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((HOST, PORT))
# server.listen()

# print(f"[SERVER] UPI Machine listening on {HOST}:{PORT}")

# while True:
#     conn, addr = server.accept()
#     thread = threading.Thread(target=handle_client, args=(conn, addr))
#     thread.start()

# import socket
# import threading
# import qrcode
# from PIL import Image, ImageTk
# import tkinter as tk
# import os

# qr_window = None
# qr_filename = "merchant_qr.png"

# # --- QR Generation ---
# def generate_qr(mid):
#     global qr_window
#     qr = qrcode.QRCode(version=1, box_size=10, border=5)
#     qr.add_data(mid)
#     qr.make(fit=True)
#     img = qr.make_image(fill="black", back_color="white")
#     img.save(qr_filename)
#     print("[QR] QR code generated for:", mid)

#     def show_qr():
#         global qr_window
#         qr_window = tk.Tk()
#         qr_window.title("Merchant QR Code")

#         image = Image.open(qr_filename)
#         photo = ImageTk.PhotoImage(image)

#         w, h = image.size
#         sw = qr_window.winfo_screenwidth()
#         sh = qr_window.winfo_screenheight()
#         x = (sw - w) // 2
#         y = (sh - h) // 2
#         qr_window.geometry(f"{w}x{h}+{x}+{y}")

#         label = tk.Label(qr_window, image=photo)
#         label.image = photo
#         label.pack()

#         qr_window.mainloop()

#     threading.Thread(target=show_qr, daemon=True).start()

# # --- Server Setup ---
# HOST = '0.0.0.0'
# PORT = 5000
# BANK_IP = '192.168.137.30'  # Replace with actual bank IP
# BANK_PORT = 6000

# # def handle_transaction(merchant_id):
# #     generate_qr(merchant_id)

# #     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #     server.bind((HOST, PORT))
# #     server.listen(1)
# #     print(f"[UPI MACHINE] Waiting for user device on {HOST}:{PORT}...")

# #     conn, addr = server.accept()
# #     print(f"[+] Connected to user at {addr}")

# #     data = conn.recv(4096).decode()
# #     print(f"[DATA from {addr}] {data}")

# #     if data.startswith("USER:"):
# #         try:
# #             bank_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #             bank_socket.connect((BANK_IP, BANK_PORT))
# #             bank_socket.send(data.encode())
# #             response = bank_socket.recv(4096).decode()
# #             conn.send(response.encode())
# #             bank_socket.close()

# #             # Close QR window and delete image
# #             global qr_window
# #             if qr_window:
# #                 qr_window.quit()
# #                 qr_window = None
# #             if os.path.exists(qr_filename):
# #                 os.remove(qr_filename)
# #                 print("[QR] Closed QR window and deleted image.")
# #         except Exception as e:
# #             print("[ERROR] Could not contact bank:", e)
# #             conn.send(b"ERROR: Bank connection failed.")
# #     conn.close()
# #     server.close()

# def handle_transaction_loop():
#     global qr_window

#     while True:
#         mid = input("\nEnter Merchant ID for this transaction (or type 'exit' to quit): ").strip()
#         if mid.lower() == "exit":
#             print("[UPI MACHINE] Shutting down transaction loop.")
#             break

#         # Generate and show QR
#         generate_qr(mid)

#         try:
#             # Wait for USER connection
#             print("[UPI MACHINE] Waiting for user to connect on port 5000...")
#             user_conn, user_addr = server.accept()
#             print(f"[USER CONNECTED] From {user_addr}")
#             user_data = user_conn.recv(4096).decode()
#             print(f"[DATA from USER] {user_data}")

#             # Wait for BANK connection
#             bank_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             bank_socket.bind(('0.0.0.0', 7000))
#             bank_socket.listen(1)
#             print("[UPI MACHINE] Waiting for bank to connect on port 7000...")

#             bank_conn, bank_addr = bank_socket.accept()
#             print(f"[BANK CONNECTED] From {bank_addr}")

#             bank_conn.send(user_data.encode())
#             response = bank_conn.recv(4096).decode()
#             print(f"[BANK RESPONSE] {response}")

#             user_conn.send(response.encode())

#             # Close connections
#             user_conn.close()
#             bank_conn.close()
#             bank_socket.close()

#         except Exception as e:
#             print("[ERROR] Transaction failed:", e)

#         # Cleanup QR
#         if qr_window is not None:
#             qr_window.quit()
#             qr_window = None
#         if os.path.exists(qr_filename):
#             os.remove(qr_filename)
#             print("[QR] QR code window closed and image deleted.")


# handle_transaction_loop()

import socket
import time
import threading
import qrcode
from PIL import Image, ImageTk
import tkinter as tk
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

qr_window = None
qr_filename = "merchant_qr.png"

def load_upi_private_key():
    with open("upi_private.pem", "rb") as f:
        private_key = RSA.import_key(f.read())
    return PKCS1_OAEP.new(private_key)

def load_bank_public_key():
    with open("bank_public.pem", "rb") as f:
        key = RSA.import_key(f.read())
    return PKCS1_OAEP.new(key)

def rol(x, r, n_bits=64):
    """Rotate left operation for 64-bit word size"""
    return ((x << r) | (x >> (n_bits - r))) & ((1 << n_bits) - 1)

def ror(x, r, n_bits=64):
    """Rotate right operation for 64-bit word size"""
    return ((x >> r) | (x << (n_bits - r))) & ((1 << n_bits) - 1)

def encrypt_mid(mid):
    
    # Generate timestamp for key derivation
    timestamp = int(time.time())
    
    # Create key using timestamp - 16 bytes for 64-bit word size (2 words)
    key = f"UPI{timestamp}KEY".ljust(16)
    
    # Take up to 16 characters of MID (128 bits) for 64-bit word size
    mid_truncated = mid[:16].ljust(16)  # Pad to 16 bytes if needed
    
    # Encrypt using SPECK cipher with 64-bit word size
    word_size = 64
    rounds = 27  # Standard rounds for Speck64/128
    
    # Convert key to bytes if it's a string
    if isinstance(key, str):
        key = key.encode('utf-8')
    
    # Convert plaintext to bytes if it's a string
    if isinstance(mid_truncated, str):
        mid_truncated = mid_truncated.encode('utf-8')
    
    # Generate round keys - for 64-bit word size, 16-byte key
    key_int = int.from_bytes(key, byteorder='little')
    k = [(key_int >> (64 * i)) & ((1 << 64) - 1) for i in range(2)]
    l = k[1:]  # [k1]  # noqa: E741
    round_keys = [k[0]]  # Start with k0
    
    for i in range(rounds - 1):
        l[0] = (ror(l[0], 8, word_size) + round_keys[i]) % (1 << word_size) ^ i
        round_keys.append(l[0])
        # Note: With only 2 key words, we don't need to rotate l
    
    # Encrypt plaintext with 64-bit word size
    plaintext_int = int.from_bytes(mid_truncated, byteorder='little')
    b = plaintext_int & ((1 << 64) - 1)          # Lower 64 bits
    a = (plaintext_int >> 64) & ((1 << 64) - 1)  # Upper 64 bits
    
    # Apply encryption rounds
    for i in range(rounds):
        a = (ror(a, 8, word_size) + b) % (1 << word_size) ^ round_keys[i]
        b = rol(b, 3, word_size) ^ a
    
    # Combine the two parts
    result = (a << 64) | b
    
    # Convert to hex string
    vmid = result.to_bytes(16, byteorder='little').hex()
    
    return {"vmid": vmid, "timestamp": timestamp}

# --- QR Generation ---
def generate_qr(mid):
    global qr_window
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(mid)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save(qr_filename)
    print("[QR] QR code generated for:", mid)

    def show_qr():
        try:
            global qr_window
            qr_window = tk.Tk()
            qr_window.title("Merchant QR Code")

            image = Image.open(qr_filename)
            photo = ImageTk.PhotoImage(image)

            label = tk.Label(qr_window, image=photo)
            label.image = photo
            label.pack()

            qr_window.update_idletasks()

            w, h = image.size
            sw = qr_window.winfo_screenwidth()
            sh = qr_window.winfo_screenheight()
            x = (sw - w) // 2
            y = (sh - h) // 2
            qr_window.geometry(f"{w}x{h}+{x}+{y}")

            qr_window.mainloop()
        except Exception as e:
            print("[QR ERROR]", e)


    threading.Thread(target=show_qr).start()

# --- Server Setup ---
HOST = '0.0.0.0'
PORT = 5000
BANK_PORT = 7000

def handle_transaction_loop():
    global qr_window

    while True:
        mid = input("\nEnter Merchant ID for this transaction (or type 'exit' to quit): ").strip()
        if mid.lower() == "exit":
            print("[UPI MACHINE] Shutting down transaction loop.")
            break

        vmid = encrypt_mid(mid)

        vmid_only = vmid['vmid']

        # Generate and show QR
        generate_qr(vmid_only)

        try:
            # Create socket to accept USER connection
            user_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            user_socket.bind((HOST, PORT))
            user_socket.listen(1)
            print("[UPI MACHINE] Waiting for user to connect on port 5000...")
            user_conn, user_addr = user_socket.accept()
            print(f"[USER CONNECTED] From {user_addr}")
            user_data = user_conn.recv(4096)
            print(f"[DATA from USER] {user_data}")
            user_socket.close()

            upi_cipher = load_upi_private_key()
            decrypted_data = upi_cipher.decrypt(user_data).decode()
            #print("[UPI MACHINE] Decrypted raw message:", decrypted_data)


            #message_part, timestamp = decrypted_data.split("|", 1)

            #decrypted_message = decrypt_vmid(message_part, timestamp)
            #print("[UPI MACHINE] Decrypted message:", decrypted_message)
            #print("[UPI MACHINE] Timestamp:", timestamp)

            parts = decrypted_data.split(";")
            mmid = [p for p in parts if p.startswith("MMID=")][0].split("=")[1]
            pin = [p for p in parts if p.startswith("PIN=")][0].split("=")[1]
            amount = [p for p in parts if p.startswith("AMOUNT=")][0].split("=")[1]
            qr_field = [p for p in parts if p.startswith("QR=")][0].split("=")[1]

            #print("The vmid is:" , vmid['vmid'])
            #print("The qr_data is:" , qr_field)

            if qr_field==vmid['vmid']:
                print("[UPI MACHINE] QR code verified successfully.")

                # Create socket to accept BANK connection
                bank_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                bank_socket.bind((HOST, BANK_PORT))
                bank_socket.listen(1)

                print("[UPI MACHINE] Waiting for bank to connect on port 7000...")
                bank_conn, bank_addr = bank_socket.accept()
                print(f"[BANK CONNECTED] From {bank_addr}")

                bank_message = f"{mmid};{pin};{amount};{mid}"

                bank_cipher = load_bank_public_key()
                encrypted_data = bank_cipher.encrypt(bank_message.encode())

                # Forward to bank and get response
                bank_conn.send(encrypted_data)
                response = bank_conn.recv(4096).decode()
                print(f"[BANK RESPONSE] {response}")
                bank_conn.close()
                bank_socket.close()

                # Send response to user
                user_conn.send(response.encode())
                user_conn.close()
            else:
                print("[UPI MACHINE] QR code verification failed.")
                user_conn.send(b"ERROR: QR code verification failed.")
                user_conn.close()

        except Exception as e:
            print("[ERROR] Transaction failed:", e)

        # Cleanup QR
        if qr_window is not None:
            qr_window.quit()
            qr_window = None
        if os.path.exists(qr_filename):
            os.remove(qr_filename)
            print("[QR] QR code window closed and image deleted.")

# --- Start ---
handle_transaction_loop()

