"""
Sistema integral orientado a objetos Software FJ
"""
# Curso: Programación
# Institucion UNAD
# Grupo: 558
# Integrantes: Brayan Steven Morales - Juan Sebastian Zamora

from abc import ABC, abstractmethod
import logging
import re
import tkinter as tk
from tkinter import messagebox, ttk

# Configuración de logs
logging.basicConfig(
    filename="sistema_software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    encoding="utf-8",
)


# Excepciones personalizadas
class SoftwareFJError(Exception):
    pass


class ClienteInvalidoError(SoftwareFJError):
    pass


class ServicioNoDisponibleError(SoftwareFJError):
    pass


class ReservaError(SoftwareFJError):
    pass


# 3. Clase abstracta base
class EntidadBase(ABC):
    def __init__(self, identificador: str):
        if not identificador or not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("El identificador no puede estar vacío.")
        self._identificador = identificador.strip()

    @property
    def identificador(self) -> str:
        return self._identificador

    @abstractmethod
    def obtener_detalles(self) -> str:
        pass


# Clase Cliente
class Cliente(EntidadBase):
    def __init__(self, documento_cliente: str, nombre: str, correo: str, telefono: str):
        try:
            super().__init__(documento_cliente)
        except ValueError as e:
            raise ClienteInvalidoError(f"Documento de cliente inválido: {e}") from e
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(
                f"Nombre inválido: '{valor}'. Debe tener al menos 3 caracteres."
            )
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not valor or not isinstance(valor, str) or not re.match(patron, valor.strip()):
            raise ClienteInvalidoError(
                f"Correo inválido: '{valor}'. Formato esperado: usuario@dominio.com."
            )
        self._correo = valor.strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if (
            not valor
            or not isinstance(valor, str)
            or not valor.strip().isdigit()
            or len(valor.strip()) < 7
        ):
            raise ClienteInvalidoError(
                f"Teléfono inválido: '{valor}'. Debe contener solo dígitos (mín. 7)."
            )
        self._telefono = valor.strip()

    def obtener_detalles(self) -> str:
        return (
            f"Cliente [Documento: {self.identificador}, Nombre: {self.nombre}, "
            f"Correo: {self.correo}, Teléfono: {self.telefono}]"
        )


