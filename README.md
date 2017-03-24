# skynet_beeva


## Requisitos
* Nombres de participantes: Eduardo Glez, Fernando, Andrea, Carlos, Martha, Claudia.
* Instalar elasticsearch en su versión 5.2.2
* Instalar python en su versión 3.6
* Instalar apache en su versión 2.4.6

## Instrucciones 

> Se usó la versión de apache predeterminada que trae centos 7: Apache/2.4.6 (CentOS)
  Importante:Los siguientes pasos se hicieron como root.
 * Descargar e instalar elasticsearch, comando:

 **wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.2.2.rpm**
  **rpm --install elasticsearch-5.2.2.rpm**
* Inicializar elasticsearch, confirmando primero su estatus:

  **systemctl status elasticsearch.service**
  **systemctl start elasticsearch.service**
  
* Para confirmar que está corriendo se debe ver en el navegador en el puerto por default que es 9200:
> localhost:9200

* Inicializar el servicio apache con el comando:
  **systemctl start httpd**

* En la carpeta /var/www/html/ clonar el repositorio “skynet_beeva”.
 comando:

**git clone https://github.com/drefk99/skynet_beeva.git**

> > La carpeta “data” contiene los json de elasticsearch el cual manda los datos historios y además se
> > recuperan los json de python de los datos mas relevantes obtenidos del día y además contiene el JavaScript de
> > las graficas en donde se obtiene los datos de los json para el manejo de las graficas.

> > En “pages” contiene los html utilizados, la parte visual.

> > En las carpetas “dist” y “vendor” contiene los css y el framework boostrap para facilitar el manejo de la
> > parte visual.

* en ese directorio skynet_beeva crear el virtualenv con el comando

**virtualenv -p python3.6 env**
	
* activar el virtualenv

**source env/bin/activate**
	
* A continuación  instalar el archivo requirements.txt que instala los paquetes necesarios de los scripts:

**pip install -r requirements.txt**

## Descarga de historico

> Para descargar los archivos historicos de Bancomer se creo un script en python que se encargará de descargar los tuits
> del dia con base a la fecha actual de forma automatica. Basta con ejecutar el achivo auto_todo.sh que se 
> encuentra en la carpeta "python-scripts-historico".

* Para eso primero se debe establecer permisos de ejecución al archivo  auto_todo.sh, comando:

**chmod755 python-scripts-historico/auto_todo.sh**

* Abir el archivo auto_todo.sh y establecer las rutas absolutas para el env y el archivo charles.py (leer la parte comentada en ese archivo). Ejemplo:

 **source /var/www/html/skynet_beeva/env/bin/activate**
 
 **python /var/www/html/skynet_beeva/python-scripts-historico/charls.py bancomer**

> Lo anterior es importante porque el proceso indicado en  auto_todo.sh será ejecutado por el cron, de tal forma se encargará de inicializar el env y ejecutar el archivo charles.py. charles.py es el archivo que extrae los tuits historicos y se encuentra en la misma carpeta.

* En el archivo  charls.py es necesario agregar las credenciales para acceder a la API de Twitter.

* Después hay que ejecutar el archivo auto_todo.sh ubicándose en la carpeta python-scripts-historico:

**./auto_todo.sh**

> Ese archivo toma la fecha actual del sistema y descarga todos los tweets del día con el horario del 
meridiano de greenwich en un json dentro de la carpeta: 

> > **skynet_beeva/python-scripts-historico/datoJ**

> El nombre del archivo en esa carpeta será bancomerAAAA-MM-DD.json

* Si desea unicamente ejecutar el archivo charls.py para obtener tuits de cualuqier banco y cualquier fecha (maximo una semana con anterioridad de acuerdo a las polticas de Twitter) necesita tres argumentos : nombre_banco, la fecha de inicio y la fecha de termino en formato "aaaa/mm/dd", como se puede observar acontinuación.

**python charls.py "banco" "fecha_ini" "fecha_fin"**

* Si se desea consultar el contenido de la base de datos solo requiere el nombre del banco y la fecha (aaaa-mm-dd), y 
* sustituir los valores entre comillas en los siguientes comandos en terminal:

