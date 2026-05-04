import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='VulnLab Scanner - Escáner educativo de vulnerabilidades OWASP Top 10.'
    )

    parser.add_argument(
        "-u", "--url",
        required=True,
        help="URL del sitio web vulnerable a escanear (ejemplo: http://localhost:8080)"
    )

    parser.add_argument(
        "--xss",
        action="store_true",
        help="Escanear vulberabilidades de Cross-Site Scripting (XSS)"
    )

    parser.add_argument(
        "--sqli",
        action="store_true",
        help="Escanear vulnerabilidades de Inyección SQL (SQLi)"
    )

    parser.add_argument(
        "--headers",
        action="store_true",
        help="Revisar headers de seguridad"
    )

    return parser.parse_args()