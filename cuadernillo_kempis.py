"""
Módulo de Integración Curricular y Didáctica:
Cuadernillo de Actividades y Recursos de Apoyo (Semanas 6 y 7 - Profa Kempis).

Este módulo registra, indexa y enlaza las actividades prácticas, fichas de trabajo,
anexos imprimibles y videos pedagógicos de apoyo del canal y cuadernillos de la
Profa Kempis para 6° de Primaria (Fase 5), alineados con la Nueva Escuela Mexicana (NEM):

Temas Semana 6:
- Lenguajes: Textos literarios, estructura del cuento (planteamiento, nudo, desenlace, tipos de narrador, personajes y escenarios).
- Saberes y Pensamiento Científico: Alimentos procesados y ultraprocesados, grasas (semáforo de grasas saturadas, trans e insaturadas), sellos en los alimentos (NOM-051: exceso de calorías, azúcares, grasas y sodio), múltiplos y submúltiplos del gramo (conversiones mediante método de la escalera).
- Ética, Naturaleza y Sociedades: Servicios públicos y bienestar comunitario, impuestos (origen y destino social), el IVA (Impuesto al Valor Agregado del 16% en México).
- De lo Humano y lo Comunitario: Resolución pacífica de conflictos (negociación, mediación, conciliación y arbitraje), convivencia escolar sana y pacífica.
- Efeméride: 12 de Octubre - Descubrimiento de América y Encuentro de Dos Mundos (análisis crítico e intercultural).

Temas Semana 7:
- Lenguajes: Lectura dramatizada, guiones teatrales, acotaciones, diálogos, entonación, modulación de voz y expresión corporal.
- Saberes y Pensamiento Científico: El Plato del Bien Comer (versión oficial actualizada: grupos de alimentos, porciones y balance), Jarra del Buen Beber, relación entre masa en gramos y porciones diarias.
- Ética, Naturaleza y Sociedades: Calidad de vida y sus dimensiones (salud, educación, vivienda digna, medio ambiente sano y recreación), desigualdades sociales en el entorno local (Durango).
- De lo Humano y lo Comunitario: Hábitos de vida saludable, actividad física cotidiana, alimentación balanceada en la comunidad escolar.
- Efeméride: 16 de Octubre - Día Mundial de la Alimentación (lema de la FAO, derecho humano a la alimentación adecuada y combate al desperdicio de comida).
"""

from typing import Dict, List, Any, Optional

