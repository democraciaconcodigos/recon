recon
=====

Reconocimiento de imágenes para el proyecto Democracia con Códigos


Instalacion
===========

Armar el entorno:

> apt-get install python-skimage

> apt-get install python-sklearn

> mkvirtualenv recon

> workon recon

> pip install numpy


Como Trabajar
=============

Obtener los últimos cambios:

> git pull

> pip install -r requirements.txt

> python manage.py migrate

Si la migracion se queja por tablas ya creadas, por ejemplo, para el modulo tgp, usar

> python manage.py migrate tgp --fake 
 


Branchear desde master:

> git checkout -b nombre_de_branch

> git add nuevo_archivo_o_modificado

> git commit -m "mensaje"

> git push origin nombre_de_branch


