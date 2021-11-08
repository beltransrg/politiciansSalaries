#PEC 1 Practica de Web Scraping
Práctica 1 de la asignatura Tipología y ciclo de vida de los datos.
Extracción atributos asociados a cargos públicos del portal de trasparencia Newtral.
(https://transparentia.newtral.es/)


### General Info
Para ejecutar el script es necesario instalar las siguientes bibliotecas:
 pip install selenium
 
También es necesario disponer de firefox Browser instalado para poder realizar la navegación.
 
La ejecución del fichero se lleva a cabo mediante el job de python scraper.py sin necesidad de incluir parámetros.
En la carpeta docs/ se puede encontrar el resultado de la extracción en formato csv bajo el nombre "SPANISH_POLITICIANS_SALARIES.csv"



├── LICENSE
├── README.md          
├── data
│   └── SPANISH_POLITICIANS_SALARIES.csv            <- Dataset generado
├── notebooks          <- En la carpeta notebooks encontramos un acceso vía notebook al código
│
├── pec1src            <- Código fuente empleado en este proyecto
│   ├── __init__.py    <- Creación del módulo Python
│   │
│   ├── scrapper.py   	<- Módulo principal para ejecutar el proceso de extracción
│   │				   		
│   ├── writer  	<-  Módulo python encargado de generar el fichero de salida a partir de una lista proporcionada por el módulo scrapper.py
