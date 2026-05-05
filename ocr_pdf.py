"""
Este archivo hace:
    -La pdf_a_imagenes, coge el pdf, lo pasa a imagenes para que lo pueda entender el OCR
    -La funcion leer_imagenes, lo que hace es de las imagenes coger el texto y lo devuelve
"""
#Forzar CPU "normal", para evitar problemas con la aceleracion de oneDNN
import os
os.environ["FLAGS_use_oneDNN"] = "0"
#No tenemos conectividad
os.environ["DISABLE_MODEL_SOURCE_CHECK"] = "True"

from pdf2image import convert_from_path
import numpy as np

def pdf_a_imagenes(ruta):
    imagenes = convert_from_path(ruta, dpi=300)
    return imagenes

def leer_imagenes(imagenes, ocr, detecta_tablas):
    resultado_final={
        "texto":"",
        "tablas":[]
    }
    for img in imagenes:
        img_np=np.array(img)
        resultado_ocr = ocr.ocr(img_np)

        for linea in resultado_ocr[0]:
            resultado_final["texto"]+=linea[1][0]+"\n"

        estructura=detecta_tablas(img_np)
        for bloque in estructura:
            if bloque["type"] == "table":
                resultado_final["tablas"].append(
                    bloque["res"]["html"]
                )
    return resultado_final