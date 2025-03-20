# Extractor de Audio de OSU

Este programa permite extraer automáticamente los archivos de audio de los beatmaps de OSU (archivos .osz) sin necesidad de convertirlos manualmente a mp3.

## Características

- Extrae archivos de audio (mp3) de los archivos .osz
- Procesa múltiples archivos en una carpeta y sus subcarpetas
- Renombra los archivos de audio con el nombre del beatmap
- Muestra un resumen de la operación

## Requisitos

- Python 3.6 o superior
- No requiere bibliotecas externas (usa módulos estándar de Python)

## Uso

- Abrir el programa para que se generen las carpetas de entrada y salida.
- Colocar los archivos.osz en la carpeta de entrada.
- Ejecutar el programa nuevamente.

## Notas

- El programa no elimina/modifíca los archivos.osz originales

- ## Autor
- Este programa fue creado por [Fernando Zamorano](https://luisvallez.github.io/Portafolio/)

## Funcionamiento

El programa:

1. Busca todos los archivos .osz en la carpeta de entrada y sus subcarpetas
2. Busca archivos de audio dentro del archivo
3. Extrae los archivos de audio (canciones) encontrados
4. Renombra los archivos con el nombre del beatmap
5. Muestra un resumen de la operación
