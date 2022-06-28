import os
import socket
import threading


PORT = 5050
IP = socket.gethostbyname(socket.gethostname())
ADDRESS = (IP, PORT)

# binds server to socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def put():
    pass

#////////////////////////////////////////////////////////////////
def ls(conn):

    # This is my path
    path = "D:\\final\\server"

    # to store files in a list
    list = ""

    # dirs=directories
    for (root, dirs, file) in os.walk(path):
        for f in file:
            if '.txt' in f:
                list += f + "\n"

    # print(list)

    conn.send(list.encode('utf-8'))

# ////////////////////////////////////////////////////////////////

def get(name, conn):
    

    # reads the file in binary mode
    # file = open(f"server\{name}.txt", "rb")
    #file = open(f"D:\final\server\"{name}.txt", "rb")
    file = open(f"D:/final/server/{name}.txt", "rb")
    # print(file)

    # get the size of the file
    #file_size = os.path.getsize(f"server/{name}.txt")
    file_size = os.path.getsize(f"D:/final/server/{name}.txt")
    # print(size)

    # send the first 1000 bytes of the file
    # conn.send(file.read(10))
    buffer_size = 1000
    counter = 1

    send_bytes = file.read(buffer_size)
    print(f"send bytes : {send_bytes}")    
    conn.send(send_bytes)

    while ((buffer_size * counter) < file_size) :

        s = file.seek(counter * buffer_size)
        print(f" seek {counter}: {s}")

        send_bytes = file.read(buffer_size)
        print(f"send bytes : {send_bytes}")

        conn.send(send_bytes)
        counter = counter + 1
        print(f"counter : {counter}")
    


    # print(file.read())
    file.close()
    # conn.close()
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()


# //////////////////////////////////////////////////////////


# handle the connection of one client
def handle_client (conn, addr):
    print(f"Accepted connection from client : {addr} ")

    try:
        connected = True
        while(connected):
            print("\nWaiting for client input ...")
                      
            message = conn.recv(1024).decode('utf-8') 
            message = message.split(" ")
            # print(message)
            if(message[0] == "get"):
                get(message[1], conn)
                #conn.send("get".encode("utf-8"))
            elif(message[0] == "put"):
                put()
            elif(message[0] == "ls"):
                ls(conn)
            elif(message[0] == "quit"):
                connected = False
                print(f"Client {addr} leaved.")
            else:
                print("Invalid Command!")
            break

        conn.close()

    except KeyboardInterrupt:
        print('\Wait')
        server.close()                            
        print('End.')

# //////////////////////////////////////////////////////////////////////////

# server starts to listen to the clients
def start():
    server.listen(5)

    print("Waiting for connections ...")

    while True:
        conn, addr = server.accept()

        #handshake
        conn.send("welcome".encode('utf-8'))

        # handle the connection of >1 clients, parallel
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        # print the number of active clients
        print(f"[ACTIVE CONNECTOINS] {threading.activeCount() - 1}")

        



print("Server is starting...")

start()