from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer



app = FastAPI()

#http://127.0.0.1:8000

#@ app.get es el decorador que indica el objeto app va utilizar metodo http get y la ruta,que con "/" es la ruta raiz
#async lo utilizamos para indicar que es una funcion asincronica

data = pd.read_csv("data.csv")

@app.get("/")
async def inicio():
    return {"message":"Bienvenido a la API de Proyecto individual Henry"}


@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia:str):
   '''Ingrese un dia de la semana en Español y podras ver la cantidad de estrenos historicos en ese dia '''
   dia = dia.capitalize()
   if dia == "Lunes":
      day = "Monday"
   elif dia == "Martes":
      day = "Tuesday"
   elif dia == "Miercoles":
      day = "Wednesday"
   elif dia == "Jueves":
      day = "Thursday"
   elif dia == "Viernes":
      day = "Friday"
   elif dia == "Sabado":
      day = "Saturday"
   elif dia == "Domingo":
      day = "Sunday"
   else:
      return {"respuesta":"Ha ingresado un dia incorrecto vuelva a intentarlo"}
   cantidad = (data[data["release_day"] == day]).shape[0]
   return {'dia': dia, 'cantidad': cantidad}

@app.get("/cantidad_filmaciones_mes/{mes}")
async def  cantidad_filmaciones_mes(mes:str):
   '''Ingrese un mes del año en Español y podras ver la cantidad de estrenos historicos en ese mes '''
   mes = mes.capitalize()
   meses = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
   if mes not in meses:
      return {"respuesta":"Ha ingresado un mes incorrecto vuelva a intentarlo"}
   for i,elemento in enumerate(meses):
      if mes == elemento:
          month = i+1
          break
   cantidad =(data[data["release_month"] == month]).shape[0]
   return {'mes':mes, 'cantidad':cantidad}


@app.get("/score_titulo/{titulo}")
def score_titulo( titulo:str ):
   '''Ingrese un nombre de pelicula y podras ver el año de estreno y que tan popular es '''
   dataframe = data[data["title"] == titulo]
   if dataframe.shape[0] < 1:
      return {"respuesta":"Hemos intentado encontrar informacion sobre la pelicula,pero no lo hemos logrado.Le sugerimos pruebe con esta pelicula, Jumanji"}
   if dataframe.shape[0] > 1:
      dataframe = dataframe.sort_values("release_year", ascending=False)
   anio = dataframe["release_year"].iloc[0]
   popularidad = dataframe["popularity"].iloc[0]
   return {'titulo': titulo, 'anio':int(anio) , 'popularidad':popularidad}



@app.get("/votos_titulos/{titulo}") 
def votos_titulo(titulo):
   '''Ingrese un nombre de pelicula y podras ver el año de estreno y sus valoraciones '''
   dataframe = data[data["title"] == titulo]
   dataframe = dataframe.sort_values('release_year', ascending=False)
   anio = (dataframe["release_year"].iloc[0])
   valoraciones = dataframe["vote_count"].iloc[0]
   promedio = round((dataframe["vote_average"].iloc[0]),2)
   if valoraciones>=2000:
       return {'titulo': titulo, 'anio':int(anio) ,'voto_total':valoraciones, 'voto_promedio':promedio}
   else:
      return {"respuesta":"La película tiene menos de 2000 valoraciones,intente con otro titutlo"}


@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor:str):
   '''Ingrese un nombre de actor y podras ver la cantidad de peliculas en las que ha participado y su exito '''
   #Utilizamos el metodo explode para ampliar los registros,uno para cada actor de la lista y luego una funcion lambda para crear una mascara para registros donde aparesca el nombre del actor
   dataframe = data[data['actor_names'].apply(lambda x: nombre_actor in x)]
   #En algunas peliculas los directores tambien participan por lo que en este paso aclaramos que si para esa pelicula ademas de actor fue direcctor no la tome en cuenta
   if dataframe.shape[0] == 0:
      return f"Hemos intentado encontrar informacion sobre las peliculas dirigidas por {nombre_actor},pero no lo hemos logrado.Le sugerimos pruebe con este actor, Brad Pitt"
   cantidad = dataframe.shape[0]
   #Utilizamos una mascara para que las peliculas que tienen retorno 0 no generen ruido en el promedio
   dataframe = dataframe[dataframe["return"] != 0 ]
   retorno = round((dataframe["return"].sum()),2)
   promedio = round((retorno/cantidad),2)
   return {'actor':nombre_actor, 'cantidad_filmaciones':cantidad, 'retorno_total':retorno,'retorno_promedio':promedio}


