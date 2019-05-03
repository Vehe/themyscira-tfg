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
