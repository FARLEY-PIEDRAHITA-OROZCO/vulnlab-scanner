from colorama import Fore, Style, init

init(autoreset=True)

def info(message):
    print(Fore.CYAN + "[INFO] " + message)

def success(message):
    print(Fore.GREEN + "[OK] " + message)

def warning(message):
    print(Fore.YELLOW + "[WARN] " + message)

def error(message):
    print(Fore.RED + "[ERROR] " + message)

def vulnerability(message):
    print(Fore.MAGENTA + "[VULN] " + message)