@app.get("/get_director/{nombre_director}")
async def get_director(nombre_director:str):
   '''Ingrese un nombre de director y podras ver informacion sobre sus peliculas y su exito '''
   dataframe = data[data['director_names'].apply(lambda x: nombre_director in x)]
   if dataframe.shape[0] < 1:
      return f"Hemos intentado encontrar informacion sobre las peliculas dirigidas por {nombre_director},pero no lo hemos logrado.Le sugerimos pruebe con este director, John Lasseter"
   dataframe = dataframe[dataframe["return"] != 0 ]
   retorno = round((dataframe["return"].sum()),2)
   nombre = dataframe["title"].to_list()
   fecha = dataframe["release_date"].to_list()
   retorno_ind = dataframe["return"].to_list()
   costo = dataframe["budget"].to_list()
   ganancia = dataframe["revenue"].to_list()
   return {'director': nombre_director, 'retorno_total_director':retorno, 
           'peliculas':nombre, 'anio':fecha, 'retorno_pelicula':retorno_ind, 
           'budget_pelicula':costo, 'revenue_pelicula':ganancia
           }



data_similitud = pd.read_csv("similitud.csv",index_col="title")

@app.get('/recomendacion/{titulo}')
def recomendacion(titulo: str):
    '''Ingresa un nombre de película y recibe una recomendación de cinco películas similares'''
    if titulo in data_similitud.columns:
        # Obtén los valores de similitud de la película con todas las demás películas
        similitudes = data_similitud[titulo].values
        # Ordena los valores de similitud de forma descendente y obtén los índices correspondientes
        indices_ordenados = np.argsort(similitudes)[::-1]
        # Obtén los nombres de las películas más similares (excluyendo la película dada)
        peliculas_similares = [data_similitud.columns[idx] for idx in indices_ordenados if data_similitud.columns[idx] != titulo]
        # Limita la lista a las 5 películas más similares
        peliculas_similares = peliculas_similares[:5]
    else:
        # No se encontró el título exacto, se realizará una búsqueda aproximada
        vectorizer = TfidfVectorizer()
        titulos_peliculas = list(data_similitud.columns)
        titulos_peliculas.append(titulo)  # Agrega el título ingresado a la lista de títulos
        matriz_tfidf = vectorizer.fit_transform(titulos_peliculas)
        # Calcula la similitud coseno entre el título ingresado y todos los títulos
        similitud = cosine_similarity(matriz_tfidf[-1], matriz_tfidf[:-1])
        # Encuentra el índice de la película más similar en orden descendente
        indice_pelicula_similar = np.argmax(similitud)
        # Obtén el nombre de la película más similar
        pelicula_similar = titulos_peliculas[indice_pelicula_similar]
        # Obtén los valores de similitud de la película similar con todas las demás películas
        similitudes = data_similitud[pelicula_similar].values
        # Ordena los valores de similitud de forma descendente y obtén los índices correspondientes
        indices_ordenados = np.argsort(similitudes)[::-1]
        # Obtén los nombres de las películas más similares (excluyendo la película similar)
        peliculas_similares = [data_similitud.columns[idx] for idx in indices_ordenados if data_similitud.columns[idx] != pelicula_similar]
        # Limita la lista a las 5 películas más similares
        peliculas_similares = peliculas_similares[:5]
    return {'lista_recomendada': peliculas_similares}




