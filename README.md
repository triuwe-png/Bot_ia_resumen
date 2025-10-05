# Bot IA Resumidos

Aplicación web sencilla (Flask) que permite subir texto, PDF o DOCX y generar un resumen con la API de OpenAI. Incluye descarga del resumen en TXT (el usuario puede elegir el nombre).

---

## Estructura del proyecto

```
bot-ia-resumidos/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── uploads/
└── .gitignore
```

---

## Requisitos locales

- Python 3.10+ (recomendado)
- Una API Key de OpenAI

Instala dependencias:
```bash
pip install -r requirements.txt
```

Crea un archivo `.env` (NO lo subas a GitHub) con:
```
OPENAI_API_KEY=tu_clave_aqui
```

Ejecuta localmente:
```bash
python app.py
```
Abre: `http://127.0.0.1:10000`

---

## Deploy en Render.com (paso a paso)

1. **Crear cuenta en Render**  
   Ve a https://render.com y crea una cuenta (puedes conectar con GitHub).

2. **Subir el proyecto a GitHub**  
   - Crea un nuevo repositorio (por ejemplo `bot-ia-resumidos`).
   - Asegúrate de incluir todos los archivos excepto `.env` (usa `.gitignore` provisto).
   - Haz commit y push al repo.

3. **Crear un Web Service en Render**  
   - En el panel de Render haz clic en **New +** → **Web Service**.
   - Conecta tu cuenta de GitHub y selecciona el repositorio `bot-ia-resumidos`.
   - Configura:
     - **Name:** bot-ia-resumidos
     - **Environment:** Python
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python app.py`
   - En **Advanced** → **Environment** variables, agrega:
     - `OPENAI_API_KEY` = `sk-...` (tu clave real de OpenAI)

4. **Deploy**  
   - Render instalará dependencias y desplegará la app. Espera hasta que el estado sea `Live`.
   - Obtendrás una URL pública tipo `https://bot-ia-resumidos.onrender.com`.

5. **Probar**  
   - Abre la URL pública. Sube un PDF o pega texto y genera un resumen.
   - Prueba la descarga del resumen con el nombre personalizado.

---

## Notas y recomendaciones

- No subas tu `.env` ni la clave de OpenAI a GitHub.
- Si deseas ejecutar con más rendimiento en producción, puedes usar Gunicorn:
  - Instala `gunicorn` y cambia el start command en Render a: `gunicorn app:app --bind 0.0.0.0:$PORT`
- Si el modelo seleccionado no está disponible o quieres otro, edita `model="gpt-4o-mini"` en `app.py`.
- Para soporte con Stripe/PayPal o guardar resúmenes en la nube (Firebase/DB), puedo ayudarte a extender el proyecto.

---

## Autor
Hecho con 💚 por David Castaño