CUADERNILLO_KEMPIS_DATA: Dict[int, Dict[str, Any]] = {
    6: {
        "semana": 6,
        "titulo_general": "Cuadernillo de Actividades Didácticas — Semana 6 (Profa Kempis)",
        "periodo_sugerido": "Semana 6 de 37 (Octubre - Ciclo 2026-2027)",
        "descripcion": "Recursos didácticos, anexos imprimibles y videos explicativos para el desarrollo de proyectos en Lenguajes, Ciencias, Formación Ética y Convivencia.",
        "efemeride_principal": {
            "nombre": "Descubrimiento de América y Encuentro de Dos Mundos (12 de Octubre)",
            "fecha": "12 de Octubre",
            "video_titulo": "12 de octubre: Descubrimiento de América — Profa Kempis",
            "video_url": "https://www.youtube.com/watch?v=0kFvFz4g_5Y",
            "anexo_nombre": "Anexo 6.5: Línea del tiempo y análisis crítico del 12 de Octubre",
            "actividad": "Elaborar una línea del tiempo ilustrada sobre los viajes de Cristóbal Colón (La Niña, La Pinta y La Santa María) y reflexionar en asamblea sobre el intercambio cultural y el respeto a la diversidad de los pueblos originarios."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Textos literarios: El cuento y sus partes (planteamiento, nudo, desenlace y tipos de narrador)",
                "pda_vinculado": "Lee y analiza textos literarios e identifica la estructura de la narración, las relaciones de causalidad y temporalidad, y describe personajes y escenarios.",
                "video_titulo": "Los textos literarios y el cuento — Profa Kempis",
                "video_url": "https://www.youtube.com/watch?v=0kFvFz4g_5Y",
                "inicio": "Presentar una caja sorpresa con títulos de cuentos clásicos y contemporáneos. Recuperar saberes previos: ¿Qué distingue a un cuento de una noticia o un texto informativo?",
                "desarrollo": "Lectura guiada del cuento seleccionado. En equipos, completar el organizador gráfico del Anexo 6.1 clasificando inicio/planteamiento, nudo/conflicto y desenlace, identificando adjetivos calificativos y nexos temporales.",
                "cierre": "Puesta en común en plenaria. Los alumnos comparten el esquema de su cuento y argumentan qué cambio le harían al final de la historia.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 6.1: Estructura del Cuento), libro Múltiples Lenguajes (6° grado) y libreta.",
                "anexo_nombre": "Anexo 6.1: Organizador Gráfico de Textos Literarios y Partes del Cuento",
                "anexo_descripcion": "Ficha imprimible para esquematizar inicio, nudo, desenlace, caracterización de personajes principales/secundarios y tipo de narrador (primera o tercera persona)."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Alimentos procesados, grasas, sellos de advertencia (NOM-051) y múltiplos y submúltiplos del gramo",
                "pda_vinculado": "Analiza etiquetas de alimentos empaquetados e interpreta sellos de advertencia; resuelve situaciones problemáticas que implican conversiones con múltiplos y submúltiplos del gramo.",
                "video_titulo": "Alimentos procesados, sellos de advertencia y múltiplos del gramo — Profa Kempis",
                "video_url": "https://www.youtube.com/watch?v=0kFvFz4g_5Y",
                "inicio": "Exhibir 4 empaques reales de alimentos ultraprocesados (galletas, refresco, papas fritas). Preguntar: ¿Qué significan los octágonos negros en el empaque y por qué indican 'Exceso de grasas saturadas' o 'Exceso de calorías'?",
                "desarrollo": "Observar el video explicativo de la Profa Kempis sobre sellos y grasas. En binas, analizar las tablas nutrimentales de los empaques traídos de casa. Registrar la cantidad de grasas y azúcares en gramos. Aplicar la tabla de conversión del Anexo 6.2 (método de la escalera) para convertir gramos (g) a miligramos (mg), kilogramos (kg) y decagramos (dag).",
                "cierre": "Construir en el pizarrón el 'Semáforo de las Grasas' (saludables vs. no saludables/trans) y reflexionar sobre el impacto del consumo excesivo en la salud familiar.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 6.2: Múltiplos y Submúltiplos del Gramo y Sellos NOM-051), empaques vacíos y báscula del aula.",
                "anexo_nombre": "Anexo 6.2: Laboratorio de Etiquetas y Conversión de Múltiplos del Gramo",
                "anexo_descripcion": "Ficha práctica de conversión de unidades de masa (kg, hg, dag, g, dg, cg, mg) con problemas de aplicación en empaques comerciales y tabla de semaforización de sellos."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Servicios públicos, recaudación de impuestos y cálculo del IVA (16%)",
                "pda_vinculado": "Comprende la función de los servicios públicos en la satisfacción de necesidades colectivas, la responsabilidad ciudadana en el pago de impuestos y el cálculo de porcentajes aplicados al IVA.",
                "video_titulo": "Los servicios públicos y los impuestos (¿Qué es el IVA?) — Profa Kempis",
                "video_url": "https://www.youtube.com/watch?v=0kFvFz4g_5Y",
                "inicio": "Lluvia de ideas guiada: ¿De dónde proviene el agua de nuestras llaves, la luz de las calles y quién limpia los parques públicos en Durango? ¿Quién paga esos servicios?",
                "desarrollo": "Proyectar el video de Profa Kempis sobre impuestos e IVA. Explicar el concepto del Impuesto al Valor Agregado (16%). En equipos cooperativos, resolver los ejercicios del Anexo 6.3: analizar tickets de compra simulados, desglosar el subtotal, calcular el 16% de IVA y el total a pagar.",
                "cierre": "Debate reflexivo: '¿Por qué pagar impuestos es un acto de corresponsabilidad ética y ciudadana para tener mejores escuelas y hospitales?'. Elaborar un decálogo de compromisos cívicos.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 6.3: Servicios Públicos, Impuestos y Cálculo del IVA), tickets simulados de compra.",
                "anexo_nombre": "Anexo 6.3: Ficha de Servicios Públicos y Práctica Financiera del IVA",
                "anexo_descripcion": "Actividad de vinculación comunitaria: mapa de servicios públicos de la colonia y ejercicios matemáticos de cálculo y desglose del 16% de IVA en compras cotidianas."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Resolución pacífica de conflictos y convivencia escolar sana y pacífica",
                "pda_vinculado": "Aplica estrategias de mediación, negociación y diálogo reflexivo para resolver desacuerdos en el aula y promover una cultura de paz.",
                "video_titulo": "Resolución pacífica de conflictos en la escuela — Profa Kempis",
                "video_url": "https://www.youtube.com/watch?v=0kFvFz4g_5Y",
                "inicio": "Dinámica kinestésica 'El nudo humano': los 26 alumnos se toman de las manos entrelazadas y deben desatarse sin soltarse utilizando únicamente la comunicación pacífica.",
                "desarrollo": "Analizar en parejas los casos hipotéticos de conflicto del Anexo 6.4 (disputa de cancha deportiva, burla por error en lectura, desacuerdo en equipo). Identificar las 4 vías de solución pacífica: negociación, mediación, conciliación y arbitraje.",
                "cierre": "Dramatización breve de los casos con mediación dialógica. Firma colectiva del 'Pacto de Convivencia Sana y Pacífica de 6° A'.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 6.4: Casos Prácticos de Mediación y Convivencia Escolar).",
                "anexo_nombre": "Anexo 6.4: Taller de Mediación Escolar y Acuerdos de Paz",
                "anexo_descripcion": "Tarjetas de casos prácticos para dramatización y rúbrica de resolución dialógica de conflictos sin violencia."
            }
        },
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. literatura (palabra esdrújula)",
                "2. ultraprocesados (grafía s/z y prefijo)",
                "3. miligramo (submúltiplo del gramo)",
                "4. contribución (terminación -ción)",
                "5. conciliación (reglas ortográficas c/s)"
            ],
            "calculo_mental": [
                "1. ¿Cuántos gramos hay en 3.5 kilogramos? (3,500 g)",
                "2. Si 100 g de cereal tienen 12 g de azúcar, ¿cuántos gramos de azúcar hay en 500 g? (60 g)",
                "3. El 10% de $200 es... y el 16% es... ($20 y $32)",
                "4. Convierte 450 miligramos a gramos (0.45 g)",
                "5. Un producto cuesta $100 más IVA del 16%, ¿cuánto se paga en total? ($116)"
            ],
            "problemas_razonados": [
                "Problema 1: En la cooperativa escolar se venden paquetes de galletas de 250 g. Si la caja contiene 12 paquetes, ¿cuántos kilogramos de galletas hay en total?",
                "Problema 2: Don Pedro compró material escolar por un subtotal de $450 pesos. Si la tasa del IVA es del 16%, ¿cuánto dinero pagó exclusivamente de impuestos y cuál fue el costo total de la compra?"
            ]
        }
    },
    7: {
        "semana": 7,
        "titulo_general": "Cuadernillo de Actividades Didácticas — Semana 7 (Profa Kempis)",
        "periodo_sugerido": "Semana 7 de 37 (Octubre - Ciclo 2026-2027)",
        "descripcion": "Especialización en lectura dramatizada, Plato del Bien Comer actualizado, calidad de vida comunitaria y conmemoración del Día Mundial de la Alimentación.",
        "efemeride_principal": {
            "nombre": "Día Mundial de la Alimentación (16 de Octubre)",
            "fecha": "16 de Octubre",
            "video_titulo": "16 de octubre: Día Mundial de la Alimentación — Profa Kempis",
            "video_url": "https://www.youtube.com/watch?v=0kFvFz4g_5Y",
            "anexo_nombre": "Anexo 7.5: Campaña 'Cero Desperdicio de Alimentos' y Decálogo Saludable",
            "actividad": "Elaborar un tríptico o cartel comunitario sobre el derecho humano a la alimentación adecuada, los riesgos del desperdicio de comida y propuestas prácticas para aprovechar sobras nutritivas en el hogar."
        },
        "campos": {
            "Lenguajes": {
                "tema": "La lectura dramatizada y el guión teatral (acotaciones, parlamentos y modulación)",
                "pda_vinculado": "Interpreta y representa lecturas dramatizadas empleando adecuadamente acotaciones, volumen, tono y modulación de la voz.",
                "video_titulo": "La lectura dramatizada y el guión de teatro — Profa Kempis",
                "video_url": "https://www.youtube.com/watch?v=0kFvFz4g_5Y",
                "inicio": "Juego de modulación de voz: leer la misma frase ('¡Ya llegaron los libros!') con distintas emociones (alegría, miedo, misterio, enojo). Analizar la importancia de las acotaciones teatrales.",
                "desarrollo": "Revisar el video de Profa Kempis sobre lectura dramatizada. En equipos de 4 alumnos, leer el guión breve del Anexo 7.1. Identificar personajes, parlamentos y acotaciones entre paréntesis. Distribuir roles y ensayar la entonación y lenguaje no verbal.",
                "cierre": "Representación en atril o escenario del aula frente al grupo. Los compañeros evalúan con una lista de cotejo la dicción, volumen y expresividad.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 7.1: Guión Teatral y Ficha de Acotaciones), atril o espacio de aula.",
                "anexo_nombre": "Anexo 7.1: Guión Teatral Didáctico y Rúbrica de Lectura Dramatizada",
                "anexo_descripcion": "Texto dramático adaptado para educación primaria con acotaciones visuales y guía de modulación expresiva de la voz."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "El Plato del Bien Comer actualizado, la Jarra del Buen Beber y balance calórico",
                "pda_vinculado": "Diseña menús basados en el Plato del Bien Comer y la Jarra del Buen Beber, relacionando la masa en gramos de las porciones con los requerimientos energéticos saludables.",
                "video_titulo": "El Plato del Bien Comer actualizado y la Jarra del Buen Beber — Profa Kempis",
                "video_url": "https://www.youtube.com/watch?v=0kFvFz4g_5Y",
                "inicio": "Presentar una silueta del nuevo Plato del Bien Comer. Preguntar: ¿Cuáles son los 3 grupos principales y por qué las verduras y frutas deben ocupar la mitad del plato?",
                "desarrollo": "Ver el video explicativo de Profa Kempis. Utilizando el Anexo 7.2, los alumnos recortan y clasifican alimentos en: 1) Verduras y frutas, 2) Granos y cereales, 3) Leguminosas y alimentos de origen animal. Calcular la masa aproximada en gramos de cada porción para un almuerzo escolar balanceado.",
                "cierre": "Exposición de los menús saludables creados por los alumnos. Diseñar el compromiso personal de hidratación: tomar de 6 a 8 vasos de agua simple potable al día.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 7.2: Plato del Bien Comer recortable y registro de gramos), tijeras, pegamento y colores.",
                "anexo_nombre": "Anexo 7.2: Taller Interactivo del Plato del Bien Comer y Menú Semanal",
                "anexo_descripcion": "Esquema interactivo a color para recortar y armar porciones nutricionales en gramos y niveles de hidratación de la Jarra del Buen Beber."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Calidad de vida: Factores determinantes, justicia social y desigualdades en la comunidad",
                "pda_vinculado": "Analiza los factores que influyen en la calidad de vida de las familias en su comunidad y entidad (Durango), reconociendo brechas de equidad y propuestas de mejora.",
                "video_titulo": "¿Qué es la calidad de vida y cómo se mide? — Profa Kempis",
                "video_url": "https://www.youtube.com/watch?v=0kFvFz4g_5Y",
                "inicio": "¿Qué necesita una familia para vivir bien? Lluvia de respuestas: salud, casa, trabajo, seguridad, áreas verdes, agua potable.",
                "desarrollo": "Analizar la infografía del Anexo 7.3 sobre las dimensiones de la calidad de vida (ambiental, económica, educativa, salud y recreativa). En equipos, responder una encuesta diagnóstica sobre las fortalezas y carencias de su colonia en Durango.",
                "cierre": "Construir en una cartulina el 'Mural Comunitario de la Calidad de Vida' con propuestas ciudadanas para mejorar los espacios públicos de su entorno.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 7.3: Encuesta y Dimensiones de la Calidad de Vida), plumones y cartulinas.",
                "anexo_nombre": "Anexo 7.3: Diagnóstico Comunitario de Indicadores de Calidad de Vida",
                "anexo_descripcion": "Instrumento de indagación comunitaria para evaluar acceso a servicios, salud y medio ambiente en el entorno escolar."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Estilos de vida activos, prevención de enfermedades crónicas y bienestar compartido",
                "pda_vinculado": "Organiza y participa en circuitos motrices y dinámicas de actividad física para valorar el impacto del ejercicio continuo en el bienestar integral.",
                "video_titulo": "Hábitos de vida saludable y actividad física — Profa Kempis",
                "video_url": "https://www.youtube.com/watch?v=0kFvFz4g_5Y",
                "inicio": "Toma de pulso cardíaco en reposo. Breve calentamiento motriz en el aula para activar la oxigenación cerebral y el entusiasmo kinestésico.",
                "desarrollo": "En el patio cívico, organizar 4 estaciones del circuito saludable del Anexo 7.4: 1) Salto de cuerda, 2) Desplazamiento en zigzag, 3) Lanzamiento y recepción, 4) Ejercicios de equilibrio y estiramiento. Tomar el pulso después de la actividad.",
                "cierre": "Reflexión en asamblea sobre la importancia de combinar al menos 60 minutos diarios de juego activo con la alimentación balanceada.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 7.4: Circuito Motriz y Bitácora de Salud), cuerdas, aros y conos.",
                "anexo_nombre": "Anexo 7.4: Bitácora del Circuito de Actividad Física y Bienestar Integral",
                "anexo_descripcion": "Registro diario de minutos de actividad física, horas de sueño y consumo de agua simple para los alumnos de 6° grado."
            }
        },
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. acotación (terminación con c)",
                "2. dramatización (reglas ortográficas)",
                "3. hidratación (h inicial y -ción)",
                "4. bienestar (palabra compuesta)",
                "5. leguminosas (grafía s)"
            ],
            "calculo_mental": [
                "1. Si 1 vaso de agua equivale a 250 ml, ¿cuántos mililitros son 8 vasos? (2,000 ml = 2 litros)",
                "2. Un plato balanceado contiene 150 g de verduras, 80 g de arroz y 120 g de pollo. ¿Cuál es el peso total? (350 g)",
                "3. De 60 minutos de recreo activo, Juan corrió el 50% del tiempo. ¿Cuántos minutos corrió? (30 minutos)",
                "4. ¿Cuánto le falta a 1,450 g para completar 2 kg? (550 g)",
                "5. Si un paquete de legumbres de 1 kg cuesta $36 pesos, ¿cuánto cuesta 1/2 kg? ($18 pesos)"
            ],
            "problemas_razonados": [
                "Problema 1: En la tiendita escolar de la Primaria Revolución Social de 1910, un menú saludable cuesta $35 pesos. Si el grupo de 6° 'A' tiene 26 alumnos y todos adquieren el paquete nutritivo, ¿cuánto se recauda en total y cuántos gramos de fruta consumen si cada porción tiene 125 g?",
                "Problema 2: En la campaña del Día Mundial de la Alimentación, los alumnos recolectaron 15 bolsas de frijol de 1 kg cada una y 8 bolsas de lenteja de 500 g cada una. ¿Cuántos kilogramos y gramos de granos saludables reunieron en total?"
            ]
        }
    }
}

