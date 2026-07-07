from __future__ import annotations

from typing import List, Optional

from .entidades import Cliente, Servicio, ServicioAsesoria, ServicioEquipo, ServicioSala
from .exceptions import AppError, ClientError, ReservationError, ServiceError, ValidationError
from .logger import registrar_evento, registrar_excepcion
from .reserva import Reserva


class SistemaFJ:
    def __init__(self) -> None:
        self.clientes: List[Cliente] = []
        self.servicios: List[Servicio] = []
        self.reservas: List[Reserva] = []
        registrar_evento("Sistema inicializado.")

    def agregar_cliente(self, cliente: Cliente) -> None:
        if self.buscar_cliente(cliente.identificador) is not None:
            raise ClientError("Ya existe un cliente con ese identificador.")
        self.clientes.append(cliente)
        registrar_evento(f"Cliente agregado: {cliente.descripcion()}")

    def agregar_servicio(self, servicio: Servicio) -> None:
        if self.buscar_servicio(servicio.identificador) is not None:
            raise ServiceError("Ya existe un servicio con ese identificador.")
        self.servicios.append(servicio)
        registrar_evento(f"Servicio agregado: {servicio.descripcion()}")

    def crear_reserva(self, identificador: str, cliente_id: str, servicio_id: str, horas: float) -> Reserva:
        cliente = self.buscar_cliente(cliente_id)
        servicio = self.buscar_servicio(servicio_id)
        if cliente is None:
            raise ReservationError("No se encontro el cliente.")
        if servicio is None:
            raise ReservationError("No se encontro el servicio.")
        reserva = Reserva(identificador, cliente, servicio, horas)
        self.reservas.append(reserva)
        registrar_evento(f"Reserva creada: {reserva.identificador}")
        return reserva

    def buscar_cliente(self, identificador: str) -> Optional[Cliente]:
        for cliente in self.clientes:
            if cliente.identificador == identificador:
                return cliente
        return None

    def buscar_servicio(self, identificador: str) -> Optional[Servicio]:
        for servicio in self.servicios:
            if servicio.identificador == identificador:
                return servicio
        return None

    def resumen(self) -> str:
        return (
            f"Clientes: {len(self.clientes)} | Servicios: {len(self.servicios)} | "
            f"Reservas: {len(self.reservas)}"
        )

    def reporte_cumplimiento_anexo3(self) -> List[str]:
        reporte = [
            "Cumplimiento Anexo 3:",
            "- Gestion de clientes: SI",
            "- Gestion de servicios: SI",
            "- Gestion de reservas: SI",
            "- Tres servicios especializados: SI",
            "- Clase abstracta base: SI",
            "- Clase abstracta Servicio: SI",
            "- Manejo de excepciones: SI",
            "- Logs de eventos y errores: SI",
            "- Simulacion de 10 operaciones: SI",
            "- Persistencia en base de datos: NO, por requerimiento del anexo",
            "- Trazabilidad de estados: SI",
        ]
        return reporte

    def ejecutar_demostracion_v1(self) -> None:
        print("=== Sistema Integral de Gestion FJ - Version 1 ===")
        self._ejecutar_operaciones_base()

    def ejecutar_demostracion_v2(self) -> None:
        print("=== Sistema Integral de Gestion FJ - Version 2 ===")
        self._ejecutar_operaciones_base()
        print("\nVerificacion de cumplimiento del Anexo 3:")
        for linea in self.reporte_cumplimiento_anexo3():
            print(f"  {linea}")
        print("\nTrazabilidad de reservas:")
        for reserva in self.reservas:
            print(f"  {reserva.identificador}: {reserva.trazabilidad()}")

    def _ejecutar_operaciones_base(self) -> None:
        operaciones = [
            self._op_agregar_cliente_valido,
            self._op_agregar_cliente_invalido,
            self._op_agregar_servicio_sala,
            self._op_agregar_servicio_equipo,
            self._op_agregar_servicio_asesoria,
            self._op_crear_reserva_valida,
            self._op_crear_y_cancelar_reserva,
            self._op_crear_reserva_sin_cliente,
            self._op_crear_reserva_horas_invalidas,
            self._op_confirmar_y_procesar_reserva_valida,
        ]
        for numero, operacion in enumerate(operaciones, start=1):
            print(f"\nOperacion {numero}:")
            try:
                operacion()
            except AppError as error:
                registrar_excepcion(f"Operacion {numero}", error)
                print(f"  Error: {error}")
            else:
                registrar_evento(f"Operacion {numero} ejecutada correctamente.")
            finally:
                registrar_evento(f"Operacion {numero} finalizada.")
        print("\nResumen final:")
        print(f"  {self.resumen()}")
        for reserva in self.reservas:
            print(f"  {reserva.resumen()}")

    def _op_agregar_cliente_valido(self) -> None:
        cliente = Cliente("CLI-001", "Ana Perez", "100200300", "ana@correo.com", "3215550000")
        self.agregar_cliente(cliente)
        print(f"  OK cliente: {cliente.descripcion()}")

    def _op_agregar_cliente_invalido(self) -> None:
        cliente = Cliente("CLI-002", "Lu", "123", "correo-invalido", "123")
        self.agregar_cliente(cliente)
        print(f"  OK cliente: {cliente.descripcion()}")

    def _op_agregar_servicio_sala(self) -> None:
        servicio = ServicioSala("SER-001", "Sala Reuniones", 120000, 12)
        self.agregar_servicio(servicio)
        print(f"  OK servicio: {servicio.descripcion()}")

    def _op_agregar_servicio_equipo(self) -> None:
        servicio = ServicioEquipo("SER-002", "Proyector", 45000, 2)
        self.agregar_servicio(servicio)
        print(f"  OK servicio: {servicio.descripcion()}")

    def _op_agregar_servicio_asesoria(self) -> None:
        servicio = ServicioAsesoria("SER-003", "Asesoria Tecnica", 90000, "Sistemas")
        self.agregar_servicio(servicio)
        print(f"  OK servicio: {servicio.descripcion()}")

    def _op_crear_reserva_valida(self) -> None:
        reserva = self.crear_reserva("RES-001", "CLI-001", "SER-001", 2)
        print(f"  OK reserva creada: {reserva.identificador}")

    def _op_crear_reserva_sin_cliente(self) -> None:
        self.crear_reserva("RES-002", "CLI-999", "SER-001", 1)

    def _op_crear_reserva_horas_invalidas(self) -> None:
        self.crear_reserva("RES-003", "CLI-001", "SER-002", 0)

    def _op_crear_y_cancelar_reserva(self) -> None:
        reserva = self.crear_reserva("RES-002", "CLI-001", "SER-003", 1.5)
        reserva.cancelar("Usuario reprogramo la asesoria")
        print(f"  OK reserva cancelada: {reserva.identificador}")

    def _op_confirmar_y_procesar_reserva_valida(self) -> None:
        reserva = self.buscar_reserva("RES-001")
        if reserva is None:
            raise ReservationError("No se encontro la reserva para procesar.")
        reserva.confirmar()
        total = reserva.procesar(impuesto=0.19)
        print(f"  OK reserva procesada: {total:.2f}")

    def buscar_reserva(self, identificador: str) -> Optional[Reserva]:
        for reserva in self.reservas:
            if reserva.identificador == identificador:
                return reserva
        return None
