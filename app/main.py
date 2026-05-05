from app.cli import parse_args
from app.utils.helpers import is_valid_url
from app.utils.logger import info, success, error, warning
from app.scanner.headers import check_headers
from app.scanner.headers import check_headers
from app.utils.renderer import render_headers
from app.utils.reporter import save_report
from app.utils.logger import success

def main():
    args = parse_args()

    if not is_valid_url(args.url):
        error("La URL debe comenzar con http:// o https://")
        return
    
    if not (args.xss or args.sqli or args.headers):
        warning("No seleccionaste ningún escaneo. Usa --all o especifica uno.")

    if args.all:
        args.xss = True
        args.sqli = True
        args.headers = True

    info(f"[+] Objetivo: {args.url}")

    if args.xss:
        success("[*] Escaneo XSS activado")

    if args.sqli:
        success("[*] Escaneo SQLi activado")

    if args.headers:
        result = check_headers(args.url)
        render_headers(result)
        path = save_report(result)
        success(f"Reporte guardado en: {path}")
        
if __name__ == "__main__":
    main()