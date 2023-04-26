# Tarea 1: DCCavaCava 🏖⛏

## Consideraciones generales :octocat:

La tarea está completa, es decir, cree todas las clases y metodos para permitir el flujo completo del juego permitiendo crear nuevas partidas y cargar partidas existentes. Tambien realice el bonus de Gardar Partida. Las funciones se encuentran comentadas para aclarar lo que hacen.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Programación Orientada a Objetos: 42 pts (35%)
##### ✅ Diagrama: El diagrama incluye todas las clases, atributos, metodos y relaciones
##### ✅ Definición de clases, atributos, métodos y properties: Se definieron clases para el Torneo, Arena, Excavadores e Items.
##### ✅ Relaciones entre clases: Se crearon clases con herencia para las arenas, excavadores y items. Además de una clase abstracta para la arena
#### Preparación programa: 11 pts (9%)
##### ✅ Creación de partidas: Es capaz de crear una partida leyendo la informacion de los archivos csv para crear la arena con los items y el equipo para luego instanciar la clase Torneo
#### Entidades: 22 pts (18%)
##### ✅ Excavador: Se implemento la clase Excavador con todos los atributos y metodos mencionados en el enunciado. Ademas un metodo para reaccionar a un evento
##### ✅ Arena: Se implemento la clase Arena y clases hijas para cada tipo de arena. Tienen todos los atributos y unos metodos para definir ciertas propiedades de la arena (su reaccion a un evento y la probabilidad de encotrar items)
##### ✅ Torneo: Se implemento la clase Torneo con todos los metodos y atributos mencionados en el enunciado. Ademas unos metodos para manejar los eventos.
#### Flujo del programa: 31 pts (26%)
##### ✅ Menú de Inicio: Se implementaron todas las opciones del menu de inicio (nueva partida, cargar partida y salir)
##### ✅ Menú Principal: Se implementaron todas las opciones de el menu principal (simular día, ver estado, ver items, guardar partida, volver y salir)
##### ✅ Simulación día Torneo: Se implemento completamente dividiendose en distintas funciones que se encargan de cavar, encontrar los items, manejar los eventos y por ultimo revisar la energia de los excavadores
##### ✅ Mostrar estado torneo: Se imprimen el día actual, los metros cavados por cada excavador trabajando y los totales, los items encontrados por cada excavador y el total por tipo item, si ocurrio un evento y su efecto y por ultimo los excavadores que descansaron.
##### ✅ Menú Ítems: Se imprimen todos los items en la mochila y las opciones de volver y salir. Ademas se permite seleccionar y usar un item.
##### ✅ Guardar partida: Guarda la partida en un archivo .txt en la carpeta Partidas pidiendo el nombre al usuario y valida el nombre
##### ✅ Robustez: Se verifica un input valido en cada menu y además se verifica que el nombre de archivo para guardar partida sea valido (en windows)
#### Manejo de archivos: 14 pts (12%)
##### ✅ Archivos CSV Es capaz de leer todos los archivos csv y luego convertirlos en sus respectivas clases
##### ✅ Archivos TXT Es capaz de guardar multiples partidas en formato .txt
##### ✅ parametros.py: Incluye todos los parametros especificados en el enunciado (excepto DIAS_TORNEO que se uso DIAS_TOTALES_TORNEO) y algunos parametros creados por mi como los tipos de arena, items, excavador
#### Bonus: 3 décimas máximo
##### ✅ Guardar Partida: Al momento de guardar partida se pide el nombre de archivo y se valida guardandola en la carpeta Partidas. La opcion para cargar partida desplega un menu mostrando todas las partidas disponibles

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```menu.py```.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```path, listdir```
2. ```random```: ```random, choice, choices, sample```
3. ```collections```: ```defaultdic```
3. ```typing```: ```Union```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```parametros```: contiene los parametros pedidos en el enunciado y algunos que consideré necesarios
2. ```menu```: contiene las funciones para imprimir los menus y manejar las selecciones del usuario
3. ```torneo```: contiene la clase torneo y las funciones para instanciarla y manejarla (seleccionar el equipo, la arena, los items, etc)
4. ```entidades_torneo```: contiene las entidades del torneo (items, arenas y excavadores) y unas funciones para instanciar estas

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Los tesoros cambian la arena de la misma forma que los eventos, es decir, se busca de manera aleatoria una arena nueva que cumpla con el requisito del tipo (https://github.com/IIC2233/Syllabus/issues/171)
2. Como el ExcavadorHibrido pierde la mitad de energia hay una division por dos que puede dar decimales. El enunciado no especificaba que hacer con este valor (si redondearlo o truncarlo o ninguno). Decidi truncarlo usando int() para asi mantener la energia como un int y no float (https://github.com/IIC2233/Syllabus/issues/137)
3. Un derrumbe afecta a todas las arenas y por tanto la arena normal tambien es reelegida despues de un derrumbe (https://github.com/IIC2233/Syllabus/issues/171)
4. El tesoro que agrega un excavador al equipo permite repeticion (puede elegir a un excavador que ya este en el equipo) para no limitar el flujo del juego.
5. Los items encontrados en la arena no se eliminan de la arena (pueden encontrarse varias veces) asi si eventualmente no se produce un cambio de arena en mucho tiempo se pueden seguir encontrando items.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. https://github.com/IIC2233/Syllabus/blob/main/Tareas/T1/Sala%20Ayuda/Sala%20Ayuda%20-%20Menus.ipynb : este contiene codigo de ejemplo para el manejo de varios menus. Esta implementado en ```menu.py``` en los diferentes tipos de menus (se utiliza el mismo metodo para el llamado a otros menus y manejo de inputs)
2. https://github.com/IIC2233/Syllabus/blob/main/Tareas/T1/Sala%20Ayuda/Sala%20Ayuda%20-%20Probabilidades.ipynb : este contiene codigo para el manejo de probabilidades en python. Este esta implementado en ```torneo.py``` en las lineas 91 a 94 y ```entidades_torneo.py``` en las lineas 191 a 193. Se usa para calcular si ocurre un evento y cual, si se encuentran items y de que tipo.
