import socket

# Define a porta e o host do socket
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print('Listening on port %s ...' % SERVER_PORT)

try:
    while True:    
        # Wait for client connections
        client_connection, client_address = server_socket.accept()
        
        # Get the client request
        request = client_connection.recv(1024).decode()
        # print(request)
        print(f"Conexão de {client_address} foi estabelecida")

        # Parse HTTP headers
        headers = request.split('\n')
        filename = headers[0].split()[1]

        # Get the content of the file
        if filename == '/':
            filename = '/index.html'
    
        try:
            fin = open('htdocs'+ filename, encoding="utf8", errors='ignore')
            content = fin.read()
            fin.close()

            
            response = 'HTTP/1.1 200 OK\n\n'+ content

        except FileNotFoundError:

            fin = open('htdocs/notFound.html')
            content = fin.read()
            fin.close()

            response = 'HTTP/1.1 404 NOT FOUND\n\n'+ content

        # Send HTTP response    
        client_connection.sendall(response.encode())
        client_connection.close()

except KeyboardInterrupt:

# Close socket
    server_socket.close()