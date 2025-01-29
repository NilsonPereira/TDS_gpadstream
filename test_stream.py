import socket
import numpy as np
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cnt = 0
address = "127.0.0.1"
port = 10123
time.sleep(1)

print("Sending UDP messages...")
while True:
    message = f"1,{cnt},{cnt+1},{cnt+2},{cnt+3},{cnt},{cnt},{cnt}\n"
    sock.sendto(message.encode(), (address, port))
    cnt += 1
    time.sleep(1)
sock.close()

