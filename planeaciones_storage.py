"""
Módulo de Persistencia, Historial y Autoguardado de Planeaciones Didácticas (NEM)
Utiliza SQLite para almacenamiento local ligero, atómico, seguro y sin dependencias externas.
Permite autoguardado en tiempo real por usuario y semana (1 a 37), historial de versiones y restauración completa.
"""

import sqlite3
import json
import os
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any

DB_FILENAME = "planeaciones_storage.db"

def get_db_path(custom_path: Optional[str] = None) -> str:
    if custom_path:
        return custom_path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, DB_FILENAME)

def init_db(db_path: Optional[str] = None) -> None:
    """Inicializa la base de datos y crea las tablas e índices si no existen."""
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
                hash_contenido TEXT
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_semana ON planeaciones(username, semana)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_timestamp ON planeaciones(username, timestamp DESC)")
        conn.commit()
    finally:
        conn.close()

def calcular_hash_planeacion(data: Dict[str, Any]) -> str:
    """Calcula un hash MD5 de los datos clave para evitar escrituras redundantes si nada ha cambiado."""
    clave = f"{data.get('semana')}|{data.get('campos_formativos')}|{data.get('metodologia')}|" \
            f"{data.get('ejes_articuladores')}|{data.get('contenidos_pda')}|{data.get('libros_seleccionados')}|" \
            f"{data.get('dias_seleccionados')}|{data.get('directrices')}|{data.get('num_sesiones')}|" \
            f"{len(data.get('planeacion_generada') or '')}|{data.get('planeacion_generada')}"
    return hashlib.md5(clave.encode("utf-8", errors="ignore")).hexdigest()

def guardar_planeacion(
    username: str,
    data: Dict[str, Any],
    es_autoguardado: bool = True,
    version_nombre: str = "Autoguardado",
    db_path: Optional[str] = None
) -> Optional[int]:
    """
    Guarda o actualiza una planeación en la base de datos local.
    Si es autoguardado, actualiza el registro existente de ese usuario y semana escolar.
    Si no es autoguardado (guardado manual con versión), inserta un nuevo registro en el historial.
    """
    init_db(db_path)
    path = get_db_path(db_path)
    now = datetime.now()
    fecha_str = now.strftime("%d/%m/%Y %H:%M:%S")
    timestamp = now.timestamp()
    
    semana = int(data.get("semana", 20))
    periodo = str(data.get("periodo", f"Semana {semana} de 37"))
    grado = str(data.get("grado", '6° de Primaria'))
    grupo = str(data.get("grupo", 'A'))
    
    campos_list = data.get("campos_formativos") or []
    campos_str_display = ", ".join(campos_list[:2]) + ("..." if len(campos_list) > 2 else "")
    titulo = data.get("titulo") or f"Semana {semana} ({periodo}) — {campos_str_display}"
    
    campos_json = json.dumps(campos_list, ensure_ascii=False)
    metodologia = str(data.get("metodologia", "Aprendizaje Basado en Proyectos Comunitarios"))
    ejes_json = json.dumps(data.get("ejes_articuladores") or [], ensure_ascii=False)
    pda_json = json.dumps(data.get("contenidos_pda") or [], ensure_ascii=False)
    libros_json = json.dumps(data.get("libros_seleccionados") or [], ensure_ascii=False)
    guia_cte = str(data.get("guia_cte", ""))
    dias_json = json.dumps(data.get("dias_seleccionados") or ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"], ensure_ascii=False)
    dias_fechas_json = json.dumps(data.get("dias_fechas") or {}, ensure_ascii=False)
    directrices = str(data.get("directrices") or "")
    num_sesiones = int(data.get("num_sesiones", 5))
    planeacion_generada = data.get("planeacion_generada") or ""
    prompt_enviado = data.get("prompt_enviado") or ""
    url_referencia = str(data.get("url_referencia") or "")
    hash_cont = calcular_hash_planeacion(data)

    conn = sqlite3.connect(path)
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
                # Si el contenido no ha cambiado, no hacer escritura innecesaria
                if exist_hash == hash_cont:
                    return exist_id
                
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
                        hash_contenido = ?
                    WHERE id = ?
                """, (
                    periodo, titulo, grado, grupo, fecha_str, timestamp,
                    campos_json, metodologia, ejes_json, pda_json, libros_json,
                    guia_cte, dias_json, dias_fechas_json, directrices, num_sesiones,
                    planeacion_generada, prompt_enviado, url_referencia, version_nombre,
                    hash_cont, exist_id
                ))
                conn.commit()
                return exist_id

        # Insertar nuevo registro
        cursor.execute("""
            INSERT INTO planeaciones (
                username, semana, periodo, titulo, grado, grupo,
                fecha_guardado, timestamp, campos_formativos, metodologia,
                ejes_articuladores, contenidos_pda, libros_seleccionados,
                guia_cte, dias_seleccionados, dias_fechas, directrices,
                num_sesiones, planeacion_generada, prompt_enviado,
                url_referencia, es_autoguardado, version_nombre, hash_contenido
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username, semana, periodo, titulo, grado, grupo,
            fecha_str, timestamp, campos_json, metodologia,
            ejes_json, pda_json, libros_json,
            guia_cte, dias_json, dias_fechas_json, directrices,
            num_sesiones, planeacion_generada, prompt_enviado,
            url_referencia, 1 if es_autoguardado else 0, version_nombre, hash_cont
        ))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def listar_planeaciones(username: str, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Lista el historial de planeaciones guardadas para el usuario,
    ordenadas por semana y fecha de guardado.
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
            
            resultado.append({
                "id": r["id"],
                "username": r["username"],
                "semana": r["semana"],
                "periodo": r["periodo"],
                "titulo": r["titulo"],
                "grado": r["grado"],
                "grupo": r["grupo"],
                "fecha_guardado": r["fecha_guardado"],
                "timestamp": r["timestamp"],
                "campos_formativos": campos_list,
                "metodologia": r["metodologia"],
                "num_sesiones": r["num_sesiones"],
                "es_autoguardado": bool(r["es_autoguardado"]),
                "version_nombre": r["version_nombre"],
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

        return {
            "id": row["id"],
            "username": row["username"],
            "semana": row["semana"],
            "periodo": row["periodo"],
            "titulo": row["titulo"],
            "grado": row["grado"],
            "grupo": row["grupo"],
            "fecha_guardado": row["fecha_guardado"],
            "timestamp": row["timestamp"],
            "campos_formativos": safe_json(row["campos_formativos"], []),
            "metodologia": row["metodologia"],
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
            "hash_contenido": row["hash_contenido"]
        }
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
