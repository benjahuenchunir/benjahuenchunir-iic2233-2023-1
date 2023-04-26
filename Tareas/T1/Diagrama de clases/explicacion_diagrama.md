# Explicación diagrama de clases:

Se tiene la clase principal que es ```Torneo```. Esta contiene todos los atributos y metodos mencionados en el enunciado. Luego estan las clases ```Item```, ```Arena``` y ```Excavador``` que tienen una relación de composición con torneo (estas no tienen sentido fuera de la clase torneo). 

La clase ```Item``` contiene atributos comunes entre la clase ```Consumible``` y ```Tesoro``` que heredan de ella. 

La clase ```Arena``` contiene el comportamiento comun entre los distintos tipos de arena (normal, mojada, rocosa, magnetica). De esta heredan ```ArenaNormal```, ```ArenaRocosa``` y ```ArenaMojada``` que contienen metodos para reflejar sus respectivos cambios y posibles transformaciones. Además existe ```ArenaMagnetica``` que hereda de ```ArenaRocosa``` y ```ArenaMojada```.

La clase ```Excavador``` contiene los atributos y metodos comunes para todos los excavadores. De esta hereda el ```ExcavadorDocencio``` y el ```ExcavadorTareo``` donde cada uno de estos sobreescribe el funcionamiento de uno de los metodos. Por último, ```ExcavadorHibrido``` hereda de ambos y modifica un poco los metodos de estos.

Los eventos no serán clases, sino que se manejaran dentro de los metodos de la clase ```Torneo```.