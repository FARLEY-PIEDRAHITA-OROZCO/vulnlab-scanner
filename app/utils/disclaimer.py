"""Módulo de aviso legal y validación de permisos para VulnLab Scanner.

Muestra el descargo de responsabilidad y solicita confirmación
antes de realizar cualquier escaneo.
"""

import sys
from app.utils.logger import warning, error, info
from app.config import Config


DISCLAIMER_TEXT = """
================================================================================
                         AVISO LEGAL - VULNLAB SCANNER
================================================================================

Este escáner está diseñado exclusivamente para propósitos de seguridad ética.
AL UTILIZAR ESTA HERRAMIENTA, USTED DECLARA QUE:

1. Solo escaneará sistemas para los cuales tiene autorización explícita.
2. No utilizará esta herramienta para actividades ilegales o malintencionadas.
3. Es responsable del uso que le dé a los resultados del escaneo.
4. El autor de esta herramienta no se hace responsable por mal uso.

PENALIZACIONES: El escaneo no autorizado de sistemas puede violar leyes
locales, nacionales e internacionales, acarreando sanciones penales.

================================================================================
"""

def show_disclaimer():
    """Muestra el aviso legal completo."""
    print(DISCLAIMER_TEXT)

def request_confirmation() -> bool:
    """Solicita confirmación explícita de permisos al usuario.
    
    Returns:
        True si el usuario confirma, False si cancela.
    """
    # Verificar si estamos en un entorno interactivo
    if not sys.stdin.isatty():
        error("No se puede obtener confirmación en un entorno no interactivo.")
        error("Por favor ejecuta la herramienta en una terminal interactiva.")
        return False
    
    warning("Antes de continuar, debes confirmar que tienes permisos para escanear.")
    print()
    
    try:
        while True:
            response = input("¿Tienes autorización explícita para escanear este objetivo? (si/no): ").strip().lower()
            
            if response in ["si", "sí", "yes", "y"]:
                info("Confirmación recibida. Iniciando escaneo...")
                return True
            elif response in ["no", "n"]:
                error("Escaneo cancelado por el usuario.")
                return False
            else:
                warning("Por favor responde 'si' o 'no'")
    except EOFError:
        error("Error al leer entrada. Asegúrate de ejecutar en terminal interactiva.")
        return False

def check_legal_requirements(accept_flag: bool = False) -> bool:
    """Verifica todos los requisitos legales antes del escaneo.
    
    Args:
        accept_flag: Si es True, asume que el usuario aceptó vía línea de comandos.
        
    Returns:
        True si se cumplen los requisitos, False en caso contrario.
    """
    show_disclaimer()
    
    # Si el usuario pasó --accept-disclaimer
    if accept_flag:
        info("Aviso legal aceptado vía línea de comandos.")
        return True
    
    return request_confirmation()
