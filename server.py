import socket
import sys
import os
import time
from Client.common_functions import send_file, recv_file, send_listing
# import statement depends on Client Folder to be existent within the Server Folder;
# alternative implimentations with sys.getpath() possible

# Create the socket 
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname) #get ip address of server

#exceptions related to ports and invalid command-line arguments
try:
	srv_sock.bind(("0.0.0.0", int(sys.argv[1]))) # sys.argv[1] is the 1st argument on the command line
	#queue for new connection requests
	srv_sock.listen(10)
	print("("+ ip + ", "+str(int(sys.argv[1]))+"): server up and running")
except Exception as e:
	print(e)

#loop back to wait for new client connections when finished
while True:
        #try establishing a connection with a client
        try:
            cli_sock, cli_addr = srv_sock.accept() #accepting a new connection
            cli_addr_str = str(cli_addr) 
            print("Client " + cli_addr_str + " connected.")

        except Exception as e:
            print(e)

        try:
            command = cli_sock.recv(3).decode('utf-8')  # receive command and decode
            filename = ""

            if command == "put":
                filename = cli_sock.recv(4094).decode('utf-8')  # receive filename and decode
                client_message = cli_sock.recv(1).decode('utf-8') #receive status confirmation character
                #checks if file exists in client directory
                if client_message == str(1):
                    raise Exception("file does not exist in client directory") #check beforehand, so no file with no contents is created
                recv_file(cli_sock, filename)

            elif command == "get":
                filename = cli_sock.recv(4094).decode('utf-8')  # receive filename and decode
                send_file(cli_sock, filename)

            elif command == "lis":
                command = "list"
                send_listing(cli_sock)

            print(cli_addr_str + " " + command + " " + filename + " success") #success message
            
        except Exception as e:
            print(cli_addr_str + " " +command + " "+ filename + " failure: " + str(e)) #failure message

        finally:
            #whether transfer successful or not, close client connection and loop back to wait for new ones
            time.sleep(0.1)
            cli_sock.close()

    
