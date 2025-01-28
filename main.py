import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import yfinance as yf
import time
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from IPython.display import clear_output

# Configuración de la página principal
# Cargar la imagen
image = Image.open("btc.png")  # Reemplaza con la ruta de tu imagen

# Crear dos columnas: una para la imagen y otra para el título
col1, col2 = st.columns([0.2, 0.8])  # Ajusta el ancho de las columnas según sea necesario

# Colocar la imagen en la primera columna (izquierda)
with col1:
    st.image(image, width=100)  # Ajusta el ancho de la imagen según sea necesario

# Colocar el título en la segunda columna (derecha)
with col2:
    st.title("Bot de Trading de Bitcoin")
#st.title("Bot de Trading de Bitcoin")

# Configuración de la barra lateral

#image = Image.open("btc.png")  # Reemplaza con la ruta de tu imagen
st.sidebar.title("Parámetros de SMA")
#st.sidebar.image(image, use_column_width=True)

# Sliders para los períodos de SMA
sma_short = st.sidebar.slider("Periodo de SMA corto", min_value=5, max_value=50, value=10)
sma_long = st.sidebar.slider("Periodo de SMA largo", min_value=20, max_value=100, value=50)

# Función para importar datos de Bitcoin
def importar_base_bitcoin():
    global df_bitcoin
    end_date = datetime.now()
    start_date = end_date - timedelta(days=14)
    df_bitcoin = yf.download(
        tickers="BTC-USD",
        start=start_date.strftime('%Y-%m-%d'),
        end=end_date.strftime('%Y-%m-%d'),
        interval="15m"
    )
    if df_bitcoin.empty:
        raise ValueError("No se encontraron datos para el intervalo especificado.")
    df_bitcoin.columns = [col[0] for col in df_bitcoin.columns]
    return df_bitcoin

# Función para extraer el precio actual y la tendencia de Bitcoin
def extraer_tendencias():
    global precio_actual, tendencia, color
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"}
    url = "https://coinmarketcap.com/es/currencies/bitcoin/"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        s = BeautifulSoup(response.content, "html.parser")
        label_precio = s.find('span', {"data-test": "text-cdp-price-display"})
        if label_precio:
            precio_actual = float(label_precio.getText().replace("$", "").replace(",", ""))
        else:
            precio_actual = None
        label_variacion = s.find('p', {'color': True, 'data-change': True})
        if label_variacion:
            color = label_variacion['color']
            if color == 'green':
                tendencia = "alta"
            elif color == 'red':
                tendencia = "baja"
            else:
                tendencia = None
        return precio_actual, tendencia
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud: {e}")
        return None, None

# Función para limpiar los datos
def limpieza_datos():
    global df_bitcoin, df_bitcoin_limpio, media_bitcoin
    df_bitcoin_limpio = df_bitcoin.copy()
    df_bitcoin_limpio = df_bitcoin_limpio[~df_bitcoin_limpio.index.duplicated(keep='first')]
    df_bitcoin_limpio['Close'] = df_bitcoin_limpio['Close'].ffill()
    df_bitcoin_limpio = df_bitcoin_limpio[df_bitcoin_limpio['Volume'] > 0]
    Q1 = df_bitcoin_limpio['Close'].quantile(.25)
    Q3 = df_bitcoin_limpio['Close'].quantile(.75)
    IQR = Q3 - Q1
    selection = (df_bitcoin_limpio['Close'] >= Q1 - 1.5 * IQR) & (df_bitcoin_limpio['Close'] <= Q3 + 1.5 * IQR)
    df_bitcoin_limpio = df_bitcoin_limpio[selection]
    media_bitcoin = df_bitcoin_limpio['Close'].mean().round(2)
    return df_bitcoin_limpio, media_bitcoin

# Función para calcular las medias móviles
def calcular_sma():
    global df_bitcoin_limpio
    df_bitcoin_limpio['SMA_short'] = df_bitcoin_limpio['Close'].rolling(window=sma_short).mean()
    df_bitcoin_limpio['SMA_long'] = df_bitcoin_limpio['Close'].rolling(window=sma_long).mean()
    return df_bitcoin_limpio

