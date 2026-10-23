import sqlite3


DB_NAME = "cun_sistema.db"


def crear_base_datos_cun():
    """Crea las tablas necesarias para el sistema de soporte de la CUN."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estudiantes (
                id_estudiante TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                programa TEXT NOT NULL,
                promedio REAL DEFAULT 0.0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS docentes (
                id_docente TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                area TEXT NOT NULL,
                correo TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets_soporte (
                id_ticket INTEGER PRIMARY KEY AUTOINCREMENT,
                id_estudiante TEXT NOT NULL,
                id_docente TEXT,
                categoria TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                estado TEXT DEFAULT 'ABIERTO',
                FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
                FOREIGN KEY (id_docente) REFERENCES docentes(id_docente)
            )
        """)

        conn.commit()
    print("[Exitoso] Base de datos 'cun_sistema.db' creada correctamente.")


class Persona:
    """Clase padre para las personas registradas en el sistema."""

    def __init__(self, identificacion, nombre):
        self.__identificacion = identificacion
        self.__nombre = nombre

    @property
    def identificacion(self):
        return self.__identificacion

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        if not nuevo_nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = nuevo_nombre.strip()


class Estudiante(Persona):
    """Estudiante: hereda los datos comunes de Persona."""

    def __init__(self, id_estudiante, nombre, programa, promedio=0.0):
        super().__init__(id_estudiante, nombre)
        self.__programa = programa
        self.__promedio = float(promedio)

    @property
    def id_estudiante(self):
        return self.identificacion

    @property
    def programa(self):
        return self.__programa

    @property
    def promedio(self):
        return self.__promedio

    def guardar(self):
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            conn.execute("""
                INSERT INTO estudiantes (id_estudiante, nombre, programa, promedio)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id_estudiante) DO UPDATE SET
                    nombre=excluded.nombre,
                    programa=excluded.programa,
                    promedio=excluded.promedio
            """, (self.id_estudiante, self.nombre, self.programa, self.promedio))
            conn.commit()

    @staticmethod
    def listar():
        with sqlite3.connect(DB_NAME) as conn:
            return conn.execute("""
                SELECT id_estudiante, nombre, programa, promedio
                FROM estudiantes ORDER BY nombre
            """).fetchall()


class Docente(Persona):
    """Docente: segunda clase derivada de Persona."""

    def __init__(self, id_docente, nombre, area, correo=""):
        super().__init__(id_docente, nombre)
        self.__area = area
        self.__correo = correo

    @property
    def id_docente(self):
        return self.identificacion

    @property
    def area(self):
        return self.__area

    @property
    def correo(self):
        return self.__correo

    def guardar(self):
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                INSERT INTO docentes (id_docente, nombre, area, correo)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id_docente) DO UPDATE SET
                    nombre=excluded.nombre,
                    area=excluded.area,
                    correo=excluded.correo
            """, (self.id_docente, self.nombre, self.area, self.correo))
            conn.commit()

    @staticmethod
    def listar():
        with sqlite3.connect(DB_NAME) as conn:
            return conn.execute("""
                SELECT id_docente, nombre, area, correo
                FROM docentes ORDER BY nombre
            """).fetchall()


class TicketSoporte:
    """Ticket de soporte. Se relaciona con un estudiante y opcionalmente con un docente."""

    ESTADOS_VALIDOS = ("ABIERTO", "EN PROCESO", "CERRADO")

    def __init__(self, id_estudiante, categoria, descripcion, id_docente=None,
                 estado="ABIERTO"):
        self.__id_ticket = None
        self.__id_estudiante = id_estudiante
        self.__id_docente = id_docente
        self.__categoria = categoria
        self.__descripcion = descripcion
        estado = estado.upper()
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("Estado inválido. Use: ABIERTO, EN PROCESO o CERRADO.")
        self.__estado = estado

    @property
    def id_ticket(self):
        return self.__id_ticket

    @property
    def id_estudiante(self):
        return self.__id_estudiante

    @property
    def id_docente(self):
        return self.__id_docente

    @property
    def categoria(self):
        return self.__categoria

    @property
    def descripcion(self):
        return self.__descripcion

    @property
    def estado(self):
        return self.__estado

    def guardar(self):
        """Guarda el ticket y valida la relación con estudiante/docente mediante claves foráneas."""
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO tickets_soporte
                    (id_estudiante, id_docente, categoria, descripcion, estado)
                VALUES (?, ?, ?, ?, ?)
            """, (self.id_estudiante, self.id_docente, self.categoria,
                  self.descripcion, self.estado))
            self.__id_ticket = cursor.lastrowid
            conn.commit()
        return self.__id_ticket

    @staticmethod
    def listar():
        with sqlite3.connect(DB_NAME) as conn:
            return conn.execute("""
                SELECT t.id_ticket, e.nombre, t.categoria, t.descripcion,
                       t.estado, COALESCE(d.nombre, 'Sin asignar')
                FROM tickets_soporte AS t
                JOIN estudiantes AS e ON e.id_estudiante = t.id_estudiante
                LEFT JOIN docentes AS d ON d.id_docente = t.id_docente
                ORDER BY t.id_ticket DESC
            """).fetchall()


def mostrar_filas(titulo, filas):
    print(f"\n--- {titulo} ---")
    if not filas:
        print("No hay registros.")
        return
    for fila in filas:
        print(" | ".join(str(valor) for valor in fila))


def menu():
    crear_base_datos_cun()
    while True:
        print("""
========== SISTEMA CUN: MESA DE AYUDA ==========
1. Registrar estudiante
2. Registrar docente
3. Crear ticket de soporte
4. Consultar estudiantes
5. Consultar docentes
6. Consultar tickets
0. Salir
""")
        opcion = input("Seleccione una opción: ").strip()

        try:
            if opcion == "1":
                estudiante = Estudiante(
                    input("Código del estudiante: ").strip(),
                    input("Nombre completo: ").strip(),
                    input("Programa académico: ").strip(),
                    input("Promedio (ej. 4.2): ").strip() or 0.0
                )
                estudiante.guardar()
                print("Estudiante guardado correctamente.")

            elif opcion == "2":
                docente = Docente(
                    input("Código del docente: ").strip(),
                    input("Nombre completo: ").strip(),
                    input("Área o asignatura: ").strip(),
                    input("Correo (opcional): ").strip()
                )
                docente.guardar()
                print("Docente guardado correctamente.")

            elif opcion == "3":
                id_estudiante = input("Código del estudiante registrado: ").strip()
                id_docente = input("Código del docente asignado (Enter si no tiene): ").strip() or None
                categoria = input("Categoría (software, red, aula, equipo, otra): ").strip()
                descripcion = input("Descripción del problema: ").strip()
                ticket = TicketSoporte(id_estudiante, categoria, descripcion, id_docente)
                ticket_id = ticket.guardar()
                print(f"Ticket #{ticket_id} creado correctamente.")

            elif opcion == "4":
                mostrar_filas("ESTUDIANTES", Estudiante.listar())

            elif opcion == "5":
                mostrar_filas("DOCENTES", Docente.listar())

            elif opcion == "6":
                mostrar_filas("TICKETS DE SOPORTE", TicketSoporte.listar())

            elif opcion == "0":
                print("Programa finalizado.")
                break
            else:
                print("Opción no válida. Intente de nuevo.")

        except (ValueError, sqlite3.Error) as error:
            print(f"No se pudo completar la operación: {error}")


if __name__ == "__main__":
    menu()
