import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import threading
import time


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

ventana = ctk.CTk()
ventana.title("JUEGO DEL ROMPECABEZAS")
ventana.geometry("900x900")
ventana.configure(fg_color="#e6eafd")

titulos = ctk.CTkFont(family="Lilita One", size=50, weight="bold")
subtitulos = ctk.CTkFont(family="Lilita One", size=25, weight="bold")
botones = ctk.CTkFont(family="Lilita One", size=21, weight="bold")
texto = ctk.CTkFont(family="Roboto", size=20, weight="normal")


# ==============================================================
# WIDGETS PRINCIPALES
# ==============================================================

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


# ==============================================================
# CARGA DEL ARCHIVO
# ==============================================================

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

        if len(contenido) < 2 * n + 1:
            print("Error: el archivo no tiene suficientes filas.")
            return

        def parsear_fila(linea):
            return [int(x.strip()) for x in linea.split(',')]

        inicio = [parsear_fila(row) for row in contenido[1:n + 1]]
        final = [parsear_fila(row) for row in contenido[n + 1:2 * n + 1]]

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


# ==============================================================
# VISTA DE MATRICES INICIAL Y FINAL
# ==============================================================

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

    contenedor = ctk.CTkFrame(master=ventana, fg_color="transparent")
    contenedor.place(relx=0.5, rely=0.25, anchor="n", y=60)
    widgets_datos.append(contenedor)

    dibujar_matriz(contenedor, inicio, titulo_texto="Inicio", columna=0)
    dibujar_matriz(contenedor, final, titulo_texto="Final", columna=1)

    boton_continuar.configure(command=lambda: continuar())
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

    n, inicio, final = ventana.datos
    coordenadas(n, inicio, final)


# ==============================================================
# VISTA DE COORDENADAS
# ==============================================================

def coordenadas(n, inicio, final):
    limpiar_widgets_datos()

    label_tam = ctk.CTkLabel(
        master=ventana,
        text=f"Coordenadas de la Matriz {n} x {n}",
        font=subtitulos,
        text_color="#3a3d81",
        fg_color="transparent"
    )
    label_tam.place(relx=0.5, rely=0.10, anchor="center")
    widgets_datos.append(label_tam)

    contenedor = ctk.CTkFrame(master=ventana, fg_color="transparent")
    contenedor.place(relx=0.5, rely=0.18, anchor="n")
    widgets_datos.append(contenedor)

    # Posiciones meta de cada ficha (según la matriz final)
    posiciones_finales = {}
    for x in range(n):
        for y in range(n):
            v = final[x][y]
            if v != 0:
                posiciones_finales[v] = (x + 1, y + 1)

    # Posiciones iniciales (según la matriz de inicio)
    posiciones_iniciales = {}
    for x in range(n):
        for y in range(n):
            v = inicio[x][y]
            if v != 0:
                posiciones_iniciales[v] = (x + 1, y + 1)

    # Matriz de Inicio: muestra posición actual (origen)
    dibujar_matriz_coordenadas(
        contenedor,
        matriz=inicio,
        titulo_texto="Inicio",
        columna=0,
        posiciones_finales=posiciones_finales,
        mostrar_origen=True
    )

    # Matriz Final: muestra la posición que tenía cada ficha al inicio
    dibujar_matriz_coordenadas(
        contenedor,
        matriz=final,
        titulo_texto="Final",
        columna=1,
        posiciones_finales=posiciones_finales,
        mostrar_origen=False
    )

    boton_regresar.place(relx=0.42, rely=0.92, anchor="center")
    boton_continuar.configure(command=lambda: calcular_heuristica(n, inicio, final))
    boton_continuar.place(relx=0.58, rely=0.92, anchor="center")


