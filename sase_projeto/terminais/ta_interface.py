import socket
import tkinter as tk
from tkinter import messagebox, ttk

PORTA_SERVIDOR = 5000
HOST_SERVIDOR = "127.0.0.1"

def solicitar_senha_backend(guiche_id):
    """Faz a comunicação pura com o servidor via Socket"""
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((HOST_SERVIDOR, PORTA_SERVIDOR))
        
    
        mensagem = f"chamar_proxima:{guiche_id}"
        cliente.send(mensagem.encode('utf-8'))
        
        resposta = cliente.recv(1024).decode('utf-8').strip()
        cliente.close()
        return resposta
    except socket.error as e:
        return f"ERRO|Não foi possível conectar ao servidor: {e}"

class AplicacaoTA:
    def __init__(self, root):
        self.root = root
        self.root.title("SASE - Terminal de Atendimento")
        self.root.geometry("450x350")
        self.root.configure(bg="#f4f6f9")
        
        self.guiche_id = tk.StringVar(value="1")
        
        self.criar_elementos()

    def criar_elementos(self):
      
        lbl_titulo = tk.Label(self.root, text="PAINEL DO ATENDENTE", font=("Arial", 16, "bold"), bg="#f4f6f9", fg="#333")
        lbl_titulo.pack(pady=15)
        
       
        frame_guiche = tk.Frame(self.root, bg="#f4f6f9")
        frame_guiche.pack(pady=10)
        
        tk.Label(frame_guiche, text="Número do Guichê (1 ou 2):", font=("Arial", 11), bg="#f4f6f9").pack(side=tk.LEFT, padx=5)
        ent_guiche = tk.Entry(frame_guiche, textvariable=self.guiche_id, width=5, font=("Arial", 11), justify="center")
        ent_guiche.pack(side=tk.LEFT)
        
       
        self.frame_senha = tk.LabelFrame(self.root, text=" Último Chamado ", font=("Arial", 10, "bold"), bg="#ffffff", bd=2, relief="groove")
        self.frame_senha.pack(pady=20, fill="both", expand=True, padx=20)
        
        self.lbl_senha = tk.Label(self.frame_senha, text="Aguardando...", font=("Arial", 20, "bold"), bg="#ffffff", fg="#d32f2f")
        self.lbl_senha.pack(pady=10)
        
        self.lbl_detalhes = tk.Label(self.frame_senha, text="Clique em 'Chamar Próximo' para iniciar", font=("Arial", 10, "italic"), bg="#ffffff", fg="#666")
        self.lbl_detalhes.pack(pady=5)
        
     
        btn_chamar = tk.Button(self.root, text="Chamar Próximo Cliente", font=("Arial", 12, "bold"), bg="#2e7d32", fg="white", bd=0, cursor="hand2", command=self.chamar_proximo)
        btn_chamar.pack(pady=15, ipady=8, fill="x", padx=20)

    def chamar_proximo(self):
        gid = self.guiche_id.get().strip()
        if gid not in ["1", "2"]:
            messagebox.showwarning("Aviso", "Por favor, digite um guichê válido (1 ou 2).")
            return
            
        resposta = solicitar_senha_backend(gid)
        
        if resposta == "Nenhuma Senha":
            self.lbl_senha.config(text="Fila Vazia", fg="#757575")
            self.lbl_detalhes.config(text="Não há senhas aguardando atendimento.")
        elif resposta.startswith("ERRO"):
            erro_msg = resposta.split("|")[1]
            messagebox.showerror("Erro de Conexão", erro_msg)
        else:
            
            partes = resposta.split("|")
            senha, setor, sala, atendente = partes[0], partes[1], partes[2], partes[3]
            
      
            self.lbl_senha.config(text=f"SENHA: {senha}", fg="#2e7d32")
            self.lbl_detalhes.config(text=f"{setor} (Sala {sala} - {atendente})")

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoTA(root)
    root.mainloop()