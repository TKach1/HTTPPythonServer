# Feito por Wesley Brandão
import socket
import threading
import os

def handle_client(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Requisição recebida:\n{request}")

    # Parse da requisição HTTP
    lines = request.split('\r\n')
    if len(lines) > 0:
        first_line = lines[0].split()
        if len(first_line) > 1:
            method = first_line[0]
            path = first_line[1]

            if path.startswith('/'):
                path = path[1:]

            if path == '':
                path = 'index.html'

            if os.path.exists(path):
                with open(path, 'rb') as file:
                    content = file.read()

                if path.endswith('.html'):
                    content_type = 'text/html'
                elif path.endswith('.jpg') or path.endswith('.jpeg'):
                    content_type = 'image/jpeg'
                else:
                    content_type = 'application/octet-stream'

                # HTTP Response
                response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(content)}\r\n\r\n"
                client_socket.sendall(response.encode('utf-8') + content)
            else:
                response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1>"
                client_socket.sendall(response.encode('utf-8'))

    client_socket.close()

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Servidor ouvindo em {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Conexão aceita de {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    start_server('0.0.0.0', 8080)
