
#Forzar CPU "normal", para evitar problemas con la aceleracion de oneDNN
import os
os.environ["FLAGS_use_oneDNN"] = "0"
#No tenemos conectividad
os.environ["DISABLE_MODEL_SOURCE_CHECK"] = "True"
import pandas as pd

from prompt_ia import extraer_datos_con_ia
from comprobar_json import comprobar_respuesta
from ocr_pdf import leer_imagenes, pdf_a_imagenes

CARPETA_PDFS = "pdfs"
SALIDA_EXCEL = "salida/resultado.xlsx"

def main():
    resultados = []

    # Crear carpeta de salida si no existe
    os.makedirs(os.path.dirname(SALIDA_EXCEL), exist_ok=True)

    archivos = os.listdir(CARPETA_PDFS)
    if not archivos:
        print(f"⚠️ No hay archivos en la carpeta {CARPETA_PDFS}")
        return

    for archivo in archivos:
        if not archivo.lower().endswith(".pdf"):
            continue

        ruta_pdf = os.path.join(CARPETA_PDFS, archivo)
        print(f"\nProcesando: {archivo}")

        try:
            # 1️⃣ Convertir PDF a imágenes
            imagenes = pdf_a_imagenes(ruta_pdf)

            # 2️⃣ Aplicar OCR
            texto = leer_imagenes(imagenes)
            print(texto)

            """if not texto.strip():
                print(f"   ⚠️ No se pudo extraer texto de {archivo}")
                continue"""
            # 4️⃣ Llamar a la IA
            respuesta_ia = extraer_datos_con_ia(texto)
            print(respuesta_ia)
            print(respuesta_ia)
            # 5️⃣ Validar / parsear JSON
            datos = comprobar_respuesta(respuesta_ia, ruta_pdf)

            # 6️⃣ Añadir metadatos
            datos["archivo"] = archivo
            resultados.append(datos)

        except Exception as e:
            print(f"⚠️ Error procesando {archivo}: {e}")
            continue

    # 7️⃣ Crear Excel si hay resultados
    if resultados:
        df = pd.DataFrame(resultados)
        df.to_excel(SALIDA_EXCEL, index=False)
        print(f"\n✅ Proceso terminado. Excel generado en: {SALIDA_EXCEL}")
    else:
        print("\n⚠️ No se generaron resultados.")

if __name__ == "__main__":
    main()