def dibujar_matriz_coordenadas(parent, matriz, titulo_texto, columna,
                               posiciones_finales, mostrar_origen=True):
    n = len(matriz)

    # Se adapta al tamaño n (igual que dibujar_matriz)
    espacio = 380
    lado = max(14, min(60, espacio // n))
    pad = max(1, lado // 10)

    # Si la celda es muy pequeña, ocultamos el texto de coordenadas
    mostrar_coords = lado >= 28

    fuente_num = ctk.CTkFont(
        family="Roboto",
        size=max(8, lado // 3),
        weight="bold"
    )
    fuente_coord = ctk.CTkFont(
        family="Roboto",
        size=max(6, lado // 5),
        weight="normal"
    )

    marco = ctk.CTkFrame(parent, fg_color="transparent")
    marco.grid(row=0, column=columna, padx=20)

    ctk.CTkLabel(
        master=marco,
        text=titulo_texto,
        font=subtitulos,
        text_color="#3a3d81",
        fg_color="transparent"
    ).grid(row=0, column=0, columnspan=n, pady=(0, 10))

    alto_celda = lado + (lado // 2 if mostrar_coords else 0)

    for i, fila in enumerate(matriz):
        for j, valor in enumerate(fila):
            celda_frame = ctk.CTkFrame(
                master=marco,
                fg_color="#3a3d81" if valor != 0 else "#b0bfe9",
                corner_radius=max(4, lado // 4),
                width=lado,
                height=alto_celda
            )
            celda_frame.grid(row=i + 1, column=j, padx=pad, pady=pad)
            celda_frame.grid_propagate(False)

            label_num = ctk.CTkLabel(
                master=celda_frame,
                text=str(valor),
                font=fuente_num,
                text_color="#ffffff" if valor != 0 else "#3a3d81",
                fg_color="transparent"
            )
            label_num.pack(
                pady=(1, 0) if mostrar_coords else 0,
                expand=not mostrar_coords,
                fill="both" if not mostrar_coords else "none"
            )

            if mostrar_coords:
                if valor != 0:
                    if mostrar_origen:
                        coord = (i + 1, j + 1)
                    else:
                        coord = posiciones_finales.get(valor, (i + 1, j + 1))
                    texto_coord = f"({coord[0]},{coord[1]})"
                else:
                    texto_coord = "—"

                label_coord = ctk.CTkLabel(
                    master=celda_frame,
                    text=texto_coord,
                    font=fuente_coord,
                    text_color="#ffffff" if valor != 0 else "#3a3d81",
                    fg_color="transparent"
                )
                label_coord.pack(pady=(0, 1))


# ==============================================================
# HEURÍSTICAS
# ==============================================================

def heuristica_manhattan(estado, meta):
    n = len(estado)
    pos_meta = {}
    for i in range(n):
        for j in range(n):
            if meta[i][j] != 0:
                pos_meta[meta[i][j]] = (i, j)

    h = 0
    for i in range(n):
        for j in range(n):
            v = estado[i][j]
            if v != 0:
                fi, fj = pos_meta[v]
                h += abs(i - fi) + abs(j - fj)
    return h


def conflicto_lineal(estado, meta):
    n = len(estado)
    total = 0

    pos_meta = {}
    for i in range(n):
        for j in range(n):
            if meta[i][j] != 0:
                pos_meta[meta[i][j]] = (i, j)

    # Conflictos por filas
    for fila in range(n):
        for c1 in range(n):
            v1 = estado[fila][c1]
            if v1 == 0:
                continue
            f1, col1_meta = pos_meta[v1]
            if f1 != fila:
                continue
            for c2 in range(c1 + 1, n):
                v2 = estado[fila][c2]
                if v2 == 0:
                    continue
                f2, col2_meta = pos_meta[v2]
                if f2 != fila:
                    continue
                if col1_meta > col2_meta:
                    total += 2

    # Conflictos por columnas
    for col in range(n):
        for f1 in range(n):
            v1 = estado[f1][col]
            if v1 == 0:
                continue
            fila1_meta, c1 = pos_meta[v1]
            if c1 != col:
                continue
            for f2 in range(f1 + 1, n):
                v2 = estado[f2][col]
                if v2 == 0:
                    continue
                fila2_meta, c2 = pos_meta[v2]
                if c2 != col:
                    continue
                if fila1_meta > fila2_meta:
                    total += 2

    return total


def heuristica(estado, meta):
    return heuristica_manhattan(estado, meta) + conflicto_lineal(estado, meta)


# ==============================================================
# UTILIDADES DEL ROMPECABEZAS
# ==============================================================

def copiar(m):
    return [fila[:] for fila in m]


def encontrar_cero(estado):
    for i, fila in enumerate(estado):
        for j, v in enumerate(fila):
            if v == 0:
                return i, j
    return -1, -1


def vecinos(estado):
    n = len(estado)
    i, j = encontrar_cero(estado)
    movimientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    resultado = []
    for di, dj in movimientos:
        ni, nj = i + di, j + dj
        if 0 <= ni < n and 0 <= nj < n:
            nuevo = copiar(estado)
            nuevo[i][j], nuevo[ni][nj] = nuevo[ni][nj], nuevo[i][j]
            resultado.append(nuevo)
    return resultado


def serializar(estado):
    return tuple(tuple(f) for f in estado)


def contar_inversiones(estado_flat, n):
    seq = [x for x in estado_flat if x != 0]
    inv = 0
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                inv += 1
    return inv


def es_resoluble(inicio, meta):
    """
      - n impar  -> resoluble si inversiones(inicio) y inversiones(meta) tienen la misma paridad.
      - n par    -> depende de la fila del 0 contada desde abajo.
    """
    n = len(inicio)
    flat_ini = [inicio[i][j] for i in range(n) for j in range(n)]
    flat_met = [meta[i][j] for i in range(n) for j in range(n)]

    inv_ini = contar_inversiones(flat_ini, n)
    inv_met = contar_inversiones(flat_met, n)

    if n % 2 == 1:
        return (inv_ini % 2) == (inv_met % 2)
    else:
        # fila del 0 desde abajo (1-indexed)
        fila0_ini = n - (flat_ini.index(0) // n)
        fila0_met = n - (flat_met.index(0) // n)
        return ((inv_ini + fila0_ini) % 2) == ((inv_met + fila0_met) % 2)


# ==============================================================
# IDA*  (Iterative Deepening A*)
# ==============================================================

def ida_estrella(inicio, meta, callback_progreso=None):
    """
    Devuelve (camino, iteraciones) con camino = lista de estados
    desde inicio hasta meta. Si no hay solución, (None, iteraciones).
    """
    inicio_ser = serializar(inicio)
    meta_ser = serializar(meta)

    umbral = heuristica(inicio, meta)
    camino = [inicio]
    iteraciones = [0]
    iteracion_ida = 0

    # Transposition table: estado_ser -> g mínimo visto en esta iteración
    while True:
        iteracion_ida += 1
        if callback_progreso:
            callback_progreso(iteraciones[0], iteracion_ida, umbral)

        tt = {}  # transposition table por iteración

        resultado = _buscar_con_umbral(
            camino=camino,
            g=0,
            umbral=umbral,
            meta=meta,
            meta_ser=meta_ser,
            contador=iteraciones,
            tt=tt
        )

        if resultado[0] == "ENCONTRADO":
            return camino[:], iteraciones[0]

        if resultado[0] == float('inf'):
            return None, iteraciones[0]

        umbral = resultado[0]


def _buscar_con_umbral(camino, g, umbral, meta, meta_ser, contador, tt):
    estado = camino[-1]
    estado_ser = serializar(estado)

    # Poda por transposition table
    g_previo = tt.get(estado_ser)
    if g_previo is not None and g_previo <= g:
        return (float('inf'), None)
    tt[estado_ser] = g

    h = heuristica(estado, meta)
    f = g + h

    if f > umbral:
        return (f, None)

    if estado_ser == meta_ser:
        return ("ENCONTRADO", None)

    minimo = float('inf')

    for vecino in vecinos(estado):
        # Evitar retroceso inmediato
        if len(camino) >= 2 and serializar(vecino) == serializar(camino[-2]):
            continue

        # Evitar ciclos en el camino actual
        vecino_ser = serializar(vecino)
        if any(serializar(c) == vecino_ser for c in camino):
            continue

        camino.append(vecino)
        contador[0] += 1

        resultado, _ = _buscar_con_umbral(
            camino, g + 1, umbral, meta, meta_ser, contador, tt
        )

        if resultado == "ENCONTRADO":
            return ("ENCONTRADO", None)

        if isinstance(resultado, (int, float)) and resultado < minimo:
            minimo = resultado

        camino.pop()

    return (minimo, None)


# ==============================================================
# VISTA DE CÁLCULO Y RESULTADO
# ==============================================================

def calcular_heuristica(n, inicio, final):
    limpiar_widgets_datos()
    boton_regresar.place_forget()
    boton_continuar.place_forget()

    titulo.configure(text="Cálculo f(n) = g(n) + h(n)  [IDA*]")
    titulo.place(relx=0.5, rely=0.10, anchor="center")

    # Verificación de solubilidad (evita búsquedas infinitas)
    if not es_resoluble(inicio, final):
        label = ctk.CTkLabel(
            master=ventana,
            text="El rompecabezas NO tiene solución.\n"
                 "(paridad de inversiones distinta entre inicio y meta)",
            font=texto,
            text_color="#3a3d81",
            fg_color="transparent",
            justify="center"
        )
        label.place(relx=0.5, rely=0.5, anchor="center")
        widgets_datos.append(label)
        boton_regresar.place(relx=0.5, rely=0.8, anchor="center")
        return

    label_estado = ctk.CTkLabel(
        master=ventana,
        text="Calculando solución con IDA*...",
        font=texto,
        text_color="#3a3d81",
        fg_color="transparent",
        justify="center"
    )
    label_estado.place(relx=0.5, rely=0.5, anchor="center")
    widgets_datos.append(label_estado)

    def progreso(nodos, iter_ida, umbral):
        ventana.after(0, lambda: label_estado.configure(
            text=(
                f"Calculando con IDA*...\n"
                f"Iteración: {iter_ida}\n"
                f"Umbral actual: {umbral}\n"
                f"Nodos expandidos: {nodos}"
            )
        ))

    def resolver():
        h_ini = heuristica(inicio, final)
        camino, iteraciones = ida_estrella(inicio, final, callback_progreso=progreso)
        ventana.after(0, lambda: mostrar_resultado(
            n, inicio, final, h_ini, camino, iteraciones
        ))

    threading.Thread(target=resolver, daemon=True).start()


def mostrar_resultado(n, inicio, final, h_ini, camino, iteraciones):
    limpiar_widgets_datos()

    if camino is None:
        label = ctk.CTkLabel(
            master=ventana,
            text="No se encontró solución.",
            font=texto,
            text_color="#3a3d81",
            fg_color="transparent"
        )
        label.place(relx=0.5, rely=0.5, anchor="center")
        widgets_datos.append(label)
        boton_regresar.place(relx=0.5, rely=0.8, anchor="center")
        return

    texto_res = (
        f"Heurística inicial h(inicio) = {h_ini}\n"
        f"Nodos expandidos: {iteraciones}\n"
        f"Longitud de la solución: {len(camino) - 1} movimientos"
    )

    label = ctk.CTkLabel(
        master=ventana,
        text=texto_res,
        font=texto,
        text_color="#3a3d81",
        fg_color="transparent",
        justify="center"
    )
    label.place(relx=0.5, rely=0.4, anchor="center")
    widgets_datos.append(label)

    boton_animar = ctk.CTkButton(
        master=ventana,
        text="Ver solución paso a paso",
        font=botones,
        corner_radius=24,
        fg_color="#3a3d81",
        hover_color="#b0bfe9",
        text_color="#ffffff",
        command=lambda: animar_solucion(n, camino)
    )
    boton_animar.place(relx=0.5, rely=0.6, anchor="center")
    widgets_datos.append(boton_animar)

    boton_regresar.place(relx=0.5, rely=0.8, anchor="center")


# ==============================================================
# ANIMACIÓN DE LA SOLUCIÓN
# ==============================================================

def animar_solucion(n, camino):
    limpiar_widgets_datos()
    titulo.place_forget()

    label = ctk.CTkLabel(
        master=ventana,
        text="Solución paso a paso",
        font=subtitulos,
        text_color="#3a3d81",
        fg_color="transparent"
    )
    label.place(relx=0.5, rely=0.08, anchor="center")
    widgets_datos.append(label)

    contenedor = ctk.CTkFrame(master=ventana, fg_color="transparent")
    contenedor.place(relx=0.5, rely=0.15, anchor="n")
    widgets_datos.append(contenedor)

    lado = max(40, min(80, 360 // n))
    pad = max(3, lado // 12)
    fuente_celda = ctk.CTkFont(
        family="Roboto",
        size=max(11, lado // 3),
        weight="bold"
    )

    marco = ctk.CTkFrame(contenedor, fg_color="transparent")
    marco.pack()

    celdas = []
    for i in range(n):
        fila_celdas = []
        for j in range(n):
            celda = ctk.CTkLabel(
                master=marco,
                text="",
                font=fuente_celda,
                width=lado,
                height=lado,
                corner_radius=lado // 2,
                fg_color="#b0bfe9",
                text_color="#3a3d81"
            )
            celda.grid(row=i, column=j, padx=pad, pady=pad)
            fila_celdas.append(celda)
        celdas.append(fila_celdas)

    label_paso = ctk.CTkLabel(
        master=ventana,
        text=f"Paso 0 de {len(camino) - 1}",
        font=texto,
        text_color="#3a3d81",
        fg_color="transparent"
    )
    label_paso.place(relx=0.5, rely=0.75, anchor="center")
    widgets_datos.append(label_paso)

    boton_saltar = ctk.CTkButton(
        master=ventana,
        text="Ver resultado final",
        font=botones,
        width=220,
        height=40,
        corner_radius=20,
        fg_color="#b0bfe9",
        hover_color="#8fa3dd",
        text_color="#3a3d81",
        command=lambda: mostrar_estado_final(n, camino, celdas, label_paso)
    )
    boton_saltar.place(relx=0.5, rely=0.85, anchor="center")
    widgets_datos.append(boton_saltar)

    def actualizar_paso(idx):
        if idx >= len(camino):
            label_paso.configure(text=f"¡Resuelto! ({len(camino) - 1} movimientos)")
            boton_regresar.place(relx=0.5, rely=0.92, anchor="center")
            return

        estado = camino[idx]
        for i in range(n):
            for j in range(n):
                v = estado[i][j]
                if v == 0:
                    celdas[i][j].configure(
                        text="0",
                        fg_color="#b0bfe9",
                        text_color="#3a3d81"
                    )
                else:
                    celdas[i][j].configure(
                        text=str(v),
                        fg_color="#3a3d81",
                        text_color="#ffffff"
                    )

        label_paso.configure(text=f"Paso {idx} de {len(camino) - 1}")
        ventana.after(400, lambda: actualizar_paso(idx + 1))

    actualizar_paso(0)


def mostrar_estado_final(n, camino, celdas, label_paso):
    estado = camino[-1]
    for i in range(n):
        for j in range(n):
            v = estado[i][j]
            if v == 0:
                celdas[i][j].configure(text="0", fg_color="#b0bfe9", text_color="#3a3d81")
            else:
                celdas[i][j].configure(text=str(v), fg_color="#3a3d81", text_color="#ffffff")
    label_paso.configure(text=f"¡Resuelto! ({len(camino) - 1} movimientos)")
    boton_regresar.place(relx=0.5, rely=0.92, anchor="center")


# ==============================================================
# INICIO
# ==============================================================

boton.configure(command=seleccionar_archivo)

ventana.mainloop()