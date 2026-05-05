"""Clase base abstracta para todos los escáneres de vulnerabilidades.

Define la interfaz común que deben implementar todos los módulos
de escaneo en VulnLab Scanner.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from app.config import Config
from app.utils.logger import info, vulnerability

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False


class BaseScanner(ABC):
    """Clase base abstracta para todos los escáneres de vulnerabilidades.
    
    Attributes:
        name (str): Nombre del escáner.
        target_url (str): URL objetivo a escanear.
        session (ScannerSession): Sesión HTTP activa.
        results (list): Lista de resultados del escaneo.
        dry_run (bool): Si es True, solo simula sin enviar ataques.
    """
    
    def __init__(self, target_url: str, session, dry_run: bool = False):
        """Inicializa el escáner con la URL objetivo y sesión.
        
        Args:
            target_url: URL de la aplicación a escanear.
            session: Objeto de sesión para realizar peticiones.
            dry_run: Modo de solo simulación.
        """
        self.name = self.__class__.__name__
        self.target_url = target_url
        self.session = session
        self.results = []
        self.dry_run = dry_run
        self.use_progress = TQDM_AVAILABLE and not dry_run
    
    @abstractmethod
    def scan(self) -> list:
        """Ejecuta el escaneo de vulnerabilidades.
        
        Returns:
            Lista de diccionarios con resultados del escaneo.
        """
        pass
    
    @abstractmethod
    def get_payloads(self) -> list:
        """Retorna la lista de payloads para este escáner.
        
        Returns:
            Lista de payloads de ataque.
        """
        pass
    
    def add_result(self, vuln_name: str, severity: str, 
                   description: str, evidence: str = ""):
        """Agrega un resultado al listado de vulnerabilidades encontradas.
        
        Args:
            vuln_name: Nombre de la vulnerabilidad.
            severity: Nivel de severidad (CRITICAL, HIGH, MEDIUM, LOW).
            description: Descripción detallada.
            evidence: Evidencia encontrada (opcional).
        """
        result = {
            "scanner": self.name,
            "vulnerability": vuln_name,
            "severity": severity,
            "url": self.target_url,
            "description": description,
            "evidence": evidence,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        
        if not self.dry_run:
            vulnerability(f"[{severity}] {vuln_name} detectado en {self.target_url}")
    
    def get_results(self) -> list:
        """Retorna todos los resultados del escaneo.
        
        Returns:
            Lista de resultados.
        """
        return self.results
    
    def clear_results(self):
        """Limpia los resultados anteriores."""
        self.results = []
    
    def display_scan_start(self):
        """Muestra mensaje de inicio de escaneo."""
        info(f"[{self.name}] Iniciando escaneo en: {self.target_url}")
        if self.dry_run:
            info("Modo DRY-RUN: No se enviarán ataques reales")
        if self.use_progress:
            info("Barras de progreso habilitadas")
    
    def progress_iter(self, items, desc="Procesando"):
        """Retorna un iterador con barra de progreso si está disponible.
        
        Args:
            items: Lista de elementos a iterar.
            desc: Descripción de la barra.
            
        Returns:
            Iterador (tqdm o normal).
        """
        if self.use_progress:
            return tqdm(items, desc=f"[{self.name}] {desc}", unit="item")
        return items
