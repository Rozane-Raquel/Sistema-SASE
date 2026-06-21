import socket
import threading
import tkinter as tk
from tkinter import messagebox

PORTA_SERVIDOR = 5000
HOST_SERVIDOR = "127.0.0.1"

class AplicacaoTV:
    def __init__(self, root):
        self.root = root
        self.root.title("SASE - Painel de Visualização (TV)")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a237e")  
        
        
        
        self.criar_elementos()
        
       
        self.conexao_ativa = True
        self.thread_socket = threading.Thread(target=self.escutar_servidor, daemon=True)
        self.thread_socket.start()

    def criar_elementos(self):
      
        lbl_topo = tk.Label(
            self.root, 
            text="SISTEMA DE ATENDIMENTO", 
            font=("Arial", 24, "bold"), 
            bg="#1a237e", 
            fg="#ffffff"
        )
        lbl_topo.pack(pady=30)
        
       
        self.frame_senha = tk.Frame(self.root, bg="#ffffff", bd=5, relief="solid")
        self.frame_senha.pack(pady=20, padx=50, fill="both", expand=True)
        
        lbl_texto_senha = tk.Label(
            self.frame_senha, 
            text="SENHA", 
            font=("Arial", 28, "bold"), 
            bg="#ffffff", 
            fg="#555555"
        )
        lbl_texto_senha.pack(pady=(20, 0))
        
        
        self.lbl_senha = tk.Label(
            self.frame_senha, 
            text="---", 
            font=("Arial", 90, "bold"), 
            bg="#ffffff", 
            fg="#d32f2f"
        )
        self.lbl_senha.pack(pady=10)
        
       
        self.lbl_local = tk.Label(
            self.frame_senha, 
            text="Aguardando inicialização do sistema...", 
            font=("Arial", 22, "bold"), 
            bg="#ffffff", 
            fg="#1a237e"
        )
        self.lbl_local.pack(pady=10)
        
        self.lbl_atendente = tk.Label(
            self.frame_senha, 
            text="", 
            font=("Arial", 16, "italic"), 
            bg="#ffffff", 
            fg="#666666"
        )
        self.lbl_atendente.pack(pady=10)

      
        lbl_rodape = tk.Label(
            self.root, 
            text="Por favor, aguarde a sua senha ser chamada no painel.", 
            font=("Arial", 14), 
            bg="#1a237e", 
            fg="#b0bec5"
        )
        lbl_rodape.pack(pady=20)

    def escutar_servidor(self):
       
        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((HOST_SERVIDOR, PORTA_SERVIDOR))
            
           
            cliente.send("REGISTRAR_TV".encode('utf-8'))
            
            while self.conexao_ativa:
                dados = cliente.recv(1024).decode('utf-8').strip()
                
                if not dados:
                    break
                
               
                if dados.startswith("PAINEL:"):
                    conteudo = dados.split(":", 1)[1]
                    partes = conteudo.split("|")
                    
                    senha = partes[0]
                    setor = partes[1]
                    sala = partes[2]
                    atendente = partes[3]
                    
                   
                    self.root.after(0, self.atualizar_tela, senha, setor, sala, atendente)
                    
        except socket.error as e:
            self.root.after(0, lambda: messagebox.showerror("Erro na TV", f"Conexão perdida com o servidor: {e}"))
        finally:
            cliente.close()

    def atualizar_tela(self, senha, setor, sala, atendente):
      
        self.lbl_senha.config(text=senha)
        self.lbl_local.config(text=f"{setor} - SALA {sala}")
        self.lbl_atendente.config(text=f"Atendente: {atendente}")
        
    
        self.frame_senha.config(bg="#fff59d") 
        self.root.after(1000, lambda: self.frame_senha.config(bg="#ffffff"))

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoTV(root)
    root.mainloop()