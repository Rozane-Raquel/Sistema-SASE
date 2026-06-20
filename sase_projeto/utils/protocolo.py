#  padrão de comunicação entre os sockets (ex: JSON ou strings formatadas)
import json

def empacotar_mensagem(tipo_origem, comando, dados):
    return json.dumps({'origem': tipo_origem, 'comando': comando, 'dados': dados}).encode('utf-8')
