import socket
import sys
import os

"""Opens the file with the given filename
#and sends its data over the network through the provided socket.
"""
def send_file(socket, filename):
    #if filename not in current directory raise an error
    if filename not in os.listdir():
        socket.send(str(1).encode('utf-8')) #1 is sent to indicate an error
        raise Exception("file does not exist in current directory")
    socket.send(str(0).encode('utf-8')) #if no error, 0 is sent
    with open(filename, "rb") as f:
        sendfile = f.read()
        socket.sendall(sendfile) #sendall data that is read out from the file


""" Creates the file with the given filename
and stores into it data received from the provided socket."""
def recv_file(socket, filename):
    #if the filename already exists in the directory raise an error
    if filename in os.listdir():
        raise Exception("file already exists in directory")
    #open file in exclusionary binary mode
    with open(filename, "xb") as f:
        #receive till no more data transmitted
        while True:
            recvfile = socket.recv(4096)
            if not recvfile:
                break
            f.write(recvfile) #write to the target file


"""Generates and sends the directory listing from
the server to the client via the provided socket."""
def send_listing(socket):
    directory = os.listdir() #list of filenames
    msg = bytearray()
    #each file in directory encoded and the bytearray extended
    for file in directory:
        bytes_sent = str.encode(" "+file)
        msg.extend(bytes_sent)
    socket.sendall(msg)


"""Receives the listing from the server via the
provided socket and prints it on screen."""
def recv_listing(socket):
    data = socket.recv(4096).decode().split(" ") #returns list
    for element in data:
        print(element.strip())
    print("\n") #formatting





