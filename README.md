# AIVA-Reconocimiento-de-actividades-humanas

Práctica de la asginatura de Aplicaciones Industriales y Comerciales.

Alumnos: Lei Han, Byron Sánchez

Descripción del problema
--------------
Esta práctica consiste en un sistema de reconocimiento de actividades humanas, instalado en frente de una tienda dentro de un centro comercial.

Su función es grabar a la puerta de entrada de la tienda y reconocer a las personas en movimiento. Los movimientos de las personas se identifican en tres tipos: entrar en la tienda; salir de la tienda; ninguna de las anteriores. 

Para cada tipo de movimiento se registra el número de personas que realiza esta acción, este resultado será actualizado en un archivo CSV.


Instalaciones previas
------------
Para poder lanzar los scripts de python que se usarán en este proyecto, primero se instalará python3.X, desde una terminal de linux ejecutamos:

>sudo apt install python3.7

Ahora instalaremos las dependencias, usando el archivo requirements.txt, desde el terminal se deberá lanzar:

>pip3 install -r requirements.txt

Con esto ya estará hecho todo el set up.

Lanzar script
------------
Para lanzar el script de demo desde el terminal lanzar la siguiente instrucción
>cd fase3_sistema/
>python3 People_Detector.py --video /path/to/video.avi

Donde /path/to/video.avi está sustituida por la ruta concreta del video.


Instalar el sistema dockerizado
------------
1. Para la instalación previa de Docker ver la [documentación de Docker](https://docs.docker.com/engine/install/).

2. El archivo imagen de Docker está actualizado en la página de [Docker Hub](https://hub.docker.com/r/lhanurjc/people_detector). Está creado bajo el sistema de Ubuntu.

 - Para instalar la imagen se ejecuta:
>docker pull lhanurjc/people_detector:latest

La imagen del Docker Hub es una demo que contiene a un video como argumento por defecto. Se puede ejecutar directamente.

 - Para crear la imagen desde local utilizando el Dockerfile, se ejecuta en el directorio raíz de este proyecto:
>docker build -t people_detector:latest .

3. Una vez instalado la imagen, ejecutar para instanciar y ejecutar el contenedor.
>docker run lhanurjc/people_detector:latest

4. La ruta de almacenamiento de Docker está localizado en:
>/var/lib/docker/overlay2/id_contenedor/diff/person_detector.csv
