from app.cli import parse_args
from app.utils.helpers import is_valid_url

def main():
    args = parse_args()

    if not is_valid_url(args.url):
        print("[ERROR] La URL debe comenzar con http:// o https://")
        return

    if args.all:
        args.xss = True
        args.sqli = True
        args.headers = True

    print(f"[+] Objetivo: {args.url}")

    if args.xss:
        print("[*] Escaneo XSS activado")

    if args.sqli:
        print("[*] Escaneo SQLi activado")

    if args.headers:
        print("[*] Escaneo de headers activado")
        
if __name__ == "__main__":
    main()