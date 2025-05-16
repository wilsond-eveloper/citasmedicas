import tkinter as tk
from tkinter import messagebox
from openpyxl import Workbook 
from openpyxl import load_workbook 
from openpyxl.styles import Font, Color, PatternFill 
from openpyxl.utils import get_column_letter # Funcionalidad para obtener la letra de la columna
import re

# Crear el libro de excel
wb = load_workbook('datos.xlsx')  # load_workbook es una función, no un método
ws = wb.active
# Crear una nueva hoja de excel 
ws.append(['Nombre', 'Apellido', 'Email', 'Edad', 'Sexo'])

# Guardar cambios
wb.save('datos.xlsx')  # Cargar el libro de excel

# Función para guardar los datos en el archivo de excel
def guardar_datos():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    email = entry_email.get()   
    edad = entry_edad.get()
    sexo = sexo_var.get()

    if not nombre or not apellido or not email or not edad:
        messagebox.showerror("Error", "Por favor, completa todos los campos.")
        return
    try:
        edad = int(edad)
    except ValueError:
        messagebox.showerror("Error", "La edad debe ser un número.")
        return

    # Validar el formato del email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Error", "El formato del email es incorrecto.")
        return

    ws.append([nombre, apellido, email, edad, sexo]) # Agregar los datos a la hoja de excel 
    wb.load_workbook('datos.xlsx') # Guardar el archivo de excel
    messagebox.showinfo("Éxito", "Los datos se han guardado correctamente.")



root = tk.Tk()
root.title("Formulario de Registro")
root.config(bg='#4b6587')
root.geometry("700x400") # Tamaño de la ventana
root.resizable(False, False) # No se puede cambiar el tamaño de la ventana
label_style = {
    'bg': '#4b6587',
    'fg': '#f7fff7',
    'font': ('Arial', 12)
}
entry_style = {
    'bg': '#f7fff7',
    'fg': '#4b6587',
    'font': ('Arial', 12)
}

label_nombre = tk.Label(root, text="Nombre", **label_style)
label_nombre.grid(row=0, column=0, padx=10, pady=10)
entry_nombre = tk.Entry(root, **entry_style)
entry_nombre.grid(row=0, column=1, padx=10, pady=10)

label_apellido = tk.Label(root, text="Apellido", **label_style)
label_apellido.grid(row=1, column=0, padx=10, pady=10)
entry_apellido = tk.Entry(root, **entry_style)
entry_apellido.grid(row=1, column=1, padx=10, pady=10)

label_email = tk.Label(root, text="Email", **label_style)
label_email.grid(row=2, column=0, padx=10, pady=10)
entry_email = tk.Entry(root, **entry_style)
entry_email.grid(row=2, column=1, padx=10, pady=10)

label_edad = tk.Label(root, text="Edad", **label_style)
label_edad.grid(row=3, column=0, padx=10, pady=10)    
entry_edad = tk.Entry(root, **entry_style)
entry_edad.grid(row=3, column=1, padx=10, pady=10)

label_sexo = tk.Label(root, text="Sexo", **label_style)
label_sexo.grid(row=4, column=0, padx=10, pady=10)    
sexo_var = tk.StringVar()
sexo_var.set("Masculino") # Valor por defecto
sexo_masculino = tk.Radiobutton(root, text="Masculino", variable=sexo_var, value="Masculino", **label_style)
sexo_femenino = tk.Radiobutton(root, text="Femenino", variable=sexo_var, value="Femenino", **label_style)
sexo_masculino.grid(row=4, column=1, padx=10, pady=10)
sexo_femenino.grid(row=4, column=2, padx=10, pady=10)


boton_guardar = tk.Button(root, text="Guardar", command=guardar_datos, **label_style, width=40)
boton_guardar.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop() # Para que la ventana se mantenga abierta