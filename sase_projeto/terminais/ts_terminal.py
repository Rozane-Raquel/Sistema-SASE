# Módulo TS: Terminal de Senhas.
# Deve gerar senhas crescentes do tipo N ou P e enviar ao SRV.  
import socket


contador_n= 0
contador_p= 0

def gerar_senha_normal():
    global contador_n
    senha_n= "N" +  str(contador_n)
    contador_n += 1
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria um socket TCP/IP
    cliente.connect(("127.0.0.1", 5000)) # conecta ao servidor
    mensagem = f"gerar:{senha_n}"
    cliente.send(mensagem.encode('utf-8')) #  envia uma mensagem para o servidor
    resposta = cliente.recv(1024).decode('utf-8')
    print(f"[TS] Senha {senha_n} enviada. Resposta do Servidor: {resposta}")
    cliente.close()
    return senha_n

def gerar_senha_prioritaria():
    global contador_p
    senha_p= "P" +  str(contador_p)
    contador_p += 1
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria um socket TCP/IP
    cliente.connect(("127.0.0.1", 5000)) # conecta ao servidor
    mensagem = f"gerar:{senha_p}"
    cliente.send(mensagem.encode('utf-8')) #  envia uma mensagem para o servidor
    resposta = cliente.recv(1024).decode('utf-8')
    print(f"[TS] Senha {senha_p} enviada. Resposta do Servidor: {resposta}")
    cliente.close()
    return senha_p

'''testes'''
for i in range (5):
  gerar_senha_normal()
  gerar_senha_prioritaria()

