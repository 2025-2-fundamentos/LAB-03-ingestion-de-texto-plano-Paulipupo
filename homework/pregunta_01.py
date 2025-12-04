"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import re

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    
    ruta = "files/input/clusters_report.txt"

    with open(ruta, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    start_idx = 0
    for i, line in enumerate(lines):
        if line.startswith("-"):
            start_idx = i + 1
            break

    data_lines = lines[start_idx:]

    registros = []
    actual = None

    for line in data_lines:
        line = line.rstrip("\n")

        if not line.strip():
            continue

        m = re.match(r"\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)", line)
        if m:
            if actual is not None:
                registros.append(actual)

            cluster = int(m.group(1))
            cantidad = int(m.group(2))
            porcentaje = float(m.group(3).replace(",", "."))
            palabras = m.group(4).strip()

            actual = {
                "cluster": cluster,
                "cantidad_de_palabras_clave": cantidad,
                "porcentaje_de_palabras_clave": porcentaje,
                "principales_palabras_clave": palabras,
            }
        else:
            texto = line.strip()
            if actual is not None:
                actual["principales_palabras_clave"] += " " + texto

    if actual is not None:
        registros.append(actual)

    df = pd.DataFrame(registros)
    def limpiar_palabras(s: str) -> str:
        s = s.replace(".", "")
        s = re.sub(r"\s+", " ", s.strip())
        s = re.sub(r"\s*,\s*", ", ", s)
        return s

    df["principales_palabras_clave"] = df["principales_palabras_clave"].apply(
        limpiar_palabras
    )

    return df