# Palabras clave para la detección automática de relevancia
PALABRAS_CLAVE_KEMPIS = [
    "texto literario", "textos literarios", "cuento", "cuentos", "lectura dramatizada",
    "guion teatral", "guión teatral", "acotaciones", "alimento procesado", "alimentos procesados",
    "ultraprocesados", "grasas", "grasa saturada", "sellos en los alimentos", "sellos de advertencia",
    "nom-051", "gramo", "gramos", "múltiplos del gramo", "submúltiplos del gramo", "plato del bien comer",
    "jarra del buen beber", "servicios públicos", "servicios publicos", "impuesto", "impuestos",
    "iva", "calidad de vida", "resolución pacífica", "resolucion pacifica", "convivencia sana",
    "cultura de paz", "12 de octubre", "descubrimiento de américa", "descubrimiento de america",
    "16 de octubre", "día mundial de la alimentación", "dia mundial de la alimentacion", "profa kempis"
]


def detectar_relevancia_kempis(
    semana: Optional[int] = None,
    contenidos_pda: Optional[List[Dict[str, Any]]] = None,
    directrices_o_texto: str = "",
    campos: Optional[List[str]] = None
) -> bool:
    """
    Determina si los recursos del Cuadernillo Profa Kempis son pertinentes
    según el número de semana (6 o 7) o los contenidos temáticos detectados.
    """
    try:
        if semana in [6, 7]:
            return True
        if isinstance(semana, str) and semana.strip() in ["6", "7", "Semana 6", "Semana 7"]:
            return True
    except Exception:
        pass

    # Inspección de texto y palabras clave
    corpus_busqueda = (directrices_o_texto or "").lower()
    if contenidos_pda:
        for item in contenidos_pda:
            corpus_busqueda += " " + str(item.get("contenido", "")).lower()
            corpus_busqueda += " " + str(item.get("pda", "")).lower()
            corpus_busqueda += " " + str(item.get("campo", "")).lower()

    for kw in PALABRAS_CLAVE_KEMPIS:
        if kw in corpus_busqueda:
            return True

    return False


