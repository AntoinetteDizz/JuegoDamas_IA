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
TEXTO_COLOR = (50, 50, 60)     # Color del texto (negro)

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

# Función para dibujar el tablero
def dibujar_tablero():
    for fila in range(4):
        for columna in range(4):
            color = NEGRO if (fila + columna) % 2 == 0 else BLANCO
            pygame.draw.rect(pantalla, color, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))
            pygame.draw.rect(pantalla, NEGRO, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA), 2)  # Bordes

# Función para dibujar las piezas con borde gris
def dibujar_fichas():
    for fila in range(4):
        for columna in range(4):
            if tablero[fila][columna] == 1:  # Ficha blanca
                pygame.draw.circle(pantalla, GRIS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 3)
                pygame.draw.circle(pantalla, PBLANCAS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3)
            elif tablero[fila][columna] == 2:  # Ficha negra
                pygame.draw.circle(pantalla, GRIS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3 + 3)
                pygame.draw.circle(pantalla, PNEGRAS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3)

# Función para mostrar el turno del jugador
def mostrar_turno():
    # Crear el texto
    texto = fuente.render(f"Turno: {'Blanco' if jugador_turno == 1 else 'Negro'}", True, TEXTO_COLOR)
    pantalla.blit(texto, (10, 10))

# Función para manejar los eventos del ratón
def manejar_eventos():
    global pieza_seleccionada, posicion_original, jugador_turno
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Detectar clic en el ratón
        if evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos
            fila = y // TAMANO_CASILLA
            columna = x // TAMANO_CASILLA

            # Si ya hay una pieza seleccionada, intentar moverla
            if pieza_seleccionada:
                if es_movimiento_valido(fila, columna):
                    # Mover la pieza a la nueva casilla
                    tablero[fila][columna] = pieza_seleccionada
                    tablero[posicion_original[0]][posicion_original[1]] = 0
                    pieza_seleccionada = None
                    # Cambiar el turno del jugador
                    jugador_turno = 2 if jugador_turno == 1 else 1
                else:
                    # Si el movimiento no es válido, regresamos la pieza a su posición original
                    tablero[posicion_original[0]][posicion_original[1]] = pieza_seleccionada
                    pieza_seleccionada = None  # Deseleccionar pieza

            # Seleccionar una pieza si está en el turno del jugador actual
            elif tablero[fila][columna] == jugador_turno:
                pieza_seleccionada = tablero[fila][columna]
                posicion_original = (fila, columna)  # Guardar la posición original
                tablero[fila][columna] = 0  # Vaciar la casilla

# Función para verificar si el movimiento es válido
def es_movimiento_valido(fila_destino, columna_destino):
    global pieza_seleccionada
    fila_origen, columna_origen = obtener_coordenadas_pieza(pieza_seleccionada)

    # Verificar que la casilla de destino esté vacía
    if tablero[fila_destino][columna_destino] != 0:
        return False

    # Verificar si el movimiento es diagonal (movimiento simple)
    if abs(fila_destino - fila_origen) == 1 and abs(columna_destino - columna_origen) == 1:
        return True

    # Verificar captura (salto sobre una pieza rival)
    if abs(fila_destino - fila_origen) == 2 and abs(columna_destino - columna_origen) == 2:
        # Coordenadas de la pieza que está siendo saltada
        fila_rival = (fila_destino + fila_origen) // 2
        columna_rival = (columna_destino + columna_origen) // 2
        # Verificar que la pieza rival esté en el medio
        if tablero[fila_rival][columna_rival] != 0 and tablero[fila_rival][columna_rival] != pieza_seleccionada:
            # Realizar la captura
            tablero[fila_rival][columna_rival] = 0  # Eliminar la pieza rival
            return True
    return False

# Función para obtener las coordenadas de la pieza seleccionada
def obtener_coordenadas_pieza(pieza):
    for fila in range(4):
        for columna in range(4):
            if tablero[fila][columna] == pieza:
                return fila, columna
    return None, None

# Función principal del juego
def main():
    while True:
        manejar_eventos()

        # Rellenar la pantalla con un fondo gris claro
        pantalla.fill((211, 211, 211))

        # Dibujar el tablero y las piezas
        dibujar_tablero()
        dibujar_fichas()

        # Mostrar el turno del jugador
        mostrar_turno()

        # Actualizar la pantalla
        pygame.display.flip()

        # Limitar el framerate a 60 FPS
        pygame.time.Clock().tick(60)

# Llamada a la función principal
if __name__ == "__main__":
    main()
