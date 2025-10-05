from flask import Flask, render_template, request, make_response
from openai import OpenAI
from dotenv import load_dotenv
import os
import PyPDF2
from docx import Document
from werkzeug.utils import secure_filename

# Cargar variables de entorno
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_KEY:
    print("WARNING: OPENAI_API_KEY no encontrada en variables de entorno. Añádela antes de ejecutar la app.")

client = OpenAI(api_key=OPENAI_KEY)

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def extraer_texto_pdf(path):
    texto = ""
    with open(path, "rb") as archivo:
        lector = PyPDF2.PdfReader(archivo)
        for pagina in lector.pages:
            try:
                texto += pagina.extract_text() or ""
            except Exception:
                pass
    return texto

def extraer_texto_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def generar_resumen(texto, nivel="corto"):
    # Limitar tamaño del prompt para evitar excesos
    texto_acotado = texto[:12000]
    prompt = f"Resume el siguiente texto en un nivel {nivel}:\n\n{texto_acotado}"

    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=600
    )

    resumen = ""
    try:
        resumen = respuesta.choices[0].message.content.strip()
    except Exception:
        resumen = "Error al generar el resumen. Revisa tu clave y los límites del modelo."
    return resumen

@app.route("/", methods=["GET", "POST"])
def index():
    resumen = ""
    origen = ""
    if request.method == "POST":
        nivel = request.form.get("nivel", "corto")
        texto = request.form.get("texto", "").strip()
        archivo = request.files.get("archivo")

        contenido = texto

        if archivo and archivo.filename != "":
            nombre_archivo = secure_filename(archivo.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], nombre_archivo)
            archivo.save(path)

            if nombre_archivo.lower().endswith(".pdf"):
                contenido = extraer_texto_pdf(path)
                origen = nombre_archivo
            elif nombre_archivo.lower().endswith(".docx"):
                contenido = extraer_texto_docx(path)
                origen = nombre_archivo
            else:
                contenido = "Formato no soportado. Sube un PDF o Word (.docx)."

        if contenido:
            resumen = generar_resumen(contenido, nivel)

    return render_template("index.html", resumen=resumen, origen=origen)

@app.route("/download", methods=["POST"])
def download():
    resumen = request.form.get("resumen_text", "")
    filename = request.form.get("filename", "resumen.txt").strip()
    if not filename:
        filename = "resumen.txt"
    if not filename.lower().endswith(".txt"):
        filename += ".txt"

    # Crear respuesta con attachment
    response = make_response(resumen)
    response.headers.set("Content-Type", "text/plain; charset=utf-8")
    response.headers.set("Content-Disposition", f"attachment; filename={filename}")
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    # No activar debug en producción
    app.run(host="0.0.0.0", port=port)
