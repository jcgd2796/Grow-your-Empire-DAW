#! /bin/sh
gunicorn --certfile=cert.pem --keyfile=privkey.pem TFM.wsgi -b 192.168.4.130:10443 --access-logfile "-"
