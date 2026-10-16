"""
Módulo de integración con la SDK oficial de Google GenAI (Gemini)
para la generación automatizada de planeaciones didácticas bajo el modelo NEM (SEP).
"""

import os
import time
import socket
import requests
import streamlit as st
from typing import Dict, Any, Tuple
from google import genai
from google.genai import types
try:
    import httpx
except ImportError:
    httpx = None
try:
    from nem_data import METODOLOGIAS_SOCIOCRITICAS
except ImportError:
    METODOLOGIAS_SOCIOCRITICAS = {}

DEFAULT_MODEL = "gemini-3.8-flash"
AVAILABLE_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.8-pro",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "gemini-1.5-pro"
]

def verificar_conexion_internet(host: str = "www.google.com", port: int = 80, timeout: float = 3.0) -> bool:
    """
    Verifica si existe una conexión activa a internet antes de iniciar la generación de la planeación.
    Utiliza socket para una comprobación rápida a nivel TCP y requests como mecanismo de respaldo
    para validar la conectividad hacia la web y APIs externas.

    Parámetros:
        host (str): Servidor contra el cual comprobar conectividad socket (por defecto: 'www.google.com').
        port (int): Puerto de conexión TCP (por defecto: 80).
        timeout (float): Tiempo máximo de espera en segundos (por defecto: 3.0).

    Retorna:
        bool: True si hay conexión a internet activa, False si no hay red o expira el tiempo de espera.
    """
    # 1. Comprobación rápida vía socket TCP
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        return True
    except (socket.timeout, socket.gaierror, socket.error, OSError, PermissionError):
        pass

    # 2. Respaldo mediante requests HTTP/HTTPS
    try:
        resp = requests.head("https://www.google.com", timeout=timeout)
        if resp.status_code < 500:
            return True
    except Exception:
        pass

    try:
        resp = requests.get("https://www.google.com", timeout=timeout)
        return resp.status_code < 500
    except Exception:
        return False

def get_client(api_key: str = None) -> genai.Client:
    """Crea e inicializa el cliente oficial de Google GenAI."""
    key = api_key or os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("No se proporcionó una GEMINI_API_KEY válida. Ingrésala en la barra lateral o en las variables de entorno.")
    return genai.Client(api_key=key)

def build_system_instruction() -> str:
    """Instrucción de sistema para el rol de Especialista Pedagógico SEP."""
    return """Eres el Especialista Principal en Pedagogía Curricular y Didáctica de la Secretaría de Educación Pública (SEP) de México, experto consumado en el Plan de Estudio 2022 y el modelo de la Nueva Escuela Mexicana (NEM).

Tu misión es diseñar planeaciones didácticas auténticas, contextualizadas, profundas y rigurosamente estructuradas para el trabajo docente en educación primaria (Fases 3, 4 y 5).

REGLAS PEDAGÓGICAS INQUEBRANTABLES:
1. Lenguaje docente mexicano formal, constructivo, inclusivo y orientado a la comunidad.
2. Cada sesión didáctica DEBE estructurarse explícitamente en tres momentos:
   - **Inicio** (Recuperación de conocimientos previos, detonación del interés, problematización, 15-20 min).
   - **Desarrollo** (Construcción colaborativa o individual, indagación, trabajo con libros de texto SEP - LTG, análisis, 50-60 min).
   - **Cierre** (Metacognición, puesta en común comunitaria, síntesis y valoración del aprendizaje, 15-20 min).
3. Incluir las ACTIVIDADES DE INICIO DEL DÍA (rutina matutina permanente de 5 sesiones) con:
   - Dictado reflexivo (5 palabras/enunciados vinculados a la temática).
   - Cálculo mental contextualizado (5 operaciones acordes a la fase y grado).
   - Problema matemático razonado (con datos, operaciones y resultado interpretado).
4. Vinculación estricta con los Libros de Texto Gratuitos (LTG) de la SEP:
   - Cita explícitamente sugerencias de páginas de los libros: Proyectos de Aula / Escolares / Comunitarios, Nuestros Saberes y Múltiples Lenguajes.
5. Evaluación formativa real: Evitar generalidades; describe criterios observables y diseña un instrumento concreto (como rúbrica analítica o lista de cotejo con indicadores claros de logro).
6. Ajustes razonables / Inclusión: Estrategias de atención a la diversidad (DUA) y barreras para el aprendizaje y la participación (BAP).
"""

