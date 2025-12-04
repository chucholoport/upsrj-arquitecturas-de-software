# **Arquitectura en Capas (layered architecture)**  

- [**Arquitectura en Capas (layered architecture)**](#arquitectura-en-capas-layered-architecture)
  - [Características de la arquitectura](#características-de-la-arquitectura)
  - [Planteamiento](#planteamiento)
  - [Pasos a seguir](#pasos-a-seguir)
    - [1. Crear el componente `common/`](#1-crear-el-componente-common)
    - [2. Dividir las clases por componentes](#2-dividir-las-clases-por-componentes)
    - [3. Crear el componente `interfaces/`](#3-crear-el-componente-interfaces)
    - [4. Crear el componente `app/`](#4-crear-el-componente-app)
    - [5. Convertir `repos/user.py` en un repositorio con SQL](#5-convertir-reposuserpy-en-un-repositorio-con-sql)
    - [6. Usar el sistema de templates de Flask](#6-usar-el-sistema-de-templates-de-flask)
  - [Rutas obligatorias](#rutas-obligatorias)
    - [API (JSON)](#api-json)
    - [Templates (HTML)](#templates-html)
  - [Estructura final del proyecto](#estructura-final-del-proyecto)
  - [Contacto](#contacto)


## Características de la arquitectura
- **Separación por capas**:  
  - **Models** → definen la estructura de datos (DTOs o entidades).  
  - **Repos** → manejan el acceso a los datos (in‑memory primero, luego SQL).  
  - **Services** → contienen la lógica de negocio y validaciones.  
  - **Interfaces** → definen contratos para acoplamiento suave.  
  - **App** → organiza la aplicación Flask en tres partes:  
    - `main.py` → inicialización.  
    - `api.py` → rutas REST (JSON).  
    - `routes.py` → rutas HTML (templates).  
  - **Common** → centraliza configuración, mensajes y utilidades compartidas.  
  - **Templates** → interfaz visual embellecida con HTML y CSS.

- **Acoplamiento suave**: gracias a las interfaces (`IUserRepository`, `IUserService`), cualquier implementación puede sustituirse sin romper el resto del sistema.  

- **Dualidad API + UI**: la aplicación expone tanto endpoints REST (`/api/users`, `/api/users/new`) como vistas HTML (`/users`, `/users/new`), lo que la convierte en un proyecto híbrido: **backend API + frontend básico con templates**.  

- **Escalabilidad didáctica**: la estructura está pensada para crecer hacia arquitecturas más complejas (n‑capas, microservicios, serverless).

---

## Planteamiento

Este proyecto parte de un archivo único `main.py` y evoluciona hacia una arquitectura modular, siguiendo las convenciones de estilo de **PEP 8** y aplicando separación de responsabilidades. El objetivo es que aprendas a organizar tu código en componentes claros y escalables.

---

## Pasos a seguir

### 1. Crear el componente `common/`
- Crea una carpeta llamada `common/`. Dentro de ella, agrega:
  - **config.py** → define variables globales como host, puerto y modo debug.  
  - **view.py** → centraliza mensajes y errores predefinidos para mantener consistencia.  
  - **utils.py** → funciones auxiliares como normalización de cadenas para evitar duplicación de lógica.

---

### 2. Dividir las clases por componentes
- Crea la carpeta `models/`. Dentro de ella, agrega:
  - **user.py** → define el modelo `User`.  
- Crea la carpeta `repos/`. Dentro de ella, agrega:
  - **user.py** → contiene la clase `UserRepository` encargada de manejar el acceso a los datos (inicialmente en memoria).  
- Crea la carpeta `services/`. Dentro de ella, agrega:
  - **user.py** → contiene la clase `UserService`, donde se implementa la lógica de negocio y validaciones.

---

### 3. Crear el componente `interfaces/`
- Crea la carpeta `interfaces/`. Dentro de ella, agrega:
  - **user.py** → define las interfaces `IUserRepository` y `IUserService`. Estas interfaces actúan como contratos: especifican qué métodos deben existir en un repositorio o servicio, sin importar cómo estén implementados. Esto permite cambiar la implementación sin afectar el resto del sistema.

---

### 4. Crear el componente `app/`  
En este paso ya no trabajaremos con un único `main.py` en la raíz del proyecto. La idea es organizar la aplicación dentro de un nuevo componente llamado **`app/`**, que contendrá los archivos principales de la aplicación Flask.

Dentro de `app/` deberás crear:

- **main.py**  
  Este archivo será el punto de entrada de la aplicación. Su responsabilidad es inicializar Flask, cargar la configuración desde `common/config.py` y arrancar el servidor. Aquí no se definen rutas ni lógica de negocio, únicamente se prepara la aplicación para ejecutarse.

- **routes.py**  
  Este archivo se encargará de definir las rutas que renderizan **templates HTML** (por ejemplo, `/users` y `/users/new`). En él se conectan las vistas con los servicios y repositorios, y se utilizan los mensajes definidos en `common/view.py`. De esta forma, las rutas de interfaz quedan separadas del archivo principal, lo que facilita la organización y el mantenimiento.

- **api.py**  
  Este archivo se encargará de definir las rutas de la **API REST** (por ejemplo, `/api/users` y `/api/users/new`). Aquí se exponen los endpoints que devuelven y reciben datos en formato JSON, conectando directamente con los servicios y repositorios. De esta manera, se mantiene una separación clara entre las rutas de la API y las rutas de la interfaz HTML.

---

### 5. Convertir `repos/user.py` en un repositorio con SQL
- Sustituye la implementación en memoria por una base de datos real usando **SQLAlchemy**.  
- Define un modelo `User` como tabla en la base de datos.  
- Ajusta el repositorio para que los métodos `get_users` y `add_user` interactúen con SQL en lugar de listas en memoria.  
- Configura la conexión en `common/config.py` para que el proyecto pueda cambiar fácilmente de SQLite a PostgreSQL o MySQL.

---

### 6. Usar el sistema de templates de Flask  
En este paso vamos a enseñar cómo Flask no solo sirve para construir APIs que devuelven JSON, sino también para crear interfaces web embellecidas con HTML y CSS.  

- Crea una carpeta llamada **`templates/`** en la raíz del proyecto.  
- Dentro de ella, define un archivo **`index.html`** que actuará como el **cluster de funciones**: será la página principal desde donde el usuario podrá acceder a las distintas funcionalidades de la aplicación.  
  - En este archivo se deben colocar botones o enlaces que permitan navegar hacia las demás vistas (por ejemplo, “Listar usuarios” y “Crear nuevo usuario”).  
- Además, crea dos templates adicionales:  
  - **`users.html`** → mostrará la lista completa de usuarios en una tabla o lista embellecida con HTML y CSS.  
  - **`new_user.html`** → contendrá un formulario sencillo con un campo de texto para ingresar el nombre y un botón para enviar la información, permitiendo crear un nuevo usuario.  
- Modifica el componente `app/routes.py` para que, además de las rutas que devuelven JSON, tenga rutas que rendericen estos templates usando `render_template`.  

---

## Rutas obligatorias

### API (JSON)
Estas rutas exponen la lógica de negocio en formato JSON:

- **GET `/api/users`**  
  - Devuelve la lista de usuarios en formato JSON.  
  - Respuesta esperada: `200 OK` con un array de objetos `{id, name}`.  

- **POST `/api/users/new`**  
  - Crea un nuevo usuario a partir de un JSON con el campo `"name"`.  
  - Respuesta esperada:  
    - `201 Created` con el objeto del usuario creado.  
    - `400 Bad Request` si falta el campo `"name"` o si el nombre es inválido.

---

### Templates (HTML)
Estas rutas renderizan vistas embellecidas con HTML y CSS:

- **GET `/users`**  
  - Renderiza `users.html`, mostrando la lista completa de usuarios en una tabla o lista.  
  - Respuesta esperada: `200 OK` y contenido HTML con los nombres de los usuarios.  

- **GET `/users/new`**  
  - Renderiza `new_user.html`, mostrando un formulario para crear un nuevo usuario.  
  - Respuesta esperada: `200 OK` y contenido HTML con un campo de texto y un botón.  

- **POST `/users/new`**  
  - Procesa el formulario enviado desde `new_user.html`.  
  - Respuesta esperada:  
    - `302 Redirect` hacia `/users` si el usuario se creó correctamente.  
    - `400 Bad Request` si el formulario está incompleto.

---

## Estructura final del proyecto

```bash
src
├── app/
│   ├── main.py        # Punto de entrada de la aplicación Flask
│   ├── routes.py      # Rutas para templates HTML (users, users/new)
│   └── api.py         # Rutas para la API REST (api/users, api/users/new)
├── common/
│   ├── config.py      # Variables de configuración globales
│   ├── view.py        # Mensajes y errores predefinidos
│   └── utils.py       # Funciones auxiliares compartidas
├── models/
│   └── user.py        # Modelo de datos User
├── repos/
│   └── user.py        # Repositorio de usuarios (primero en memoria, luego con SQL)
├── services/
│   └── user.py        # Lógica de negocio y validaciones
├── interfaces/
│   └── user.py        # Interfaces para acoplamiento suave (IUserRepository, IUserService)
└── templates/
    ├── index.html     # Página principal (cluster de funciones)
    ├── users.html     # Vista para listar usuarios
    └── new_user.html  # Vista para crear un nuevo usuario
```

---

## Contacto

¿Dudas? Consulta los archivos de ayuda o pregunta a tu instructor.

**Autor:** Jesús Salvador López Ortega  
[LinkedIn](https://www.linkedin.com/in/jesus-salvador-lopez-ortega/) | [GitHub](https://github.com/chucholoport) | [Correo Institucional](mailto:jlopez@upsrj.edu.mx)
