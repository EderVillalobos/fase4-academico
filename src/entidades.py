from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

from .exceptions import ValidationError


class EntidadBase(ABC):
    def __init__(self, identificador: str) -> None:
        identificador = str(identificador).strip()
        if not identificador:
            raise ValidationError("El identificador es obligatorio.")
        self._identificador = identificador
        self._fecha_creacion = datetime.now()

    @property
    def identificador(self) -> str:
        return self._identificador

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    @abstractmethod
    def descripcion(self) -> str:
        raise NotImplementedError


class Cliente(EntidadBase):
    def __init__(self, identificador: str, nombre: str, documento: str, correo: str, telefono: str) -> None:
        super().__init__(identificador)
        self._nombre = ""
        self._documento = ""
        self._correo = ""
        self._telefono = ""
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        valor = str(valor).strip()
        if len(valor) < 3:
            raise ValidationError("El nombre del cliente debe tener al menos 3 caracteres.")
        self._nombre = valor

    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str) -> None:
        valor = str(valor).strip()
        if len(valor) < 5:
            raise ValidationError("El documento debe tener al menos 5 caracteres.")
        self._documento = valor

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        valor = str(valor).strip().lower()
        if "@" not in valor or "." not in valor:
            raise ValidationError("El correo no tiene un formato valido.")
        self._correo = valor

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        valor = str(valor).strip()
        if len(valor) < 7:
            raise ValidationError("El telefono debe tener al menos 7 caracteres.")
        self._telefono = valor

    def descripcion(self) -> str:
        return f"{self.nombre} ({self.documento})"


class Servicio(EntidadBase, ABC):
    def __init__(self, identificador: str, nombre: str, tarifa_base: float) -> None:
        super().__init__(identificador)
        self._nombre = ""
        self._tarifa_base = 0.0
        self._activo = True
        self.nombre = nombre
        self.tarifa_base = tarifa_base

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        valor = str(valor).strip()
        if len(valor) < 3:
            raise ValidationError("El nombre del servicio debe tener al menos 3 caracteres.")
        self._nombre = valor

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        try:
            valor = float(valor)
        except ValueError as exc:
            raise ValidationError("La tarifa base debe ser numerica.") from exc
        if valor <= 0:
            raise ValidationError("La tarifa base debe ser mayor que cero.")
        self._tarifa_base = valor

    @property
    def activo(self) -> bool:
        return self._activo

    def desactivar(self) -> None:
        self._activo = False

    def activar(self) -> None:
        self._activo = True

    @abstractmethod
    def calcular_costo(self, horas: float = 1, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        raise NotImplementedError

    def descripcion(self) -> str:
        return f"{self.nombre} - base {self.tarifa_base:.2f}"


class ServicioSala(Servicio):
    def __init__(self, identificador: str, nombre: str, tarifa_base: float, capacidad: int) -> None:
        super().__init__(identificador, nombre, tarifa_base)
        self._capacidad = 0
        self.capacidad = capacidad

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor: int) -> None:
        valor = int(valor)
        if valor <= 0:
            raise ValidationError("La capacidad debe ser mayor que cero.")
        self._capacidad = valor

    def calcular_costo(self, horas: float = 1, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        subtotal = self.tarifa_base * float(horas)
        retorno = subtotal + (subtotal * float(impuesto)) - float(descuento)
        return max(retorno, 0.0)

    def descripcion(self) -> str:
        return f"Sala {self.nombre} para {self.capacidad} personas"


class ServicioEquipo(Servicio):
    def __init__(self, identificador: str, nombre: str, tarifa_base: float, cantidad: int) -> None:
        super().__init__(identificador, nombre, tarifa_base)
        self._cantidad = 0
        self.cantidad = cantidad

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        valor = int(valor)
        if valor <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero.")
        self._cantidad = valor

    def calcular_costo(self, horas: float = 1, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        subtotal = self.tarifa_base * float(horas) * self.cantidad
        retorno = subtotal + (subtotal * float(impuesto)) - float(descuento)
        return max(retorno, 0.0)

    def descripcion(self) -> str:
        return f"Equipo {self.nombre} x {self.cantidad}"


class ServicioAsesoria(Servicio):
    def __init__(self, identificador: str, nombre: str, tarifa_base: float, especialidad: str) -> None:
        super().__init__(identificador, nombre, tarifa_base)
        self._especialidad = ""
        self.especialidad = especialidad

    @property
    def especialidad(self) -> str:
        return self._especialidad

    @especialidad.setter
    def especialidad(self, valor: str) -> None:
        valor = str(valor).strip()
        if len(valor) < 4:
            raise ValidationError("La especialidad debe tener al menos 4 caracteres.")
        self._especialidad = valor

    def calcular_costo(self, horas: float = 1, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        subtotal = self.tarifa_base * float(horas)
        retorno = subtotal + (subtotal * float(impuesto)) - float(descuento)
        return max(retorno, 0.0)

    def descripcion(self) -> str:
        return f"Asesoria {self.nombre} en {self.especialidad}"

