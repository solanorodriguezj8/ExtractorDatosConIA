"""
Este archivo, recibe el json y lo comprueba, ya que si llega a estar el json mal, no queremos que se rompa el programa
"""
import json

def comprobar_respuesta(respuesta,ruta):
    try:
        #Limpiamos el string para evitar fallos
        respuesta_limpia=respuesta.strip().strip("`")
        return json.loads(respuesta_limpia)
    except json.JSONDecodeError:
        """Mejora: archivo con ruta de los pdf mal"""
        print(f"Archivo mal procesado: {ruta}")
        return {
            "nombre_provedor":None,
            "numero_factura":None,
            "base_imponible":None,
            "importe_IVA":None,
            "termino_de_pago":None,
            "fecha_vencimiento":None
        }