#!/usr/bin/env python3
"""
Script para ejecutar todos los tests automáticamente.
"""
import subprocess
import sys

def run_tests():
    """Ejecuta pytest y muestra los resultados."""
    print("🧪 Ejecutando tests del Ciclopuerto 2V...")
    print("=" * 50)
    
    # Ejecutar pytest
    result = subprocess.run(
        ["pytest", "-v", "--tb=short"],
        capture_output=True,
        text=True
    )
    
    # Mostrar resultados
    print(result.stdout)
    
    if result.stderr:
        print("⚠️  Errores:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    
    # Mostrar resumen
    print("=" * 50)
    if result.returncode == 0:
        print("✅ ¡Todos los tests pasaron!")
    else:
        print("❌ Algunos tests fallaron")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())