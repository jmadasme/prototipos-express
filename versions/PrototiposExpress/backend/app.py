"""
PrototiposExpress — Backend API (Flask)
========================================
Endpoints:
  - GET  /                Sirve el frontend estático (landing page)
  - GET  /<path:path>     Sirve archivos estáticos del frontend (CSS, JS, etc.)
  - POST /api/contacto    Recibe datos del formulario y envía email vía SMTP Gmail
  - GET  /health          Health check

Configuración vía variables de entorno:
  - SMTP_USER  (ej: jmadasme@gmail.com)
  - SMTP_PASS  (contraseña de aplicación de Gmail)
Variables opcionales:
  - TO_EMAIL   (destinatario, por defecto jmadasme@gmail.com)

Ejecutar desde el directorio raíz del proyecto o desde backend/.
"""

import os
import re
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Ruta base del frontend (relativa a este archivo)
# ---------------------------------------------------------------------------
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

# ---------------------------------------------------------------------------
# Configuración básica
# ---------------------------------------------------------------------------
load_dotenv()

app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
)
logger = logging.getLogger("prototiposexpress")

# ---------------------------------------------------------------------------
# Constantes SMTP
# ---------------------------------------------------------------------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
TO_EMAIL = os.getenv("TO_EMAIL", "jmadasme@gmail.com")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def compose_email_html(data: dict) -> str:
    """Compone un email HTML formateado con los datos del formulario."""
    nombre = _escape_html(data.get("nombre", ""))
    email = _escape_html(data.get("email", ""))
    telefono = _escape_html(data.get("telefono", ""))
    empresa = _escape_html(data.get("empresa", ""))
    necesidad = _escape_html(data.get("necesidad", ""))
    plazo = _escape_html(data.get("plazo", ""))

    return f"""\
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f9; margin: 0; padding: 0;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background: #f4f6f9; padding: 40px 20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="background: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 8px 30px rgba(0,0,0,0.08);">
          <tr>
            <td style="background: linear-gradient(135deg, #06b6d4, #3b82f6); padding: 32px 40px; text-align: center;">
              <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🛠️ Nueva Solicitud de Reunión</h1>
              <p style="color: rgba(255,255,255,0.85); margin: 8px 0 0; font-size: 15px;">PrototiposExpress — Lead Capturado</p>
            </td>
          </tr>
          <tr>
            <td style="padding: 32px 40px;">
              <table width="100%" cellpadding="0" cellspacing="0" style="font-size: 15px; color: #1e293b;">
                <tr>
                  <td style="padding: 10px 0; border-bottom: 1px solid #e2e8f0;">
                    <strong style="color: #64748b; display: inline-block; width: 130px;">Nombre:</strong>
                    {nombre}
                  </td>
                </tr>
                <tr>
                  <td style="padding: 10px 0; border-bottom: 1px solid #e2e8f0;">
                    <strong style="color: #64748b; display: inline-block; width: 130px;">Email:</strong>
                    <a href="mailto:{email}" style="color: #06b6d4;">{email}</a>
                  </td>
                </tr>
                <tr>
                  <td style="padding: 10px 0; border-bottom: 1px solid #e2e8f0;">
                    <strong style="color: #64748b; display: inline-block; width: 130px;">Teléfono:</strong>
                    {telefono}
                  </td>
                </tr>
                <tr>
                  <td style="padding: 10px 0; border-bottom: 1px solid #e2e8f0;">
                    <strong style="color: #64748b; display: inline-block; width: 130px;">Empresa:</strong>
                    {empresa}
                  </td>
                </tr>
                <tr>
                  <td style="padding: 10px 0; border-bottom: 1px solid #e2e8f0;">
                    <strong style="color: #64748b; display: inline-block; width: 130px;">Plazo deseado:</strong>
                    {plazo}
                  </td>
                </tr>
                <tr>
                  <td style="padding: 14px 0;">
                    <strong style="color: #64748b; display: block; margin-bottom: 8px;">Necesidad:</strong>
                    <p style="margin: 0; background: #f8fafc; padding: 16px; border-radius: 8px; line-height: 1.6; white-space: pre-wrap;">{necesidad}</p>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="background: #f8fafc; padding: 20px 40px; text-align: center; border-top: 1px solid #e2e8f0;">
              <p style="margin: 0; color: #94a3b8; font-size: 13px;">
                Este lead fue capturado desde el formulario de <strong>PrototiposExpress</strong>.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def _escape_html(text: str) -> str:
    """Escapa caracteres HTML para prevenir inyección."""
    replacements = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#x27;",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def send_contact_email(data: dict) -> None:
    """Envía el email con los datos de contacto vía SMTP Gmail."""
    msg = MIMEMultipart("alternative")
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL
    msg["Subject"] = f"🛠️ Nueva solicitud - {data.get('nombre', '')} de {data.get('empresa', '')}"

    html_content = compose_email_html(data)
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)


def validate_contact_data(data: dict) -> tuple[bool, str]:
    """
    Valida los campos requeridos del formulario.
    Retorna (es_válido, mensaje_de_error).
    """
    required_fields = {
        "nombre": "nombre",
        "email": "correo electrónico",
        "telefono": "teléfono",
        "empresa": "empresa",
        "necesidad": "necesidad",
        "plazo": "plazo",
    }

    for field_key, field_label in required_fields.items():
        value = data.get(field_key, "")
        if not value or not isinstance(value, str) or not value.strip():
            return False, f"El campo '{field_label}' es obligatorio."

    # Validar formato de email
    email = data.get("email", "").strip()
    if not re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "El formato del correo electrónico no es válido."

    return True, ""


# ---------------------------------------------------------------------------
# Frontend estático
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def serve_index():
    """Sirve la landing page principal."""
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.route("/<path:path>", methods=["GET"])
def serve_static(path):
    """Sirve archivos estáticos (CSS, JS, imágenes, etc.) del frontend."""
    file_path = os.path.join(FRONTEND_DIR, path)
    # Seguridad: evitar directory traversal
    if not os.path.abspath(file_path).startswith(FRONTEND_DIR):
        return jsonify({"error": "Acceso denegado"}), 403
    if os.path.isfile(file_path):
        return send_from_directory(FRONTEND_DIR, path)
    # Fallback: si no existe el archivo, servir index.html (SPA-like)
    return send_from_directory(FRONTEND_DIR, "index.html")


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"}), 200


@app.route("/api/contacto", methods=["POST"])
def contacto():
    """
    Recibe datos del formulario, valida y envía email.
    Espera JSON con: nombre, email, telefono, empresa, necesidad, plazo
    """
    # Validar Content-Type
    if not request.is_json:
        return jsonify({"status": "error", "message": "Content-Type debe ser application/json."}), 400

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "error", "message": "El cuerpo de la solicitud no es válido."}), 400

    # Validar campos
    is_valid, error_msg = validate_contact_data(data)
    if not is_valid:
        return jsonify({"status": "error", "message": error_msg}), 400

    # Verificar que SMTP esté configurado
    if not SMTP_USER or not SMTP_PASS:
        logger.error("SMTP_USER o SMTP_PASS no están configurados en las variables de entorno.")
        return jsonify({"status": "error", "message": "Error de configuración del servidor de correo."}), 500

    try:
        send_contact_email(data)
        logger.info("Email enviado exitosamente a %s", TO_EMAIL)
        return jsonify({"status": "ok", "message": "Solicitud enviada con éxito."}), 200
    except smtplib.SMTPAuthenticationError:
        logger.error("Error de autenticación SMTP. Verifica SMTP_USER y SMTP_PASS.")
        return jsonify({"status": "error", "message": "Error de autenticación con el servidor de correo."}), 500
    except smtplib.SMTPException as exc:
        logger.error("Error SMTP al enviar email: %s", exc)
        return jsonify({"status": "error", "message": "Error al enviar el correo. Intenta nuevamente."}), 500
    except Exception as exc:
        logger.error("Error inesperado: %s", exc)
        return jsonify({"status": "error", "message": "Error interno del servidor."}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    if not SMTP_USER or not SMTP_PASS:
        logger.warning(
            "SMTP_USER y/o SMTP_PASS no están configurados. "
            "Crea un archivo .env en backend/ con esas variables."
        )

    logger.info("Iniciando servidor PrototiposExpress en puerto %d (debug=%s)", port, debug)
    print(f"\n🌐 Landing page: http://localhost:{port}/")
    print(f"🔗 API endpoint:  http://localhost:{port}/api/contacto")
    print(f"❤️  Health check:  http://localhost:{port}/health\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
