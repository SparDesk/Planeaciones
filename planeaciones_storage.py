"""
Módulo de Persistencia, Historial, Autoguardado y Gestión Personalizada de Archivos (NEM)
Utiliza SQLite para almacenamiento relacional atómico y archivos físicos JSON organizados por carpetas/categorías.
Permite autoguardado en tiempo real, guardado con nombre personalizado y ruta/categoría, historial de versiones y restauración completa.
"""

import sqlite3
import json
import os
import re
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any
from nem_data import parsear_metodologia_lista, formatear_metodologia_str

DB_FILENAME = "planeaciones_storage.db"
DIR_GUARDADOS_DEFAULT = "guardados"

CATEGORIAS_RUTAS_DEFAULT = [
    "Trimestre 1 (Diagnóstico e Inicio)",
    "Trimestre 2 (Desarrollo y Proyectos)",
    "Trimestre 3 (Consolidación y Cierre)",
    "Proyectos de Aula",
    "Proyectos Comunitarios",
    "Proyectos Escolares",
    "CTE y Fase Intensiva",
    "Carpeta General"
]

def get_db_path(custom_path: Optional[str] = None) -> str:
    if custom_path:
        return custom_path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, DB_FILENAME)

def init_db(db_path: Optional[str] = None) -> None:
    """Inicializa la base de datos y crea las tablas, columnas e índices si no existen."""
    path = get_db_path(db_path)
    conn = sqlite3.connect(path)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS planeaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                semana INTEGER NOT NULL,
                periodo TEXT NOT NULL,
                titulo TEXT NOT NULL,
                grado TEXT NOT NULL,
                grupo TEXT NOT NULL,
                fecha_guardado TEXT NOT NULL,
                timestamp REAL NOT NULL,
                campos_formativos TEXT NOT NULL,
                metodologia TEXT NOT NULL,
                ejes_articuladores TEXT NOT NULL,
                contenidos_pda TEXT NOT NULL,
                libros_seleccionados TEXT NOT NULL,
                guia_cte TEXT,
                dias_seleccionados TEXT NOT NULL,
                dias_fechas TEXT NOT NULL,
                directrices TEXT,
                num_sesiones INTEGER NOT NULL,
                planeacion_generada TEXT,
                prompt_enviado TEXT,
                url_referencia TEXT,
                es_autoguardado INTEGER DEFAULT 1,
                version_nombre TEXT DEFAULT 'Autoguardado',
                hash_contenido TEXT,
                nombre_archivo TEXT,
                categoria_ruta TEXT
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_semana ON planeaciones(username, semana)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_timestamp ON planeaciones(username, timestamp DESC)")

        # Migración segura: agregar columnas nombre_archivo y categoria_ruta si no existen
        cursor.execute("PRAGMA table_info(planeaciones)")
        cols = [row[1] for row in cursor.fetchall()]
        if "nombre_archivo" not in cols:
            cursor.execute("ALTER TABLE planeaciones ADD COLUMN nombre_archivo TEXT")
        if "categoria_ruta" not in cols:
            cursor.execute("ALTER TABLE planeaciones ADD COLUMN categoria_ruta TEXT")
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_cat ON planeaciones(username, categoria_ruta)")
        conn.commit()
    finally:
        conn.close()

def calcular_hash_planeacion(data: Dict[str, Any]) -> str:
    """Calcula un hash MD5 de los datos clave para evitar escrituras redundantes si nada ha cambiado."""
    clave = f"{data.get('semana')}|{data.get('campos_formativos')}|{data.get('metodologia')}|" \
            f"{data.get('ejes_articuladores')}|{data.get('contenidos_pda')}|{data.get('libros_seleccionados')}|" \
            f"{data.get('dias_seleccionados')}|{data.get('directrices')}|{data.get('num_sesiones')}|" \
            f"{len(data.get('planeacion_generada') or '')}|{data.get('planeacion_generada')}|" \
            f"{data.get('nombre_archivo')}|{data.get('categoria_ruta')}"
    return hashlib.md5(clave.encode("utf-8", errors="ignore")).hexdigest()

