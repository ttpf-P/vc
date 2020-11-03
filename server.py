import socket
import concurrent.futures as cf
import selectors
import time
import types
import serverFiles.tcp.main as tcp

#events = selectors.EVENT_READ | selectors.EVENT_WRITE
events = selectors.EVENT_READ

s = socket.socket()
s.bind(("",12345))
s.listen()
s.setblocking(False)

#create selectors to look for read/writeability in sockets
sel = selectors.DefaultSelector()
sel.register(s, selectors.EVENT_READ, data=None)

addr_list = {}


ID=0


def accept(sock):
    global ID
    conn, addr = sock.accept()
    print("addr:"+str(addr))
    conn.setblocking(False)
    data_cont=types.SimpleNamespace(auth="0",ID=ID,message_len=0,message_type=b"")#creating data container
    addr_list[ID]=(conn,data_cont)
    ID+=1
    sel.register(conn, events, data=data_cont)#register connection with data container @ selector


def handle_tcp_data(data_processed):
    #print("bguaeifhueouf")
    print(len(data_processed))

def black_magic(key, mask):
    """main tcp handler"""
    #print("key: "+str(key))
    #print("mask: "+str(mask))
    conn = key.fileobj

    if mask & selectors.EVENT_READ: #connection is readable

        data = conn.recv(16) #read header
        if data==b"":
            sel.unregister(conn)
            del addr_list[key.data.ID]
        else:
            print("recv")
            try:
                datalen = int(data[:8])
            except:
                print("bad header, returning")
            datatype = data[8:16]
            key.data.message_type=datatype
            data = conn.recv(datalen)
            if len(data)!=datalen:
                print("bad header, returning")
                return


            #print(datalen)
            header=(datalen,datatype)
            tcp.handle_tcp_data(header,data,key.data)#let the tcp module handle that
            print(datalen,datatype)

            #print(str(data))



while True:
    print("bis hier keine errors")
    events_ = sel.select()
    for key, mask in events_:
        if key.data is None:
            accept(key.fileobj)
        else:
            black_magic(key, mask)
