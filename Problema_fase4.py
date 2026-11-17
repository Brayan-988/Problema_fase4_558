"""
Sistema integral orientado a objetos Software FJ
"""
# Curso: Programación
# Institucion UNAD
# Grupo: 558
# Integrantes: Brayan Steven Morales-Sebastian Zamora Cuervo

from abc import ABC, abstractmethod
import logging

# Configuración de logs

logging.basicConfig(
    filename='sistema_software_fj.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    encoding='utf-8'
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
        self._identificador = identificador

    @property
    def identificador(self) -> str:
        return self._identificador

    @abstractmethod
    def obtener_detalles(self) -> str:
        pass

# Clase Cliente

class Cliente(EntidadBase):
    def __init__(self, documento_cliente: str, nombre: str, correo: str, telefono: str):

        if not documento_cliente or not documento_cliente.isdigit():
            raise ClienteInvalidoError("El documento debe contener números.")

        super().__init__(documento_cliente)

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre inválido: '{valor}'. Debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise ClienteInvalidoError(f"Correo inválido: '{valor}'. Falta '@' o dominio.")
        self._correo = valor.strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not valor.isdigit() or len(valor) < 7:
            raise ClienteInvalidoError(f"Teléfono inválido: '{valor}'. Debe contener solo dígitos (mín. 7).")
        self._telefono = valor.strip()

    def obtener_detalles(self) -> str:
        return f"Cliente [documento: {self.identificador}, Nombre: {self.nombre}, Correo: {self.correo}, Teléfono: {self.telefono}]"



 
# CLASE ABSTRACTA SERVICIO


class Servicio(EntidadBase):

    def __init__(self, identificador, nombre, precio_base):
        super().__init__(identificador)

        if not isinstance(precio_base, (int, float)) or precio_base <= 0:
            raise ServicioNoDisponibleError("El precio debe ser mayor a cero.")

        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self, cantidad):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_parametros(self, cantidad):
        pass

    def obtener_detalles(self):
        return self.describir_servicio()



# SERVICIO DE RESERVA DE SALAS

class ReservaSala(Servicio):

    def validar_parametros(self, cantidad):
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            raise ServicioNoDisponibleError("Las horas deben ser mayores a cero.")

    def calcular_costo(self, cantidad, descuento=0):
        self.validar_parametros(cantidad)

        if not 0 <= descuento <= 100:
            raise ValueError("Descuento inválido.")

        total = self.precio_base * cantidad
        return total - (total * descuento / 100)

    def describir_servicio(self):
        return f"Sala: {self.nombre} - Precio por hora: ${self.precio_base}"



# SERVICIO DE ALQUILER DE EQUIPOS

class AlquilerEquipo(Servicio):

    def validar_parametros(self, cantidad):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ServicioNoDisponibleError("La cantidad de equipos debe ser positiva.")

    def calcular_costo(self, cantidad, descuento=0):
        self.validar_parametros(cantidad)

        if not 0 <= descuento <= 100:
            raise ValueError("Descuento inválido.")

        total = self.precio_base * cantidad
        return total - (total * descuento / 100)

    def describir_servicio(self):
        return f"Equipo: {self.nombre} - Precio por unidad: ${self.precio_base}"



# SERVICIO DE ASESORÍAS ESPECIALIZADAS


class Asesoria(Servicio):

    def validar_parametros(self, cantidad):
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            raise ServicioNoDisponibleError("Las horas de asesoría deben ser positivas.")

    def calcular_costo(self, cantidad, descuento=0):
        self.validar_parametros(cantidad)

        if not 0 <= descuento <= 100:
            raise ValueError("Descuento inválido.")

        total = self.precio_base * cantidad
        return total - (total * descuento / 100)

    def describir_servicio(self):
        return f"Asesoría: {self.nombre} - Precio por hora: ${self.precio_base}"


# ==========================================
# CLASE RESERVA
# ==========================================

class Reserva(EntidadBase):

    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)

        if not isinstance(cliente, Cliente):
            raise ReservaError("Debe seleccionar un cliente válido.")

        if not isinstance(servicio, Servicio):
            raise ReservaError("Debe seleccionar un servicio válido.")

        servicio.validar_parametros(duracion)

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    def confirmar(self):
        if self.estado != "Pendiente":
            raise ReservaError("La reserva no se puede confirmar.")

        self.estado = "Confirmada"
        logging.info(f"Reserva {self.identificador} confirmada.")

    def cancelar(self):
        if self.estado == "Cancelada":
            raise ReservaError("La reserva ya fue cancelada.")

        self.estado = "Cancelada"
        logging.info(f"Reserva {self.identificador} cancelada.")
    

    def procesar(self):
        try:
            if self.estado != "Confirmada":
                raise ReservaError("La reserva debe estar confirmada.")

            costo = self.servicio.calcular_costo(self.duracion)
            logging.info(f"Reserva procesada. Total: ${costo}")
            return costo

        except Exception as e:
            logging.error(f"Error al procesar reserva: {e}")
            raise ReservaError("No fue posible procesar la reserva.") from e

    def obtener_detalles(self):
        return (
            f"Reserva: {self.identificador} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Duración: {self.duracion} | "
            f"Estado: {self.estado}"
        )


# CLASE PRINCIPAL DE GESTIÓN


