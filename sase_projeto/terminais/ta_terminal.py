'''Terminal de Atendimento'''
''' Solicita uma próxima senha válida ao servidor SRV'''


import socket
import time

porta_servidor=5000

SETORES = {
    "1": "Cadastro único",
    "2": "Auxilios",
}

def escolher_setor():
    while True:
        print("Selecione o setor deste guiche:")
        print("1. Cadastro único")
        print("2. Auxilios")
        opcao = input("Opçao: ").strip()
        if opcao in SETORES:
            return SETORES[opcao]
        print("[Opçao inválida] Digite 1 ou 2.")

def chamar_proxima_senha(guiche_id):
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect(("127.0.0.1", porta_servidor))
        
        mensagem = f"chamar_proxima:{guiche_id}"
        cliente.send(mensagem.encode('utf-8'))
        
        resposta_completa = cliente.recv(1024).decode('utf-8').strip()
        
        print("=" * 50)
        if resposta_completa == "Nenhuma Senha":
            print("Não há senhas aguardando.")
        else:
            
            partes = resposta_completa.split("|")
            senha     = partes[0]
            setor     = partes[1]
            sala      = partes[2]
            atendente = partes[3]
            
           
            print(f"_____SENHA: {senha}_____")
            print(f"-> {setor} (Sala {sala} - Atendente: {atendente})")
            
        print("=" * 50)
    except socket.error as e:
        print(f"\n [ERRO TA] Falha na comunicação: {e}")
    finally:
        cliente.close()


def menu_atendimento():
    
    guiche_id = input("Digite o número do guichê (1 ou 2): ").strip()
    
    while True:
        print(f'\n>>> PAINEL DO ATENDENTE - GUICHÊ {guiche_id} <<<')
        print("1. Chamar próximo cliente")
        print("2. Deslogar / Sair")
        print('-' * 50)

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\nSolicitando próxima senha...")
            chamar_proxima_senha(guiche_id) 
            time.sleep(1)
        elif opcao == "2":
            print("\nEncerrando guichê.")
            break
        else:
            print ("\n [Opção inválida] Digite somente 1 ou 2. ")

if __name__  == "__main__":
    menu_atendimento() 
         