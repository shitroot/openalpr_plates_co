# Openalpr Webservice en un contenedor Docker adaptado para placas colombianas

Este repositorio contiene el proyecto y todo lo necesario para construir una imagen docker que puede ser usada para leer y detectar placas colombianas, ya sea enviando una imagen,  video, o mediante el uso de camara web

En el proyecto puede encontrarse el Dockerfile el cual cotiene las instrucciones necesarias para construir la imagen con todo el sistema instalado y listo para funcionar, la imagen pase sobre la que se instalan los componentes de la libreria es una DEBIAN 9 con Python 3.6.6 instalado,  en la que ademas se instalan TORNADO una libreria que permite crear un servidor web, y opencv, lo que tambien facilita el post procesamiento de una imagen segun se requiera.

El siguiente comando en el docker file instala los componentes en el sistema de tal manera que openalpr pueda ser integrado con python, lo que permite importar openalpr como libreria.


```
RUN cd /storage/projects/alpr/src/bindings/python && \
      python setup.py install && \
      ./make.sh
``` 
la documentacion se encuentra disponible en http://doc.openalpr.com/bindings.html

si se desea   que el reconocedor reconosca placas de motos, se cambia el archivo co.patterns en la ruta openalpr/runtime_data/postprocess
donde el archivo tiene las siguientes expresiones regulares:

```
base		@@@###
base		[A-Z][A-Z][A-Z][0-9][0-9][0-9]
base		[A-Z][A-Z][A-Z]###
base 		@@@[0-9][0-9][0-9]
```
cambiando las expresiones indicadas para las placas de una moto

## install docker 
se debe  como primer paso tener docker instalado en el host,  en caso de no tener docker instalado se ejecuta el siguiente comando para instalar la ultima version

```
sudo apt-get install docker-ce 
```
para mas informacion sobre comandos observar la documentacion oficial:
https://docs.docker.com/install/linux/docker-ce/ubuntu/#set-up-the-repository




## To Build

```
docker build -t openalprco .
```


## To run on real time using web camera
```
 docker run  -it --device /dev/video0  openalprco -c co webcam
```
## testing with image o video

```
docker run    -v $(pwd):/data:ro openalprco -j  -c co imagen.jpg
```
## To run from real time stream 

```
docker run -it --device /dev/video0 openalprco -c co http://admin:admin@192.168.0.3:9000/video
docker run -it  openalprco -c co http://admin:admin@192.168.0.3:9000/video
```




### detalles lista de comandos
```
user@linux:~/openalpr$ alpr --help

USAGE: 

   alpr  [-c <country_code>] [--config <config_file>] [-n <topN>] [--seek
         <integer_ms>] [-p <pattern code>] [--clock] [-d] [-j] [--]
         [--version] [-h] <image_file_path>


Where: 

   -c <country_code>,  --country <country_code>
     Country code to identify (either us for USA or eu for Europe). 
     Default=co

   --config <config_file>
     Path to the openalpr.conf file

   -n <topN>,  --topn <topN>
     Max number of possible plate numbers to return.  Default=10

   --seek <integer_ms>
     Seek to the specified millisecond in a video file. Default=0

   -p <pattern code>,  --pattern <pattern code>
     Attempt to match the plate number against a plate pattern (e.g., md
     for Maryland, ca for California)

   --clock
     Measure/print the total time to process image and all plates. 
     Default=off

   -d,  --detect_region
     Attempt to detect the region of the plate image.  [Experimental] 
     Default=off

   -j,  --json
     Output recognition results in JSON format.  Default=off

   --,  --ignore_rest
     Ignores the rest of the labeled arguments following this flag.

   --version
     Displays version information and exits.

   -h,  --help
     Displays usage information and exits.

   <image_file_path>
     Image containing license plates


   OpenAlpr Command Line Utility

```

Documentacion oficial
---------------

La documentacion detallada esta disponible en [doc.openalpr.com](http://doc.openalpr.com/)

## openalpr.conf.defaults  file
este archivo contiene la configuracion basica para el funcionamiento de la libreria, desde este file se puede configurar si se usa cpu, o gpu para el procesamiento de las imagenes (se debe tener instalado los divers de gpu) en el host,  si se desea activar esta opcion puede seguir los pasos en el siguiente link: https://marmelab.com/blog/2018/03/21/using-nvidia-gpu-within-docker-container.html
 El archivo openalpr.conf.defauls se encuentra dentro de la carpeta config del proyecto.

 en el archivo main.cpp en la linea  361 comienza la parte en la que se describe el procesamiento de json, la ruta del file es 
 ``` openalpr/src/main.cpp```

