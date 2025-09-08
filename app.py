# ----------------------------
# LIBRERIAS Y DEMAS
# ----------------------------

from flask import Flask, render_template, request, send_file, session, redirect, url_for, Response
from PIL import Image
import stepic
import io
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))  # Necesario para session

# ----------------------------
# DOMINIOS
# ----------------------------

# Página principal
@app.route("/")
def index():
    return render_template("index.html")

# Ocultar mensaje en imagen
@app.route("/hide", methods=["POST"])
def hide():
    try:
        file = request.files["image"]
        message = request.form["message"]

        if not file or not message:
            return render_template("error.html", error="Falta imagen o mensaje.")

        img = Image.open(file.stream)
        encoded = stepic.encode(img, message.encode("utf-8"))

        # Guardamos en memoria
        img_io = io.BytesIO()
        encoded.save(img_io, format="PNG")
        img_io.seek(0)

        return send_file(
            img_io,
            mimetype="image/png",
            as_attachment=True,
            download_name="hidden.png"
        )
    except Exception as e:
        return render_template("error.html", error=f"Error ocultando: {str(e)}")

# Revelar mensaje de imagen
@app.route("/reveal", methods=["POST"])
def reveal():
    try:
        file = request.files["image"]

        if not file:
            return render_template("error.html", error="No subiste ninguna imagen.")

        img = Image.open(file.stream)
        msg = stepic.decode(img)  # stepic ya devuelve str en Python 3

        if not msg:
            return render_template("error.html", error="No se encontró mensaje oculto.")

        return render_template("result.html", message=msg)

    except Exception as e:
        return render_template("error.html", error=f"Error revelando: {str(e)}")

# Subdominio de prueba
@app.route("/osiudhf")
def easter_egg():
    return "<h1 style='color:white; text-align:center; margin-top:50px;'>🐱‍👤 Te metiste al subdominio secreto localhost:5000/osiudhf</h1>"

# Acerca de
@app.route("/about")
def about():
    return render_template("about.html")

# Créditos
@app.route("/credits")
def credits():
    return render_template("credits.html")

# ----------------------------
# COSAS DE ADMINS
# ----------------------------

# Página de login
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Solo un admin hardcodeado para este ejemplo
        if username == "admin" and password == "1234":
            session["admin"] = username
            return redirect(url_for("admin_panel"))
        return render_template("login.html", error="Usuario o contraseña incorrecta")

    return render_template("login.html")

# Panel admin
@app.route("/admin")
def admin_panel():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    return render_template("admin.html")

# Logout opcional
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("index"))

# Revisar actividad reciente
@app.route("/admin/activity")
def admin_activity():
    return render_template("admin_activity.html")

# Administrar usuarios
@app.route("/admin/users")
def admin_users():
    return render_template("admin_users.html")

# Configurar sistema
@app.route("/admin/settings")
def admin_settings():
    return render_template("admin_settings.html")


# ----------------------------
# ARCHIVOS .TXT
# ----------------------------

# robots.txt
@app.route("/robots.txt")
def robots():
    try:
        with open("txt/robots.txt", "r", encoding="utf-8") as f:
            content = f.read()
        return Response(content, mimetype="text/plain")
    except FileNotFoundError:
        return "Archivo robots.txt no encontrado", 404

# humans.txt
@app.route("/humans.txt")
def humans():
    try:
        with open("txt/humans.txt", "r", encoding="utf-8") as f:
            content = f.read()
        return Response(content, mimetype="text/plain")
    except FileNotFoundError:
        return "Archivo humans.txt no encontrado", 404
    
# intro.txt
@app.route("/intro.txt")
def intro_txt():
    try:
        with open("txt/intro.txt", "r", encoding="utf-8") as f:
            content = f.read()
        return Response(content, mimetype="text/plain")
    except FileNotFoundError:
        return "Archivo intro.txt no encontrado", 404 

# ----------------------------
# MANEJADORES DE ERRORES
# ----------------------------

# Página 404 → 404.html
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Página 405 → error.html
@app.errorhandler(405)
def method_not_allowed(e):
    return render_template("error.html", error="Error 405: El método no está permitido para esta URL."), 405

# Error interno 500 → error.html
@app.errorhandler(500)
def internal_error(e):
    return render_template("error.html", error="Error 500: Ha ocurrido un error interno en el servidor."), 500

# ----------------------------
# Ejecutar app en una web
# ----------------------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Usa el puerto del hosting, si no 5000
    debug_mode = os.environ.get("FLASK_DEBUG", "1") == "1"  # Opcional, controlable
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
