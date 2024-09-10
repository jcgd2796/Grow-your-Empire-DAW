#! /bin/sh
gunicorn --certfile=cert.pem --keyfile=privkey.pem Grow_your_empire.wsgi -b 192.168.4.130:10443 --access-logfile "-"
