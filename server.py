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
    data_cont=types.SimpleNamespace(auth="NOAUTH",ID=ID,message_len=0,message_type=b"",message=b"",header=b"")#creating data container
    addr_list[ID]=(conn,data_cont)
    ID+=1
    sel.register(conn, events, data=data_cont)#register connection with data container @ selector


def handle_tcp_data(data_processed):
    print(data_processed)

def black_magic(key, mask):
    """main tcp handler"""
    #print("key: "+str(key))
    #print("mask: "+str(mask))
    conn = key.fileobj
    
    if mask & selectors.EVENT_READ: #connection is readable
        data = conn.recv(1024)
        while data!=b"":
            if key.data.message_len==0:
                if len(data)<16 and header==b"":
                    header=data
                elif header!=b"":
                    if data+header<16:
                        header+=data
                    else:
                        data=header+data
                        datalen = data[:8]
                        key.data.message_len=int(datalen)
                        datatype = data[8:16]
                        key.data.message_type=datatype
                        data=data[16:]
                else:
                    datalen = data[:8]
                    key.data.message_len=int(datalen)
                    datatype = data[8:16]
                    key.data.message_type=datatype
                    data=data[16:]
            if key.data.message_len==0 and datatype == b"" and not datalen == b"":#bad health, closing connection
                print("closing connection "+ str(key.data.ID)+" due to bad health")
                data==b""
            readlen=len(data)
            if readlen<=key.data.message_len:
                key.data.message+=data[:key.data.message_len]
                key.data.message_len=0
                handle_tcp_data(key.data.message)
                key.data.message=b""
                data=data[key.data.message_len:]
            else:
                key.data.message+=data
                key.data.message_len-=readlen
                data=b""
            

        print(datalen,datatype)
        
        #print(str(data))
        if data==b"":
            sel.unregister(conn)
            del addr_list[key.data.ID]
    

while True:
    print("bis hier keine errors")
    events_ = sel.select()
    for key, mask in events_:
        if key.data is None:
            accept(key.fileobj)
        else:
            black_magic(key, mask)

