# Createing a Super User
python manage.py createsuperuser

# Running the Server
gunicorn runs the server for linux, uvicorn for windows.
`<gunicorn|uvicorn> cytherapi.asgi:application`

`uvicorn cytherapi.asgi:application --port 5000 --reload`
`uvicorn cytherapi.asgi:application --ssl-certfile .\certs\cyther.local.pem --ssl-keyfile .\certs\cyther.local-key.pem --port 5000 --timeout-keep-alive 30 --ws-ping-timeout 15`


HTTP: Not supported anymore.
`python manage.py runserver`


HTTPS: First, you need self signed certs.

When that is finished (below), run the server with:
`python manage.py runserver_plus --cert-file=certs\cyther.local.pem --key-file=D:.\certs\cyther.local-key.pem 5000`

Access the admin page via `https://cyther.local:5000/admin`

# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser