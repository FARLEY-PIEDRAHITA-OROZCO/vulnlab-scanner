import os
import json
from datetime import datetime

def save_report(data, folder="reports"):
    # Crear carpeta si no existe
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Nombre único basado en fecha
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.json"

    filepath = os.path.join(folder, filename)

    # Guardar archivo
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return filepath