import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import openpyxl
from openpyxl import Workbook
import os
import re
from datetime import datetime

class SistemaCitas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Citas Médicas")
        self.root.geometry("1200x700")
        
        # Variables para los campos
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.apellido_var = tk.StringVar()
        self.edad_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.sexo_var = tk.StringVar(value="Masculino")
        
        # Lista para almacenar citas
        self.citas = []
        self.contador_id = 1
        
        self.crear_widgets()
        self.cargar_citas()
    
    def crear_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame de formulario
        form_frame = ttk.LabelFrame(main_frame, text="Datos del Paciente", padding="10")
        form_frame.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
        
        # Campos del formulario
        ttk.Label(form_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.id_var, state="readonly").grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.nombre_var).grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(form_frame, text="Apellido:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.apellido_var).grid(row=2, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(form_frame, text="Edad:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.edad_var).grid(row=3, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(form_frame, textvariable=self.email_var).grid(row=4, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(form_frame, text="Sexo:").grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Combobox(form_frame, textvariable=self.sexo_var, 
                    values=["Masculino", "Femenino", "Otro"]).grid(row=5, column=1, sticky=tk.EW, pady=5)
        
        # Botones CRUD
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Nuevo", command=self.nueva_cita).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Guardar", command=self.guardar_cita).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Editar", command=self.editar_cita).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar", command=self.eliminar_cita).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exportar a Excel", command=self.exportar_excel).pack(side=tk.LEFT, padx=5)
        
        # Frame para las tablas
        tables_frame = ttk.Frame(main_frame)
        tables_frame.grid(row=1, column=0, sticky=tk.NSEW, pady=10)
        
        # Notebook (pestañas) para las tablas
        notebook = ttk.Notebook(tables_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Pestaña de Citas
        citas_tab = ttk.Frame(notebook)
        notebook.add(citas_tab, text="Citas Médicas")
        
        # Treeview para mostrar citas
        self.tree = ttk.Treeview(citas_tab, columns=("ID", "Nombre", "Apellido", "Edad", "Email", "Sexo"), 
                                show="headings", selectmode="browse")
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellido", text="Apellido")
        self.tree.heading("Edad", text="Edad")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Sexo", text="Sexo")
        
        # Ajustar anchos de columnas
        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Nombre", width=150)
        self.tree.column("Apellido", width=150)
        self.tree.column("Edad", width=50, anchor=tk.CENTER)
        self.tree.column("Email", width=200)
        self.tree.column("Sexo", width=100, anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(citas_tab, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        

        # Evento de selección en el treeview
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_cita)
        
        # Configurar el grid para que se expanda
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        form_frame.columnconfigure(1, weight=1)
    
    def validar_campos(self):
        # Validar nombre y apellido (solo letras y espacios)
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', self.nombre_var.get()):
            messagebox.showerror("Error", "El nombre solo puede contener letras y espacios")
            return False
        
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', self.apellido_var.get()):
            messagebox.showerror("Error", "El apellido solo puede contener letras y espacios")
            return False
        
        # Validar edad (número entre 1 y 120)
        try:
            edad = int(self.edad_var.get())
            if edad < 1 or edad > 120:
                messagebox.showerror("Error", "La edad debe estar entre 1 y 120 años")
                return False
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número válido")
            return False
        
        # Validar email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', self.email_var.get()):
            messagebox.showerror("Error", "Ingrese un email válido")
            return False
        
        return True
    
    def limpiar_campos(self):
        self.id_var.set("")
        self.nombre_var.set("")
        self.apellido_var.set("")
        self.edad_var.set("")
        self.email_var.set("")
        self.sexo_var.set("Masculino")
    
    def nueva_cita(self):
        self.limpiar_campos()
        nuevo_id = str(self.contador_id)
        self.id_var.set(nuevo_id)
        self.registrar_cambio("Nuevo", nuevo_id, "Preparando nueva cita")
    
    def guardar_cita(self):
        if not self.validar_campos():
            return
        
        if not self.id_var.get():
            messagebox.showerror("Error", "Seleccione 'Nuevo' para crear una cita")
            return
        
        id_cita = self.id_var.get()
        
        # Crear diccionario con los datos
        cita = {
            "id": id_cita,
            "nombre": self.nombre_var.get(),
            "apellido": self.apellido_var.get(),
            "edad": self.edad_var.get(),
            "email": self.email_var.get(),
            "sexo": self.sexo_var.get()
        }
        
        # Verificar si es nuevo o edición
        if not any(c['id'] == id_cita for c in self.citas):
            # Nueva cita
            self.citas.append(cita)
            self.contador_id += 1
            self.registrar_cambio("Creación", id_cita, 
                                 f"Nuevo paciente: {cita['nombre']} {cita['apellido']}")
            mensaje = "Cita creada correctamente"
        else:
            # Edición de cita existente
            for i, c in enumerate(self.citas):
                if c['id'] == id_cita:
                    cambios = []
                    for key in c:
                        if c[key] != cita[key]:
                            cambios.append(f"{key}: {c[key]} → {cita[key]}")
                    self.citas[i] = cita
                    if cambios:
                        self.registrar_cambio("Edición", id_cita, "; ".join(cambios))
                    break
            mensaje = "Cita actualizada correctamente"
        
        self.actualizar_treeview()
        self.limpiar_campos()
        messagebox.showinfo("Éxito", mensaje)
    
    def editar_cita(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione una cita para editar")
            return
        
        item = self.tree.item(seleccionado)
        valores = item['values']
        
        self.id_var.set(valores[0])
        self.nombre_var.set(valores[1])
        self.apellido_var.set(valores[2])
        self.edad_var.set(valores[3])
        self.email_var.set(valores[4])
        self.sexo_var.set(valores[5])
        
        self.registrar_cambio("Preparar edición", valores[0], "Cita cargada para edición")
    
    def eliminar_cita(self):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Seleccione una cita para eliminar")
            return
        
        item = self.tree.item(seleccionado)
        id_cita = item['values'][0]
        nombre = item['values'][1]
        apellido = item['values'][2]
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la cita de {nombre} {apellido}?"):
            self.citas = [c for c in self.citas if c['id'] != id_cita]
            self.actualizar_treeview()
            self.registrar_cambio("Eliminación", id_cita, f"Paciente: {nombre} {apellido}")
            messagebox.showinfo("Éxito", "Cita eliminada correctamente")
    
    def seleccionar_cita(self, event):
        seleccionado = self.tree.selection()
        if seleccionado:
            item = self.tree.item(seleccionado)
            valores = item['values']
            
            self.id_var.set(valores[0])
            self.nombre_var.set(valores[1])
            self.apellido_var.set(valores[2])
            self.edad_var.set(valores[3])
            self.email_var.set(valores[4])
            self.sexo_var.set(valores[5])
    
    def actualizar_treeview(self):
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ordenar citas por ID
        citas_ordenadas = sorted(self.citas, key=lambda x: int(x['id']))
        
        # Agregar citas al treeview
        for cita in citas_ordenadas:
            self.tree.insert("", tk.END, values=(
                cita['id'],
                cita['nombre'],
                cita['apellido'],
                cita['edad'],
                cita['email'],
                cita['sexo']
            ))
    
    def cargar_citas(self):
        # Aquí podrías cargar citas desde un archivo si lo deseas
        pass
    
    def exportar_excel(self):
        if not self.citas:
            messagebox.showerror("Error", "No hay citas para exportar")
            return
        
        # Pedir al usuario dónde guardar el archivo
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")],
            title="Guardar como"
        )
        
        if not archivo:
            return  # Usuario canceló
        
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Citas Médicas"
            
            # Encabezados
            ws.append(["ID", "Nombre", "Apellido", "Edad", "Email", "Sexo"])
            
            # Datos
            for cita in self.citas:
                ws.append([
                    cita['id'],
                    cita['nombre'],
                    cita['apellido'],
                    cita['edad'],
                    cita['email'],
                    cita['sexo']
                ])
            
            
            # Guardar el archivo
            wb.save(archivo)
            self.registrar_cambio("Exportar", "Todos", f"Archivo exportado: {archivo}")
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a {archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el archivo: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaCitas(root)
    root.mainloop()