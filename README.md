![](https://github.com/jumacaq/Robot_Trading_BTC-USD/blob/main/robot_btc.png)
# Robot_Trading_BTC-USD
## Descripción: 
Desarrollamos este programa con librerías del lenguaje Python dentro de un notebook de Google Colab con el fin de tomar decisiones de compra y venta de Bitcoin en tiempo real.
El proyecto consta de los siguientes pasos:

### Configuración del ambiente: 
Utilizaremos el Jupyter Notebook que ofrece Google Colaboratory, también necesitarás instalar algunas librerías de Python que son esenciales para este proyecto, como: <br>
<br>
- Numpy 
- Pandas 
- Matplotlib
- Yfinance
- BeautifulSoup
- Request
- Clear_output
- Time

### Obtención de datos:
Necesitaremos acceder a la API de Yahoo Finance que proporciona datos históricos de precios de Bitcoin en formato JSON, para esto usaremos la biblioteca yfinance de Python,cuya documentación esta en el siguiente enlace: https://pypi.org/project/yfinance/ (Haz clic derecho y selecciona "Abrir en una nueva pestaña") <br> 

![image](https://github.com/jumacaq/Robot_Trading_BTC-USD/blob/main/yfinance.png))

Luego, utilizando la biblioteca BeautifulSoup realizaremos el Web Scraping de la página https://coinmarketcap.com/ (Haz clic derecho y selecciona "Abrir en una nueva pestaña") para extraer el precio actual del Bitcoin BTC en dólares USD y la variación de su precio en la última hora, luego crearemos una función que retornará el precio actualizado del Bitcoin y también su tendencia <br>
<br>
![image](https://github.com/Valamca/Robot_Trading/assets/129345721/4f3e3df5-1afe-4c40-8610-9589e6d8c10e)

### Limpieza de datos: 
Una vez cargados los datos en un DataFrame de Pandas se procede a su tratamiento y manipulación para obtener una base limpia, luego se construye la función que retornará el precio promedio del Bitcoin.

### Tomar decisiones: 
Primero creamos una función calcular_sma() para calcular las SMA(Media movil simple) de corto y largo plazo las cuales sirven para suavizar fluctuaciones y como indicadores de toma de decisiones.

Luego crearemos una función tomar_decisiones() dentro de ella construiremos el algoritmo que retornará la variable algoritmo_decision que nos indicará cuando comprar, vender o esperar.

### Visualización: 
Se utiliza la librería Matplotlib para crear una función que retornará el gráfico donde se mostrará la evolución del precio del Bitcoin durante el periodo seleccionado al obtener los datos históricos, se dibujarán tres líneas: una que indica el movimiento del precio y las otras dos que reflejan el recorrido de la media movil corta(SMA_short) y la media móvil larga(SMA_long) . Por último, se agrega un cuadro de texto a la señal de decisión en el gráfico que indique “Vender”, “Comprar” o “Esperar” según sea la decisión del algoritmo.<br>
<br>

### Automatización: 
Finalmente, ahora que se tienen: la extracción de información,  la limpieza de datos, la visualización, y el algoritmo de decisión, es hora de automatizar el proceso. Se utiliza la librería de Python "time" para ejecutar el algoritmo de decisión cada 5 minutos y actualizar el gráfico.

### Despliegue en streamlit:
Este robot trading esta desplegado en streamlit [Visitalo aquí](https://robot-trading-btc-usd.streamlit.app/) que tiene una sección lateral izquierda para ajustar los parámetros de las medias móviles y una sección principal donde se muestran datos actualizados cada 5 minutos del precio de bitcoin, la tendencia, el precio promedio de los últimos 14 días, los parámetros de las medias móviles, la decisión de compra/ venta /espera y el gráfico de visualización.