**curl -XGET "ip_o_host:9200/skynet_beeva/nombre_banco/aaaa-mm-dd?pretty=true"**

> > en navegador
**ip_o_host:9200/skynet_beeva/nombre_banco/aaaa-mm-dd?pretty=true**


## Scripts de Python para el análisis

* Establecer permisos de ejecución al archivo ejecutable auto_todo.sh, comando:

**chmod 755 python-scripts-analisis/auto_todo.sh**

> > Este archivo automatiza la ejecución de los scripts que se encargan de la extracción y análisis de los tuits. El cron ejecuta este proceso.

* En el archivo python-scripts-analisis/auto_todo.sh establecer la ruta absoluta al env para activarlo, ejemplo:

**source /var/www/html/skynet_beeva/python-scripts-analisis/env/bin/activate**

* En el script de extract.py, el cual se encarga de extaer los tuits, es necesario agregar las credenciales para acceder a la API de Twitter. 

* Una vez hecho cambiarse a la carpeta  python-scripts-analisis y ejecutar elarchivo auto_todo.sh:

**./auto_todo.sh**
> > Lo anterior permitirá obtener el análisis de seis bancos (bancomer, banorte, banamex, scotiabank, HSBC, santander) del dia que se ejecuta el script.
> > Generará tres archivos por cada banco, uno con los tuits extraidos, otro con el análisis y otro de resultados (cuántos positivos y negativos) dentro de la carpeta /skynet_beeva/python-scripts-analisis.

* Si se quiere obtener análisis (polaridad negativa y positiva) específica de un solo banco y de fechas especificas (no mayores a una semana atrás) se ejecuta el script extract.py con tres argumentos:

	* El nombre del banco para búsqueda ej: Bancomer (nota: puedes poner cualquier nombre de banco que opere en México) 
	*  Fecha de inicio de búsqueda ej: 2017-03-18
	*  Fecha de termino de búsqueda ej: 2017-03-19
	
> > Ejemplo :

**python extract.py 'nombre_banco' 'fecha_inicio' 'fecha_termino'**

>Nota: El script test-naives-bayes.py es para crear un clasificador a partir de un dataset con una columna con tuits y otra con su etiqueta correspondiente. En la misma carpeta, en el archivo pickle ya esta creado un clasificador y un diccionario necesario para el script: load_classifier.py, el cual realiza el análisis de polaridad positiva y negativa.

* en el caso de Santander, se debe utilizar la cadena "Banco Santander" porque el término Santander tiene varios significados. 

## Subir los archivos a elasticsearch:

* El script subida_predi.py es para subir la información a la base de datos, necesita dos argumentos el primero es el doc_type, que para nuestro caso es el nombre del banco y el segundo es el nombre del archivo a subir (ojo: sin .json).Ejemplo:

**python subida_predi.py 'bancomer' 'bancomer_2017-03-22_resultados'**

> El script embed_test.py junta la parte de extracción(extract.py), análisis(load_classifier.py) y envio a la base de datos de Elasticsearch(subida_predi.py) tiene como argumentos el nombre del banco la fecha de inicio y fecha de término, como el script extract.py.

* Para comprobar que la información se encuentra en la base de datos se ejecuta en el navegador:

	**host:9200/skynet_beeva/nombre_banco/nombre_del_archivo**
	
* Tomando como ejemplo la anterior inyección de datos a elasticsearch, se usaria en el navegador para ver la información:

	**http://localhost:9200/skynet_beeva/bancomer/bancomer_2017-03-22_resultados**
	
* El auto_todo.sh es para correr el script test_embed.py de manera continua con crontab, se puede configurar la ruta del script y el intervalo de tiempo

## Ingreso

* Para ingresar al frontend desde el navegador se necesita tener arriba el apache e ingresar a la dirección 
* http://ip_o_host:port/skynet_beeva/pages

> >  El frontend que se muestra es el ejemplo mostrado en la presentación el viernes pasado, además está en proceso de mejora en relación con el histórico (formato tabla)


  
