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

# Inicialización de Pygame
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption("Tablero de Damas 4x4")

# Representación del tablero (1: ficha blanca, 2: ficha negra, 0: casilla vacía)
tablero = [[0 for _ in range(4)] for _ in range(4)]

# Inicialización de las piezas en el tablero (colocamos dos piezas por jugador)
# Piezas blancas (1) en las casillas negras de las primeras dos filas
tablero[0][0] = 1  # Ficha blanca en (0, 0)
tablero[0][2] = 1  # Ficha blanca en (0, 2)

# Piezas negras (2) en las casillas negras de las últimas dos filas
tablero[3][1] = 2  # Ficha negra en (3, 1)
tablero[3][3] = 2  # Ficha negra en (3, 3)

# Función para dibujar el tablero
def dibujar_tablero():
    for fila in range(4):
        for columna in range(4):
            # Alternando colores de las casillas entre blanco y negro
            color = NEGRO if (fila + columna) % 2 == 0 else BLANCO
            pygame.draw.rect(pantalla, color, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA))
            pygame.draw.rect(pantalla, NEGRO, (columna * TAMANO_CASILLA, fila * TAMANO_CASILLA, TAMANO_CASILLA, TAMANO_CASILLA), 2)  # Bordes

# Función para dibujar las piezas con borde gris
def dibujar_fichas():
    for fila in range(4):
        for columna in range(4):
            if tablero[fila][columna] == 1:  # Ficha blanca
                # Primero dibujamos el borde gris
                pygame.draw.circle(pantalla, GRIS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3+3)
                # Luego dibujamos la ficha blanca encima
                pygame.draw.circle(pantalla, PBLANCAS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3)
            elif tablero[fila][columna] == 2:  # Ficha negra
                # Primero dibujamos el borde gris
                pygame.draw.circle(pantalla, GRIS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3+3)
                # Luego dibujamos la ficha negra encima
                pygame.draw.circle(pantalla, PNEGRAS, (columna * TAMANO_CASILLA + TAMANO_CASILLA // 2, fila * TAMANO_CASILLA + TAMANO_CASILLA // 2), TAMANO_CASILLA // 3)

# Función para manejar los eventos del ratón
def manejar_eventos():
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Función principal del juego
def main():
    # Bucle principal del juego
    while True:
        # Manejar eventos
        manejar_eventos()

        # Rellenar la pantalla con un fondo gris claro
        pantalla.fill((211, 211, 211))

        # Dibujar el tablero y las piezas
        dibujar_tablero()
        dibujar_fichas()

        # Actualizar la pantalla
        pygame.display.flip()

        # Limitar el framerate a 60 FPS
        pygame.time.Clock().tick(60)

# Llamada a la función principal
if __name__ == "__main__":
    main()