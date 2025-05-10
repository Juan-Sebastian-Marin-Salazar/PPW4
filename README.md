# PPW4
Proyecto 4 de Programacion Web

Equipo de desarrollo “No compila”:

Zavalza Covarrubias Edgar Enrique

Telles Castro Jose Ricardo

Marin Salazar Juan Sebastian

Estrada Bustos Miguel Angel

===========================================================================

Requisitos de la aplicación:

Requisito 1.- Tener visual studio code

Requisito 2.- Tener las extenciones necesarias 
(GitHub Pull Requests, Live Server) y lenguajes requeridos (Python)

Requisito 3.- Tener instaladas las siguientes librerias de Python: Flask, 
FLask-Login, FLask-MySQLdb, FLask-WTF, Jinja2, MarkupSafe, WTForms, 
Werkzeug, blinker, click, colorama, itsdangerous, mysqlclient, pip

Requisito 4.- Tener un navegador

Requisito 5.- Tener MYSQL

===========================================================================

Instrucciones de instalacion nuestro sitio web:

Paso 1.- Clonar el repositorio: 
https://github.com/Juan-Sebastian-Marin-Salazar/PPW4.git

Paso 2.- En MYSQL ejecutar el script llamado: 
scripts.sql de la carpeta 'PPW4\database\scripts.sql'

Paso 3.- Despues de ejecutar ese script, ir al archivo llamado: 
config.py en la carpeta 'PPW4\app\config.py' y cambiar el campo MYSQL_PASSWORD = "su_contrasena"

paso 4.- Ejecutar el app.py que se encuentra en la direccion 'PPW4\app\app.py'

===========================================================================

Uso de nuestro sitio web:

- Para utilizar nuestro sitio como usuario comun se tienen dos cuentas precargadas

email: Edgar@gmail.com  password: 123

email: Sebastian@gmail.com  password: 123

- Para utilizarla como Trabajador/Worker

email: Ricardo@gmail.com  password: 123

- Para utilizarla como administrador/admin

email: Miguel@gmail.com  password: 123


Los trabajadores y administradores tienen opciones que no tiene un usuario comun:

- Un usuario comun puede realizar crear carritos y realizar compras.
- Un trabajador puede realizar todas las operaciones de un usuario comun, más poder realizar entregas de ordenes.
- Un administrador puede realizar todas las operaciones de un trabajador, más agregar platillos a la base de datos.
