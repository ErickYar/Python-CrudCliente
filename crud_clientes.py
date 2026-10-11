"""
Proyecto: CRUD de clientes con MySQL
Autor: erick yarleque
Descripción: Sistema de gestión de clientes (Crear, Leer, Actualizar, Eliminar)
usando Python, POO y MySQL.
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()


class ClienteDB:
    """Clase que maneja la conexión y operaciones CRUD sobre la tabla clientes."""

    def __init__(self, host, usuario, password, base_datos):
        self.config = {
            "host": host,
            "user": usuario,
            "password": password,
            "database": base_datos,
        }

    def conectar(self):
        """Establece la conexión con MySQL."""
        try:
            conexion = mysql.connector.connect(**self.config)
            return conexion
        except Error as e:
            print(f"❌ Error de conexión: {e}")
            return None

    def crear_cliente(self, nombre, correo, telefono):
        """Inserta un nuevo cliente."""
        conexion = self.conectar()
        if not conexion:
            return
        try:
            cursor = conexion.cursor()
            sql = "INSERT INTO clientes (nombre, correo, telefono) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nombre, correo, telefono))
            conexion.commit()
            print(f"✅ Cliente '{nombre}' registrado con ID {cursor.lastrowid}.")
        except Error as e:
            print(f"❌ Error al insertar: {e}")
        finally:
            cursor.close()
            conexion.close()

    def listar_clientes(self):
        """Devuelve todos los clientes."""
        conexion = self.conectar()
        if not conexion:
            return []
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, correo, telefono FROM clientes")
            resultados = cursor.fetchall()
            print(f"\n📋 {len(resultados)} cliente(s) encontrado(s):")
            for fila in resultados:
                print(f"  ID: {fila[0]} | {fila[1]} | {fila[2]} | {fila[3]}")
            return resultados
        except Error as e:
            print(f"❌ Error al listar: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()

    def actualizar_cliente(self, id_cliente, nombre, correo, telefono):
        """Actualiza los datos de un cliente existente."""
        conexion = self.conectar()
        if not conexion:
            return
        try:
            cursor = conexion.cursor()
            sql = """UPDATE clientes
                     SET nombre = %s, correo = %s, telefono = %s
                     WHERE id = %s"""
            cursor.execute(sql, (nombre, correo, telefono, id_cliente))
            conexion.commit()
            if cursor.rowcount:
                print(f"✅ Cliente con ID {id_cliente} actualizado.")
            else:
                print(f"⚠️ No existe cliente con ID {id_cliente}.")
        except Error as e:
            print(f"❌ Error al actualizar: {e}")
        finally:
            cursor.close()
            conexion.close()

    def eliminar_cliente(self, id_cliente):
        """Elimina un cliente por ID."""
        conexion = self.conectar()
        if not conexion:
            return
        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = %s", (id_cliente,))
            conexion.commit()
            if cursor.rowcount:
                print(f"✅ Cliente con ID {id_cliente} eliminado.")
            else:
                print(f"⚠️ No existe cliente con ID {id_cliente}.")
        except Error as e:
            print(f"❌ Error al eliminar: {e}")
        finally:
            cursor.close()
            conexion.close()


def menu():
    """Menú interactivo por consola."""
    db = ClienteDB(
    host=os.getenv("DB_HOST", "localhost"),
    usuario=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD"),   # nunca en el código
    base_datos=os.getenv("DB_NAME", "empresa_db"),
)
    while True:
        print("\n=== GESTIÓN DE CLIENTES ===")
        print("1. Registrar cliente")
        print("2. Listar clientes")
        print("3. Actualizar cliente")
        print("4. Eliminar cliente")
        print("5. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre: ")
            correo = input("Correo: ")
            telefono = input("Teléfono: ")
            db.crear_cliente(nombre, correo, telefono)
        elif opcion == "2":
            db.listar_clientes()
        elif opcion == "3":
            id_cliente = int(input("ID del cliente: "))
            nombre = input("Nuevo nombre: ")
            correo = input("Nuevo correo: ")
            telefono = input("Nuevo teléfono: ")
            db.actualizar_cliente(id_cliente, nombre, correo, telefono)
        elif opcion == "4":
            id_cliente = int(input("ID del cliente a eliminar: "))
            db.eliminar_cliente(id_cliente)
        elif opcion == "5":
            print("👋 Saliendo del sistema...")
            break
        else:
            print("⚠️ Opción no válida.")


if __name__ == "__main__":
    menu()