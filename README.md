# Themyscira

## Desplegar una copia local
Para desplegar el proyecto de manera local tanto el servidor web, como la base de datos, debemos tener instalado docker con antelación. 
- [Como instalar Docker en Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- [Como instalar Docker en Windows](https://docs.docker.com/docker-for-windows/install/)

Yo lo realizare sobre una máquina `Ubuntu 16.04`. 
Una vez tengamos docker instalado, debemos seguir los siguientes pasos:

Primero tenemos que clonar y entrar al directorio con los siguientes comandos:
```sh
$ git clone https://github.com/Vehe/themyscira-tfg.git
$ cd themyscira-tfg
```

Ahora deberemos construir la imagen a partir del fichero `Dockerfile`, para ello, ejecutamos:
```sh
$ docker build -t themyscira .
```
Lo que hemos hecho a sido crear una imagen local con el nombre de `themyscira`, a parir de esta imagen crearemos el contenedor.

Una vez hecho esto, creamos un contenedor a parir de esta imagen con el comando:
```sh
$ docker run -d --name themyscira -p 80:80 themyscira
```
Con el parámetro `-d` le indicamos que se ejecute en detached mode, osea background, la flag `--name themyscira` se usar para darle un nombre al contenedor, esto no es obligatorio, en caso de no asignarla, se le da un nombre random.
Es importante indicar `-p 80:80`, ya que le decimos que el puerto 80 de nuestra máquina host, es el puerto 80 de la maquina guest, osea el contenedor.
Por ultimo, le indicamos la imagen a partir de la cual tiene que crear el contenedor, en este caso `themyscira`.

Si todo ha ido bien, deberíamos ver algo como lo siguiente:
```
$ docker run -d --name themyscira -p 80:80 themyscira
75a46d37b019fbd743776d478930a14037e7e99cf7472a6e82b9e02624086b58
```

Y para comprobar que está funcionando:
```
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED              STATUS              PORTS                NAMES
75a46d37b019        themyscira          "/bin/sh -c 'service"   About a minute ago   Up About a minute   0.0.0.0:80->80/tcp   themyscira
```

Podemos ver que el contenedor se está ejecutando correctamente, por lo que si abirimos nuestro navegador y vamos a `http://localhost/` deberíamos ver la página principal de la web.

## Acceder a la base de datos por comando

Si tenemos desplegada nuestra copia local del proyecto siguiendo la explicación anterior, debemos tener un contenedor llamado `themyscira`, asi que partiremos de esta base.

Podemos acceder a la base de datos que usa la web a través de comando, para ello, primero necesitamos una shell en el contenedor, ejecutaremos el siguiente comando:
```sh
$ docker exec -it themyscira bash
```

Ahora deberíamos estar dentro del container en una shell como usuario root, para acceder a la base de datos, cambiaremos al usuario `postgres`, así que ejecutamos:
```sh
# su postgres
```

Ejecutamos sobre la shell del usuario `postgres` lo siguiente:
```sh
$ psql -d themyscira
```

De esta manera entramos a la shell que nos proporciona `POSTGRESQL` directamente en la base de datos `themyscira`, que es la que usa nuestra web.
Para ver las tablas que tenemos, ejecutamos lo siguiente:
```
themyscira=# \dt
```

Deberíamos ver un resultado igual que este:
```
                   List of relations
 Schema |            Name            | Type  |  Owner
--------+----------------------------+-------+----------
 public | auth_group                 | table | postgres
 public | auth_group_permissions     | table | postgres
 public | auth_permission            | table | postgres
 public | auth_user                  | table | postgres
 public | auth_user_groups           | table | postgres
 public | auth_user_user_permissions | table | postgres
 public | django_admin_log           | table | postgres
 public | django_content_type        | table | postgres
 public | django_migrations          | table | postgres
 public | django_session             | table | postgres
 public | themyscira_autor           | table | postgres
 public | themyscira_question        | table | postgres
 public | themyscira_response        | table | postgres
 public | themyscira_timestamp       | table | postgres
 public | themyscira_video           | table | postgres
(15 rows)
```

El hecho de tener esta shell en el contenedor no influye en el servidor web o la base de datos, estos siguen funcionando en el background.

Podemos ejecutar sentencias como:
```sh
themyscira=# SELECT * FROM themyscira_video;
```

Para salir de la shell de `POSTGRESQL` escribimos `\q`, y posteriormente `exit` hasta salir del shell del contenedor.
