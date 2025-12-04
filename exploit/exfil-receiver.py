import socket
import threading

HOST = 'localhost' #127.0.0.1
PORT = 12345
CHUNK = 4096

def client(client_socket: socket, client_addr):

    print(f"Connection from {client_addr}")
    client_socket.settimeout(30) #arbitrary timeout for client

    try:
        data = b''  #bytestring, will contain bytestring sent by client
        i = 0       #file number written
        while True:
            request_data = client_socket.recv(CHUNK) #no need to decode, we are writing binary data

            #stop receiving if client has sent all data available to it
            if not request_data:
                break
            
            data += request_data

            #eof reached if length of received data is less than chunk size
            if (len(request_data) < CHUNK):

                #write data to file
                filename = "file" + str(i) + ".pkl"
                with open(filename, 'wb') as f:
                    f.write(data)

                data = b''
                i += 1

            #send acknowledgement to client
            response = "ack"
            client_socket.send(response.encode())

    except Exception as e:
        print(e)
    
    #close client socket
    finally:
        client_socket.close()
        print(f"Closed connection with {client_addr}")

def start():
    #create and start server socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        #run until process is interrupted (ctrl+c does not work on windows)
        while True:
            try:
                client_socket, client_addr = server_socket.accept()
                threading.Thread(target=client, args=(client_socket, client_addr)).start() #handle clients in separate thread
            except KeyboardInterrupt:
                print("Shutting attack code server down.")
                break

if __name__ == "__main__":
    start()