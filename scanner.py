import cv2
from pyzbar.pyzbar import decode

def scan_qr_code():
    cap = cv2.VideoCapture(0)
    decoded_data = None

    print("Opening camera. Press 'q' to quit after scanning.")

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

# --- Usage ---
data = scan_qr_code()
if data:
    print("Scanned QR Code Data stored in variable 'data':", data)
else:
    print("No QR code scanned.")
