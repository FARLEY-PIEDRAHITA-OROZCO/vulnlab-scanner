def is_valid_url(url: str) -> bool:
    """Verifica si una URL es válida (debe empezar con http:// o https://)."""
    if not url or not isinstance(url, str):
        return False
    return url.startswith("http://") or url.startswith("https://")