class GestionSoftwareFJ:

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def agregar_cliente(self, cliente):
        try:
            if not isinstance(cliente, Cliente):
                raise ClienteInvalidoError("Cliente no válido.")

            if any(c.identificador == cliente.identificador
                   for c in self.clientes):
                raise ClienteInvalidoError("El cliente ya existe.")

            self.clientes.append(cliente)
            logging.info("Cliente registrado correctamente.")

        except ClienteInvalidoError as e:
            logging.error(f"Error al registrar cliente: {e}")
            raise

    def agregar_servicio(self, servicio):
        try:
            if not isinstance(servicio, Servicio):
                raise SoftwareFJError("Servicio no válido.")

            self.servicios.append(servicio)
            logging.info("Servicio registrado correctamente.")

        except SoftwareFJError as e:
            logging.error(f"Error al registrar servicio: {e}")
            raise

    def agregar_reserva(self, reserva):
        if not isinstance(reserva, Reserva):
            raise ReservaError("Reserva no válida.")

        self.reservas.append(reserva)
        logging.info("Reserva registrada correctamente.")

    def mostrar_clientes(self):
        for cliente in self.clientes:
            print(cliente.obtener_detalles())

    def mostrar_servicios(self):
        for servicio in self.servicios:
            print(servicio.describir_servicio())

    def mostrar_reservas(self):
        for reserva in self.reservas:
            print(reserva.obtener_detalles())


# Módulo de entrada de cliente

def solicitar_cliente_interactivo(sistema: GestionSoftwareFJ):
    """
    Solicita los datos del cliente por consola, los valida mediante las propiedades
    de la clase Cliente y maneja las excepciones en caso de datos erróneos.
    """
    
    print(" REGISTRO INTERACTIVO DE NUEVO CLIENTE - SOFTWARE FJ")
   
    
    try:
        documento_cli = input("Ingrese Documento del cliente (ej. 885965): ").strip()
        nombre = input("Ingrese Nombre Completo (mín. 3 caracteres): ").strip()
        correo = input("Ingrese Correo Electrónico (ej. usuario@email.com): ").strip()
        telefono = input("Ingrese Teléfono (solo números, mín. 7 dígitos): ").strip()
        
        # Al instanciar, los setters de la clase Cliente validan automáticamente los datos
        nuevo_cliente = Cliente(documento_cli, nombre, correo, telefono)
        
        # Si la validación es exitosa, se agrega a la lista interna del sistema
        sistema.agregar_cliente(nuevo_cliente)
        
        print("\n[ÉXITO] ¡Cliente validado y registrado correctamente!")
        print(f"  -> {nuevo_cliente.obtener_detalles()}")
        logging.info(f"Cliente registrado interactivamente: {nuevo_cliente.identificador}")
        
    except Exception as e:
        print(f"\n[ERROR INESPERADO] Ocurrió un fallo en el ingreso: {e}")
        logging.error(f"Error inesperado al registrar cliente: {e}", exc_info=True)

    else:
        print("\n[ELSE] El proceso terminó sin errores.")

    finally:
        print("[ESTABLE] Fin del proceso de registro de cliente.\n")



# Ejecucion del sistema

if __name__ == "__main__":

    sistema = GestionSoftwareFJ()

    print("\n===== SISTEMA SOFTWARE FJ =====")

    # OPERACIÓN 1: Registrar un cliente
    cliente1 = Cliente("12345", "Sebastian", "sebastian@gmail.com", "3001234567")
    sistema.agregar_cliente(cliente1)
    print("1. Cliente registrado.")

    # OPERACIÓN 2: Registrar otro cliente
    cliente2 = Cliente("67890", "Carlos", "carlos@gmail.com", "3101234567")
    sistema.agregar_cliente(cliente2)
    print("2. Segundo cliente registrado.")

    # OPERACIÓN 3: Registrar servicio de sala
    sala = ReservaSala("S01", "Sala de reuniones", 50000)
    sistema.agregar_servicio(sala)
    print("3. Servicio de sala registrado.")

    # OPERACIÓN 4: Registrar servicio de alquiler de equipos
    equipo = AlquilerEquipo("E01", "Alquiler de computadores", 30000)
    sistema.agregar_servicio(equipo)
    print("4. Servicio de equipos registrado.")

    # OPERACIÓN 5: Registrar servicio de asesoría
    asesoria = Asesoria("A01", "Asesoría informática", 80000)
    sistema.agregar_servicio(asesoria)
    print("5. Servicio de asesoría registrado.")

    # OPERACIÓN 6: Crear una reserva
    reserva1 = Reserva("R01", cliente1, sala, 2)
    sistema.agregar_reserva(reserva1)
    print("6. Reserva creada.")

    # OPERACIÓN 7: Confirmar la reserva
    reserva1.confirmar()
    print("7. Reserva confirmada.")

    # OPERACIÓN 8: Calcular el costo de un servicio
    costo = sala.calcular_costo(2)
    print(f"8. Costo de reserva de sala: ${costo}")

    # OPERACIÓN 9: Calcular un servicio con descuento
    costo_descuento = asesoria.calcular_costo(2, 10)
    print(f"9. Costo de asesoría con descuento: ${costo_descuento}")

    # OPERACIÓN 10: Intentar crear una reserva con duración inválida
    try:
        reserva_error = Reserva("R02", cliente2, equipo, 0)
        sistema.agregar_reserva(reserva_error)

    except (ReservaError, ServicioNoDisponibleError) as e:
        print(f"10. Error controlado correctamente: {e}")

    print("\n===== RESUMEN DEL SISTEMA =====")
    sistema.mostrar_clientes()
    sistema.mostrar_servicios()
    sistema.mostrar_reservas()
