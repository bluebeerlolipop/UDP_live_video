import socket
import cv2

UDP_IP = '127.0.0.1'
UDP_PORT = 9505

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Fail to open Camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Fail to read Frame")
        break

    frame = cv2.resize(frame, (320, 240))  # frame size
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]  # quality 조절
    result, encimg = cv2.imencode('.jpg', frame, encode_param)

    if not result:
        print("JPEG encoding fail")
        continue

    data = encimg.tobytes()

    # size 분할
    max_packet_size = 4096
    total_packets = len(data) // max_packet_size + 1
    sock.sendto(str(total_packets).encode(), (UDP_IP, UDP_PORT))

    for i in range(total_packets):
        part = data[i*max_packet_size:(i+1)*max_packet_size]
        sock.sendto(part, (UDP_IP, UDP_PORT))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
