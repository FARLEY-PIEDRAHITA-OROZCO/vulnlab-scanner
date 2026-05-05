"""Módulo para detección de Vulnerable Components (A06 - OWASP Top 10).

Este módulo implementa detección básica de:
- Versiones desactualizadas de JavaScript (jQuery, Angular, etc.)
- Versiones desactualizadas de CDNs (Bootstrap, React, etc.)
- Headers de tecnologías (X-Powered-By, Server)
"""

from app.scanner.base import BaseScanner
from app.utils.payloads import COMPONENTS_PAYLOADS
from app.utils.logger import info, warning, success
from urllib.parse import urlparse
import re


class ComponentsScanner(BaseScanner):
    """Escáner de Vulnerable Components (SCA básico).
    
    Detecta tecnologías desactualizadas que puedan
    contener vulnerabilidades conocidas.
    """
    
    def __init__(self, target_url: str, session, dry_run: bool = False):
        """Inicializa el escáner de Components.
        
        Args:
            target_url: URL de la aplicación a escanear.
            session: Sesión HTTP para realizar peticiones.
            dry_run: Si es True, solo simula sin atacar.
        """
        super().__init__(target_url, session, dry_run)
        self.payloads = self.get_payloads()
        self.technologies_found = []
    
    def get_payloads(self) -> list:
        """Retorna la lista de payloads para Components.
        
        Returns:
            Lista de payloads de tipo components.
        """
        return COMPONENTS_PAYLOADS
    
    def _extract_scripts(self, html_content: str) -> list:
        """Extrae URLs de scripts JS del HTML.
        
        Args:
            html_content: Contenido HTML de la página.
            
        Returns:
            Lista de URLs de scripts encontrados.
        """
        # Buscar src de script tags
        pattern = r'<script[^>]*src=["\']([^"\']+)["\'][^>]*>'
        matches = re.findall(pattern, html_content, re.IGNORECASE)
        return matches
    
    def _extract_cdns(self, html_content: str) -> list:
        """Extrae referencias a CDNs.
        
        Args:
            html_content: Contenido HTML de la página.
            
        Returns:
            Lista de tuplas (cdn_name, url, version_aprox).
        """
        cdn_patterns = [
            (r'jquery[/-](\d+\.\d+(\.\d+)?)', 'jQuery'),
            (r'bootstrap[/-](\d+\.\d+(\.\d+)?)', 'Bootstrap'),
            (r'react[/-](\d+\.\d+(\.\d+)?)', 'React'),
            (r'angular[/-](\d+\.\d+(\.\d+)?)', 'Angular'),
            (r'vue[/-](\d+\.\d+(\.\d+)?)', 'Vue.js'),
        ]
        
        found = []
        for pattern, name in cdn_patterns:
            matches = re.findall(pattern, html_content, re.IGNORECASE)
            if matches:
                version = matches[0][0] if matches else "unknown"
                found.append((name, version))
        
        return found
    
    def _check_technology_headers(self, headers: dict) -> list:
        """Verifica headers que revelan tecnologías.
        
        Args:
            headers: Headers de la respuesta HTTP.
            
        Returns:
            Lista de tecnologías detectadas por headers.
        """
        tech_headers = {
            'X-Powered-By': 'ASP.NET/PHP/Express',
            'Server': 'Web Server',
            'X-AspNet-Version': 'ASP.NET Version',
        }
        
        found = []
        for header, tech in tech_headers.items():
            if header in headers:
                found.append((tech, headers[header]))
        
        return found
    
    def _check_version_vulnerable(self, tech_name: str, version: str) -> bool:
        """Verifica si una versión es conocida como vulnerable.
        
        Args:
            tech_name: Nombre de la tecnología.
            version: Versión detectada.
            
        Returns:
            True si es vulnerable, False en caso contrario.
        """
        # Versiones vulnerables (ejemplos básicos)
        vulnerable_versions = {
            'jQuery': ['1.0', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8', '1.9', '1.10', '1.11', '1.12'],
            'Bootstrap': ['2.0', '2.1', '2.2', '2.3', '3.0', '3.1', '3.2', '3.3'],
        }
        
        if tech_name in vulnerable_versions:
            for vuln_ver in vulnerable_versions[tech_name]:
                if version.startswith(vuln_ver):
                    return True
        return False
    
    def scan(self) -> list:
        """Ejecuta el escaneo de Vulnerable Components.
        
        Returns:
            Lista de diccionarios con resultados del escaneo.
        """
        self.display_scan_start()
        self.clear_results()
        
        info("Iniciando detección de Vulnerable Components (A06)")
        
        if self.dry_run:
            info("[DRY-RUN] Solo simularía detección de componentes")
            return self.get_results()
        
        try:
            # Obtener página principal
            info(f"Analizando: {self.target_url}")
            response = self.session.get(self.target_url)
            html_content = response.text
            headers = response.headers
            
            # 1. Verificar headers de tecnologías
            info("Paso 1: Verificando headers de tecnologías...")
            tech_headers = self._check_technology_headers(headers)
            
            for tech, version in tech_headers:
                self.add_result(
                    vuln_name="Technology Disclosure via Headers",
                    severity="LOW",
                    description=f"Header revela tecnología: {tech}",
                    evidence=f"Header: {tech} = {version}"
                )
            
            # 2. Extraer y analizar scripts
            info("Paso 2: Analizando scripts JS...")
            scripts = self._extract_scripts(html_content)
            info(f"Encontrados {len(scripts)} scripts")
            
            # 3. Buscar CDNs y versiones
            info("Paso 3: Verificando CDNs y versiones...")
            cdns = self._extract_cdns(html_content)
            
            for cdn_name, version in cdns:
                severity = "MEDIUM" if self._check_version_vulnerable(cdn_name, version) else "LOW"
                self.add_result(
                    vuln_name="Outdated Component Detected",
                    severity=severity,
                    description=f"Componente desactualizado: {cdn_name}",
                    evidence=f"Versión detectada: {version}"
                )
            
            # 4. Buscar firmas en el HTML
            info("Paso 4: Buscando firmas en HTML...")
            for payload in self.payloads:
                if payload["type"] == "outdated_js":
                    if payload["name"].lower() in html_content.lower():
                        self.add_result(
                            vuln_name="Potentially Vulnerable JS Library",
                            severity="MEDIUM",
                            description=f"Biblioteca JS detectada: {payload['name']}",
                            evidence=f"Biblioteca: {payload['name']} (posiblemente desactualizada)"
                        )
            
        except Exception as e:
            warning(f"Error al escanear componentes: {str(e)}")
        
        success(f"Escaneo A06 completado. Vulnerabilidades encontradas: {len(self.results)}")
        return self.get_results()
