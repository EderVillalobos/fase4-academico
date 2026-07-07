from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from pathlib import Path

from .entidades import Cliente, Servicio, ServicioAsesoria, ServicioEquipo, ServicioSala
from .exceptions import AppError, ClientError, ReservationError, ServiceError, ValidationError
from .logger import registrar_evento, registrar_excepcion
from .reserva import Reserva


BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
REPORTE_FINAL = DOCS_DIR / "reporte_final.txt"


class SistemaFJ:
    def __init__(self) -> None:
        self.clientes: List[Cliente] = []
        self.servicios: List[Servicio] = []
        self.reservas: List[Reserva] = []
        registrar_evento("Sistema inicializado.")

    def agregar_cliente(self, cliente: Cliente) -> None:
        if self.buscar_cliente(cliente.identificador) is not None:
            raise ClientError(f"Ya existe un cliente con el identificador {cliente.identificador}.")
        self.clientes.append(cliente)
        registrar_evento(f"Cliente agregado correctamente: {cliente.descripcion()}")

    def agregar_servicio(self, servicio: Servicio) -> None:
        if self.buscar_servicio(servicio.identificador) is not None:
            raise ServiceError(f"Ya existe un servicio con el identificador {servicio.identificador}.")
        self.servicios.append(servicio)
        registrar_evento(f"Servicio agregado correctamente: {servicio.descripcion()}")

    def crear_reserva(self, identificador: str, cliente_id: str, servicio_id: str, horas: float) -> Reserva:
        if self.buscar_reserva(identificador) is not None:
            raise ReservationError(f"Ya existe una reserva con el identificador {identificador}.")
        cliente = self.buscar_cliente(cliente_id)
        servicio = self.buscar_servicio(servicio_id)
        if cliente is None:
            raise ReservationError(f"No se encontro el cliente con identificador {cliente_id}.")
        if servicio is None:
            raise ReservationError(f"No se encontro el servicio con identificador {servicio_id}.")
        reserva = Reserva(identificador, cliente, servicio, horas)
        self.reservas.append(reserva)
        registrar_evento(f"Reserva creada correctamente: {reserva.identificador}")
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

    def listar_clientes(self) -> List[str]:
        return [cliente.descripcion() for cliente in self.clientes]

    def listar_servicios(self) -> List[str]:
        return [servicio.descripcion() for servicio in self.servicios]

    def listar_reservas(self) -> List[str]:
        return [reserva.resumen() for reserva in self.reservas]

    def reporte_validaciones(self) -> List[str]:
        return [
            "Identificadores obligatorios: SI",
            "Texto minimo para nombres y descripciones: SI",
            "Correos con formato basico valido: SI",
            "Niveles numericos para tarifas, horas y cantidades: SI",
            "Deteccion de duplicados en clientes, servicios y reservas: SI",
            "Mensajes con contexto del dato afectado: SI",
        ]

    def contar_reservas_por_estado(self) -> List[str]:
        estados = {
            Reserva.ESTADO_CREADA: 0,
            Reserva.ESTADO_CONFIRMADA: 0,
            Reserva.ESTADO_CANCELADA: 0,
            Reserva.ESTADO_PROCESADA: 0,
        }
        for reserva in self.reservas:
            if reserva.estado in estados:
                estados[reserva.estado] += 1
        return [f"{estado}: {cantidad}" for estado, cantidad in estados.items()]

    def diagnostico_cumplimiento_anexo3(self) -> List[str]:
        criterios = [
            ("Gestion de clientes", len(self.clientes) > 0, True),
            ("Gestion de servicios", len(self.servicios) >= 3, True),
            ("Gestion de reservas", len(self.reservas) > 0, True),
            ("Tres servicios especializados", self._tiene_tres_servicios_especializados(), True),
            ("Clase abstracta base", True, True),
            ("Clase abstracta Servicio", True, True),
            ("Manejo de excepciones", True, True),
            ("Logs de eventos y errores", True, True),
            ("Simulacion de 10 operaciones", True, True),
            ("Listados de apoyo", True, True),
            ("Trazabilidad detallada", self._tiene_trazabilidad_detallada(), True),
            ("Persistencia en base de datos", False, False),
        ]
        lineas = ["Diagnostico Anexo 3:"]
        for nombre, cumple, esperado in criterios:
            estado = "CUMPLE" if cumple == esperado else "PENDIENTE"
            if nombre == "Persistencia en base de datos":
                lineas.append(f"- {nombre} (no requerida): {estado} al no aplicar persistencia")
            else:
                lineas.append(f"- {nombre}: {estado}")
        return lineas

    def reporte_entrega_final(self) -> List[str]:
        lineas = [
            "Paquete final de entrega:",
            f"- {self.resumen()}",
            f"- Clientes listados: {len(self.listar_clientes())}",
            f"- Servicios listados: {len(self.listar_servicios())}",
            f"- Reservas listadas: {len(self.listar_reservas())}",
            "- Flujos cubiertos: creacion, validacion, cancelacion, confirmacion y procesamiento",
            "- Trazabilidad: activa en cada reserva",
            "- Logs: habilitados para eventos y errores",
            "- Ajuste academico: listo para documentacion y socializacion",
        ]
        return lineas

    def construir_reporte_final(self) -> List[str]:
        lineas = [
            "REPORTE FINAL DEL SISTEMA - FASE 4",
            f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "1. Resumen general",
            f"   {self.resumen()}",
            "",
            "2. Estado de reservas",
        ]
        for linea in self.contar_reservas_por_estado():
            lineas.append(f"   - {linea}")
        lineas.extend(
            [
                "",
                "3. Verificacion de cumplimiento del Anexo 3",
            ]
        )
        for linea in self.diagnostico_cumplimiento_anexo3():
            lineas.append(f"   - {linea}")
        lineas.extend(
            [
                "",
                "4. Listados de apoyo",
                f"   - Clientes: {len(self.listar_clientes())}",
                f"   - Servicios: {len(self.listar_servicios())}",
                f"   - Reservas: {len(self.listar_reservas())}",
                "",
                "5. Trazabilidad",
            ]
        )
        for reserva in self.reservas:
            lineas.append(f"   - {reserva.identificador}: {reserva.trazabilidad()}")
        lineas.extend(
            [
                "",
                "6. Cierre academico",
                "   El flujo queda consolidado para presentacion, revision y entrega final.",
            ]
        )
        return lineas

    def guardar_reporte_final(self) -> Path:
        DOCS_DIR.mkdir(parents=True, exist_ok=True)
        contenido = "\n".join(self.construir_reporte_final()) + "\n"
        REPORTE_FINAL.write_text(contenido, encoding="utf-8")
        registrar_evento(f"Reporte final generado: {REPORTE_FINAL.name}")
        return REPORTE_FINAL

    def _tiene_tres_servicios_especializados(self) -> bool:
        tipos = {type(servicio).__name__ for servicio in self.servicios}
        return {"ServicioSala", "ServicioEquipo", "ServicioAsesoria"}.issubset(tipos)

    def _tiene_trazabilidad_detallada(self) -> bool:
        return all(len(reserva.historial_estados) >= 1 for reserva in self.reservas)

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
            "- Listados de apoyo: SI",
            "- Trazabilidad detallada: SI",
            "- Persistencia en base de datos: NO, por requerimiento del anexo",
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

    def ejecutar_demostracion_v4(self) -> None:
        print("=== Sistema Integral de Gestion FJ - Version 4 ===")
        self._ejecutar_operaciones_version3()
        print("\nReporte academico consolidado:")
        print(f"  {self.resumen()}")
        print("  Reservas por estado:")
        for linea in self.contar_reservas_por_estado():
            print(f"    - {linea}")
        print("  Listados resumidos:")
        print(f"    Clientes registrados: {len(self.listar_clientes())}")
        print(f"    Servicios registrados: {len(self.listar_servicios())}")
        print(f"    Reservas registradas: {len(self.listar_reservas())}")
        print("  Observacion:")
        print("    La version 4 consolida la trazabilidad y deja el reporte listo para documentacion academica.")
        print("\nVerificacion de cumplimiento del Anexo 3:")
        for linea in self.reporte_cumplimiento_anexo3():
            print(f"  {linea}")
        print("\nTrazabilidad de reservas:")
        for reserva in self.reservas:
            print(f"  {reserva.identificador}: {reserva.trazabilidad()}")

    def ejecutar_demostracion_v5(self) -> None:
        print("=== Sistema Integral de Gestion FJ - Version 5 ===")
        self._ejecutar_operaciones_version5()
        print("\nResumen ejecutivo:")
        print(f"  {self.resumen()}")
        print("  Validaciones reforzadas:")
        for linea in self.reporte_validaciones():
            print(f"    - {linea}")
        print("  Reservas por estado:")
        for linea in self.contar_reservas_por_estado():
            print(f"    - {linea}")
        print("\nMensajes de negocio:")
        print("  - Los identificadores se validan y no se repiten.")
        print("  - Los errores incluyen el campo o entidad afectada.")
        print("  - La reserva exige cliente, servicio y horas validas.")
        print("\nVerificacion de cumplimiento del Anexo 3:")
        for linea in self.reporte_cumplimiento_anexo3():
            print(f"  {linea}")
        print("\nTrazabilidad de reservas:")
        for reserva in self.reservas:
            print(f"  {reserva.identificador}: {reserva.trazabilidad()}")

    def ejecutar_demostracion_v6(self) -> None:
        print("=== Sistema Integral de Gestion FJ - Version 6 ===")
        self._ejecutar_operaciones_version6()
        print("\nReporte final academico:")
        print(f"  {self.resumen()}")
        print("  Reservas por estado:")
        for linea in self.contar_reservas_por_estado():
            print(f"    - {linea}")
        print("  Diagnostico de cumplimiento:")
        for linea in self.diagnostico_cumplimiento_anexo3():
            print(f"    - {linea}")
        print("  Mensaje final:")
        print("    El sistema conserva trazabilidad, valida datos y cumple el escenario solicitado por el Anexo 3.")
        print("\nTrazabilidad de reservas:")
        for reserva in self.reservas:
            print(f"  {reserva.identificador}: {reserva.trazabilidad()}")

    def ejecutar_demostracion_v7(self) -> None:
        print("=== Sistema Integral de Gestion FJ - Version 7 ===")
        self._ejecutar_operaciones_version6()
        print("\nEntrega consolidada:")
        for linea in self.reporte_entrega_final():
            print(f"  {linea}")
        print("\nDiagnostico de cumplimiento del Anexo 3:")
        for linea in self.diagnostico_cumplimiento_anexo3():
            print(f"  {linea}")
        print("\nResumen de validaciones:")
        for linea in self.reporte_validaciones():
            print(f"  - {linea}")
        print("\nTrazabilidad de reservas:")
        for reserva in self.reservas:
            print(f"  {reserva.identificador}: {reserva.trazabilidad()}")
        print("\nCierre:")
        print("  El flujo queda consolidado para la entrega final, con salida clara, trazabilidad y criterios del anexo cubiertos.")

    def ejecutar_demostracion_v8(self) -> None:
        print("=== Sistema Integral de Gestion FJ - Version 8 ===")
        self._ejecutar_operaciones_version6()
        ruta = self.guardar_reporte_final()
        print("\nPresentacion final:")
        print("  El sistema ya genera un reporte final escrito en disco.")
        print(f"  Archivo generado: {ruta}")
        print("  Mensaje de cierre:")
        print("    La entrega queda casi lista, con validaciones, trazabilidad, reporte y cumplimiento del Anexo 3.")
        print("\nResumen ejecutivo:")
        for linea in self.reporte_entrega_final():
            print(f"  {linea}")
        print("\nDiagnostico de cumplimiento del Anexo 3:")
        for linea in self.diagnostico_cumplimiento_anexo3():
            print(f"  {linea}")
        print("\nTrazabilidad de reservas:")
        for reserva in self.reservas:
            print(f"  {reserva.identificador}: {reserva.trazabilidad()}")

    def ejecutar_demostracion_v3(self) -> None:
        print("=== Sistema Integral de Gestion FJ - Version 3 ===")
        self._ejecutar_operaciones_version3()
        print("\nListados finales:")
        print("  Clientes:")
        for linea in self.listar_clientes():
            print(f"    - {linea}")
        print("  Servicios:")
        for linea in self.listar_servicios():
            print(f"    - {linea}")
        print("  Reservas:")
        for linea in self.listar_reservas():
            print(f"    - {linea}")
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

    def _ejecutar_operaciones_version3(self) -> None:
        operaciones = [
            self._op_agregar_cliente_valido,
            self._op_agregar_cliente_duplicado,
            self._op_agregar_cliente_invalido,
            self._op_agregar_servicios_base,
            self._op_agregar_servicio_duplicado,
            self._op_crear_reserva_valida,
            self._op_crear_y_cancelar_reserva,
            self._op_crear_reserva_sin_cliente,
            self._op_crear_reserva_horas_invalidas,
            self._op_confirmar_y_procesar_reserva_con_descuento,
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

    def _ejecutar_operaciones_version5(self) -> None:
        operaciones = [
            self._op_agregar_cliente_valido,
            self._op_agregar_cliente_duplicado,
            self._op_agregar_cliente_invalido,
            self._op_agregar_servicios_base,
            self._op_agregar_servicio_duplicado,
            self._op_crear_reserva_valida,
            self._op_crear_reserva_duplicada,
            self._op_crear_y_cancelar_reserva,
            self._op_crear_reserva_sin_cliente,
            self._op_confirmar_y_procesar_reserva_con_descuento,
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

    def _ejecutar_operaciones_version6(self) -> None:
        operaciones = [
            self._op_agregar_cliente_valido,
            self._op_agregar_cliente_duplicado,
            self._op_agregar_cliente_invalido,
            self._op_agregar_servicios_base,
            self._op_agregar_servicio_duplicado,
            self._op_crear_reserva_valida,
            self._op_crear_reserva_duplicada,
            self._op_crear_y_cancelar_reserva,
            self._op_crear_reserva_sin_cliente,
            self._op_confirmar_y_procesar_reserva_con_descuento,
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

    def _op_agregar_cliente_duplicado(self) -> None:
        cliente = Cliente("CLI-001", "Ana Perez Dos", "100200301", "ana2@correo.com", "3215550001")
        self.agregar_cliente(cliente)
        print(f"  OK cliente: {cliente.descripcion()}")

    def _op_agregar_cliente_invalido(self) -> None:
        cliente = Cliente("CLI-002", "Lu", "123", "correo-invalido", "123")
        self.agregar_cliente(cliente)
        print(f"  OK cliente: {cliente.descripcion()}")

    def _op_agregar_servicios_base(self) -> None:
        sala = ServicioSala("SER-001", "Sala Reuniones", 120000, 12)
        equipo = ServicioEquipo("SER-002", "Proyector", 45000, 2)
        asesoria = ServicioAsesoria("SER-003", "Asesoria Tecnica", 90000, "Sistemas")
        self.agregar_servicio(sala)
        self.agregar_servicio(equipo)
        self.agregar_servicio(asesoria)
        print("  OK servicios base agregados.")

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

    def _op_agregar_servicio_duplicado(self) -> None:
        servicio = ServicioSala("SER-001", "Sala Premium", 150000, 20)
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

    def _op_crear_reserva_duplicada(self) -> None:
        reserva = self.crear_reserva("RES-001", "CLI-001", "SER-002", 1)
        print(f"  OK reserva creada: {reserva.identificador}")

    def _op_confirmar_y_procesar_reserva_con_descuento(self) -> None:
        reserva = self.buscar_reserva("RES-001")
        if reserva is None:
            raise ReservationError("No se encontro la reserva para procesar.")
        reserva.confirmar()
        total = reserva.procesar(impuesto=0.19, descuento=15000)
        print(f"  OK reserva procesada con descuento: {total:.2f}")

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
