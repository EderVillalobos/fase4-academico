from __future__ import annotations

from datetime import datetime

from .entidades import Cliente, Servicio
from .exceptions import ReservationError, ValidationError


class Reserva:
    ESTADO_CREADA = "creada"
    ESTADO_CONFIRMADA = "confirmada"
    ESTADO_CANCELADA = "cancelada"
    ESTADO_PROCESADA = "procesada"

    def __init__(self, identificador: str, cliente: Cliente, servicio: Servicio, horas: float) -> None:
        identificador = str(identificador).strip()
        if not identificador:
            raise ValidationError("El identificador de la reserva es obligatorio.")
        if horas <= 0:
            raise ValidationError("La duracion de la reserva debe ser mayor que cero.")
        self.identificador = identificador
        self.cliente = cliente
        self.servicio = servicio
        self.horas = float(horas)
        self.estado = self.ESTADO_CREADA
        self.total = 0.0
        self.fecha_actualizacion = datetime.now()

    def _actualizar_estado(self, estado: str) -> None:
        self.estado = estado
        self.fecha_actualizacion = datetime.now()

    def confirmar(self) -> None:
        if self.estado == self.ESTADO_CANCELADA:
            raise ReservationError("No se puede confirmar una reserva cancelada.")
        if self.estado == self.ESTADO_PROCESADA:
            raise ReservationError("No se puede confirmar una reserva procesada.")
        if self.estado == self.ESTADO_CONFIRMADA:
            raise ReservationError("La reserva ya esta confirmada.")
        self._actualizar_estado(self.ESTADO_CONFIRMADA)

    def cancelar(self, motivo: str = "") -> None:
        if self.estado == self.ESTADO_CANCELADA:
            raise ReservationError("La reserva ya estaba cancelada.")
        if self.estado == self.ESTADO_PROCESADA:
            raise ReservationError("No se puede cancelar una reserva procesada.")
        self._actualizar_estado(self.ESTADO_CANCELADA)
        self.motivo_cancelacion = motivo.strip()

    def procesar(self, impuesto: float = 0.0, descuento: float = 0.0) -> float:
        if not self.servicio.activo:
            raise ReservationError("El servicio no esta disponible.")
        if self.estado == self.ESTADO_CANCELADA:
            raise ReservationError("No se puede procesar una reserva cancelada.")
        if self.estado != self.ESTADO_CONFIRMADA:
            raise ReservationError("La reserva debe estar confirmada antes de procesarse.")
        self.total = self.servicio.calcular_costo(self.horas, impuesto=impuesto, descuento=descuento)
        self._actualizar_estado(self.ESTADO_PROCESADA)
        return self.total

    def resumen(self) -> str:
        return (
            f"Reserva {self.identificador}: {self.cliente.descripcion()} -> "
            f"{self.servicio.descripcion()} | horas={self.horas} | estado={self.estado} | total={self.total:.2f}"
        )
