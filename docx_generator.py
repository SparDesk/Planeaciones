"""
Generador de documentos oficiales en formato Microsoft Word (.docx)
para las planeaciones escolares de la Primaria Revolución Social 1910.
Adopta estrictamente el diseño, tipografía y la paleta de colores estilo Gemini:
- Tipografía global oficial SEP ('Arial', 10 pt)
- Manipulación XML (w:shd) con sintaxis: <w:shd w:val="clear" w:color="auto" w:fill="HEX_COLOR"/>
- Encabezados principales (Días de la semana, CAMPO FORMATIVO, etc.): Fondo Morado Intenso (#7209B7), texto blanco, negrita y centrado.
- Subencabezados o Secciones (Inicio, Desarrollo, Cierre, Dictado, Cálculo, etc.): Fondo Lavanda / Lila Suave (#F3E8FF), texto Morado Oscuro (#311B92), negrita.
- Celdas de contenido (texto de planeación, dictado, desarrollo): Fondo completamente Blanco (#FFFFFF), texto oscuro.
- Bordes de tabla finos en morado tenue (#D8B4FE) para diseño limpio y minimalista.
"""

import io
import re
from typing import Dict, Any
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# Paleta de Colores Estilo Gemini
COLOR_MORADO_INTENSO = RGBColor(114, 9, 183)    # #7209B7 (Encabezados principales)
COLOR_MORADO_OSCURO = RGBColor(49, 27, 146)     # #311B92 (Subencabezados / Secciones)
COLOR_TEXTO_OSCURO = RGBColor(30, 41, 59)       # #1E293B (Celdas de contenido)
COLOR_BLANCO = RGBColor(255, 255, 255)           # #FFFFFF

HEX_MORADO_INTENSO = "7209B7"
HEX_MORADO_OSCURO = "311B92"
HEX_LILA_SUAVE = "F3E8FF"
HEX_BLANCO = "FFFFFF"
HEX_BORDE_TENUE = "D8B4FE"

DIAS_FECHAS_OFICIALES = {
    "Lunes": "LUNES 02 DE FEBRERO DE 2026",
    "Martes": "MARTES 03 DE FEBRERO DE 2026",
    "Miércoles": "MIÉRCOLES 04 DE FEBRERO DE 2026",
    "Jueves": "JUEVES 05 DE FEBRERO DE 2026",
    "Viernes": "VIERNES 06 DE FEBRERO DE 2026"
}


def extract_day_from_text(text: str) -> str:
    """Identifica el día de la semana normalizando acentos y variantes."""
    if not text:
        return ""
    t = text.lower()
    if re.search(r'\blunes\b', t):
        return "Lunes"
    if re.search(r'\bmartes\b', t):
        return "Martes"
    if re.search(r'\bmi[eé]rcoles\b', t):
        return "Miércoles"
    if re.search(r'\bjueves\b', t):
        return "Jueves"
    if re.search(r'\bviernes\b', t):
        return "Viernes"
    return ""


def set_cell_background(cell, hex_color: str):
    """
    Establece el color de fondo de una celda en formato XML inyectando
    el elemento <w:shd w:val="clear" w:color="auto" w:fill="HEX_COLOR"/> en tcPr.
    """
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('shd'):
            tcPr.remove(child)
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{hex_color}"/>')
    tcPr.append(shading_elm)


