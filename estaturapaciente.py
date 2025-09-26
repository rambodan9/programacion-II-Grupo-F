# Importación de librerías
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Función para enmascarar fecha
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
        fecha_actual = datetime.now().date()
        fecha_nacimiento = datetime.strptime(fechaN.get(), "%d-%m-%Y").date()
        edad = fecha_actual.year - fecha_nacimiento.year
        edadVar.set(edad)
    else:
        edadVar.set("")
    return True

# Función para guardar en archivo
def guardar_en_archivo():
    try:
        with open("pacientes.txt", "w", encoding="utf-8") as archivo:
            for paciente in paciente_data:
                archivo.write(
                    f"{paciente['Nombre']} | {paciente['FechaN']} | {paciente['Edad']} | "
                    f"{paciente['Género']} | {paciente['GrupoS']} | {paciente['TipoS']} | "
                    f"{paciente['CentroM']} | {paciente['Estatura']}\n"
                )
        # Guardar también en pacienteestatura.txt
        with open("pacienteestatura.txt", "w", encoding="utf-8") as archivo_est:
            for paciente in paciente_data:
                archivo_est.write(
                    f"{paciente['Nombre']} | {paciente['Estatura']}\n"
                )
        messagebox.showinfo("Éxito", "Datos guardados correctamente en 'pacientes.txt' y 'pacienteestatura.txt'")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")

# Lista de pacientes
paciente_data = []

# Función para registrar paciente
def registrarpaciente():
    if not nombreP.get() or not fechaN.get() or not edadVar.get() or not estaturaP.get():
        messagebox.showwarning("Datos incompletos", "Por favor, complete todos los campos obligatorios.")
        return

    paciente = {
        "Nombre": nombreP.get(),
        "FechaN": fechaN.get(),
        "Edad": edadVar.get(),
        "Género": genero.get(),
        "GrupoS": entryGrupoS.get(),
        "TipoS": tipoSeguro.get(),
        "CentroM": centroM.get(),
        "Estatura": estaturaP.get()
    }
    # Agregar paciente a la lista
    paciente_data.append(paciente)
    
    # Guardar datos en archivo
    guardar_en_archivo()

    # Actualizar la vista del treeview
    cargar_treeview()

    # Limpiar los campos después del registro
    nombreP.delete(0, tk.END)
    fechaN.delete(0, tk.END)
    edadVar.set("")
    entryGrupoS.delete(0, tk.END)
    estaturaP.delete(0, tk.END)
    tipoSeguro.set("Público")
    centroM.set("Hospital Central")
    genero.set("Masculino")

# Función para cargar los datos al Treeview
def cargar_treeview():
    for paciente in treeview.get_children():
        treeview.delete(paciente)

    for i, item in enumerate(paciente_data):
        treeview.insert(
            "", "end", iid=str(i),
            values=(
                item["Nombre"],
                item["FechaN"],
                item["Edad"],
                item["Género"],
                item["GrupoS"],
                item["TipoS"],
                item["CentroM"],
                item["Estatura"]
            )
        )

# Función para eliminar paciente seleccionado
def eliminar_paciente():
    seleccionado = treeview.selection()
    if seleccionado:
        for item in seleccionado:
            treeview.delete(item)
        # Eliminar de la lista paciente_data
        indices_seleccionados = [int(item) for item in seleccionado]
        indices_seleccionados.sort(reverse=True)  # Para eliminar de atrás hacia adelante
        for index in indices_seleccionados:
            paciente_data.pop(index)
        # Guardar cambios en el archivo
        guardar_en_archivo()
    else:
        messagebox.showwarning("Selección inválida", "Seleccione un paciente para eliminar.")

# Crear ventana principal
ventanaPrincipal = tk.Tk()
ventanaPrincipal.title("Libro de Pacientes y Doctores")
ventanaPrincipal.geometry("950x600")

# Crear contenedor NoteBook (pestañas)
pestañas = ttk.Notebook(ventanaPrincipal)

# Crear frames
framePacientes = ttk.Frame(pestañas)
frameDoctores = ttk.Frame(pestañas)

# Agregar pestañas al NoteBook
pestañas.add(framePacientes, text="Pacientes")
pestañas.add(frameDoctores, text="Doctores")

# Mostrar las pestañas en la ventana
pestañas.pack(expand=True, fill="both")

