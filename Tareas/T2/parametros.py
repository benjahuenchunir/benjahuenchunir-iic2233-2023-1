ANCHO_GRILLA = 11 # NO EDITAR
LARGO_GRILLA = 16 # NO EDITAR

# Complete con los demás parámetros

#  Ventana inicio
MIN_CARACTERES = 5
MAX_CARACTERES = 10
NOMBRE_INVALIDO_VACIO = 'El nombre de usuario no puede estar vacio'
NOMBRE_INVALIDO_ALFANUMERICO = 'El nombre de usuario debe ser alfanumerico'
NOMBRE_INVALIDO_LARGO = f'El nombre de usuario debe contener entre {MIN_CARACTERES} y {MAX_CARACTERES} caracteres incluyendo los extremos'

TAMANO_GRILLA = 50
ANCHO_MAPA = ANCHO_GRILLA - 2
LARGO_MAPA = LARGO_GRILLA - 2
TIEMPO_JUEGO = 110



LUIGI_QUIETO = 'front'

PATH_MAPAS = 'mapas/'
PATH_FONDO = 'sprites/Fondos/fondo_inicio.png'
PATH_LOGO = 'sprites/Elementos/logo.png'
PATH_ELEMENTOS = 'sprites/Elementos/'
PATH_ENTIDADES = 'sprites/Personajes/'

NOMBRE_LUIGI = 'luigi'
CANTIDAD_VIDAS = 3


# Fantasmas
MIN_VELOCIDAD = 0.3
MAX_VELOCIDAD = 0.8
DERECHA = 'rigth'
IZQUIERDA = 'left'
VERTICAL = 'vertical'
DIRECCIONES_FANTASMA = {DERECHA: [TAMANO_GRILLA], IZQUIERDA: [-TAMANO_GRILLA], VERTICAL: [TAMANO_GRILLA, -TAMANO_GRILLA]}

ARRIBA = 'arriba'
ABAJO = 'abajo'

# Constructor
MODO_CONSTRUCTOR = 'Modo constructor'
MAPA_BORDE = 'B'
MAPA_LUIGI = 'L'
MAPA_PARED = 'P'
MAPA_FUEGO = 'F'
MAPA_FANTASMA_H = 'H'
MAPA_FANTASMA_V = 'V'
MAPA_ESTRELLA = 'S'
MAPA_ROCA = 'R'

TIPO_HORIZONTAL = 'white'
TIPO_VERTICAL = 'red'
FANTASMA_CONVERSION = {
    MAPA_FANTASMA_H:'white',
    MAPA_FANTASMA_V: 'red',
}
NOMBRES_DIRECCIONES_FANTASMA = {FANTASMA_CONVERSION[MAPA_FANTASMA_H]: [DERECHA, IZQUIERDA], FANTASMA_CONVERSION[MAPA_FANTASMA_V]: [VERTICAL]}


SPRITES_ELEMENTOS = {MAPA_BORDE: PATH_ELEMENTOS + 'bordermap.png',
                     MAPA_FUEGO: PATH_ELEMENTOS + 'fire.png',
                     MAPA_ESTRELLA: PATH_ELEMENTOS + 'osstar.png',
                     MAPA_ROCA: PATH_ELEMENTOS + 'rock.png',
                     MAPA_PARED: PATH_ELEMENTOS + 'wall.png'}
SPRITES_ENTIDADES = {
    MAPA_LUIGI: PATH_ENTIDADES + 'luigi_front.png',
    MAPA_FANTASMA_H: PATH_ENTIDADES + 'white_ghost_rigth_1.png',
    MAPA_FANTASMA_V: PATH_ENTIDADES + 'red_ghost_vertical_1.png',
}
FILTRO_TODOS = 'Todos'
FILTROS = {FILTRO_TODOS: SPRITES_ENTIDADES | SPRITES_ELEMENTOS, 'Bloques': SPRITES_ELEMENTOS, 'Entidades': SPRITES_ENTIDADES}

MAXIMO_LUIGI = 1
MAXIMO_ESTRELLA = 1
MAXIMO_ELEMENTOS = {
    MAPA_LUIGI: 1,
    MAPA_PARED: 5,
    MAPA_FUEGO: 3,
    MAPA_FANTASMA_H: 3,
    MAPA_FANTASMA_V: 2,
    MAPA_ESTRELLA: 1,
    MAPA_ROCA: 2
}

MAXIMO_FANTASMAS_VERTICAL = 2 # TODO es necesario estos, los defini con otro nombre y en diccionario
MAXIMO_FANTASMAS_HORIZONTAL = 3
