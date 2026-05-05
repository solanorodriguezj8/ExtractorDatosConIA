"""
Este archivo coge el texto del pdf, y crea un prompt(conversacion) con la ia para que saque los datos necesarios en un JSON
"""
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss-safeguard"

def extraer_datos_con_ia(texto):
    prompt=f"""
    Eres un sistema de extracción de datos de facturas OCR.

    Devuelve SOLO JSON válido.
    SOLO UN JSON VÁLIDO.
    QUIERO EL JSON PURO, NADA DE COMENTARIOS.
    Usa null si no existe el dato.

    Campos a extraer:
    - nombre_provedor
    - numero_factura
    - base_imponible
    - importe_IVA
    - termino_de_pago
    - fecha_factura

    Reglas IMPORTANTES:
    1. Fecha factura 
    - Se tiene que poner de esta manera "dd-mm-AAAA".
    - Es la fecha de expedición.
    - Solo puede haber una.
    - No puede ser mas tarde que la fecha actual.

    2. termino_de_pago es un número de días.
    Ejemplos válidos:
    - "pago a 30 dias" → 30
    - "Giro a 60 dias" → 60
    Si no hay plazo → null.
    - Puede haber varios giros, se escriben todos los que se detecten.

    3. base_imponible:
    - No puede ser nunca null.
    - Buscar "Base imponible", "B. imponible", "B. IMPONIBLE".
    - Tiene que ser un numero sin nada mas, nada de "kg" ni de "m" ni nada.
    - Si no aparece:
        base_imponible = total_factura - importe_IVA.

    4. importe_IVA:
    - NO es el porcentaje (21% o "21" o "21.00").
    - Buscar el IMPORTE del IVA.
    - Puedes estar puesto como "x.x" o "x,x".
    - No puede ser nunca null.
    - Si no aparece:
        importe_IVA = total_factura - base_imponible.

    Texto:
    <<<
    {texto}
    >>>
    """

    response=requests.post(
        OLLAMA_URL,
        json={
            "model":MODELO,
            "prompt":prompt,
            "stream":False,
            "keep_alive":0
        }
    )
    return response.json()["response"]