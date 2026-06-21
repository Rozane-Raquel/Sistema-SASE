'''Terminal de Senhas'''
'''Gera senhas crescentes do tipo N ou P e enviar ao SRV'''


import socket


contador_n= 1
contador_p= 1

def gerar_senha_normal():
    global contador_n
    senha_n= "N" +  str(contador_n)
    contador_n += 1
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(("127.0.0.1", 5000)) 
    mensagem = f"gerar:{senha_n}"
    cliente.send(mensagem.encode('utf-8')) 
    resposta = cliente.recv(1024).decode('utf-8')
    print(f"[TS] Senha {senha_n} enviada. Resposta do Servidor: {resposta}")
    cliente.close()
    return senha_n

def gerar_senha_prioritaria():
    global contador_p
    senha_p= "P" +  str(contador_p)
    contador_p += 1
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    cliente.connect(("127.0.0.1", 5000))
    mensagem = f"gerar:{senha_p}"
    cliente.send(mensagem.encode('utf-8')) 
    resposta = cliente.recv(1024).decode('utf-8')
    print(f"[TS] Senha {senha_p} enviada. Resposta do Servidor: {resposta}")
    cliente.close()
    return senha_p

'''testes'''
for i in range (6):
  gerar_senha_normal()
  gerar_senha_prioritaria()

