'''Terminal de Visualização'''
'''Exibe em tempo real a mesma senha enviada ao TA'''


import socket


porta_servidor = 5000
def iniciar_painel_tv():
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        try:
            cliente.connect(("127.0.0.1", porta_servidor))
            mensagem_registro = "REGISTRAR_TV"

            cliente.send(mensagem_registro.encode('utf-8'))
            print ("=" * 50)
            print ("   Painel de visualização iniciado (TV)   ")
            print ("   Aguardando senhas...   ")
            print ("=" * 50)

            while True:

                dados = cliente.recv(1024).decode('utf-8').strip()

                if not dados:
                    print ('\n [AVISO] Conexão com o servidor encerrada.')
                    break

                if dados.startswith("PAINEL:"):

                    partes = dados.split(":", 1)[1].split("|")

                    senha     = partes[0]
                    setor     = partes[1]
                    sala      = partes[2]
                    atendente = partes[3]

                    print("\n" + "#" * 40)
                    print(f">>> NOVO ATENDIMENTO <<<")
                    print(f"{senha} - {setor} (Sala {sala} - Atendente: {atendente})")
                    print("#" * 40)

        except socket.error as e:
            print (f"[ERRO TV] Não foi possível conectar ao painel central: {e}")

        except KeyboardInterrupt:
            print("Desligando painel de visualização...")

        finally:
            cliente.close()

if __name__ == "__main__": 
    iniciar_painel_tv()