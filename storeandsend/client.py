import socket
import threading
import os

import buffer

HOST = '127.0.0.1'
PORT = 2345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


path = './receive_video/'

while True:
    with s:

        while True:
            files_to_send = os.listdir(path)

            if len(files_to_send) >= 1:
                break
            else:
                continue


        sbuf = buffer.Buffer(s)

        hash_type = 'a'

        #files = os.listdir(path)

        for file_name in files_to_send:
            print(file_name)
            sbuf.put_utf8(hash_type)
            sbuf.put_utf8(file_name)

            file_size = os.path.getsize(path + file_name)
            sbuf.put_utf8(str(file_size))

            with open(path + file_name, 'rb') as f:
                sbuf.put_bytes(f.read())
            print('File Sent')

        os.system(f"rm ./receive_video/*.mp4")
