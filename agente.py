import pygame
import sys

# Constantes del juego
ANCHO_VENTANA = 400
ALTO_VENTANA = 400
TAMANO_CASILLA = 100
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
PBLANCAS = (245, 245, 225)  # Color para piezas blancas
PNEGRAS = (71, 71, 70)      # Color para piezas negras
GRIS = (169, 169, 169)      # Color gris para el borde
VERDE = (50, 205, 50)       # Verde para movimientos válidos
TEXTO_COLOR = (50, 50, 60)  # Color del texto (negro)
ROJO = (255, 0, 0)  # Color para el borde de la reina

# Inicialización de contadores
movimientos_totales = 0
fichas_blancas = 2  # Número inicial de fichas blancas
fichas_negras = 2   # Número inicial de fichas negras

# Inicialización de Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Tablero de Damas 4x4")

# Inicializar fuente
fuente = pygame.font.Font(None, 36)

# Representación del tablero (1: ficha blanca, 2: ficha negra, 0: casilla vacía)
tablero = [[0 for _ in range(4)] for _ in range(4)]

# Inicialización de las piezas en el tablero (colocamos dos piezas por jugador)
tablero[0][0] = 1  # Ficha blanca en (0, 0)
tablero[0][2] = 1  # Ficha blanca en (0, 2)
tablero[3][1] = 2  # Ficha negra en (3, 1)
tablero[3][3] = 2  # Ficha negra en (3, 3)

# Variables para controlar la pieza seleccionada y su posición original
pieza_seleccionada = None
posicion_original = None
jugador_turno = 1  # 1 para jugador blanco, 2 para jugador negro
movimientos_disponibles = []  # Lista de movimientos válidos

# Función para dibujar el tablero
def dibujar_tablero():
    for fila in range(4):
        for columna in range(4):
            color = NEGRO if (fila + columna) % 2 == 0 else BLANCO
            pygame.draw.rect(pantalla, color, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))
            pygame.draw.rect(pantalla, NEGRO, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA), 2)  # Bordes

# Función para dibujar los movimientos disponibles
def dibujar_movimientos_disponibles():
    for fila, columna in movimientos_disponibles:
        pygame.draw.rect(pantalla, VERDE, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))

# Función para dibujar las piezas
def dibujar_fichas():
    for fila in range(4):
        for columna in range(4):
            if tablero[fila][columna] == 1 or tablero[fila][columna] == -1:  # Ficha blanca o reina blanca
                pygame.draw.circle(pantalla, GRIS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 3)
                pygame.draw.circle(pantalla, PBLANCAS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3)
                if tablero[fila][columna] == -1:
                    pygame.draw.circle(pantalla, ROJO, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 6, 3)
            elif tablero[fila][columna] == 2 or tablero[fila][columna] == -2:  # Ficha negra o reina negra
                pygame.draw.circle(pantalla, GRIS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 3)
                pygame.draw.circle(pantalla, PNEGRAS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3)
                if tablero[fila][columna] == -2:
                    pygame.draw.circle(pantalla, ROJO, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 6, 3)

# Función para mostrar el turno del jugador
def mostrar_turno():
    texto = fuente.render(f"Turno: {'Blanco' if jugador_turno == 1 else 'Negro'}", True, TEXTO_COLOR)
    pantalla.blit(texto, (10, 10))

# Función para manejar los eventos del ratón
def manejar_eventos():
   
    global pieza_seleccionada, posicion_original, jugador_turno, movimientos_disponibles, movimientos_totales, fichas_negras

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos
            fila = y // TAMANO_CASILLA
            columna = x // TAMANO_CASILLA

            # Asegurarse de que solo las piezas blancas (jugador) puedan ser seleccionadas
            if jugador_turno == 1:  # Si es el turno del jugador (jugador 1 controla las piezas blancas)
                if pieza_seleccionada:
                    if (fila, columna) in movimientos_disponibles:
                        # Mover la pieza
                        movimientos_totales += 1
                        tablero[fila][columna] = pieza_seleccionada
                        tablero[posicion_original[0]][posicion_original[1]] = 0
                        
                        # Convertir en reina si llegamos al borde del tablero
                        if (pieza_seleccionada == 1 and fila == 3) or (pieza_seleccionada == 2 and fila == 0):
                            tablero[fila][columna] = -pieza_seleccionada  # Convertir a reina (negativa para indicar que es reina)
                        
                        # Eliminar pieza capturada si hay captura
                        if abs(fila - posicion_original[0]) == 2:
                            fila_rival = (fila + posicion_original[0]) // 2
                            columna_rival = (columna + posicion_original[1]) // 2
                            tablero[fila_rival][columna_rival] = 0
                            fichas_negras -= 1  # Restamos una ficha blanca
                        
                        pieza_seleccionada = None
                        movimientos_disponibles = []
                        jugador_turno = 2  # Cambiar turno a la IA
                    else:
                        # Si no es un movimiento válido, volver a colocar la pieza seleccionada en su posición original
                        tablero[posicion_original[0]][posicion_original[1]] = pieza_seleccionada
                        pieza_seleccionada = None
                        movimientos_disponibles = []
                elif tablero[fila][columna] == 1:  # Solo seleccionar piezas blancas (jugador 1)
                    pieza_seleccionada = tablero[fila][columna]
                    posicion_original = (fila, columna)
                    tablero[fila][columna] = 0
                    movimientos_disponibles = obtener_movimientos_validos(fila, columna)
            # Si el turno es de la IA, no se hace nada en este bloque, ya que la IA maneja sus propios movimientos