def generate_planeacion(
    datos_escuela: Dict[str, Any],
    campos_formativos: list,
    metodologia: str,
    ejes_articuladores: list,
    contenidos_pda: list,
    directrices_docente: str,
    contexto_archivos: str = "",
    libros_seleccionados: list = None,
    guia_cte: str = None,
    programa_sintetico: str = None,
    dias_seleccionados: list = None,
    num_sesiones: int = 5,
    api_key: str = None,
    modelo: str = DEFAULT_MODEL,
    busqueda_web: bool = False,
    contexto_url: str = "",
    **kwargs
) -> Tuple[str, str]:
    """
    Envía la solicitud a Gemini usando la SDK oficial de Google GenAI y retorna el texto generado,
    articulando dinámicamente Libros de Texto SEP, Guía del CTE, Programa Sintético y contexto web.
    
    Parámetros obligatorios enriquecidos:
        libros_seleccionados: Lista o texto de libros de texto SEP seleccionados.
        guia_cte: Guía u orientaciones de Consejo Técnico Escolar seleccionadas.
        programa_sintetico: Texto extraído o directrices del Programa Sintético de la NEM.
        contexto_url: Texto extraído de una URL de referencia pedagógica mediante web scraping.
    """
    # Verificación preventiva de conectividad a internet
    if not verificar_conexion_internet():
        raise ConnectionError("No hay conexión a internet. Por favor, revisa tu red e inténtalo de nuevo.")

    client = get_client(api_key)

    # Compatibilidad con posibles alias vía kwargs
    if libros_seleccionados is None:
        libros_seleccionados = kwargs.get("libros", [])

    if guia_cte is None:
        guia_cte = kwargs.get("guia_cte_seleccionada", "Orientaciones CTE - 5ª Sesión Ordinaria (Febrero 2026)")

    guia_cte_detalle = kwargs.get("guia_cte_detalle", None)

    if programa_sintetico is None:
        programa_sintetico = kwargs.get("programa_sintetico_destacado", "")

    if not contexto_url:
        contexto_url = kwargs.get("contexto_url", "")

    if dias_seleccionados is None:
        dias_seleccionados = kwargs.get("dias_seleccionados") or kwargs.get("dias_planeados") or datos_escuela.get("dias_seleccionados") or datos_escuela.get("dias_planeados") or ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    if not dias_seleccionados:
        dias_seleccionados = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    num_sesiones = len(dias_seleccionados)

    # Detalle de la metodología seleccionada
    metodologia_info = METODOLOGIAS_SOCIOCRITICAS.get(metodologia, {})
    fases_metodologicas = "\n".join(metodologia_info.get("fases_oficiales", []))

    # Formateo de Contenidos y PDA
    articulacion_txt = ""
    for idx, item in enumerate(contenidos_pda, 1):
        articulacion_txt += f"\n- Contenido {idx}: {item.get('contenido', '')}\n  PDA {idx}: {item.get('pda', '')}"

    if isinstance(libros_seleccionados, (list, tuple, set)):
        libros_txt = ", ".join(str(x) for x in libros_seleccionados) if libros_seleccionados else "Proyectos de Aula, Proyectos Escolares, Proyectos Comunitarios, Nuestros Saberes, Múltiples Lenguajes"
    else:
        libros_txt = str(libros_seleccionados or "Proyectos de Aula, Proyectos Escolares, Proyectos Comunitarios, Nuestros Saberes, Múltiples Lenguajes")

    cte_nombre = str(guia_cte or "Orientaciones CTE - 5ª Sesión Ordinaria (Febrero 2026)")
    cte_enfoque = guia_cte_detalle.get("enfoque", "Evaluación formativa y proyectos comunitarios") if isinstance(guia_cte_detalle, dict) else "Evaluación formativa y proyectos comunitarios"
    cte_directrices = guia_cte_detalle.get("directrices", "Priorizar la evaluación dialógica y atención a BAP.") if isinstance(guia_cte_detalle, dict) else "Priorizar la evaluación dialógica y atención a BAP."
    prog_sintetico_txt = str(programa_sintetico).strip() if programa_sintetico else "Contenidos sintéticos y Procesos de Desarrollo de Aprendizaje (PDA) oficiales de la Fase correspondiente (NEM)."
    programa_sintetico = prog_sintetico_txt

    busqueda_web = busqueda_web or kwargs.get("busqueda_web", False)
    directriz_busqueda_web_txt = ""
    if busqueda_web:
        directriz_busqueda_web_txt = """
=== BÚSQUEDA WEB EN TIEMPO REAL (GOOGLE SEARCH GROUNDING) ===
Antes de estructurar la secuencia didáctica, utiliza tu herramienta de búsqueda en internet para encontrar ejemplos prácticos, noticias recientes o dinámicas interactivas modernas relacionadas con el Contenido y PDA seleccionado. Integra estos hallazgos web de forma natural dentro de las actividades de Inicio, Desarrollo y Cierre.
"""

    directriz_contexto_url_txt = ""
    if contexto_url and str(contexto_url).strip():
        directriz_contexto_url_txt = f"""
=== MATERIAL DE REFERENCIA DESDE URL (WEB SCRAPING) ===
El usuario ha proporcionado el siguiente material de referencia extraído de una página web educativa: {contexto_url}. Analiza este contenido y adapta las secuencias didácticas semanales o por proyectos basándote en los ejemplos y la estructura de este material.
"""

    fase_correspondiente = datos_escuela.get('fase', 'Fase 5')
    grado_seleccionado = datos_escuela.get('grado', '5° de Primaria')

    prompt = f"""{build_system_instruction()}

Elabora la planeación didáctica completa, oficial y lista para aplicar, bajo las siguientes especificaciones:

=== DATOS GENERALES DE LA INSTITUCIÓN ===
- Escuela: {datos_escuela.get('nombre_escuela', 'Primaria Revolucion Social 1910')}
- CCT: {datos_escuela.get('cct', '10EPR0361N')}
- Docente Titular: {datos_escuela.get('docente', 'Aday Domínguez Domínguez')}
- Director de la Escuela: {datos_escuela.get('director', 'José Guillermo Borjas Díaz')}
- Grado y Fase: {datos_escuela.get('grado', '5° de Primaria')} ({datos_escuela.get('fase', 'Fase 5')}) Grupo '{datos_escuela.get('grupo', 'A')}'
- Temporalidad: {datos_escuela.get('periodo', 'Semana 20')} ({num_sesiones} sesiones didácticas programadas: {', '.join(dias_seleccionados)})
- Ciclo Escolar: {datos_escuela.get('ciclo_escolar', '2025-2026')}
- Turno: {datos_escuela.get('turno', 'Matutino')}

=== DÍAS DE LA SEMANA A PLANEAR (OBLIGATORIO) ===
- Días de la semana a planear: {dias_seleccionados}
REGLA ESTRICTA: SOLO debes generar la secuencia didáctica para los siguientes días: {dias_seleccionados}. TIENES ESTRICTAMENTE PROHIBIDO mencionar, planear o incluir tablas para cualquier otro día de la semana.

=== CONFIGURACIÓN CURRICULAR (SEP - NEM) ===
- Campos Formativos seleccionados: {', '.join(campos_formativos)}
- Metodología Sociocrítica: {metodologia}
  Fases/Momentos metodológicos a seguir estrictamente:
{fases_metodologicas}
- Ejes Articuladores: {', '.join(ejes_articuladores)}

=== RECURSOS SEP Y ARTICULACIÓN METODOLÓGICA (NEM) ===
- Libros a utilizar: {libros_seleccionados}
  * Títulos de los libros de texto seleccionados: {libros_txt}
  * REQUISITO PEDAGÓGICO: En la secuencia didáctica, cita expresamente sugerencias de páginas y dinámicas concretas de estos libros para consulta y trabajo de los alumnos.

- Tomar en cuenta la guía: {guia_cte}
  * Guía y Orientaciones CTE seleccionadas: {cte_nombre}
  * Enfoque pedagógico del mes: {cte_enfoque}
  * Directrices CTE aplicadas: {cte_directrices}
  * REQUISITO CTE: Articula estas directrices en el plano didáctico, la evaluación formativa y los ajustes razonables.

=== PROGRAMA SINTÉTICO Y ANÁLISIS CURRICULAR ===
Basa los contenidos y la progresión de aprendizajes estrictamente en el siguiente Programa Sintético proporcionado: {programa_sintetico}
* REGLA DE FIDELIDAD CURRICULAR: Extrae y articula los Contenidos sintéticos, los Procesos de Desarrollo de Aprendizaje (PDA), los Campos Formativos y los Ejes Articuladores exactos correspondientes.

=== ARTICULACIÓN CURRICULAR (CONTENIDOS Y PDA PRIORIZADOS) ===
{articulacion_txt}

=== DIRECTRICES DEL PLAN ANALÍTICO Y NOTAS DEL DOCENTE ===
{directrices_docente if directrices_docente.strip() else 'Atender los problemas comunitarios de rezago lector, redacción autónoma, cálculo mental y convivencia pacífica.'}
{directriz_busqueda_web_txt}
=== TEXTOS Y ARCHIVOS DE REFERENCIA ADICIONALES APORTADOS ===
{contexto_archivos}
{directriz_contexto_url_txt}
ESTRUCTURA DE RESPUESTA EXIGIDA (Usa Markdown profesional, encabezados claros y tablas):

# I. DATOS DE IDENTIFICACIÓN Y DOSIFICADOR GENERAL DEL PROYECTO
- Nombre sugerido para el Proyecto Integrador (atractivo y motivante para las y los alumnos).
- Propósito general del proyecto.
- Escenario (Aula, Escolar o Comunitario).
- Metodología y justificación pedagógica.
- Ejes articuladores en acción.

# II. ARTICULACIÓN CURRICULAR (TABLA NEM)
Genera una tabla con:
| Campo Formativo | Contenido Sintético | Procesos de Desarrollo de Aprendizaje (PDA) | Vinculación con Libros SEP (LTG) |

# III. ACTIVIDADES DE INICIO DEL DÍA (RUTINA MATUTINA)
REGLA ESTRICTA: SOLO debes generar la secuencia didáctica para los siguientes días: {dias_seleccionados}. TIENES ESTRICTAMENTE PROHIBIDO mencionar, planear o incluir tablas para cualquier otro día de la semana.
Desarrolla la rutina matutina ÚNICAMENTE para los siguientes días: {dias_seleccionados}. No inventes actividades para los días que no estén en esta lista. Genera exactamente {num_sesiones} rutinas, una por cada día:
Para cada día en {dias_seleccionados}:
- Sesión N ([Día de la semana]):
  * Dictado: 5 palabras u oraciones con dificultad ortográfica acorde a la temática.
  * Cálculo Mental: 5 operaciones contextualizadas.
  * Problema Matemático Razonado: Enunciado, datos, operaciones y resultado interpretado.

# IV. SECUENCIA DIDÁCTICA DETALLADA (PLANO DIDÁCTICO POR SESIONES)
REGLA ESTRICTA: SOLO debes generar la secuencia didáctica para los siguientes días: {dias_seleccionados}. TIENES ESTRICTAMENTE PROHIBIDO mencionar, planear o incluir tablas para cualquier otro día de la semana.
Estructura la Secuencia Didáctica separando claramente cada día. Para cada día incluido en {dias_seleccionados}, debes proporcionar sus respectivas actividades de Inicio, Desarrollo y Cierre. No agrupes todos los días en un solo bloque. Estructura la secuencia didáctica ÚNICAMENTE para los siguientes días: {dias_seleccionados}. No inventes actividades para los días que no estén en esta lista. Desarrolla detalladamente exactamente una sesión por cada día en {dias_seleccionados} (total: {num_sesiones} sesiones):
### Sesión N: [Día de la semana] - [Nombre de la Sesión y Fase/Momento Metodológico correspondiente]
- **Tiempo estimado:** (ej. 90 minutos)
- **Inicio (15-20 min):** Descripción paso a paso de actividades, preguntas detonadoras y recuperación de conocimientos previos.
- **Desarrollo (50-60 min):** Pasos concretos, dinámicas de trabajo (equipos/individual), consulta de páginas sugeridas de libros SEP (Nuestros Saberes, Proyectos, Múltiples Lenguajes) y producción de evidencias tangibles.
- **Cierre (15-20 min):** Socialización, síntesis, conclusiones colectivas y metacognición.
- **Recursos didácticos y materiales:** Materiales concretos, cuadernos, impresiones o láminas.
- **Evidencia / Producto de la sesión:** Qué entregará o registrará el estudiante.

# V. INSTRUMENTO DE EVALUACIÓN FORMATIVA
### Rúbrica Analítica de Desempeño ({fase_correspondiente} - {grado_seleccionado})
Diseña una tabla de Instrumento de Evaluación (Rúbrica Analítica o Lista de Cotejo) con:
| Criterio / Indicador de Logro | Nivel Sobresaliente | Nivel Satisfactorio | Nivel Básico | Requiere Apoyo |

# VI. AJUSTES RAZONABLES Y ATENCIÓN A LA DIVERSIDAD (BAP - DUA)
Estrategias concretas para estudiantes con ritmos de aprendizaje diversos, apoyo en lectura/escritura y barreras de aprendizaje.

# VII. OBSERVACIONES GENERALES Y ESPACIO DE SEGUIMIENTO
Reflexiones docentes para el diario de clase y seguimiento directivo.
"""

    # Configuración de búsqueda web (Google Search Grounding: tools='google_search_retrieval' / google_search)
    call_config = None
    if busqueda_web:
        try:
            call_config = types.GenerateContentConfig(tools=[{"google_search": {}}])
        except Exception:
            try:
                call_config = types.GenerateContentConfig(tools=[{"google_search_retrieval": {}}])
            except Exception:
                call_config = {"tools": [{"google_search": {}}]}

    # Sistema de reintentos automáticos (Manejo de Errores 503 UNAVAILABLE, fallas de conexión y tiempos de espera)
    max_intentos = 3
    for intento in range(1, max_intentos + 1):
        try:
            call_kwargs = {
                "model": "gemini-3.8-flash",
                "contents": prompt
            }
            if call_config:
                call_kwargs["config"] = call_config
            response = client.models.generate_content(**call_kwargs)
            return response.text, prompt
        except (
            ConnectionError,
            TimeoutError,
            socket.timeout,
            socket.gaierror,
            socket.error,
            OSError,
            requests.exceptions.RequestException,
            *( [httpx.RequestError, httpx.TimeoutException] if httpx else [] )
        ) as conn_err:
            if intento < max_intentos:
                st.warning(f"⚠️ Inestabilidad de red o tiempo de espera con la API de Gemini (intento {intento}/{max_intentos}). Reintentando en 3 segundos...")
                time.sleep(3)
            else:
                st.error("No hay conexión a internet o se agotó el tiempo de espera al comunicarse con Gemini.")
                raise ConnectionError(
                    f"Falla de conexión a internet o tiempo de espera agotado al consultar la API de Gemini: {conn_err}"
                ) from conn_err
        except Exception as e:
            error_str = str(e)
            is_conn_or_timeout = any(term in error_str.lower() for term in [
                "connection", "conexión", "timed out", "timeout", "connecterror",
                "readtimeout", "network", "unreachable", "getaddrinfo", "econnreset",
                "econnrefused", "temporary failure in name resolution"
            ])
            if is_conn_or_timeout:
                if intento < max_intentos:
                    st.warning(f"⚠️ Error de red o tiempo de espera detectado (intento {intento}/{max_intentos}). Reintentando en 3 segundos...")
                    time.sleep(3)
                else:
                    st.error("Error de conexión con la API de Gemini tras varios reintentos.")
                    raise ConnectionError(
                        f"Error de conexión o tiempo de espera al comunicarse con Gemini: {error_str}"
                    ) from e
            elif "503" in error_str:
                if intento < max_intentos:
                    st.warning("Servidores de Google saturados. Reintentando en 5 segundos...")
                    time.sleep(5)
                else:
                    st.error("Servidores de Google saturados tras 3 intentos. Por favor, intenta más tarde.")
                    raise e
            else:
                # Si el error no es de conexión ni 503, se propaga para su manejo
                raise e

