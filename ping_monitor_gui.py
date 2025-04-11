import subprocess
import os
import time
import platform
from datetime import datetime
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

class PingMonitorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Monitor de Perda de Pacotes")
        self.master.geometry("500x430")
        self.master.config(bg="#f2f2f2")

        self.host = "google.com"
        self.intervalo = 10  # padrão
        self.log_file = self.definir_log_padrao()
        self.monitorando = False

        # Interface
        frame = tk.Frame(self.master, bg="#f2f2f2")
        frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.label_titulo = tk.Label(frame, text="Monitor de Perda de Pacotes", font=("Arial", 20), bg="#f2f2f2")
        self.label_titulo.pack(pady=10)

        self.label_status = tk.Label(frame, text=f"Log padrão: {self.log_file}", font=("Arial", 10), bg="#f2f2f2")
        self.label_status.pack(pady=5)

        self.btn_selecionar = tk.Button(frame, text="Selecionar outro local de log", font=("Arial", 14),
                                        command=self.selecionar_arquivo, bg="#4CAF50", fg="white", relief="flat")
        self.btn_selecionar.pack(pady=5, fill=tk.X)

        self.label_intervalo = tk.Label(frame, text="Intervalo do Ping (segundos):", font=("Arial", 14), bg="#f2f2f2")
        self.label_intervalo.pack(pady=5)

        self.combo_intervalo = ttk.Combobox(frame, values=["5", "10", "30", "60"], state="readonly", width=10)
        self.combo_intervalo.set("10")
        self.combo_intervalo.pack(pady=5)

        self.btn_iniciar = tk.Button(frame, text="Iniciar Monitoramento", font=("Arial", 14),
                                     command=self.iniciar_monitoramento, bg="#2196F3", fg="white", relief="flat")
        self.btn_iniciar.pack(pady=5, fill=tk.X)

        self.btn_parar = tk.Button(frame, text="Parar Monitoramento", font=("Arial", 14), state="disabled",
                                   command=self.parar_monitoramento, bg="#f44336", fg="white", relief="flat")
        self.btn_parar.pack(pady=5, fill=tk.X)

        self.label_rodape = tk.Label(frame, text="github.com/luanujk", font=("Arial", 8), bg="#f2f2f2", fg="gray")
        self.label_rodape.pack(side=tk.BOTTOM, pady=10)

    def definir_log_padrao(self):
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        return os.path.join(desktop_path, "ping.txt")

    def selecionar_arquivo(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Salvar log como"
        )
        if caminho:
            self.log_file = caminho
            self.label_status.config(text=f"Log selecionado: {self.log_file}")

    def ping_site(self):
        try:
            startupinfo = None
            if platform.system() == "Windows":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            resultado = subprocess.run(
                ['ping', '-n', '1', self.host],
                capture_output=True,
                text=True,
                shell=False,
                startupinfo=startupinfo
            )
            return "TTL=" in resultado.stdout
        except Exception as e:
            print(f"Erro no ping: {e}")
            return False

    def registrar_falha(self):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensagem = f"Perda de pacote detectada em: {timestamp}\n"
        with open(self.log_file, "a") as f:
            f.write(mensagem)
        print(mensagem.strip())

    def loop_monitoramento(self):
        while self.monitorando:
            if not self.ping_site():
                self.registrar_falha()
            time.sleep(self.intervalo)

    def animar_botao_monitoramento(self):
        estados = ["Monitorando.", "Monitorando..", "Monitorando..."]
        i = 0
        while self.monitorando:
            novo_texto = estados[i % 3]
            self.btn_iniciar.config(text=novo_texto, bg="#1976D2", fg="white")
            i += 1
            time.sleep(0.7)
        self.btn_iniciar.config(text="Iniciar Monitoramento", bg="#2196F3", fg="white")

    def iniciar_monitoramento(self):
        try:
            self.intervalo = int(self.combo_intervalo.get())
        except ValueError:
            messagebox.showwarning("Aviso", "Selecione um intervalo válido.")
            return

        self.monitorando = True
        self.btn_iniciar.config(state="disabled")
        self.btn_parar.config(state="normal")
        self.label_status.config(text=f"Monitorando... Salvando em: {self.log_file}")

        self.thread = threading.Thread(target=self.loop_monitoramento, daemon=True)
        self.thread.start()

        self.thread_animacao = threading.Thread(target=self.animar_botao_monitoramento, daemon=True)
        self.thread_animacao.start()

    def parar_monitoramento(self):
        self.monitorando = False
        self.btn_iniciar.config(state="normal")
        self.btn_parar.config(state="disabled")
        self.label_status.config(text=f"Monitoramento parado. Último log em: {self.log_file}")

# Execução
if __name__ == "__main__":
    root = tk.Tk()
    app = PingMonitorApp(root)
    root.mainloop()
