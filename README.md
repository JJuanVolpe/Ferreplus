

# Ferreplus: Sistema ideado para cadena ferretera ubicada en Buenos Aires 🔩 🔧 🔨

## Desarrollado para la cátedra Ingeniería de Software 2

Este archivo [`README.md`](https://raw.githubusercontent.com/JJuanVolpe/Ferreplus/main/README.md) contiene las especificaciones necesarias para trabajar con el proyecto en conjunto con sus dependencias de forma organizada y clara. Así también está sujeto a mejoras/modificaciones por parte de los integrantes.


Este archivo readme [`README.md`](https://raw.githubusercontent.com/JJuanVolpe/Ferreplus/main/README.md) contiene las especificaciones necesarias para trabajar con el proyecto en conjunto con sus dependencias de forma organizada y clara. Así también está sujeto a mejoras/modificaciones por parte de los integrantes

<p align="center">
<img alt="Logo of group" width="30%" src="https://raw.githubusercontent.com/jjuanvolpe/ferreplus/main/myapp/static/logo.png"><br>
<em>Ferreplus logo</em>
</p>

## Table of contents

* [Introduction](#introduction)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Basic Usage](#basic-usage)
* [Usage](#usage)
* [Known issues and limitations](#known-issues-and-limitations)
* [Getting help](#getting-help)
* [Contributing](#contributing)
* [License](#license)
* [Acknowledgments](#acknowledgments)

## Introduction

El objetivo del proyecto en detalle se encuentra en la carpeta que contiene los [documentos de elicitacion de requerimientos](docs\SRS+PGP.pdf) conformados por el SRS Y GPG.
Para una visión más detallada de las funcionalidades a desarrollar contamos con la Historias de Usuario incluidas en el SRS.
La visión general del sistema simula una aplicación la cuál permite a usuarios no registrados ver las distintas sucursales de la cadena ferretera, registrarse e iniciar sesión.
Existen 3 roles respecto a los usuarios autenticados: Gerentes, Empleados y Clientes. Estos poseen acciones compartidas entre ambos roles cómo lo son cerrar sesión o las funcionalidades referidas a la edición de datos de su perfil. Sin embargo difieren a grandes rasgos:

* Los clientes son quiénes generan intercambios, ven artículos a la venta y conocen beneficios disponibles.
* Por otro lado los empleados pueden "validar" éstos trueques y/o administrar stock.
* Los gerentes gestionan las sucursales y los empleados, a su vez pueden conocer estadísticas a través de la plataforma.

## Installation

Clone el repositorio:

```sh
git clone https://github.com/JJuanVolpe/Ferreplus
```

## Prerequisites:

* Django
* Python 3
* SQLite3

Instale los requerimientos para el proyecto:

```sh
pip install -r requirements.txt
```

## Basic-Usage:

Para crear un proyecto utilizando django ejecutamos:

```sh
django-admin startproject <name-project>
```

Sin embargo este repositorio cuenta con el proyecto ya creado, el cuál asume cómo "raíz" llamado myapp.
Podemos generar aplicaciones altamente escalables conformando nuestro proyecto con carpetas denominadas "aplicaciones"

Para crear aplicaciones dentro de nuestro proyecto podemos ejecutar:

```sh
python manage.py startapp <name-app>
```

Este comando nos permite generar los archivos que permiten especificar las funcionalidades de una aplicación que termina acoplandose dentro de nuestro proyecto. Dentro de cada aplicación habrán archivos importantes:

* apps.py: Permite la configuración de la aplicación específica
* views.py: Definimos que enviar al navegador para que se vea en pantalla (ej. permite servir archivos html)
* models.py: Permite crear las clases que se convertirán en tablas (Django se encarga de las modificaciones y creación de las mismas).
* migrations: Se registran las modificaciones hechas a la BD.

Para correr el servidor podemos ejecutar el siguiente comando, permitiendo como parámetro el n° de puerto dónde ejecutaremos el proyecto:

```sh
python manage.py runserver <3000>
```

Si no agregamos un número, se ejecuta en el puerto por defecto

## Usage

El comando makemigrations se encarga de empaquetar los cambios del modelo en archivos de migración individuales (análogos a los commits).
Detectan los cambios de los modelos de las aplicaciones (Para esto se busca en todas las apps creadas dentro de nuestro proyecto),
aunque podemos especificar en que aplicación hemos realizado cambios y agregarla cómo parámetro opcional

```sh
python manage.py makemigrations
```

Mientras que migrate se encarga de aplicarlos a la base de datos. Es decir se encarga de efectuar los cambios a la BD efectivamente.

```sh
python manage.py migrate
```

### To format the Style using autopep press F1 and select format

***Notar que se deben aplicar los comandos anteriores en el orden correspondiente para poder ejecutar el código actual, debido a que deben crearse los modelos y tablas mediante Python y Django para el correcto funcionamiento del proyecto***
