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

# Inicialización de Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Tablero de Damas 4x4")

# Inicializar fuente
fuente = pygame.font.Font(None, 36)

# Representación del tablero (1: ficha blanca, 2: ficha negra, -1: reina blanca, -2: reina negra, 0: casilla vacía)
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
            if tablero[fila][columna] == 1:  # Ficha blanca
                pygame.draw.circle(pantalla, GRIS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 3)
                pygame.draw.circle(pantalla, PBLANCAS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3)
            elif tablero[fila][columna] == 2:  # Ficha negra
                pygame.draw.circle(pantalla, GRIS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 3)
                pygame.draw.circle(pantalla, PNEGRAS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3)
            elif tablero[fila][columna] == -1:  # Reina blanca
                pygame.draw.circle(pantalla, GRIS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 3)
                pygame.draw.circle(pantalla, (255, 223, 186), (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3)
            elif tablero[fila][columna] == -2:  # Reina negra
                pygame.draw.circle(pantalla, GRIS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 3)
                pygame.draw.circle(pantalla, (123, 63, 0), (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3)

# Función para mostrar el turno del jugador
def mostrar_turno():
    texto = fuente.render(f"Turno: {'Blanco' if jugador_turno == 1 else 'Negro'}", True, TEXTO_COLOR)
    pantalla.blit(texto, (10, 10))

# Función para manejar los eventos del ratón
def manejar_eventos():
    global pieza_seleccionada, posicion_original, jugador_turno, movimientos_disponibles
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos
            fila = y // TAMANO_CASILLA
            columna = x // TAMANO_CASILLA

            if pieza_seleccionada:
                if (fila, columna) in movimientos_disponibles:
                    # Mover la pieza
                    tablero[fila][columna] = pieza_seleccionada
                    tablero[posicion_original[0]][posicion_original[1]] = 0
                    # Eliminar pieza capturada si hay captura
                    if abs(fila - posicion_original[0]) == 2:
                        fila_rival = (fila + posicion_original[0]) // 2
                        columna_rival = (columna + posicion_original[1]) // 2
                        tablero[fila_rival][columna_rival] = 0
                    pieza_seleccionada = None
                    movimientos_disponibles = []
                    jugador_turno = 2 if jugador_turno == 1 else 1
                    # Comprobar si una pieza llegó al borde para convertirse en reina
                    if jugador_turno == 1 and fila == 3:
                        tablero[fila][columna] = -1  # Convertir en reina blanca
                    elif jugador_turno == 2 and fila == 0:
                        tablero[fila][columna] = -2  # Convertir en reina negra
                else:
                    tablero[posicion_original[0]][posicion_original[1]] = pieza_seleccionada
                    pieza_seleccionada = None
                    movimientos_disponibles = []
            elif tablero[fila][columna] == jugador_turno:
                pieza_seleccionada = tablero[fila][columna]
                posicion_original = (fila, columna)
                tablero[fila][columna] = 0
                movimientos_disponibles = obtener_movimientos_validos(fila, columna, pieza_seleccionada)

# Función para obtener los movimientos válidos de una pieza
def obtener_movimientos_validos(fila, columna, pieza):
    movimientos = []
    
    # Pieza blanca normal
    if pieza == 1:
        if fila + 1 < 4:
            if columna - 1 >= 0 and tablero[fila + 1][columna - 1] == 0:  # Movimiento diagonal izquierda
                movimientos.append((fila + 1, columna - 1))
            if columna + 1 < 4 and tablero[fila + 1][columna + 1] == 0:  # Movimiento diagonal derecha
                movimientos.append((fila + 1, columna + 1))
    
    # Pieza negra normal
    elif pieza == 2:
        if fila - 1 >= 0:
            if columna - 1 >= 0 and tablero[fila - 1][columna - 1] == 0:  # Movimiento diagonal izquierda
                movimientos.append((fila - 1, columna - 1))
            if columna + 1 < 4 and tablero[fila - 1][columna + 1] == 0:  # Movimiento diagonal derecha
                movimientos.append((fila - 1, columna + 1))
    
    # Reina blanca (pieza == -1)
    elif pieza == -1:
        # Movimientos diagonales hacia adelante y hacia atrás
        # Hacia arriba izquierda
        f, c = fila, columna
        while f - 1 >= 0 and c - 1 >= 0:
            f -= 1
            c -= 1
            if tablero[f][c] == 0:  # Casilla vacía
                movimientos.append((f, c))
            elif tablero[f][c] == 2:  # Pieza negra
                break
            else:
                break
        
        # Hacia arriba derecha
        f, c = fila, columna
        while f - 1 >= 0 and c + 1 < 4:
            f -= 1
            c += 1
            if tablero[f][c] == 0:  # Casilla vacía
                movimientos.append((f, c))
            elif tablero[f][c] == 2:  # Pieza negra
                break
            else:
                break
        
        # Hacia abajo izquierda
        f, c = fila, columna
        while f + 1 < 4 and c - 1 >= 0:
            f += 1
            c -= 1
            if tablero[f][c] == 0:  # Casilla vacía
                movimientos.append((f, c))
            elif tablero[f][c] == 1:  # Pieza blanca
                break
            else:
                break
        
        # Hacia abajo derecha
        f, c = fila, columna
        while f + 1 < 4 and c + 1 < 4:
            f += 1
            c += 1
            if tablero[f][c] == 0:  # Casilla vacía
                movimientos.append((f, c))
            elif tablero[f][c] == 1:  # Pieza blanca
                break
            else:
                break
    
    # Reina negra (pieza == -2)
    elif pieza == -2:
        # Movimientos diagonales hacia adelante y hacia atrás
        # Hacia arriba izquierda
        f, c = fila, columna
        while f - 1 >= 0 and c - 1 >= 0:
            f -= 1
            c -= 1
            if tablero[f][c] == 0:  # Casilla vacía
                movimientos.append((f, c))
            elif tablero[f][c] == 1:  # Pieza blanca
                break
            else:
                break
        
        # Hacia arriba derecha
        f, c = fila, columna
        while f - 1 >= 0 and c + 1 < 4:
            f -= 1
            c += 1
            if tablero[f][c] == 0:  # Casilla vacía
                movimientos.append((f, c))
            elif tablero[f][c] == 1:  # Pieza blanca
                break
            else:
                break
        
        # Hacia abajo izquierda
        f, c = fila, columna
        while f + 1 < 4 and c - 1 >= 0:
            f += 1
            c -= 1
            if tablero[f][c] == 0:  # Casilla vacía
                movimientos.append((f, c))
            elif tablero[f][c] == 2:  # Pieza negra
                break
            else:
                break
        
        # Hacia abajo derecha
        f, c = fila, columna
        while f + 1 < 4 and c + 1 < 4:
            f += 1
            c += 1
            if tablero[f][c] == 0:  # Casilla vacía
                movimientos.append((f, c))
            elif tablero[f][c] == 2:  # Pieza negra
                break
            else:
                break

    return movimientos

# Bucle principal del juego
while True:
    pantalla.fill(BLANCO)  # Limpiar la pantalla
    dibujar_tablero()
    dibujar_fichas()
    dibujar_movimientos_disponibles()
    mostrar_turno()
    manejar_eventos()
    pygame.display.flip()  # Actualizar la pantalla
    pygame.time.Clock().tick(60)  # Controlar la velocidad del juego