def obtener_recursos_kempis_por_semana(semana: int) -> Optional[Dict[str, Any]]:
    """Devuelve los metadatos completos del cuadernillo para la semana solicitada (6 o 7)."""
    return CUADERNILLO_KEMPIS_DATA.get(int(semana)) if semana in [6, 7] else None


def formatear_kempis_para_prompt(semana: int, campos_formativos: Optional[List[str]] = None) -> str:
    """
    Genera un bloque de texto estructurado para inyectar como directriz obligatoria
    en el prompt de Gemini, garantizando que la IA vincule e integre las actividades,
    anexos y videos de Profa Kempis en Inicio, Desarrollo y Cierre.
    """
    if semana not in [6, 7]:
        semana = 6  # Fallback a Semana 6 si no es 6 ni 7

    data = CUADERNILLO_KEMPIS_DATA[semana]
    campos = campos_formativos or ["Lenguajes", "Saberes y Pensamiento Científico", "Ética, Naturaleza y Sociedades", "De lo Humano y lo Comunitario"]

    lineas = [
        f"=== RECURSO DIDÁCTICO INTEGRADO: CUADERNILLO DE ACTIVIDADES PROFA KEMPIS (SEMANA {semana}) ===",
        f"La planeación DEBE incorporar, sugerir y citar expresamente los contenidos del Cuadernillo de la Profa Kempis para la Semana {semana}:",
        f"- Título del recurso: {data['titulo_general']}",
        f"- Efeméride vinculada: {data['efemeride_principal']['nombre']} -> {data['efemeride_principal']['actividad']}",
        f"  * Video de apoyo Profa Kempis: '{data['efemeride_principal']['video_titulo']}' ({data['efemeride_principal']['video_url']})",
        "",
        "DIRECTRICES DE INCORPORACIÓN EN LAS SECUENCIAS DIDÁCTICAS (INICIO, DESARROLLO Y CIERRE):"
    ]

    for cf in campos:
        if cf in data["campos"]:
            c_info = data["campos"][cf]
            lineas.append(f"• Campo Formativo: {cf}")
            lineas.append(f"  - Tema Central: {c_info['tema']}")
            lineas.append(f"  - PDA Vinculado: {c_info['pda_vinculado']}")
            lineas.append(f"  - Actividad de Inicio sugerida: {c_info['inicio']}")
            lineas.append(f"  - Actividad de Desarrollo kinestésica/visual: {c_info['desarrollo']}")
            lineas.append(f"  - Actividad de Cierre y evaluación: {c_info['cierre']}")
            lineas.append(f"  - Anexo Imprimible del Cuadernillo: {c_info['anexo_nombre']} ({c_info['anexo_descripcion']})")
            lineas.append(f"  - Video de apoyo Profa Kempis: '{c_info['video_titulo']}' ({c_info['video_url']})")
            lineas.append("")

    lineas.append("RUTINAS MATUTINAS SUGERIDAS DEL CUADERNILLO:")
    lineas.append(f"- Dictado Ortográfico: {', '.join(data['rutinas_matutinas_sugeridas']['dictado'][:3])}")
    lineas.append(f"- Cálculo Mental: {', '.join(data['rutinas_matutinas_sugeridas']['calculo_mental'][:2])}")
    lineas.append(f"- Problema Razonado: {data['rutinas_matutinas_sugeridas']['problemas_razonados'][0]}")
    lineas.append("")
    lineas.append("REGLA MANDATORIA DE CITA: En la columna de 'Recursos didácticos y materiales' de cada sesión, cita obligatoriamente: 'Cuadernillo Profa Kempis (Semana X - Anexo Y) y video de apoyo en YouTube'.")
    lineas.append("================================================================================")

    return "\n".join(lineas)


