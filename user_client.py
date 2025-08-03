import socket
import cv2
from pyzbar.pyzbar import decode
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def load_upi_public_key():
    with open("upi_public.pem", "rb") as f:
        key = RSA.import_key(f.read())
    return PKCS1_OAEP.new(key)

# --- Configuration ---
upi_ip = '192.168.191.170'  # IP address of the UPI machine
upi_port = 5000           # Port the UPI machine is listening on

# --- QR Scanner ---
def scan_qr_code():
    cap = cv2.VideoCapture(0)
    decoded_data = None

    print("Opening camera. Scan the merchant's QR code. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        for barcode in decode(frame):
            decoded_data = barcode.data.decode('utf-8')
            print("QR Code Data:", decoded_data)
            cap.release()
            cv2.destroyAllWindows()
            return decoded_data

        cv2.imshow("QR Scanner - Press 'q' to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return None

# --- Main Workflow ---
def main():
    qr_data = scan_qr_code()
    if not qr_data:
        print("No QR code scanned. Exiting.")
        return

    try:
        # Connect to UPI machine
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((upi_ip, upi_port))
        print("Connected to UPI Machine.")

        print("The vmid read from qr code is:", qr_data)

        # User inputs
        mmid = input("Enter your MMID: ").strip()
        pin = input("Enter your PIN: ").strip()
        amount = input("Enter amount to pay: ").strip()

        # Construct message
        message = f"MMID={mmid};PIN={pin};AMOUNT={amount};QR={qr_data}"
        #message_encoded = encrypt_mid(message)
        #timestamp = message_encoded["timestamp"]
        #message_send = message_encoded["vmid"]

        #final_message = f"{message_send}|{timestamp}"

        cipher = load_upi_public_key()
        encrypted_data = cipher.encrypt(message.encode())


        sock.send(encrypted_data)

        # Get response
        response = sock.recv(4096).decode()
        print("Transaction status from UPI Machine:", response)

    except Exception as e:
        print("Failed to complete transaction:", e)

    finally:
        sock.close()

# --- Run ---
if __name__ == "__main__":
    main()


