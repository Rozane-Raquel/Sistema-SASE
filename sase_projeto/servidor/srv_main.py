# Módulo SRV: Escuta conexões socket de TS, TA e TV.
# Deve registrar o instante em que recebe e envia mensagens.
import socket
import threading
from datetime import datetime 
from gerenciador_filas import GerenciadorFilas
lock = threading.Lock()





def selecionar_proxima_senha():

    with lock:

        if not GerenciadorFilas.fila_normal and not GerenciadorFilas.fila_prioritaria:
            return "Não existe senhas aguardando..."

        if GerenciadorFilas.contagem_normal_seguida >=2:

            if GerenciadorFilas.fila_prioritaria:
                senha=GerenciadorFilas.fila_prioritaria.pop(0)
                GerenciadorFilas.contagem_normal_seguida=0
                return senha
            
            elif GerenciadorFilas.fila_normal:
                senha = GerenciadorFilas.fila_normal.pop(0)
                GerenciadorFilas.contagem_normal_seguida +=1
                return senha
            
        if GerenciadorFilas.fila_prioritaria:

            senha = GerenciadorFilas.fila_prioritaria.pop(0)
            GerenciadorFilas.contagem_normal_seguida=0
            return senha
        
        elif GerenciadorFilas.fila_normal:

            senha = GerenciadorFilas.fila_normal.pop(0)
            GerenciadorFilas.contagem_normal_seguida +=1
            return senha 
        
        return "Nenhuma Senha"


def transmitir_tv (mensagem):
    with lock:
        lista_remover = []
        for tv_socket in GerenciadorFilas.terminais_tv :
            
            try:
                tv_socket.sendall(mensagem.encode('utf-8'))
            except (socket.error, BrokenPipeError):
                lista_remover.append(tv_socket)


        for tv_morta in lista_remover:
            if tv_morta in GerenciadorFilas.terminais_tv:
                GerenciadorFilas.terminais_tv.remove(tv_morta)

def gerenciar_cliente (cliente_socket, cliente_address):
    print (f"[CONEXÃO] Novo terminal conectado de {cliente_address}")

    try:
        requisicao = cliente_socket.recv(1024).decode('utf-8').strip()
        if not requisicao:
            return 
        
        if requisicao.startswith("gerar:"):
            tipo_e_senha= requisicao.split(':')[1]
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [TS] Recebida nova senha gerada: {tipo_e_senha}")

            with lock:
                if tipo_e_senha.startswith('N'):
                    GerenciadorFilas.fila_normal.append(tipo_e_senha)
                elif tipo_e_senha.startswith('P'):
                    GerenciadorFilas.fila_prioritaria.append(tipo_e_senha)

            cliente_socket.sendall('ok'.encode('utf-8'))
            cliente_socket.close()

        elif requisicao == "chamar_proxima:":
            senha_selecionada=selecionar_proxima_senha()
            timestamp = datetime.now().strftime("%H:%M:%S")
            if senha_selecionada != "NENHUMA_SENHA":
                print(f"[{timestamp}] [SRV] Enviando senha {senha_selecionada} para o TA.")
                transmitir_tv(f"PAINEL:{senha_selecionada}")
            else: 
                print(f"[{timestamp}] [SRV] TA solicitou senha, mas as filas estão vazias.")
            cliente_socket.sendall(senha_selecionada.encode('utf-8'))
            cliente_socket.close()


        elif requisicao == "REGISTRAR_TV":
            with lock:
                GerenciadorFilas.terminais_tv.append(cliente_socket)
            print(f"[TV] Painel de visualização registrado com sucesso. Mantendo conexão aberta...")
            return

    except Exception as e:
        print(f"[ERRO] Falha ao processar cliente {cliente_address}: {e}")
        cliente_socket.close()

def iniciar_servidor(host='127.0.0.1', port=5000):
  
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ''' Permite reutilizar a porta imediatamente se o servidor for reiniciado rapidamente'''
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"[PRONTO] Servidor SASE iniciado com sucesso em {host}:{port}")
        print("Aguardando conexões dos módulos (TS, TA, TV)...")
        
        while True:
            '''Bloqueia até que um cliente se conecte'''
            client_socket, client_address = server_socket.accept()
            
            '''Cria uma thread dedicada para atender a este cliente em paralelo'''
            thread_cliente = threading.Thread(
                target=gerenciar_cliente, 
                args=(client_socket, client_address)
            )
            thread_cliente.daemon = True # Encerra as threads se o script principal fechar
            thread_cliente.start()
            
    except KeyboardInterrupt:
        print("\n[DESLIGANDO] Finalizando o servidor central...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    iniciar_servidor()

