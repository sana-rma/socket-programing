import os
import socket

PORT = 5050
IP = socket.gethostbyname(socket.gethostname())
ADDRESS = (IP, PORT)

def reconnect():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)



def get(name):
    file = open(f"{name}.txt", "ab")

    while True:
        recieve_bytes = client.recv(1000)

        if not recieve_bytes:
            break

        file.write(recieve_bytes) 

    file.close()
    print("file received.")
    # client.close()
    # reconnect()
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    reconnect()

def ls(conn):
    list = conn.recv(1024).decode('utf-8') 
    print(list)




try:
     # connects client to server
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)

    #handshake.print
    print(client.recv(1024).decode('utf-8'))
    
    # gets the commands from client
    while True:
        message = input("ftp > ")                    
        client.send(message.encode('utf-8'))

        message = message.split(" ")
        # print(message)
        # recieved_message = client.recv(1024)
        if message[0] == "get":
            get(message[1])
            # reconnect()
        elif message[0] == "ls":
            ls(client)
        elif message[0] == "put":
            # put(message[1])
            pass
        
        elif(message[0] == "quit"):
           break          
        
        
except KeyboardInterrupt:
    client.close()                     
    print("End.")
