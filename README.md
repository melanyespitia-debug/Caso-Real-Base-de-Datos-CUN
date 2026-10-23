# Sistema CUN — Mesa de Ayuda TI

Proyecto académico en Python y SQLite para registrar estudiantes, docentes y tickets de soporte técnico, aplicando Programación Orientada a Objetos.

## Requisitos
- Python 3 instalado.
- No requiere instalar librerías externas: utiliza `sqlite3`, incluido en Python.

## Archivos
- `main.py`: clases, menú, operaciones de registro y consultas.
- `cun_sistema.db`: base de datos SQLite creada al ejecutar el programa.
- `README.md`: instrucciones del proyecto.

## Cómo ejecutar
1. Descargue o clone el repositorio.
2. Abra una terminal en la carpeta del proyecto.
3. Ejecute:

   ```bash
   python main.py
   ```

4. El programa creará `cun_sistema.db` automáticamente y mostrará un menú de opciones.

## Funcionalidades
1. Registrar estudiantes.
2. Registrar docentes.
3. Crear tickets de soporte, vinculados a un estudiante y opcionalmente a un docente.
4. Consultar estudiantes, docentes y tickets.

## Conceptos de POO aplicados
- **Encapsulamiento:** los atributos se definen como privados con doble guion bajo (`__atributo`) y se consultan mediante propiedades.
- **Herencia:** `Estudiante` y `Docente` heredan de la clase `Persona`.
- **Composición/relación entre objetos:** `TicketSoporte` se vincula con un estudiante y puede tener un docente asignado mediante sus identificadores; la base de datos asegura la integridad referencial con claves foráneas.
- **Persistencia:** las clases guardan y consultan datos usando el módulo `sqlite3` y consultas parametrizadas.

## Estructura de la base de datos
- `estudiantes`: código, nombre, programa y promedio.
- `docentes`: código, nombre, área y correo.
- `tickets_soporte`: estudiante, docente opcional, categoría, descripción y estado.

Estados permitidos para un ticket: `ABIERTO`, `EN PROCESO` y `CERRADO`.


