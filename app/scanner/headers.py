import requests
from app.utils.config import Config
from app.utils.logger import info, warning, success, error

SECURITY_HEADERS = {
    "x-Frame-options": ["DENY", "SAMEORIGIN"],
    "X-Content-Type-Options": ["nosniff"],
    "Strict-Transport-Security": None,
    "Content-Security-Policy": None,
    "Referrer-Policy": None
}

def check_headers(url):
    info("Analizando los encabezados de seguridad.")

    try:
        response = requests.get(
            url,
            headers={"User-Agent": Config.USER_AGENT},
            timeout=Config.TIMEOUT
        )
    except requests.RequestException as e:
        error(f"Error al realizar la solicitud: {e}")
        return
    
    headers = response.headers

    for header, expected_values in SECURITY_HEADERS.items():
        if header not in headers:
            warning(f"El encabezado '{header}' no está presente.")
        else:
            value = headers[header]

            if expected_values:
                if value.upper() in expected_values:
                    success(f"{header} correctamente configurado ({value})")
                else:
                    warning(f"{header} valor inseguro: {value}")
            else:
                success(f"{header} presente")