def sanitizar_nombre_ruta(nombre: str) -> str:
    """Elimina caracteres no permitidos en nombres de archivos o carpetas del sistema operativo."""
    if not nombre:
        return ""
    # Reemplazar caracteres prohibidos en Windows y Unix: \ / : * ? " < > |
    limpio = re.sub(r'[\\/*?:"<>|]', "", str(nombre)).strip()
    limpio = re.sub(r'\s+', '_', limpio)
    return limpio or "Archivo"

def guardar_archivo_fisico_json(
    data: Dict[str, Any],
    nombre_archivo: str,
    categoria_ruta: str,
    base_folder: Optional[str] = None
) -> str:
    """
    Guarda una copia física en archivo JSON en la subcarpeta correspondiente a su categoría/ruta.
    Ejemplo: guardados/Trimestre_2/Planeacion_Semana_20_Matematicas.json
    """
    try:
        if not base_folder:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            base_folder = os.path.join(base_dir, DIR_GUARDADOS_DEFAULT)
        
        cat_clean = sanitizar_nombre_ruta(categoria_ruta) or "General"
        cat_dir = os.path.join(base_folder, cat_clean)
        os.makedirs(cat_dir, exist_ok=True)

        nom_clean = sanitizar_nombre_ruta(nombre_archivo)
        if not nom_clean:
            sem = data.get("semana", 1)
            nom_clean = f"Planeacion_Semana_{sem}"
        if not nom_clean.lower().endswith(".json"):
            nom_clean += ".json"

        target_path = os.path.join(cat_dir, nom_clean)
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return target_path
    except Exception:
        return ""

