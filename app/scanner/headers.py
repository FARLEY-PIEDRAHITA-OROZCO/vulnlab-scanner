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

    result = {
        "target": url,
        "scanner": "headers",
        "results": {
            "secure": [],
            "missing": [],
            "misconfigured": []
        }
    }

    try:
        response = requests.get(
            url,
            headers={"User-Agent": Config.USER_AGENT},
            timeout=Config.TIMEOUT
        )
    except requests.RequestException as e:
        error(f"Error al realizar la solicitud: {e}")
        return result
    
    headers = response.headers

    for header, expected_values in SECURITY_HEADERS.items():
        
        if header not in headers:
            result["results"]["missing"].append({
                "header": header,
                "message": "Header no presente"
            })
        else:
            value = headers[header]

            if expected_values:
                if value.upper() in expected_values:
                    result["results"]["secure"].append({
                        "header": header,
                        "value": value
                    })
                else:
                    result["results"]["misconfigured"].append({
                        "header": header,
                        "value": value,
                        "message": "Valor inseguro"
                    })
            else:
                result["results"]["secure"].append({
                    "header": header,
                    "value": value
                })
                
    return result