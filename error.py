import socket
import sys
import time

delay = sys.argv[1]
iface = sys.argv[2]
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
s.bind(("wlp2s0", 0))
while True:
    src_addr = b"\x01\x02\x03\x04\x05\x06"
    dst_addr = b"\x01\x02\x03\x04\x05\x06"
    payload = (b"[" * 30) + b"PAYLOAD" + (b"]" * 30)
    checksum = b"\x00\x00\x00\x00"
    ethertype = b"\x08\x01"
    s.send (dst_addr+src_addr+ethertype+payload+checksum)
    time.sleep (delay)