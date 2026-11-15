# Prototipos Express · Landing · Netlify

![Estado](https://img.shields.io/badge/estado-preservado-2A9D8F?style=flat-square)
![Versiones](https://img.shields.io/badge/versiones-1-457B9D?style=flat-square)
![Sección](https://img.shields.io/badge/sección-software-5B7C99?style=flat-square)
![Licencia](https://img.shields.io/badge/licencia-MIT-06141b?style=flat-square)

> Landing y backend para captar interesados en prototipos gratuitos, desplegable en Netlify.

Este repositorio reúne **1 versión** de Prototipos Express en `versions/`.
Cada carpeta conserva el contenido original de su etapa, sin `.git`, dependencias
instaladas ni binarios pesados. La documentación de operación y de código está en
[`docs/`](docs/), y el sitio del proyecto en [`docs/index.html`](docs/index.html).

## Índice de versiones

| Versión | Qué aporta | Archivos |
|---|---|---:|
| [`PrototiposExpress`](versions/PrototiposExpress/) | Landing, backend y configuración de despliegue en Netlify para captar leads. | 11 |

La versión de referencia de esta familia es **`PrototiposExpress`**: es la que se usa
para el README base y para los documentos canónicos. Las demás se mantienen
completas para que se pueda reconstruir la evolución y comparar decisiones.

## Arranque rápido

```bash
git clone https://github.com/jmadasme/prototipos-express.git
cd prototipos-express/versions/PrototiposExpress
# revisá el README para build y variables de entorno
npm install && npm run dev
```

Las variables de entorno y el destino de los formularios no se incluyen. Sin ellas el backend no envía nada.

<!-- ficha -->
## Ficha de evaluación

**Madurez global: 3.2/5**

| Criterio | Nota | Evidencia |
|---|---:|---|
| Madurez | 2/5 | Landing y backend mínimo sin autenticación, persistencia ni pruebas automatizadas; el alcance declarado es validar demanda. |
| Reproducibilidad | 3/5 | El frontend se sirve con cualquier servidor HTTP; el backend exige Python 3.9+, dependencias y credenciales SMTP válidas. |
| Documentación | 4/5 | README, datasheet y guía de desarrollador cubren instalación, API y despliegue; la descripción del flujo alterna Netlify y Flask. |
| Honestidad de límites | 3/5 | Declara que no hay base de datos, autenticación ni backend en producción, pero la arquitectura y el flujo del formulario se contradicen. |
| Valor demostrativo | 3/5 | Muestra captación, validación en dos capas y despliegue estático; los casos y métricas del README son ilustrativos, no resultados verificados. |
| Facilidad de despliegue | 4/5 | Netlify publica la carpeta frontend sin build; el backend opcional requiere variables de entorno y un servidor WSGI. |

Es un ejercicio de validación temprana: landing estática y backend mínimo, con límites claros y una documentación más ambiciosa que el producto. El conjunto sirve para medir interés, no para operar un servicio.

## Lo que no funcionó

### PrototiposExpress — Formulario atado a Netlify

El formulario envía a Netlify Forms mediante fetch a la raíz del sitio, de modo que solo confirma envíos cuando la página está desplegada en Netlify. El backend Flask existe, pero el README indica cambiar a mano la URL a /api/contacto para probarlo localmente. Se mantuvo el sitio estático y el backend como alternativa de desarrollo.

### PrototiposExpress — Leads solo por correo

Los datos del formulario no se guardan en una base: se envían por correo y quedan solo en la bandeja de destino. El README descarta autenticación, cuentas y persistencia, así que no hay forma de consultar, deduplicar ni medir leads desde el sitio. La limitación es explícita y acota el uso a validación inicial.

### PrototiposExpress — Credenciales SMTP manuales

El envío real depende de una cuenta de Gmail con verificación en dos pasos y una contraseña de aplicación configurada en variables de entorno. Sin SMTP_USER y SMTP_PASS, el backend responde con error de configuración. El servidor Flask se declara solo para desarrollo y no se despliega en Netlify.

<!-- /ficha -->

## Documentación

- [`docs/datasheet.md`](docs/datasheet.md) — instalación, operación y límites.
- [`docs/developer.md`](docs/developer.md) — arquitectura, módulos y extensión.
- [`docs/REFERENCES.md`](docs/REFERENCES.md) — estándares, librerías y fuentes.
- [`docs/index.html`](docs/index.html) — página del proyecto (GitHub Pages).

## El proyecto en detalle

### PrototiposExpress

Landing page profesional para la captura de interesados en servicios de prototipado rapido de soluciones de software y hardware. El sistema permite que un cliente potencial solicite una reunion sin compromiso, detalle su necesidad y plazo deseado, y reciba un prototipo funcional gratuito para testeo. Solo si el prototipo demuestra valor real, el cliente paga por el servicio.

---

### Indice

- [Descripcion del servicio](#descripcion-del-servicio)
- [Principio de funcionamiento](#principio-de-funcionamiento)
- [Tecnologias ofrecidas](#tecnologias-ofrecidas)
- [Arquitectura del sistema](#arquitectura-del-sistema)
- [Forma de operar (para el cliente)](#forma-de-operar-para-el-cliente)
- [Ejemplos de uso](#ejemplos-de-uso)
- [Requisitos del sistema](#requisitos-del-sistema)
- [Configuracion del correo electronico](#configuracion-del-correo-electronico)
- [Ejecucion local del proyecto](#ejecucion-local-del-proyecto)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Advertencias y precauciones](#advertencias-y-precauciones)

---

### Descripcion del servicio

**PrototiposExpress** es un servicio de prototipado rapido que transforma conceptos e ideas en prototipos funcionales reales de software y hardware, sin costo inicial para el cliente. El equipo esta compuesto por **6 tecnicos altamente capacitados** con movilizacion propia y experiencia comprobada en industrias exigentes como casinos, financieras, retail y banca.

La propuesta de valor es simple: el cliente no arriesga nada. PrototiposExpress desarrolla un prototipo funcional, el cliente lo prueba en su entorno real, y solo si encuentra valor tangible, se acuerda un modelo de pago justo.

---

### Principio de funcionamiento

El servicio opera bajo un modelo de **captura de necesidad - prototipado - testeo gratuito - pago por valor**:

```
Solicitud de reunion
        |
        v
Captura de necesidad y deadline
        |
        v
Desarrollo de prototipo funcional (sin costo)
        |
        v
Periodo de pruebas sin compromiso
        |
        v
Si hay valor real -> Pago por servicio
Si no hay valor -> Sin costo, sin compromiso
```

#### Detalle del ciclo

1. **Solicitud de reunion**: El cliente completa un formulario en la landing page con sus datos, descripcion de la necesidad y plazo deseado.
2. **Analisis de requerimientos**: El equipo de PrototiposExpress se reune con el cliente (presencial o virtual) para entender a fondo el problema, el alcance y las restricciones tecnicas.
3. **Prototipado funcional**: Se desarrolla un prototipo real y funcional de la solucion, utilizando las tecnologias mas adecuadas para el caso.
4. **Pruebas sin costo**: El cliente recibe el prototipo y lo evalua en su entorno real durante el periodo acordado, sin ningun compromiso de pago.
5. **Pago por valor**: Si el prototipo demuestra valor real para el negocio del cliente, se acuerda un modelo de servicio justo. En caso contrario, no hay costo alguno.

---

### Tecnologias ofrecidas

PrototiposExpress abarca **9 areas tecnologicas** para cubrir practicamente cualquier necesidad de prototipado:

| Categoria | Tecnologias | Aplicaciones tipicas |
|-----------|-------------|---------------------|
| **Web** | Frontend + Backend (HTML, CSS, JavaScript, Python, etc.) | Aplicaciones web completas, paneles de control, portales |
| **Escritorio Windows** | .exe, .msi, .NET, C++ | Programas nativos Windows con interfaz grafica profesional |
| **Escritorio Linux (Debian)** | GTK, Qt, Python, aplicaciones nativas | Software para distribuciones Debian y derivadas (Ubuntu, Mint) |
| **Servicios / APIs** | Flask, REST, microservicios, procesos background | APIs REST, automatizacion, integracion de sistemas |
| **Hardware WiFi** | ESP32, ESP8266 | IoT, sensores inalambricos, domotica, monitoreo remoto |
| **Bluetooth / BLE** | HC-05, HC-06, nRF, BLE | Comunicacion inalambrica de corto alcance, beacons, perifericos |
| **LoRa** | SX127x, Heltec, LPWAN | Comunicacion de largo alcance y bajo consumo, sensores remotos |
| **Ethernet** | Conexion por cable, servidores embebidos | IoT industrial, sistemas criticos, comunicacion cableada |
| **Radiofrecuencia** | 433 MHz, 315 MHz, nRF24L01 | Telemetria, control remoto, sensores inalambricos de bajo costo |

---

### Arquitectura del sistema

El proyecto es un **sitio 100% estatico** (HTML + CSS + JS plano) optimizado para **Netlify**. El formulario de contacto utiliza **Netlify Forms**, que captura los datos automaticamente y los entrega via notificacion por email sin necesidad de backend.

```
+------------------------------------------------------------------+
|                    NETLIFY (Hosting + Forms)                       |
|                                                                   |
|   https://prototiposexpress.netlify.app/                           |
|          |                                                         |
|   GET /  --------->  frontend/index.html  (Landing page)          |
|   GET /css/* ----->  styles.css  (Estilos y animaciones)          |
|   GET /js/* ------>  main.js     (Logica de cliente)              |
|          |                                                         |
|   POST / (Form AJAX) ---> Netlify Forms captura los datos         |
|          |                    y envia notificacion email           |
|   +------------------------------------------------------------+  |
|   | Frontend:                                                   |  |
|   | - Landing page profesional                                  |  |
|   | - Formulario de contacto con validacion en tiempo real      |  |
|   | - Animaciones de scroll con Intersection Observer           |  |
|   | - Diseño responsive (320px a 1920px+)                       |  |
|   | - Navegacion suave entre secciones                          |  |
|   | - Envio AJAX a Netlify Forms                                |  |
|   +------------------------------------------------------------+  |
+------------------------------------------------------------------+
                               |
              Netlify Forms (notificacion email)
                               |
+------------------------------v------------------------------------+
|                       CORREO DESTINO                               |
|                                                                   |
|   jmadasme@gmail.com                                               |
|   (configurable desde dashboard Netlify)                          |
+------------------------------------------------------------------+
```

> **Nota**: Localmente, el formulario envia los datos a Netlify Forms solo cuando el sitio esta desplegado en Netlify. Para desarrollo local, el formulario mostrara un mensaje de confirmacion simulado (ver seccion de Ejecucion Local).

#### Flujo de datos del formulario

1. El usuario completa el formulario en la landing page y hace clic en "Enviar solicitud".
2. El frontend (main.js) valida cada campo en tiempo real: campos vacios, formato de email, formato de telefono, fecha valida.
3. Si la validacion es exitosa, se realiza una peticion `fetch POST /api/contacto` con un JSON que contiene `{nombre, email, telefono, empresa, necesidad, plazo}`.
4. El backend Flask recibe los datos, los valida nuevamente (doblez defensivo), compone un email con formato HTML profesional y lo envia via SMTP de Gmail.
5. El backend responde con `{"status": "ok"}` en caso de exito, o `{"status": "error", "message": "..."}` en caso de error.
6. El frontend muestra un mensaje de exito o error al usuario segun la respuesta.

---

### Forma de operar (para el cliente)

#### Paso 1: Acceder a la landing page

Abre la pagina web de PrototiposExpress en tu navegador. La pagina se carga con un diseno moderno y oscuro, con navegacion superior fija.

#### Paso 2: Conocer el servicio

Navega por las secciones para entender como funciona el servicio, que tecnologias ofrecemos y en que industrias tenemos experiencia:
- **Como funciona**: Explica el pipeline de 5 pasos.
- **Tecnologias**: Muestra las 9 areas tecnologicas que dominamos.
- **Industrias**: Sectores donde tenemos experiencia comprobada.
- **Equipo**: Informacion sobre los 6 tecnicos.
- **Por que nosotros**: Diferenciadores clave.

#### Paso 3: Solicitar una reunion

Desplazate hasta la seccion "Solicita tu reunion" (o haz clic en el boton "Solicitar reunion" en el menu de navegacion). Completa el formulario con:

- **Nombre completo**: Tu nombre o el de tu empresa.
- **Correo electronico**: Un email valido donde recibir la respuesta.
- **Telefono**: Numero de contacto.
- **Empresa**: Nombre de tu organizacion.
- **Describe tu necesidad**: Explica tu idea, el problema que resuelve y la tecnologia que imaginas. Cuanto mas detalle, mejor.
- **Plazo deseado**: Fecha estimada en la que necesitas el prototipo.

#### Paso 4: Envio y confirmacion

Haz clic en "Enviar solicitud". Recibiras una confirmacion visual en la pagina indicando que tu solicitud fue enviada con exito. El equipo de PrototiposExpress te contactara en un maximo de **24 horas** para agendar una reunion sin compromiso.

#### Paso 5: Reunion y prototipado

Tras la reunion, el equipo analizara tus requerimientos y desarrollara un prototipo funcional. Recibiras el prototipo para pruebas sin ningun costo inicial.

---

### Ejemplos de uso

#### Ejemplo 1: Sistema de monitoreo de temperatura con LoRa

Un cliente del sector agricola necesita monitorear la temperatura de sus invernaderos en tiempo real:

1. **Solicitud**: Completa el formulario indicando necesidad de monitoreo IoT, plazo de 3 semanas.
2. **Reunion**: Se acuerda usar sensores con modulo LoRa SX1278 para largo alcance.
3. **Prototipo**: Se entregan 3 nodos sensores con LoRa + gateway central con dashboard web.
4. **Pruebas**: El cliente instala los sensores en sus invernaderos durante 2 semanas.
5. **Resultado**: El sistema funciona correctamente, reduciendo perdidas en un 15%. Se acuerda un servicio de mantenimiento y escalado.

#### Ejemplo 2: Aplicacion de escritorio para gestion de inventario

Un retail necesita una aplicacion Windows para gestionar inventario en local:

1. **Solicitud**: Formulario describiendo la necesidad de una app .exe con base de datos local.
2. **Reunion**: Se definen funcionalidades: escaneo de codigos de barras, reportes, exportacion a Excel.
3. **Prototipo**: Se entrega un instalador .msi con la aplicacion funcional.
4. **Pruebas**: El cliente prueba en 3 sucursales durante 1 mes.
5. **Resultado**: La aplicacion agiliza el inventario en un 40%. Se acuerda licenciamiento por sucursal.

#### Ejemplo 3: API REST para integracion bancaria

Una fintech necesita una API para procesar pagos:

1. **Solicitud**: Formulario detallando la necesidad de una API REST con autenticacion.
2. **Reunion**: Se definen endpoints, esquemas de datos, requisitos de seguridad.
3. **Prototipo**: Se entrega API Flask con documentacion Swagger, endpoints funcionales.
4. **Pruebas**: El equipo de la fintech integra la API en su entorno de pruebas.
5. **Resultado**: La API maneja 1000 transacciones/min sin errores. Se firma contrato anual.

---

### Requisitos del sistema

#### Para ejecutar el frontend

- Cualquier navegador web moderno (Chrome, Firefox, Edge, Safari).
- No requiere instalacion de dependencias. El frontend es estatico (HTML + CSS + JS).
- Conexion a internet para cargar FontAwesome desde CDN.

#### Para ejecutar el backend

- **Python 3.9+** instalado en el sistema.
- **pip** (gestor de paquetes de Python).
- Acceso a internet para envio de correos SMTP.
- Cuenta de Gmail con **contraseña de aplicacion** configurada.

#### Compatibilidad de navegadores

| Navegador | Version minima | Estado |
|-----------|---------------|--------|
| Google Chrome | 60+ | Compatible |
| Mozilla Firefox | 55+ | Compatible |
| Microsoft Edge | 79+ | Compatible |
| Apple Safari | 12+ | Compatible |

---

### Configuracion del correo electronico

El backend utiliza Gmail SMTP para enviar los correos. Es necesario configurar una **contraseña de aplicacion** de Gmail, ya que Google no permite el uso de la contraseña normal de la cuenta para accesos SMTP desde aplicaciones externas.

#### Paso 1: Crear una contraseña de aplicacion en Gmail

1. Inicia sesion en tu cuenta de Google (la que usaras como remitente, por ejemplo `jmadasme@gmail.com`).
2. Ve a tu cuenta de Google: [myaccount.google.com/security](https://myaccount.google.com/security).
3. Activa la **Verificacion en dos pasos** si aun no lo has hecho (es requisito para crear contraseñas de aplicacion).
4. Una vez activada la verificacion en dos pasos, busca "Contraseñas de aplicacion" en el buscador de la pagina de seguridad o ve a: [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).
5. Selecciona "Correo" como aplicacion y "Windows" (u "Otra") como dispositivo.
6. Google generara una contraseña de 16 caracteres (ejemplo: `abcd efgh ijkl mnop`). **Copiala inmediatamente** porque no se mostrara de nuevo.

#### Paso 2: Configurar las variables de entorno

Crea un archivo `.env` en la carpeta `backend/` con el siguiente contenido:

```env
SMTP_USER=jmadasme@gmail.com
SMTP_PASS=abcd efgh ijkl mnop
```

Reemplaza los valores con tu correo y la contraseña de aplicacion generada.

**Nota**: Si usas otro correo como remitente, tambien puedes configurar el destinatario:

```env
SMTP_USER=tu_correo@gmail.com
SMTP_PASS=tu_contraseña_de_aplicacion
TO_EMAIL=jmadasme@gmail.com
```

---

### Despliegue en Netlify (recomendado)

La forma mas rapida de poner el sitio en produccion.

#### Metodo 1: Deploy desde GitHub (automatico)

1. Sube este repositorio a tu cuenta de GitHub.
2. Ve a [app.netlify.com](https://app.netlify.com) e inicia sesion con GitHub.
3. Haz clic en **"Add new site"** → **"Import an existing project"**.
4. Conecta tu repositorio de GitHub.
5. Configuracion automatica (Netlify detectara `netlify.toml`):
   - **Publish directory**: `frontend`
   - **Build command**: *ninguno* (es HTML/CSS/JS plano)
6. Haz clic en **"Deploy site"**.

#### Metodo 2: Deploy manual (drag & drop)

1. Arrastra la carpeta `frontend/` al area de upload en [app.netlify.com/drop](https://app.netlify.com/drop).

#### Configurar notificaciones del formulario

Una vez desplegado:

1. Ve a **Site settings** → **Forms** → **Form notifications**.
2. Agrega una **Email notification** para el formulario `contacto`.
3. Ingresa **jmadasme@gmail.com** como destinatario.
4. Netlify enviara un email cada vez que alguien complete el formulario.

#### (Opcional) Dominio personalizado

En **Site settings** → **Domain management** puedes configurar un dominio propio.

---

### Ejecucion local (desarrollo)

El sitio es 100% estatico, por lo que puedes servirlo con cualquier servidor HTTP simple:

#### Opcion A: Python (mas simple)

```bash
cd proyectos/PrototiposExpress/frontend
python3 -m http.server 8000
# Abrir http://localhost:8000
```

#### Opcion B: Live Server (VS Code)

Con la extension **Live Server**, hacer clic derecho en `index.html` → **"Open with Live Server"**.

#### Opcion C: Backend Flask (con envio real de correos)

Si deseas probar el envio de correos localmente con el backend Flask:

```bash
cd proyectos/PrototiposExpress/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env con SMTP_USER y SMTP_PASS
python app.py
# Abrir http://localhost:5000
```

> **Nota**: Cuando usas el backend Flask, debes cambiar el fetch en `main.js` a `'/api/contacto'` para que funcione localmente (en lugar del endpoint de Netlify Forms).

---

### Estructura del proyecto

```
proyectos/PrototiposExpress/
├── README.md                        <- Este archivo
├── PLAN.md                          <- Plan original del proyecto
├── AUDIT_REPORT.md                  <- Informe de auditoria de codigo
├── netlify.toml                     <- Configuracion de deploy en Netlify
├── frontend/
│   ├── index.html                   <- Landing page (estructura HTML)
│   ├── css/
│   │   └── styles.css               <- Estilos CSS (responsive, animaciones)
│   └── js/
│       └── main.js                  <- Logica frontend (navegacion, formulario, animaciones)
├── backend/                         <- Backend Flask (solo para desarrollo local)
│   ├── app.py                       <- Servidor Flask (frontend + API)
│   ├── requirements.txt             <- Dependencias Python
│   ├── .env.example                 <- Plantilla para variables de entorno
│   └── .env                         <- Variables de entorno (NO SUBIR A GIT)
└── docs/
    ├── datasheet.md                 <- Documentacion de usuario y preguntas frecuentes
    └── developer.md                 <- Documentacion tecnica para desarrolladores
```

---

### Advertencias y precauciones

#### Seguridad de credenciales

- **NUNCA subas el archivo `.env`** a repositorios publicos o compartas las credenciales SMTP.
- El archivo `.env` contiene la contraseña de aplicacion de Gmail, que permite enviar correos desde tu cuenta.
- Si accidentalmente subes credenciales a un repositorio publico, cambia inmediatamente tu contraseña de aplicacion desde la configuracion de Google.
- Para desarrollo local, mantén el `.env` en `backend/.env` (ya esta incluido en `.gitignore` si configuras el repositorio adecuadamente).

#### Configuracion SMTP

- La contraseña de aplicacion de Gmail solo funciona si la **Verificacion en dos pasos** esta activada en la cuenta de Google.
- Si cambias la contraseña de tu cuenta de Google, las contraseñas de aplicacion existentes siguen funcionando. Si las revocas, debes generar nuevas.
- Gmail impone limites de envio: maximo 500 destinatarios por dia y 2,000 mensajes por dia (para cuentas gratuitas).

#### Produccion

- El servidor Flask incluido es para **desarrollo**. En produccion, usa un servidor WSGI como Gunicorn o uWSGI.
- Configura variables de entorno en el servidor de produccion, no uses archivos `.env` en entornos productivos a menos que esten correctamente protegidos.
- Considera usar HTTPS en produccion para proteger la comunicacion entre frontend y backend.
- Si despliegas en Render, Railway, Heroku o similar, configura las variables de entorno desde el panel de administracion de la plataforma.

#### Compatibilidad

- El frontend usa Intersection Observer API, que es compatible con navegadores modernos pero puede no funcionar en navegadores muy antiguos. main.js incluye un fallback para esta situacion.
- El formulario requiere JavaScript habilitado para funcionar. Sin JS, el formulario no se enviara.
- FontAwesome se carga desde CDN. Sin conexion a internet, los iconos no se mostraran (pero el resto de la pagina funciona).

#### Privacidad

- Los datos del formulario se envian por correo electronico sin cifrado de extremo a extremo. Se recomienda no enviar informacion altamente sensible a traves del formulario.
- Los datos se almacenan unicamente en el correo de destino. No hay base de datos asociada al proyecto.

---

### Licencia

Este proyecto es de codigo abierto. Todos los derechos reservados 2026 PrototiposExpress.

---

Licencia MIT © 2026 jmadasme. Las versiones se publican como material de
referencia; los nombres de hardware y marcas pertenecen a sus respectivos dueños.
