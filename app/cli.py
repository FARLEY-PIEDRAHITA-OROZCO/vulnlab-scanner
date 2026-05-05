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
    
    auth_group.add_argument(
        "--login-username-field",
        default="username",
        help="Nombre del campo de usuario en el formulario (default: username)"
    )
    
    auth_group.add_argument(
        "--login-password-field",
        default="password",
        help="Nombre del campo de contraseña en el formulario (default: password)"
    )

    # Opciones de reporte
    report_group = parser.add_argument_group('Reportes')
    
    report_group.add_argument(
        "--report-format",
        choices=["json", "html", "ambos"],
        default="ambos",
        help="Formato del reporte (default: ambos)"
    )
    
    report_group.add_argument(
        "--report-output",
        default="./reports",
        help="Directorio de salida para reportes (default: ./reports)"
    )

    # Opciones adicionales
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo simular escaneo sin enviar ataques reales"
    )
    
    parser.add_argument(
        "--rate-limit",
        type=float,
        help="Segundos entre peticiones (default: 0.5)"
    )
    
    parser.add_argument(
        "--disclaimer",
        action="store_true",
        help="Mostrar aviso legal y salir"
    )
    
    parser.add_argument(
        "--accept-disclaimer",
        action="store_true",
        help="Aceptar aviso legal (para entornos no interactivos)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Modo verbose (más detalles)"
    )

    args = parser.parse_args()
    
    # Validar que se proporcione URL a menos que sea --disclaimer
    if not args.disclaimer and not args.url:
        parser.error("the following arguments are required: -u/--url (or use --disclaimer)")
    
    return args
