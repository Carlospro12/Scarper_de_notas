# 📰 Scraper de notas orquestado por Apache Airflow 🌬️


Este proyecto tiene como objetivo principal extraer las notas de un periódico específico utilizando un scraper y orquestando el proceso mediante Apache Airflow. Todo esto se realiza en un entorno Google Cloud ☁️, aprovechando las herramientas y servicios que nos ofrece la plataforma.

## Tecnologías utilizadas 🚀

- Python 🐍
- Apache Airflow 🌬️
- Google Cloud Storage 🗄️
- Google Cloud Composer 🎵
- lxml 🌳
- requests 🌐
- Slack 💬

## ¿Cómo funciona? 🤔

El proceso comienza con un desencadenador de Airflow que se ejecuta según una programación definida. El scraper se encarga de extraer las notas del periódico y las almacena en un archivo CSV.

Posteriormente, el archivo CSV es subido a un bucket de Google Cloud Storage para su almacenamiento y procesamiento posterior. 

Este proyecto también cuenta con la funcionalidad de notificar a través de un canal de Slack una vez que los archivos han sido guardados en el bucket de Google Cloud Storage. Esto es especialmente útil para mantener al equipo informado del proceso y asegurarse de que los archivos se estén guardando correctamente.

## Contribuyendo 🤝

¡Siéntete libre de contribuir a este proyecto! Puedes hacerlo mediante la apertura de una solicitud de extracción y comentar sobre las mejoras que propones.

## Licencia 📜

Este proyecto se distribuye bajo la licencia MIT. Siéntete libre de usarlo para tus propios proyectos o para fines comerciales.
