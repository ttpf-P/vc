import socket
import concurrent.futures as cf
import selectors
import time
import types

#events = selectors.EVENT_READ | selectors.EVENT_WRITE
events = selectors.EVENT_READ

s = socket.socket()
s.bind(("",12345))
s.listen()
s.setblocking(False)

sel = selectors.DefaultSelector()
sel.register(s, selectors.EVENT_READ, data=None)

addr_list = {}


ID=0


def accept(sock):
    global ID
    conn, addr = sock.accept()
    print("addr:"+str(addr))
    conn.setblocking(False)
    data_cont=types.SimpleNamespace(auth="NOAUTH",ID=ID)
    addr_list[ID]=(conn,data_cont)
    ID+=1
    sel.register(conn, events, data=data_cont)

def black_magic(key, mask):
    print("key: "+str(key))
    print("mask: "+str(mask))
    conn = key.fileobj
    if mask & selectors.EVENT_READ:
        data = conn.recv(1024)
        datalen = data[:8]
        datatype = data[8:16]
        print(datalen.decode(),datatype.decode())
        if datatype == b"" and not datalen == b"":
            print("closing connection "+ str(key.data.ID)+" due to bad health")
        #print(str(data))
        if data==b"":
            sel.unregister(conn)
            addr_list
    

while True:
    print("bis hier keine errors")
    events_ = sel.select()
    for key, mask in events_:
        if key.data is None:
            accept(key.fileobj)
        else:
            black_magic(key, mask)

