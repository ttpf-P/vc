import socket
s=socket.socket()
s.connect(("127.0.0.1",12345))
s.sendall(b"00002024\x00GARBAGE"+b"1"*2024)
s.close()
