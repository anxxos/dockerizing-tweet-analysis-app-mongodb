# Dockerización de una aplicación de análisis de tweets

En esta práctica se empaqueta y distribuye una aplicación Python que descarga y analiza tweets. Los resultados del análisis se guardan en una base de datos MongoDB, y la información se muestra en la web. La versión de la aplicación empaquetada en contenedores Docker realiza el análisis en local usando Hadoop streaming, mediante _mrjob -r local_.

> *IMPORTANTE*: Se adjuntan los archivos tweets.json y output.txt resultantes de la ejecución. Antes de realizar cualquier otra ejecución, es conveniente eliminar dichos archivos para evitar cualquier tipo de error de sobreescritura.


### SOBRE LA CREACIÓN Y EJECUCIÓN DE CONTENEDORES 

#### Si se desea crear las imágenes antes de ejecutar las aplicaciones, situarse en la carpeta que contiene la práctica y ejecutar:

`$ sudo docker-compose build`

Posteriormente, para ejecutar los contenedores:

`$ sudo docker-compose up`

#### Si se desea crear las imágenes al momento de ejecutar los contenedores de las aplicaciones:

`$ sudo docker-compose up --build`

#### Si se desea descargar las imágenes de Docker-Hub en lugar de construirlas a partir de los archivos 'Dockerfile' contenidos en la práctica (como las opciones anteriores), modificar el archivo 'docker-compose.yml' de la siguiente manera:

version: '3'
services:
  tweetanalysis:
    environment:       
      - TIME=200
      - ATK='153033963-jP68EHbn2wJvaCSSQ5bO4V27aKXew4J6TCODJGuy'
      - ATS='Zh25lNhA6tjSxgNq0zkAuyoWkYO3g60f4AaPg1kcVIOMq'
      - CK='JqNuqL2hzorubHxGPLqf6szSU'
      - CS='mxbkcTBA1tiP0VtVU2SzwOwBhHC6IDN5fP84FdMiaCP3OGkaMa'
    image: practicacloud_tweetanalysis:latest
  web:
    ports:
      - "5000:5000"     
    image: practicacloud_web:latest
    links:
      - db
  db:
    image: mongo:3.0.2
    links:
      - tweetanalysis

Una vez modificado, únicamente es necesario el archivo 'docker-compose.yml'. Ejecutar entonces:

`$ sudo docker-compose up`

### SOBRE LA PUBLICACIÓN DE CONTENEDORES

#### Será necesario acceder a una cuenta de DockerHub:

`$ sudo docker login`

#### Para etiquetar las imágenes:

`$ sudo docker tag <image_id> <account_name>/`
`practicacloud_tweetanalysis:latest`
`$ sudo docker tag <image_id> <account_name>/`
`practicacloud_web:latest`

#### Para publicar las imágenes:

`$ sudo docker push <account_name>/`
`practicacloud_tweetanalysis:latest`
`$ sudo docker push <account_name>/`
`practicacloud_web:latest`

