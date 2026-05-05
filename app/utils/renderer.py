from app.utils.logger import success, warning, error, info

def render_headers(result):
    if "error" in result:
        error(result["error"])
        return

    info(f"Resultados para {result['target']}")

    for item in result["results"]["secure"]:
        success(f"{item['header']} OK ({item['value']})")

    for item in result["results"]["missing"]:
        warning(f"{item['header']} faltante")

    for item in result["results"]["misconfigured"]:
        warning(f"{item['header']} mal configurado ({item['value']})")