Para poder utilizar la aplicación correctamente, son necesarias las librerías de Python "django-crontab", "pymysql", y "django-nested-admin".
```
python -m pip install django-crontab
python -m pip install pymysql
python -m pip install django-nested-admin
```
Además, se debe crear un usuario de tipo administrador:
```
python3 manage.py createsuperuser
```

Una vez que se ha creado el usuario administrador, podemos acceder al área de administración (/admin) y crear nuevos usuarios.
Al crear entidades de tipo Student vinculadas a un usuario, se genera automáticamente la aldea del usuario, aunque deshabilitada.
Al estar deshabilitada, no genera recursos diariamente, aunque se puede habilitar si su propietario accede al área de gestión de su aldea (/DAWActivity/manager).

Creado para la versión 5.1 de Django ([https://docs.djangoproject.com/en/5.1/releases/5.1/]), utilizando Python 3.10.12