# Crear elementos en la pestaña de Pacientes
# Nombre
labelNombre = tk.Label(framePacientes, text="Nombre Completo:")
labelNombre.grid(row=0, column=0, padx=5, pady=5, sticky="w")
nombreP = tk.Entry(framePacientes)
nombreP.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Fecha de nacimiento
labelFechaN = tk.Label(framePacientes, text="Fecha de Nacimiento:")
labelFechaN.grid(row=1, column=0, padx=5, pady=5, sticky="w")
validacion_fecha = ventanaPrincipal.register(enmascarar_fecha)
fechaN = ttk.Entry(framePacientes, validate="key", validatecommand=(validacion_fecha, '%P'))
fechaN.grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Edad (readonly)
labelEdad = tk.Label(framePacientes, text="Edad:")
labelEdad.grid(row=2, column=0, padx=5, pady=5, sticky="w")
edadVar = tk.StringVar()
edadP = tk.Entry(framePacientes, textvariable=edadVar, state="readonly")
edadP.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Estatura
labelEstatura = tk.Label(framePacientes, text="Estatura (cm):")
labelEstatura.grid(row=3, column=0, padx=5, pady=5, sticky="w")
estaturaP = tk.Entry(framePacientes)
estaturaP.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Género
labelGenero = tk.Label(framePacientes, text="Género:")
labelGenero.grid(row=4, column=0, padx=5, pady=5, sticky="w")
genero = tk.StringVar()
genero.set("Masculino")  # Valor por defecto
radioMasculino = ttk.Radiobutton(framePacientes, text="Masculino", variable=genero, value="Masculino")
radioMasculino.grid(row=4, column=1, padx=5, sticky="w")
radioFemenino = ttk.Radiobutton(framePacientes, text="Femenino", variable=genero, value="Femenino")
radioFemenino.grid(row=5, column=1, padx=5, sticky="w")

# Grupo sanguíneo
labelGrupoS = tk.Label(framePacientes, text="Grupo Sanguíneo:")
labelGrupoS.grid(row=6, column=0, padx=5, pady=5, sticky="w")
entryGrupoS = tk.Entry(framePacientes)
entryGrupoS.grid(row=6, column=1, padx=5, pady=5, sticky="w")

# Tipo de seguro
labelTipoS = tk.Label(framePacientes, text="Tipo de Seguro:")
labelTipoS.grid(row=7, column=0, padx=5, pady=5, sticky="w")
tipoSeguro = tk.StringVar()
tipoSeguro.set("Público")  # Valor por defecto
comboTipoS = ttk.Combobox(framePacientes, values=["Público", "Privado", "Ninguno"], textvariable=tipoSeguro)
comboTipoS.grid(row=7, column=1, padx=5, pady=5, sticky="w")

# Centro médico
labelCentroM = tk.Label(framePacientes, text="Centro Médico:")
labelCentroM.grid(row=8, column=0, padx=5, pady=5, sticky="w")
centroM = tk.StringVar()
centroM.set("Hospital Central")  # Valor por defecto
comboCentroM = ttk.Combobox(framePacientes, values=["Hospital Central", "Clínica Norte", "Centro Salud Sur"], textvariable=centroM)
comboCentroM.grid(row=8, column=1, padx=5, pady=5, sticky="w")

# Botones
btnFrame = tk.Frame(framePacientes)
btnFrame.grid(row=9, column=1, columnspan=2, pady=5, sticky="w")

btnRegistrar = tk.Button(btnFrame, text="Registrar", bg="green", fg="white", command=registrarpaciente)
btnRegistrar.grid(row=0, column=0, padx=5)

btnEliminar = tk.Button(btnFrame, text="Eliminar", bg="red", fg="white", command=eliminar_paciente)
btnEliminar.grid(row=0, column=1, padx=5)

# Treeview para mostrar los pacientes
treeview = ttk.Treeview(framePacientes, columns=("Nombre", "FechaN", "Edad", "Género", "GrupoS", "TipoS", "CentroM", "Estatura"), show="headings")
treeview.heading("Nombre", text="Nombre")
treeview.heading("FechaN", text="Fecha de Nacimiento")
treeview.heading("Edad", text="Edad")
treeview.heading("Género", text="Género")
treeview.heading("GrupoS", text="Grupo Sanguíneo")
treeview.heading("TipoS", text="Tipo de Seguro")
treeview.heading("CentroM", text="Centro Médico")
treeview.heading("Estatura", text="Estatura (cm)")

# Definir el ancho de las columnas
treeview.column("Nombre", width=200)
treeview.column("FechaN", width=120)
treeview.column("Edad", width=50)
treeview.column("Género", width=100)
treeview.column("GrupoS", width=100)
treeview.column("TipoS", width=100)
treeview.column("CentroM", width=150)
treeview.column("Estatura", width=100)

treeview.grid(row=10, column=0, columnspan=4, padx=5, pady=5)

# Scrollbar vertical
scrollbar = ttk.Scrollbar(framePacientes, orient="vertical", command=treeview.yview)
treeview.configure(yscroll=scrollbar.set)
scrollbar.grid(row=10, column=4, sticky="ns")

def cargar_desde_archivo():
    try:
        with open("pacientes.txt", "r", encoding="utf-8") as archivo:
            paciente_data.clear()
            for linea in archivo:
                partes = linea.strip().split(" | ")
                if len(partes) == 8:
                    paciente = {
                        "Nombre": partes[0],
                        "FechaN": partes[1],
                        "Edad": partes[2],
                        "Género": partes[3],
                        "GrupoS": partes[4],
                        "TipoS": partes[5],
                        "CentroM": partes[6],
                        "Estatura": partes[7],
                    }
                    paciente_data.append(paciente)
        cargar_treeview()
    except FileNotFoundError:
        open("pacientes.txt", "w", encoding="utf-8").close()

cargar_desde_archivo()
ventanaPrincipal.mainloop()
