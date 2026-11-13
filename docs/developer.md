# PrototiposExpress — Guia para desarrolladores

---

## Indice

1. [Introduccion](#introduccion)
2. [Estructura del proyecto](#estructura-del-proyecto)
3. [Frontend: explicacion del codigo fuente](#frontend-explicacion-del-codigo-fuente)
   - [index.html](#indexhtml)
   - [styles.css](#stylescss)
   - [main.js](#mainjs)
4. [Backend: explicacion del codigo fuente](#backend-explicacion-del-codigo-fuente)
   - [app.py](#apppy)
   - [requirements.txt](#requirementstxt)
5. [API de funciones](#api-de-funciones)
   - [Frontend (main.js)](#frontend-mainjs)
   - [Backend (app.py)](#backend-apppy)
6. [Flujo de envio de correo](#flujo-de-envio-de-correo)
7. [Configuracion SMTP detallada](#configuracion-smtp-detallada)
8. [Guia de modificacion y extension](#guia-de-modificacion-y-extension)
9. [Como contribuir](#como-contribuir)
10. [Como hacer deploy](#como-hacer-deploy)
11. [Pruebas](#pruebas)
12. [Referencias](#referencias)

---

## Introduccion

Este documento esta dirigido a desarrolladores que necesitan entender, modificar o extender el codigo fuente del proyecto **PrototiposExpress**. Proporciona una explicacion detallada de la arquitectura, los modulos, las funciones y los flujos de datos, asi como guias practicas para contribuir, desplegar y mantener el proyecto.

El proyecto es una landing page profesional 100% estatica (HTML + CSS + JS) para captura de leads. El formulario de contacto utiliza **Netlify Forms** para el envio de datos sin necesidad de backend. El proyecto incluye tambien un backend Flask opcional para desarrollo local con envio real de correos via SMTP.

---

## Estructura del proyecto

```
proyectos/PrototiposExpress/
│
├── README.md                          # Documentacion principal del proyecto
├── PLAN.md                            # Plan original con especificaciones
├── AUDIT_REPORT.md                    # Informe de auditoria de codigo
├── netlify.toml                       # Configuracion de deploy en Netlify
│
├── frontend/                          # Aplicacion frontend (cliente)
│   ├── index.html                     # Estructura HTML de la landing page
│   ├── css/
│   │   └── styles.css                 # Estilos CSS con tema oscuro
│   └── js/
│       └── main.js                    # Logica de cliente (JS vanilla)
│
├── backend/                           # Backend Flask (solo desarrollo local)
│   ├── app.py                         # Servidor Flask (frontend + API)
│   ├── requirements.txt               # Dependencias Python
│   ├── .env.example                   # Plantilla para variables de entorno
│   └── .env                           # Variables de entorno (NO SUBIR A GIT)
│
└── docs/                              # Documentacion generada
    ├── datasheet.md                   # Documentacion de usuario
    └── developer.md                   # Esta guia para desarrolladores
```

---

## Frontend: explicacion del codigo fuente

### index.html

**Archivo**: `frontend/index.html`
**Proposito**: Estructura semantica de la landing page.

El HTML esta organizado en secciones claramente delimitadas con comentarios. Cada seccion corresponde a un bloque funcional de la pagina:

#### Estructura general

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <!-- Meta tags, titulo, recursos -->
</head>
<body>
  <nav class="navbar">...</nav>           <!-- Navegacion fija -->
  <section class="hero" id="hero">...</section>           <!-- Portada -->
  <section class="section" id="como-funciona">...</section> <!-- Pipeline -->
  <section class="section section-dark" id="tecnologias">...</section> <!-- Tecnologias -->
  <section class="section" id="industrias">...</section>   <!-- Industrias -->
  <section class="section section-dark" id="equipo">...</section>   <!-- Equipo -->
  <section class="section" id="por-que-nosotros">...</section>      <!-- Diferenciadores -->
  <section class="section section-dark" id="contacto">...</section> <!-- Formulario -->
  <footer class="footer">...</footer>     <!-- Pie de pagina -->
  <script src="js/main.js"></script>
</body>
</html>
```

#### Detalles importantes

- **Meta tags**: Incluye `viewport` para responsive, `description` para SEO, y `charset` UTF-8.
- **FontAwesome**: Se carga desde CDN de cdnjs con atributo `crossorigin="anonymous"`.
- **IDs de secciones**: Cada seccion tiene un `id` que coincide con los anchors del menu de navegacion (ej: `#tecnologias`, `#contacto`).
- **Formulario**: El formulario tiene `id="contactForm"` y cada input tiene `name` y `id` que coinciden con los campos esperados por el backend (`nombre`, `email`, `telefono`, `empresa`, `necesidad`, `plazo`). Incluye `novalidate` para que la validacion sea manejada por JavaScript.
- **Mensajes de error**: Cada campo tiene un `<span>` contiguo con `id="error-NOMBRE"` para mostrar errores de validacion.
- **Mensaje del formulario**: Un `<div id="formMessage">` debajo del formulario muestra mensajes de exito, error o carga.

### styles.css

**Archivo**: `frontend/css/styles.css`
**Proposito**: Definir la apariencia visual de la landing page.

#### Arquitectura CSS

El archivo sigue una organizacion modular con las siguientes secciones:

1. **CSS Custom Properties (variables)**: Definidas en `:root` para colores, fuentes, radios de borde, sombras y transiciones. Esto permite mantener consistencia visual y facilita la personalizacion del tema.

2. **Reset y base**: Normalizacion basica de estilos (box-sizing, margin/padding cero, scroll suave).

3. **Tipografia**: Estilos para titulos, subtitulos, texto de secciones.

4. **Botones**: Clases `.btn`, `.btn-primary`, `.btn-outline`, `.btn-lg`, `.btn-submit` con variantes de color, hover, y estados deshabilitados.

5. **Navbar**: Barra de navegacion fija con efecto blur (backdrop-filter), sombra al hacer scroll (clase `.scrolled`), y menu responsive.

6. **Hero**: Seccion de portada con gradientes radiales de fondo, tipografia grande y botones de accion.

7. **Steps grid**: Cuadricula de 5 pasos con conectores mediante grid CSS (`grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr auto 1fr`).

8. **Tech grid**: Cuadricula de 3 columnas para las tarjetas de tecnologias.

9. **Industrias, Equipo, Diferenciales**: Estilos especificos para cada seccion.

10. **Formulario de contacto**: Estilos para inputs, textareas, estados de error, focus, y mensajes (success, error, loading).

11. **Footer**: Grid de 3 columnas con informacion de contacto.

12. **Animaciones**: Clases `.animate-fade-up` y `.animate-on-scroll` para animaciones controladas por Intersection Observer.

13. **Media queries**: Breakpoints para 1024px (tablet), 768px (mobile), 480px (small mobile) y 1400px+ (large screens).

#### Sistema de diseno (variables CSS)

```css
:root {
  --color-bg: #0b0f1a;              /* Fondo principal (oscuro) */
  --color-bg-card: #131826;          /* Fondo de tarjetas */
  --color-bg-dark: #080b14;          /* Fondo de secciones alternas */
  --color-accent: #06b6d4;           /* Color acento (cian) */
  --color-primary: #3b82f6;          /* Color primario (azul) */
  --color-text: #e2e8f0;             /* Texto principal */
  --color-text-muted: #94a3b8;       /* Texto secundario */
  --color-border: #2a3350;           /* Bordes */
  --color-success: #10b981;          /* Verde exito */
  --color-error: #ef4444;            /* Rojo error */
  --max-width: 1200px;               /* Ancho maximo del contenido */
  --nav-height: 70px;                /* Altura de la barra de navegacion */
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1); /* Transicion estandar */
}
```

#### Patrones de diseno destacados

- **Tema oscuro**: Todo el diseno utiliza una paleta de colores oscuros con acentos cian y azul.
- **Efecto glass**: La navbar usa `backdrop-filter: blur(16px)` para el efecto de vidrio.
- **Gradientes en texto**: Los titulos de seccion usan `background: linear-gradient(...)` con `background-clip: text` para texto gradiente.
- **Hover elevacion**: Todas las tarjetas se elevan (`translateY`) y muestran sombra al hacer hover.

### main.js

**Archivo**: `frontend/js/main.js`
**Proposito**: Logica de interaccion del lado del cliente.

El archivo esta escrito en JavaScript vanilla (ES6+) y se ejecuta cuando el DOM esta listo. Se organiza en 4 funciones principales que se inicializan en `DOMContentLoaded`:

```javascript
document.addEventListener('DOMContentLoaded', () => {
  initNavbar();             // Navegacion y menu movil
  initScrollAnimations();   // Animaciones con Intersection Observer
  initContactForm();        // Validacion y envio del formulario
  initSmoothScroll();       // Scroll suave para anchors
});
```

#### initNavbar()

Gestiona el comportamiento de la barra de navegacion:

- **Toggle del menu movil**: Al hacer clic en el boton hamburguesa (`.nav-toggle`), se alterna la clase `active` en el menu y se cambia el icono entre `fa-bars` y `fa-times`.
- **Cierre automatico**: Al hacer clic en cualquier enlace del menu, se cierra el menu movil.
- **Efecto de scroll**: Cuando el scroll supera 50px, se agrega la clase `scrolled` a la navbar para cambiar su opacidad y sombra.

#### initScrollAnimations()

Implementa animaciones basadas en la visibilidad de los elementos:

- Utiliza `IntersectionObserver` con `threshold: 0.15` y `rootMargin: '0px 0px -60px 0px'`.
- Cuando un elemento con clase `.animate-on-scroll` entra en el viewport, se le agrega la clase `visible`, que dispara la transicion CSS de opacidad 0->1 y translateY 40px->0.
- Una vez visible, se deja de observar el elemento (`observer.unobserve()`).
- Los elementos del hero (`.animate-fade-up`) se muestran inmediatamente sin esperar scroll.
- Incluye un fallback para navegadores sin IntersectionObserver: todos los elementos animados se muestran de inmediato.

#### initSmoothScroll()

Proporciona scroll suave para enlaces internos (`a[href^="#"]`):

- Escucha clics en todos los enlaces que comienzan con `#`.
- Usa `element.scrollIntoView({ behavior: 'smooth', block: 'start' })` para desplazarse suavemente.
- Previene el comportamiento por defecto del enlace.

#### initContactForm()

Gestiona el formulario de contacto completo, incluyendo:

**Validacion en tiempo real**:
- Cada input y textarea tiene un listener `blur` que ejecuta `validateField()`.
- Cada input tiene un listener `input` que limpia el error mientras el usuario escribe.

**Envio asincrono**:
1. Previene el envio tradicional del formulario (`e.preventDefault()`).
2. Resetea el mensaje de estado.
3. Ejecuta `validateField()` en todos los campos requeridos.
4. Si hay errores, desplaza la vista al primer error y detiene el envio.
5. Construye el payload JSON con los valores de los campos.
6. Muestra estado de carga: deshabilita el boton, cambia el texto a "Enviando..." y muestra un mensaje de carga.
7. Envia una peticion `fetch POST /api/contacto` con `Content-Type: application/json`.
8. Procesa la respuesta:
   - Si es exitosa (`response.ok && data.status === 'ok'`): muestra mensaje verde de exito y resetea el formulario.
   - Si falla: muestra mensaje rojo con el error.
   - Si hay error de red (`Failed to fetch`): muestra mensaje especifico.
9. En el bloque `finally`, restaura el boton a su estado original.

#### validateField(input)

Valida un campo individual y retorna `true`/`false`:

- Verifica si el campo es obligatorio y esta vacio.
- Para email: valida con regex `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`.
- Para telefono: valida con regex `/^[\d\s+()-]{7,20}$/`.
- Para plazo: verifica que la fecha sea posterior al dia actual.
- Si hay error: agrega clase `error` al input y muestra el mensaje en el span de error correspondiente.

#### Manejo de errores

- Errores de red: captura `Failed to fetch` y muestra mensaje amigable.
- Errores del servidor: muestra el mensaje devuelto por el backend.
- Errores de validacion: muestra mensajes especificos por campo.
- Estados de carga: deshabilita interaccion y muestra feedback visual.

---

## Backend: explicacion del codigo fuente

### app.py

**Archivo**: `backend/app.py`
**Proposito**: Servidor Flask unificado que sirve el frontend estatico (landing page) y la API REST para envio de correos.

#### Estructura general

```python
# 1. Imports (bibliotecas)
import os, re, smtplib, logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# 2. Ruta base del frontend
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

# 3. Configuracion inicial
load_dotenv()
app = Flask(__name__)
CORS(app)

# 4. Constantes SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
TO_EMAIL = os.getenv("TO_EMAIL", "jmadasme@gmail.com")

# 5. Funciones helper
def compose_email_html(data): ...
def _escape_html(text): ...
def send_contact_email(data): ...
def validate_contact_data(data): ...

# 6. Rutas del frontend estatico
@app.route("/", methods=["GET"])
def serve_index(): ...

@app.route("/<path:path>", methods=["GET"])
def serve_static(path): ...

# 7. Endpoints API
@app.route("/health", methods=["GET"])
def health(): ...

@app.route("/api/contacto", methods=["POST"])
def contacto(): ...

# 8. Entry point
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    ...
```

#### Endpoints

**`GET /` (Frontend)**

- **Proposito**: Sirve la landing page principal (`frontend/index.html`).
- **Respuesta**: Archivo HTML completo con todas las secciones.
- **Uso**: Abrir `http://localhost:5000/` en el navegador.

**`GET /<path:path>` (Archivos estaticos)**

- **Proposito**: Sirve archivos estaticos (CSS, JS, imagenes) desde la carpeta `frontend/`.
- **Ejemplos**: `/css/styles.css`, `/js/main.js`.
- **Seguridad**: Incluye proteccion contra directory traversal (path traversal).
- **Fallback**: Si el archivo no existe, sirve `index.html` (comportamiento SPA-like).

**`GET /health`**

- **Proposito**: Health check para monitoreo.
- **Respuesta exitosa**: `{"status": "ok"}` con codigo 200.
- **Uso**: Verificar que el servidor esta corriendo.

**`POST /api/contacto`**

- **Proposito**: Recibir datos del formulario de contacto y enviar correo electronico.
- **Content-Type requerido**: `application/json`.
- **Cuerpo esperado**:
  ```json
  {
    "nombre": "string",
    "email": "string (formato email)",
    "telefono": "string (7-20 digitos)",
    "empresa": "string",
    "necesidad": "string",
    "plazo": "string (YYYY-MM-DD)"
  }
  ```
- **Respuesta exitosa (200)**: `{"status": "ok", "message": "Solicitud enviada con exito."}`
- **Respuestas de error**:
  - `400`: Campos invalidos o faltantes.
  - `500`: Error de configuracion SMTP, error de autenticacion, error de envio, o error interno.

#### Funciones helper

**`compose_email_html(data: dict) -> str`**

Compone un email en formato HTML profesional con los datos del formulario. Utiliza una plantilla HTML embebida en el codigo con estilos inline (compatibles con clientes de correo). La plantilla incluye:

- Encabezado con gradiente (cian a azul).
- Tabla con los campos: nombre, email, telefono, empresa, plazo.
- Seccion para la descripcion de la necesidad con fondo gris claro.
- Pie con atribucion.

**`_escape_html(text: str) -> str`**

Escapa caracteres HTML peligrosos para prevenir inyeccion XSS en el correo:
- `&` -> `&amp;`
- `<` -> `&lt;`
- `>` -> `&gt;`
- `"` -> `&quot;`
- `'` -> `&#x27;`

**`send_contact_email(data: dict) -> None`**

Conecta con el servidor SMTP de Gmail y envia el correo:

1. Crea un mensaje MIME multipart con contenido HTML.
2. Configura From, To y Subject (incluye nombre y empresa del solicitante).
3. Adjunta el HTML generado por `compose_email_html()`.
4. Establece conexion SMTP a `smtp.gmail.com:587`.
5. Inicia TLS con `server.starttls()`.
6. Se autentica con `SMTP_USER` y `SMTP_PASS`.
7. Envia el mensaje.
8. La conexion se cierra automaticamente al salir del bloque `with`.

**`validate_contact_data(data: dict) -> tuple[bool, str]`**

Valida los campos del formulario:

1. Verifica que todos los campos requeridos existan y no esten vacios.
2. Valida el formato del email con expresion regular.
3. Retorna `(True, "")` si todo es valido, o `(False, "mensaje de error")` si hay problemas.

#### Manejo de errores SMTP

El endpoint `contacto()` maneja explicitamente 4 tipos de errores:

| Error | Captura | Respuesta HTTP | Mensaje |
|-------|---------|----------------|---------|
| SMTP no configurado | Verificacion previa | 500 | "Error de configuracion del servidor de correo." |
| Error de autenticacion | `smtplib.SMTPAuthenticationError` | 500 | "Error de autenticacion con el servidor de correo." |
| Error SMTP generico | `smtplib.SMTPException` | 500 | "Error al enviar el correo. Intenta nuevamente." |
| Error inesperado | `Exception` (catch-all) | 500 | "Error interno del servidor." |

#### Configuracion de logging

```python
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
)
logger = logging.getLogger("prototiposexpress")
```

Los mensajes de log incluyen:
- Inicio del servidor con puerto y modo debug.
- Confirmacion de envio de email exitoso.
- Errores SMTP con detalles del problema.
- Advertencia si SMTP_USER o SMTP_PASS no estan configurados.

### requirements.txt

**Archivo**: `backend/requirements.txt`
**Proposito**: Listar las dependencias Python necesarias para ejecutar el backend.

```
flask==3.1.1
flask-cors==5.0.1
python-dotenv==1.1.0
```

| Dependencia | Version | Proposito |
|-------------|---------|-----------|
| Flask | 3.1.1 | Framework web para crear el servidor API |
| flask-cors | 5.0.1 | Middleware para permitir CORS (Cross-Origin Resource Sharing) |
| python-dotenv | 1.1.0 | Carga variables de entorno desde archivo `.env` |

---

## API de funciones

### Frontend (main.js)

#### Funciones publicas

| Funcion | Parametros | Retorno | Descripcion |
|---------|-----------|---------|-------------|
| `initNavbar()` | Ninguno | `void` | Inicializa la barra de navegacion: toggle movil, efecto scroll |
| `initScrollAnimations()` | Ninguno | `void` | Configura Intersection Observer para animaciones al hacer scroll |
| `initContactForm()` | Ninguno | `void` | Configura validacion y envio asincrono del formulario |
| `initSmoothScroll()` | Ninguno | `void` | Agrega scroll suave a todos los enlaces internos |
| `validateField(input)` | `input`: Elemento HTML | `boolean` | Valida un campo individual, muestra error si es invalido |

#### Flujo de inicializacion

```
DOMContentLoaded
  ├── initNavbar()
  ├── initScrollAnimations()
  ├── initContactForm()
  └── initSmoothScroll()
```

### Backend (app.py)

#### Funciones internas

| Funcion | Parametros | Retorno | Descripcion |
|---------|-----------|---------|-------------|
| `compose_email_html(data)` | `data: dict` | `str` | Genera HTML formateado para el correo |
| `_escape_html(text)` | `text: str` | `str` | Escapa caracteres HTML peligrosos |
| `send_contact_email(data)` | `data: dict` | `None` | Envia el correo via SMTP Gmail |
| `validate_contact_data(data)` | `data: dict` | `tuple(bool, str)` | Valida campos del formulario |

#### Endpoints

| Metodo | Ruta | Request | Response exitosa | Codigos de error |
|--------|------|---------|-----------------|------------------|
| `GET` | `/health` | Ninguno | `200: {"status": "ok"}` | Ninguno |
| `POST` | `/api/contacto` | JSON con `nombre, email, telefono, empresa, necesidad, plazo` | `200: {"status": "ok", "message": "..."}` | `400` (validacion), `500` (SMTP) |

---

## Flujo de envio de correo

A continuacion se describe el flujo completo desde que el usuario hace clic en "Enviar" hasta que el correo llega al destino:

```
Usuario hace clic en "Enviar solicitud"
        |
        v
[Frontend] Prevencion de envio por defecto (e.preventDefault())
        |
        v
[Frontend] Validacion de todos los campos (validateField)
        |
        +-- Si hay errores --> Scroll al primer error, STOP
        |
        v
[Frontend] Construccion de payload JSON
        |
        v
[Frontend] fetch POST /api/contacto
        |  Headers: Content-Type: application/json
        |  Body: JSON.stringify(payload)
        |
        v
[Backend] Flask recibe la solicitud
        |
        v
[Backend] Validacion de Content-Type (debe ser application/json)
        |
        v
[Backend] Validacion de datos (validate_contact_data)
        |
        +-- Si invalido --> 400 Bad Request
        |
        v
[Backend] Verificacion de SMTP_USER y SMTP_PASS
        |
        +-- Si no configurados --> 500 Error de configuracion
        |
        v
[Backend] send_contact_email(data)
        |
        v
[Backend] Composicion de email HTML (compose_email_html)
        |
        v
[Backend] Conexion SMTP a smtp.gmail.com:587
        |
        v
[Backend] STARTTLS (seguridad)
        |
        v
[Backend] Autenticacion (SMTP_USER / SMTP_PASS)
        |
        +-- SMTPAuthenticationError --> 500 Error de autenticacion
        |
        v
[Backend] Envio del mensaje
        |
        +-- SMTPException --> 500 Error SMTP
        |
        v
[Backend] Respuesta 200: {"status": "ok"}
        |
        v
[Frontend] Recepcion de respuesta
        |
        +-- ok --> Mensaje verde de exito, reset del formulario
        |
        +-- error --> Mensaje rojo con descripcion del error
```

---

## Configuracion SMTP detallada

### Variables de entorno

El backend utiliza las siguientes variables de entorno, cargadas desde el archivo `.env` mediante `python-dotenv`:

| Variable | Obligatoria | Valor por defecto | Descripcion |
|----------|-------------|-------------------|-------------|
| `SMTP_USER` | Si | `""` (vacio) | Correo electronico remitente para SMTP |
| `SMTP_PASS` | Si | `""` (vacio) | Contrasena de aplicacion de Gmail |
| `TO_EMAIL` | No | `"jmadasme@gmail.com"` | Correo destino de las solicitudes |
| `PORT` | No | `5000` | Puerto del servidor Flask |
| `FLASK_DEBUG` | No | `"false"` | Modo debug de Flask (`"true"` para activar) |

### Archivo .env (ejemplo)

```env
SMTP_USER=jmadasme@gmail.com
SMTP_PASS=abcd efgh ijkl mnop
TO_EMAIL=jmadasme@gmail.com
PORT=5000
FLASK_DEBUG=true
```

### Configuracion SMTP de Gmail

```
Servidor: smtp.gmail.com
Puerto: 587 (TLS)
Autenticacion: Requerida
Cifrado: STARTTLS
```

### Como generar una contrasena de aplicacion de Gmail

1. Activar la verificacion en dos pasos en la cuenta de Google: [myaccount.google.com/security](https://myaccount.google.com/security).
2. Ir a Contrasenas de aplicacion: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
3. Seleccionar "Correo" y "Windows" (u "Otra").
4. Copiar la contrasena de 16 caracteres generada.

### Limites de SMTP de Gmail

- **500 destinatarios por dia** (para cuentas gratuitas).
- **2,000 mensajes por dia** (para cuentas gratuitas).
- Para volumenes mayores, se recomienda usar Gmail Workspace o un servicio de correo transaccional (SendGrid, Mailgun, Amazon SES).

---

## Guia de modificacion y extension

### Agregar una nueva seccion a la landing page

1. **HTML**: Agrega una nueva `<section>` en `index.html` con un `id` unico y la clase `section` (o `section section-dark` para fondo alterno).
2. **CSS**: Agrega los estilos necesarios en `styles.css`. Usa las variables CSS existentes para mantener consistencia visual.
3. **Navegacion**: Agrega un enlace en `<ul class="nav-menu">` apuntando al `id` de la nueva seccion.
4. **Animacion**: Agrega la clase `animate-on-scroll` a los elementos que quieras animar al hacer scroll.

### Agregar un nuevo campo al formulario

1. **HTML**: Agrega el nuevo campo en el formulario dentro de `index.html`. Usa la estructura existente como referencia:
   ```html
   <div class="form-group">
     <label for="nuevo_campo">Nuevo Campo *</label>
     <input type="text" id="nuevo_campo" name="nuevo_campo" required>
     <span class="form-error" id="error-nuevo_campo"></span>
   </div>
   ```
2. **JS**: En `initContactForm()`, agrega el nuevo campo al array `fields` para que sea validado.
3. **JS**: En la construccion del `payload`, agrega el nuevo campo.
4. **Backend**: En `app.py`, agrega el nuevo campo en:
   - `validate_contact_data()`: Agregalo a `required_fields`.
   - `compose_email_html()`: Agregalo al template HTML del correo.
   - `send_contact_email()`: El subject puede incluir el nuevo campo si se desea.

### Cambiar el diseno visual

- **Colores**: Modifica las variables CSS en `:root`. Los cambios se reflejan en toda la pagina automaticamente.
- **Tipografia**: Cambia `--font-sans` por otra fuente.
- **Tema claro**: Si se desea un tema claro, modifica los valores de `--color-bg`, `--color-text`, etc.
- **Layout**: Ajusta `--max-width` para cambiar el ancho maximo del contenido.

### Agregar un nuevo endpoint al backend

```python
@app.route("/api/nuevo-endpoint", methods=["GET"])
def nuevo_endpoint():
    # Logica del endpoint
    return jsonify({"status": "ok", "data": ...}), 200
```

### Cambiar el servicio de correo SMTP

Para usar otro proveedor SMTP (no Gmail):

1. Cambia `SMTP_SERVER` y `SMTP_PORT` en `app.py`.
2. Ajusta la configuracion TLS segun el proveedor (algunos usan puerto 465 con SSL en lugar de 587 con TLS).
3. Para SSL (puerto 465), cambia `smtplib.SMTP` por `smtplib.SMTP_SSL`.

Ejemplo para SendGrid:

```python
SMTP_SERVER = "smtp.sendgrid.net"
SMTP_PORT = 587
# Usar API key de SendGrid como SMTP_PASS
```

---

## Como contribuir

### Flujo de trabajo recomendado

1. **Fork o clonar** el repositorio.
2. **Crear una rama** para tu contribucion:
   ```bash
   git checkout -b feature/mi-mejora
   ```
3. **Realizar los cambios** en el codigo siguiendo las guias de estilo.
4. **Probar los cambios** localmente.
5. **Hacer commit** con mensajes claros y descriptivos:
   ```bash
   git commit -m "Agrega validacion de RUT en formulario de contacto"
   ```
6. **Enviar un Pull Request** describiendo los cambios realizados.

### Guias de estilo

#### HTML
- Usar HTML5 semantico (`<section>`, `<nav>`, `<footer>`, etc.).
- Indentacion con 2 espacios.
- Atributos en orden: `id`, `class`, `name`, `type`, etc.
- Comentarios para separar secciones.

#### CSS
- Usar las variables CSS definidas en `:root`.
- Organizar por secciones con comentarios.
- Preferir clases sobre IDs para estilos.
- Mantener la especificidad baja.
- Usar `rem` para fuentes y `px` para bordes/sombras.
- Mobile-first: los estilos base son para movil, los media queries agregan capas para pantallas mas grandes.

#### JavaScript
- Usar `'use strict'`.
- Nombres de funciones en camelCase.
- Variables con nombres descriptivos en ingles o español.
- Comentarios JSDoc para funciones principales.
- Evitar dependencias externas (el proyecto usa JS vanilla).

#### Python
- Seguir PEP 8.
- Nombres de funciones en snake_case.
- Tipo de retorno documentado en docstrings.
- Imports al inicio del archivo (no dentro de funciones).
- Usar logging en lugar de print.

### Pruebas antes de contribuir

- Verificar que `GET /health` responde `200`.
- Verificar que `POST /api/contacto` con datos correctos responde `200` (o `500` si SMTP no configurado).
- Verificar que `POST /api/contacto` con datos invalidos responde `400`.
- Verificar que el frontend se ve correctamente en Chrome, Firefox y Edge.
- Verificar el diseño responsive en 320px, 768px y 1920px.

---

## Como hacer deploy

### Opcion 1: Deploy en Render (recomendado para produccion)

Render ofrece hosting gratuito para servicios web con soporte para Python.

#### Backend en Render

1. Crea una cuenta en [render.com](https://render.com).
2. Conecta tu repositorio de GitHub/GitLab.
3. Crea un nuevo **Web Service**.
4. Configuracion:
   - **Name**: `prototiposexpress-api`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free
5. Agrega las variables de entorno en el panel de Render:
   - `SMTP_USER`: `jmadasme@gmail.com`
   - `SMTP_PASS`: (tu contraseña de aplicacion)
   - `TO_EMAIL`: `jmadasme@gmail.com`
6. Despliega. Render te dara una URL como `https://prototiposexpress-api.onrender.com`.

#### Frontend en Render (Static Site)

1. Crea un nuevo **Static Site** en Render.
2. Configuracion:
   - **Name**: `prototiposexpress`
   - **Root Directory**: `frontend`
   - **Build Command**: (vacio, es estatico)
   - **Publish Directory**: `.`
3. Despliega. Render te dara una URL como `https://prototiposexpress.onrender.com`.

**Nota importante**: Si el frontend esta en un dominio diferente al backend, el CORS del backend (flask-cors) ya esta configurado para permitirlo. Sin embargo, en `main.js` la URL de la API es relativa (`/api/contacto`). Si el frontend y backend estan en dominios separados, debes cambiar la URL en `main.js`:

```javascript
// En main.js, linea 192
const apiUrl = 'https://prototiposexpress-api.onrender.com/api/contacto';
```

### Opcion 2: Deploy en Railway

Similar a Render, pero con una interfaz diferente.

1. Crea cuenta en [railway.app](https://railway.app).
2. Conecta el repositorio.
3. Railway detecta automaticamente el proyecto Flask.
4. Configura las variables de entorno en el panel.
5. Despliega.

### Opcion 3: Deploy en VPS (produccion profesional)

#### Requisitos del VPS
- Linux (Debian/Ubuntu recomendado).
- Python 3.9+.
- Nginx o Apache como proxy inverso.
- (Opcional) Docker.

#### Pasos

1. **Actualizar el sistema**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Instalar Python y pip**:
   ```bash
   sudo apt install python3 python3-pip python3-venv -y
   ```

3. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu-usuario/prototiposexpress.git
   cd prototiposexpress/backend
   ```

4. **Crear entorno virtual e instalar dependencias**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn  # Servidor WSGI para produccion
   ```

5. **Configurar variables de entorno**:
   ```bash
   nano .env
   ```
   Agregar:
   ```env
   SMTP_USER=jmadasme@gmail.com
   SMTP_PASS=tu_contraseña
   TO_EMAIL=jmadasme@gmail.com
   ```

6. **Configurar Nginx como proxy inverso**:
   ```nginx
   server {
       listen 80;
       server_name tudominio.com;
   
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

7. **Ejecutar con Gunicorn**:
   ```bash
   gunicorn -w 4 -b 127.0.0.1:8000 app:app
   ```

8. **Servir el frontend**: Copia los archivos de `frontend/` a `/var/www/html/` o configuralo como otro bloque en Nginx.

9. **Configurar SSL** con Certbot/Let's Encrypt para HTTPS.

### Opcion 4: Deploy local con Docker

Crea un `Dockerfile` en la raiz del proyecto:

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Construir y ejecutar:

```bash
docker build -t prototiposexpress .
docker run -p 5000:5000 --env-file backend/.env prototiposexpress
```

---

## Pruebas

### Pruebas manuales del backend

```bash
# Health check
curl http://localhost:5000/health

# Envio exitoso (requiere SMTP configurado)
curl -X POST http://localhost:5000/api/contacto \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test Usuario",
    "email": "test@ejemplo.com",
    "telefono": "+56 9 1234 5678",
    "empresa": "Test SPA",
    "necesidad": "Test de integracion del formulario",
    "plazo": "2026-12-31"
  }'

# Prueba de validacion (campo faltante)
curl -X POST http://localhost:5000/api/contacto \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Test"}'

# Prueba de validacion (email invalido)
curl -X POST http://localhost:5000/api/contacto \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test",
    "email": "invalido",
    "telefono": "123456789",
    "empresa": "Test",
    "necesidad": "Test",
    "plazo": "2026-12-31"
  }'

# Prueba de Content-Type incorrecto
curl -X POST http://localhost:5000/api/contacto \
  -H "Content-Type: text/plain" \
  -d 'datos'
```

### Pruebas del frontend

1. Abrir la pagina en Chrome, Firefox y Edge.
2. Verificar diseño responsive con DevTools (toggle device toolbar).
3. Verificar animaciones al hacer scroll.
4. Verificar navegacion suave entre secciones.
5. Verificar validacion del formulario (campos vacios, email invalido, fecha pasada).
6. Verificar mensaje de exito/error al enviar.

---

## Despliegue en Netlify

### netlify.toml

El archivo `netlify.toml` en la raiz del proyecto configura el deploy en Netlify:

```toml
[build]
  publish = "frontend"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
```

### Netlify Forms (envio de formularios)

El formulario de contacto utiliza **Netlify Forms** para el envio de datos sin backend:

1. El formulario HTML tiene el atributo `data-netlify="true"` y un campo oculto `<input type="hidden" name="form-name" value="contacto" />`.
2. El JavaScript (`main.js`) envia los datos via AJAX a `POST /` con `Content-Type: application/x-www-form-urlencoded`.
3. Netlify captura automaticamente la submission y la muestra en el dashboard.
4. Para recibir notificaciones por email, configurar en Netlify: **Site settings → Forms → Form notifications → Add notification → Email**.

### Pasos para desplegar

1. Subir el repositorio a GitHub.
2. En Netlify, importar el repositorio (Netlify detectara automaticamente `netlify.toml`).
3. No requiere comando de build (es HTML/CSS/JS plano).
4. Publicar desde la carpeta `frontend/`.
5. Configurar notificaciones de formulario hacia jmadasme@gmail.com.

### Consideraciones

- **El backend Flask no se despliega en Netlify**. Solo se usa para desarrollo local.
- En Netlify, el formulario envia los datos a Netlify Forms directamente.
- Para desarrollo local, el formulario intentara enviar a Netlify Forms (solo funciona si el sitio esta deployado en Netlify). Para probar localmente con envio real de correos, usar el backend Flask.

---

## Referencias

- **Documentacion de Flask**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **Documentacion de Flask-CORS**: [https://flask-cors.readthedocs.io/](https://flask-cors.readthedocs.io/)
- **python-dotenv**: [https://github.com/theskumar/python-dotenv](https://github.com/theskumar/python-dotenv)
- **SMTP de Gmail**: [https://support.google.com/mail/answer/7126229](https://support.google.com/mail/answer/7126229)
- **Contrasenas de aplicacion de Google**: [https://support.google.com/accounts/answer/185833](https://support.google.com/accounts/answer/185833)
- **Intersection Observer API**: [https://developer.mozilla.org/es/docs/Web/API/Intersection_Observer_API](https://developer.mozilla.org/es/docs/Web/API/Intersection_Observer_API)
- **FontAwesome 6**: [https://fontawesome.com/](https://fontawesome.com/)
- **Gunicorn**: [https://gunicorn.org/](https://gunicorn.org/)
- **Render**: [https://render.com/](https://render.com/)

---

## Notas finales

- Manten las dependencias actualizadas revisando periodicamente las versiones en PyPI.
- No subas archivos `.env`, `__pycache__/`, `venv/` ni otros archivos generados al repositorio.
- Revisa el archivo `AUDIT_REPORT.md` para conocer las incidencias detectadas y las mejoras pendientes.
- Para reportar bugs o sugerir mejoras, abre un issue en el repositorio del proyecto.

---

*Documentacion generada para desarrolladores - PrototiposExpress 2026*
