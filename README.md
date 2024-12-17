# Juego de Damas 4x4 con Pygame

Este proyecto implementa un juego de Damas (Checkers) en un tablero de 4x4, utilizando el módulo **Pygame**. El juego permite que un jugador humano controle las piezas blancas, mientras que la IA controla las piezas negras. El objetivo es mover las piezas según las reglas estándar de Damas, capturar las piezas del oponente y, si es posible, promover las piezas a reinas.

## Requisitos

Para ejecutar el juego, necesitas tener instalado **Python  3.13.1** y la librería **Pygame**.

### Instalación

1. **Instalar Python  3.13.1**: Si no tienes Python instalado, puedes descargarlo desde su [sitio oficial](https://www.python.org/downloads/).
   
2. **Instalar Pygame**: Una vez que Python esté instalado, abre la terminal (o símbolo del sistema en Windows) y ejecuta el siguiente comando para instalar Pygame:

    ```bash
    pip install pygame
    ```

3. **Clonar el repositorio o descargar los archivos**: Si aún no tienes el código en tu máquina, puedes clonar este repositorio (si está disponible en un repositorio de GitHub) o descargar los archivos directamente.

### Ejecutar el juego

1. Una vez que tengas los archivos en tu computadora, navega al directorio del proyecto usando la terminal o el explorador de archivos.

2. Ejecuta el archivo `juego_damas.py` con el siguiente comando en la terminal:

    ```bash
    python juego_damas.py
    ```

3. El juego se abrirá en una ventana de Pygame. El jugador humano controla las piezas blancas, mientras que la IA controla las piezas negras.

## Cómo jugar

- **Tablero**: El tablero tiene un tamaño de 4x4, con las casillas alternadas en colores claros y oscuros.
- **Piezas**: Hay dos tipos de piezas:
  - **Ficha blanca**: Controlada por el jugador.
  - **Ficha negra**: Controlada por la IA.
  - **Reina**: Las piezas alcanzan la última fila del tablero se convierten en reinas, que pueden moverse en cualquier dirección.
  
- **Movimiento**: Las piezas se mueven diagonalmente. Si hay una pieza enemiga en una casilla adyacente, se puede saltar sobre ella para capturarla.
  
- **Turnos**: El jugador humano mueve las piezas blancas, mientras que la IA mueve las piezas negras. El juego continúa hasta que se captura a todas las piezas del oponente o no hay más movimientos posibles.

## Lógica de la IA

La IA utiliza un algoritmo básico para determinar los movimientos. En cada turno, la IA evalúa todos los posibles movimientos y selecciona el que maximice sus probabilidades de ganar. Si tiene la opción de capturar una pieza, lo hará.

## Estructura del código

- **Inicialización de Pygame**: Se configura la ventana de Pygame, el tablero de 4x4 y las piezas.
- **Dibujo del tablero**: Se dibujan las casillas, las piezas y las posibles acciones disponibles para el jugador y la IA.
- **Manejo de eventos**: Se controla la interacción con el jugador, permitiendo seleccionar y mover las piezas.
- **Lógica de movimiento**: Se gestionan los movimientos de las piezas, incluyendo los movimientos simples y las capturas.
