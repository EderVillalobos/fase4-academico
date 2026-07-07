from __future__ import annotations

from .logger import registrar_evento
from .sistema import SistemaFJ


def main() -> None:
    registrar_evento("Inicio de ejecucion de version 6.")
    sistema = SistemaFJ()
    sistema.ejecutar_demostracion_v6()
    registrar_evento("Fin de ejecucion de version 6.")


if __name__ == "__main__":
    main()