# Clase Servicio y Especializados
class Servicio(EntidadBase, ABC):
    UNIDADES_VALIDAS = ("Horas", "Días")

    def __init__(
        self,
        id_servicio: str,
        nombre_servicio: str,
        costo_base: float,
        disponible: bool = True,
    ):
        try:
            super().__init__(id_servicio)
        except ValueError as e:
            raise ServicioNoDisponibleError(f"ID de servicio inválido: {e}") from e
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base
        self.disponible = disponible

    @property
    def nombre_servicio(self) -> str:
        return self._nombre_servicio

    @nombre_servicio.setter
    def nombre_servicio(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ServicioNoDisponibleError(f"Nombre de servicio inválido: '{valor}'.")
        self._nombre_servicio = valor.strip()

    @property
    def costo_base(self) -> float:
        return self._costo_base

    @costo_base.setter
    def costo_base(self, valor: float):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or valor < 0:
            raise ServicioNoDisponibleError(
                "El costo base debe ser un número mayor o igual a cero."
            )
        self._costo_base = float(valor)

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        if not isinstance(valor, bool):
            raise ServicioNoDisponibleError("La disponibilidad debe ser booleana (True/False).")
        self._disponible = valor

    def validar_parametros(self, cantidad: int, unidad: str, descuento: float = 0.0):
        if not self.disponible:
            raise ServicioNoDisponibleError(f"Servicio '{self.nombre_servicio}' no disponible.")
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ServicioNoDisponibleError("La cantidad de tiempo debe ser un entero mayor a cero.")
        if unidad not in self.UNIDADES_VALIDAS:
            raise ServicioNoDisponibleError(
                f"Unidad inválida: '{unidad}'. Use 'Horas' o 'Días'."
            )
        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or descuento < 0
            or descuento > 100
        ):
            raise ServicioNoDisponibleError("El descuento debe estar entre 0% y 100%.")

    @abstractmethod
    def describir_servicio(self) -> str:
        pass

    @abstractmethod
    def calcular_costo(
        self,
        cantidad: int = 1,
        unidad: str = "Horas",
        aplicar_iva: bool = False,
        descuento: float = 0.0,
        **kwargs,
    ) -> float:
        pass

    def obtener_detalles(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return (
            f"Servicio [{self.identificador}] {self.nombre_servicio} "
            f"- ${self.costo_base:,.2f} ({estado})"
        )


class ReservaSalas(Servicio):
    def __init__(
        self,
        id_servicio: str,
        nombre_servicio: str,
        costo_base: float,
        capacidad: int,
        disponible: bool = True,
    ):
        super().__init__(id_servicio, nombre_servicio, costo_base, disponible)
        self.capacidad = capacidad

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @capacidad.setter
    def capacidad(self, valor: int):
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise ServicioNoDisponibleError("La capacidad de la sala debe ser mayor a cero.")
        self._capacidad = valor

    def describir_servicio(self) -> str:
        return f"Reserva de Sala: {self.nombre_servicio} (Capacidad: {self.capacidad})"

    def calcular_costo(
        self,
        cantidad: int = 1,
        unidad: str = "Horas",
        aplicar_iva: bool = True,
        descuento: float = 0.0,
        **kwargs,
    ) -> float:
        self.validar_parametros(cantidad, unidad, descuento)
        # Tarifa base por hora; 1 día equivale a 8 horas operativas
        factor_tiempo = cantidad * 8 if unidad == "Días" else cantidad
        subtotal = self.costo_base * factor_tiempo
        if descuento > 0:
            subtotal -= subtotal * (descuento / 100)
        return round(subtotal * 1.19 if aplicar_iva else subtotal, 2)


class AlquilerEquipos(Servicio):
    def __init__(
        self,
        id_servicio: str,
        nombre_servicio: str,
        costo_base: float,
        tipo_equipo: str,
        disponible: bool = True,
    ):
        super().__init__(id_servicio, nombre_servicio, costo_base, disponible)
        self.tipo_equipo = tipo_equipo

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    @tipo_equipo.setter
    def tipo_equipo(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ServicioNoDisponibleError("El tipo de equipo es obligatorio.")
        self._tipo_equipo = valor.strip()

    def describir_servicio(self) -> str:
        return f"Alquiler de Equipo: {self.nombre_servicio} (Tipo: {self.tipo_equipo})"

    def calcular_costo(
        self,
        cantidad: int = 1,
        unidad: str = "Días",
        aplicar_iva: bool = False,
        descuento: float = 0.0,
        seguro_adicional: bool = False,
        **kwargs,
    ) -> float:
        self.validar_parametros(cantidad, unidad, descuento)
        # Tarifa base por día; si se alquila por horas se fracciona en jornadas de 8 horas
        factor_tiempo = cantidad / 8 if unidad == "Horas" else cantidad
        costo_unitario = self.costo_base + (15000.0 if seguro_adicional else 0.0)
        total = costo_unitario * factor_tiempo
        if descuento > 0:
            total -= total * (descuento / 100)
        return round(total * 1.19 if aplicar_iva else total, 2)


class AsesoriasEspecializadas(Servicio):
    def __init__(
        self,
        id_servicio: str,
        nombre_servicio: str,
        costo_base: float,
        nivel: str,
        disponible: bool = True,
    ):
        super().__init__(id_servicio, nombre_servicio, costo_base, disponible)
        self.nivel = nivel

    @property
    def nivel(self) -> str:
        return self._nivel

    @nivel.setter
    def nivel(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ServicioNoDisponibleError("El nivel de asesoría es obligatorio.")
        self._nivel = valor.strip()

    def describir_servicio(self) -> str:
        return f"Asesoría: {self.nombre_servicio} (Nivel: {self.nivel})"

    def calcular_costo(
        self,
        cantidad: int = 1,
        unidad: str = "Horas",
        aplicar_iva: bool = False,
        descuento: float = 0.0,
        paquete_empresarial: bool = False,
        **kwargs,
    ) -> float:
        self.validar_parametros(cantidad, unidad, descuento)
        # Tarifa base por hora; 1 día equivale a 8 horas de consultoría
        horas_totales = cantidad * 8 if unidad == "Días" else cantidad
        total = self.costo_base * horas_totales
        if paquete_empresarial:
            total *= 0.85
        if descuento > 0:
            total -= total * (descuento / 100)
        return round(total * 1.19 if aplicar_iva else total, 2)


# Clase Reserva y Gestor Interno
class Reserva(EntidadBase):
    def __init__(
        self,
        id_reserva: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion: int,
        unidad_tiempo: str,
        *args,
        **kwargs,
    ):
        super().__init__(id_reserva)
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.unidad_tiempo = unidad_tiempo
        self.args = args
        self.kwargs = kwargs
        self.estado = "PENDIENTE"
        self.costo_calculado = 0.0

    def procesar_reserva(self):
        try:
            if self.estado == "CANCELADA":
                raise ReservaError(
                    f"No se puede procesar la reserva {self.identificador} porque está cancelada."
                )
            if not isinstance(self.cliente, Cliente) or not isinstance(self.servicio, Servicio):
                raise ReservaError("Cliente o servicio inválido en la reserva.")
            self.costo_calculado = self.servicio.calcular_costo(
                self.duracion,
                self.unidad_tiempo,
                *self.args,
                **self.kwargs,
            )
        except (ServicioNoDisponibleError, ValueError, TypeError) as e:
            error_msg = f"Fallo al calcular costo en reserva {self.identificador}: {e}"
            logging.error(error_msg, exc_info=True)
            raise ReservaError(error_msg) from e
        else:
            self.estado = "CONFIRMADA"
            logging.info(
                f"Reserva {self.identificador} confirmada. Total: ${self.costo_calculado:,.2f}"
            )
        finally:
            logging.info(
                f"Cierre de ciclo operativo para reserva {self.identificador}. Estado: {self.estado}"
            )

    def cancelar_reserva(self):
        if self.estado == "CANCELADA":
            raise ReservaError(f"La reserva {self.identificador} ya se encontraba cancelada.")
        self.estado = "CANCELADA"
        logging.warning(f"Reserva {self.identificador} cancelada por el usuario.")

    def obtener_detalles(self) -> str:
        return (
            f"Reserva [{self.identificador}] Cliente: {self.cliente.nombre} | "
            f"Serv: {self.servicio.nombre_servicio} | Tiempo: {self.duracion} {self.unidad_tiempo} | "
            f"Costo: ${self.costo_calculado:,.2f} [{self.estado}]"
        )


class GestionSoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

        # Precargar servicios iniciales
        self.servicios.append(
            ReservaSalas("SL-01", "Sala Ejecutiva Principal", 50000, 15, True)
        )
        self.servicios.append(
            AlquilerEquipos("RV-01", "Kit Realidad Virtual Pro", 30000, "Hardware", True)
        )
        self.servicios.append(
            AsesoriasEspecializadas(
                "CA-01", "Consultoría Arquitectura SW", 120000, "Senior", True
            )
        )

    def agregar_cliente(self, cliente: Cliente):
        if not isinstance(cliente, Cliente):
            raise ClienteInvalidoError("Solo se pueden agregar instancias válidas de Cliente.")
        self.clientes.append(cliente)

    def agregar_servicio(self, servicio: Servicio):
        if not isinstance(servicio, Servicio):
            raise ServicioNoDisponibleError("Solo se pueden agregar instancias válidas de Servicio.")
        self.servicios.append(servicio)

    def agregar_reserva(self, reserva: Reserva):
        if not isinstance(reserva, Reserva):
            raise ReservaError("Solo se pueden agregar instancias válidas de Reserva.")
        self.reservas.append(reserva)


def ejecutar_simulacion_operaciones(sistema: GestionSoftwareFJ) -> list[str]:
    """
    Ejecuta 10 operaciones completas (válidas e inválidas) en memoria sin base de datos,
    garantizando la continuidad ante errores y registrando los resultados en el log.
    """
    resultados = []

    def registrar(num: int, titulo: str, ok: bool, detalle: str):
        etiqueta = "EXITO" if ok else "ERROR_CONTROLADO"
        linea = f"{num:02d}. [{etiqueta}] {titulo}: {detalle}"
        resultados.append(linea)
        logging.info(f"SIMULACION | {linea}")

    # Registro válido de cliente
    try:
        cliente_valido = Cliente("10102030", "Camila Rojas", "camila.rojas@correo.co", "3105551234")
        sistema.agregar_cliente(cliente_valido)
        registrar(1, "Registro cliente válido", True, cliente_valido.obtener_detalles())
    except ClienteInvalidoError as e:
        registrar(1, "Registro cliente válido", False, str(e))

    # Registro inválido de cliente (correo y teléfono incorrectos)
    try:
        cliente_invalido = Cliente("900111", "Lu", "correo_invalido", "12a45")
        sistema.agregar_cliente(cliente_invalido)
        registrar(2, "Registro cliente inválido", True, cliente_invalido.obtener_detalles())
    except ClienteInvalidoError as e:
        registrar(2, "Registro cliente inválido", False, str(e))

    # Creación correcta de servicio
    try:
        servicio_valido = ReservaSalas("SL-02", "Sala Conferencias Norte", 75000, 25, True)
        sistema.agregar_servicio(servicio_valido)
        registrar(3, "Creación servicio válida", True, servicio_valido.describir_servicio())
    except ServicioNoDisponibleError as e:
        registrar(3, "Creación servicio válida", False, str(e))

    # Creación incorrecta de servicio (costo base negativo)
    try:
        servicio_invalido = AlquilerEquipos("EQ-ERR", "Estación Trabajo", -20000, "PC", True)
        sistema.agregar_servicio(servicio_invalido)
        registrar(4, "Creación servicio inválida", True, servicio_invalido.describir_servicio())
    except ServicioNoDisponibleError as e:
        registrar(4, "Creación servicio inválida", False, str(e))

    # Reserva exitosa de sala
    try:
        cli = sistema.clientes[0]
        res_sala = Reserva(
            "R-001", cli, sistema.servicios[0], 2, "Horas", aplicar_iva=True, descuento=5.0
        )
        res_sala.procesar_reserva()
        sistema.agregar_reserva(res_sala)
        registrar(5, "Reserva exitosa sala", True, res_sala.obtener_detalles())
    except ReservaError as e:
        registrar(5, "Reserva exitosa sala", False, str(e))

    # Reserva exitosa de alquiler de equipos
    try:
        cli = sistema.clientes[0]
        res_equipo = Reserva(
            "R-002", cli, sistema.servicios[1], 3, "Días", seguro_adicional=True
        )
        res_equipo.procesar_reserva()
        sistema.agregar_reserva(res_equipo)
        registrar(6, "Reserva exitosa equipos", True, res_equipo.obtener_detalles())
    except ReservaError as e:
        registrar(6, "Reserva exitosa equipos", False, str(e))

    # Reserva exitosa de asesoría especializada
    try:
        cli = sistema.clientes[0]
        res_asesoria = Reserva(
            "R-003", cli, sistema.servicios[2], 5, "Horas", paquete_empresarial=True
        )
        res_asesoria.procesar_reserva()
        sistema.agregar_reserva(res_asesoria)
        registrar(7, "Reserva exitosa asesoría", True, res_asesoria.obtener_detalles())
    except ReservaError as e:
        registrar(7, "Reserva exitosa asesoría", False, str(e))

    # Reserva fallida por servicio no disponible
    try:
        cli = sistema.clientes[0]
        sala_ocupada = ReservaSalas("SL-03", "Sala Auditorio", 60000, 30, False)
        res_fallida_disp = Reserva("R-004", cli, sala_ocupada, 2, "Horas")
        res_fallida_disp.procesar_reserva()
        sistema.agregar_reserva(res_fallida_disp)
        registrar(8, "Reserva servicio no disponible", True, res_fallida_disp.obtener_detalles())
    except ReservaError as e:
        registrar(8, "Reserva servicio no disponible", False, str(e))

    # Reserva fallida por duración inválida
    try:
        cli = sistema.clientes[0]
        res_fallida_dur = Reserva("R-005", cli, sistema.servicios[0], 0, "Horas")
        res_fallida_dur.procesar_reserva()
        sistema.agregar_reserva(res_fallida_dur)
        registrar(9, "Reserva duración inválida", True, res_fallida_dur.obtener_detalles())
    except ReservaError as e:
        registrar(9, "Reserva duración inválida", False, str(e))

    # Cancelación válida y reintento inválido de cancelar nuevamente
    try:
        if sistema.reservas:
            objetivo = sistema.reservas[0]
            objetivo.cancelar_reserva()
            try:
                objetivo.cancelar_reserva()
            except ReservaError as e_reintento:
                registrar(
                    10,
                    "Cancelación y reintento bloqueado",
                    True,
                    f"Cancelada '{objetivo.identificador}'; doble cancelación rechazada: {e_reintento}",
                )
        else:
            registrar(10, "Cancelación de reserva", False, "No existen reservas para cancelar.")
    except ReservaError as e:
        registrar(10, "Cancelación de reserva", False, str(e))

    return resultados


# Interfaz Gráfica con Tkinter (Tema Oscuro + Selección Horas/Días + Cancelación)
class AppSoftwareFJGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Integral de Gestión")
        self.root.geometry("880x680")
        self.root.minsize(750, 580)

        # Paleta de colores Tema Oscuro (Dark Mode)
        self.bg_principal = "#121212"
        self.bg_secundario = "#1E1E1E"
        self.bg_input = "#2C2C2C"
        self.fg_texto = "#F3F4F6"
        self.fg_secundario = "#9CA3AF"
        self.acento_azul = "#2563EB"
        self.acento_azul_hover = "#1D4ED8"
        self.acento_rojo = "#DC2626"
        self.acento_rojo_hover = "#B91C1C"

        self.root.configure(bg=self.bg_principal)
        self.sistema = GestionSoftwareFJ()

        self.configurar_estilos_oscuros()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self.crear_pestana_clientes()
        self.crear_pestana_reservas()

    def configurar_estilos_oscuros(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure("TFrame", background=self.bg_principal)
        self.style.configure(
            "TLabel", background=self.bg_principal, foreground=self.fg_texto, font=("Roboto UI", 10)
        )
        self.style.configure(
            "Title.TLabel",
            background=self.bg_principal,
            foreground="#60A5FA",
            font=("Roboto UI", 12, "bold"),
        )

        self.style.configure(
            "TLabelframe", background=self.bg_secundario, bordercolor="#374151", relief="solid"
        )
        self.style.configure(
            "TLabelframe.Label",
            background=self.bg_secundario,
            foreground="#93C5FD",
            font=("Roboto UI", 10, "bold"),
        )

        self.style.configure("TNotebook", background=self.bg_principal, borderwidth=0)
        self.style.configure(
            "TNotebook.Tab",
            background=self.bg_secundario,
            foreground=self.fg_secundario,
            padding=[15, 6],
            font=("Roboto UI", 10, "bold"),
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", self.acento_azul)],
            foreground=[("selected", "#FFFFFF")],
        )

        self.style.configure(
            "TEntry",
            fieldbackground=self.bg_input,
            foreground=self.fg_texto,
            insertcolor=self.fg_texto,
            bordercolor="#4B5563",
        )
        self.style.configure(
            "TCombobox",
            fieldbackground=self.bg_input,
            background=self.bg_secundario,
            foreground=self.fg_texto,
            arrowcolor=self.fg_texto,
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.bg_input)],
            selectbackground=[("readonly", self.acento_azul)],
            selectforeground=[("readonly", "#FFFFFF")],
        )

        self.style.configure(
            "Primary.TButton",
            background=self.acento_azul,
            foreground="#FFFFFF",
            font=("Roboto UI", 10, "bold"),
            padding=6,
            borderwidth=0,
        )
        self.style.map("Primary.TButton", background=[("active", self.acento_azul_hover)])

        self.style.configure(
            "Danger.TButton",
            background=self.acento_rojo,
            foreground="#FFFFFF",
            font=("Roboto UI", 10, "bold"),
            padding=6,
            borderwidth=0,
        )
        self.style.map("Danger.TButton", background=[("active", self.acento_rojo_hover)])

    def crear_pestana_clientes(self):
        pestana = ttk.Frame(self.notebook)
        self.notebook.add(pestana, text=" Gestión de clientes ")

        lbl_titulo = ttk.Label(
            pestana, text="Registro y validación de clientes", style="Title.TLabel"
        )
        lbl_titulo.pack(pady=12)

        frm_form = ttk.LabelFrame(pestana, text=" Datos del cliente ")
        frm_form.pack(fill="x", padx=20, pady=5)

        lbl_style_interno = {
            "background": self.bg_secundario,
            "foreground": self.fg_texto,
            "font": ("Roboto UI", 10),
        }

        tk.Label(frm_form, text="Documento del cliente:", **lbl_style_interno).grid(
            row=0, column=0, sticky="w", padx=12, pady=6
        )
        self.txt_doc = ttk.Entry(frm_form, width=32)
        self.txt_doc.grid(row=0, column=1, padx=12, pady=6)

        tk.Label(frm_form, text="Nombre completo:", **lbl_style_interno).grid(
            row=1, column=0, sticky="w", padx=12, pady=6
        )
        self.txt_nombre = ttk.Entry(frm_form, width=32)
        self.txt_nombre.grid(row=1, column=1, padx=12, pady=6)

        tk.Label(frm_form, text="Correo electrónico:", **lbl_style_interno).grid(
            row=2, column=0, sticky="w", padx=12, pady=6
        )
        self.txt_correo = ttk.Entry(frm_form, width=32)
        self.txt_correo.grid(row=2, column=1, padx=12, pady=6)

        tk.Label(frm_form, text="Teléfono:", **lbl_style_interno).grid(
            row=3, column=0, sticky="w", padx=12, pady=6
        )
        self.txt_telefono = ttk.Entry(frm_form, width=32)
        self.txt_telefono.grid(row=3, column=1, padx=12, pady=6)

        btn_registrar = ttk.Button(
            frm_form,
            text="Validar y registrar cliente",
            style="Primary.TButton",
            command=self.registrar_cliente_gui,
        )
        btn_registrar.grid(row=4, column=0, columnspan=2, pady=14)

        frm_lista = ttk.LabelFrame(pestana, text=" Clientes registrados en listas internas ")
        frm_lista.pack(fill="both", expand=True, padx=20, pady=10)

        self.listbox_clientes = tk.Listbox(
            frm_lista,
            height=8,
            bg=self.bg_input,
            fg=self.fg_texto,
            selectbackground=self.acento_azul,
            selectforeground="#FFFFFF",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#374151",
            font=("Roboto", 10),
        )
        self.listbox_clientes.pack(fill="both", expand=True, padx=12, pady=12)

    def registrar_cliente_gui(self):
        try:
            doc = self.txt_doc.get().strip()
            nombre = self.txt_nombre.get().strip()
            correo = self.txt_correo.get().strip()
            tel = self.txt_telefono.get().strip()

            nuevo_cliente = Cliente(doc, nombre, correo, tel)
            self.sistema.agregar_cliente(nuevo_cliente)

            self.refrescar_lista_clientes()
            messagebox.showinfo(
                "Éxito", f"Cliente '{nombre}' validado y registrado correctamente."
            )
            logging.info(f"Cliente registrado interactivamente en GUI: {doc}")

            self.txt_doc.delete(0, tk.END)
            self.txt_nombre.delete(0, tk.END)
            self.txt_correo.delete(0, tk.END)
            self.txt_telefono.delete(0, tk.END)

        except ClienteInvalidoError as cie:
            messagebox.showerror("Error de validación", str(cie))
            logging.warning(f"Intento fallido de cliente en GUI: {cie}")
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un fallo: {e}")
            logging.error(f"Error inesperado al registrar cliente GUI: {e}", exc_info=True)

    def crear_pestana_reservas(self):
        pestana = ttk.Frame(self.notebook)
        self.notebook.add(pestana, text=" Gestión y cancelación de reservas ")

        lbl_titulo = ttk.Label(
            pestana, text="Procesamiento y control de reservas", style="Title.TLabel"
        )
        lbl_titulo.pack(pady=12)

        frm_form = ttk.LabelFrame(pestana, text=" Crear nueva reserva ")
        frm_form.pack(fill="x", padx=20, pady=5)

        lbl_style_interno = {
            "background": self.bg_secundario,
            "foreground": self.fg_texto,
            "font": ("Roboto UI", 10),
        }

        tk.Label(frm_form, text="ID Reserva:", **lbl_style_interno).grid(
            row=0, column=0, sticky="w", padx=12, pady=6
        )
        self.txt_id_reserva = ttk.Entry(frm_form, width=32)
        self.txt_id_reserva.grid(row=0, column=1, padx=12, pady=6)

        tk.Label(frm_form, text="Seleccionar cliente:", **lbl_style_interno).grid(
            row=1, column=0, sticky="w", padx=12, pady=6
        )
        self.combo_clientes = ttk.Combobox(frm_form, width=30, state="readonly")
        self.combo_clientes.grid(row=1, column=1, padx=12, pady=6)

        tk.Label(frm_form, text="Seleccionar Servicio:", **lbl_style_interno).grid(
            row=2, column=0, sticky="w", padx=12, pady=6
        )
        self.combo_servicios = ttk.Combobox(frm_form, width=30, state="readonly")
        self.combo_servicios.grid(row=2, column=1, padx=12, pady=6)
        self.combo_servicios["values"] = [s.obtener_detalles() for s in self.sistema.servicios]

        # Fila de Cantidad y Selector de Unidad (Horas / Días)
        tk.Label(frm_form, text="Cantidad de tiempo:", **lbl_style_interno).grid(
            row=3, column=0, sticky="w", padx=12, pady=6
        )

        frm_tiempo = ttk.Frame(frm_form)
        frm_tiempo.configure(style="TFrame")
        frm_tiempo.grid(row=3, column=1, sticky="w", padx=12, pady=6)

        self.txt_duracion = ttk.Entry(frm_tiempo, width=15)
        self.txt_duracion.pack(side="left", padx=(0, 8))

        self.combo_unidad = ttk.Combobox(
            frm_tiempo, width=11, values=["Horas", "Días"], state="readonly"
        )
        self.combo_unidad.pack(side="left")
        self.combo_unidad.set("Horas")

        btn_procesar = ttk.Button(
            frm_form,
            text="Procesar y confirmar reserva",
            style="Primary.TButton",
            command=self.procesar_reserva_gui,
        )
        btn_procesar.grid(row=4, column=0, columnspan=2, pady=14)

        self.notebook.bind("<<NotebookTabChanged>>", self.actualizar_combos)

        # Sección de Historial y Cancelación de Reservas
        frm_lista = ttk.LabelFrame(
            pestana, text=" Historial de reservas (Seleccione una para cancelar) "
        )
        frm_lista.pack(fill="both", expand=True, padx=20, pady=10)

        self.listbox_reservas = tk.Listbox(
            frm_lista,
            height=6,
            bg=self.bg_input,
            fg=self.fg_texto,
            selectbackground=self.acento_azul,
            selectforeground="#FFFFFF",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#374151",
            font=("Consolas", 10),
        )
        self.listbox_reservas.pack(fill="both", expand=True, padx=12, pady=(12, 6))

        frm_botones = ttk.Frame(frm_lista)
        frm_botones.configure(style="TFrame")
        frm_botones.pack(pady=(4, 12))

        btn_cancelar = ttk.Button(
            frm_botones,
            text="Cancelar reserva seleccionada",
            style="Danger.TButton",
            command=self.cancelar_reserva_gui,
        )
        btn_cancelar.pack(side="left", padx=6)

        btn_simular = ttk.Button(
            frm_botones,
            text="Simular 10 operaciones",
            style="Primary.TButton",
            command=self.simular_operaciones_gui,
        )
        btn_simular.pack(side="left", padx=6)

    def actualizar_combos(self, event=None):
        clientes_docs = [f"{c.identificador} - {c.nombre}" for c in self.sistema.clientes]
        self.combo_clientes["values"] = clientes_docs
        self.combo_servicios["values"] = [s.obtener_detalles() for s in self.sistema.servicios]

    def refrescar_lista_clientes(self):
        self.listbox_clientes.delete(0, tk.END)
        for cli in self.sistema.clientes:
            self.listbox_clientes.insert(tk.END, cli.obtener_detalles())

    def simular_operaciones_gui(self):
        resumen = ejecutar_simulacion_operaciones(self.sistema)
        self.refrescar_lista_clientes()
        self.refrescar_lista_reservas()
        self.actualizar_combos()
        messagebox.showinfo("Simulación completada", "\n".join(resumen))

    def procesar_reserva_gui(self):
        try:
            id_res = self.txt_id_reserva.get().strip()
            cliente_seleccionado = self.combo_clientes.get()
            idx_serv = self.combo_servicios.current()
            duracion_str = self.txt_duracion.get().strip()
            unidad_tiempo = self.combo_unidad.get()

            if not id_res or not cliente_seleccionado or idx_serv == -1 or not duracion_str:
                raise ReservaError("Faltan parámetros obligatorios para procesar la reserva.")

            if not duracion_str.isdigit():
                raise ValueError("La cantidad de tiempo debe ser un número entero válido.")

            duracion = int(duracion_str)
            doc_cliente = cliente_seleccionado.split(" - ")[0]
            cliente_obj = next(
                (c for c in self.sistema.clientes if c.identificador == doc_cliente), None
            )

            if not cliente_obj:
                raise ReservaError("No se encontró el cliente seleccionado.")

            servicio_obj = self.sistema.servicios[idx_serv]

            reserva = Reserva(
                id_res,
                cliente_obj,
                servicio_obj,
                duracion,
                unidad_tiempo,
                aplicar_iva=True,
                descuento=5.0,
            )
            reserva.procesar_reserva()

            self.sistema.agregar_reserva(reserva)
            self.refrescar_lista_reservas()

            messagebox.showinfo(
                "Éxito",
                f"¡Reserva {id_res} confirmada!\nCosto Total: ${reserva.costo_calculado:,.2f}",
            )
            logging.info(f"Reserva creada en GUI: {id_res}")

            self.txt_id_reserva.delete(0, tk.END)
            self.txt_duracion.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error en reserva", str(e))
            logging.error(f"Error procesando reserva en GUI: {e}", exc_info=True)

    def cancelar_reserva_gui(self):
        try:
            seleccion = self.listbox_reservas.curselection()
            if not seleccion:
                raise ReservaError(
                    "Por favor, seleccione una reserva de la lista para cancelarla."
                )

            indice = seleccion[0]
            reserva_obj = self.sistema.reservas[indice]

            confirmacion = messagebox.askyesno(
                "Confirmar cancelación",
                f"¿Está seguro que desea cancelar la reserva '{reserva_obj.identificador}' "
                f"del cliente {reserva_obj.cliente.nombre}?",
            )

            if confirmacion:
                reserva_obj.cancelar_reserva()
                self.refrescar_lista_reservas()
                messagebox.showinfo(
                    "Reserva cancelada",
                    f"La reserva {reserva_obj.identificador} ha sido cancelada correctamente.",
                )

        except ReservaError as re:
            messagebox.showwarning("Operación no permitida", str(re))
            logging.error(f"Error controlado al cancelar reserva en GUI: {re}")
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Ocurrió un error al cancelar: {e}")
            logging.error(f"Error inesperado al cancelar reserva GUI: {e}", exc_info=True)

    def refrescar_lista_reservas(self):
        self.listbox_reservas.delete(0, tk.END)
        for res in self.sistema.reservas:
            self.listbox_reservas.insert(tk.END, res.obtener_detalles())


if __name__ == "__main__":
    root = tk.Tk()
    app = AppSoftwareFJGUI(root)
    root.mainloop()