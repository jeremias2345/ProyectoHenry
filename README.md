Bienvenidos a mi Projecto - una API y ML project de data sobre peliculas.


| Informacion  | 
| ------------- | 
| Esta es una API(Interfaz de programación de aplicaciones) que proporciona informacion sobre peliculas.Desde, cantidad de peliculas por mes y por dia, la popularidad o cantidad de votos por pelicula y la cantidad de peliculas sobre actores y directores. Luego creamos sistema de recomendacion de peliculas usando ML(Machine Learning) basado en contenido.
 Toda la data fue proporcionada por IDMB(Base de datos de peliculas). | 

#### Documentacion

https://proyecto-henry-lsam.onrender.com/

#### Como se usa?
Para usar la api ingresamos a traves del link proporcionado en la documentacion donde veremos seis endpoints,puntos de informacion.
1)Cantidad_filmaciones_dia este punto de informacion requiere que le indiques un dia de la semana en español y brindara la cantidad de peliculas que se producieron historicamente en ese dia.
2)Cantidad_filmaciones_mes este punto de informacion requiere que le indiques un mes del año en español y brindara la cantidad de peliculas que se producieron historicamente en ese mes.
3)Score_titulo este punto de informacion requiere que le indiques el titulo de una pelicula y brindara informacion sobre  el año de su lanzamiento y su popularidad.
4)Votos_titulo este punto de informacion requiere que le indiques el titulo de una pelicula y brindara informacion sobre  el año de su lanzamiento,la cantidad de votos recibidos en IDMB y su promedio
5)Get_actor este punto de informacion requiere que le indiques el nombre de un actor y brindara informacion sobre la cantidad de peliculas en las que participo ,el retorno de inversion de las mismas y el promedio de ellas.El retorno nos indicara cuantos dolares generaron las peliculas,por ejemplo un retorno de dos indica que por cada peso invertido la ganancia bruta fue de dos.
6)Get_director este punto de informacion requiere que le indiques el nombre de un director y brindara informacion sobre las peliculas en las que participo asi como el año de su lanzamientos y algunos datos sobre su exito economico.
7)Recomendacion este punto de informacion requiere que le indiques el nombre de una pelicula y brindara los nombres de los cinco titulos mas similares para que puedas disfrutar.


PROCESO
#### ETL(Extraccion,Transformacion,Carga)

_Comenzamos con dos datasets, "movies_datasets.csv" y "credits.csv". 
_Generamos dos tablas(Dataframes) una para cada fuente de datos.Las mismas contaban con datos anidados con diccionarios o listas de diccionarios dificultando el acceso a la informacion.
_Las columnas anidadas de la tabla credits fueron desarmadas mediante funciones.
_Exploramos los valores de ID de ambas tablas y eliminamos los valores duplicados.
_Hicimos un merge how=left para mantener todos los registros de movies_datasets y agregar columnas provenientes de credits,asi logramos tener todos los datos completos en una sola tabla.

Ahora tenemos todos los datos integrados en una sola tabla.

Luego se continuo con los siguientes procesos:
_Eliminamos columnas innecesarias para el proceso.
_Luego evaluamnos los valores nulos de las columnas "revenue" y "budget",los rellenamos con 0 y cambiamos los tipos de datos.
_Se creo una nueva columna para sacar el retorno dividiendo los valores de cada fila de las columnas "revenue" y "budget".
_Eliminamos registros que tengan valores nulos en la columna "release_date".
_Se cambio el formato de la columna "release_date" para que sea el adecuado; AAAA-mm-dd.
_Se crearon columnas para el dia,el año y el mes.
_Se crearon las funciones que posteriormente serian cargadas para ser consumidas por la API.
_Para finalizar se guardaron los cambios hechos en el proceso en data.csv.


### EDA(Analisis exploratorio de datos)

El objetivo del EDA fue conocer la calidad de los datos verificando los tipos y la consistencia de los mismos,tambien indagamos en valores atipicos para las variables de tipo cuantitativas.Ademas tuvimos una primera aproximacion a la distribucion y comportamiento de los datos informacion valiosa para generar analisis posteriores con mayor profundidad.
En este analisis no relacionamos columnas excepto en el caso de "vote_average" y "popularity" gracias al cual concluimos que los datos de popularity no tenian la calidad esperada.Acompañamos el analisis con graficos y algunas breves conclusiones como el rapido crecimiento en la cantidad de peliculas producidas en los ultimos años.Para variables cualitativas nominales utilizamos la libreria Wordcloud para mostrar graficamente la frecuencia de las mismas.


### Sistema de recomendacion

Tuvimos un problema al subir la carpeta al repositorio local generando la perdida del archivo en el cual se desarrollo el mismo por lo que a continuacion indicaremos el proceso que se siguio.

1_Se importo desde la libreria
2_Generamos una tabla(dataframe) basado en data.csv obtenido previamente gracias al proceso de ETL.
3_Se seleccionaron las columnas que serian utilizadas:title,release_year,vote_average,genres,runtime y original_languages.
4_Se reducio el dataframe a solo aquellos titulos que tuvieran todos los valores.
4_Seteamos el index del dataframe con la columna title.
5_Para las demas columnas generamos rangos y utilizamos pandas.cut() para asignar los valores a los rangos
6_Utilizamos la funcion get_dummies para codificar de manera binaria con 0 y 1 
7_Una vez que tenemos todas las columnas serializadas en 0 y 1 las concatenamos
8_Utilizamos similitud coseno para generar una matriz de similitud donde los index y las columnas van a ser los titulos de las peliculas 
9_Como tenemos un dataset acotado para que sea posible su procesamiento,generamos una funcion gracias a la libreria TfidfVectorizer para determinar la cercania del titulo ingresado por el usuario con otros del dataset.
10_En base al titulo mas cercano buscamos los 5 titulos con mayor similitud.
