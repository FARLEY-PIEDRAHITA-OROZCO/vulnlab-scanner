"""Utilidades de logging para VulnLab Scanner.

Provee funciones para mostrar mensajes coloreados
en la consola usando colorama (compatible con Windows).
"""

from colorama import Fore, Style, init

# Inicializar colorama (auto-reset)
init(autoreset=True)


def info(message: str):
    """Muestra un mensaje informativo (cyan)."""
    print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")


def success(message: str):
    """Muestra un mensaje de éxito (verde)."""
    print(f"{Fore.GREEN}[OK] {message}{Style.RESET_ALL}")


def warning(message: str):
    """Muestra un mensaje de advertencia (amarillo)."""
    print(f"{Fore.YELLOW}[WARN] {message}{Style.RESET_ALL}")


def error(message: str):
    """Muestra un mensaje de error (rojo)."""
    print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")


def vulnerability(message: str):
    """Muestra una vulnerabilidad detectada (magenta)."""
    print(f"{Fore.MAGENTA}[VULN] {message}{Style.RESET_ALL}")
