import socket

s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
s.bind(("lo", 0))
src_addr = b"\x01\x02\x03\x04\x05\x06"
dst_addr = b"\x01\x02\x03\x04\x05\x06"
payload = (b"[" * 30) + b"PAYLOAD" + (b"]" * 30)
checksum = b"\x00\x00\x00\x00"
ethertype = b"\x08\x01"
s.send (dst_addr+src_addr+ethertype+payload+checksum)