import socket
import os

import buffer

HOST = ''
PORT = 10000

# If server and client run in same local directory,
# need a separate place to store the uploads.

s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)
print("Waiting for a connection.....")
conn, addr = s.accept()

while True:
    #print("Accepted a connection request from %s:%s"%(clientAddress[0], clientAddress[1]));

        #dataFromClient = conn.recv(1024)
        #print(dataFromClient.decode('utf-8'));
        sendData ='>>>'
        conn.send(sendData.encode('utf-8'))



    # Send some data back to the client

        #conn.send("Hello Client!".encode());

conn.close()
