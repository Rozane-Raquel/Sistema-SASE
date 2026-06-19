import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria um socket TCP/IP
server.bind(("127.0.0.1", 5000)) # liga o socket a um endereço e porta
server.listen() # coloca o socket em modo de escuta para aguardar conexões
print("Servidor no ar, esperando conexão...")
conexao, endereco = server.accept() # aceita uma conexão
print("Conexão estabelecida com:", endereco)
dados = conexao.recv(1024) # recebe dados do cliente
print("Recebi:", dados.decode()) # imprime os dados recebidos
conexao.send("recebi seu oi!".encode()) # envia uma resposta para o cliente
conexao.close() # fecha a conexão