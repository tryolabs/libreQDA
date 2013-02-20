[LibreQDA](https://github.com/tryolabs/libreQDA)
================================================

Instalación
===========

[Virtualenv](https://pypi.python.org/pypi/virtualenv)
------------------------------------------------------
Para mayor comodidad se recomienda utilizar un virtualenv.

1. Instalar Virtualenv: (`sudo apt-get install virtualenv` en Debian/Ubuntu).
2. Una vez instalado, crear un Virtualenv: `virtualenv libreqda`.
3. Activar el Virtualenv: `cd libreqda` y luego `source bin/activate`.

Obtener el código
-----------------
Antes que nada, debemos obtener el código de LibreQDA: `git clone https://github.com/tryolabs/libreQDA.git`.

Dependencias
------------
Antes de poder comenzar es necesario instalar algunas dependencias.

1. Instalar `build-essential`: `sudo apt-get install build-essential`.
2. Instalar MySQL: `sudo apt-get install mysql-server libmysqlclient-dev`.
3. El archivo `requirements.txt` contiene una lista de dependencias a instalar. Es posible instalar todas de forma automática con el comando `pip install -r requirements.txt`.

Python-docx
-----------
Para poder extraer el texto de archivos ``docx` es necesario instalar `python-docx`.

1. Obtener el código desde su [repositorio en Github](https://github.com/mikemaccana/python-docx): `git clone https://github.com/mikemaccana/python-docx.git`.
2. Ir al directorio con el código: `cd python-docx`.
3. Instalar con: `python setup.py install`.

Configurar y ejecutar
---------------------
1. Crear una base de datos para LibreQDA.
2. Copiar el archivo `local_settings.py.template` que se encuentra junto al código a `local_settings.py`.
3. Abrir el nuevo archivo, `local_settings.py` y editar según sea necesario.
4. Crear la base de datos con django: `python manage.py syncdb`.
5. Ejecutar con: `python manage.py runserver`
