import tkinter as tk
from tkinter import messagebox

def mostrarEdad():
    edad = spin.get()
    messagebox.showinfo("Edad", f"La edad seleccionada es {edad}")

ventana = tk.Tk()
ventana.title("Selector de Edad")

# Spinbox de números del 1 al 10 para edad
labelEdad = tk.Label(ventana, text="Edad")
labelEdad.grid(row=0, column=0, padx=5, sticky="w")

spin = tk.Spinbox(ventana, from_=1, to=10)
spin.grid(row=0, column=1, padx=10, pady=10)

boton = tk.Button(ventana, text="Obtener valor", command=mostrarEdad)
boton.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

ventana.mainloop()
