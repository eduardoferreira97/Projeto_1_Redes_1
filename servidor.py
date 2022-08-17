import socket

# Define a porta e o host do socket
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

# Cria o socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Defina o valor da opção de soquete fornecida
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Liga o socket ao endereço
server_socket.bind((SERVER_HOST, SERVER_PORT))
# Habilita o servidor aceite conexões
server_socket.listen(1)
print('Acessando a porta %s ...' % SERVER_PORT)

try:
    while True:    
        # Espera pela conecxão do cliente
        client_connection, client_address = server_socket.accept()
        
        # Recebe a solicitação do cliente
        request = client_connection.recv(1024).decode()
        # print(request)
        print(f"Conexão {client_address} estabelecida")

        # Analisa o cabeçalho de solicitação HTTP 
        headers = request.split('\n')
        filename = headers[0].split()[1]

        
        if filename == '/':
            filename = '/index.html'
    
        try:
            # Pega o conteudo do arquivo
            fin = open('htdocs'+ filename)
            content = fin.read()
            fin.close()

            
            response = 'HTTP/1.1 200 OK\n\n'+ content

        except FileNotFoundError:

            fin = open('htdocs/notFound.html')
            content = fin.read()
            fin.close()

            response = 'HTTP/1.1 404 NOT FOUND\n\n'+ content

        # Envia a resposta do HTTP para o socket   
        client_connection.sendall(response.encode())
        # ermina a conexão do cliente com o socket
        client_connection.close()

except KeyboardInterrupt:

# Fecha o socket
    server_socket.close()