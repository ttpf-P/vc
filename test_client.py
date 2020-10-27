import socket
s=socket.socket()
s.connect(("127.0.0.1",12345))
s.send(b"00000004\x00GARBAGE1234")
s.close()
