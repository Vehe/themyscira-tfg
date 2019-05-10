FROM python:3.7
LABEL maintainer="Pablo Chueca vehedev@gmail.com"

# Establecemos las variables de entorno para la conexión con la base de datos.
ENV DB_NAME themyscira
ENV DB_USER postgres
ENV DB_PASSWORD password
ENV DB_HOST 127.0.0.1
ENV CORREO_PW password
ENV CORREO_HOST example@example.com

# Instalación de los paquetes necesarios para el funcionamiento, creamos la base de datos que vamos a usar.
RUN apt-get update -y && \
    apt-get install -y build-essential libssl-dev libffi-dev python-dev git postgresql postgresql-contrib && \
    mkdir /tfg

# Copiamos el código a la carpeta tfg y establecemos esta como directorio de trabajo.
COPY . /tfg/
WORKDIR /tfg

# Instalamos los paquetes necesarios para python y creamos las tablas en la base de datos.
RUN pip install -r requirements.txt

# Indicamos que vamos a exponer el puerto 80.
EXPOSE 80/tcp

# Al crear el container se inicia la base de datos, creando la base de datos y cargandole los datos, a su vez, se iniciar le servidor web.
ENTRYPOINT service postgresql start && \
    runuser -u postgres -- /usr/bin/psql -c "CREATE DATABASE themyscira;" && \
    runuser -u postgres -- /usr/bin/psql -c "ALTER USER postgres WITH PASSWORD 'password';" && \
    python manage.py migrate && python manage.py runscript loadData && \
    python manage.py runserver 0.0.0.0:80
