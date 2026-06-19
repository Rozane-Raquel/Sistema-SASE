import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria um socket TCP/IP
server.connect(("127.0.0.1", 5000)) # conecta ao servidor
server.send("oi".encode()) #  envia uma mensagem para o servidor
resposta = server.recv(1024) # recebe a resposta do servidor
print("Servidor disse:", resposta.decode())