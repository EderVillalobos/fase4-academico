from __future__ import annotations

from .logger import registrar_evento
from .sistema import SistemaFJ


def main() -> None:
    registrar_evento("Inicio de ejecucion de version 8.")
    sistema = SistemaFJ()
    sistema.ejecutar_demostracion_v8()
    registrar_evento("Fin de ejecucion de version 8.")


if __name__ == "__main__":
    main()