# Función para tomar decisiones basadas en SMA
def tomar_decisiones():
    global df_bitcoin_limpio, precio_actual, tendencia, media_bitcoin, algoritmo_decision, color
    if 'SMA_short' not in df_bitcoin_limpio or 'SMA_long' not in df_bitcoin_limpio:
        raise ValueError("Faltan las columnas SMA_short y SMA_long.")
    if 'Decision' not in df_bitcoin_limpio:
        df_bitcoin_limpio['Decision'] = 'Wait'
    latest_data = df_bitcoin_limpio.iloc[-1]
    sma_corto = latest_data['SMA_short']
    sma_largo = latest_data['SMA_long']
    if sma_corto > sma_largo and precio_actual < media_bitcoin and tendencia == 'alta':
        algoritmo_decision = 'Comprar'
        color = '#228b22'
    elif sma_corto < sma_largo and precio_actual >= media_bitcoin and tendencia == 'baja':
        algoritmo_decision = 'Vender'
        color = '#dc143c'
    else:
        algoritmo_decision = 'Esperar'
        color = '#ff8c00'
    df_bitcoin_limpio.loc[df_bitcoin_limpio.index[-1], 'Decision'] = algoritmo_decision
    return df_bitcoin_limpio, algoritmo_decision, color

# Función para visualizar los datos
#Creamos la función visualizacion()
def visualizacion():
  global df_bitcoin_limpio, precio_actual, tendencia, media_bitcoin, algoritmo_decision
  plt.clf()  # Limpia la figura actual
  df_bitcoin_limpio['Average'] = media_bitcoin
  #Algoritmo para dar color al texto de la variable 'algoritmo_decision'
  if algoritmo_decision == 'Vender':
      color_decision = 'green'
  elif algoritmo_decision =='Comprar':
      color_decision = 'red'
  else:
      color_decision = '#ff8c00'
  #Configuramos el tamaño del gráfico en una proporción de 16x5,damos color al fondo del gráfico
  plt.rc('figure',figsize = (15,8),facecolor='#E8DEE1')
  #Agregamos un título al gráfico y a los ejes x,y
  plt.title('GRAFICO PARA DECIDIR COMPRA-VENTA DE BITCOIN',fontsize=20,weight = 'bold')
  plt.xlabel('Fecha')
  plt.ylabel('Precio Actual en USD')
  #Con el método plot()dibujamos una línea en el gráfico, con los datos del índice y la columna 'Close' de la base
  #df_bitcoin,nombramos etiqueta,damos estilo y color a dicha línea
  plt.plot(df_bitcoin_limpio.index, df_bitcoin_limpio['Close'], label='Precio de Cierre', linestyle='-', color='Gray', alpha=0.7)
  #Con el método plot()dibujamos una línea en el gráfico, con los datos del índice y la columna 'Promedio' de la base
  #df_bitcoin,nombramos etiqueta y damos estilo y color
  plt.plot(df_bitcoin_limpio.index, df_bitcoin_limpio['Average'], label='Precio Promedio', linestyle='dashdot', color='Red')
  #Creating SMA_short line
  plt.plot(df_bitcoin_limpio.index, df_bitcoin_limpio['SMA_short'], label='SMA_short', linestyle='-', color='Blue',alpha=0.8)
  #Creating SMA_long line
  plt.plot(df_bitcoin_limpio.index, df_bitcoin_limpio['SMA_long'], label='SMA_long', linestyle='-', color='Orange',alpha=0.8)
  #Con el método annotate()muestra un mensaje dentro del gráfico con la decisión calculada del algoritmo_decision,
  #damos al texto tamaño, color y resaltamos
  plt.annotate(f'Decision: {algoritmo_decision}',xy=(df_bitcoin_limpio.index[-1], 103000), fontsize=12,
               color=color_decision,weight = 'bold')
  #Agregamos leyendas al gráfico
  plt.legend()
  #Agregamos cuadrículas al gráfico, para observar mejor las intersecciones de los ejes
  plt.grid(True,alpha=0.3)
  st.pyplot(plt)

# Ejecución principal
while True:
    try:
        clear_output()
        importar_base_bitcoin()
        extraer_tendencias()
        limpieza_datos()
        calcular_sma()  # Asegúrate de llamar a calcular_sma() antes de tomar_decisiones()
        tomar_decisiones()
        st.write(f"**Precio actual de Bitcoin:** ${precio_actual}")
        st.write(f"**Tendencia:** {tendencia}")
        st.write(f"**Precio promedio:** ${media_bitcoin}")
        st.write(f"**Parámetros de SMA:** Corto = {sma_short}, Largo = {sma_long}")
        st.write(f"**Decisión del algoritmo:** {algoritmo_decision}")
        st.write("**Iniciando ciclo de análisis:**")
        visualizacion()
        time.sleep(300)
    except Exception as e:
        st.error(f"Error: {e}")
        time.sleep(300)
