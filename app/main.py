from app.cli import parse_args

def main():
    args = parse_args()

    print(f"[+] Objetivo: {args.url}")

    if args.xss:
        print("[*] Escaneo XSS activado")

    if args.sqli:
        print("[*] Escaneo SQLi activado")

    if args.headers:
        print("[*] Escaneo de headers activado")

if __name__ == "__main__":
    main()