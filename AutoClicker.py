import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pyautogui
from pynput import keyboard, mouse
from pynput.mouse import Button
import json
import os

class AutoClicker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Auto Clicker - Fortnite")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Variáveis de controle
        self.is_running = False
        self.click_thread = None
        self.listener = None
        self.hotkey_pressed = False
        
        # Configurações padrão
        self.click_interval = 0.1  # segundos
        self.click_type = "left"  # left, right, middle
        self.hotkey = "f6"  # tecla para ativar/desativar
        self.click_position = None  # None = posição atual do mouse
        
        # Desabilitar fail-safe do pyautogui para jogos
        pyautogui.FAILSAFE = False
        
        self.setup_ui()
        self.load_settings()
        self.start_hotkey_listener()
        
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Título
        title_label = ttk.Label(main_frame, text="🎮 Auto Clicker para Fortnite", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Configuração de intervalo
        ttk.Label(main_frame, text="Intervalo entre cliques (segundos):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.interval_var = tk.StringVar(value=str(self.click_interval))
        interval_entry = ttk.Entry(main_frame, textvariable=self.interval_var, width=10)
        interval_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Tipo de clique
        ttk.Label(main_frame, text="Tipo de clique:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.click_type_var = tk.StringVar(value=self.click_type)
        click_combo = ttk.Combobox(main_frame, textvariable=self.click_type_var, 
                                  values=["left", "right", "middle"], state="readonly", width=10)
        click_combo.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Configuração de hotkey
        ttk.Label(main_frame, text="Tecla de ativação:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.hotkey_var = tk.StringVar(value=self.hotkey)
        hotkey_frame = ttk.Frame(main_frame)
        hotkey_frame.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        self.hotkey_entry = ttk.Entry(hotkey_frame, textvariable=self.hotkey_var, width=10)
        self.hotkey_entry.pack(side=tk.LEFT)
        
        capture_btn = ttk.Button(hotkey_frame, text="Capturar", command=self.capture_hotkey)
        capture_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Posição do clique
        ttk.Label(main_frame, text="Posição do clique:").grid(row=4, column=0, sticky=tk.W, pady=5)
        position_frame = ttk.Frame(main_frame)
        position_frame.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        self.position_var = tk.StringVar(value="Posição atual do mouse")
        self.position_label = ttk.Label(position_frame, textvariable=self.position_var)
        self.position_label.pack(side=tk.LEFT)
        
        set_pos_btn = ttk.Button(position_frame, text="Definir Posição", command=self.set_click_position)
        set_pos_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        clear_pos_btn = ttk.Button(position_frame, text="Limpar", command=self.clear_position)
        clear_pos_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Status
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        
        self.status_var = tk.StringVar(value="⏹️ Parado")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, font=("Arial", 12, "bold"))
        status_label.pack()
        
        # Botões de controle
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        self.start_btn = ttk.Button(button_frame, text="▶️ Iniciar", command=self.start_clicking)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(button_frame, text="⏹️ Parar", command=self.stop_clicking, state="disabled")
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Salvar configurações
        save_btn = ttk.Button(button_frame, text="💾 Salvar Config", command=self.save_settings)
        save_btn.pack(side=tk.LEFT, padx=5)
        
        # Informações
        info_frame = ttk.LabelFrame(main_frame, text="Informações", padding="10")
        info_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        
        info_text = """
🎯 Como usar:
1. Configure o intervalo entre cliques (ex: 0.1 = 10 cliques/seg)
2. Escolha o tipo de clique (esquerdo/direito/meio)
3. Defina a tecla de ativação (padrão: F6)
4. Opcionalmente, defina uma posição fixa para clicar
5. Pressione a tecla de ativação para iniciar/parar

⚠️ Aviso: Use com responsabilidade e respeite os termos de uso dos jogos.
        """
        info_label = ttk.Label(info_frame, text=info_text, justify=tk.LEFT)
        info_label.pack()
        
    def capture_hotkey(self):
        self.hotkey_entry.configure(state="readonly")
        self.hotkey_entry.delete(0, tk.END)
        self.hotkey_entry.insert(0, "Pressione uma tecla...")
        
        def on_key_press(key):
            try:
                if hasattr(key, 'char') and key.char:
                    hotkey = key.char.lower()
                else:
                    hotkey = str(key).replace('Key.', '')
                
                self.root.after(0, lambda: self.set_hotkey(hotkey))
                return False  # Para o listener
            except:
                pass
        
        # Para o listener atual se existir
        if self.listener:
            self.listener.stop()
        
        # Inicia listener temporário para capturar tecla
        temp_listener = keyboard.Listener(on_press=on_key_press)
        temp_listener.start()
        
    def set_hotkey(self, hotkey):
        self.hotkey = hotkey
        self.hotkey_var.set(hotkey)
        self.hotkey_entry.configure(state="normal")
        self.restart_hotkey_listener()
        
    def set_click_position(self):
        messagebox.showinfo("Definir Posição", 
                           "Posicione o mouse onde deseja clicar e pressione OK em 3 segundos...")
        self.root.after(3000, self.capture_position)
        
    def capture_position(self):
        x, y = pyautogui.position()
        self.click_position = (x, y)
        self.position_var.set(f"Posição: ({x}, {y})")
        
    def clear_position(self):
        self.click_position = None
        self.position_var.set("Posição atual do mouse")
        
    def start_hotkey_listener(self):
        def on_hotkey():
            if not self.hotkey_pressed:
                self.hotkey_pressed = True
                if self.is_running:
                    self.root.after(0, self.stop_clicking)
                else:
                    self.root.after(0, self.start_clicking)
                
                # Reset flag após um tempo
                threading.Timer(0.5, lambda: setattr(self, 'hotkey_pressed', False)).start()
        
        try:
            if self.listener:
                self.listener.stop()
            
            # Tenta diferentes formatos de hotkey
            hotkey_combinations = [
                self.hotkey,
                f"<{self.hotkey}>",
                self.hotkey.lower(),
                self.hotkey.upper()
            ]
            
            for hk in hotkey_combinations:
                try:
                    self.listener = keyboard.GlobalHotKeys({hk: on_hotkey})
                    self.listener.start()
                    break
                except:
                    continue
                    
        except Exception as e:
            print(f"Erro ao configurar hotkey: {e}")
            
    def restart_hotkey_listener(self):
        self.start_hotkey_listener()
        
    def start_clicking(self):
        try:
            self.click_interval = float(self.interval_var.get())
            if self.click_interval <= 0:
                raise ValueError("Intervalo deve ser maior que 0")
        except ValueError:
            messagebox.showerror("Erro", "Intervalo inválido! Use um número decimal (ex: 0.1)")
            return
            
        self.click_type = self.click_type_var.get()
        self.is_running = True
        
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_var.set("▶️ Executando...")
        
        self.click_thread = threading.Thread(target=self.click_loop, daemon=True)
        self.click_thread.start()
        
    def stop_clicking(self):
        self.is_running = False
        
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_var.set("⏹️ Parado")
        
    def click_loop(self):
        while self.is_running:
            try:
                if self.click_position:
                    x, y = self.click_position
                    if self.click_type == "left":
                        pyautogui.click(x, y, button='left')
                    elif self.click_type == "right":
                        pyautogui.click(x, y, button='right')
                    elif self.click_type == "middle":
                        pyautogui.click(x, y, button='middle')
                else:
                    if self.click_type == "left":
                        pyautogui.click(button='left')
                    elif self.click_type == "right":
                        pyautogui.click(button='right')
                    elif self.click_type == "middle":
                        pyautogui.click(button='middle')
                        
                time.sleep(self.click_interval)
            except Exception as e:
                print(f"Erro no clique: {e}")
                break
                
    def save_settings(self):
        settings = {
            'click_interval': self.interval_var.get(),
            'click_type': self.click_type_var.get(),
            'hotkey': self.hotkey_var.get(),
            'click_position': self.click_position
        }
        
        try:
            with open('autoclicker_settings.json', 'w') as f:
                json.dump(settings, f)
            messagebox.showinfo("Sucesso", "Configurações salvas!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")
            
    def load_settings(self):
        try:
            if os.path.exists('autoclicker_settings.json'):
                with open('autoclicker_settings.json', 'r') as f:
                    settings = json.load(f)
                
                self.interval_var.set(settings.get('click_interval', '0.1'))
                self.click_type_var.set(settings.get('click_type', 'left'))
                self.hotkey_var.set(settings.get('hotkey', 'f6'))
                self.click_position = settings.get('click_position')
                
                if self.click_position:
                    x, y = self.click_position
                    self.position_var.set(f"Posição: ({x}, {y})")
                    
                # Atualizar hotkey listener
                self.hotkey = settings.get('hotkey', 'f6')
                self.restart_hotkey_listener()
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            
    def on_closing(self):
        self.is_running = False
        if self.listener:
            self.listener.stop()
        self.root.destroy()
        
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    # Verificar se as bibliotecas estão instaladas
    try:
        import pyautogui
        import pynput
    except ImportError as e:
        print("Erro: Bibliotecas necessárias não encontradas!")
        print("Execute os comandos abaixo para instalar:")
        print("pip install pyautogui")
        print("pip install pynput")
        exit(1)
    
    app = AutoClicker()
    app.run()