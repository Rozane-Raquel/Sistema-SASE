# Controla as listas N e P. Lembre-se da regra:
# Para cada duas SEAs do tipo N informadas, a próxima deve ser P (se houver)
class GerenciadorFilas:
    def __init__(self):
        self.fila_normal = []
        self.fila_prioritaria = []
        self.contagem_normal_seguida = 0
        self.terminais_tv=[]