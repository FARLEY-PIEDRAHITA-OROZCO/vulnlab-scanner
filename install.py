"""Script de instalación automática para VulnLab Scanner.

Este script ayuda a configurar el entorno virtual e instalar
todas las dependencias necesarias.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command: list, description: str) -> bool:
    """Ejecuta un comando y maneja errores.
    
    Args:
        command: Lista con el comando y argumentos.
        description: Descripción del comando para mostrar al usuario.
        
    Returns:
        True si el comando fue exitoso, False en caso contrario.
    """
    print(f"\n[*] {description}...")
    try:
        subprocess.run(command, check=True)
        print(f"[OK] {description} completado.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error al {description.lower()}: {e}")
        return False


def main():
    """Función principal de instalación."""
    print("=" * 60)
    print("VulnLab Scanner - Instalación Automática")
    print("=" * 60)
    
    # Obtener directorio del proyecto
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Verificar Python
    print(f"\n[*] Verificando Python...")
    try:
        subprocess.run([sys.executable, "--version"], check=True)
    except subprocess.CalledProcessError:
        print("[ERROR] Python no está instalado o no está en PATH.")
        sys.exit(1)
    
    # Crear entorno virtual
    venv_path = project_dir / ".venv"
    if not venv_path.exists():
        if not run_command(
            [sys.executable, "-m", "venv", str(venv_path)],
            "Creando entorno virtual"
        ):
            sys.exit(1)
    else:
        print("\n[*] El entorno virtual ya existe.")
    
    # Determinar ejecutable de Python en el entorno virtual
    if os.name == "nt":  # Windows
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:  # Linux/Mac
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
    
    # Actualizar pip
    run_command(
        [str(pip_exe), "install", "--upgrade", "pip"],
        "Actualizando pip"
    )
    
    # Instalar dependencias
    requirements = project_dir / "requirements.txt"
    if requirements.exists():
        if not run_command(
            [str(pip_exe), "install", "-r", str(requirements)],
            "Instalando dependencias"
        ):
            sys.exit(1)
    else:
        print("\n[WARN] No se encontró requirements.txt")
    
    # Instalar dependencias de desarrollo (opcional)
    requirements_dev = project_dir / "requirements-dev.txt"
    if requirements_dev.exists():
        response = input("\n¿Instalar dependencias de desarrollo? (si/no): ").strip().lower()
        if response in ["si", "sí", "yes", "y"]:
            run_command(
                [str(pip_exe), "install", "-r", str(requirements_dev)],
                "Instalando dependencias de desarrollo"
            )
    
    print("\n" + "=" * 60)
    print("Instalación completada exitosamente.")
    print("=" * 60)
    print("\nPara activar el entorno virtual:")
    if os.name == "nt":
        print("  .\\.venv\\Scripts\\activate")
    else:
        print("  source .venv/bin/activate")
    print("\nPara ejecutar el escáner:")
    print("  python -m app.main -u http://ejemplo.com --all")
    print()


if __name__ == "__main__":
    main()
