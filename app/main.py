"""Punto de entrada principal de VulnLab Scanner.

Coordina la inicialización, autenticación, escaneo y generación
de reportes siguiendo la arquitectura modular.
"""

from app.cli import parse_args
from app.config import Config
from app.core.session import ScannerSession
from app.utils.helpers import is_valid_url
from app.utils.logger import info, success, error, warning
from app.utils.disclaimer import check_legal_requirements
from app.utils.reporter import save_report
from app.scanner.xss import XSSScanner
from app.scanner.sqli import SQLiScanner
from app.scanner.headers import HeadersScanner
from app.scanner.access_control import AccessControlScanner
from app.scanner.auth import AuthScanner
from app.scanner.components import ComponentsScanner
from datetime import datetime
import concurrent.futures


def main():
    """Función principal que orquesta el escaneo."""
    args = parse_args()
    
    # Mostrar disclaimer y salir si se solicita
    if args.disclaimer:
        from app.utils.disclaimer import show_disclaimer
        show_disclaimer()
        return
    
    # Validar URL objetivo
    if not is_valid_url(args.url):
        error("La URL debe comenzar con http:// o https://")
        return
    
    # Verificar requisitos legales
    if not check_legal_requirements(args.accept_disclaimer):
        return
    
    # Mostrar configuración
    info("=" * 60)
    info("VulnLab Scanner - Iniciando escaneo")
    info("=" * 60)
    Config.display()
    
    # Determinar qué escáneres ejecutar
    if args.all:
        args.xss = True
        args.sqli = True
        args.headers = True
        args.access_control = True
        args.auth = True
        args.vuln_components = True
    
    if not (args.xss or args.sqli or args.headers):
        warning("No seleccionaste ningún escaneo. Usa --all o especifica uno.")
        return
    
    # Inicializar sesión
    info(f"[+] Objetivo: {args.url}")
    session = ScannerSession(rate_limit=args.rate_limit)
    
    # Realizar login si se proporcionan credenciales
    if args.login_url and args.username and args.password:
        if not session.login(
            args.login_url, 
            args.username, 
            args.password,
            args.login_username_field,
            args.login_password_field
        ):
            error("Fallo en la autenticación. Continuando sin sesión...")
    
    # Información del escaneo
    scan_info = {
        "target_url": args.url,
        "start_time": datetime.now().isoformat(),
        "scanners_used": [],
        "authenticated": session.is_authenticated
    }
    
    all_results = []
    
    try:
        # Ejecutar escáneres en paralelo si hay más de uno
        scanners_to_run = []
        if args.xss:
            scanners_to_run.append(("XSSScanner", XSSScanner, args.url, session, args.dry_run))
        if args.sqli:
            scanners_to_run.append(("SQLiScanner", SQLiScanner, args.url, session, args.dry_run))
        if args.headers:
            scanners_to_run.append(("HeadersScanner", HeadersScanner, args.url, session, args.dry_run))
        if args.access_control:
            scanners_to_run.append(("AccessControlScanner", AccessControlScanner, args.url, session, args.dry_run))
        if args.auth:
            scanners_to_run.append(("AuthScanner", AuthScanner, args.url, session, args.dry_run))
        if args.vuln_components:
            scanners_to_run.append(("ComponentsScanner", ComponentsScanner, args.url, session, args.dry_run))
        
        if len(scanners_to_run) > 1:
            # Ejecución paralela
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                future_to_scanner = {
                    executor.submit(scanner_class, url, sess, dry): name
                    for name, scanner_class, url, sess, dry in scanners_to_run
                }
                for future in concurrent.futures.as_completed(future_to_scanner):
                    scanner_name = future_to_scanner[future]
                    try:
                        results = future.result().scan()
                        all_results.extend(results)
                        scan_info["scanners_used"].append(scanner_name)
                    except Exception as e:
                        error(f"Error en {scanner_name}: {str(e)}")
        else:
            # Ejecución secuencial (original)
            for name, scanner_class, url, sess, dry in scanners_to_run:
                scanner = scanner_class(url, sess, dry)
                results = scanner.scan()
                all_results.extend(results)
                scan_info["scanners_used"].append(name)
        
        # Actualizar información del escaneo
        scan_info["end_time"] = datetime.now().isoformat()
        
        # Generar reportes
        if not args.dry_run and all_results:
            info("=" * 60)
            info("Generando reportes...")
            info("=" * 60)
            
            saved_files = save_report(
                all_results, 
                scan_info,
                report_format=args.report_format,
                output_dir=args.report_output
            )
            
            for filepath in saved_files:
                success(f"Reporte guardado en: {filepath}")
        elif args.dry_run:
            info("Modo DRY-RUN: No se generan reportes")
        else:
            info("No se encontraron vulnerabilidades para reportar")
        
        # Resumen final
        from app.utils.reporter import generate_summary
        summary = generate_summary(all_results)
        
        info("=" * 60)
        info("RESUMEN DEL ESCANEO")
        info("=" * 60)
        info(f"Total vulnerabilidades: {summary['total_vulnerabilities']}")
        info(f"  - Críticas: {summary['critical']}")
        info(f"  - Altas: {summary['high']}")
        info(f"  - Medias: {summary['medium']}")
        info(f"  - Bajas: {summary['low']}")
        
    finally:
        # Cerrar sesión
        session.close()


if __name__ == "__main__":
    main()
