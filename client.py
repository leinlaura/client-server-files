import socket
import sys
import os
from common_functions import send_file,recv_file,recv_listing

# Create the socket with which we will connect to the server
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#get hostname and port variables
try:
	hostname = sys.argv[1]
	port = int(sys.argv[2])
except Exception as e:
	print(e)
	exit(1) #indicate failure

srv_addr = (hostname, int(port)) #server address
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname) #get server ip address
ip_port = "(" + ip +", "+ str(port) +")" #to be used for messages


#checking validity of command and filename variables
try:
	command = str(sys.argv[3])  # parsing command
	filename = ""
	if command not in ["put", "get", "list"]:
		raise Exception("command not valid")
	if command in ["put","get"]:
		filename = str(sys.argv[4]) #if command put or get, parse filename
		if len(command.encode("utf-8")) > 4096:
			raise Exception("filename too long")

except Exception as e:
	print(e)
	exit(1) #indicate failure

#try connecting to the server
#if successful print message
try:
	cli_sock.connect(srv_addr)
	print("Connected to " + ip_port + ".")

#if establishing connection unsuccessful:
except Exception as e:
	print(ip_port + " " + command + " " + filename + " failure: " + str(e)) #failure message
	exit(1)

try:
	cli_sock.send(command.encode('utf-8'))  # pass command to server

	if command == "put":
		cli_sock.send(filename.encode('utf-8')) #pass filename to server
		send_file(cli_sock, filename) #call function from common_functions

	elif command=="get":
		cli_sock.send(filename.encode('utf-8'))  # pass filename to server
		server_message = cli_sock.recv(1).decode('utf-8')
		if server_message == str(1): #1 is passed if no file error raised on server side
			raise Exception("file does not exist in server directory")
		recv_file(cli_sock, filename)

	elif command == "list":
		recv_listing(cli_sock)

	#message to print if execution successful
	print(ip_port + " " + command + " "+ filename + " success") #success message

except Exception as e:
	#message to print if execution unsuccessful
	print(ip_port + " " + command + " " + filename + " failure: " + str(e)) #failure message

finally:
	#close connection
	cli_sock.close()