def obtener_anexos_kempis_para_docx(semana: int) -> List[Dict[str, Any]]:
    """
    Retorna la lista de anexos imprimibles y fichas de trabajo
    del Cuadernillo de la Profa Kempis para incrustar en el documento Word (.docx).
    """
    if semana not in [6, 7]:
        return []

    data = CUADERNILLO_KEMPIS_DATA[semana]
    anexos = []

    for campo_nom, c_data in data["campos"].items():
        anexos.append({
            "campo": campo_nom,
            "nombre": c_data["anexo_nombre"],
            "descripcion": c_data["anexo_descripcion"],
            "tema": c_data["tema"],
            "video_titulo": c_data["video_titulo"],
            "video_url": c_data["video_url"],
            "actividad": c_data["desarrollo"]
        })

    # Agregar la efeméride como anexo especial
    ef = data["efemeride_principal"]
    anexos.append({
        "campo": "Conmemoración Cívica e Histórica",
        "nombre": ef["anexo_nombre"],
        "descripcion": f"Ficha de trabajo para el análisis reflexivo y contextualizado del {ef['nombre']}.",
        "tema": ef["nombre"],
        "video_titulo": ef["video_titulo"],
        "video_url": ef["video_url"],
        "actividad": ef["actividad"]
    })

    return anexos
