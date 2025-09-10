# Importación de librerías
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# ------------------- FUNCIÓN PARA PACIENTES -------------------
def enmascarar_fecha(texto):
    limpio = ''.join(filter(str.isdigit, texto))
    formato_final = ""

    if len(limpio) > 8:
        limpio = limpio[:8]
    if len(limpio) > 4:
        formato_final = f"{limpio[:2]}-{limpio[2:4]}-{limpio[4:]}"
    elif len(limpio) > 2:
        formato_final = f"{limpio[:2]}-{limpio[2:]}"
    else:
        formato_final = limpio

    if fechaN.get() != formato_final:
        fechaN.delete(0, tk.END)
        fechaN.insert(0, formato_final)

    if len(fechaN.get()) == 10:
        try:
            fecha_actual = datetime.now().date()
            fecha_nacimiento = datetime.strptime(fechaN.get(), "%d-%m-%Y").date()
            edad = fecha_actual.year - fecha_nacimiento.year
            if (fecha_actual.month, fecha_actual.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
                edad -= 1
            edadVar.set(edad)
        except:
            edadVar.set("")
    else:
        edadVar.set("")
    return True

# ------------------- FUNCIONES PARA DOCTORES -------------------
def registrar_doctor():
    nombre = entryNombreD.get().strip()
    especialidad = especialidadD.get().strip()
    edad = entryEdadD.get().strip()
    telefono = entryTelefonoD.get().strip()

    if not nombre or not especialidad or not edad or not telefono:
        messagebox.showwarning("Campos vacíos", "Por favor complete todos los campos.")
        return

    treeviewD.insert("", tk.END, values=(nombre, especialidad, edad, telefono))

    # limpiar campos
    entryNombreD.delete(0, tk.END)
    especialidadD.set("")
    entryEdadD.delete(0, tk.END)
    entryTelefonoD.delete(0, tk.END)

def eliminar_doctor():
    seleccionado = treeviewD.selection()
    if not seleccionado:
        messagebox.showwarning("Eliminar", "Seleccione un doctor para eliminar.")
        return
    for item in seleccionado:
        treeviewD.delete(item)

# ------------------- CREACIÓN DE VENTANA -------------------
ventanaPrincipal = tk.Tk()
ventanaPrincipal.title("Libro de Pacientes y Doctores")
ventanaPrincipal.geometry("890x600")

# Crear contenedor NoteBook (pestañas)
pestañas = ttk.Notebook(ventanaPrincipal)

# Crear frames
framePacientes = ttk.Frame(pestañas)
frameDoctores = ttk.Frame(pestañas)

# Agregar pestañas al NoteBook
pestañas.add(framePacientes, text="Pacientes")
pestañas.add(frameDoctores, text="Doctores")
pestañas.pack(expand=True, fill="both")

# ------------------- PESTAÑA PACIENTES -------------------
# Nombre
labelNombre = tk.Label(framePacientes, text=" Nombre Completo:")
labelNombre.grid(row=0, column=0, padx=5, pady=5, sticky="w")
nombreP = tk.Entry(framePacientes)
nombreP.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Fecha de nacimiento
labelFechaN = tk.Label(framePacientes, text=" Fecha de Nacimiento:")
labelFechaN.grid(row=1, column=0, padx=5, pady=5, sticky="w")
validacion_fecha = ventanaPrincipal.register(enmascarar_fecha)
fechaN = ttk.Entry(framePacientes, validate="key", validatecommand=(validacion_fecha, '%P'))
fechaN.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Edad (readonly)
labelEdad = tk.Label(framePacientes, text=" Edad:")
labelEdad.grid(row=2, column=0, padx=5, pady=5, sticky="w")
edadVar = tk.StringVar()
edadP = tk.Entry(framePacientes, textvariable=edadVar, state="readonly")
edadP.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Género
labelGenero = tk.Label(framePacientes, text=" Género:")
labelGenero.grid(row=3, column=0, padx=5, pady=5, sticky="w")
genero = tk.StringVar()
genero.set("Masculino")
radioMasculino = ttk.Radiobutton(framePacientes, text="Masculino", variable=genero, value="Masculino")
radioMasculino.grid(row=3, column=1, padx=5, sticky="w")
radioFemenino = ttk.Radiobutton(framePacientes, text="Femenino", variable=genero, value="Femenino")
radioFemenino.grid(row=4, column=1, padx=5, sticky="w")

# Grupo sanguíneo
labelGrupoS = tk.Label(framePacientes, text=" Grupo Sanguíneo:")
labelGrupoS.grid(row=5, column=0, padx=5, pady=5, sticky="w")
entryGrupoS = tk.Entry(framePacientes)
entryGrupoS.grid(row=5, column=1, padx=5, pady=5, sticky="w")

# Tipo de seguro
labelTipoS = tk.Label(framePacientes, text=" Tipo de Seguro:")
labelTipoS.grid(row=6, column=0, padx=5, pady=5, sticky="w")
tipoSeguro = tk.StringVar()
tipoSeguro.set("Público")
comboTipoS = ttk.Combobox(framePacientes, values=["Público", "Privado", "Ninguno"], textvariable=tipoSeguro)
comboTipoS.grid(row=6, column=1, padx=5, pady=5, sticky="w")

# Tipo de centro médico
labelCentroM = tk.Label(framePacientes, text=" Centro Médico:")
labelCentroM.grid(row=7, column=0, padx=5, pady=5, sticky="w")
centroM = tk.StringVar()
centroM.set("Hospital Central")
comboCentroM = ttk.Combobox(framePacientes, values=["Hospital Central", "Clínica Norte", "Centro Salud Sur"], textvariable=centroM)
comboCentroM.grid(row=7, column=1, padx=5, pady=5, sticky="w")

# Frame para botones pacientes
btnFrame = tk.Frame(framePacientes)
btnFrame.grid(row=8, column=1, columnspan=2, pady=5, sticky="w")
btnRegistrar = tk.Button(btnFrame, text="Registrar", bg="green", fg="white", command="")
btnRegistrar.grid(row=0, column=0, padx=5)
btnEliminar = tk.Button(btnFrame, text="Eliminar", bg="red", fg="White", command="")
btnEliminar.grid(row=0, column=1, padx=5)

# Treeview para pacientes
treeview = ttk.Treeview(framePacientes, columns=("Nombre", "FechaN", "Edad", "Género", "GrupoS", "TipoS", "CentroM"), show="headings")
treeview.heading("Nombre", text="Nombre")
treeview.heading("FechaN", text="Fecha de Nacimiento")
treeview.heading("Edad", text="Edad")
treeview.heading("Género", text="Género")
treeview.heading("GrupoS", text="Grupo Sanguíneo")
treeview.heading("TipoS", text="Tipo de Seguro")
treeview.heading("CentroM", text="Centro Médico")
treeview.column("Nombre", width=200)
treeview.column("FechaN", width=120)
treeview.column("Edad", width=50)
treeview.column("Género", width=100)
treeview.column("GrupoS", width=100)
treeview.column("TipoS", width=100)
treeview.column("CentroM", width=150)
treeview.grid(row=9, column=0, columnspan=4, padx=5, pady=5)
scrollbar = ttk.Scrollbar(framePacientes, orient="vertical", command=treeview.yview)
treeview.configure(yscroll=scrollbar.set)
scrollbar.grid(row=9, column=4, sticky="ns")

# ------------------- PESTAÑA DOCTORES -------------------
# Nombre
labelNombreD = tk.Label(frameDoctores, text="Nombre:")
labelNombreD.grid(row=0, column=0, padx=5, pady=5, sticky="w")
entryNombreD = tk.Entry(frameDoctores)
entryNombreD.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Especialidad
labelEspecialidadD = tk.Label(frameDoctores, text="Especialidad:")
labelEspecialidadD.grid(row=1, column=0, padx=5, pady=5, sticky="w")
especialidadD = tk.StringVar()
comboEspecialidadD = ttk.Combobox(frameDoctores, values=["Cardiología", "Dermatología", "Neurología", "Pediatría", "Ginecología", "Ortopedia"], textvariable=especialidadD, state="readonly")
comboEspecialidadD.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Edad
labelEdadD = tk.Label(frameDoctores, text="Edad:")
labelEdadD.grid(row=2, column=0, padx=5, pady=5, sticky="w")
entryEdadD = tk.Spinbox(frameDoctores, from_=0, to=100, width=5)
entryEdadD.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Teléfono
labelTelefonoD = tk.Label(frameDoctores, text="Teléfono:")
labelTelefonoD.grid(row=3, column=0, padx=5, pady=5, sticky="w")
entryTelefonoD = tk.Entry(frameDoctores)
entryTelefonoD.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Frame botones doctores
btnFrameD = tk.Frame(frameDoctores)
btnFrameD.grid(row=4, column=1, columnspan=2, pady=5, sticky="w")
btnRegistrarD = tk.Button(btnFrameD, text="Registrar", bg="green", fg="white", command=registrar_doctor)
btnRegistrarD.grid(row=0, column=0, padx=5)
btnEliminarD = tk.Button(btnFrameD, text="Eliminar", bg="red", fg="white", command=eliminar_doctor)
btnEliminarD.grid(row=0, column=1, padx=5)

# Treeview doctores
treeviewD = ttk.Treeview(frameDoctores, columns=("Nombre", "Especialidad", "Edad", "Teléfono"), show="headings")
treeviewD.heading("Nombre", text="Nombre")
treeviewD.heading("Especialidad", text="Especialidad")
treeviewD.heading("Edad", text="Edad")
treeviewD.heading("Teléfono", text="Teléfono")
treeviewD.column("Nombre", width=180)
treeviewD.column("Especialidad", width=140)
treeviewD.column("Edad", width=60)
treeviewD.column("Teléfono", width=120)
treeviewD.grid(row=5, column=0, columnspan=4, padx=5, pady=5)
scrollbarD = ttk.Scrollbar(frameDoctores, orient="vertical", command=treeviewD.yview)
treeviewD.configure(yscroll=scrollbarD.set)
scrollbarD.grid(row=5, column=4, sticky="ns")

ventanaPrincipal.mainloop()
