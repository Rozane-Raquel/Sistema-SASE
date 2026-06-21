'''Terminal de Atendimento'''
''' Solicita uma próxima senha válida ao servidor SRV'''


import socket
import time

porta_servidor=5000

def chamar_proxima_senha(numero_guiche):

    try:
        cliente=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(("127.0.0.1", porta_servidor))


        mensagem= "chamar_proxima"

        cliente.send(mensagem.encode('utf-8'))

        senha_recebida = cliente.recv(1024).decode('utf-8').strip()

        print ("=" * 50)

        if senha_recebida == "nenhuma_senha":
            print (f'[Guichê {numero_guiche}] não há senhas aguardando no momento')

        else:
            print(f'[Guichê {numero_guiche}] >>> CHAMANDO SENHA: {senha_recebida} <<<')

        print ('=' * 50)
    except socket.error as e:
        print (f'\n [ERRO TA] Falha na comunicação com o servidor: {e}')

    finally:
        cliente.close()

def menu_atendimento():
    guiche = input ("digite o número deste guichê de atendimento: ").strip()

    while True:
        print (f'>>> PAINEL DO ATENDENTE - GUICHÊ {guiche} <<<')
        print ("1. Chamar próximo cliente")
        print ("2. Deslogar / Sair")
        print ('-' * 50)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print ("\n Solicitando próxima senha: ")
            chamar_proxima_senha(guiche)
            time.sleep(1)

        elif opcao == "2":
            print("\nEncerrando guichê. ")
            break
        else:
            print ("\n [Opção inválida] Digite somente 1 ou 2. ")

if __name__  == "__main__":
    menu_atendimento() 
         