def guardar_planeacion(
    username: str,
    data: Dict[str, Any],
    es_autoguardado: bool = True,
    version_nombre: str = "Autoguardado",
    nombre_archivo: Optional[str] = None,
    categoria_ruta: Optional[str] = None,
    db_path: Optional[str] = None
) -> Optional[int]:
    """
    Guarda o actualiza una planeación en la base de datos local y sincroniza un archivo JSON físico en disco.
    Permite asignar un nombre personalizado de archivo y una categoría o ruta de destino.
    """
    init_db(db_path)
    path = get_db_path(db_path)
    now = datetime.now()
    fecha_str = now.strftime("%d/%m/%Y %H:%M:%S")
    timestamp = now.timestamp()
    
    semana = int(data.get("semana", 1))
    periodo = str(data.get("periodo", f"Semana {semana} de 37"))
    grado = str(data.get("grado", '6° de Primaria'))
    grupo = str(data.get("grupo", 'A'))
    
    campos_list = data.get("campos_formativos") or []
    if isinstance(campos_list, str):
        try:
            campos_list = json.loads(campos_list)
        except Exception:
            campos_list = [campos_list]
    elif not isinstance(campos_list, list):
        campos_list = list(campos_list)

    campos_str_display = ", ".join(str(c) for c in campos_list[:2]) + ("..." if len(campos_list) > 2 else "")
    titulo = data.get("titulo") or f"Semana {semana} ({periodo}) — {campos_str_display}"
    campos_json = json.dumps(campos_list, ensure_ascii=False)
    metodologia_raw = data.get("metodologia")
    metodologia_lista = parsear_metodologia_lista(metodologia_raw)
    metodologia = json.dumps(metodologia_lista, ensure_ascii=False)

    def safe_dump_list(val, default):
        if val is None:
            return json.dumps(default, ensure_ascii=False)
        if isinstance(val, str):
            try:
                parsed = json.loads(val)
                return json.dumps(parsed, ensure_ascii=False)
            except Exception:
                return json.dumps([val], ensure_ascii=False)
        return json.dumps(val, ensure_ascii=False)

    def safe_dump_dict(val, default):
        if val is None:
            return json.dumps(default, ensure_ascii=False)
        if isinstance(val, str):
            try:
                parsed = json.loads(val)
                return json.dumps(parsed if isinstance(parsed, dict) else default, ensure_ascii=False)
            except Exception:
                return json.dumps(default, ensure_ascii=False)
        return json.dumps(val, ensure_ascii=False)

    ejes_json = safe_dump_list(data.get("ejes_articuladores"), [])
    pda_json = safe_dump_list(data.get("contenidos_pda"), [])
    libros_json = safe_dump_list(data.get("libros_seleccionados"), [])
    guia_cte = str(data.get("guia_cte", ""))
    dias_json = safe_dump_list(data.get("dias_seleccionados"), ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
    dias_fechas_json = safe_dump_dict(data.get("dias_fechas"), {})
    directrices = str(data.get("directrices") or "")
    num_sesiones = int(data.get("num_sesiones", 5))
    planeacion_generada = data.get("planeacion_generada") or ""
    prompt_enviado = data.get("prompt_enviado") or ""
    url_referencia = str(data.get("url_referencia") or "")

    # Determinar nombre personalizado de archivo
    if not nombre_archivo:
        nombre_archivo = data.get("nombre_archivo")
    if not nombre_archivo:
        primer_campo = str(campos_list[0]) if campos_list else "General"
        campo_slug = re.sub(r'[^a-zA-Z0-9]', '', primer_campo)
        nombre_archivo = f"Planeacion_Semana_{semana}_{campo_slug}"

    # Determinar categoría o ruta de destino
    if not categoria_ruta:
        categoria_ruta = data.get("categoria_ruta")
    if not categoria_ruta:
        if semana <= 13:
            categoria_ruta = "Trimestre 1 (Diagnóstico e Inicio)"
        elif semana <= 26:
            categoria_ruta = "Trimestre 2 (Desarrollo y Proyectos)"
        else:
            categoria_ruta = "Trimestre 3 (Consolidación y Cierre)"

    data_con_metas = dict(data)
    data_con_metas["nombre_archivo"] = nombre_archivo
    data_con_metas["categoria_ruta"] = categoria_ruta
    hash_cont = calcular_hash_planeacion(data_con_metas)

    conn = sqlite3.connect(path)
    reg_id = None
    try:
        cursor = conn.cursor()
        
        # Si es autoguardado, verificar si ya existe registro de autoguardado para este usuario y semana
        if es_autoguardado:
            cursor.execute(
                "SELECT id, hash_contenido FROM planeaciones WHERE username = ? AND semana = ? AND es_autoguardado = 1 ORDER BY id DESC LIMIT 1",
                (username, semana)
            )
            row = cursor.fetchone()
            if row:
                exist_id, exist_hash = row
                # Si el contenido no ha cambiado, no hacer re-escritura en base de datos
                if exist_hash == hash_cont:
                    reg_id = exist_id
                else:
                    cursor.execute("""
                        UPDATE planeaciones SET
                            periodo = ?,
                            titulo = ?,
                            grado = ?,
                            grupo = ?,
                            fecha_guardado = ?,
                            timestamp = ?,
                            campos_formativos = ?,
                            metodologia = ?,
                            ejes_articuladores = ?,
                            contenidos_pda = ?,
                            libros_seleccionados = ?,
                            guia_cte = ?,
                            dias_seleccionados = ?,
                            dias_fechas = ?,
                            directrices = ?,
                            num_sesiones = ?,
                            planeacion_generada = ?,
                            prompt_enviado = ?,
                            url_referencia = ?,
                            version_nombre = ?,
                            hash_contenido = ?,
                            nombre_archivo = ?,
                            categoria_ruta = ?
                        WHERE id = ?
                    """, (
                        periodo, titulo, grado, grupo, fecha_str, timestamp,
                        campos_json, metodologia, ejes_json, pda_json, libros_json,
                        guia_cte, dias_json, dias_fechas_json, directrices, num_sesiones,
                        planeacion_generada, prompt_enviado, url_referencia, version_nombre,
                        hash_cont, nombre_archivo, categoria_ruta, exist_id
                    ))
                    conn.commit()
                    reg_id = exist_id

        if reg_id is None:
            # Insertar nuevo registro
            cursor.execute("""
                INSERT INTO planeaciones (
                    username, semana, periodo, titulo, grado, grupo,
                    fecha_guardado, timestamp, campos_formativos, metodologia,
                    ejes_articuladores, contenidos_pda, libros_seleccionados,
                    guia_cte, dias_seleccionados, dias_fechas, directrices,
                    num_sesiones, planeacion_generada, prompt_enviado,
                    url_referencia, es_autoguardado, version_nombre, hash_contenido,
                    nombre_archivo, categoria_ruta
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                username, semana, periodo, titulo, grado, grupo,
                fecha_str, timestamp, campos_json, metodologia,
                ejes_json, pda_json, libros_json,
                guia_cte, dias_json, dias_fechas_json, directrices,
                num_sesiones, planeacion_generada, prompt_enviado,
                url_referencia, 1 if es_autoguardado else 0, version_nombre, hash_cont,
                nombre_archivo, categoria_ruta
            ))
            conn.commit()
            reg_id = cursor.lastrowid
    finally:
        conn.close()

    # Guardar copia en archivo físico JSON en su carpeta de categoría correspondiente
    if reg_id:
        data_archivo = dict(data)
        data_archivo["id"] = reg_id
        data_archivo["username"] = username
        data_archivo["nombre_archivo"] = nombre_archivo
        data_archivo["categoria_ruta"] = categoria_ruta
        data_archivo["fecha_guardado"] = fecha_str
        guardar_archivo_fisico_json(data_archivo, nombre_archivo, categoria_ruta)

    return reg_id

def listar_planeaciones(username: str, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Lista el historial de planeaciones guardadas para el usuario,
    ordenadas por semana y fecha de guardado, incluyendo nombre personalizado y categoría.
    """
    init_db(db_path)
    path = get_db_path(db_path)
    conn = sqlite3.connect(path)
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, username, semana, periodo, titulo, grado, grupo,
                   fecha_guardado, timestamp, campos_formativos, metodologia,
                   num_sesiones, es_autoguardado, version_nombre,
                   nombre_archivo, categoria_ruta,
                   CASE WHEN planeacion_generada IS NOT NULL AND LENGTH(TRIM(planeacion_generada)) > 0 THEN 1 ELSE 0 END as tiene_plan,
                   LENGTH(IFNULL(planeacion_generada, '')) as len_plan
            FROM planeaciones
            WHERE username = ?
            ORDER BY semana ASC, timestamp DESC
        """, (username,))
        rows = cursor.fetchall()
        
        resultado = []
        for r in rows:
            campos_raw = r["campos_formativos"]
            try:
                campos_list = json.loads(campos_raw)
            except Exception:
                campos_list = []

            sem_num = r["semana"]
            cat_default = "Trimestre 1 (Diagnóstico e Inicio)" if sem_num <= 13 else ("Trimestre 2 (Desarrollo y Proyectos)" if sem_num <= 26 else "Trimestre 3 (Consolidación y Cierre)")
            nom_default = f"Planeacion_Semana_{sem_num}"
            
            resultado.append({
                "id": r["id"],
                "username": r["username"],
                "semana": sem_num,
                "periodo": r["periodo"],
                "titulo": r["titulo"],
                "grado": r["grado"],
                "grupo": r["grupo"],
                "fecha_guardado": r["fecha_guardado"],
                "timestamp": r["timestamp"],
                "campos_formativos": campos_list,
                "metodologia": formatear_metodologia_str(r["metodologia"]),
                "num_sesiones": r["num_sesiones"],
                "es_autoguardado": bool(r["es_autoguardado"]),
                "version_nombre": r["version_nombre"],
                "nombre_archivo": r["nombre_archivo"] or nom_default,
                "categoria_ruta": r["categoria_ruta"] or cat_default,
                "tiene_plan": bool(r["tiene_plan"]),
                "len_plan": r["len_plan"]
            })
        return resultado
    finally:
        conn.close()

def obtener_planeacion_por_id(planeacion_id: int, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Recupera la planeación completa y deserializa todos los campos estructurados."""
    init_db(db_path)
    path = get_db_path(db_path)
    conn = sqlite3.connect(path)
    try:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM planeaciones WHERE id = ?", (planeacion_id,))
        row = cursor.fetchone()
        if not row:
            return None
        
        def safe_json(val, default):
            try:
                return json.loads(val) if val else default
            except Exception:
                return default

        sem_num = row["semana"]
        cat_default = "Trimestre 1 (Diagnóstico e Inicio)" if sem_num <= 13 else ("Trimestre 2 (Desarrollo y Proyectos)" if sem_num <= 26 else "Trimestre 3 (Consolidación y Cierre)")
        nom_default = f"Planeacion_Semana_{sem_num}"

        return {
            "id": row["id"],
            "username": row["username"],
            "semana": sem_num,
            "periodo": row["periodo"],
            "titulo": row["titulo"],
            "grado": row["grado"],
            "grupo": row["grupo"],
            "fecha_guardado": row["fecha_guardado"],
            "timestamp": row["timestamp"],
            "campos_formativos": safe_json(row["campos_formativos"], []),
            "metodologia": parsear_metodologia_lista(row["metodologia"]),
            "ejes_articuladores": safe_json(row["ejes_articuladores"], []),
            "contenidos_pda": safe_json(row["contenidos_pda"], []),
            "libros_seleccionados": safe_json(row["libros_seleccionados"], []),
            "guia_cte": row["guia_cte"],
            "dias_seleccionados": safe_json(row["dias_seleccionados"], ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]),
            "dias_fechas": safe_json(row["dias_fechas"], {}),
            "directrices": row["directrices"],
            "num_sesiones": row["num_sesiones"],
            "planeacion_generada": row["planeacion_generada"],
            "prompt_enviado": row["prompt_enviado"],
            "url_referencia": row["url_referencia"],
            "es_autoguardado": bool(row["es_autoguardado"]),
            "version_nombre": row["version_nombre"],
            "hash_contenido": row["hash_contenido"],
            "nombre_archivo": row["nombre_archivo"] or nom_default,
            "categoria_ruta": row["categoria_ruta"] or cat_default
        }
    finally:
        conn.close()

def obtener_planeacion_por_nombre(username: str, nombre_archivo: str, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Busca y recupera una planeación a partir de su nombre personalizado de archivo."""
    init_db(db_path)
    path = get_db_path(db_path)
    conn = sqlite3.connect(path)
    try:
        cursor = conn.cursor()
        nom_limpio = sanitizar_nombre_ruta(nombre_archivo).replace(".json", "")
        cursor.execute(
            "SELECT id FROM planeaciones WHERE username = ? AND (nombre_archivo = ? OR nombre_archivo LIKE ?) ORDER BY timestamp DESC LIMIT 1",
            (username, nombre_archivo, f"{nom_limpio}%")
        )
        row = cursor.fetchone()
        if row:
            return obtener_planeacion_por_id(row[0], db_path)
        return None
    finally:
        conn.close()

def eliminar_planeacion_por_id(planeacion_id: int, db_path: Optional[str] = None) -> bool:
    """Elimina una planeación del almacenamiento local por su ID."""
    init_db(db_path)
    path = get_db_path(db_path)
    conn = sqlite3.connect(path)
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM planeaciones WHERE id = ?", (planeacion_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def obtener_resumen_semanas_cubiertas(username: str, db_path: Optional[str] = None) -> Dict[str, Any]:
    """Retorna métricas de cobertura escolar (de 1 a 37 semanas) para el docente."""
    planes = listar_planeaciones(username, db_path)
    semanas_con_plan = set(p["semana"] for p in planes if p["tiene_plan"])
    semanas_configuradas = set(p["semana"] for p in planes)
    return {
        "total_registros": len(planes),
        "semanas_completas": len(semanas_con_plan),
        "semanas_configuradas": len(semanas_configuradas),
        "porcentaje_avance": round((len(semanas_con_plan) / 37.0) * 100, 1),
        "lista_semanas_completas": sorted(list(semanas_con_plan)),
        "lista_semanas_pendientes": [s for s in range(1, 38) if s not in semanas_con_plan]
    }

# ==========================================
# FUNCIONES EXPORTADAS Y ALIASES DE COMPATIBILIDAD
# ==========================================

def cargar_planeacion(planeacion_id: int, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Función de carga directa de una planeación por su ID."""
    return obtener_planeacion_por_id(planeacion_id, db_path)

def cargar_planeacion_guardada(planeacion_id: int, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Función de carga de una planeación guardada en almacenamiento local."""
    return obtener_planeacion_por_id(planeacion_id, db_path)

def cargar_archivo_planeacion(nombre_archivo: str, username: Optional[str] = None, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Carga una planeación buscando por su nombre personalizado de archivo."""
    user = username or "docente"
    return obtener_planeacion_por_nombre(user, nombre_archivo, db_path)

def guardar_planeacion_con_nombre(
    username: str,
    data: Dict[str, Any],
    nombre_archivo: str,
    categoria_ruta: Optional[str] = None,
    es_autoguardado: bool = False,
    db_path: Optional[str] = None
) -> Optional[int]:
    """Guarda una planeación asignando explícitamente nombre de archivo y categoría."""
    return guardar_planeacion(
        username=username,
        data=data,
        es_autoguardado=es_autoguardado,
        version_nombre=nombre_archivo,
        nombre_archivo=nombre_archivo,
        categoria_ruta=categoria_ruta,
        db_path=db_path
    )

def guardar_planeacion_nombre_ruta(
    username: str,
    data: Dict[str, Any],
    nombre_archivo: Optional[str] = None,
    categoria_ruta: Optional[str] = None,
    es_autoguardado: bool = False,
    db_path: Optional[str] = None
) -> Optional[int]:
    """Guarda una planeación asociando nombre de archivo y ruta organizativa."""
    return guardar_planeacion(
        username=username,
        data=data,
        es_autoguardado=es_autoguardado,
        version_nombre=nombre_archivo or "Version",
        nombre_archivo=nombre_archivo,
        categoria_ruta=categoria_ruta,
        db_path=db_path
    )

def guardar_con_nombre_ruta(
    username: str,
    data: Dict[str, Any],
    nombre_archivo: Optional[str] = None,
    categoria_ruta: Optional[str] = None,
    es_autoguardado: bool = False,
    db_path: Optional[str] = None
) -> Optional[int]:
    """Alias para guardar_planeacion_nombre_ruta."""
    return guardar_planeacion_nombre_ruta(
        username=username,
        data=data,
        nombre_archivo=nombre_archivo,
        categoria_ruta=categoria_ruta,
        es_autoguardado=es_autoguardado,
        db_path=db_path
    )

def listar_archivos_guardados(username: str, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Alias para listar todas las planeaciones y archivos guardados."""
    return listar_planeaciones(username, db_path)

def listar_planeaciones_guardadas(username: str, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Alias para listar todas las planeaciones y archivos guardados."""
    return listar_planeaciones(username, db_path)

def eliminar_planeacion(planeacion_id: int, db_path: Optional[str] = None) -> bool:
    """Alias para eliminar una planeación por su ID."""
    return eliminar_planeacion_por_id(planeacion_id, db_path)

def listar_categorias_rutas(username: Optional[str] = None, db_path: Optional[str] = None) -> List[str]:
    """Retorna la lista de categorías y carpetas de ruta disponibles."""
    cats = list(CATEGORIAS_RUTAS_DEFAULT)
    if username:
        planes = listar_planeaciones(username, db_path)
        for p in planes:
            c = p.get("categoria_ruta")
            if c and c not in cats:
                cats.append(c)
    return cats

def obtener_planeaciones_por_categoria(
    username: str,
    categoria: Optional[str] = None,
    db_path: Optional[str] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """Agrupa las planeaciones del docente por su categoría o carpeta de destino."""
    planes = listar_planeaciones(username, db_path)
    resultado: Dict[str, List[Dict[str, Any]]] = {}
    for p in planes:
        c = p.get("categoria_ruta") or "Carpeta General"
        if categoria and c != categoria:
            continue
        resultado.setdefault(c, []).append(p)
    return resultado

CATEGORIAS_RUTAS = CATEGORIAS_RUTAS_DEFAULT
DIR_GUARDADOS = DIR_GUARDADOS_DEFAULT

__all__ = [
    "DB_FILENAME",
    "DIR_GUARDADOS",
    "DIR_GUARDADOS_DEFAULT",
    "CATEGORIAS_RUTAS",
    "CATEGORIAS_RUTAS_DEFAULT",
    "get_db_path",
    "init_db",
    "calcular_hash_planeacion",
    "sanitizar_nombre_ruta",
    "guardar_archivo_fisico_json",
    "guardar_planeacion",
    "guardar_planeacion_con_nombre",
    "guardar_planeacion_nombre_ruta",
    "guardar_con_nombre_ruta",
    "listar_planeaciones",
    "listar_archivos_guardados",
    "listar_planeaciones_guardadas",
    "obtener_planeacion_por_id",
    "obtener_planeacion_por_nombre",
    "cargar_planeacion",
    "cargar_planeacion_guardada",
    "cargar_archivo_planeacion",
    "eliminar_planeacion_por_id",
    "eliminar_planeacion",
    "obtener_resumen_semanas_cubiertas",
    "listar_categorias_rutas",
    "obtener_planeaciones_por_categoria"
]
