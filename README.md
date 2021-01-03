# client-server-files
Python TCP socket application which lets you transfer files between a server and a client

The server can be executed through the command line via "python server.py <port number>"; the client can then establish a connection via "python client.py <hostname> <port> <request>". Valid request types are "put" and "get" which are followed by a filename.Those either upload (put) or download (get) a file to or from the server. "list" lists all files in the server directory.