def set_table_borders(table, color="D8B4FE", sz="4", val="single"):
    """
    Configura bordes finos en un color gris claro o morado tenue (D8B4FE)
    para que el diseño de las tablas luzca limpio, minimalista y elegante.
    """
    tblPr = table._tbl.tblPr
    for child in list(tblPr):
        if child.tag.endswith('tblBorders'):
            tblPr.remove(child)
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def set_cell_margins(cell, top=80, bottom=80, left=100, right=100):
    """Ajusta los márgenes interiores (padding) de una celda."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def parse_plan_sections(plan_text: str) -> Dict[str, Any]:
    """Extrae las secciones pedagógicas del texto en Markdown para rellenar tablas."""
    data = {
        "nombre_proyecto": "Guardianes de la Memoria y la Salud Comunitaria",
        "campo_formativo": "Lenguajes, Saberes y Pensamiento Científico",
        "duracion": "2 semanas (10 sesiones)",
        "proposito": "Investigar los hábitos de alimentación e historia comunitaria mediante proyectos para fortalecer la lectura, redacción y pensamiento matemático.",
        "metodologia": "Aprendizaje Basado en Proyectos Comunitarios",
        "escenario": "Comunitario y de Aula",
        "libros_texto": "Proyectos Comunitarios (págs. 20-33), Nuestros Saberes (págs. 68-75)",
        "problematica": "Dificultades en la redacción autónoma de textos informativos, comprensión lectora y resolución de problemas fraccionarios.",
        "ejes": "Pensamiento crítico, Vida saludable, Apropiación de las culturas a través de la lectura y la escritura",
        "contenidos": "Comprensión y producción de textos informativos sobre temas colectivos.",
        "pda": "Selecciona y lee textos informativos; elabora resúmenes y trípticos para difundir en la comunidad.",
        "rutinas": [],
        "sesiones": [],
        "rutinas_por_dia": {},
        "sesiones_por_dia": {},
        "adecuaciones": "Uso de apoyos visuales y tutoría entre pares. Graduación de problemas con material concreto.",
        "observaciones": "Seguimiento puntual a estudiantes con rezago en el diario de campo del docente."
    }

    # Extraer campos de identificación curricular
    m_proj = re.search(r'Nombre (?:sugerido para el |del )?Proyecto[:\s\*]+([^\n]+)', plan_text, re.IGNORECASE)
    if m_proj:
        data["nombre_proyecto"] = m_proj.group(1).replace('"', '').replace('*', '').strip()

    m_campo = re.search(r'Campo(?:s)? Formativo(?:s)?[:\s\*]+([^\n]+)', plan_text, re.IGNORECASE)
    if m_campo:
        data["campo_formativo"] = m_campo.group(1).replace('*', '').strip()

    m_dur = re.search(r'Duración(?: Total)?(?: del Plan)?[:\s\*]+([^\n]+)', plan_text, re.IGNORECASE)
    if m_dur:
        data["duracion"] = m_dur.group(1).replace('*', '').strip()

    m_prop = re.search(r'Propósito[:\s\*]+([^\n]+)', plan_text, re.IGNORECASE)
    if m_prop:
        data["proposito"] = m_prop.group(1).replace('*', '').strip()

    m_met = re.search(r'Metodología(?: Sociocrítica)?[:\s\*]+([^\n]+)', plan_text, re.IGNORECASE)
    if m_met:
        data["metodologia"] = m_met.group(1).replace('*', '').strip()

    m_ejes = re.search(r'Ejes Articuladores[:\s\*]+([^\n]+)', plan_text, re.IGNORECASE)
    if m_ejes:
        data["ejes"] = m_ejes.group(1).replace('*', '').strip()

    m_lib = re.search(r'Libros de Texto(?: Gratuitos)?(?: \(LTG\))?[:\s\*]+([^\n]+)', plan_text, re.IGNORECASE)
    if m_lib:
        data["libros_texto"] = m_lib.group(1).replace('*', '').strip()

    m_prob = re.search(r'Problemática(?: del Plan Analítico)?[:\s\*]+([^\n]+)', plan_text, re.IGNORECASE)
    if m_prob:
        data["problematica"] = m_prob.group(1).replace('*', '').strip()

    m_cont = re.search(r'Contenido(?: Sintético)?[:\s\*]+([^\n]+)', plan_text, re.IGNORECASE)
    if m_cont:
        data["contenidos"] = m_cont.group(1).replace('*', '').strip()

    m_pda = re.search(r'PDA[:\s\*]+([^\n]+)', plan_text, re.IGNORECASE)
    if m_pda:
        data["pda"] = m_pda.group(1).replace('*', '').strip()

    # 1. Extraer actividades de inicio (rutina matutina) de la Sección III
    sec_iii_match = re.search(r'# III\..*?(?=# IV\.|\Z)', plan_text, re.DOTALL)
    sec_iii_text = sec_iii_match.group(0) if sec_iii_match else plan_text

    rutina_blocks = re.findall(r'(###[^\n]+)(.*?)(?=\n###|\n# |\Z)', sec_iii_text, re.DOTALL)
    for idx_r, (hdr, block) in enumerate(rutina_blocks, 1):
        num_m = re.search(r'Sesión (\d+)', hdr, re.IGNORECASE)
        num = num_m.group(1) if num_m else str(idx_r)
        day_detected = extract_day_from_text(hdr) or extract_day_from_text(block[:120])
        dictado_m = re.search(r'Dictado[:\s\*]+([^\n]+)', block, re.IGNORECASE)
        calculo_m = re.search(r'Cálculo Mental[:\s\*]+([^\n]+)', block, re.IGNORECASE)
        problema_m = re.search(r'Problema (?:Matemático )?Razonado[:\s\*]+([^\n]+)', block, re.IGNORECASE)

        r_item = {
            "sesion": num,
            "dia": day_detected,
            "dictado": dictado_m.group(1).replace('*', '').strip() if dictado_m else "Palabras clave del vocabulario científico y ortográfico.",
            "calculo": calculo_m.group(1).replace('*', '').strip() if calculo_m else "Operaciones combinadas de cálculo mental rápido.",
            "problema": problema_m.group(1).replace('*', '').strip() if problema_m else "Problema razonado de situaciones de la vida cotidiana."
        }
        data["rutinas"].append(r_item)
        if day_detected:
            data["rutinas_por_dia"][day_detected] = r_item

    # 2. Extraer secuencias didácticas de la Sección IV
    sec_iv_match = re.search(r'# IV\..*?(?=# V\.|\Z)', plan_text, re.DOTALL)
    sec_iv_text = sec_iv_match.group(0) if sec_iv_match else plan_text

    sesion_blocks = re.findall(r'(###[^\n]+)(.*?)(?=\n###|\n# |\Z)', sec_iv_text, re.DOTALL)
    for idx_s, (hdr, block) in enumerate(sesion_blocks, 1):
        num_m = re.search(r'Sesión (\d+)', hdr, re.IGNORECASE)
        num = num_m.group(1) if num_m else str(idx_s)
        day_detected = extract_day_from_text(hdr) or extract_day_from_text(block[:120])

        inicio_m = re.search(r'(?:^|\n)[ \t]*(?:[-*][ \t]*)?(?:\*\*)?Inicio[^\:\n]*\:(.*?)(?=(?:\n[ \t]*(?:[-*][ \t]*)?(?:\*\*)?Desarrollo)|\Z)', block, re.DOTALL | re.IGNORECASE)
        desarrollo_m = re.search(r'(?:^|\n)[ \t]*(?:[-*][ \t]*)?(?:\*\*)?Desarrollo[^\:\n]*\:(.*?)(?=(?:\n[ \t]*(?:[-*][ \t]*)?(?:\*\*)?Cierre)|\Z)', block, re.DOTALL | re.IGNORECASE)
        cierre_m = re.search(r'(?:^|\n)[ \t]*(?:[-*][ \t]*)?(?:\*\*)?Cierre[^\:\n]*\:(.*?)(?=(?:\n[ \t]*(?:[-*][ \t]*)?(?:\*\*)?Recursos|\n[ \t]*(?:[-*][ \t]*)?(?:\*\*)?Evidencia)|\Z)', block, re.DOTALL | re.IGNORECASE)
        recursos_m = re.search(r'(?:^|\n)[ \t]*(?:[-*][ \t]*)?(?:\*\*)?Recursos[^\:\n]*\:(.*?)(?=(?:\n[ \t]*(?:[-*][ \t]*)?(?:\*\*)?Evidencia)|\Z)', block, re.DOTALL | re.IGNORECASE)
        proposito_m = re.search(r'Propósito(?: de la sesión)?[:\s\*]+([^\n]+)', block, re.IGNORECASE)

        inicio_txt = inicio_m.group(1).replace('*', '').strip() if inicio_m else "[Redactar actividades de inicio aquí]"
        desarrollo_txt = desarrollo_m.group(1).replace('*', '').strip() if desarrollo_m else "[Redactar actividades de desarrollo aquí]"
        cierre_txt = cierre_m.group(1).replace('*', '').strip() if cierre_m else "[Redactar actividades de cierre aquí]"
        recursos_txt = recursos_m.group(1).replace('*', '').strip() if recursos_m else "Libro de texto gratuito, libreta de notas y materiales del aula."
        proposito_txt = proposito_m.group(1).replace('*', '').strip() if proposito_m else "Reconocer y aplicar saberes comunitarios."

        s_item = {
            "sesion": num,
            "dia": day_detected,
            "inicio": inicio_txt,
            "desarrollo": desarrollo_txt,
            "cierre": cierre_txt,
            "recursos": recursos_txt,
            "proposito": proposito_txt
        }
        data["sesiones"].append(s_item)
        if day_detected:
            data["sesiones_por_dia"][day_detected] = s_item

    return data


def add_initial_signatures(doc, datos_escuela: Dict[str, Any]):
    """
    Distribución Inicial Paso 1:
    Genera las líneas de firmas centradas para el Director Escolar y Docente titular del Grupo.
    """
    docente = datos_escuela.get("docente", "Maestra Aday Domínguez Domínguez") if datos_escuela else "Maestra Aday Domínguez Domínguez"
    director = datos_escuela.get("director", "Guillermo Gerardo Borjas Díaz") if datos_escuela else "Guillermo Gerardo Borjas Díaz"

    table_firmas = doc.add_table(rows=2, cols=2)
    table_firmas.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_firmas.autofit = False
    set_table_borders(table_firmas, color=HEX_BORDE_TENUE)

    row0 = table_firmas.rows[0]
    row0.cells[0].text = "____________________________________________\nDOCENTE TITULAR DEL GRUPO"
    row0.cells[1].text = "____________________________________________\nDIRECTOR ESCOLAR"

    row1 = table_firmas.rows[1]
    row1.cells[0].text = f"Prof(a). {docente}"
    row1.cells[1].text = f"Prof. {director}"

    col_widths = [Inches(3.75), Inches(3.75)]
    for r in [row0, row1]:
        for c_idx, c in enumerate(r.cells):
            c.width = col_widths[c_idx]
            set_cell_background(c, HEX_BLANCO)
            c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_cell_margins(c, top=40, bottom=40, left=60, right=60)
            if c.paragraphs and c.paragraphs[0].runs:
                c.paragraphs[0].runs[0].font.name = 'Arial'
                c.paragraphs[0].runs[0].font.size = Pt(8.5)
                c.paragraphs[0].runs[0].font.bold = True
                c.paragraphs[0].runs[0].font.color.rgb = COLOR_MORADO_OSCURO

    doc.add_paragraph()  # Espacio


def add_institutional_header_table(doc, datos_escuela: Dict[str, Any]):
    """
    Distribución Inicial Paso 2:
    Crea la tabla de encabezado institucional con paleta estilo Gemini:
    Fondo Lavanda/Lila Suave (#F3E8FF) con texto Morado Oscuro (#311B92).
    """
    nombre_escuela = datos_escuela.get("nombre_escuela", "Escuela Primaria “Revolución Social de 1910”") if datos_escuela else "Escuela Primaria “Revolución Social de 1910”"
    cct = datos_escuela.get("cct", "10EPR0361N") if datos_escuela else "10EPR0361N"
    periodo = datos_escuela.get("periodo", "Semana 20 de 37") if datos_escuela else "Semana 20 de 37"
    ciclo = datos_escuela.get("ciclo_escolar", "2026-2027") if datos_escuela else "2026-2027"
    grado = datos_escuela.get("grado", "6° de Primaria") if datos_escuela else "6° de Primaria"
    grupo = datos_escuela.get("grupo", "A") if datos_escuela else "A"
    fase = datos_escuela.get("fase", "Fase 5") if datos_escuela else "Fase 5"
    turno = datos_escuela.get("turno", "Matutino") if datos_escuela else "Matutino"
    zona_str = f"{datos_escuela.get('zona_escolar', 'Zona 49')} / {datos_escuela.get('sector', 'Sector 02')}" if datos_escuela else "Zona 49 / Sector 02"

    t_inst = doc.add_table(rows=2, cols=4)
    t_inst.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_inst.autofit = False
    set_table_borders(t_inst, color=HEX_BORDE_TENUE)

    meta_rows = [
        [("Nombre de la Escuela:", nombre_escuela.upper()), ("C.C.T.:", cct), ("Semana:", periodo), ("Ciclo Escolar:", ciclo)],
        [("Grado y Grupo:", f"{grado} '{grupo}'"), ("Fase Curricular:", fase), ("Turno:", turno), ("Zona Escolar:", zona_str)]
    ]
    for r_i, r_data in enumerate(meta_rows):
        for c_i, (lbl, val) in enumerate(r_data):
            cell = t_inst.rows[r_i].cells[c_i]
            cell.width = Inches(1.87)
            set_cell_background(cell, HEX_LILA_SUAVE if r_i == 0 else HEX_BLANCO)
            set_cell_margins(cell, top=45, bottom=45, left=55, right=55)
            cell.text = ""
            p = cell.paragraphs[0]
            r_lbl = p.add_run(f"{lbl}\n")
            r_lbl.font.name = 'Arial'
            r_lbl.font.size = Pt(7.5)
            r_lbl.font.bold = True
            r_lbl.font.color.rgb = COLOR_MORADO_OSCURO

            r_val = p.add_run(val)
            r_val.font.name = 'Arial'
            r_val.font.size = Pt(8)
            r_val.font.color.rgb = COLOR_TEXTO_OSCURO

    doc.add_paragraph()  # Espacio


def add_horario_escolar_table(doc, datos_escuela=None):
    """
    Distribución Inicial Paso 3:
    Genera la tabla general del HORARIO ESCOLAR con paleta estilo Gemini:
    - Encabezados principales: Fondo Morado Intenso (#7209B7), texto blanco centrado.
    - Columna de horarios: Fondo Lavanda/Lila Suave (#F3E8FF), texto Morado Oscuro (#311B92).
    - Celdas de contenido: Fondo Blanco (#FFFFFF), texto oscuro.
    - Bordes finos en morado tenue (#D8B4FE).
    """
    fase = datos_escuela.get('fase', 'Fase 5') if datos_escuela else 'Fase 5'
    grado = datos_escuela.get('grado', '5° de Primaria') if datos_escuela else '5° de Primaria'

    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_h = p_h.add_run(f"HORARIO ESCOLAR — {fase.upper()} ({grado.upper()})")
    r_h.font.name = 'Arial'
    r_h.font.bold = True
    r_h.font.size = Pt(11)
    r_h.font.color.rgb = COLOR_MORADO_INTENSO

    headers = ["Horario", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    table_h = doc.add_table(rows=7, cols=len(headers))
    table_h.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_h.autofit = False
    set_table_borders(table_h, color=HEX_BORDE_TENUE)

    col_widths = [Inches(1.5), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.2), Inches(1.2)]
    for c_idx, h_text in enumerate(headers):
        cell = table_h.rows[0].cells[c_idx]
        cell.text = h_text
        cell.width = col_widths[c_idx]
        set_cell_background(cell, HEX_MORADO_INTENSO)
        set_cell_margins(cell, top=50, bottom=50, left=50, right=50)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p.runs:
            p.runs[0].font.name = 'Arial'
            p.runs[0].font.bold = True
            p.runs[0].font.size = Pt(8)
            p.runs[0].font.color.rgb = COLOR_BLANCO

    raw_schedule = [
        ("08:00 - 08:30", ["Act. de Inicio", "Act. de Inicio", "Act. de Inicio", "Act. de Inicio", "Act. de Inicio"]),
        ("08:30 - 10:00", ["Lenguajes", "Lenguajes", "Lenguajes", "Lenguajes", "Lenguajes"]),
        ("10:00 - 10:30", ["RECESO", "RECESO", "RECESO", "RECESO", "RECESO"]),
        ("10:30 - 11:30", ["Pensamiento C.", "Pensamiento C.", "Pensamiento C.", "Pensamiento C.", "Pensamiento C."]),
        ("11:30 - 12:15", ["Ética, Nat. y Soc.", "Ética, Nat. y Soc.", "Ética, Nat. y Soc.", "Ética, Nat. y Soc.", "Ética, Nat. y Soc."]),
        ("12:15 - 13:00", ["De lo Humano", "Ed. Física", "De lo Humano", "Artes", "De lo Humano"])
    ]

    for r_idx, (hora, materias) in enumerate(raw_schedule, 1):
        row = table_h.rows[r_idx]
        row_vals = [hora] + materias
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.text = val
            cell.width = col_widths[c_idx]
            set_cell_margins(cell, top=45, bottom=45, left=45, right=45)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER

            if c_idx == 0:
                # Subencabezado de horario: Fondo Lila Suave, texto Morado Oscuro negrita
                set_cell_background(cell, HEX_LILA_SUAVE)
                if p.runs:
                    p.runs[0].font.name = 'Arial'
                    p.runs[0].font.size = Pt(7.5)
                    p.runs[0].font.bold = True
                    p.runs[0].font.color.rgb = COLOR_MORADO_OSCURO
            elif val == "RECESO":
                # Resaltado especial de receso
                set_cell_background(cell, HEX_LILA_SUAVE)
                if p.runs:
                    p.runs[0].font.name = 'Arial'
                    p.runs[0].font.size = Pt(7.5)
                    p.runs[0].font.bold = True
                    p.runs[0].font.color.rgb = COLOR_MORADO_INTENSO
            else:
                # Celdas de contenido: Fondo Blanco (#FFFFFF)
                set_cell_background(cell, HEX_BLANCO)
                if p.runs:
                    p.runs[0].font.name = 'Arial'
                    p.runs[0].font.size = Pt(7.5)
                    p.runs[0].font.color.rgb = COLOR_TEXTO_OSCURO

    doc.add_paragraph()  # Espacio


def add_project_metadata_table(doc, parsed_info: Dict[str, Any], datos_escuela: Dict[str, Any]):
    """
    Distribución Inicial Paso 4:
    Crea la tabla de metadatos del proyecto con paleta estilo Gemini:
    Subencabezados en Morado Oscuro sobre fondo Lila Suave (#F3E8FF) / Blanco (#FFFFFF).
    """
    campo_formativo = parsed_info.get("campo_formativo", "Lenguajes, Saberes y Pensamiento Científico")
    if datos_escuela and "campos_formativos" in datos_escuela and datos_escuela["campos_formativos"]:
        if isinstance(datos_escuela["campos_formativos"], list):
            campo_formativo = ", ".join(datos_escuela["campos_formativos"])
        else:
            campo_formativo = str(datos_escuela["campos_formativos"])

    periodo = datos_escuela.get('periodo', 'Semana 20 de 37') if datos_escuela else 'Semana 20'
    duracion = parsed_info.get("duracion", f"{periodo} (2 semanas)")
    fase = datos_escuela.get('fase', 'Fase 5') if datos_escuela else 'Fase 5'
    grado = datos_escuela.get('grado', '5° de Primaria') if datos_escuela else '5° de Primaria'
    grupo = datos_escuela.get('grupo', 'A') if datos_escuela else 'A'

    t_meta = doc.add_table(rows=6, cols=2)
    t_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_meta.autofit = False
    set_table_borders(t_meta, color=HEX_BORDE_TENUE)

    meta_cells = [
        (("Nombre del Proyecto:", parsed_info['nombre_proyecto']), ("Campo Formativo:", campo_formativo)),
        (("Duración:", duracion), ("Metodología:", parsed_info['metodologia'])),
        (("Escenario:", parsed_info['escenario']), ("Libro de Texto:", parsed_info['libros_texto'])),
        (("Problemática:", parsed_info['problematica']), ("Ejes Articuladores:", parsed_info['ejes'])),
        (("Propósito:", parsed_info['proposito']), ("Fase y Grado:", f"{fase} — {grado} '{grupo}'")),
        (("Contenidos:", parsed_info['contenidos']), ("PDA:", parsed_info['pda']))
    ]

    for r_i, (c0_pair, c1_pair) in enumerate(meta_cells):
        r = t_meta.rows[r_i]
        bg_color = HEX_LILA_SUAVE if r_i % 2 == 0 else HEX_BLANCO
        for c_i, (lbl, val) in enumerate([c0_pair, c1_pair]):
            cell = r.cells[c_i]
            cell.width = Inches(3.75)
            set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
            cell.text = ""
            p = cell.paragraphs[0]
            r_lbl = p.add_run(f"{lbl}\n")
            r_lbl.font.name = 'Arial'
            r_lbl.font.size = Pt(7.5)
            r_lbl.font.bold = True
            r_lbl.font.color.rgb = COLOR_MORADO_OSCURO

            r_val = p.add_run(val)
            r_val.font.name = 'Arial'
            r_val.font.size = Pt(8)
            r_val.font.color.rgb = COLOR_TEXTO_OSCURO

    doc.add_paragraph()  # Espacio


def add_document_credits(doc):
    """Agrega la frase oficial de créditos al pie del documento Word generado."""
    doc.add_paragraph()
    p_cred = doc.add_paragraph()
    p_cred.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cred = p_cred.add_run("Desarrollado para la labor pedagógica")
    r_cred.font.name = 'Arial'
    r_cred.font.size = Pt(8.5)
    r_cred.font.italic = True
    r_cred.font.color.rgb = COLOR_MORADO_OSCURO

    for section in doc.sections:
        footer = section.footer
        p_foot = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        p_foot.text = "Desarrollado para la labor pedagógica"
        p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p_foot.runs:
            p_foot.runs[0].font.name = 'Arial'
            p_foot.runs[0].font.size = Pt(8)
            p_foot.runs[0].font.italic = True
            p_foot.runs[0].font.color.rgb = RGBColor(148, 163, 184)


def build_docx_planeacion(datos_escuela: Dict[str, Any], plan_text: str) -> io.BytesIO:
    """
    Construye la planeación oficial en Word (.docx) con rediseño tecnológico estilo Gemini:
    - Tipografía global estándar SEP: 'Arial' 10 pt
    - Encabezados principales: Fondo Morado Intenso (#7209B7), texto Blanco, negrita y centrado.
    - Subencabezados o Secciones: Fondo Lavanda / Lila Suave (#F3E8FF), texto Morado Oscuro (#311B92), negrita.
    - Celdas de contenido: Fondo completamente Blanco (#FFFFFF), texto oscuro (#1E293B).
    - Bordes de tablas finos en morado tenue (#D8B4FE).
    - Secuencia de actividades optimizada como la columna más ancha.
    """
    parsed_info = parse_plan_sections(plan_text)

    doc = Document()
    document = doc

    # Configuración del estilo global del documento: Arial 10 pt
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = COLOR_TEXTO_OSCURO
    rFonts = normal_style.element.rPr.get_or_add_rFonts()
    rFonts.set(qn('w:ascii'), 'Arial')
    rFonts.set(qn('w:hAnsi'), 'Arial')
    rFonts.set(qn('w:cs'), 'Arial')

    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    # Encabezado principal del documento
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_header.add_run("SECRETARÍA DE EDUCACIÓN PÚBLICA — NUEVA ESCUELA MEXICANA\n")
    r_sub.font.name = 'Arial'
    r_sub.font.bold = True
    r_sub.font.size = Pt(9.5)
    r_sub.font.color.rgb = COLOR_MORADO_OSCURO

    r_plano = p_header.add_run("PLANO DIDÁCTICO DE INTERVENCIÓN DOCENTE")
    r_plano.font.name = 'Arial'
    r_plano.font.bold = True
    r_plano.font.size = Pt(12)
    r_plano.font.color.rgb = COLOR_MORADO_INTENSO

    # =======================================================
    # DISTRIBUCIÓN INICIAL (Antes de los días)
    # =======================================================
    # 1. Líneas de firmas centradas para "Director Escolar" y "Docente titular del Grupo"
    add_initial_signatures(doc, datos_escuela)

    # 2. Tabla de encabezado institucional (Nombre de Escuela, CCT, Semana y Ciclo Escolar)
    add_institutional_header_table(doc, datos_escuela)

    # 3. Tabla general del "HORARIO ESCOLAR" con columnas de lunes a viernes
    add_horario_escolar_table(doc, datos_escuela=datos_escuela)

    # 4. Tabla de metadatos del proyecto (Nombre, Campo, Duración, Metodología, Escenario, Libro, Problemática, Ejes, Propósito, Contenidos y PDA)
    add_project_metadata_table(doc, parsed_info, datos_escuela)

    # =======================================================
    # DISTRIBUCIÓN DINÁMICA POR DÍA (for dia in dias_seleccionados:)
    # =======================================================
    dias_seleccionados = datos_escuela.get('dias_seleccionados') or datos_escuela.get('dias_planeados') or ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    for dia in dias_seleccionados:
        dia_idx = dias_seleccionados.index(dia)

        # 1. Asignar la rutina correspondiente al día específico
        rutina = None
        if "rutinas_por_dia" in parsed_info and dia in parsed_info["rutinas_por_dia"]:
            rutina = parsed_info["rutinas_por_dia"][dia]
        elif dia_idx < len(parsed_info.get("rutinas", [])):
            rutina = parsed_info["rutinas"][dia_idx]

        if not rutina:
            rutina = {
                "dictado": f"Palabras clave y vocabulario ortográfico para {dia}.",
                "calculo": f"Operaciones combinadas de cálculo mental para {dia}.",
                "problema": f"Problema matemático razonado contextualizado para {dia}."
            }

        # 2. Asignar la secuencia didáctica correspondiente al día específico
        sesion = None
        if "sesiones_por_dia" in parsed_info and dia in parsed_info["sesiones_por_dia"]:
            sesion = parsed_info["sesiones_por_dia"][dia]
        elif dia_idx < len(parsed_info.get("sesiones", [])):
            sesion = parsed_info["sesiones"][dia_idx]

        if not sesion:
            sesion = {
                "inicio": f"[Redactar actividades de inicio para {dia} aquí]",
                "desarrollo": f"[Redactar actividades de desarrollo para {dia} aquí]",
                "cierre": f"[Redactar actividades de cierre para {dia} aquí]",
                "recursos": "Materiales del aula y libros de texto SEP.",
                "proposito": "Fortalecer saberes comunitarios y pensamiento crítico."
            }

        # Encabezado de nivel 2 para el día
        h_dia = document.add_heading(f"Día: {dia}", level=2)
        h_dia.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if h_dia.runs:
            h_dia.runs[0].font.name = 'Arial'
            h_dia.runs[0].font.size = Pt(11)
            h_dia.runs[0].font.bold = True
            h_dia.runs[0].font.color.rgb = COLOR_MORADO_INTENSO

        # Construir tabla unificada de 5 filas y 4 columnas
        table = document.add_table(rows=5, cols=4)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        set_table_borders(table, color=HEX_BORDE_TENUE)

        # Ajuste de Columnas: configurar anchos de celda de modo que la secuencia de actividades sea la más ancha
        col_widths = [Inches(1.4), Inches(3.4), Inches(1.2), Inches(1.5)]
        for row in table.rows:
            for c_i, w in enumerate(col_widths):
                row.cells[c_i].width = w

        # 1. Fila de Título del Día: Centrada, abarcando todas las columnas (ej. "MARTES 03 DE FEBRERO DE 2026")
        # Regla 1: Encabezado principal -> Fondo Morado Intenso (#7209B7), texto Blanco, negrita y centrado
        title_cell = table.rows[0].cells[0].merge(table.rows[0].cells[3])
        title_cell.width = Inches(7.5)
        dias_fechas_map = (datos_escuela.get("dias_fechas") or {}) if isinstance(datos_escuela, dict) else {}
        title_text = dias_fechas_map.get(dia) or DIAS_FECHAS_OFICIALES.get(dia, f"{dia.upper()} DE LA SEMANA ESCOLAR")
        title_cell.text = title_text
        set_cell_background(title_cell, HEX_MORADO_INTENSO)
        set_cell_margins(title_cell, top=60, bottom=60, left=80, right=80)
        p_title = title_cell.paragraphs[0]
        p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p_title.runs:
            p_title.runs[0].font.name = 'Arial'
            p_title.runs[0].font.bold = True
            p_title.runs[0].font.size = Pt(11)
            p_title.runs[0].font.color.rgb = COLOR_BLANCO

        # 2. Fila de Actividades de Inicio: Con las cabeceras exactas
        # Regla 2: Subencabezados o Secciones -> Fondo Lavanda o Lila Suave (#F3E8FF), texto Morado Oscuro (#311B92), negrita
        headers_inicio = ["ACTIVIDADES DE INICIO DEL DÍA", "DICTADO", "CÁLCULO MENTAL", "PROBLEMA MATEMÁTICO"]
        for c_idx, h_txt in enumerate(headers_inicio):
            c = table.rows[1].cells[c_idx]
            c.text = h_txt
            set_cell_background(c, HEX_LILA_SUAVE)
            set_cell_margins(c, top=45, bottom=45, left=45, right=45)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if p.runs:
                p.runs[0].font.name = 'Arial'
                p.runs[0].font.bold = True
                p.runs[0].font.size = Pt(8)
                p.runs[0].font.color.rgb = COLOR_MORADO_OSCURO

        # Fila 2: Llenar las celdas de inicio con la información correspondiente generada por la IA
        # Col 0: Subencabezado en Lila Suave (#F3E8FF)
        c0_rutina = table.rows[2].cells[0]
        c0_rutina.text = "RUTINA MATUTINA\nPERMANENTE"
        set_cell_background(c0_rutina, HEX_LILA_SUAVE)
        set_cell_margins(c0_rutina, top=45, bottom=45, left=45, right=45)
        p_r0 = c0_rutina.paragraphs[0]
        p_r0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if p_r0.runs:
            p_r0.runs[0].font.name = 'Arial'
            p_r0.runs[0].font.bold = True
            p_r0.runs[0].font.size = Pt(7.5)
            p_r0.runs[0].font.color.rgb = COLOR_MORADO_OSCURO

        # Cols 1, 2, 3: Regla 3 -> Celdas de contenido: Fondo completamente Blanco (#FFFFFF), texto Gris Oscuro
        contenido_inicio = [rutina.get("dictado", ""), rutina.get("calculo", ""), rutina.get("problema", "")]
        for c_idx, txt in enumerate(contenido_inicio, 1):
            c = table.rows[2].cells[c_idx]
            c.text = txt
            set_cell_background(c, HEX_BLANCO)
            set_cell_margins(c, top=45, bottom=45, left=45, right=45)
            if c.paragraphs and c.paragraphs[0].runs:
                c.paragraphs[0].runs[0].font.name = 'Arial'
                c.paragraphs[0].runs[0].font.size = Pt(7.5)
                c.paragraphs[0].runs[0].font.color.rgb = COLOR_TEXTO_OSCURO

        # 3. Fila de Cabeceras de Secuencia: "CAMPO FORMATIVO", "SECUENCIA DE ACTIVIDADES", etc.
        # Regla 1: Encabezados principales -> Fondo Morado Intenso (#7209B7), texto Blanco, negrita y centrado
        headers_secuencia = ["CAMPO FORMATIVO", "SECUENCIA DE ACTIVIDADES", "RECURSOS DIDÁCTICOS", "EVALUACIÓN"]
        for c_idx, h_txt in enumerate(headers_secuencia):
            c = table.rows[3].cells[c_idx]
            c.text = h_txt
            set_cell_background(c, HEX_MORADO_INTENSO)
            set_cell_margins(c, top=45, bottom=45, left=45, right=45)
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if p.runs:
                p.runs[0].font.name = 'Arial'
                p.runs[0].font.bold = True
                p.runs[0].font.size = Pt(8)
                p.runs[0].font.color.rgb = COLOR_BLANCO

        # 4. Filas de Campos Formativos: Por cada campo, coloca su nombre en la 1ra col,
        # y en la 2da divide claramente los momentos de "Inicio:", "Desarrollo:" y "Cierre:"
        campo_nombre = parsed_info.get("campo_formativo", "Lenguajes")
        if datos_escuela and "campos_formativos" in datos_escuela and datos_escuela["campos_formativos"]:
            if isinstance(datos_escuela["campos_formativos"], list):
                campo_nombre = ", ".join(datos_escuela["campos_formativos"])
            else:
                campo_nombre = str(datos_escuela["campos_formativos"])

        proposito_sesion = sesion.get("proposito") or parsed_info.get("proposito", "Fortalecer saberes de la comunidad y pensamiento crítico.")

        # Col 0: Subencabezado / Sección -> Fondo Lavanda o Lila Suave (#F3E8FF)
        c_campo = table.rows[4].cells[0]
        c_campo.text = f"{campo_nombre.upper()}\n\nSESIÓN {sesion.get('sesion', '1')}\n\nPropósito de la sesión:\n{proposito_sesion}"
        set_cell_background(c_campo, HEX_LILA_SUAVE)
        set_cell_margins(c_campo, top=45, bottom=45, left=45, right=45)
        if c_campo.paragraphs and c_campo.paragraphs[0].runs:
            c_campo.paragraphs[0].runs[0].font.name = 'Arial'
            c_campo.paragraphs[0].runs[0].font.size = Pt(7.5)
            c_campo.paragraphs[0].runs[0].font.bold = True
            c_campo.paragraphs[0].runs[0].font.color.rgb = COLOR_MORADO_OSCURO

        # Col 1: Regla 3 -> Celda de contenido con fondo completamente Blanco (#FFFFFF)
        # Subsecciones Inicio, Desarrollo, Cierre resaltadas en Morado Oscuro
        c_seq = table.rows[4].cells[1]
        c_seq.text = f"Inicio:\n{sesion['inicio']}\n\nDesarrollo:\n{sesion['desarrollo']}\n\nCierre:\n{sesion['cierre']}"
        set_cell_background(c_seq, HEX_BLANCO)
        set_cell_margins(c_seq, top=45, bottom=45, left=50, right=50)
        for p in c_seq.paragraphs:
            if p.runs:
                p.runs[0].font.name = 'Arial'
                p.runs[0].font.size = Pt(7.5)
                p.runs[0].font.color.rgb = COLOR_TEXTO_OSCURO

        # Col 2: Recursos didácticos -> Celda de contenido con fondo completamente Blanco (#FFFFFF)
        c_rec = table.rows[4].cells[2]
        c_rec.text = f"{sesion.get('recursos', 'Cuaderno del alumno, anexos y libros de texto SEP.')}"
        set_cell_background(c_rec, HEX_BLANCO)
        set_cell_margins(c_rec, top=45, bottom=45, left=45, right=45)
        if c_rec.paragraphs and c_rec.paragraphs[0].runs:
            c_rec.paragraphs[0].runs[0].font.name = 'Arial'
            c_rec.paragraphs[0].runs[0].font.size = Pt(7.5)
            c_rec.paragraphs[0].runs[0].font.color.rgb = COLOR_TEXTO_OSCURO

        # Col 3: Evaluación formativa -> Celda de contenido con fondo completamente Blanco (#FFFFFF)
        c_eva = table.rows[4].cells[3]
        c_eva.text = "Listas de cotejo, observación directa, registro en diario de campo y producciones en el cuaderno."
        set_cell_background(c_eva, HEX_BLANCO)
        set_cell_margins(c_eva, top=45, bottom=45, left=45, right=45)
        if c_eva.paragraphs and c_eva.paragraphs[0].runs:
            c_eva.paragraphs[0].runs[0].font.name = 'Arial'
            c_eva.paragraphs[0].runs[0].font.size = Pt(7.5)
            c_eva.paragraphs[0].runs[0].font.color.rgb = COLOR_TEXTO_OSCURO

        document.add_paragraph()

    add_document_credits(doc)

    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf
