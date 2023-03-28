# Tarea 0: DCCeldas 💣🐢🏰


Un buen ```README.md``` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea, y consecuentemente cómo funciona su programa, por lo en general, entre más ordenado y limpio sea éste, mejor será 

Para nuestra suerte, GitHub soporta el formato [MarkDown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet))

Un buen ```README.md``` no tiene por que ser muy extenso tampoco, hay que ser **concisos** (a menos que lo consideren necesario) pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio 

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

Explicación: mantén el emoji correspondiente, de manera honesta, para cada item. Si quieres, también puedes agregarlos a los títulos:
- ❌ si **NO** completaste lo pedido
- ✅ si completaste **correctamente** lo pedido
- 🟠 si el item está **incompleto** o tiene algunos errores
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
El módulo principal de la tarea a ejecutar es  ```menu.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```functions.py``` en el directorio principal
2. ```tablero.py``` en el directorio principal


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

1. La funcion solucionar_tablero del archivo functions.py no soluciona directamente el tablero, sino que retorna la funcion solucionar_tablero_recursiva y esta se encarga de solucionar el tablero y cumplir con los requisitos de la funcion solucionar_tablero. Inicialmente lo solucionaba directamente en esa funcion, pero con la limitación de no poder cambiar los parametros que recibian, era muy lento. Por ejemplo, un tablero de 5x5 lo resolvía en 5 minutos y medio mientras que ahora lo hace en 0,3 segundos. Esto lo hice basandome en la respuesta del issue 93.

-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<https://github.com/IIC2233/Syllabus/blob/main/Tareas/T0/Sala%20Ayuda/laberinto.py>: este resuelve un laberinto de forma recursiva y está implementado en el archivo functions.py en las líneas 54-65 y verifica que el moverse a una posicion sea valida para la funcion verificar_alcance_bomba, es decir, este dentro del tablero y no sea una tortuga. También esta en las lineas 115-130, donde seguí una estructura similar para resolver el tablero recursivamente.
