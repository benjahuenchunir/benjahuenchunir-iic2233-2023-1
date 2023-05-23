# Tarea 2: DCCazafantasmas 👻🧱🔥

## Consideraciones generales :octocat:

La tarea esta completa, es decir, cree la ventana de inicio y de juego, cada una con todas sus funciones y modos. Además implemente el bonus de jugar de nuevo y el de drag and drop. En el enunciado se pedía especificar las lineas de los elementos pintados en amarillo o azul, eso está en una sección más abajo.

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores

**⚠️⚠️NO BASTA CON SOLO PONER EL COLOR DE LO IMPLEMENTADO**,
SINO QUE SE DEBERÁ EXPLICAR QUÉ SE REALIZO DETALLADAMENTE EN CADA ITEM.
⚠️⚠️

#### Ventanas: 27 pts (27%)
##### ✅ Ventana de Inicio Se verifica el nombre de usuario notificando en caso de error y permite abrir cualquier mapa o el modo constructor. Ademas posee un boton para salir
##### ✅ Ventana de Juego: El modo constructor posee una lista de elementos para colocar en el mapa que se pueden filtrar indicando si el usuario intenta colocar un elemento enuna posicion invalida. Se puede limpiar el mapa e iniciar el juego.  El modo juego posee un contador para el tiempo y muestra las vidas. Al perder/ganar se muestra una alerta con la opcion de jugar de nuevo o salir.
#### Mecánicas de juego: 47 pts (47%)
##### ✅ Luigi: Luigi se mueve con las teclas wasd solo a posiciones validas y muriendo si entra en contacto con un fantasma o fuego. Además es capaz de arrastrar una roca.
##### ✅ Fantasmas: Se mueven independiente el uno del otro y a su propia velocidad, muere si choca con uego y rebota en rocas y paredes
##### ✅ Modo Constructor: No se puede superponer elementos ni colocarlos fuera de la grilla, los elementos tienen cantidad maxima que se actualiza al colocarlos y el juego no puede iniciar sin un luigi y una estrella
##### ✅ Fin de ronda: El juego termina al ganar, quedarse sin vidas o acabarse el tiempo, indicando el resultado y puntaje ademas de los botones respectivos
#### Interacción con el usuario: 14 pts (14%)
##### ✅ Clicks: El constructor funciona clickeando el elemento y posicion deseada
##### ✅ Animaciones: El movimiento de los personajes es discreto (se mueve de casilla en casilla), pero intercalando las imagenes para crear la animacion (tanto de luigi y de los fantasmas, la roca no intercala imagenes pero esta animada)
#### Funcionalidades con el teclado: 8 pts (8%)
##### ✅ Pausa: Es posible pausar el juego con el boton y con la tecla P, esto afecta al tiempo y movimiento de los sprites
##### ✅ K + I + L: Elimina los fantasmas del juego con la combinacion de teclas, si Luigi muere los fantasmas se reinician teniendo que activar nuevamente el cheat
##### ✅ I + N + F: Congela el tiempo y otorga vidas infinitas a Luigi (para este y el cheatcode anterior no se requiere ningun orden, solamente que se presionen las tres teclas)
#### Archivos: 4 pts (4%)
##### ✅ Sprites: Se utilizaron todos los sprites
##### ✅ Parametros.py: Se utilizaron parametros
#### Bonus: 8 décimas máximo
##### ✅ Volver a Jugar: Al final de la partida se despliega la alerta con la puntuacion obtenida y un boton para volver a jugar que resetea el mapa, vidas, cheatcodes y tiempo
##### ❌ Follower Villain: No hice nada
##### ❌ Drag and Drop: No hice nada

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```PyQt5```
2. ```sys```: ```exit```, ```__excepthook__```
3. ```os```: ```listdir```, ```path``` Para leer los mapas en al carpeta mapas y manejar paths
4. ```copy```: ```deepcopy``` Para hacer una copia del mapa (una lista de listas)

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```main```: Es el modulo principal que conecta el frontend con el backend
2. ```parametros``` Contiene las constantes utilizadas
3. ```frontend```: Contiene la parte visual de las ventanas y sus componenetes principales (ej: tablero de juego y menu de juego, tablero de constructor y menu de constructor, etc)
4. ```frontend_elementos```: Contiene elementos visuales más pequeños o secundarios que se utilizan en ```frontend```
5. ```backend```: Contiene la logica para el juego (tanto de la ventana de inicio como de juego)
6. ```backend_elementos```: Contiene la logica para algunos elementos requeridos para el juego (ej: luigi, fantasmas, etc)

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. En los cheatcodes, el INF permanece activo cuando Luigi muere, en cambio el KIL se debe volver a activar. Cuando se reinicia el juego se resetean todos los cheatcodes