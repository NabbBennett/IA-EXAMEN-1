import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog


# ===============CONFIGURACIÓN ===============

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("JUEGO DEL ROMPECABEZAS ")
ventana.geometry("900x900")
ventana.configure(fg_color="#e6eafd")

titulos = ctk.CTkFont(family="Lilita One", size=50, weight="bold")
subtitulos = ctk.CTkFont(family="Lilita One", size=25, weight="bold")
botones = ctk.CTkFont(family="Lilita One", size=21, weight="bold")
texto   = ctk.CTkFont(family="Roboto", size=20, weight="normal")

# ================ PANTALLA ================

titulo = ctk.CTkLabel(
    master=ventana,
    text="JUEGO DEL\nROMPECABEZAS",
    font=titulos,
    text_color="#3a3d81",
    fg_color="transparent"
)
titulo.place(relx=0.5, rely=0.45, anchor="center")

boton = ctk.CTkButton(
    master=ventana,
    text="Ingresar archivo",
    font=botones,
    corner_radius=32,
    fg_color="#3a3d81",
    hover_color="#b0bfe9",
    text_color="#ffffff",
    hover=True,
)
boton.place(relx=0.5, rely=0.7, anchor="center")

widgets_datos = []

boton_regresar = ctk.CTkButton(
    master=ventana,
    text="Regresar",
    font=botones,
    width=140,
    height=40,
    corner_radius=20,
    fg_color="#b0bfe9",
    hover_color="#8fa3dd",
    text_color="#3a3d81",
    command=lambda: retroceder(),
)

boton_continuar = ctk.CTkButton(
    master=ventana,
    text="Continuar",
    font=botones,
    width=140,
    height=40,
    corner_radius=20,
    fg_color="#3a3d81",
    hover_color="#b0bfe9",
    text_color="#ffffff",
    command=lambda: continuar(),
)

# =============== FUNCIONES ===============

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Archivos de texto", "*.txt")]
    )
    if not archivo:
        return

    try:
        with open(archivo, 'r') as f:
            contenido = f.read().strip().splitlines()

        n = int(contenido[0].strip())

        # Validar que haya suficientes líneas
        if len(contenido) < 2 * n + 1:
            print("Error: el archivo no tiene suficientes filas.")
            return

        # Parseo tolerante a comas y espacios
        def parsear_fila(linea):
            return [int(x.strip()) for x in linea.split(',')]

        inicio = [parsear_fila(row) for row in contenido[1:n+1]]
        final  = [parsear_fila(row) for row in contenido[n+1:2*n+1]]

        # Validar dimensiones
        for fila in inicio + final:
            if len(fila) != n:
                print("Error: una fila no coincide con el tamaño n.")
                return

    except (ValueError, IndexError) as e:
        print(f"Error al leer el archivo: {e}")
        return

    iniciar_transicion(n, inicio, final)


def iniciar_transicion(n, inicio, final):
    boton.configure(state="disabled")
    boton.place_forget()
    ventana.datos = (n, inicio, final)
    animar_titulo(paso=0)


def animar_titulo(paso):
    total_pasos = 25
    inicio_y = 0.45
    final_y = 0.15

    if paso > total_pasos:
        n, inicio, final = ventana.datos
        mostrar_datos(n, inicio, final)
        return

    t = paso / total_pasos
    nueva_y = inicio_y + (final_y - inicio_y) * t
    titulo.place(relx=0.5, rely=nueva_y, anchor="center")
    ventana.after(10, lambda: animar_titulo(paso + 1))


def mostrar_datos(n, inicio, final):
    limpiar_widgets_datos()

    label_tam = ctk.CTkLabel(
        master=ventana,
        text=f"Matriz de {n} x {n}",
        font=texto,
        text_color="#3a3d81",
        fg_color="transparent"
    )
    label_tam.place(relx=0.5, rely=0.25, anchor="center")
    widgets_datos.append(label_tam)

    # Contenedor de matrices
    contenedor = ctk.CTkFrame(master=ventana, fg_color="transparent")
    contenedor.place(relx=0.5, rely=0.25, anchor="n", y=60)
    widgets_datos.append(contenedor)

    dibujar_matriz(contenedor, inicio, titulo_texto="Inicio", columna=0)
    dibujar_matriz(contenedor, final,  titulo_texto="Final",  columna=1)

    # Botones
    boton_regresar.place(relx=0.42, rely=0.90, anchor="center")
    boton_continuar.place(relx=0.58, rely=0.90, anchor="center")


def dibujar_matriz(parent, matriz, titulo_texto, columna):
    n = len(matriz)
    espacio = 330
    lado = max(12, min(55, espacio // n))
    pad = max(2, lado // 10)

    fuente_celda = ctk.CTkFont(
        family="Roboto",
        size=max(9, lado // 3),
        weight="bold"
    )

    marco = ctk.CTkFrame(parent, fg_color="transparent")
    marco.grid(row=0, column=columna, padx=40)

    ctk.CTkLabel(
        master=marco,
        text=titulo_texto,
        font=subtitulos,
        text_color="#3a3d81",
        fg_color="transparent"
    ).grid(row=0, column=0, columnspan=n, pady=(0, 15))

    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):
            es_vacio = (valor == 0)
            celda = ctk.CTkLabel(
                master=marco,
                text=str(valor) if not es_vacio else "0",
                font=fuente_celda,
                width=lado,
                height=lado,
                corner_radius=lado // 2,
                fg_color="#b0bfe9" if es_vacio else "#3a3d81",
                text_color="#3a3d81" if es_vacio else "#ffffff"
            )
            celda.grid(row=i + 1, column=j, padx=pad, pady=pad)
            
# Segunda pantalla: Procedimiento 

def limpiar_widgets_datos():
    for w in widgets_datos:
        w.destroy()
    widgets_datos.clear()


def retroceder():
    boton_regresar.place_forget()
    boton_continuar.place_forget()
    limpiar_widgets_datos()

    titulo.configure(text="JUEGO DEL\nROMPECABEZAS")
    titulo.place(relx=0.5, rely=0.35, anchor="center")

    boton.configure(state="normal")
    boton.place(relx=0.5, rely=0.65, anchor="center")


def continuar():
    limpiar_widgets_datos()
    boton_regresar.place_forget()
    boton_continuar.place_forget()
    titulo.place_forget()

    label_procedimiento = ctk.CTkLabel(
        master=ventana,
        text="Procedimiento",
        font=subtitulos,
        fg_color="#3a3d81",
        text_color="#ffffff",
        corner_radius=12
    )
    label_procedimiento.place(relx=0.5, rely=0.1, anchor="center")
    widgets_datos.append(label_procedimiento)

#procedimiento para resolver el rompecabezas 
    #ALGORITMO: IDA*
    
# Conectamos el botón inicial
boton.configure(command=seleccionar_archivo)

ventana.mainloop()