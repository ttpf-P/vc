import serverFiles.tcp.authentication as auth


msgTypes = {b"\x00\x00\x00LOGIN":auth.login}

def handle_tcp_data(header,data_processed,conn_data):
    print(len(data_processed))
    try:
        msgTypes[header[1]](header,data_processed,conn_data)
    except KeyError:
        print("bad msgType, returning")
        return
