# Tarea 0: DCCeldas 💣🐢🏰

## Consideraciones generales :octocat:

La tarea esta completa, es decir, implemente todas las funciones requeridas y cumplí con el bonus de Funciones atómicas. Las funciones se encuentran comentadas para explicar su función. Para la implementacion de la funcion verificar_alcance_bomba use las coordenadas como se indican (fil, col). Sin embargo, para el resto de las implementaciones use (col, fil) por comodidad.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Menú de Inicio (5 pts) (7%)
##### ✅ Seleccionar Archivo
##### ✅ Validar Archivos
#### Menú de Acciones (11 pts) (15%) 
##### ✅ Opciones
##### ✅ Mostrar tablero 
##### ✅ Validar bombas y tortugas
##### ✅ Revisar solución
##### ✅ Solucionar tablero
##### ✅ Salir
#### Funciones (34 pts) (45%)
##### ✅ Cargar tablero
##### ✅ Guardar tablero
##### ✅ Valor bombas
##### ✅ Alcance bomba
##### ✅ Verificar tortugas
##### ✅ Solucionar tablero
#### General: (19 pts) (25%)
##### ✅ Manejo de Archivos
##### ✅ Menús
##### ✅ tablero.py
##### ✅ Módulos
##### ✅ PEP-8
#### Bonus: 6 décimas
##### ✅ Funciones atómicas
##### ❌ Regla 5

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```menu.py```.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```os```: ```path```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```menu```: Contiene las funciones para mostrar el menu de inicio y de acciones, ```mostrar_menu_inicio()```, ```mostrar_menu_acciones()``` y otras para manejar las opciones escogidas por el usuario.
2. ```functions```: contiene las funciones requeridas para manejar el tablero (validarlo, solucionarlo, guardarlo, etc)

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. La funcion solucionar_tablero del archivo functions.py no soluciona directamente el tablero, sino que retorna la funcion solucionar_tablero_recursiva y esta se encarga de solucionar el tablero y cumplir con los requisitos de la funcion solucionar_tablero. Inicialmente lo solucionaba directamente en esa funcion, pero con la limitación de no poder cambiar los parametros que recibían, era muy lento. Por ejemplo, un tablero de 5x5 lo resolvía en 5 minutos y medio mientras que ahora lo hace en 0,3 segundos. Esto lo hice basandome en la respuesta del issue 93.

-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<https://github.com/IIC2233/Syllabus/blob/main/Tareas/T0/Sala%20Ayuda/laberinto.py>: este resuelve un laberinto de forma recursiva y está implementado en el archivo functions.py en las líneas 47-58 y verifica que el moverse a una posicion sea valida para la funcion verificar_alcance_bomba, es decir, este dentro del tablero y no sea una tortuga. También esta en las lineas 128-146, donde seguí una estructura similar para resolver el tablero recursivamente.
