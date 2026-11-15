"""
Sistema integral orientado a objetos Software FJ
"""
# Curso: Programación
# Institucion UNAD
# Grupo: 558
# Integrantes: Brayan Steven Morales

from abc import ABC, abstractmethod
from datetime import datetime
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
        
    except ClienteInvalidoError as cie:
        print(f"\n[ERROR DE VALIDACIÓN] No se pudo registrar el cliente: {cie}")
        logging.warning(f"Intento fallido de registro de cliente: {cie}")
    except Exception as e:
        print(f"\n[ERROR INESPERADO] Ocurrió un fallo en el ingreso: {e}")
        logging.error(f"Error inesperado al registrar cliente: {e}", exc_info=True)
    finally:
        print("[ESTABLE] Fin del proceso de registro de cliente.\n")



# Ejecucion del sistema

if __name__ == "__main__":
    sistema_fj = GestionSoftwareFJ()
    
    print(">>> SOFTWARE FJ INICIADO <<<")
    
    # Ejecutamos la solicitud interactiva
    solicitar_cliente_interactivo(sistema_fj)
    
    print(f"Total de clientes activos en la lista interna: {len(sistema_fj.clientes)}")