def generate_sample_fallback(
    datos_escuela: Dict[str, Any],
    campos_formativos: list,
    metodologia: str,
    ejes: list,
    dias_seleccionados: list = None,
    contexto_url: str = "",
    **kwargs
) -> str:
    """
    Genera una planeación didáctica pre-elaborada completa de 5° Grado en caso de que
    el usuario desee visualizar el resultado o explorar la app antes de ingresar su API Key,
    ajustando las rutinas y sesiones estrictamente a los días seleccionados.
    """
    escuela = datos_escuela.get('nombre_escuela', 'Primaria Revolución Social 1910')
    cct = datos_escuela.get('cct', '10EPR0361N')
    docente = datos_escuela.get('docente', 'Aday Domínguez Domínguez')
    director = datos_escuela.get('director', 'José Guillermo Borjas Díaz')
    grado_seleccionado = datos_escuela.get('grado', '5° de Primaria')
    fase_correspondiente = datos_escuela.get('fase', 'Fase 5')
    grupo = datos_escuela.get('grupo', 'A')
    periodo = datos_escuela.get('periodo', 'Semana 20')
    ciclo = datos_escuela.get('ciclo_escolar', '2025-2026')

    if dias_seleccionados is None:
        dias_seleccionados = datos_escuela.get('dias_seleccionados') or datos_escuela.get('dias_planeados') or ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    if not dias_seleccionados:
        dias_seleccionados = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    num_sesiones = len(dias_seleccionados)

    sample_rutinas = {
        "Lunes": "- **Dictado:** 1. Nutrición, 2. Biodiversidad, 3. Ultraprocesados, 4. Investigación, 5. Convivencia.\n- **Cálculo Mental:** a) 250 + 750, b) 1200 - 450, c) 8 x 7 + 14, d) La mitad de 350, e) 100 x 3.5.\n- **Problema Razonado:** En la cooperativa escolar se vendieron 45 paquetes de fruta fresca a $18 pesos cada uno. ¿Cuánto dinero se recaudó en total y cuál sería la ganancia si el costo inicial fue de $420 pesos?",
        "Martes": "- **Dictado:** 1. Digestión, 2. Equitativo, 3. Tríptico, 4. Argumentación, 5. Colaboración.\n- **Cálculo Mental:** a) 3/4 + 1/4, b) 450 ÷ 9, c) 60 x 5, d) 1000 - 325, e) Doble de 2.75.\n- **Problema Razonado:** Para una receta comunitaria se necesitan 3/4 kg de manzanas y 1/2 kg de peras. ¿Cuántos kilogramos de fruta se utilizarán en total?",
        "Miércoles": "- **Dictado:** 1. Concientización, 2. Hidratación, 3. Metabolismo, 4. Ciudadanía, 5. Democracia.\n- **Cálculo Mental:** a) 15 x 6, b) 800 - 260, c) 1/2 de 120, d) 4.5 + 3.8, e) 72 ÷ 8.\n- **Problema Razonado:** Don José compró una caja de 120 naranjas. Si 1/4 de las naranjas están verdes y el resto maduras, ¿cuántas naranjas maduras tiene disponibles?",
        "Jueves": "- **Dictado:** 1. Información, 2. Proporción, 3. Vitaminas, 4. Hábitos, 5. Respeto.\n- **Cálculo Mental:** a) 50 x 8, b) 2000 - 650, c) 2/5 + 1/5, d) Triple de 45, e) 63 ÷ 7 + 12.\n- **Problema Razonado:** Un vaso de agua natural tiene 250 mililitros. Si un estudiante bebe 8 vasos al día, ¿cuántos litros de agua consume en total en una semana de 5 días escolares?",
        "Viernes": "- **Dictado:** 1. Evaluación, 2. Solidaridad, 3. Sustentable, 4. Análisis, 5. Transformación.\n- **Cálculo Mental:** a) 90 x 4, b) 500 - 185, c) 0.75 + 0.25, d) 48 ÷ 6, e) 150 x 3.\n- **Problema Razonado:** Si una familia gasta $1,800 pesos a la semana en alimentos frescos y $650 en comida ultraprocesada, ¿cuánto dinero ahorraría si reduce a la mitad el gasto en productos ultraprocesados?"
    }

    sample_sesiones = {
        "Lunes": """Fase 1. Planeación (Momento 1: Identificación y Momento 2: Recuperación)
- **Tiempo estimado:** 90 minutos.
- **Inicio (20 min):**
  * Bienvenida activa y realización de la rutina matutina (dictado y cálculo mental).
  * Dinámica detonadora "¿Qué desayunamos hoy?": En plenaria, las y los alumnos comparten sus alimentos cotidianos en una lluvia de ideas en el pizarrón.
  * Planteamiento de la pregunta generadora del proyecto: *¿De qué manera los alimentos que consumimos en la escuela y en casa impactan en nuestra energía, salud y concentración?*
- **Desarrollo (50 min):**
  * Lectura compartida en el libro *Nuestros Saberes: 5° grado*, páginas 68 a 71, analizando los conceptos de alimentos naturales, procesados y ultraprocesados.
  * En comunidades de 4 integrantes, elaboran una lista comparativa en sus libretas dividida en dos columnas: "Alimentos cotidianos nutritivos" vs. "Alimentos ultraprocesados frecuentes en la comunidad".
  * El docente acompaña a los equipos guiando la identificación del Plato del Bien Comer y la Jarra del Buen Beber.
- **Cierre (20 min):**
  * Puesta en común comunitaria: Un vocero por equipo expone uno de sus hallazgos.
  * Registro en el pizarrón del primer acuerdo de asamblea de aula para el desarrollo de la investigación.
- **Recursos didácticos:** Libro *Nuestros Saberes*, cuaderno del alumno, plumones y papel bond.
- **Evidencia:** Tabla comparativa en el cuaderno y ficha de registro de saberes previos.""",

        "Martes": """Fase 1. Planeación (Momento 3: Planificación) y Fase 2. Acción (Momento 4: Acercamiento)
- **Tiempo estimado:** 90 minutos.
- **Inicio (15 min):**
  * Rutina de inicio del día (dictado, cálculo mental y problema razonado de fracciones).
  * Recordatorio de los acuerdos de la sesión previa y lectura de una cápsula del libro *Múltiples Lenguajes*.
- **Desarrollo (55 min):**
  * Consulta del libro *Proyectos Comunitarios (5° grado)*, páginas 24 a 27.
  * Diseño participativo de un guion de entrevista para consultar a los encargados de la cooperativa escolar y familiares sobre los hábitos de consumo alimenticio.
  * Los estudiantes redactan 5 preguntas abiertas con signos de interrogación correctos y ortografía cuidada.
  * Simulación de la entrevista en parejas mediante juego de roles (entrevistador y entrevistado).
- **Cierre (20 min):**
  * Revisión en coevaluación del cuestionario diseñado.
  * Tarea de vinculación familiar: Aplicar la entrevista a dos miembros de la familia o vecinos.
- **Recursos didácticos:** Libro *Proyectos Comunitarios*, libreta de notas, lápiz y borrador.
- **Evidencia:** Borrador del guion de entrevista validado con criterios de claridad y pertinencia.""",

        "Miércoles": """Fase 2. Acción (Momento 5: Comprensión y Producción)
- **Tiempo estimado:** 90 minutos.
- **Inicio (15 min):**
  * Rutina matutina con énfasis en cálculo mental de proporciones y porcentajes simples.
  * Puesta en común de las anécdotas al aplicar la entrevista en casa.
- **Desarrollo (55 min):**
  * Vaciado colaborativo de los datos obtenidos en las entrevistas: Número de personas que consumen agua natural vs. refrescos y frutas vs. frituras.
  * Construcción de una gráfica de barras sencilla en el cuaderno para representar las frecuencias.
  * Introducción al formato del **Tríptico Informativo de Salud**: Estructura de portada, títulos, subtítulos, argumentos científicos del Plato del Bien Comer e ilustraciones.
  * Inicio del borrador del tríptico en hojas blancas dobladas en tres partes.
- **Cierre (20 min):**
  * Exposición de los primeros avances del tríptico.
  * Retroalimentación formativa del docente destacando el uso de conectores lógicos y datos verídicos.
- **Recursos didácticos:** Hojas blancas, colores, reglas, datos de las entrevistas y recortes.
- **Evidencia:** Gráfica de barras en el cuaderno y maqueta inicial del tríptico informativo.""",

        "Jueves": """Fase 2. Acción (Momento 6: Reconocimiento y Momento 7: Concreción)
- **Tiempo estimado:** 90 minutos.
- **Inicio (15 min):**
  * Rutina matutina (dictado ortográfico de términos científicos y problema matemático de medidas de capacidad).
  * Reflexión grupal sobre la importancia de la revisión y corrección de textos propios.
- **Desarrollo (55 min):**
  * Intercambio de borradores de trípticos entre comunidades de aprendizaje mediante una rúbrica sencilla de coevaluación.
  * Incorporación de sugerencias de mejora: Corrección de puntuación, mayúsculas y claridad visual.
  * Elaboración de la versión final del tríptico con tipografía cuidada, colores vivos y mensajes persuasivos para promover estilos de vida activos y saludables.
  * Ensayo breve de cómo presentarán el tríptico a otros grupos de la primaria Revolución Social 1910.
- **Cierre (20 min):**
  * Organización de la jornada de difusión: Asignación de roles (presentadores, encargados de registro fotográfico, moderadores).
- **Recursos didácticos:** Trípticos finalizados, cartulinas de apoyo, marcadores y lista de cotejo.
- **Evidencia:** Tríptico informativo final terminado y evaluado con rúbrica docente.""",

        "Viernes": """Fase 3. Intervención (Momentos 8, 9, 10 y 11: Difusión, Consideraciones y Avances)
- **Tiempo estimado:** 90 minutos.
- **Inicio (15 min):**
  * Rutina de inicio del día (dictado, cálculo mental y problema matemático integrador).
  * Palabras de motivación y recordatorio del protocolo de respeto durante las exposiciones en otros salones.
- **Desarrollo (50 min):**
  * Visita a grupos de Fase 3 y 4 (1° a 4° grado) para entregar y explicar los trípticos informativos comunitarios.
  * Colocación de un periódico mural de salud en el patio cívico escolar de la Primaria Revolución Social 1910 con el lema *"Alimentación Sana para Mentes Fuertes"*.
  * Registro de firmas y comentarios de los docentes y compañeros visitantes.
- **Cierre (25 min):**
  * Círculo de diálogo reflexivo de asamblea: ¿Qué aprendimos?, ¿qué dificultades superamos?, ¿cómo cambió nuestra manera de alimentarnos?
  * Autoevaluación final de la experiencia mediante una diana de evaluación formativa.
- **Recursos didácticos:** Mural escolar, cinta adhesiva, trípticos y dianas de evaluación.
- **Evidencia:** Registro fotográfico de la socialización, diana de autoevaluación y notas en el diario de campo."""
    }

    rutinas_str = ""
    sesiones_str = ""
    for idx, dia in enumerate(dias_seleccionados, 1):
        r_txt = sample_rutinas.get(dia, sample_rutinas["Lunes"])
        rutinas_str += f"### Sesión {idx} ({dia}):\n{r_txt}\n\n"
        s_txt = sample_sesiones.get(dia, sample_sesiones["Lunes"])
        sesiones_str += f"### Sesión {idx}: {dia} - {s_txt}\n\n"

    dias_str = ", ".join(dias_seleccionados)

    return f"""# I. DATOS DE IDENTIFICACIÓN Y DOSIFICADOR GENERAL DEL PROYECTO

- **Nombre del Proyecto:** "Guardianes de la Memoria y la Salud Comunitaria"
- **Escuela:** {escuela} | **C.C.T.:** {cct}
- **Docente:** Prof(a). {docente} | **Director:** Prof. {director}
- **Fase y Grado:** {fase_correspondiente} — {grado_seleccionado} Grupo '{grupo}'
- **Temporalidad:** {periodo} ({num_sesiones} sesiones: {dias_str}) | **Ciclo Escolar:** {ciclo}
- **Escenario:** Comunitario y de Aula
- **Metodología Sociocrítica:** {metodologia}
- **Ejes Articuladores:** {', '.join(ejes)}
- **Propósito:** Que las y los alumnos de {grado_seleccionado} investiguen, mediante textos informativos y el método de proyectos comunitarios, los hábitos de alimentación saludable en su entorno escolar y local, desarrollando habilidades de producción escrita (trípticos y cápsulas informativas) y resolución de problemas fraccionarios y porcentuales vinculados con la nutrición.

---

# II. ARTICULACIÓN CURRICULAR (TABLA NEM)

| Campo Formativo | Contenido Sintético | Procesos de Desarrollo de Aprendizaje (PDA) | Vinculación con Libros SEP (LTG) |
| :--- | :--- | :--- | :--- |
| **Lenguajes** | Comprensión y producción de textos informativos sobre temas colectivos. | Selecciona y lee textos informativos; elabora resúmenes, cuadros sinópticos y trípticos para prevenir problemas de salud comunitaria. | *Proyectos Comunitarios* (págs. 20-33) y *Múltiples Lenguajes* (págs. 42-45) |
| **Saberes y Pensamiento Científico** | Alimentación saludable y resolución de operaciones fraccionarias. | Explica las características de la dieta correcta (completa, equilibrada, variada, inocua) y resuelve problemas que implican calcular fracciones de cantidades. | *Nuestros Saberes* (págs. 68-75) |
| **De lo Humano y lo Comunitario** | Acciones individuales que repercuten en la conservación y mejora de la salud. | Construye alternativas saludables de alimentación y estilo de vida con base en la toma de decisiones asertivas. | *Proyectos de Aula* (págs. 54-61) |

---

# III. ACTIVIDADES DE INICIO DEL DÍA (RUTINA MATUTINA - {num_sesiones} SESIONES: {dias_str.upper()})

{rutinas_str.strip()}

---

# IV. SECUENCIA DIDÁCTICA DETALLADA (PLANO DIDÁCTICO POR SESIONES: {dias_str.upper()})

{sesiones_str.strip()}

---

# V. INSTRUMENTO DE EVALUACIÓN FORMATIVA

### Rúbrica Analítica de Desempeño ({fase_correspondiente} - {grado_seleccionado})

| Criterio de Evaluación | Nivel Sobresaliente (10 - 9) | Nivel Satisfactorio (8 - 7) | Nivel Básico (6) | Requiere Apoyo (5) |
| :--- | :--- | :--- | :--- | :--- |
| **Comprensión y Análisis Curricular** | Explica con claridad científica los nutrientes, el Plato del Bien Comer y contrasta de forma crítica con la realidad comunitaria. | Identifica los grupos de alimentos y reconoce hábitos saludables en su entorno con pocos errores conceptuales. | Menciona algunos alimentos saludables pero le cuesta diferenciarlos de los procesados. | Muestra confusión entre alimentos nutritivos y perjudiciales. |
| **Producción Escrita (Tríptico)** | Elabora un tríptico con estructura completa, ortografía impecable, imágenes alusivas y argumentos sólidos y persuasivos. | Diseña el tríptico con estructura comprensible; comete pocos errores ortográficos menores que no afectan el sentido. | El tríptico carece de alguno de los elementos formales o presenta varios errores de redacción. | Presenta un texto incompleto sin formato de tríptico ni organización visual. |
| **Habilidades Matemáticas (Cálculo y Razonamiento)** | Resuelve con autonomía problemas de fracciones, sumas y medidas de capacidad, interpretando el resultado en su vida diaria. | Resuelve la mayoría de los problemas de cálculo mental y razonamiento con mínima orientación del docente. | Resuelve operaciones mecánicas pero requiere apoyo constante en el planteamiento razonado. | Dificultad severa para realizar cálculos básicos y comprender los enunciados. |
| **Trabajo Colaborativo y Ejes Articuladores** | Participa de manera empática, solidaria e inclusiva en su comunidad de aula, respetando la diversidad de opiniones. | Colabora adecuadamente en el equipo cumpliendo con las tareas asignadas en tiempo y forma. | Participa de manera intermitente o requiere mediación docente para integrarse al equipo. | Muestra resistencia para colaborar con sus pares en el aula. |

---

# VI. AJUSTES RAZONABLES Y ATENCIÓN A LA DIVERSIDAD (BAP - DUA)

1. **Principio de Múltiples Formas de Representación (DUA):** Uso constante de apoyos visuales (láminas del Plato del Bien Comer, colores para identificar fracciones y esquemas gráficos sintetizados) para alumnos con estilos de aprendizaje visual y cinestésico.
2. **Atención a alumnos con ritmo de lectura en consolidación:** Se propicia el trabajo en parejas pedagógicas (tutoría entre pares solidaria) para la lectura de los libros de texto y la redacción del borrador del tríptico.
3. **Graduación de actividades matemáticas:** Para estudiantes que requieren apoyo en cálculo mental y problemas fraccionarios, se permite el uso de material concreto (fichas, regletas o tiras de fracciones) antes de pasar a la notación abstracta.
4. **Inclusión socioemocional:** Fortalecimiento del valor del respeto y escucha activa en el momento de las asambleas de aula.

---

# VII. OBSERVACIONES GENERALES Y ESPACIO DE SEGUIMIENTO

- **Seguimiento del Diario de Clase:** Anotar diariamente incidentes críticos, alumnos que mostraron liderazgo pedagógico y aquellos que requieren retroalimentación personalizada el día siguiente.
- **Vinculación con el Programa Escolar de Mejora Continua (PEMC / Plan Analítico):** Este proyecto impacta de manera directa en la meta de reducción del consumo de comida chatarra y el aumento de la comprensión lectora en {fase_correspondiente}.
"""
