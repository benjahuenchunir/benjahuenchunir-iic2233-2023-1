# Tarea 2: DCCazafantasmas 👻🧱🔥

## Consideraciones generales :octocat:

La tarea esta completa, es decir, cree la ventana de inicio y de juego, cada una con todas sus funciones y modos. Además implemente el bonus de jugar de nuevo y el de drag and drop.

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores

**⚠️⚠️NO BASTA CON SOLO PONER EL COLOR DE LO IMPLEMENTADO**,
SINO QUE SE DEBERÁ EXPLICAR QUÉ SE REALIZO DETALLADAMENTE EN CADA ITEM.
⚠️⚠️

#### Ventanas: 27 pts (27%)
##### ✅ Ventana de Inicio 
##### ✅ Ventana de Juego
#### Mecánicas de juego: 47 pts (47%)
##### ✅ Luigi
##### ✅ Fantasmas
##### ✅ Modo Constructor
##### ✅ Fin de ronda
#### Interacción con el usuario: 14 pts (14%)
##### ✅ Clicks
##### ✅ Animaciones: El movimiento de los personajes es discreto (se mueve de casilla en casilla), pero intercalando las imagenes para crear la animacion (tanto de luigi y de los fantasmas, la roca no intercala imagenes pero esta animada)
#### Funcionalidades con el teclado: 8 pts (8%)
##### ✅ Pausa: Es posible pausar el juego con el boton y con la tecla P, esto afecta al tiempo y movimiento de los sprites
##### ✅ K + I + L: Elimina los fantasmas del juego con la combinacion de teclas, si Luigi muere los fantasmas se reinician teniendo que activar nuevamente el cheat
##### ✅ I + N + F: Congela el tiempo y otorga vidas infinitas a Luigi
#### Archivos: 4 pts (4%)
##### ✅ Sprites
##### ✅ Parametros.py
#### Bonus: 8 décimas máximo
##### ✅ Volver a Jugar: Al final de la partida se despliega la alerta con la puntuacion obtenida y un boton para volver a jugar que resetea el mapa, vidas, cheatcodes y tiempo
##### ❌ Follower Villain: No hice nada
##### ✅🟠 Drag and Drop

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5```
2. ```sys```: ```exit```, ```__excepthook__```
3. ```os```: ```listdir```, ```path```
4. ```copy```: ```deepcopy``` Para hacer una copia del mapa (una lista de listas)

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```main```: Es el modulo principal que conecta el frontend con el backend
2. ```parametros``` Contiene las constantes utilizadas
3. ```frontend```: Hecha para <insertar descripción **breve** de lo que hace o qué contiene>
4. ```backend```

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. En los cheatcodes, el INF permanece activo cuando Luigi muere, en cambio el KIL se debe volver a activar. Cuando se reinicia el juego se resetean todos los cheatcodes

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<link de código>: este hace \<lo que hace> y está implementado en el archivo <nombre.py> en las líneas <número de líneas> y hace <explicación breve de que hace>