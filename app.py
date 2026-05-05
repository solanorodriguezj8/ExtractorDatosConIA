# Importamos todo lo que necesitamos del flask, ademas de los archivos del programa
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import pandas as pd
import threading
import uuid

from prompt_ia import extraer_datos_con_ia
from comprobar_json import comprobar_respuesta
from ocr_pdf import leer_imagenes, pdf_a_imagenes

from paddleocr import PaddleOCR, PPStructure

# Inicializamos el OCR
ocr = PaddleOCR(
    use_angle_cls=True,
    lang="es",
    use_gpu=False,
    show_log=False
)

# Inicializamos para detectar tablas
detecta_tablas = PPStructure(
    show_log=False,
    use_gpu=False
)

app = Flask(__name__)
CORS(app)

# Variables constantes
CARPETA_PDFS = "pdfs"
SALIDA_EXCEL = "salida/resultado.xlsx"

os.makedirs(CARPETA_PDFS, exist_ok=True)
os.makedirs("salida", exist_ok=True)

# Diccionario para guardar el estado de los trabajos
jobs = {}

def procesar_trabajo(job_id, rutas, total_archivos):
    """Función que corre en segundo plano"""
    try:
        resultados = []

        for i, ruta_pdf in enumerate(rutas):

            jobs[job_id]['status'] = 'processing'
            jobs[job_id]['message'] = f"Procesando archivo {i+1} de {total_archivos}: {os.path.basename(ruta_pdf)}"
            jobs[job_id]['progress'] = int(((i+1) / total_archivos) * 100)

            try:
                imagenes = pdf_a_imagenes(ruta_pdf)
                texto = leer_imagenes(imagenes, ocr, detecta_tablas)
                respuesta_ia = extraer_datos_con_ia(texto)
                datos = comprobar_respuesta(respuesta_ia, ruta_pdf)

                datos["archivo"] = os.path.basename(ruta_pdf)
                resultados.append(datos)

            except Exception as e:

                print("Error en archivo:", e)

                jobs[job_id]['message'] = f"Error en archivo: {os.path.basename(ruta_pdf)}"
                jobs[job_id]['status'] = 'error'
                break

        if jobs[job_id]['status'] != 'error':

            if resultados:

                excel_path = f"salida/resultado.xlsx"

                df = pd.DataFrame(resultados)
                df.to_excel(excel_path, index=False)

                jobs[job_id]['status'] = 'done'
                jobs[job_id]['message'] = "Proceso completado. Listo para descargar."
                jobs[job_id]['file_path'] = excel_path

            else:

                jobs[job_id]['status'] = 'error'
                jobs[job_id]['message'] = "No se generaron resultados."

    except Exception as e:

        jobs[job_id]['status'] = 'error'
        jobs[job_id]['message'] = f"Error general: {str(e)}"

    finally:

        limpiar_pdfs(rutas)


@app.route("/procesar", methods=["POST"])
def procesar():

    archivos = request.files.getlist("pdfs")

    if not archivos:
        return jsonify({"error": "No se enviaron PDFs"}), 400

    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        'status': 'waiting',
        'message': 'Iniciando proceso...',
        'progress': 0,
        'file_path': None
    }

    rutas = []

    for archivo in archivos:

        ruta = os.path.join(CARPETA_PDFS, archivo.filename)
        archivo.save(ruta)
        rutas.append(ruta)

    thread = threading.Thread(
        target=procesar_trabajo,
        args=(job_id, rutas, len(rutas))
    )

    thread.daemon = True
    thread.start()

    return jsonify({
        "job_id": job_id,
        "message": "Proceso iniciado"
    })


@app.route("/status/<job_id>")
def status(job_id):

    if job_id in jobs:
        return jsonify(jobs[job_id])

    return jsonify({"error": "Job no encontrado"}), 404


@app.route("/download/<job_id>")
def download(job_id):

    if job_id in jobs and jobs[job_id]['status'] == 'done':

        file_path = jobs[job_id]['file_path']

        if os.path.exists(file_path):

            return send_file(
                file_path,
                as_attachment=True,
                download_name="resultado.xlsx"
            )

    return jsonify({"error": "Archivo no disponible"}), 404


def limpiar_pdfs(rutas):

    """Elimina los PDFs procesados"""

    for ruta in rutas:

        try:
            if os.path.exists(ruta):
                os.remove(ruta)

        except Exception as e:
            print(f"No se pudo eliminar {ruta}: {e}")