from __future__ import annotations

import io
from contextlib import redirect_stdout
from tkinter import END, LEFT, RIGHT, X, Y, BOTH, ttk, messagebox
import tkinter as tk
from tkinter import scrolledtext

from .entidades import Cliente, ServicioAsesoria, ServicioEquipo, ServicioSala
from .exceptions import AppError, ValidationError
from .logger import LOG_FILE, registrar_evento, registrar_excepcion
from .sistema import SistemaFJ


class InterfazFJ:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.sistema = SistemaFJ()
        self.root.title("Software FJ - Gestion de Clientes, Servicios y Reservas")
        self.root.geometry("1200x780")
        self.root.minsize(1100, 700)

        self._crear_estilo()
        self._crear_interfaz()
        self._actualizar_todo()

    def _crear_estilo(self) -> None:
        estilo = ttk.Style(self.root)
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass
        estilo.configure("TFrame", padding=6)
        estilo.configure("TLabel", padding=2)
        estilo.configure("TButton", padding=(10, 5))
        estilo.configure("Header.TLabel", font=("Segoe UI", 13, "bold"))

    def _crear_interfaz(self) -> None:
        contenedor = ttk.Frame(self.root)
        contenedor.pack(fill=BOTH, expand=True)

        encabezado = ttk.Frame(contenedor)
        encabezado.pack(fill=X)
        ttk.Label(
            encabezado,
            text="Software FJ",
            style="Header.TLabel",
        ).pack(side=LEFT)
        ttk.Label(
            encabezado,
            text="Sistema orientado a objetos para clientes, servicios y reservas",
        ).pack(side=LEFT, padx=12)

        self.var_resumen = tk.StringVar(value="")
        ttk.Label(encabezado, textvariable=self.var_resumen).pack(side=RIGHT)

        self.pestanas = ttk.Notebook(contenedor)
        self.pestanas.pack(fill=BOTH, expand=True, pady=(8, 0))

        self._crear_pestana_clientes()
        self._crear_pestana_servicios()
        self._crear_pestana_reservas()
        self._crear_pestana_demostracion()
        self._crear_pestana_logs()

        barra = ttk.Frame(contenedor)
        barra.pack(fill=X, pady=(6, 0))
        self.var_estado = tk.StringVar(value="Listo para registrar operaciones.")
        ttk.Label(barra, textvariable=self.var_estado).pack(side=LEFT)
        ttk.Button(barra, text="Actualizar todo", command=self._actualizar_todo).pack(side=RIGHT)

    def _crear_pestana_clientes(self) -> None:
        pestaña = ttk.Frame(self.pestanas)
        self.pestanas.add(pestaña, text="Clientes")

        form = ttk.LabelFrame(pestaña, text="Registrar cliente")
        form.pack(fill=X)

        self.var_cli_id = tk.StringVar()
        self.var_cli_nombre = tk.StringVar()
        self.var_cli_doc = tk.StringVar()
        self.var_cli_correo = tk.StringVar()
        self.var_cli_tel = tk.StringVar()

        campos = [
            ("Identificador", self.var_cli_id),
            ("Nombre", self.var_cli_nombre),
            ("Documento", self.var_cli_doc),
            ("Correo", self.var_cli_correo),
            ("Telefono", self.var_cli_tel),
        ]
        for idx, (etiqueta, variable) in enumerate(campos):
            ttk.Label(form, text=etiqueta).grid(row=idx // 2, column=(idx % 2) * 2, sticky="w", padx=4, pady=4)
            ttk.Entry(form, textvariable=variable, width=34).grid(row=idx // 2, column=(idx % 2) * 2 + 1, sticky="ew", padx=4, pady=4)

        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        botones = ttk.Frame(pestaña)
        botones.pack(fill=X, pady=(4, 6))
        ttk.Button(botones, text="Agregar cliente", command=self._accion_agregar_cliente).pack(side=LEFT)
        ttk.Button(botones, text="Limpiar", command=self._limpiar_cliente).pack(side=LEFT, padx=6)

        self.tree_clientes = self._crear_treeview(
            pestaña,
            ("ID", "Nombre", "Documento", "Correo", "Telefono"),
            ("id", "nombre", "documento", "correo", "telefono"),
        )

    def _crear_pestana_servicios(self) -> None:
        pestaña = ttk.Frame(self.pestanas)
        self.pestanas.add(pestaña, text="Servicios")

        form = ttk.LabelFrame(pestaña, text="Registrar servicio")
        form.pack(fill=X)

        self.var_ser_tipo = tk.StringVar(value="Sala")
        self.var_ser_id = tk.StringVar()
        self.var_ser_nombre = tk.StringVar()
        self.var_ser_tarifa = tk.StringVar()
        self.var_ser_extra = tk.StringVar()

        ttk.Label(form, text="Tipo").grid(row=0, column=0, sticky="w", padx=4, pady=4)
        ttk.Combobox(form, textvariable=self.var_ser_tipo, values=("Sala", "Equipo", "Asesoria"), state="readonly", width=30).grid(row=0, column=1, sticky="ew", padx=4, pady=4)
        ttk.Label(form, text="Identificador").grid(row=0, column=2, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.var_ser_id, width=34).grid(row=0, column=3, sticky="ew", padx=4, pady=4)
        ttk.Label(form, text="Nombre").grid(row=1, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.var_ser_nombre, width=34).grid(row=1, column=1, sticky="ew", padx=4, pady=4)
        ttk.Label(form, text="Tarifa base").grid(row=1, column=2, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.var_ser_tarifa, width=34).grid(row=1, column=3, sticky="ew", padx=4, pady=4)
        self.lbl_extra = ttk.Label(form, text="Capacidad")
        self.lbl_extra.grid(row=2, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.var_ser_extra, width=34).grid(row=2, column=1, sticky="ew", padx=4, pady=4)
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        self.var_ser_tipo.trace_add("write", self._actualizar_etiqueta_extra)
        self._actualizar_etiqueta_extra()

        botones = ttk.Frame(pestaña)
        botones.pack(fill=X, pady=(4, 6))
        ttk.Button(botones, text="Agregar servicio", command=self._accion_agregar_servicio).pack(side=LEFT)
        ttk.Button(botones, text="Limpiar", command=self._limpiar_servicio).pack(side=LEFT, padx=6)

        self.tree_servicios = self._crear_treeview(
            pestaña,
            ("ID", "Nombre", "Tipo", "Detalle", "Tarifa"),
            ("id", "nombre", "tipo", "detalle", "tarifa"),
        )

    def _crear_pestana_reservas(self) -> None:
        pestaña = ttk.Frame(self.pestanas)
        self.pestanas.add(pestaña, text="Reservas")

        form = ttk.LabelFrame(pestaña, text="Gestion de reserva")
        form.pack(fill=X)

        self.var_res_id = tk.StringVar()
        self.var_res_cli = tk.StringVar()
        self.var_res_ser = tk.StringVar()
        self.var_res_horas = tk.StringVar()
        self.var_res_impuesto = tk.StringVar(value="0.19")
        self.var_res_descuento = tk.StringVar(value="0")
        self.var_res_motivo = tk.StringVar()

        campos = [
            ("Identificador", self.var_res_id),
            ("Cliente ID", self.var_res_cli),
            ("Servicio ID", self.var_res_ser),
            ("Horas", self.var_res_horas),
            ("Impuesto", self.var_res_impuesto),
            ("Descuento", self.var_res_descuento),
        ]
        for idx, (etiqueta, variable) in enumerate(campos):
            fila = idx // 2
            columna = (idx % 2) * 2
            ttk.Label(form, text=etiqueta).grid(row=fila, column=columna, sticky="w", padx=4, pady=4)
            ttk.Entry(form, textvariable=variable, width=34).grid(row=fila, column=columna + 1, sticky="ew", padx=4, pady=4)

        ttk.Label(form, text="Motivo cancelacion").grid(row=3, column=0, sticky="w", padx=4, pady=4)
        ttk.Entry(form, textvariable=self.var_res_motivo, width=78).grid(row=3, column=1, columnspan=3, sticky="ew", padx=4, pady=4)
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        botones = ttk.Frame(pestaña)
        botones.pack(fill=X, pady=(4, 6))
        ttk.Button(botones, text="Crear reserva", command=self._accion_crear_reserva).pack(side=LEFT)
        ttk.Button(botones, text="Confirmar", command=self._accion_confirmar_reserva).pack(side=LEFT, padx=4)
        ttk.Button(botones, text="Procesar", command=self._accion_procesar_reserva).pack(side=LEFT, padx=4)
        ttk.Button(botones, text="Cancelar", command=self._accion_cancelar_reserva).pack(side=LEFT, padx=4)
        ttk.Button(botones, text="Limpiar", command=self._limpiar_reserva).pack(side=LEFT, padx=4)

        self.tree_reservas = self._crear_treeview(
            pestaña,
            ("ID", "Cliente", "Servicio", "Horas", "Estado", "Total"),
            ("id", "cliente", "servicio", "horas", "estado", "total"),
        )

    def _crear_pestana_demostracion(self) -> None:
        pestaña = ttk.Frame(self.pestanas)
        self.pestanas.add(pestaña, text="Demostracion")

        panel = ttk.LabelFrame(pestaña, text="Pruebas funcionales")
        panel.pack(fill=X)

        ttk.Button(panel, text="Ejecutar demostracion completa", command=self._accion_demo_completa).pack(fill=X, pady=4)
        ttk.Button(panel, text="Reiniciar sistema", command=self._accion_reiniciar).pack(fill=X, pady=4)
        ttk.Button(panel, text="Ver reporte de estado", command=self._mostrar_reporte_estado).pack(fill=X, pady=4)
        ttk.Button(panel, text="Abrir log de eventos", command=self._abrir_log).pack(fill=X, pady=4)

        salida = ttk.LabelFrame(pestaña, text="Salida de la demostracion")
        salida.pack(fill=BOTH, expand=True, pady=(8, 0))
        self.txt_salida = scrolledtext.ScrolledText(salida, height=18, wrap=tk.WORD)
        self.txt_salida.pack(fill=BOTH, expand=True)

    def _crear_pestana_logs(self) -> None:
        pestaña = ttk.Frame(self.pestanas)
        self.pestanas.add(pestaña, text="Logs")

        panel = ttk.LabelFrame(pestaña, text="Eventos registrados")
        panel.pack(fill=BOTH, expand=True)

        botones = ttk.Frame(panel)
        botones.pack(fill=X)
        ttk.Button(botones, text="Actualizar logs", command=self._refrescar_logs).pack(side=LEFT)
        ttk.Button(botones, text="Abrir archivo", command=self._abrir_log).pack(side=LEFT, padx=6)

        self.txt_logs = scrolledtext.ScrolledText(panel, height=24, wrap=tk.WORD)
        self.txt_logs.pack(fill=BOTH, expand=True, pady=(6, 0))

    def _crear_treeview(self, parent: ttk.Frame, encabezados: tuple[str, ...], columnas: tuple[str, ...]) -> ttk.Treeview:
        panel = ttk.Frame(parent)
        panel.pack(fill=BOTH, expand=True)

        tree = ttk.Treeview(panel, columns=columnas, show="headings", height=10)
        for columna, encabezado in zip(columnas, encabezados):
            tree.heading(columna, text=encabezado)
            tree.column(columna, width=130, anchor="w")

        scroll_y = ttk.Scrollbar(panel, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll_y.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True)
        scroll_y.pack(side=RIGHT, fill=Y)
        return tree

    def _actualizar_etiqueta_extra(self, *_: object) -> None:
        tipo = self.var_ser_tipo.get()
        if tipo == "Sala":
            texto = "Capacidad"
        elif tipo == "Equipo":
            texto = "Cantidad"
        else:
            texto = "Especialidad"
        self.lbl_extra.configure(text=texto)

    def _append_salida(self, texto: str) -> None:
        self.txt_salida.insert(END, texto.rstrip() + "\n")
        self.txt_salida.see(END)

    def _append_log_local(self, texto: str) -> None:
        self.txt_logs.insert(END, texto.rstrip() + "\n")
        self.txt_logs.see(END)

    def _capturar_salida(self, accion) -> str:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            accion()
        return buffer.getvalue()

    def _ejecutar_con_manejo(self, contexto: str, accion, exito: str | None = None) -> None:
        try:
            resultado = accion()
        except AppError as error:
            registrar_excepcion(contexto, error)
            messagebox.showerror("Error", str(error), parent=self.root)
            self._set_estado(f"{contexto}: error controlado.")
        except Exception as error:
            registrar_excepcion(contexto, error)
            messagebox.showerror("Error inesperado", str(error), parent=self.root)
            self._set_estado(f"{contexto}: error inesperado.")
        else:
            if exito:
                messagebox.showinfo("Correcto", exito, parent=self.root)
            elif resultado is not None:
                messagebox.showinfo("Correcto", str(resultado), parent=self.root)
            self._set_estado(f"{contexto}: completado.")
        finally:
            self._actualizar_todo()

    def _extraer_servicio(self) -> object:
        tipo = self.var_ser_tipo.get()
        identificador = self.var_ser_id.get().strip()
        nombre = self.var_ser_nombre.get().strip()
        tarifa = self.var_ser_tarifa.get().strip()
        extra = self.var_ser_extra.get().strip()
        if tipo == "Sala":
            return ServicioSala(identificador, nombre, tarifa, extra)
        if tipo == "Equipo":
            return ServicioEquipo(identificador, nombre, tarifa, extra)
        return ServicioAsesoria(identificador, nombre, tarifa, extra)

    def _accion_agregar_cliente(self) -> None:
        def operacion() -> None:
            cliente = Cliente(
                self.var_cli_id.get(),
                self.var_cli_nombre.get(),
                self.var_cli_doc.get(),
                self.var_cli_correo.get(),
                self.var_cli_tel.get(),
            )
            self.sistema.agregar_cliente(cliente)
            registrar_evento(f"Cliente agregado desde GUI: {cliente.descripcion()}")
            self._limpiar_cliente()

        self._ejecutar_con_manejo("Agregar cliente", operacion, "Cliente registrado correctamente.")

    def _accion_agregar_servicio(self) -> None:
        def operacion() -> None:
            servicio = self._extraer_servicio()
            self.sistema.agregar_servicio(servicio)
            registrar_evento(f"Servicio agregado desde GUI: {servicio.descripcion()}")
            self._limpiar_servicio()

        self._ejecutar_con_manejo("Agregar servicio", operacion, "Servicio registrado correctamente.")

    def _accion_crear_reserva(self) -> None:
        def operacion() -> None:
            reserva = self.sistema.crear_reserva(
                self.var_res_id.get(),
                self.var_res_cli.get(),
                self.var_res_ser.get(),
                self.var_res_horas.get(),
            )
            registrar_evento(f"Reserva creada desde GUI: {reserva.identificador}")
            self._limpiar_reserva()

        self._ejecutar_con_manejo("Crear reserva", operacion, "Reserva creada correctamente.")

    def _accion_confirmar_reserva(self) -> None:
        def operacion() -> None:
            reserva = self._buscar_reserva_gui()
            reserva.confirmar()
            registrar_evento(f"Reserva confirmada desde GUI: {reserva.identificador}")

        self._ejecutar_con_manejo("Confirmar reserva", operacion, "Reserva confirmada.")

    def _accion_procesar_reserva(self) -> None:
        def operacion() -> None:
            reserva = self._buscar_reserva_gui()
            try:
                impuesto = float(self.var_res_impuesto.get() or 0)
                descuento = float(self.var_res_descuento.get() or 0)
            except ValueError as exc:
                raise ValidationError("El impuesto y el descuento deben ser numericos.") from exc
            total = reserva.procesar(impuesto=impuesto, descuento=descuento)
            registrar_evento(f"Reserva procesada desde GUI: {reserva.identificador} -> {total:.2f}")
            self._append_salida(f"Reserva {reserva.identificador} procesada por {total:.2f}")

        self._ejecutar_con_manejo("Procesar reserva", operacion, "Reserva procesada.")

    def _accion_cancelar_reserva(self) -> None:
        def operacion() -> None:
            reserva = self._buscar_reserva_gui()
            reserva.cancelar(self.var_res_motivo.get())
            registrar_evento(f"Reserva cancelada desde GUI: {reserva.identificador}")

        self._ejecutar_con_manejo("Cancelar reserva", operacion, "Reserva cancelada.")

    def _accion_demo_completa(self) -> None:
        def operacion() -> str:
            self.sistema = SistemaFJ()
            salida = self._capturar_salida(self.sistema.ejecutar_demostracion_v10)
            return salida

        try:
            salida = operacion()
        except AppError as error:
            registrar_excepcion("Demostracion completa", error)
            messagebox.showerror("Error", str(error), parent=self.root)
            self._set_estado("Demostracion completa: error controlado.")
        except Exception as error:
            registrar_excepcion("Demostracion completa", error)
            messagebox.showerror("Error inesperado", str(error), parent=self.root)
            self._set_estado("Demostracion completa: error inesperado.")
        else:
            self._append_salida(salida)
            messagebox.showinfo("Demostracion", "La demostracion completa se ejecuto correctamente.", parent=self.root)
            self._set_estado("Demostracion completa ejecutada.")
        finally:
            self._actualizar_todo()

    def _accion_reiniciar(self) -> None:
        self.sistema = SistemaFJ()
        registrar_evento("Sistema reiniciado desde la GUI.")
        self._append_salida("Sistema reiniciado.")
        self._set_estado("Sistema reiniciado correctamente.")
        self._actualizar_todo()

    def _mostrar_reporte_estado(self) -> None:
        clientes = [f"- {cliente.descripcion()}" for cliente in self.sistema.clientes] or ["- Sin registros"]
        servicios = [f"- {servicio.descripcion()}" for servicio in self.sistema.servicios] or ["- Sin registros"]
        reservas = [f"- {reserva.resumen()}" for reserva in self.sistema.reservas] or ["- Sin registros"]
        lineas = [
            self.sistema.resumen(),
            "",
            "Clientes:",
            *clientes,
            "",
            "Servicios:",
            *servicios,
            "",
            "Reservas:",
            *reservas,
        ]
        self._append_salida("\n".join(lineas))
        self._set_estado("Reporte de estado mostrado.")

    def _buscar_reserva_gui(self):
        identificador = self.var_res_id.get().strip()
        if not identificador:
            raise ValidationError("Debe indicar el identificador de la reserva.")
        reserva = self.sistema.buscar_reserva(identificador)
        if reserva is None:
            raise AppError(f"No se encontro la reserva {identificador}.")
        return reserva

    def _limpiar_cliente(self) -> None:
        self.var_cli_id.set("")
        self.var_cli_nombre.set("")
        self.var_cli_doc.set("")
        self.var_cli_correo.set("")
        self.var_cli_tel.set("")

    def _limpiar_servicio(self) -> None:
        self.var_ser_tipo.set("Sala")
        self.var_ser_id.set("")
        self.var_ser_nombre.set("")
        self.var_ser_tarifa.set("")
        self.var_ser_extra.set("")
        self._actualizar_etiqueta_extra()

    def _limpiar_reserva(self) -> None:
        self.var_res_id.set("")
        self.var_res_cli.set("")
        self.var_res_ser.set("")
        self.var_res_horas.set("")
        self.var_res_impuesto.set("0.19")
        self.var_res_descuento.set("0")
        self.var_res_motivo.set("")

    def _set_estado(self, texto: str) -> None:
        self.var_estado.set(texto)

    def _refrescar_clientes(self) -> None:
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        for cliente in self.sistema.clientes:
            self.tree_clientes.insert(
                "",
                END,
                values=(
                    cliente.identificador,
                    cliente.nombre,
                    cliente.documento,
                    cliente.correo,
                    cliente.telefono,
                ),
            )

    def _refrescar_servicios(self) -> None:
        for item in self.tree_servicios.get_children():
            self.tree_servicios.delete(item)
        for servicio in self.sistema.servicios:
            if isinstance(servicio, ServicioSala):
                detalle = f"Capacidad {servicio.capacidad}"
                tipo = "Sala"
            elif isinstance(servicio, ServicioEquipo):
                detalle = f"Cantidad {servicio.cantidad}"
                tipo = "Equipo"
            else:
                detalle = f"Especialidad {servicio.especialidad}"
                tipo = "Asesoria"
            self.tree_servicios.insert(
                "",
                END,
                values=(
                    servicio.identificador,
                    servicio.nombre,
                    tipo,
                    detalle,
                    f"{servicio.tarifa_base:.2f}",
                ),
            )

    def _refrescar_reservas(self) -> None:
        for item in self.tree_reservas.get_children():
            self.tree_reservas.delete(item)
        for reserva in self.sistema.reservas:
            self.tree_reservas.insert(
                "",
                END,
                values=(
                    reserva.identificador,
                    reserva.cliente.identificador,
                    reserva.servicio.identificador,
                    f"{reserva.horas:.2f}",
                    reserva.estado,
                    f"{reserva.total:.2f}",
                ),
            )

    def _refrescar_logs(self) -> None:
        self.txt_logs.delete("1.0", END)
        if LOG_FILE.exists():
            contenido = LOG_FILE.read_text(encoding="utf-8")
            self.txt_logs.insert(END, contenido)
            self.txt_logs.see(END)
        else:
            self.txt_logs.insert(END, "Aun no hay registros de log.\n")

    def _actualizar_resumen(self) -> None:
        self.var_resumen.set(
            f"Clientes: {len(self.sistema.clientes)} | "
            f"Servicios: {len(self.sistema.servicios)} | "
            f"Reservas: {len(self.sistema.reservas)}"
        )

    def _actualizar_todo(self) -> None:
        self._actualizar_resumen()
        self._refrescar_clientes()
        self._refrescar_servicios()
        self._refrescar_reservas()
        self._refrescar_logs()

    def _abrir_log(self) -> None:
        if not LOG_FILE.exists():
            messagebox.showwarning("Logs", "Todavia no existe el archivo de log.", parent=self.root)
            return
        try:
            import os

            os.startfile(str(LOG_FILE))  # type: ignore[attr-defined]
        except Exception as error:
            registrar_excepcion("Abrir log", error)
            messagebox.showerror("Error", f"No fue posible abrir el log: {error}", parent=self.root)


def ejecutar_interfaz() -> None:
    raiz = tk.Tk()
    InterfazFJ(raiz)
    raiz.mainloop()
