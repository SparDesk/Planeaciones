# Planeaciones Escolares Educación Primaria 🇲🇽

Sistema web interactivo profesional para la generación automatizada de **Planeaciones Escolares de Primaria**, diseñado con base estricta en el modelo pedagógico de la **Nueva Escuela Mexicana (NEM)** de la **Secretaría de Educación Pública (SEP)**.

---

## 🏛️ Ficha Técnica Institucional Predeterminada

* **Institución Educativa:** Primaria Revolución Social 1910
* **Clave de Centro de Trabajo (C.C.T.):** `10EPR0361N`
* **Docente Titular:** Prof(a). Aday Domínguez Domínguez
* **Director Escolar:** Prof. José Guillermo Borjas Díaz
* **Grado y Fase:** 5° de Primaria (Fase 5) — Grupo "A"
* **Temporalidad Predeterminada:** Semana 20 (5 sesiones semanales)
* **Ciclo Escolar:** 2025-2026

---

## 🚀 Características Principales

1. **Alineación Estricta al Modelo NEM (SEP - México):**
   - **Campos Formativos:** *Lenguajes*, *Saberes y Pensamiento Científico*, *Ética, Naturaleza y Sociedades*, y *De lo Humano y lo Comunitario*.
   - **Metodologías Sociocríticas Oficiales:**
     * *Aprendizaje Basado en Proyectos Comunitarios* (Fases 1, 2 y 3 y sus 11 momentos).
     * *Aprendizaje Basado en Indagación (STEAM como enfoque)*.
     * *Aprendizaje Basado en Problemas (ABPr)* (6 momentos).
     * *Aprendizaje Servicio (AS)* (5 etapas).
   - **Ejes Articuladores:** Inclusión, Pensamiento crítico, Interculturalidad crítica, Igualdad de género, Vida saludable, Apropiación de las culturas a través de la lectura y la escritura, Artes y experiencias estéticas.

2. **Estructura Didáctica Oficial (Plano Didáctico):**
   - **Dosificador General del Proyecto:** Propósito, escenario (Aula, Escuela o Comunidad), temporalidad y vinculación.
   - **Articulación Curricular:** Contenidos sintéticos y Procesos de Desarrollo de Aprendizaje (PDA) oficiales de Fase 5 / 5° Grado.
   - **Actividades de Inicio del Día (Rutina Matutina):** Dictado ortográfico, cálculo mental ágil y problema matemático razonado diario para las 5 sesiones de la semana.
   - **Secuencia Didáctica Detallada:** Actividades divididas rigurosamente en momentos de **Inicio** (15-20 min), **Desarrollo** (50-60 min) y **Cierre** (15-20 min), con cita de páginas recomendadas de los **Libros de Texto Gratuitos (LTG)** de la SEP (*Proyectos Comunitarios*, *Proyectos de Aula*, *Nuestros Saberes*, *Múltiples Lenguajes*).
   - **Evaluación Formativa:** Rúbrica analítica por niveles de desempeño (Sobresaliente, Satisfactorio, Básico, Requiere Apoyo).
   - **Inclusión y Equidad:** Estrategias de adecuaciones curriculares y ajustes razonables basadas en el Diseño Universal para el Aprendizaje (DUA) y atención a BAP.

3. **Carga Inteligente de Documentos (Local y Nube):**
   - Soporte para archivos `.pdf`, `.docx` y `.txt` (programas sintéticos, libros SEP, guías de Consejo Técnico Escolar).
   - Área libre para notas docentes y problemáticas del Plan Analítico.

