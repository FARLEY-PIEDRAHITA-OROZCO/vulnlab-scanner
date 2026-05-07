"""Punto de entrada principal de VulnLab Scanner.

Coordina la inicialización, autenticación, escaneo y generación
de reportes siguiendo la arquitectura modular.
"""

import concurrent.futures
from datetime import datetime

from app.cli import parse_args
from app.core.session import ScannerSession
from app.scanner.access_control import AccessControlScanner
from app.scanner.auth import AuthScanner
from app.scanner.components import ComponentsScanner
from app.scanner.crypto import CryptoScanner
from app.scanner.headers import HeadersScanner
from app.scanner.insecure_design import InsecureDesignScanner
from app.scanner.security_logging import SecurityLoggingScanner
from app.scanner.sqli import SQLiScanner
from app.scanner.ssrf import SSRFScanner
from app.scanner.xss import XSSScanner
from app.utils.disclaimer import check_legal_requirements
from app.utils.helpers import is_valid_url
from app.utils.logger import error, info, success, warning
from app.utils.reporter import save_report


def _add_scanner_if_enabled(args, attr, scanner_tuple, scanners_to_run):
    """Añade un escáner a la lista si está habilitado en args."""
    if getattr(args, attr, False):
        scanners_to_run.append(scanner_tuple)


def _prepare_scanners(args, session):
    """Prepara la lista de escáneres a ejecutar.

    Args:
        args: Argumentos de línea de comandos.
        session: Sesión HTTP.

    Returns:
        Lista de tuplas (nombre, clase, url, sesión, dry_run).
    """
    scanners_to_run = []
    _add_scanner_if_enabled(args, "xss", ("XSSScanner", XSSScanner, args.url, session, args.dry_run), scanners_to_run)
    _add_scanner_if_enabled(args, "sqli", ("SQLiScanner", SQLiScanner, args.url, session, args.dry_run), scanners_to_run)
    _add_scanner_if_enabled(
        args, "headers", ("HeadersScanner", HeadersScanner, args.url, session, args.dry_run), scanners_to_run
    )
    _add_scanner_if_enabled(
        args,
        "access_control",
        ("AccessControlScanner", AccessControlScanner, args.url, session, args.dry_run),
        scanners_to_run,
    )
    _add_scanner_if_enabled(args, "auth", ("AuthScanner", AuthScanner, args.url, session, args.dry_run), scanners_to_run)
    _add_scanner_if_enabled(
        args, "vuln_components", ("ComponentsScanner", ComponentsScanner, args.url, session, args.dry_run), scanners_to_run
    )
    _add_scanner_if_enabled(args, "crypto", ("CryptoScanner", CryptoScanner, args.url, session, args.dry_run), scanners_to_run)
    _add_scanner_if_enabled(args, "ssrf", ("SSRFScanner", SSRFScanner, args.url, session, args.dry_run), scanners_to_run)
    _add_scanner_if_enabled(
        args,
        "insecure_design",
        ("InsecureDesignScanner", InsecureDesignScanner, args.url, session, args.dry_run),
        scanners_to_run,
    )
    _add_scanner_if_enabled(
        args,
        "security_logging",
        ("SecurityLoggingScanner", SecurityLoggingScanner, args.url, session, args.dry_run),
        scanners_to_run,
    )
    return scanners_to_run


def _run_parallel(scanners_to_run, all_results, scan_info):
    """Ejecuta escáneres en paralelo.

    Args:
        scanners_to_run: Lista de escáneres a ejecutar.
        all_results: Lista para acumular resultados.
        scan_info: Información del escaneo.
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_scanner = {
            executor.submit(scanner_class, url, sess, dry): name for name, scanner_class, url, sess, dry in scanners_to_run
        }
        for future in concurrent.futures.as_completed(future_to_scanner):
            scanner_name = future_to_scanner[future]
            try:
                results = future.result().scan()
                all_results.extend(results)
                scan_info["scanners_used"].append(scanner_name)
            except Exception as e:
                error(f"Error en {scanner_name}: {str(e)}")


def _run_sequential(scanners_to_run, all_results, scan_info):
    """Ejecuta escáneres secuencialmente.

    Args:
        scanners_to_run: Lista de escáneres a ejecutar.
        all_results: Lista para acumular resultados.
        scan_info: Información del escaneo.
    """
    for name, scanner_class, url, sess, dry in scanners_to_run:
        scanner = scanner_class(url, sess, dry)
        results = scanner.scan()
        all_results.extend(results)
        scan_info["scanners_used"].append(name)


def run_scan(args):
    """Ejecuta el escaneo basado en los argumentos parseados.

    Args:
        args: Objeto con argumentos de línea de comandos.
    """
    info("=" * 60)
    info("VulnLab Scanner - Iniciando escaneo")
    info("=" * 60)

    # Validar URL
    if not args.disclaimer and not is_valid_url(args.url):
        error(f"URL inválida: {args.url}")
        return

    # Mostrar aviso legal si no se omitió
    if not args.no_disclaimer:
        if not check_legal_requirements(args.url):
            return

    # Determinar qué escáneres ejecutar
    if args.all:
        args.xss = True
        args.sqli = True
        args.headers = True
        args.access_control = True
        args.auth = True
        args.vuln_components = True
        args.crypto = True
        args.ssrf = True
        args.insecure_design = True
        args.security_logging = True

    # Crear sesión
    session = ScannerSession()

    # Si se proporcionan credenciales, intentar login
    if args.login_url and args.username and args.password:
        info(f"Intentando login en: {args.login_url}")
        if session.login(args.login_url, args.username, args.password):
            success("Login exitoso!")
        else:
            warning("Login falló. Continuando sin autenticación.")

    # Información del escaneo
    scan_info = {"target_url": args.url, "start_time": datetime.now().isoformat(), "scanners_used": []}

    all_results = []

    # Ejecutar escáneres en paralelo si hay más de uno
    scanners_to_run = _prepare_scanners(args, session)

    if len(scanners_to_run) > 1:
        _run_parallel(scanners_to_run, all_results, scan_info)
    else:
        _run_sequential(scanners_to_run, all_results, scan_info)

    # Actualizar información del escaneo
    scan_info["end_time"] = datetime.now().isoformat()

    # Generar reportes
    if not args.dry_run and not args.no_report:
        info("=" * 60)
        info("Generando reportes...")
        info("=" * 60)

        saved_files = save_report(all_results, scan_info, report_format=args.report, output_dir=args.output_dir)

        for filepath in saved_files:
            success(f"Reporte guardado en: {filepath}")

    # Mostrar resumen
    success("=" * 60)
    success(f"Escaneo completado. Vulnerabilidades encontradas: {len(all_results)}")
    success("=" * 60)


def main():
    """Punto de entrada principal (para ejecución directa)."""
    args = parse_args()

    # Si no se proporciona URL y no es --disclaimer, mostrar ayuda
    if not args.url and not args.disclaimer:
        print("Error: Se requiere una URL (-u/--url) o --disclaimer")
        return

    run_scan(args)


if __name__ == "__main__":
    main()
