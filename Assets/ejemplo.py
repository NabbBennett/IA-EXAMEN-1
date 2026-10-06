import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import threading
import time
from collections import deque


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

    espacio = 380
    ancho = max(30, min(60, espacio // n))
    pad = max(3, ancho // 10)
    alto = ancho

    fuente_num = ctk.CTkFont(
        family="Roboto",
        size=max(10, ancho // 3),
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

            celda = ctk.CTkFrame(
                master=marco,
                fg_color="#b0bfe9" if es_vacio else "#3a3d81",
                corner_radius=10,
                width=ancho,
                height=alto,
                border_width=0
            )
            celda.grid(row=i + 1, column=j, padx=pad, pady=pad)
            celda.grid_propagate(False)

            label_num = ctk.CTkLabel(
                master=celda,
                text=str(valor),
                font=fuente_num,
                text_color="#3a3d81" if es_vacio else "#ffffff",
                fg_color="transparent"
            )
            label_num.place(relx=0.5, rely=0.5, anchor="center")

def limpiar_widgets_datos():
    for w in widgets_datos:
        try:
            w.destroy()
        except Exception:
            pass
    widgets_datos.clear()


def retroceder():
    ventana.animacion_activa = False
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
    calcular_heuristica(n, inicio, final)

# ==============================================================
# HEURISTICAS
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


def _tabla_walking_distance(n, meta, por_columnas=False):
    if n > 4:
        return None

    objetivo = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            valor = meta[i][j]
            if valor != 0:
                grupo = i if not por_columnas else j
                objetivo[grupo][grupo] += 1

    fila_blanco = next(
        (i if not por_columnas else j
         for i in range(n)
         for j in range(n)
         if meta[i][j] == 0),
        n - 1
    )
    inicial = (tuple(tuple(fila) for fila in objetivo), fila_blanco)
    distancias = {inicial: 0}
    pendientes = deque([inicial])

    while pendientes:
        conteos, fila_cero = pendientes.popleft()
        distancia = distancias[(conteos, fila_cero)]

        for nueva_fila in (fila_cero - 1, fila_cero + 1):
            if not 0 <= nueva_fila < n:
                continue
            for grupo in range(n):
                if conteos[nueva_fila][grupo] == 0:
                    continue
                siguiente = [list(fila) for fila in conteos]
                siguiente[nueva_fila][grupo] -= 1
                siguiente[fila_cero][grupo] += 1
                clave = (tuple(tuple(fila) for fila in siguiente), nueva_fila)
                if clave not in distancias:
                    distancias[clave] = distancia + 1
                    pendientes.append(clave)

    return distancias


_TABLAS_WD = {}


def _walking_distance_direccion(estado, meta, por_columnas):
    n = len(estado)
    clave_tabla = (serializar(meta), por_columnas)
    if clave_tabla not in _TABLAS_WD:
        _TABLAS_WD[clave_tabla] = _tabla_walking_distance(
            n, meta, por_columnas
        )

    tabla = _TABLAS_WD[clave_tabla]
    if tabla is None:
        total = 0
        for i in range(n):
            for j in range(n):
                valor = estado[i][j]
                if valor == 0:
                    continue
                for fi in range(n):
                    for fj in range(n):
                        if meta[fi][fj] == valor:
                            total += abs(
                                (i if not por_columnas else j)
                                - (fi if not por_columnas else fj)
                            )
                            break
        return total

    conteos = [[0] * n for _ in range(n)]
    fila_cero, col_cero = encontrar_cero(estado)
    for i in range(n):
        for j in range(n):
            valor = estado[i][j]
            if valor == 0:
                continue
            for fi in range(n):
                for fj in range(n):
                    if meta[fi][fj] == valor:
                        actual = i if not por_columnas else j
                        objetivo = fi if not por_columnas else fj
                        conteos[actual][objetivo] += 1
                        break

    fila_blanco = fila_cero if not por_columnas else col_cero
    clave = (tuple(tuple(fila) for fila in conteos), fila_blanco)
    return tabla.get(clave, 0)


def heuristica_walking_distance(estado, meta):
    return (
        _walking_distance_direccion(estado, meta, False)
        + _walking_distance_direccion(estado, meta, True)
    )


def heuristica_inversion_distance(estado, meta):
    n = len(estado)
    orden_meta = {
        meta[i][j]: i * n + j
        for i in range(n)
        for j in range(n)
        if meta[i][j] != 0
    }
    secuencia = [
        orden_meta[estado[i][j]]
        for i in range(n)
        for j in range(n)
        if estado[i][j] != 0
    ]
    inversiones = contar_inversiones(secuencia, n)
    return (inversiones + (2 * n - 2)) // (2 * n - 1)


def heuristica_corner_tile(estado, meta):
    n = len(estado)
    posiciones = {
        estado[i][j]: (i, j)
        for i in range(n)
        for j in range(n)
        if estado[i][j] != 0
    }
    posiciones_meta = {
        meta[i][j]: (i, j)
        for i in range(n)
        for j in range(n)
        if meta[i][j] != 0
    }
    h = heuristica_manhattan(estado, meta)
    esquinas = [(0, 0), (0, n - 1), (n - 1, 0), (n - 1, n - 1)]

    for fi, fj in esquinas:
        esquina = meta[fi][fj]
        if esquina == 0 or posiciones.get(esquina) != (fi, fj):
            continue
        vecinos_meta = []
        if fi + 1 < n:
            vecinos_meta.append(meta[fi + 1][fj])
        if fi - 1 >= 0:
            vecinos_meta.append(meta[fi - 1][fj])
        if fj + 1 < n:
            vecinos_meta.append(meta[fi][fj + 1])
        if fj - 1 >= 0:
            vecinos_meta.append(meta[fi][fj - 1])
        conflictos = 0
        for valor in vecinos_meta:
            if valor == 0 or posiciones.get(valor) == posiciones_meta.get(valor):
                continue
            actual = posiciones.get(valor)
            objetivo_vecino = posiciones_meta.get(valor)
            misma_linea = (
                actual[0] == objetivo_vecino[0]
                or actual[1] == objetivo_vecino[1]
            )
            if misma_linea:
                conflictos += 1
        if conflictos >= 2:
            h += 2
    return h


HEURISTICAS = {
    "Manhattan + conflicto lineal": heuristica,
    "Walking Distance": heuristica_walking_distance,
    "Inversion Distance": heuristica_inversion_distance,
    "Corner Tile": heuristica_corner_tile,
}


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
    n = len(inicio)
    flat_ini = [inicio[i][j] for i in range(n) for j in range(n)]
    flat_met = [meta[i][j] for i in range(n) for j in range(n)]

    inv_ini = contar_inversiones(flat_ini, n)
    inv_met = contar_inversiones(flat_met, n)

    if n % 2 == 1:
        return (inv_ini % 2) == (inv_met % 2)
    else:
        fila0_ini = n - (flat_ini.index(0) // n)
        fila0_met = n - (flat_met.index(0) // n)
        return ((inv_ini + fila0_ini) % 2) == ((inv_met + fila0_met) % 2)


# ==============================================================
# IDA*  (Iterative Deepening A*)
# ==============================================================

def ida_estrella(inicio, meta, funcion_heuristica=heuristica,
                 callback_progreso=None):
    inicio_ser = serializar(inicio)
    meta_ser = serializar(meta)

    umbral = funcion_heuristica(inicio, meta)
    camino = [inicio]
    iteraciones = [0]
    iteracion_ida = 0

    while True:
        iteracion_ida += 1
        if callback_progreso:
            callback_progreso(iteraciones[0], iteracion_ida, umbral)

        tt = {}
        resultado = _buscar_con_umbral(
            camino=camino,
            g=0,
            umbral=umbral,
            meta=meta,
            meta_ser=meta_ser,
            contador=iteraciones,
            tt=tt,
            funcion_heuristica=funcion_heuristica
        )

        if resultado[0] == "ENCONTRADO":
            return camino[:], iteraciones[0]

        if resultado[0] == float('inf'):
            return None, iteraciones[0]

        umbral = resultado[0]


def _buscar_con_umbral(camino, g, umbral, meta, meta_ser, contador, tt,
                       funcion_heuristica):
    estado = camino[-1]
    estado_ser = serializar(estado)

    g_previo = tt.get(estado_ser)
    if g_previo is not None and g_previo <= g:
        return (float('inf'), None)
    tt[estado_ser] = g

    h = funcion_heuristica(estado, meta)
    f = g + h

    if f > umbral:
        return (f, None)

    if estado_ser == meta_ser:
        return ("ENCONTRADO", None)

    minimo = float('inf')

    for vecino in vecinos(estado):
        if len(camino) >= 2 and serializar(vecino) == serializar(camino[-2]):
            continue

        vecino_ser = serializar(vecino)
        if any(serializar(c) == vecino_ser for c in camino):
            continue

        camino.append(vecino)
        contador[0] += 1

        resultado, _ = _buscar_con_umbral(
            camino, g + 1, umbral, meta, meta_ser, contador, tt,
            funcion_heuristica
        )

        if resultado == "ENCONTRADO":
            return ("ENCONTRADO", None)

        if isinstance(resultado, (int, float)) and resultado < minimo:
            minimo = resultado

        camino.pop()

    return (minimo, None)


# ==============================================================
# VISTA DE CALCULO Y RESULTADO
# ==============================================================

def comparar_heuristicas(inicio, final):
    resultados = []
    for nombre, funcion in HEURISTICAS.items():
        t0 = time.time()
        camino, nodos = ida_estrella(
            inicio, final, funcion_heuristica=funcion
        )
        resultados.append({
            "nombre": nombre,
            "f_inicial": funcion(inicio, final),
            "nodos": nodos,
            "tiempo": time.time() - t0,
            "camino": camino,
        })
    return resultados


def calcular_heuristica(n, inicio, final):
    limpiar_widgets_datos()
    boton_regresar.place_forget()
    boton_continuar.place_forget()

    titulo.configure(text="Calculo f(n) = g(n) + h(n)  [IDA*]")
    titulo.place(relx=0.5, rely=0.10, anchor="center")

    if not es_resoluble(inicio, final):
        label = ctk.CTkLabel(
            master=ventana,
            text="El rompecabezas NO tiene solucion.\n"
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
        text="Calculando solucion con IDA*...",
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
                f"Iteracion: {iter_ida}\n"
                f"Umbral actual: {umbral}\n"
                f"Nodos expandidos: {nodos}"
            )
        ))

    def resolver():
        resultados = comparar_heuristicas(inicio, final)
        ventana.after(0, lambda: mostrar_resultado(
            n, inicio, final, resultados
        ))

    threading.Thread(target=resolver, daemon=True).start()


def mostrar_resultado(n, inicio, final, resultados):
    limpiar_widgets_datos()

    resultados_validos = [r for r in resultados if r["camino"] is not None]
    if not resultados_validos:
        label = ctk.CTkLabel(
            master=ventana,
            text="No se encontro solucion.",
            font=texto,
            text_color="#3a3d81",
            fg_color="transparent"
        )
        label.place(relx=0.5, rely=0.5, anchor="center")
        widgets_datos.append(label)
        boton_regresar.place(relx=0.5, rely=0.8, anchor="center")
        return

    mejor = min(resultados_validos, key=lambda r: (r["nodos"], r["tiempo"]))
    ventana.tiempo_resolucion = mejor["tiempo"]
    ventana.resultados_algoritmos = resultados
    camino = mejor["camino"]
    lineas = [
        "Comparacion de funciones F(n) = g(n) + h(n)",
        "",
        "Heuristica                         F inicial   Nodos      Tiempo     Pasos",
        "------------------------------------------------------------------------",
    ]
    for resultado in resultados:
        pasos = (
            str(len(resultado["camino"]) - 1)
            if resultado["camino"] is not None else "SIN SOLUCION"
        )
        lineas.append(
            f"{resultado['nombre'][:34]:34} "
            f"{resultado['f_inicial']:>9} "
            f"{resultado['nodos']:>8} "
            f"{resultado['tiempo']:>8.2f} s "
            f"{pasos:>8}"
        )
    lineas.extend([
        "",
        f"Se animara la ruta con menos nodos: {mejor['nombre']}",
    ])

    label = ctk.CTkLabel(
        master=ventana,
        text="\n".join(lineas),
        font=("Courier New", 14),
        text_color="#3a3d81",
        fg_color="transparent",
        justify="center"
    )
    label.place(relx=0.5, rely=0.4, anchor="center")
    widgets_datos.append(label)

    boton_animar = ctk.CTkButton(
        master=ventana,
        text="Ver solucion paso a paso",
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
# ANIMACION DE LA SOLUCION
# ==============================================================

def animar_solucion(n, camino):
    limpiar_widgets_datos()
    mostrar_pasos(camino)
    titulo.place_forget()

    ventana.animacion_activa = True

    label = ctk.CTkLabel(
        master=ventana,
        text="Solucion paso a paso",
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
        command=lambda: detener_y_mostrar(n, camino)
    )
    boton_saltar.place(relx=0.5, rely=0.85, anchor="center")
    widgets_datos.append(boton_saltar)

    def actualizar_paso(idx):
        if not getattr(ventana, "animacion_activa", False):
            return

        try:
            if not celdas[0][0].winfo_exists():
                return
        except Exception:
            return

        if idx >= len(camino):
            mostrar_estadisticas(
                n,
                camino,
                getattr(ventana, "resultados_algoritmos", [])
            )
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


def detener_y_mostrar(n, camino):
    """Detiene la animación y muestra las estadísticas con el tablero final."""
    ventana.animacion_activa = False
    mostrar_estadisticas(
        n,
        camino,
        getattr(ventana, "resultados_algoritmos", [])
    )


# ==============================================================
# PASOS (u, d, l, r)
# ==============================================================

def mostrar_pasos(camino):
    pasos = []
    for k in range(1, len(camino)):
        estado_anterior = camino[k - 1]
        estado_actual = camino[k]
        i0, j0 = encontrar_cero(estado_anterior)
        i1, j1 = encontrar_cero(estado_actual)

        if i1 == i0 - 1 and j1 == j0:
            pasos.append('u')
        elif i1 == i0 + 1 and j1 == j0:
            pasos.append('d')
        elif i1 == i0 and j1 == j0 - 1:
            pasos.append('l')
        elif i1 == i0 and j1 == j0 + 1:
            pasos.append('r')

    print("Pasos para resolver el rompecabezas:")
    print(" -> ".join(pasos))
    print(f"Numero total de pasos: {len(pasos)}")


# ==============================================================
# ESTADISTICAS
# ==============================================================

def dificultad_por_pasos(num_pasos):
    if num_pasos <= 10:
        return "Fácil"
    if num_pasos <= 43:
        return "Medio"
    return "Difícil"


def mostrar_estadisticas(n, camino, resultados=None):
    ventana.animacion_activa = False
    limpiar_widgets_datos()
    titulo.place_forget()
    matriz_final = camino[-1]

    lado = max(40, min(80, 360 // n))
    pad = max(3, lado // 12)
    fuente_celda = ctk.CTkFont(
        family="Roboto",
        size=max(11, lado // 3),
        weight="bold"
    )

    contenedor_izq = ctk.CTkFrame(ventana, fg_color="transparent")
    contenedor_izq.place(relx=0.24, rely=0.47, anchor="center")
    widgets_datos.append(contenedor_izq)

    ctk.CTkLabel(
        contenedor_izq,
        text="Estado final",
        font=subtitulos,
        text_color="#3a3d81",
        fg_color="transparent"
    ).grid(row=0, column=0, columnspan=n, pady=(0, 10))

    for i in range(n):
        for j in range(n):
            v = matriz_final[i][j]
            celda = ctk.CTkLabel(
                contenedor_izq,
                text=str(v),
                font=fuente_celda,
                width=lado,
                height=lado,
                corner_radius=lado // 4,
                fg_color="#b0bfe9" if v == 0 else "#3a3d81",
                text_color="#3a3d81" if v == 0 else "#ffffff"
            )
            celda.grid(row=i + 1, column=j, padx=pad, pady=pad)

    # ---------- Tabla de estadísticas por algoritmo ----------
    
    if not resultados:
        resultados = getattr(ventana, "resultados_algoritmos", [])

    estadisticas = []
    for resultado in resultados:
        camino_algoritmo = resultado["camino"]
        if camino_algoritmo is None:
            estadisticas.append(
                (
                    resultado["nombre"],
                    str(resultado["f_inicial"]),
                    str(resultado["nodos"]),
                    "SIN SOLUCIÓN",
                    "—",
                    "—",
                )
            )
            continue

        pasos_algoritmo = len(camino_algoritmo) - 1
        estadisticas.append((
            resultado["nombre"],
            str(resultado["f_inicial"]),
            str(resultado["nodos"]),
            str(pasos_algoritmo),
            f"{resultado['tiempo']:.2f} s",
            dificultad_por_pasos(pasos_algoritmo),
        ))

    contenedor_der = ctk.CTkFrame(
        ventana,
        width=570,
        height=330,
        fg_color="#ffffff",
        corner_radius=20,
        border_width=2,
        border_color="#3a3d81"
    )
    contenedor_der.place(relx=0.72, rely=0.47, anchor="center")
    contenedor_der.grid_propagate(False)
    widgets_datos.append(contenedor_der)

    ctk.CTkLabel(
        contenedor_der,
        text="Estadísticas",
        font=subtitulos,
        text_color="#3a3d81",
        fg_color="transparent"
    ).grid(row=0, column=0, columnspan=6, padx=10, pady=(15, 8))

    encabezados = (
        "Algoritmo",
        "F inicial",
        "Nodos",
        "Pasos",
        "Tiempo",
        "Dificultad",
    )
    anchos_columnas = (190, 70, 75, 60, 80, 95)
    for columna, ancho in enumerate(anchos_columnas):
        contenedor_der.grid_columnconfigure(
            columna,
            minsize=ancho,
            weight=1 if columna == 0 else 0
        )

    for columna, encabezado in enumerate(encabezados):
        ctk.CTkLabel(
            contenedor_der,
            text=encabezado,
            font=("Roboto", 12, "bold"),
            text_color="#3a3d81",
            fg_color="transparent"
        ).grid(
            row=1,
            column=columna,
            sticky="w" if columna == 0 else "nsew",
            padx=4,
            pady=(3, 6)
        )

    for fila, valores in enumerate(estadisticas, start=2):
        for columna, valor in enumerate(valores):
            alineacion = "w" if columna == 0 else ""
            ctk.CTkLabel(
                contenedor_der,
                text=valor,
                font=("Roboto", 11),
                text_color="#3a3d81",
                fg_color="transparent"
            ).grid(
                row=fila,
                column=columna,
                sticky=alineacion,
                padx=4,
                pady=5
            )

    boton_regresar.place(relx=0.5, rely=0.92, anchor="center")

# ==============================================================
# ESTADISTICAS (generar )
# ==============================================================


# ==============================================================
# INICIO
# ==============================================================

ventana.animacion_activa = False
ventana.tiempo_resolucion = 0.0

boton.configure(command=seleccionar_archivo)

ventana.mainloop()