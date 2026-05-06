"""Generación de reportes para VulnLab Scanner.

Soporta guardar resultados en formato JSON y HTML
con toda la información del escaneo.
"""

import os
import json
from datetime import datetime
from urllib.parse import urlparse

from app.config import Config


def generate_summary(results: list) -> dict:
    """Genera un resumen estadístico de los resultados.
    
    Args:
        results: Lista de resultados del escaneo.
        
    Returns:
        Diccionario con el resumen.
    """
    summary = {
        "total_vulnerabilities": len(results),
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }
    
    for result in results:
        severity = result.get("severity", "").upper()
        if severity == "CRITICAL":
            summary["critical"] += 1
        elif severity == "HIGH":
            summary["high"] += 1
        elif severity == "MEDIUM":
            summary["medium"] += 1
        elif severity == "LOW":
            summary["low"] += 1
    
    return summary


def save_json_report(data: dict, output_dir: str = None) -> str:
    """Guarda el reporte en formato JSON.
    
    Args:
        data: Diccionario con los datos del reporte.
        output_dir: Directorio de salida (usa Config.REPORTS_DIR por defecto).
        
    Returns:
        Ruta del archivo guardado.
    """
    if output_dir is None:
        output_dir = Config.REPORTS_DIR
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = data.get("scan_info", {}).get("target_url", "unknown")
    domain = urlparse(target).netloc or "unknown"
    
    filename = f"{domain}_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return filepath


def save_html_report(data: dict, output_dir: str = None) -> str:
    """Guarda el reporte en formato HTML básico.
    
    Args:
        data: Diccionario con los datos del reporte.
        output_dir: Directorio de salida (usa Config.REPORTS_DIR por defecto).
        
    Returns:
        Ruta del archivo guardado.
    """
    if output_dir is None:
        output_dir = Config.REPORTS_DIR
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = data.get("scan_info", {}).get("target_url", "unknown")
    domain = urlparse(target).netloc or "unknown"
    
    filename = f"{domain}_{timestamp}.html"
    filepath = os.path.join(output_dir, filename)
    
    # HTML básico (se puede mejorar con plantillas Jinja2)
    html_content = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VulnLab Scanner - Reporte</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
        .vuln {{ border: 1px solid #ddd; padding: 10px; margin: 10px 0; }}
        .CRITICAL {{ border-left: 5px solid #d32f2f; }}
        .HIGH {{ border-left: 5px solid #f57c00; }}
        .MEDIUM {{ border-left: 5px solid #fbc02d; }}
        .LOW {{ border-left: 5px solid #689f38; }}
        .severity {{ font-weight: bold; }}
    </style>
</head>
<body>
    <h1>VulnLab Scanner - Reporte de Seguridad</h1>
    <div class="summary">
        <h2>Resumen</h2>
        <p><strong>Objetivo:</strong> {target}</p>
        <p><strong>Fecha:</strong> {timestamp}</p>
        <p><strong>Total Vulnerabilidades:</strong> {data.get('summary', {}).get('total_vulnerabilities', 0)}</p>
        <ul>
            <li>Críticas: {data.get('summary', {}).get('critical', 0)}</li>
            <li>Altas: {data.get('summary', {}).get('high', 0)}</li>
            <li>Medias: {data.get('summary', {}).get('medium', 0)}</li>
            <li>Bajas: {data.get('summary', {}).get('low', 0)}</li>
        </ul>
    </div>
    
    <h2>Detalles de Vulnerabilidades</h2>
"""
    
    for result in data.get("results", []):
        html_content += f"""
    <div class="vuln {result.get('severity', 'LOW')}">
        <h3>{result.get('vulnerability', 'Desconocido')}</h3>
        <p><span class="severity">Severidad: {result.get('severity', 'N/A')}</span></p>
        <p><strong>URL:</strong> {result.get('url', 'N/A')}</p>
        <p><strong>Descripción:</strong> {result.get('description', 'N/A')}</p>
        <p><strong>Evidencia:</strong> <code>{result.get('evidence', 'N/A')}</code></p>
        <p><strong>Scanner:</strong> {result.get('scanner', 'N/A')}</p>
    </div>
"""
    
    html_content += """
</body>
</html>
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return filepath


def save_report(results: list, scan_info: dict, 
                report_format: str = "ambos", output_dir: str = "reports") -> list:
    """Guarda el reporte en los formatos especificados.
    
    Args:
        results: Lista de resultados del escaneo.
        scan_info: Información del escaneo (target, tiempo, etc.).
        report_format: Formato del reporte (json, html, ambos).
        output_dir: Directorio de salida.
        
    Returns:
        Lista de rutas de archivos generados.
    """
    data = {
        "scan_info": scan_info,
        "results": results,
        "summary": generate_summary(results)
    }
    
    saved_files = []
    
    if report_format in ["json", "ambos"]:
        json_path = save_json_report(data, output_dir)
        saved_files.append(json_path)
    
    if report_format in ["html", "ambos"]:
        html_path = save_html_report(data, output_dir)
        saved_files.append(html_path)
    
    return saved_files
