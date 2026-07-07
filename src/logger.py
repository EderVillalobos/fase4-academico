from __future__ import annotations

from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "eventos.log"


def _ensure_log_dir() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def registrar_evento(mensaje: str, nivel: str = "INFO") -> None:
    _ensure_log_dir()
    marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea = f"[{marca_tiempo}] {nivel.upper()}: {mensaje}\n"
    with LOG_FILE.open("a", encoding="utf-8") as archivo:
        archivo.write(linea)


def registrar_excepcion(contexto: str, error: Exception) -> None:
    registrar_evento(f"{contexto} -> {type(error).__name__}: {error}", "ERROR")