4. **Generación y Descarga en Múltiples Formatos (Estructura Original):**
   - **Microsoft Word (.docx):** Replicación exacta utilizando como plantilla base la estructura del documento de referencia (*"5° SEM20 ADAY DOMINGUEZ 5° CICLO 25-26.docx"*), conservando:
     * El formato del **Horario Escolar Semanal** y el **Dosificador General de Proyectos de Intervención**.
     * Los encabezados institucionales y logos.
     * La división en tablas por días (Lunes a Viernes), separando **"Actividades de Inicio del Día"** (Dictado, Cálculo mental y Problema matemático) y la **"Secuencia de Actividades"** (Inicio, Desarrollo y Cierre).
     * Los espacios para Recursos didácticos, Evaluación formativa, Adecuaciones Curriculares y firmas institucionales de **Aday Domínguez Domínguez** (Docente) y **José Guillermo Borjas Díaz** (Director).
   - **Formato PDF (.pdf):** Generación limpia universal con `fpdf2` (sin dependencias binarias externas) lista para impresión oficial.
   - **Texto Estructurado Markdown (.md):** Para edición en plataformas digitales o notas docentes.

---

5. **Conexión Web en Tiempo Real con CONALITEG:**
   - Web scraping dinámico con `requests` y `BeautifulSoup` al portal oficial de la Comisión Nacional de Libros de Texto Gratuitos (URL: `https://libros.conaliteg.gob.mx/primaria_2025.html`).
   - Extracción automatizada de los títulos vigentes del ciclo 2025-2026 clasificados por grado (1° a 6°).
   - Mecanismo de alta resiliencia (`try-except`) con diccionario de respaldo (*fallback*) de la Nueva Escuela Mexicana ante caídas del servidor gubernamental o problemas de red.

---

## 🛠️ Requisitos Técnicos y Dependencias

El proyecto utiliza la SDK oficial de Google (`google-genai`), `python-docx` para la replicación del Word oficial, `fpdf2` para PDFs universales, `requests` y `beautifulsoup4` para la extracción en vivo de CONALITEG, y garantiza compatibilidad con WebSockets (`websockets<14.0`):

* `streamlit>=1.35.0`
* `websockets<14.0`
* `google-genai>=2.0.0`
* `python-docx>=1.1.0`
* `fpdf2>=2.7.0`
* `PyPDF2>=3.0.0`
* `pypdf>=5.0.0`
* `requests>=2.31.0`
* `beautifulsoup4>=4.12.0`
* `python-dotenv>=1.0.0`

---

## 💻 Instalación y Ejecución Local

### Paso 1: Clonar o descargar el repositorio
```bash
git clone <url-del-repositorio>
cd "Nueva carpeta"
```

### Paso 2: Crear y activar un entorno virtual
**En Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**En Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Paso 3: Instalar las dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Configurar la API Key de Gemini
Puedes definir la variable en un archivo `.env`:
```env
GEMINI_API_KEY=tu_clave_de_gemini_aqui
```
O ingresarla directamente en el campo seguro de la barra lateral de la aplicación.
*(Obtén tu clave gratuita en [Google AI Studio](https://aistudio.google.com/)).*

### Paso 5: Iniciar la aplicación
```bash
streamlit run app.py
```
La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`.

---

## ☁️ Despliegue en la Nube (Streamlit Community Cloud)

1. Sube este proyecto a tu repositorio de GitHub.
2. Ingresa a [share.streamlit.io](https://share.streamlit.io/) e inicia sesión con tu cuenta de GitHub.
3. Haz clic en **"New app"** y selecciona tu repositorio.
4. En **Main file path**, ingresa: `app.py`.
5. En la sección **Advanced Settings** -> **Secrets**, agrega tu API Key:
   ```toml
   GEMINI_API_KEY = "tu_clave_de_gemini_aqui"
   ```
6. Haz clic en **"Deploy"**. Tu aplicación quedará disponible en línea 24/7 de manera gratuita.

---

## 👥 Créditos y Atribución

* **Institución:** Escuela Primaria Revolución Social 1910 — C.C.T. 10EPR0361N
* **Docente Titular:** Prof(a). Aday Domínguez Domínguez
* **Director de la Escuela:** Prof. José Guillermo Borjas Díaz
* **Marco Normativo:** Secretaría de Educación Pública (SEP) — Plan de Estudios 2022 / Nueva Escuela Mexicana (NEM).
