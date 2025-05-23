import tkinter as tk
from tkinter import ttk

class ConfigPantalla:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuración de Pantalla")
        self.root.geometry("400x300")
        
        # Variables de configuración
        self.resolucion = tk.StringVar(value="1280x720")
        self.tema = tk.StringVar(value="claro")
        self.tamaño_fuente = tk.IntVar(value=12)
        
        self.crear_widgets()
    
    def crear_widgets(self):
        # Frame principal
        frame = ttk.Frame(self.root, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Configuración de resolución
        ttk.Label(frame, text="Resolución:").grid(row=0, column=0, sticky=tk.W, pady=5)
        resoluciones = ["800x600", "1024x768", "1280x720", "1920x1080"]
        ttk.Combobox(frame, textvariable=self.resolucion, values=resoluciones).grid(
            row=0, column=1, sticky=tk.EW, pady=5)
        
        # Configuración de tema
        ttk.Label(frame, text="Tema:").grid(row=1, column=0, sticky=tk.W, pady=5)
        temas = ["claro", "oscuro", "azul", "verde"]
        ttk.Combobox(frame, textvariable=self.tema, values=temas).grid(
            row=1, column=1, sticky=tk.EW, pady=5)
        
        # Configuración de tamaño de fuente
        ttk.Label(frame, text="Tamaño de fuente:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Scale(frame, from_=8, to=24, variable=self.tamaño_fuente, orient=tk.HORIZONTAL).grid(
            row=2, column=1, sticky=tk.EW, pady=5)
        
        # Botón para aplicar configuración
        ttk.Button(frame, text="Aplicar Configuración", command=self.aplicar_config).grid(
            row=3, column=0, columnspan=2, pady=20)
        
        # Configurar el grid para que se expanda
        frame.columnconfigure(1, weight=1)
    
    def aplicar_config(self):
        # Aquí iría la lógica para aplicar la configuración
        print(f"Configuración aplicada: Resolución={self.resolucion.get()}, "
              f"Tema={self.tema.get()}, Tamaño de fuente={self.tamaño_fuente.get()}")
        tk.messagebox.showinfo("Configuración", "Configuración aplicada correctamente")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigPantalla(root)
    root.mainloop()