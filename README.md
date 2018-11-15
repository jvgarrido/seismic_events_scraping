# seismic_events_scraping
Script Python y Dataset con los datos de eventos sísmicos de todo el mundo


Este script esta programado utilizando Selenium con el driver de Firefox y Beautifulsoup.

Los requerimientos para su ejecución son los siguientes:

Tener Python instalado

El driver ha de estar en el PATH , en este caso se ha utilizado \geckodriver-v0.23.0-win64\

Hay que instalar Selenium
pip install selenium

Hay que instalar BeautifulSoup
pip install beautifulsoup4


El dataset contiene datos desde la fecha actual 2018/11/15 hasta 2018/09/01
Un total de 10279 registros de eventos sísmicos

El script toma la fecha actual y dentro del codigo tenemos la variable extract_to_date que podemos modificar para elegir el intervalo de las fechas

Para ejecutar el script : seismic_events_scrp.py
