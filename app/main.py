from app.cli import parse_args
from app.utils.helpers import is_valid_url
from app.utils.logger import info, success, error

def main():
    args = parse_args()

    if not is_valid_url(args.url):
        error("La URL debe comenzar con http:// o https://")
        return

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
        success("[*] Escaneo de headers activado")
        
if __name__ == "__main__":
    main()