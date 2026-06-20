# Módulo TV: Terminal de Visualização.
# Exibe em tempo real a mesma senha enviada ao TA.
import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(("127.0.0.1", 5000))
server.send("oi".encode())
resposta = server.recv(1024)
print("Servidor disse:", resposta.decode())