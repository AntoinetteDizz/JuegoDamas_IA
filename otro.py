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
                # Si es reina, dibujar borde rojo
                if tablero[fila][columna] == -1:
                    pygame.draw.circle(pantalla, ROJO, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 6, 3)
            elif tablero[fila][columna] == 2 or tablero[fila][columna] == -2:  # Ficha negra o reina negra
                pygame.draw.circle(pantalla, GRIS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 3)
                pygame.draw.circle(pantalla, PNEGRAS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3)
                # Si es reina, dibujar borde rojo
                if tablero[fila][columna] == -2:
                    pygame.draw.circle(pantalla, ROJO, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 6, 3)

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
                    
                    # Convertir en reina si llegamos al borde del tablero
                    if (pieza_seleccionada == 1 and fila == 3) or (pieza_seleccionada == 2 and fila == 0):
                        tablero[fila][columna] = -pieza_seleccionada  # Convertir a reina (negativa para indicar que es reina)
                    
                    # Eliminar pieza capturada si hay captura
                    if abs(fila - posicion_original[0]) == 2:
                        fila_rival = (fila + posicion_original[0]) // 2
                        columna_rival = (columna + posicion_original[1]) // 2
                        tablero[fila_rival][columna_rival] = 0
                    
                    pieza_seleccionada = None
                    movimientos_disponibles = []
                    jugador_turno = 2 if jugador_turno == 1 else 1
                else:
                    tablero[posicion_original[0]][posicion_original[1]] = pieza_seleccionada
                    pieza_seleccionada = None
                    movimientos_disponibles = []
            elif tablero[fila][columna] == jugador_turno or abs(tablero[fila][columna]) == jugador_turno:
                pieza_seleccionada = tablero[fila][columna]
                posicion_original = (fila, columna)
                tablero[fila][columna] = 0
                movimientos_disponibles = obtener_movimientos_validos(fila, columna)

# Función para obtener movimientos válidos
def obtener_movimientos_validos(fila, columna):
    direcciones = []

    # Determinar direcciones válidas según el jugador y si la pieza es reina
    if pieza_seleccionada == 1:  # Ficha blanca normal
        direcciones = [(1, -1), (1, 1)]  # Solo hacia adelante (abajo)
    elif pieza_seleccionada == 2:  # Ficha negra normal
        direcciones = [(-1, -1), (-1, 1)]  # Solo hacia adelante (arriba)
    elif pieza_seleccionada == -1 or pieza_seleccionada == -2:  # Reina
        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Movimiento en ambas direcciones

    movimientos = []

    # Movimiento para piezas normales y reinas
    for df, dc in direcciones:
        f, c = fila + df, columna + dc
        if 0 <= f < 4 and 0 <= c < 4 and tablero[f][c] == 0:
            movimientos.append((f, c))

        # Verificar captura
        f_salto, c_salto = fila + 2 * df, columna + 2 * dc
        f_rival, c_rival = fila + df, columna + dc
        if (
            0 <= f_salto < 4 and 0 <= c_salto < 4 and
            tablero[f_rival][c_rival] != 0 and  # La casilla no está vacía
            (tablero[f_rival][c_rival] != pieza_seleccionada) and  # No puede comer a su misma pieza
            abs(tablero[f_rival][c_rival]) != abs(tablero[fila][columna]) and  # La pieza rival debe ser del color opuesto
            tablero[f_salto][c_salto] == 0  # La casilla de destino debe estar vacía
        ):
            movimientos.append((f_salto, c_salto))

    return movimientos


# Función principal del juego
def main():
    while True:
        manejar_eventos()
        pantalla.fill((211, 211, 211))
        dibujar_tablero()
        dibujar_movimientos_disponibles()
        dibujar_fichas()
        mostrar_turno()
        pygame.display.flip()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()