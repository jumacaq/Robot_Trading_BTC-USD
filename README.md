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
Necesitaremos acceder a la API de Yahoo Finance que proporciona datos históricos de precios de Bitcoin en formato JSON, para esto usaremos la biblioteca yfinance de Python,cuya documentación esta en el siguiente enlace: https://pypi.org/project/yfinance/ <br> 

![image](https://github.com/jumacaq/Robot_Trading_BTC-USD/blob/main/yfinance.png))

Luego, utilizando la biblioteca BeautifulSoup realizaremos el Web Scraping de la página https://coinmarketcap.com/ para extraer el precio actual del Bitcoin BTC en dólares USD y la variación de su precio en la última hora, luego crearemos una función que retornará el precio actualizado del Bitcoin y también su tendencia <br>
<br>
![image](https://github.com/Valamca/Robot_Trading/assets/129345721/4f3e3df5-1afe-4c40-8610-9589e6d8c10e)

### Limpieza de datos: 
Una vez cargados los datos en un DataFrame de Pandas se procede a su tratamiento y manipulación para obtener una base limpia, luego se construye la función que retornará el precio promedio del Bitcoin.

### Tomar decisiones: 
Con la obtención del precio promedio, se compara con el precio actual y tendencia del Bitcoin, que previamente se obtuvo con Web Scraping, con estas tres variables crearemos la función que retornará el algoritmo de decisión, el cual es un algoritmo simple que ayudará a los clientes inexpertos a decidir el mejor momento de comprar o vender Bitcoin.

### Visualización: 
Se utiliza la librería Matplotlib para crear una función que retornará el gráfico donde se mostrará la evolución del precio del Bitcoin durante el periodo seleccionado al obtener los datos históricos, se dibujarán dos líneas: una fluctuante que indica el movimiento del precio y la otra plana que representa el precio promedio. Por último, se muestra un mensaje en el gráfico que indique “Vender”, “Comprar” o “Esperar” según sea la decisión del algoritmo.<br>
<br>

### Automatización: 
Finalmente, ahora que se tienen: la extracción de información,  la limpieza de datos, la visualización, y el algoritmo de decisión, es hora de automatizar el proceso. Se utiliza la librería de Python "time" para ejecutar el algoritmo de decisión cada 5 minutos y actualizar el gráfico, además del método clear_output para limpiar el gráfico antes de volver a iniciar el ciclo.<br>



