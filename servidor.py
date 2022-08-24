import socket


# Define a porta e o host do socket
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8080

# Cria o socket
# F_INET (família de endereço IPV4) e SOCK_STREAM (TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Defina o valor da opção de socket fornecida
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Liga o socket ao endereço
server_socket.bind((SERVER_HOST, SERVER_PORT))
# Habilita que o servidor aceite conexões
server_socket.listen(15)

print('Acessando a porta %s ...' % SERVER_PORT)

try:
    while True:
        # Espera pela conecxão do cliente
        client_connection, client_address = server_socket.accept()

        # Recebe a solicitação do cliente
        # recv() recebe as mensagens através do socket
        request = client_connection.recv(9000).decode()
        # print(request)
        print(f"Conexão {client_address[0]} estabelecida")

        # Analisa o cabeçalho de solicitação HTTP
        headers = request.split('\n')
        filename = headers[0].split()[1]

        if filename == '/':
            filename = '/index.html'

        try:
            # Pega o conteudo do arquivo
            # with open('htdocs'+filename, encoding='utf-8') as f:
            #     content = f.read()
            # f.close()

            fin = open('htdocs' + filename, 'rb')
            content = fin.read().decode('ISO-8859-1')
            fin.close()


            # Resposta
            response = ('HTTP/1.1 200 OK\r\n' + 'Content-Type: text/html\r\n' + 'Content-Length: ' +
                        str(len(content)) + 'Accept-Ranges: bytes\r\n\r\n' + (content))

        except FileNotFoundError:

            fin = open('htdocs/notFound.html')
            content = fin.read()
            fin.close()

            # Resposta
            response = ('HTTP/1.1 404 NOT FOUND\n\n' + 'Content-Type: text/html\r\n' +
                        'Content-Length: ' + str(len(content)) + '\r\n\r\n' + (content))

        # Envia a resposta para o socket
        client_connection.sendall(response.encode())


except KeyboardInterrupt:
    # Termina a conexão do cliente com o socket
    client_connection.close()
    # Fecha o socket
    server_socket.close()
