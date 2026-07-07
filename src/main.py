from __future__ import annotations

from .logger import registrar_evento
from .interfaz import ejecutar_interfaz


def main() -> None:
    registrar_evento("Inicio de ejecucion de interfaz Tkinter.")
    ejecutar_interfaz()
    registrar_evento("Fin de ejecucion de interfaz Tkinter.")


if __name__ == "__main__":
    main()
