# Tarea 3: DCCachos

## Consideraciones generales :octocat:

La tarea esta casi completa exceptuando unos pequeños detalles, diria que en lo que más falto fue al manejar las desconexiones repentinad durante el juego.

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Networking: 18 pts (16%)
##### ✅ Protocolo Se utiliza TCP
##### ✅ Correcto uso de sockets
##### ✅ Conexión: Se puede mandar todo tipo de mansajes y el cliente y server escucharan
##### ✅ Manejo de Clientes: Se pueden conectar hasta 8 clientes segun lo mencionado en un issue (4 en juego, 4 en espera)
##### 🟠 Desconexión Repentina: en el inicio se maneja (se elimina el cliente), pero visualmente puede generar problemas. Durante el juego si es el turno del usuario deberia funcionar, el resto en realidad no fue testeado
#### Arquitectura Cliente - Servidor: 18 pts (16%)
##### ✅ Roles: EL server se encarga de manejar la informacion y validar las cosas, el backend se comunica con este y el front. Este ultimo solo contiene lo visual
##### ✅ Consistencia: Se utilizan locks al deserializar y serializar mensajes con pickle
##### ✅ Logs: Se muestran logs segun lo indicado en el enunciado
#### Manejo de Bytes: 26 pts (22%)
##### ✅ Codificación: Se utiliza littleendian para el largo, se separa en chunks y agrega los numeros de bloque
##### ✅ Decodificación: 
##### ✅ Encriptación
##### ✅ Desencriptación
##### ✅ Integración
#### Interfaz Gráfica: 22 pts (19%)
##### 🟠 Ventana de Inicio: Se muestran los usuarios a medida entran, pero las desconexiones pueden generar problemas (label de un usuario antiguo se superpone). Un jugador que entra en una partida en curso se le notifica al igual que a uno que entra a una partida con sala llena. Se rellena con bots si faltan jugadores (estos no se muestran en la sala como labels).
##### 🟠 Ventana de juego: Contiene todos los elementos solicitados, muestra los dados correspondientes y se pueden realizar todas las acciones de Turno. Faltaria indicar error en QLineEdit cuando usuario ingresa un valor invalido y desactivar el boton de usar poder si no puede (esto se verifica en el server, pero no se muestra en el frontend).  EL tema de terminar la partida no lo testee mucho.
#### Reglas de DCCachos: 22 pts (19%)
##### ✅ Inicio del juego: se lanzan los dados aleatoriamente para jugadores y bots
##### ✅ Bots: Siguen lo indicado en el enunciado (tienen un time.sleep para evitar que el turno sea instantaneo)
##### ✅ Ronda: El juego funciona, es decir, se puede pasar, dudar, usar poder y anunciar valor en los casos correspondientes
##### ✅ Termino del juego
#### Archivos: 10 pts (9%)
##### ✅ Parámetros (JSON): Contiene los parametros necesarios yse abre utilizando json y encoding
##### ✅ main.py; ejecuta el server y cliente y recibe puerto por consola
##### ✅ Cripto.py: se implementaron las dos funciones de cripto
#### Bonus: 4 décimas máximo
##### ✅ Cheatcodes: cuando se escribe see se muestran los dados de todos para el cliente que lo haya apretado
##### ❌ Turno con tiempo

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```archivo.py```. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```main.py``` en ```servidor``` (abre el server)
2. ```main.py``` en ```cliente``` (se conecta al server)


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```pyqt5```: para todo le de interfaz visual
2. ```random```: ```shuffle```, ```randint``` para randomizar una lista y obtener numeros random
3. ```time```: ```sleep``` para mostrar los dados por un tiempo y hacer que los bots no jueguen instantaneamente
4. ```socket```: manejar el server y conexiones
5. ```threading```: locks y abrir threads para cada cliente
6. ```sys```: para el hook y sys.argv

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

Servidor
1. ```main.py```: Contiene la clase principal para correr el server
2. ```utils.py```: Contiene funciones o clases utiles, como el acceso a parametros.py y la clase Mensaje ademas de otras para manejar el mensaje y el log
3. ```cripto.py```: Contiene las funciones para encriptar y desencriptar
4. ```entidades.py```: Contiene a la clase jugador y bot

Cliente
1. ```main.py```: Conecta el frontend y backend y inicia al cliente
2. ```utils.py```: Contiene funciones o clases utiles, como el acceso a parametros.py y la clase Mensaje
3. ```backend.py```: Contiene la logica del cliente ademas de lo necesario para comunicarse con el server
4. ```frontend.py```: Contiene la interfaz visual del cliente
5. ```cripto.py```: Contiene las funciones para encriptar y desencriptar


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. Experiencia 6, ayudantia y ejemplos del contenido de networking con python: Se sigue la misma estructura para iniciar el server y clientes. Además, la forma de comunicación usando una clase Mensaje es la misma que en la experiencia
