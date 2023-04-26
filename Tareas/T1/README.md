# Tarea 1: DCCavaCava 🏖⛏


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

**⚠️⚠️NO BASTA CON SOLO PONER EL COLOR DE LO IMPLEMENTADO**,
SINO QUE SE DEBERÁ EXPLICAR QUÉ SE REALIZO DETALLADAMENTE EN CADA ITEM.
⚠️⚠️

#### Programación Orientada a Objetos: 42 pts (35%)
##### ✅ Diagrama
##### ✅ Definición de clases, atributos, métodos y properties
## ✅ Relaciones entre clases: Se crearon clases con herencia para las arenas, excavadores y items. 
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
##### ✅ Robustez: Se verifica un input valido en cada menu y además se verifica que el nombre de archivo para guardar partida sea valido 
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

1. ```os```: ```path```
2. ```random```: ```choice, choices, sample```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```parametros```: contiene los parametros pedidos en el enunciado
2. ```dccavacava```: 
3. ```menu```: contiene las funciones para imprimir los menus y manejar las selecciones del usuario

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. <Descripción/consideración 1 y justificación del por qué es válido/a> 
2. Los tesoros cambian la arena. Este cambio se refleja buscando de manera aleatoria en el archivo de arenas al igual que los eventos (https://github.com/IIC2233/Syllabus/issues/171)
3. En el excavadorHibrido se asumio que al perder energia se trunca la division del valor que perdia ExcavadorDocencio en 2. (https://github.com/IIC2233/Syllabus/issues/137)
4. Un derrumbe afecta a todas las arenas y por tanto la arena normal es reelegida despues de un derrumbe (https://github.com/IIC2233/Syllabus/issues/171)
5. El tesoro que agrega excavadores permite repeticion para no limitar el flujo del juego (https://github.com/IIC2233/Syllabus/issues/134)

PD: <una última consideración (de ser necesaria) o comentario hecho anteriormente que se quiera **recalcar**>


-------



**EXTRA:** si van a explicar qué hace específicamente un método, no lo coloquen en el README mismo. Pueden hacerlo directamente comentando el método en su archivo. Por ejemplo:

```python
class Corrector:

    def __init__(self):
          pass

    # Este método coloca un 6 en las tareas que recibe
    def corregir(self, tarea):
        tarea.nota  = 6
        return tarea
```

Si quieren ser más formales, pueden usar alguna convención de documentación. Google tiene la suya, Python tiene otra y hay muchas más. La de Python es la [PEP287, conocida como reST](https://www.python.org/dev/peps/pep-0287/). Lo más básico es documentar así:

```python
def funcion(argumento):
    """
    Mi función hace X con el argumento
    """
    return argumento_modificado
```
Lo importante es que expliquen qué hace la función y que si saben que alguna parte puede quedar complicada de entender o tienen alguna función mágica usen los comentarios/documentación para que el ayudante entienda sus intenciones.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<link de código>: este hace \<lo que hace> y está implementado en el archivo <nombre.py> en las líneas <número de líneas> y hace <explicación breve de que hace>

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/syllabus/blob/main/Tareas/Descuentos.md).
