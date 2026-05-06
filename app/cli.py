"""Módulo de manejo de argumentos CLI para VulnLab Scanner.

Define todos los argumentos que el usuario puede pasar
por línea de comandos para configurar el escaneo.
"""

import argparse


def parse_args():
    """Parsea los argumentos de línea de comandos.
    
    Returns:
        Objeto con los argumentos parseados.
    """
    parser = argparse.ArgumentParser(
        description='VulnLab Scanner - Herramienta profesional de escaneo OWASP Top 10.'
    )

    # Argumentos principales
    parser.add_argument(
        "-u", "--url",
        required=False,  # No obligatorio si se usa --disclaimer
        help="URL del sitio web a escanear (ejemplo: http://localhost:8080)"
    )

    parser.add_argument(
        "-x", "--xss",
        action="store_true",
        help="Escanear vulnerabilidades de Cross-Site Scripting (XSS)"
    )

    parser.add_argument(
        "-s", "--sqli",
        action="store_true",
        help="Escanear vulnerabilidades de Inyección SQL (SQLi)"
    )

    parser.add_argument(
        "-H", "--headers",
        action="store_true",
        help="Revisar headers de seguridad HTTP"
    )

    parser.add_argument(
        "-A", "--access-control",
        action="store_true",
        help="Escanear Broken Access Control (A01 - OWASP)"
    )

    parser.add_argument(
        "-U", "--auth",
        action="store_true",
        help="Escanear Authentication Failures (A07 - OWASP)"
    )

    parser.add_argument(
        "-C", "--vuln-components",
        action="store_true",
        help="Escanear Vulnerable Components (A06 - OWASP)"
    )

    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Escanear todas las vulnerabilidades disponibles"
    )

    # Opciones de autenticación
    auth_group = parser.add_argument_group('Autenticación')
    
    auth_group.add_argument(
        "--login-url",
        help="URL de la página de login (para sitios que requieren autenticación)"
    )
    
    auth_group.add_argument(
        "--username",
        help="Usuario para autenticación"
    )
    
    auth_group.add_argument(
        "--password",
        help="Contraseña para autenticación"
    )
    
    # Opciones de reporte
    report_group = parser.add_argument_group('Reportes')
    
    report_group.add_argument(
        "--report",
        choices=["json", "html", "ambos"],
        default="ambos",
        help="Formato del reporte (json, html, ambos)"
    )
    
    report_group.add_argument(
        "--output-dir",
        default="reports",
        help="Directorio de salida para reportes (default: reports/)"
    )
    
    report_group.add_argument(
        "--no-report",
        action="store_true",
        help="No generar reportes"
    )
    
    # Otras opciones
    parser.add_argument(
        "--disclaimer",
        action="store_true",
        help="Mostrar aviso legal y salir"
    )
    
    parser.add_argument(
        "--no-disclaimer",
        action="store_true",
        help="Omitir aviso legal (no recomendado)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simular escaneo sin atacar (no envía ataques reales)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Modo verbose (más detalles)"
    )
    
    return parser.parse_args()


def main():
    """Punto de entrada para CLI (usado por entry_points)."""
    args = parse_args()
    
    # Si no se proporciona URL y no es --disclaimer, mostrar ayuda
    if not args.url and not args.disclaimer:
        print("Error: Se requiere una URL (-u/--url) o --disclaimer")
        return
    
    # Importar aquí para evitar circular imports
    from app.main import run_scan
    run_scan(args)


if __name__ == "__main__":
    main()
