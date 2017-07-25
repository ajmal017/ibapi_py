# IBApi Demo

El fin de esta demo es crear las bases de desarrollo de una API que permita el análisis numérico del Stock Market del grupo Interactive Brokers.

El desarrollo se basa en IBAPI - Python

## Setup

### TWS

Descagar el [Free Demo](https://www.interactivebrokers.com/en/index.php?f=1286) del Trade Workstation (TWS) de Interactive Brokers y registrar una cuenta.

Una vez instalado, ir a *File/Global Configuration/API/Settings* 
y cambiar los campos:

+ Enable ActiveX Sockect Clients: True
+ Read-only API: False

Luego, ir a *File/Global Configuration/API/Precautions* y deshabilitar todas las advertencias.

## Material

+ [API](http://interactivebrokers.github.io)
+ [Documentacion de la API](http://interactivebrokers.github.io/tws-api/)
+ [Webinarios](https://www.interactivebrokers.com/en/index.php?f=2227)
+ [Webinario de IBAPI - Python](https://register.gotowebinar.com/recording/recordingView?webinarKey=5481173598715649281&recordingKey=3140418896296820993&registrantEmail=linofbossiop%40outlook.com) (Llenar fomulario para acceder al video)

# Meta actual

Organizar la API de tal manera que el usuario se enfoque en el manejo de datos y toma de decisiones.

# Organizacion de los archivos 

La API provista por Interactive Brokers (IBAPI) esta en la carpeta "ibapi/", el desarrollo de nuestra API (IBAPY)se encuentra en "src/".

Simulacion de uso de la API localmente, los archivos generados se encuentan en la carpeta "tests/".

## Descripcion de IBAPI

+ Automatizar el uso de los IDs:
Los ID ligan las operaciones solicitadas por el usuario y la respuesta del TWS. 
Cuando un usuario hace una solicitud al TWS, sea comandar una accion o solicitar datos.
La naturaleza asíncrona de IBAPI requiere implementar una cola de procesos que empareje
las acciones previamente solicitadas por el usuario (generalmente recepcion de datos) y las 
nuevas solicitudes.

## Descripcion de IBAPY

La aplicacion cuenta con 3 archivos principales los cuales contienen las clases 
con el mismo nombre capitalizado:
+ clyent.py: Clyent
+ ibapy.py: Ibapy
+ wrappyer.py: Wrappyer

Todos ubicados dentro de "src/". 
Cada una de las clases cumple "aumenta" la funcionalidad provista por IBAPI.

<b>Clyent:</b>

Hereda de: Client

Maneja las solicitudes al TWS, desde datos historicos a ordenes de compra.

Todos los métodos decorados con @request incrementan automáticamente el ID. El TWS asume que 
una solicitud de ID duplicado implica una modificación a alguna solicitud ya registrada.
En el caso de las solicitudes de datos el paradigma es más flexible ya que al completarse la
transmisión solicitada es posible reutilizar el ID. Sin embargo, IBAPY pretende registrar todas
las operaciones realizadas y almacenar las respuestas obtenidas, por lo cual la duplicación de
ID será evitada.

<b>Wrappyer:</b>
Hereda de Wrapper
Los métodos contenidos dentro de esta clase se ejecutan al recibir una respuesta del TWS.
Las funciones que aumenta se basan en controlar el flujo de la aplicacion y los datos recibidos para
facilitar el manejo de los mismos.

<b>Ibapy:</b>
Esta clase junta las dos anteriores para gestionar la solicitud y reception de los datos, autogestionando 
nuevas solicitudes dependiendo de las repuestas obtenidas.

# Progreso del desarrollo:

<b> Semanas 1 - 2 </b> 

+ Estudio de la API
+ Comprendí las herramientas que ofrece la API: realizar ordenes, solicitar datos, recibir datos y 
 funcionamiento del código provisto por IBAPI.

<b> Semana 3 </b>

+ Aprendí a manejar el TWS y a interpretar la interfaz. 
+ Estudié el funcionamiento de las velas y sus componentes, comprendí el funcionamiento de los contratos y 
 las órdenes.
+ Fueron armados los requerimientos del software que se desea desarrollar.

<b> Semana 4 </b>

+ Se inició el desarrollo de clyent.py, ibapy.py, wrappyer.py
+ Fue desarrollada la estructura con la cual serán implementados los algoritmos.
+ Se logró la graficación de los datos históricos y la solicitud de compra y venta de acciones 

<b> Semana 5 </b>

+ Se crearon los helpers ubicados en "helpers/", archivos que contienen funcionalidad útil para la aplicacion y mantener
 y estilo DRY de desarrollo. Dentro de los helpers destaca el archivo utils.py. 
+ Se desarrolló la clase CandlesArray la cual condensa todos los métodos necesarios para manipular las velas convenientemente.
 Entre sus características se encuentran: manipular el ancho de la barra de las velas, para poder trabajar en funcion a segundos,
 minutos u horas intercambiablemente. Adicionalmente, ofrece una interfaz simple para accesar los datos ya suministrados.
+ La lentitud con la que responde el servidor a la solicitud de conexión inicial, impuso un ciclo de desarrollo y prueba inaceptablemente lento, 
por ello, fue necesario cambiar el esquema de desarrollo simple a Test Driven Development (TDD) para poder simular la respuesta 
del servidor y el flujo del programa al recibir la respuesta. Sin embargo, esto requirió una modificación sustancial al código ya existente.
 
<b> Semana 6 </b>

+ Se consolidó la configuración de la suite de pruebas dentro la carpeta "tests/" y se procedió a realizar pruebas a todos
  las clases creadas en las semanas anteriores. Esto implicó un consumo considerable de tiempo y estancó el desarrollo de las
  nuevas características programadas a ser realizadas esa semana, pero por otro lado, se depuró el código, mejoró la semanantica y
  la consistencia del mismo.
  
# Pendiente

<b>Solicitar largas cadenas de datos.</b> Debido a que el TWS solo responde con 1800 velas por solicitud, para poder manipular 
datos correspondientes a varios días a espacio de minutos o segundos, es necesario desarrollar una arquitectura que soporte
los eventos de solicitudes simultánas de múltiples operaciones. Esto estaba previsto ser desarrollado la semana 5, pero para
poder desarrollarse se requiere una estructura rápida de ensayo y error, por ellos se invirtió tiempo en implantar el TDD. El día 12/07/07
fue reanudado el desarrollo de esta funcionalidad. Para el 16/07/17 estará lista.

<b>Desarrollo de la interfáz gráfica.</b>

<b>Mantener actualizados los datos.</b> Los datos actualizados llegan en forma de muestras, los cuales seran transformados en velas
 y almancenados en el objeto CandlesArray(). Sin embargo, la API requiere de suscripciones a los Productos las cuales son pagas.
 

  