def obtener_movimientos_validos(fila, columna):
    movimientos = []
    pieza = tablero[fila][columna]
    direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for d_fila, d_columna in direcciones:
        nueva_fila, nueva_columna = fila + d_fila, columna + d_columna
        # Movimiento simple
        if 0 <= nueva_fila < 4 and 0 <= nueva_columna < 4 and tablero[nueva_fila][nueva_columna] == 0:
            movimientos.append((nueva_fila, nueva_columna))

        # Movimiento de captura
        salto_fila, salto_columna = fila + 2 * d_fila, columna + 2 * d_columna
        if (0 <= salto_fila < 4 and 0 <= salto_columna < 4 and
            tablero[nueva_fila][nueva_columna] not in (0, pieza) and
            tablero[salto_fila][salto_columna] == 0):
            movimientos.append((salto_fila, salto_columna))
    
    return movimientos

def movimiento_ia():
    global movimientos_totales, fichas_blancas

    mejor_movimiento = None
    mejor_valor = float('-inf')
    captura_disponible = False

    for fila in range(4):
        for columna in range(4):
            if tablero[fila][columna] == 2:  # Ficha de la IA
                movimientos = obtener_movimientos_validos(fila, columna)
                for movimiento in movimientos:
                    nueva_fila, nueva_columna = movimiento
                    es_captura = abs(nueva_fila - fila) == 2  # Verificar si es un movimiento de captura
                    if es_captura:
                        captura_disponible = True
                    
                    # Realizar movimiento
                    tablero[nueva_fila][nueva_columna] = 2
                    tablero[fila][columna] = 0
                    if es_captura:  # Simular captura
                        fila_rival = (fila + nueva_fila) // 2
                        columna_rival = (columna + nueva_columna) // 2
                        tablero[fila_rival][columna_rival] = 0
                        fichas_blancas -= 1  # Restamos una ficha blanca
                    
                    # Convertir a reina si la ficha llega a la fila 0
                    if nueva_fila == 0:
                        tablero[nueva_fila][nueva_columna] = -2  # Convertir a reina

                    valor = evaluar_tablero()
                    if valor > mejor_valor:
                        mejor_valor = valor
                        mejor_movimiento = (fila, columna, nueva_fila, nueva_columna, es_captura)
                    
                    # Deshacer movimiento
                    tablero[fila][columna] = 2
                    tablero[nueva_fila][nueva_columna] = 0
                    if es_captura:
                        tablero[fila_rival][columna_rival] = 1  # Revertir captura

    if mejor_movimiento:
        movimientos_totales += 1
        fila, columna, nueva_fila, nueva_columna, es_captura = mejor_movimiento
        tablero[nueva_fila][nueva_columna] = 2
        tablero[fila][columna] = 0
        if es_captura:
            fila_rival = (fila + nueva_fila) // 2
            columna_rival = (columna + nueva_columna) // 2
            tablero[fila_rival][columna_rival] = 0  # Eliminar ficha capturada
        
        # Convertir a reina si la ficha llega a la fila 0
        if nueva_fila == 0:
            tablero[nueva_fila][nueva_columna] = -2  # Convertir a reina

        return True
    return False

# Función de evaluación simple para Minimax
def evaluar_tablero():
    puntuacion = 0
    for fila in range(4):
        for columna in range(4):
            if tablero[fila][columna] == 2:
                puntuacion += 10  # Ficha de la IA
                if fila == 0:  # Reina
                    puntuacion += 20
            elif tablero[fila][columna] == 1:
                puntuacion -= 10  # Ficha del jugador
                if fila == 3:  # Reina
                    puntuacion -= 20
    return puntuacion

# Función para mostrar mensaje de fin de juego
def mostrar_mensaje_fin(juego_terminado, mensaje):
    texto = fuente.render(mensaje, True, TEXTO_COLOR)
    pantalla.blit(texto, (ANCHO_VENTANA // 4, ALTO_VENTANA // 2))
    pygame.display.update()
    pygame.time.wait(3000)  # Espera 3 segundos antes de cerrar el juego
    pygame.quit()
    sys.exit()

# Función para verificar el fin del juego
def verificar_fin_juego():
    global movimientos_totales, fichas_blancas, fichas_negras
    if movimientos_totales == 64:  # Si se han realizado 64 movimientos y nadie ha ganado
        mostrar_mensaje_fin(True, "Empate")
    elif fichas_blancas == 0:  # Si no quedan fichas blancas, gana el negro
        mostrar_mensaje_fin(True, "Gana el Negro")
    elif fichas_negras == 0:  # Si no quedan fichas negras, gana el blanco
        mostrar_mensaje_fin(True, "Gana el Blanco")

# Juego principal
while True:
    pantalla.fill(BLANCO)
    dibujar_tablero()
    dibujar_fichas()
    dibujar_movimientos_disponibles()
    mostrar_turno()
    verificar_fin_juego()

    # Llamar a la función de eventos para manejar los clics y otros eventos
    manejar_eventos()

    if jugador_turno == 2:  # Turno de la IA
        if movimiento_ia():
            jugador_turno = 1

    pygame.display.flip()
    pygame.time.Clock().tick(60)