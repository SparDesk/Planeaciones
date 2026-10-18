"""
Planeaciones Escolares Educación Primaria
Aplicación web interactiva profesional para la generación automatizada de
Planeaciones Escolares de Primaria basadas en el modelo de la Nueva Escuela Mexicana (NEM - SEP).
"""

import os
import json
import streamlit as st
import streamlit_authenticator as stauth
from dotenv import load_dotenv
from planeaciones_storage import (
    init_db,
    guardar_planeacion,
    guardar_planeacion_con_nombre,
    guardar_planeacion_nombre_ruta,
    cargar_planeacion,
    listar_planeaciones,
    listar_archivos_guardados,
    obtener_planeacion_por_id,
    obtener_planeacion_por_nombre,
    eliminar_planeacion_por_id,
    eliminar_planeacion,
    obtener_resumen_semanas_cubiertas,
    calcular_hash_planeacion,
    CATEGORIAS_RUTAS_DEFAULT,
    CATEGORIAS_RUTAS,
    sanitizar_nombre_ruta,
    guardar_archivo_fisico_json
)
from cuadernillo_kempis import (
    CUADERNILLO_KEMPIS_DATA,
    CATALOGO_PROYECTOS_SEP_37_SEMANAS,
    detectar_relevancia_kempis,
    obtener_recursos_kempis_por_semana,
    obtener_proyecto_semana,
    obtener_anexos_por_semana_y_dia,
    formatear_kempis_para_prompt,
    obtener_anexos_kempis_para_docx
)


# Cargar variables de entorno desde .env si existe
load_dotenv()

# Inicializar almacenamiento local SQLite para persistencia y autoguardado
init_db()

# ==========================================
# CATÁLOGOS CURRICULARES NEM Y DICCIONARIO DE RESPALDO (FALLBACK)
# ==========================================
DATOS_PREDETERMINADOS = {
    "nombre_escuela": "Escuela Primaria “Revolución Social de 1910”",
    "cct": "10EPR0361N",
    "zona_escolar": "Zona 49",
    "sector": "Sector 02",
    "entidad": "Durango",
    "docente": "Maestra Aday Domínguez Domínguez",
    "director": "Guillermo Gerardo Borjas Díaz",
    "grado": "6° de Primaria",
    "fase": "Fase 5",
    "grupo": "A",
    "matricula": 26,
    "estilos_aprendizaje": "Kinestésico y Visual",
    "periodo": "Semana 1 a 37 SEP (Oficial Ciclo 2026-2027)",
    "ciclo_escolar": "2026-2027",
    "turno": "Matutino"
}

CAMPOS_FORMATIVOS = [
    "Lenguajes",
    "Saberes y Pensamiento Científico",
    "Ética, Naturaleza y Sociedades",
    "De lo Humano y lo Comunitario"
]

METODOLOGIAS_SOCIOCRITICAS = {
    "Aprendizaje Basado en Proyectos Comunitarios": {
        "descripcion": "Recomendada especialmente para el campo formativo de Lenguajes y proyectos interdisciplinarios vinculados al aula, la escuela o la comunidad.",
        "fases_oficiales": [
            "Fase 1. Planeación: Momento 1 (Identificación), Momento 2 (Recuperación de saberes), Momento 3 (Planificación).",
            "Fase 2. Acción: Momento 4 (Acercamiento), Momento 5 (Comprensión y producción), Momento 6 (Reconocimiento), Momento 7 (Concreción).",
            "Fase 3. Intervención: Momento 8 (Integración), Momento 9 (Difusión), Momento 10 (Consideraciones / Evaluación formativa), Momento 11 (Avances)."
        ]
    },
    "Aprendizaje Basado en Indagación (STEAM como enfoque)": {
        "descripcion": "Metodología orientada al campo de Saberes y Pensamiento Científico que vincula ciencia, tecnología, ingeniería, artes y matemáticas.",
        "fases_oficiales": [
            "Fase 1: Introducción al tema, uso de conocimientos previos y planteamiento de la pregunta de indagación.",
            "Fase 2: Diseño de la investigación y desarrollo de la indagación.",
            "Fase 3: Organización y estructuración de respuestas a las preguntas de indagación (análisis de datos y evidencias).",
            "Fase 4: Presentación de los resultados de indagación y aplicación en un contexto real.",
            "Fase 5: Metacognición y reflexión sobre lo aprendido y el proceso seguido."
        ]
    },
    "Aprendizaje Basado en Problemas (ABPr)": {
        "descripcion": "Metodología ideal para el campo de Ética, Naturaleza y Sociedades, orientada a la resolución y reflexión profunda de dilemas y problemáticas reales.",
        "fases_oficiales": [
            "Momento 1. Presentemos (Planteamiento inicial del escenario o problema).",
            "Momento 2. Recolectemos (Recuperación y exploración de conocimientos previos).",
            "Momento 3. Formulemos el problema (Definición clara y acotada de la situación a transformar).",
            "Momento 4. Organicemos la experiencia (Ruta de trabajo, roles, acuerdos y tareas).",
            "Momento 5. Vivamos la experiencia (Indagación activa, experimentación y búsqueda de soluciones).",
            "Momento 6. Resultados y análisis (Reflexión crítica, metacognición y evaluación)."
        ]
    },
    "Aprendizaje Servicio (AS)": {
        "descripcion": "Metodología idónea para De lo Humano y lo Comunitario, integrando el aprendizaje curricular con el servicio solidario a la comunidad.",
        "fases_oficiales": [
            "Etapa 1. Punto de partida (Sensibilización e identificación de necesidades comunitarias).",
            "Etapa 2. Lo que sé y lo que quiero saber (Diagnóstico participativo e indagación).",
            "Etapa 3. Organicemos las actividades (Planificación del servicio y recursos).",
            "Etapa 4. Creatividad en marcha (Ejecución de las acciones de servicio colaborativo).",
            "Etapa 5. Compartimos y evaluamos lo aprendido (Rendición de cuentas, impacto social y evaluación formativa)."
        ]
    }
}

EJES_ARTICULADORES = [
    "Inclusión",
    "Pensamiento crítico",
    "Interculturalidad crítica",
    "Igualdad de género",
    "Vida saludable",
    "Apropiación de las culturas a través de la lectura y la escritura",
    "Artes y experiencias estéticas"
]

# Diccionario de respaldo interno (fallback) en caso de caída o desconexión con CONALITEG
LIBROS_SEP_POR_GRADO = {
    "1° de Primaria": [
        "Proyectos de Aula (1° grado)",
        "Proyectos Escolares (1° grado)",
        "Proyectos Comunitarios (1° grado)",
        "Nuestros Saberes: Libro para alumnos, maestros y familia (1° grado)",
        "Múltiples lenguajes (1° grado)",
        "Múltiples lenguajes: Trazos y palabras (1° grado)"
    ],
    "2° de Primaria": [
        "Proyectos de Aula (2° grado)",
        "Proyectos Escolares (2° grado)",
        "Proyectos Comunitarios (2° grado)",
        "Nuestros Saberes: Libro para alumnos, maestros y familia (2° grado)",
        "Múltiples lenguajes (2° grado)"
    ],
    "3° de Primaria": [
        "Proyectos de Aula (3° grado)",
        "Proyectos Escolares (3° grado)",
        "Proyectos Comunitarios (3° grado)",
        "Nuestros Saberes: Libro para alumnos, maestros y familia (3° grado)",
        "Múltiples lenguajes (3° grado)"
    ],
    "4° de Primaria": [
        "Proyectos de Aula (4° grado)",
        "Proyectos Escolares (4° grado)",
        "Proyectos Comunitarios (4° grado)",
        "Nuestros Saberes: Libro para alumnos, maestros y familia (4° grado)",
        "Múltiples lenguajes (4° grado)",
        "Cartografía de México y el mundo (Fases 4 y 5)"
    ],
    "5° de Primaria": [
        "Proyectos de Aula (5° grado)",
        "Proyectos Escolares (5° grado)",
        "Proyectos Comunitarios (5° grado)",
        "Nuestros Saberes: Libro para alumnos, maestros y familia (5° grado)",
        "Múltiples lenguajes (5° grado)",
        "Cartografía de México y el mundo (5° grado)"
    ],
    "6° de Primaria": [
        "Proyectos de Aula (6° grado)",
        "Proyectos Escolares (6° grado)",
        "Proyectos Comunitarios (6° grado)",
        "Nuestros Saberes: Libro para alumnos, maestros y familia (6° grado)",
        "Múltiples lenguajes (6° grado)",
        "Cartografía de México y el mundo (6° grado)"
    ]
}

LIBROS_SEP_RECOMENDADOS = LIBROS_SEP_POR_GRADO["6° de Primaria"]

GUIAS_CTE_CATALOGO = {
    "Orientaciones CTE - 1ª Sesión Ordinaria (Septiembre 2026 - Fase 5)": {
        "enfoque": "Diagnóstico socioeducativo inicial e identificación de barreras de aprendizaje.",
        "directrices": "Fortalecer habilidades fundamentales en lectoescritura, cálculo mental reflexivo y resolución de problemas matemáticos contextualizados."
    },
    "Orientaciones CTE - 2ª Sesión Ordinaria (Octubre 2026 - Fase 5)": {
        "enfoque": "Ejes articuladores y Diseño Universal para el Aprendizaje (DUA).",
        "directrices": "Garantizar la inclusión, el pensamiento crítico y la igualdad de género en todas las secuencias didácticas planeadas."
    },
    "Orientaciones CTE - 3ª Sesión Ordinaria (Noviembre 2026 - Fase 5)": {
        "enfoque": "Compromiso con la comunidad y metodologías sociocríticas activas.",
        "directrices": "Desarrollar proyectos interdisciplinarios que trasciendan el salón de clases y vinculen a las familias y el entorno local."
    },
    "Orientaciones CTE - 4ª Sesión Ordinaria (Enero 2027 - Fase 5)": {
        "enfoque": "Articulación curricular y codiseño del Plan Analítico en la Fase 5.",
        "directrices": "Vincular problemáticas del contexto escolar (alimentación, comprensión lectora, convivencia) con los contenidos sintéticos y PDA integrados."
    },
    "Orientaciones CTE - 5ª Sesión Ordinaria (Febrero 2027 - Fase 5)": {
        "enfoque": "Evaluación formativa, retroalimentación dialógica y análisis de los avances en proyectos comunitarios.",
        "directrices": "Priorizar la evaluación como un proceso continuo y no punitivo; promover la autorreflexión de los alumnos y la coevaluación en asambleas de aula. Atender BAP mediante ajustes razonables en lectura y razonamiento lógico."
    },
    "Orientaciones CTE - 6ª Sesión Ordinaria (Marzo 2027 - Fase 5)": {
        "enfoque": "Avances en la comprensión lectora, fluidez y pensamiento matemático.",
        "directrices": "Evaluar el impacto de las estrategias didácticas implementadas y reajustar actividades de apoyo para alumnos que requieren mayor acompañamiento."
    },
    "Orientaciones CTE - 7ª Sesión Ordinaria (Mayo 2027 - Fase 5)": {
        "enfoque": "Consolidación de proyectos escolares e integración de los 4 Campos Formativos.",
        "directrices": "Fortalecer la vinculación comunitaria, el diálogo reflexivo y la socialización de productos de aprendizaje en la escuela."
    },
    "Orientaciones CTE - 8ª Sesión Ordinaria (Junio 2027 - Fase 5)": {
        "enfoque": "Evaluación final del ciclo escolar, balance de proyectos comunitarios y rendición de cuentas pedagógicas.",
        "directrices": "Sistematizar los logros del Programa Analítico 2026-2027 y proyectar acuerdos de mejora formativa para el siguiente ciclo escolar."
    },
    "Guía General de Consejo Técnico Escolar - Primaria (NEM)": {
        "enfoque": "Autonomía profesional del magisterio y transformación pedagógica.",
        "directrices": "Favorecer la integración curricular, la contextualización de contenidos y el trabajo colaborativo en comunidades de aprendizaje."
    }
}

# ==========================================
# DETERMINACIÓN AUTOMÁTICA DE FASE NEM Y BANCO CURRICULAR POR GRADO (1° A 6°)
# ==========================================
DICCIONARIO_FASES_NEM = {
    "1° de Primaria": "Fase 3",
    "2° de Primaria": "Fase 3",
    "3° de Primaria": "Fase 4",
    "4° de Primaria": "Fase 4",
    "5° de Primaria": "Fase 5",
    "6° de Primaria": "Fase 5"
}

def determinar_fase_nem(grado: str) -> str:
    """
    Determina automáticamente la Fase oficial de la Nueva Escuela Mexicana (NEM):
      * Fase 3: 1° y 2° de Primaria
      * Fase 4: 3° y 4° de Primaria
      * Fase 5: 5° y 6° de Primaria
    """
    g_str = str(grado)
    for g_key, f_val in DICCIONARIO_FASES_NEM.items():
        if g_key in g_str:
            return f_val
    if "1" in g_str or "2" in g_str:
        return "Fase 3"
    elif "3" in g_str or "4" in g_str:
        return "Fase 4"
    return "Fase 5"

CONTENIDOS_PDA_POR_GRADO = {
    "1° de Primaria": {
        "Lenguajes": [
            {
                "contenido": "Escritura colectiva por medio del dictado.",
                "pda": "Reconoce espacios, alineación y direccionalidad al escribir colectivamente; revisa y corrige el texto con ayuda del docente."
            },
            {
                "contenido": "Registro y resumen de información consultada en fuentes orales, escritas o audiovisuales.",
                "pda": "Registra sobre un tema de su interés por medio de la escritura, esquema, dibujo o fotografía y expone la información a sus compañeros."
            },
            {
                "contenido": "Narración de actividades y eventos relevantes que tengan lugar en la familia, la escuela o la comunidad.",
                "pda": "Relata historias relacionadas con actividades y eventos de su entorno, identificando orden cronológico y personajes."
            }
        ],
        "Saberes y Pensamiento Científico": [
            {
                "contenido": "Cuerpo humano: estructura externa, acciones para su cuidado y sus cambios como parte del crecimiento.",
                "pda": "Compara y representa las partes externas del cuerpo humano; propone acciones para su cuidado y hábitos de higiene."
            },
            {
                "contenido": "Beneficios del consumo de alimentos saludables, de agua simple potable y de la práctica de actividad física.",
                "pda": "Indaga, registra y compara el tipo y la frecuencia de consumo de alimentos saludables y agua potable en su familia y escuela."
            },
            {
                "contenido": "Estudio de los números.",
                "pda": "Expresa oralmente la sucesión numérica en su lengua materna hasta 100, de manera ascendente y descendente a partir de un número dado."
            }
        ],
        "Ética, Naturaleza y Sociedades": [
            {
                "contenido": "Diversidad natural y sociocultural en la comunidad.",
                "pda": "Reconoce que todas las personas son únicas, valiosas y tienen derecho a la identidad, a la familia y al cuidado digno."
            },
            {
                "contenido": "Construcción de la paz mediante el diálogo: situaciones de conflicto en el aula y la escuela.",
                "pda": "Analiza situaciones de conflicto en el aula y propone soluciones basadas en el diálogo, la escucha y el respeto mutuo."
            }
        ],
        "De lo Humano y lo Comunitario": [
            {
                "contenido": "La comunidad como el espacio en el que se vive y se encuentra la escuela.",
                "pda": "Ubica algunos referentes del lugar donde vive y se encuentra la escuela con apoyo de croquis sencillos."
            },
            {
                "contenido": "Formas de ser, pensar, actuar y relacionarse.",
                "pda": "Reconoce y comparte características que lo hacen una persona única, mostrando empatía hacia las diferencias de los demás."
            }
        ]
    },
    "2° de Primaria": {
        "Lenguajes": [
            {
                "contenido": "Descripción de objetos, lugares y seres vivos de su entorno natural y social.",
                "pda": "Describe de forma oral y escrita en su lengua materna objetos, personas, seres vivos y lugares conocidos, usando vocabulario preciso."
            },
            {
                "contenido": "Uso del dibujo y la escritura para recordar actividades y acuerdos escolares.",
                "pda": "Registra por escrito instrucciones breves para realizar tareas, elaborar materiales y recordar fechas y acuerdos escolares."
            },
            {
                "contenido": "Producción e interpretación de avisos, carteles, anuncios publicitarios y letreros.",
                "pda": "Reconoce características y funciones de anuncios publicitarios; elabora letreros y carteles para difundir eventos escolares."
            }
        ],
        "Saberes y Pensamiento Científico": [
            {
                "contenido": "Estructura y funcionamiento del cuerpo humano: sistemas locomotor y digestivo.",
                "pda": "Reconoce y describe los órganos de los sentidos y del sistema digestivo; explica su función y acciones para prevenir accidentes e infecciones."
            },
            {
                "contenido": "Construcción de la noción de suma y resta, y su relación como operaciones inversas.",
                "pda": "Utiliza y explica algoritmos convencionales de suma y resta con números naturales de hasta tres cifras en problemas cotidianos."
            },
            {
                "contenido": "Medición de longitud, masa y capacidad.",
                "pda": "Estima, mide, compara, ordena y registra longitudes, usando unidades arbitrarias y el metro como unidad de referencia."
            }
        ],
        "Ética, Naturaleza y Sociedades": [
            {
                "contenido": "Respeto, cuidado y empatía hacia la naturaleza como parte de un todo interdependiente.",
                "pda": "Dialoga sobre las relaciones de reciprocidad y pertenencia hacia la naturaleza, reconociendo la importancia de su preservación."
            },
            {
                "contenido": "Historia personal y familiar, diversidad de familias y el derecho a pertenecer a una.",
                "pda": "Indaga en fuentes orales y escritas sobre la historia de su familia y comunidad, reconociendo diversas formas de organización familiar."
            }
        ],
        "De lo Humano y lo Comunitario": [
            {
                "contenido": "Sentido de comunidad y satisfacción de necesidades humanas.",
                "pda": "Identifica las necesidades básicas de las personas de su comunidad y propone acciones colectivas solidarias para satisfacerlas."
            },
            {
                "contenido": "Acciones individuales que repercuten en la conservación y mejora de la salud.",
                "pda": "Reflexiona acerca de situaciones y comportamientos que ponen en riesgo la salud, promoviendo hábitos de vida saludable."
            }
        ]
    },
    "3° de Primaria": {
        "Lenguajes": [
            {
                "contenido": "Narración de sucesos del pasado y del presente.",
                "pda": "Identifica y comprende la función y las características principales de la narración; utiliza adverbios y nexos temporales."
            },
            {
                "contenido": "Comprensión y producción de textos instructivos para realizar actividades escolares y juegos.",
                "pda": "Identifica y reflexiona sobre la función de los textos instructivos y elabora reglamentos o instructivos usando verbos en infinitivo o imperativo."
            },
            {
                "contenido": "Exposición sobre temas diversos y uso de recursos gráficos.",
                "pda": "Reconoce características de la exposición; diseña cuadros sinópticos y esquemas para apoyar su presentación oral frente al grupo."
            }
        ],
        "Saberes y Pensamiento Científico": [
            {
                "contenido": "Estructura y funcionamiento del cuerpo humano: sistemas locomotor y respiratorio.",
                "pda": "Explica y representa la estructura y función del sistema locomotor (huesos, articulaciones y músculos) y su relación con el sistema respiratorio."
            },
            {
                "contenido": "Multiplicación y división, su relación como operaciones inversas.",
                "pda": "Construye y usa un repertorio multiplicativo para resolver problemas de cálculo mental y reparto con números de hasta tres cifras."
            },
            {
                "contenido": "Propiedades de los materiales: masa y longitud; relación entre estados físicos y temperatura.",
                "pda": "Describe la masa y la longitud como propiedades medibles de los materiales a través de instrumentos como la balanza y la regla."
            }
        ],
        "Ética, Naturaleza y Sociedades": [
            {
                "contenido": "Caracterización y localización del territorio donde vive, la entidad y México.",
                "pda": "Localiza y describe las características físicas y culturales de su municipio y entidad federativa, reconociendo su patrimonio cultural."
            },
            {
                "contenido": "La vida cotidiana antes de la primera invasión europea y en el México colonial.",
                "pda": "Indaga en fuentes primarias y secundarias sobre la vida de los pueblos originarios antes de la llegada de los españoles."
            }
        ],
        "De lo Humano y lo Comunitario": [
            {
                "contenido": "La escuela como espacio de convivencia, colaboración y aprendizaje.",
                "pda": "Participa en la organización del aula y de la escuela, promoviendo el trabajo colaborativo y la resolución pacífica de desacuerdos."
            },
            {
                "contenido": "Higiene para una vida saludable en la escuela y la comunidad.",
                "pda": "Reflexiona acerca de distintas prácticas de higiene personal y ambiental, proponiendo alternativas sustentables."
            }
        ]
    },
    "4° de Primaria": {
        "Lenguajes": [
            {
                "contenido": "Comprensión y producción de textos discontinuos para organizar y presentar información.",
                "pda": "Identifica las características y funciones de los textos discontinuos (gráficas, tablas, mapas conceptuales) para sintetizar información."
            },
            {
                "contenido": "Exposición sobre temas relacionados con el cuidado de la salud.",
                "pda": "Prepara y realiza una exposición sobre la prevención de enfermedades en su comunidad, utilizando material visual pertinente."
            },
            {
                "contenido": "Creación de propuestas con intención artística para mejorar la escuela o la comunidad.",
                "pda": "Diseña y presenta proyectos artísticos comunitarios para reflexionar sobre los problemas de convivencia y entorno escolar."
            }
        ],
        "Saberes y Pensamiento Científico": [
            {
                "contenido": "Estructura y funcionamiento del cuerpo humano: sistema inmunológico y órganos de los sentidos.",
                "pda": "Explica la participación del sistema inmunológico en la defensa del cuerpo humano y las acciones para su fortalecimiento (vacunación y nutrición)."
            },
            {
                "contenido": "Estudio de los números: fracciones y decimales en contextos cotidianos.",
                "pda": "Representa y compara fracciones (medios, cuartos, octavos, dieciseisavos) con apoyo de material concreto y representaciones gráficas."
            },
            {
                "contenido": "Ecosistemas: interacciones, factores físicos y biológicos, y el cuidado de la biodiversidad.",
                "pda": "Identifica y analiza las relaciones entre los factores físicos (agua, aire, suelo, sol) y biológicos que conforman los ecosistemas locales."
            }
        ],
        "Ética, Naturaleza y Sociedades": [
            {
                "contenido": "Origen histórico de algunos símbolos para las comunidades, la entidad y México.",
                "pda": "Reconoce los símbolos nacionales (bandera, escudo, himno) y de su entidad, comprendiendo su significado histórico y sentido de identidad."
            },
            {
                "contenido": "Situaciones de discriminación en la escuela, la comunidad y el país sobre la diversidad.",
                "pda": "Analiza causas y consecuencias de la discriminación y propone acciones colectivas para favorecer la inclusión y la equidad de género."
            }
        ],
        "De lo Humano y lo Comunitario": [
            {
                "contenido": "Participación en la toma de decisiones sobre problemas de la comunidad.",
                "pda": "Propone y evalúa alternativas viables de solución a problemáticas identificadas en el entorno escolar y vecinal."
            },
            {
                "contenido": "Efectos en la vida de las personas derivados de cambios sociales, culturales y en la salud.",
                "pda": "Reflexiona sobre los cambios en las costumbres y la alimentación de su comunidad a través del tiempo y su impacto en la salud."
            }
        ]
    },
    "5° de Primaria": {
        "Lenguajes": [
            {
                "contenido": "Narración de sucesos autobiográficos.",
                "pda": "Lee textos autobiográficos e identifica las relaciones temporales de secuencia, simultaneidad y duración. Usa reflexivamente adverbios, frases adverbiales y nexos temporales para indicar secuencia."
            },
            {
                "contenido": "Comprensión y producción de textos informativos, para ampliar sus conocimientos sobre temas de interés tanto colectivo como individual.",
                "pda": "Selecciona y lee textos informativos sobre temas de su interés. Formula preguntas para guiar la búsqueda de información específica; localiza la información y elabora cuadros sinópticos y resúmenes."
            },
            {
                "contenido": "Participación en debates sobre temas de interés común.",
                "pda": "Reconoce que hay temas donde las opiniones se dividen, y es necesario sustentar las propias ideas con argumentos basados en hechos y datos."
            },
            {
                "contenido": "Elaboración de un tríptico informativo sobre la prevención de algún problema colectivo.",
                "pda": "Recopila y analiza información para difundir medidas de prevención en su comunidad escolar o vecinal; organiza la información mediante títulos, subtítulos, viñetas e imágenes pertinentes."
            }
        ],
        "Saberes y Pensamiento Científico": [
            {
                "contenido": "Estructura y funcionamiento del cuerpo humano: sistemas circulatorio, respiratorio e inmunológico, y su relación con la salud ambiental.",
                "pda": "Describe y representa mediante modelos la relación entre la nariz, tráquea y pulmones, en el intercambio de gases. Explica la participación del sistema inmunológico en la defensa del cuerpo humano."
            },
            {
                "contenido": "Alimentación saludable: características de la dieta correcta, costumbres de la comunidad, riesgos del consumo de alimentos ultraprocesados.",
                "pda": "Explica las características de la dieta correcta: variada, completa, equilibrada, inocua, suficiente y adecuada, contrastándolas con sus hábitos de consumo para diseñar menús saludables."
            },
            {
                "contenido": "Multiplicación y división, su relación como operaciones inversas.",
                "pda": "Resuelve situaciones problemáticas vinculadas a diferentes contextos que implican multiplicar números fraccionarios y números decimales, con un número natural como multiplicador."
            },
            {
                "contenido": "Figuras geométricas y sus características.",
                "pda": "Con el apoyo de instrumentos geométricos, construye, analiza y clasifica cuadriláteros a partir de sus lados, ángulos y diagonales; explica los criterios utilizados para su clasificación."
            }
        ],
        "Ética, Naturaleza y Sociedades": [
            {
                "contenido": "Valoración de la biodiversidad en el territorio donde se ubica la localidad, entidad, México y el mundo, valores, acciones sustentables.",
                "pda": "Comprende la biodiversidad, su función como elemento vital en la Tierra y en el equilibrio de la biosfera, así como la importancia para la vida humana y de las demás especies."
            },
            {
                "contenido": "La cultura de paz: construyendo ambientes libres de discriminación y violencia.",
                "pda": "Identifica las causas de conflictos cotidianos en la escuela y su comunidad, analiza alternativas de resolución mediante el diálogo, la mediación y el establecimiento de acuerdos colectivos."
            },
            {
                "contenido": "Movimientos sociales en el México de los siglos XIX y XX: la Independencia y la Revolución Mexicana.",
                "pda": "Indaga en fuentes bibliográficas y orales las causas, desarrollo e implicaciones de la Revolución Social de 1910, reconociendo el papel de campesinos, obreros y líderes revolucionarios."
            }
        ],
        "De lo Humano y lo Comunitario": [
            {
                "contenido": "Formas de ser, pensar, actuar y relacionarse.",
                "pda": "Reflexiona acerca de las formas de ser, pensar, actuar y relacionarse que tienen las personas y los factores que las originan para propiciar el entendimiento mutuo y la empatía."
            },
            {
                "contenido": "Toma de decisiones y asertividad en situaciones cotidianas.",
                "pda": "Describe los problemas de vida cotidiana que ha enfrentado y reflexiona sobre la resolución de los mismos, evaluando posibles alternativas con base en el bienestar propio y colectivo."
            },
            {
                "contenido": "Capacidades, habilidades y destrezas motrices.",
                "pda": "Reconoce posibilidades y límites al participar en situaciones de juego e iniciación deportiva, individuales y colectivas, para valorar su desempeño y determinar posibles mejoras."
            }
        ]
    },
    "6° de Primaria": {
        "Lenguajes": [
            {
                "contenido": "Comprensión y producción de textos argumentativos sobre temas polémicos.",
                "pda": "Lee textos sobre temas polémicos e identifica los argumentos sustentados; escribe textos argumentativos con postura fundamentada."
            },
            {
                "contenido": "Elaboración de un manual de juegos de patio o de mesa para favorecer la convivencia.",
                "pda": "Diseña un manual de juegos colectivos con instrucciones claras, reglas consensuadas y materiales para fomentar la inclusión en el recreo."
            },
            {
                "contenido": "Producción y envío de cartas personales y correos electrónicos con distintos propósitos.",
                "pda": "Escribe y envía cartas y correos respetando las convenciones formales, adaptando el tono según el destinatario y la intención comunicativa."
            }
        ],
        "Saberes y Pensamiento Científico": [
            {
                "contenido": "Estructura y funcionamiento del cuerpo humano: sistemas circulatorio, nervioso y endocrino en la pubertad.",
                "pda": "Explica los cambios físicos y emocionales durante la pubertad y su relación con el sistema endocrino; propone acciones de autocuidado integral."
            },
            {
                "contenido": "Relaciones de proporcionalidad: cálculo de porcentajes y aplicación comercial.",
                "pda": "Resuelve situaciones problemáticas que implican calcular porcentajes (descuentos, intereses e IVA) en contextos financieros cotidianos."
            },
            {
                "contenido": "Funciones vitales que caracterizan a plantas y animales como seres vivos, y su reproducción.",
                "pda": "Comprende y compara la reproducción sexual y asexual en plantas y animales, reconociendo su importancia para la conservación biológica."
            }
        ],
        "Ética, Naturaleza y Sociedades": [
            {
                "contenido": "La cultura democrática: principios éticos que subyacen en los acuerdos, normas y leyes.",
                "pda": "Evalúa la aplicación justa y equitativa de las normas y leyes en la vida escolar y comunitaria, promoviendo la rendición de cuentas."
            },
            {
                "contenido": "Cultura de paz: derechos humanos, justicia social y resolución pacífica de controversias.",
                "pda": "Analiza el papel de las instituciones garantes de los derechos humanos y propone acciones para erradicar cualquier tipo de violencia."
            },
            {
                "contenido": "Movimientos sociales en el México de los siglos XIX y XX: la Independencia y la Revolución Social de 1910.",
                "pda": "Analiza críticamente las causas y consecuencias de la Revolución Social de 1910 y los ideales de justicia social, reconociendo su vigencia en la transformación democrática de su entorno escolar y comunitario."
            }
        ],
        "De lo Humano y lo Comunitario": [
            {
                "contenido": "Proyectos de vida y valoración de metas personales y colectivas.",
                "pda": "Valora sus logros y habilidades en distintas áreas para plantearse metas realistas a corto y mediano plazo hacia la educación secundaria."
            },
            {
                "contenido": "Estilos de vida activos y saludables para la prevención de enfermedades crónicas.",
                "pda": "Diseña y evalúa un plan semanal de actividad física y alimentación balanceada para su comunidad escolar."
            },
            {
                "contenido": "La comunidad como el espacio para el aprendizaje y el bienestar común.",
                "pda": "Diseña, organiza y participa en acciones colectivas y círculos comunitarios para promover el acceso equitativo a tecnologías y la lectura compartida en el entorno familiar."
            }
        ]
    }
}

CONTENIDOS_PDA_EJEMPLO = CONTENIDOS_PDA_POR_GRADO["6° de Primaria"]

CONTEXTO_ESCOLAR_PREDETERMINADO = """Entorno Escolar y Comunitario (Durango):
La Escuela Primaria “Revolución Social de 1910” (CCT: 10EPR0361N, Zona 49, Sector 02) está ubicada en una zona urbana consolidada de Durango. El entorno escolar y comunitario se caracteriza por familias trabajadoras con una presencia notable de profesionistas, empleados y jubilados con fuerte arraigo social. En general, las familias muestran interés y respaldo hacia la formación escolar de sus hijos; no obstante, se detecta la conveniencia de vincular aún más las actividades escolares con la vida práctica y fortalecer el acompañamiento lector continuo en el hogar."""

CONTEXTO_GRUPAL_PREDETERMINADO = """Diagnóstico del Grupo (6° Grado Grupo “A” - Fase 5):
Matrícula oficial de 26 alumnos (niñas y niños activos, curiosos, con disposición al trabajo en equipo y alta sensibilidad social).
- Canales y Estilos de Aprendizaje Predominantes:
  * Estilo Kinestésico (predominante): El grupo aprende significativamente a través de la acción vivencial, la experimentación práctica, la manipulación de materiales concretos, la dramatización, juegos de roles y dinámicas por estaciones o proyectos activos.
  * Estilo Visual (ampliamente desarrollado): Manifiestan una excelente asimilación de conceptos mediante el empleo de organizadores gráficos (mapas mentales, mapas conceptuales, cuadros sinópticos), infografías, colores de jerarquización, esquemas interactivos y recursos audiovisuales.
- Enfoque DUA y Atención a la Diversidad: Ritmos de aprendizaje heterogéneos que demandan diversificación didáctica mediante el Diseño Universal para el Aprendizaje, trabajo en parejas pedagógicas y tutoría entre pares solidaria."""

PROBLEMATIZACIONES_PREDETERMINADAS = """Ejes de Trabajo y Problemáticas Priorizadas (Programa Analítico Ciclo Escolar 2026-2027):
1. Comprensión Lectora:
   Dificultad detectada en un porcentaje significativo de alumnos para recuperar ideas centrales, realizar inferencias complejas, deducir vocabulario contextual y estructurar posturas críticas fundadas al analizar textos informativos, literarios y científicos.
2. Velocidad y Fluidez Lectora:
   Necesidad de incrementar la precisión, dicción, modulación y velocidad en la lectura en voz alta para favorecer la seguridad personal, la expresión oral elocuente y la asimilación ágil de contenidos extensos.
3. Ortografía y Producción de Textos Escritos:
   Rezago en la aplicación sistemática de reglas de acentuación (agudas, graves, esdrújulas), manejo de grafías de uso dudoso (b/v, c/s/z, g/j, h), uso riguroso de signos de puntuación y estructuración lógica de párrafos en la redacción autónoma de textos argumentativos e informativos.
4. Asuntos Comunitarios (Promoción de la Lectura, Acceso a Tecnologías y Recursos):
   Poco hábito de lectura compartida en el contexto familiar y comunitario. Necesidad de reducir brechas de acceso a recursos de información y guiar a las y los alumnos en el uso crítico, ético y pedagógico de tecnologías digitales para la indagación, la divulgación y la resolución colaborativa de problemas del entorno."""

EJEMPLO_PROBLEMICA_ANALITICO = f"""PROGRAMA ANALÍTICO OFICIAL (CICLO ESCOLAR 2026-2027)
Escuela Primaria “Revolución Social de 1910” (CCT: 10EPR0361N) - Zona 49, Sector 02, Durango.
Docente Titular: Maestra Aday Domínguez Domínguez | Director: Guillermo Gerardo Borjas Díaz | 6° Grado Grupo “A” (Fase 5, 26 alumnos).

I. CONTEXTO ESCOLAR Y COMUNITARIO (DURANGO):
{CONTEXTO_ESCOLAR_PREDETERMINADO}

II. CONTEXTO GRUPAL Y ESTILOS DE APRENDIZAJE:
{CONTEXTO_GRUPAL_PREDETERMINADO}

III. PROBLEMATIZACIONES IDENTIFICADAS (EJES DE TRABAJO PRIORITARIOS):
{PROBLEMATIZACIONES_PREDETERMINADAS}

IV. FUNDAMENTACIÓN Y DIRECTRICES PARA EL MOTOR DE IA:
- Cruzar de manera transversal e interdisciplinaria las 4 problemáticas (comprensión lectora, velocidad lectora, ortografía y promoción comunitaria de la lectura con uso reflexivo de tecnologías) a través de los 4 Campos Formativos: Lenguajes, Saberes y Pensamiento Científico, Ética Naturaleza y Sociedades, y De lo Humano y lo Comunitario.
- Dosificar el avance pedagógico y nivel de exigencia a lo largo de las 37 semanas oficiales del Calendario Escolar SEP (Ciclo 2026-2027).
- En las rutinas matutinas de inicio, integrar dictados con retos ortográficos específicos (acentuación, grafías dudosas), cálculo mental contextualizado, lectura cronometrada de fluidez (1 minuto) y problemas matemáticos razonados vinculados a la comunidad.
- En la secuencia didáctica diaria (Inicio, Desarrollo y Cierre), incorporar obligatoriamente dinámicas kinestésicas vivenciales (manipulación, dramatización, estaciones de trabajo activas) y recursos visuales estructurados (organizadores gráficos, infografías, diagramas) para potenciar el aprendizaje de los 26 alumnos de 6° "A".
- Aplicar el enfoque DUA (Diseño Universal para el Aprendizaje) con ajustes razonables para eliminar barreras de aprendizaje y garantizar la inclusión plena.
- Diseñar productos formativos y rúbricas analíticas orientadas a la acción comunitaria en Durango y al uso pedagógico, crítico y ético de herramientas digitales."""
import calendar
import datetime
from file_processor import (
    process_uploaded_files,
    format_context_for_prompt,
    extract_text_from_pdf,
    extract_text_from_docx,
    extract_text_from_txt,
    extraer_texto_url,
    extraer_contenidos_pda_fase5
)
import socket
import requests
try:
    import httpx
except ImportError:
    httpx = None
import importlib
import gemini_engine
importlib.reload(gemini_engine)
from gemini_engine import (
    generate_planeacion,
    generate_sample_fallback,
    AVAILABLE_MODELS,
    verificar_conexion_internet
)
from docx_generator import build_docx_planeacion, parse_plan_sections, extract_day_from_text
from pdf_generator import build_pdf_planeacion
from conaliteg_scraper import obtener_libros_conaliteg, buscar_programa_sintetico_sep

try:
    from duckduckgo_search import DDGS
except ImportError:
    try:
        from ddgs import DDGS
    except ImportError:
        DDGS = None

@st.cache_data(ttl=3600, show_spinner=False)
def get_cached_conaliteg_books():
    """Obtiene y cachea en memoria los libros de texto de CONALITEG."""
    return obtener_libros_conaliteg()

import re
from urllib.parse import urlparse, parse_qs
import streamlit.components.v1 as components

# Lista de reproducción oficial predeterminada de YouTube para Educación Primaria / NEM
URL_PLAYLIST_OFICIAL_YOUTUBE = "https://www.youtube.com/watch?v=AN8rqiS_H9Y&list=PLUMiCjvK3jNw"
EMBED_PLAYLIST_OFICIAL_YOUTUBE = "https://www.youtube.com/embed/AN8rqiS_H9Y?list=PLUMiCjvK3jNw"

def extraer_embed_youtube(url_o_id: str) -> str:
    """
    Convierte cualquier enlace o identificador de YouTube al formato oficial de inserción embebida (embed).
    Asegura que los enlaces de formato 'watch?v=', 'youtu.be/', '/live/', '/shorts/', listas de reproducción
    o códigos iframe se transformen rigurosamente a 'https://www.youtube.com/embed/...' sin errores de disponibilidad ni bloqueos.
    Si el parámetro está vacío o no es válido, retorna la lista de reproducción oficial predeterminada.
    """
    if not url_o_id or not str(url_o_id).strip():
        return EMBED_PLAYLIST_OFICIAL_YOUTUBE
    
    texto = str(url_o_id).strip()
    
    # 1. Si el usuario pegó el código iframe HTML completo (<iframe src="...">)
    match_iframe = re.search(r'src=["\']([^"\']+)["\']', texto)
    if match_iframe:
        texto = match_iframe.group(1).strip()
    
    # 2. Si ya es una URL embed limpia de YouTube
    if "youtube.com/embed/" in texto or "youtube-nocookie.com/embed/" in texto:
        if texto.startswith("//"):
            return "https:" + texto
        elif not texto.startswith("http"):
            return "https://" + texto
        return texto
    
    # 3. Limpieza de protocolo
    url_limpia = texto
    if url_limpia.startswith("//"):
        url_limpia = "https:" + url_limpia
    elif not url_limpia.startswith("http://") and not url_limpia.startswith("https://"):
        if "/" in url_limpia or "?" in url_limpia:
            url_limpia = "https://" + url_limpia

    video_id = None
    list_id = None

    # Extraer parámetros de query string mediante urlparse
    try:
        parsed = urlparse(url_limpia)
        qs = parse_qs(parsed.query)
        if "list" in qs and qs["list"]:
            list_id = qs["list"][0]
        if "v" in qs and qs["v"]:
            candidate_v = qs["v"][0]
            if re.match(r'^[a-zA-Z0-9_-]{11}$', candidate_v):
                video_id = candidate_v
    except Exception:
        pass

    # Si aún no tenemos video_id, probar expresiones regulares
    if not video_id:
        # youtu.be/<id>
        match_short = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', texto)
        if match_short:
            video_id = match_short.group(1)
        # /live/<id>
        elif "/live/" in texto:
            match_live = re.search(r'/live/([a-zA-Z0-9_-]{11})', texto)
            if match_live:
                video_id = match_live.group(1)
        # /shorts/<id>
        elif "/shorts/" in texto:
            match_shorts = re.search(r'/shorts/([a-zA-Z0-9_-]{11})', texto)
            if match_shorts:
                video_id = match_shorts.group(1)
        # watch?v=<id> o &v=<id>
        elif "v=" in texto:
            match_v = re.search(r'[?&]v=([a-zA-Z0-9_-]{11})', texto)
            if match_v:
                video_id = match_v.group(1)
        # ID directo de 11 caracteres alfanuméricos
        elif re.match(r'^[a-zA-Z0-9_-]{11}$', texto):
            video_id = texto

    # Si no se encontró lista en parse_qs, buscar con regex
    if not list_id:
        match_list = re.search(r'[?&]list=([a-zA-Z0-9_-]+)', texto)
        if match_list:
            list_id = match_list.group(1)

    # Construir la URL embebida oficial
    if video_id:
        if list_id:
            return f"https://www.youtube.com/embed/{video_id}?list={list_id}"
        return f"https://www.youtube.com/embed/{video_id}"
    elif list_id:
        return f"https://www.youtube.com/embed/videoseries?list={list_id}"

    # Fallback predeterminado seguro hacia la lista de reproducción oficial
    return EMBED_PLAYLIST_OFICIAL_YOUTUBE

# ==========================================
# CONFIGURACIÓN DE PÁGINA STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Planeaciones Escolares Educación Primaria",
    page_icon="•",
    layout="wide",
    initial_sidebar_state="auto"
)

# ==========================================
# ESTILOS CSS PERSONALIZADOS (ESTÉTICA FEMENINA ELEGANTE - ESTILO GEMINI)
# ==========================================
st.markdown("""
<style>
    /* Tipografía y fuentes estilizadas modernas */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
    }

    h1, h2, h3, h4, .banner-title {
        font-family: 'Outfit', sans-serif;
    }

    /* =======================================================
       PALETA DEFINITIVA: MORADOS, LILAS Y ALTO CONTRASTE
       ======================================================= */
    :root {
        --purple-vibrant: #7C3AED;
        --purple-deep: #6D28D9;
        --purple-dark: #5B21B6;
        --purple-accent: #8B5CF6;
        --purple-border: #8B5CF6;
        --lila-soft: #F3E8FF;
        --lila-canvas: #FAF5FF;
        --text-pure-white: #FFFFFF;
        --text-deep-black: #111111;
        --text-user-input: #000000;
        --border-radius-base: 10px;
    }

    /* =======================================================
       1. PANTALLA DE LOGIN: TEXTOS, ETIQUETAS Y CAMPOS LIMPIOS
       ======================================================= */

    /* Título y subtítulo del Login adaptativos */
    .login-header-title {
        font-family: 'Outfit', sans-serif !important;
        color: #111111 !important;
        margin-top: 0.75rem !important;
        margin-bottom: 0.25rem !important;
        font-size: 1.85rem !important;
        font-weight: 700 !important;
    }

    .login-header-desc {
        color: #5B21B6 !important;
        font-size: 0.95rem !important;
        margin-bottom: 1.5rem !important;
        font-weight: 600 !important;
    }

    @media (prefers-color-scheme: dark) {
        .login-header-title {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        .login-header-desc {
            color: #F3E8FF !important;
            -webkit-text-fill-color: #F3E8FF !important;
        }
    }

    [data-theme="dark"] .login-header-title {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    [data-theme="dark"] .login-header-desc {
        color: #F3E8FF !important;
        -webkit-text-fill-color: #F3E8FF !important;
    }

    /* Tarjeta del Formulario de Login */
    [data-testid="stForm"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #FAF5FF 100%) !important;
        border: 1.5px solid #8B5CF6 !important;
        border-radius: 20px !important;
        padding: 2.2rem !important;
        box-shadow: 0 12px 36px rgba(124, 58, 237, 0.12) !important;
    }

    /* Título dentro de la tarjeta de Login */
    [data-testid="stForm"] h1,
    [data-testid="stForm"] h2,
    [data-testid="stForm"] h3,
    [data-testid="stForm"] h4 {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin-bottom: 1.25rem !important;
    }

    /* Etiquetas del formulario de Login (Usuario, Contraseña) */
    [data-testid="stForm"] label,
    [data-testid="stForm"] label p,
    [data-testid="stForm"] label span,
    [data-testid="stForm"] [data-testid="stWidgetLabel"],
    [data-testid="stForm"] [data-testid="stWidgetLabel"] *,
    [data-testid="stForm"] p,
    [data-testid="stForm"] span {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* Cajas de texto en el formulario de Login (Usuario y Contraseña) */
    [data-testid="stForm"] input,
    [data-testid="stForm"] input[type="text"],
    [data-testid="stForm"] input[type="password"],
    [data-testid="stForm"] div[data-baseweb="input"],
    [data-testid="stForm"] div[data-baseweb="input"] > div,
    [data-testid="stForm"] div[data-baseweb="base-input"] {
        background: #F3E8FF !important;
        background-color: #F3E8FF !important;
        border: 1.5px solid #8B5CF6 !important;
        border-radius: 10px !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-size: 0.96rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stForm"] div[data-baseweb="input"]:focus-within,
    [data-testid="stForm"] div[data-baseweb="input"]:focus-within > div,
    [data-testid="stForm"] input:focus {
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.35) !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* =======================================================
       2. CAJAS DE TEXTO E INPUTS GENERALES: ELIMINACIÓN DE FONDO NEGRO O VERDE
          Fondo suave (#F3E8FF), bordes morados (#8B5CF6), texto en negro (#000000).
       ======================================================= */

    /* Inputs, textareas y selects base */
    input,
    textarea,
    select,
    input[type="text"],
    input[type="password"],
    input[type="number"],
    div.stTextInput input,
    div.stTextArea textarea,
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stNumberInput"] input,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] input,
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea,
    [data-testid="stSidebar"] div[data-baseweb="input"] input,
    [data-testid="stSidebar"] div[data-baseweb="select"] input {
        background: #F3E8FF !important;
        background-color: #F3E8FF !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        opacity: 1 !important;
    }

    /* Contenedores envolventes de inputs y selectores (sin fondos verdes ni negros) */
    div[data-baseweb="input"],
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"],
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="base-input"],
    div[data-baseweb="base-input"] > div,
    div[data-baseweb="select"] > div,
    div[data-testid="stTextInput"] div[data-baseweb="input"],
    div[data-testid="stTextInput"] div[data-baseweb="input"] > div,
    div[data-testid="stTextArea"] div[data-baseweb="textarea"],
    div[data-testid="stTextArea"] div[data-baseweb="textarea"] > div,
    div[data-testid="stNumberInput"] div[data-baseweb="input"],
    div[data-testid="stNumberInput"] div[data-baseweb="input"] > div,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
    div[data-testid="stMultiSelect"] div[data-baseweb="select"] > div,
    [data-testid="stSidebar"] div[data-baseweb="input"] > div,
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background: #F3E8FF !important;
        background-color: #F3E8FF !important;
        border: 1.5px solid #8B5CF6 !important;
        border-radius: 10px !important;
        color: #000000 !important;
        transition: all 0.25s ease !important;
    }

    /* Evitar fondos verdes / amarillos / negros causados por autocompletado del navegador */
    input:-webkit-autofill,
    input:-webkit-autofill:hover,
    input:-webkit-autofill:focus,
    input:-webkit-autofill:active,
    textarea:-webkit-autofill,
    select:-webkit-autofill {
        -webkit-box-shadow: 0 0 0 1000px #F3E8FF inset !important;
        box-shadow: 0 0 0 1000px #F3E8FF inset !important;
        -webkit-text-fill-color: #000000 !important;
        color: #000000 !important;
        caret-color: #000000 !important;
        background-color: #F3E8FF !important;
        transition: background-color 5000s ease-in-out 0s !important;
    }

    /* Estado en foco de inputs y selectores */
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="input"]:focus-within > div,
    div[data-baseweb="textarea"]:focus-within,
    div[data-baseweb="textarea"]:focus-within > div,
    div[data-baseweb="select"] > div:focus-within,
    input:focus,
    textarea:focus {
        border-color: #7C3AED !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.35) !important;
        background: #FFFFFF !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* Texto seleccionado en Selectboxes */
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] span {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        font-weight: 600 !important;
    }

    /* Placeholders nítidos */
    ::placeholder,
    input::placeholder,
    textarea::placeholder {
        color: #6B7280 !important;
        -webkit-text-fill-color: #6B7280 !important;
        opacity: 0.8 !important;
    }

    /* Menú desplegable emergente de selección (Dropdown) */
    ul[data-baseweb="menu"],
    div[data-baseweb="popover"] ul {
        background-color: #FAF5FF !important;
        border-radius: 12px !important;
        border: 1.5px solid #8B5CF6 !important;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.16) !important;
    }

    li[data-baseweb="menu-item"],
    ul[data-baseweb="menu"] li {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        background-color: #FAF5FF !important;
        font-weight: 500 !important;
    }

    li[data-baseweb="menu-item"]:hover,
    li[data-baseweb="menu-item"][aria-selected="true"] {
        background: #F3E8FF !important;
        color: #5B21B6 !important;
        -webkit-text-fill-color: #5B21B6 !important;
    }

    /* =======================================================
       3. TEXTOS Y ETIQUETAS: CONTRASTE ESTRICTO
          - Contenedores claros o blancos -> Gris oscuro / negro profundo (#1F2937)
          - Contenedores oscuros o de color (tarjetas de información, alertas) -> Blanco (#FFFFFF) o lila muy claro (#F3E8FF)
          - Círculos / Puntos decorativos -> Morado vibrante (#7C3AED)
       ======================================================= */

    /* Reglas generales para Lienzo Oscuro */
    @media (prefers-color-scheme: dark) {
        .stApp,
        [data-testid="stAppViewContainer"],
        .block-container {
            color: #F3E8FF !important;
        }
        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3,
        [data-testid="stAppViewContainer"] h4 {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
    }

    [data-theme="dark"] [data-testid="stAppViewContainer"] h1,
    [data-theme="dark"] [data-testid="stAppViewContainer"] h2,
    [data-theme="dark"] [data-testid="stAppViewContainer"] h3,
    [data-theme="dark"] [data-testid="stAppViewContainer"] h4 {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* Reglas generales para Lienzo Claro: forzar #1F2937 en párrafos, etiquetas y títulos */
    @media (prefers-color-scheme: light) {
        .stApp,
        [data-testid="stAppViewContainer"],
        .block-container,
        div.stMarkdown p:not([data-testid="stAlert"] *),
        div.stMarkdown span:not([data-testid="stAlert"] *):not(.purple-dot):not([style*="#7C3AED"]):not([style*="rgb(124, 58, 237)"]),
        div.stMarkdown li:not([data-testid="stAlert"] *),
        [data-testid="stWidgetLabel"] label,
        [data-testid="stWidgetLabel"] p,
        [data-testid="stWidgetLabel"] span {
            color: #1F2937 !important;
            -webkit-text-fill-color: #1F2937 !important;
        }
        h1, h2, h3, h4 {
            color: #1F2937 !important;
            -webkit-text-fill-color: #1F2937 !important;
        }
    }

    [data-theme="light"] [data-testid="stWidgetLabel"] label,
    [data-theme="light"] [data-testid="stWidgetLabel"] p,
    [data-theme="light"] [data-testid="stWidgetLabel"] span,
    [data-theme="light"] div.stMarkdown p:not([data-testid="stAlert"] *),
    [data-theme="light"] div.stMarkdown span:not([data-testid="stAlert"] *):not(.purple-dot):not([style*="#7C3AED"]):not([style*="rgb(124, 58, 237)"]) {
        color: #1F2937 !important;
        -webkit-text-fill-color: #1F2937 !important;
    }

    /* CONTENEDORES CON FONDO CLARO O BLANCO (Sidebar, Tarjetas NEM, Formulario, Dropdowns)
       Se fuerza color gris oscuro / negro profundo (#1F2937) en todo momento para garantizar máxima legibilidad */
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"],
    [data-testid="stSidebar"] > div:first-child,
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"],
    div[data-testid="stSidebarUserContent"] {
        background-color: #FAF5FF !important;
        border-right: 1.5px solid #EDE9FE !important;
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] label p,
    [data-testid="stSidebar"] label span,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"],
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] *,
    [data-testid="stSidebar"] div.stMarkdown p:not([data-testid="stAlert"] *),
    [data-testid="stSidebar"] div.stMarkdown span:not([data-testid="stAlert"] *):not(.purple-dot):not([style*="#7C3AED"]):not([style*="rgb(124, 58, 237)"]),
    [data-testid="stSidebar"] p:not([data-testid="stAlert"] *),
    [data-testid="stSidebar"] span:not([data-testid="stAlert"] *):not(.badge-sep):not([data-baseweb="tag"] *):not(.purple-dot):not([style*="#7C3AED"]):not([style*="rgb(124, 58, 237)"]),
    [data-testid="stForm"] label,
    [data-testid="stForm"] label *,
    [data-testid="stForm"] p:not([data-testid="stAlert"] *),
    [data-testid="stForm"] span:not([data-testid="stAlert"] *):not([data-baseweb="tag"] *):not(.purple-dot):not([style*="#7C3AED"]):not([style*="rgb(124, 58, 237)"]),
    .nem-card,
    .nem-card p:not([data-testid="stAlert"] *),
    .nem-card span:not([data-testid="stAlert"] *):not(.badge-sep):not([data-baseweb="tag"] *):not(.purple-dot):not([style*="#7C3AED"]):not([style*="rgb(124, 58, 237)"]),
    .nem-card div:not([data-testid="stAlert"]):not([data-testid="stAlert"] *),
    .nem-card li:not([data-testid="stAlert"] *),
    .nem-card label,
    .nem-card label *,
    .nem-card [data-testid="stWidgetLabel"] *,
    .nem-card table,
    .nem-card th,
    .nem-card td,
    ul[data-baseweb="menu"] li,
    div[data-baseweb="popover"] li {
        color: #1F2937 !important;
        -webkit-text-fill-color: #1F2937 !important;
    }

    /* Subtítulos y descripciones en contenedores claros (#374151) */
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
    [data-testid="stSidebar"] .stCaption,
    .nem-card [data-testid="stCaptionContainer"] p,
    .nem-card .stCaption,
    [data-testid="stForm"] [data-testid="stCaptionContainer"] p,
    div.stCaption p {
        color: #374151 !important;
        -webkit-text-fill-color: #374151 !important;
        font-weight: 500 !important;
    }

    /* Subtítulos dentro de expanders oscuros en la barra lateral (#F3E8FF / #FFFFFF) */
    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] [data-testid="stCaptionContainer"] p,
    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] .stCaption,
    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] [data-testid="stCaptionContainer"] span {
        color: #F3E8FF !important;
        -webkit-text-fill-color: #F3E8FF !important;
        font-weight: 500 !important;
    }

    /* Títulos en barra lateral y tarjetas NEM */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: #4C1D95 !important;
        -webkit-text-fill-color: #4C1D95 !important;
        font-weight: 700 !important;
    }

    .nem-card h1, .nem-card h2, .nem-card h3, .nem-card h4 {
        color: #1F2937 !important;
        -webkit-text-fill-color: #1F2937 !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
    }

    .nem-card-title {
        color: #4C1D95 !important;
        -webkit-text-fill-color: #4C1D95 !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
    }

    /* =======================================================
       TARJETAS DE INFORMACIÓN, ALERTAS Y NOTAS DE RESPALDO SEP
       (Contenedores oscuros / de color: Texto en Blanco #FFFFFF y Lila muy claro #F3E8FF)
       Aplica a: Modo de Respaldo SEP, Plantilla de Word, Consejos de Respaldo y Advertencias
    /* =======================================================
       TARJETAS DE INFORMACIÓN, ALERTAS Y NOTAS DE RESPALDO SEP
       (Contenedores oscuros: Texto en Blanco Nítido #FFFFFF con Máximo Contraste)
       Aplica a: Modo de Respaldo SEP, Plantilla de Word, Consejos de Respaldo y Advertencias
       ======================================================= */
    div[data-testid="stAlert"],
    div[data-testid="stNotification"],
    div.stAlert,
    [data-testid="stSidebar"] div[data-testid="stAlert"],
    [data-testid="stSidebar"] div.stAlert,
    .nem-card div[data-testid="stAlert"],
    .nem-card div.stAlert,
    div[data-testid="stAppViewContainer"] div[data-testid="stAlert"] {
        background: linear-gradient(135deg, #2E1065 0%, #1E1B4B 100%) !important;
        background-color: #2E1065 !important;
        border: 1.5px solid #8B5CF6 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 16px rgba(124, 58, 237, 0.22) !important;
        padding: 0.95rem 1.25rem !important;
        margin: 0.75rem 0 !important;
    }

    /* Texto principal de notas y alertas en blanco nítido (#FFFFFF) garantizado */
    div[data-testid="stAlert"] *,
    div[data-testid="stNotification"] *,
    div.stAlert *,
    [data-testid="stSidebar"] div[data-testid="stAlert"] *,
    [data-testid="stSidebar"] div.stAlert *,
    .nem-card div[data-testid="stAlert"] *,
    .nem-card div.stAlert *,
    div[data-testid="stAppViewContainer"] div[data-testid="stAlert"] * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    div[data-testid="stAlert"] p,
    div[data-testid="stAlert"] span,
    div[data-testid="stAlert"] div,
    div[data-testid="stAlert"] li,
    div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p,
    div[data-testid="stNotification"] p,
    div[data-testid="stNotification"] span,
    div.stAlert p,
    div.stAlert span,
    [data-testid="stSidebar"] div[data-testid="stAlert"] p,
    [data-testid="stSidebar"] div[data-testid="stAlert"] span {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-size: 0.94rem !important;
        line-height: 1.55 !important;
    }

    /* Títulos destacados y textos en negrita dentro de alertas en blanco nítido (#FFFFFF) */
    div[data-testid="stAlert"] strong,
    div[data-testid="stAlert"] b,
    div[data-testid="stAlert"] em,
    div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] strong,
    div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] b,
    div[data-testid="stNotification"] strong,
    div[data-testid="stNotification"] b,
    div.stAlert strong,
    div.stAlert b,
    [data-testid="stSidebar"] div[data-testid="stAlert"] strong,
    [data-testid="stSidebar"] div[data-testid="stAlert"] b,
    .nem-card div[data-testid="stAlert"] strong {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Código inline dentro de notas de respaldo y alertas (ej. site:sep.gob.mx) */
    div[data-testid="stAlert"] code,
    div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] code,
    div[data-testid="stNotification"] code,
    div.stAlert code,
    [data-testid="stSidebar"] div[data-testid="stAlert"] code,
    .nem-card div[data-testid="stAlert"] code {
        background: #4C1D95 !important;
        background-color: #4C1D95 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border: 1.5px solid #A78BFA !important;
        border-radius: 6px !important;
        padding: 2px 7px !important;
        font-weight: 600 !important;
        font-size: 0.88em !important;
        font-family: 'Consolas', 'Monaco', monospace !important;
    }

    /* Enlaces dentro de notas y alertas */
    div[data-testid="stAlert"] a,
    div[data-testid="stNotification"] a,
    div.stAlert a {
        color: #E9D5FF !important;
        -webkit-text-fill-color: #E9D5FF !important;
        text-decoration: underline !important;
        font-weight: 600 !important;
    }

    /* Iconos SVG dentro de notas y alertas */
    div[data-testid="stAlert"] svg,
    div[data-testid="stNotification"] svg,
    div.stAlert svg,
    [data-testid="stSidebar"] div[data-testid="stAlert"] svg,
    .nem-card div[data-testid="stAlert"] svg {
        fill: #FFFFFF !important;
        color: #FFFFFF !important;
    }

    /* =======================================================
       BOTÓN / EXPANDER DE PERSONALIZAR CONTENIDOS Y PDA
       ======================================================= */
    div[data-testid="stExpander"],
    details[data-testid="stExpander"] {
        border: 1.5px solid #8B5CF6 !important;
        border-radius: 14px !important;
        background-color: #FFFFFF !important;
        margin: 1rem 0 !important;
        overflow: hidden !important;
        box-shadow: 0 2px 10px rgba(124, 58, 237, 0.08) !important;
        transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
    }

    div[data-testid="stExpander"]:hover,
    details[data-testid="stExpander"]:hover {
        border-color: #7C3AED !important;
        box-shadow: 0 4px 16px rgba(124, 58, 237, 0.16) !important;
    }

    /* Botón de cabecera del expander (Summary): claro (#EDE9FE) con texto legible #1F2937 */
    details[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary {
        background: #EDE9FE !important;
        background-color: #EDE9FE !important;
        border-radius: 12px !important;
        padding: 0.85rem 1.25rem !important;
        cursor: pointer !important;
        border-bottom: 1.5px solid #C4B5FD !important;
        transition: all 0.25s ease !important;
    }

    details[data-testid="stExpander"] summary:hover,
    div[data-testid="stExpander"] summary:hover,
    [data-testid="stExpander"] summary:hover {
        background: #DDD6FE !important;
        background-color: #DDD6FE !important;
    }

    /* Texto del botón de personalizar contenidos: perfectamente legible (#1F2937 oscuro profundo) */
    details[data-testid="stExpander"] summary,
    details[data-testid="stExpander"] summary *,
    details[data-testid="stExpander"] summary span,
    details[data-testid="stExpander"] summary p,
    details[data-testid="stExpander"] summary div,
    div[data-testid="stExpander"] summary,
    div[data-testid="stExpander"] summary *,
    div[data-testid="stExpander"] summary span,
    div[data-testid="stExpander"] summary p,
    div[data-testid="stExpander"] summary div,
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary *,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary div {
        color: #1F2937 !important;
        -webkit-text-fill-color: #1F2937 !important;
        font-weight: 700 !important;
        font-size: 0.98rem !important;
        letter-spacing: 0.2px !important;
    }

    /* Icono del chevron en expander */
    details[data-testid="stExpander"] summary svg,
    div[data-testid="stExpander"] summary svg,
    [data-testid="stExpander"] summary svg {
        fill: #7C3AED !important;
        color: #7C3AED !important;
    }

    /* Contenedor desplegado general (Details): Fondo claro con textos en #1F2937 */
    div[data-testid="stExpanderDetails"],
    div[data-testid="stExpanderDetails"] * {
        background-color: #FFFFFF !important;
        color: #1F2937 !important;
        -webkit-text-fill-color: #1F2937 !important;
    }

    div[data-testid="stExpanderDetails"] label,
    div[data-testid="stExpanderDetails"] label p,
    div[data-testid="stExpanderDetails"] label span,
    div[data-testid="stExpanderDetails"] p,
    div[data-testid="stExpanderDetails"] span {
        color: #1F2937 !important;
        -webkit-text-fill-color: #1F2937 !important;
    }

    div[data-testid="stExpanderDetails"] textarea,
    div[data-testid="stExpanderDetails"] input {
        color: #1F2937 !important;
        -webkit-text-fill-color: #1F2937 !important;
        background-color: #FFFFFF !important;
        border: 1.5px solid #C4B5FD !important;
    }

    /* =======================================================
       CORRECCIÓN DE CONTRASTE DEFINITIVA: DIRECTRICES CTE EN SIDEBAR
       Texto claro, nítido y legible (#F3E8FF / #FFFFFF) sobre fondo oscuro/morado
       ======================================================= */
    [data-testid="stSidebar"] div[data-testid="stExpander"],
    [data-testid="stSidebar"] details[data-testid="stExpander"] {
        background-color: #1E1B4B !important;
        border: 1px solid #7C3AED !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }

    [data-testid="stSidebar"] details[data-testid="stExpander"] summary,
    [data-testid="stSidebar"] div[data-testid="stExpander"] summary,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        background: #2E1065 !important;
        background-color: #2E1065 !important;
        border-bottom: 1px solid #4C1D95 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] details[data-testid="stExpander"] summary *,
    [data-testid="stSidebar"] details[data-testid="stExpander"] summary span,
    [data-testid="stSidebar"] details[data-testid="stExpander"] summary p,
    [data-testid="stSidebar"] div[data-testid="stExpander"] summary *,
    [data-testid="stSidebar"] div[data-testid="stExpander"] summary span,
    [data-testid="stSidebar"] div[data-testid="stExpander"] summary p {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] details[data-testid="stExpander"] summary svg,
    [data-testid="stSidebar"] div[data-testid="stExpander"] summary svg {
        fill: #C084FC !important;
        color: #C084FC !important;
    }

    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"],
    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] * {
        background-color: #1E1B4B !important;
        color: #F3E8FF !important;
        -webkit-text-fill-color: #F3E8FF !important;
    }

    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] strong,
    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] b,
    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] h1,
    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] h2,
    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] h3,
    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] h4 {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* Adaptación en modo oscuro para el botón de personalizar contenidos */
    @media (prefers-color-scheme: dark) {
        div[data-testid="stExpander"],
        details[data-testid="stExpander"] {
            border-color: #A78BFA !important;
            background-color: #1E1B4B !important;
        }

        details[data-testid="stExpander"] summary,
        div[data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary {
            background: #2E1065 !important;
            background-color: #2E1065 !important;
            border-bottom: 1.5px solid #4C1D95 !important;
        }

        details[data-testid="stExpander"] summary:hover,
        div[data-testid="stExpander"] summary:hover,
        [data-testid="stExpander"] summary:hover {
            background: #3B0764 !important;
            background-color: #3B0764 !important;
        }

        details[data-testid="stExpander"] summary,
        details[data-testid="stExpander"] summary *,
        details[data-testid="stExpander"] summary span,
        details[data-testid="stExpander"] summary p,
        details[data-testid="stExpander"] summary div,
        div[data-testid="stExpander"] summary,
        div[data-testid="stExpander"] summary *,
        div[data-testid="stExpander"] summary span,
        div[data-testid="stExpander"] summary p,
        div[data-testid="stExpander"] summary div,
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary *,
        [data-testid="stExpander"] summary span,
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary div {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        details[data-testid="stExpander"] summary svg,
        div[data-testid="stExpander"] summary svg,
        [data-testid="stExpander"] summary svg {
            fill: #FFFFFF !important;
            color: #FFFFFF !important;
        }

        div[data-testid="stExpanderDetails"],
        div[data-testid="stExpanderDetails"] * {
            background-color: #1E1B4B !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        div[data-testid="stExpanderDetails"] label,
        div[data-testid="stExpanderDetails"] label p,
        div[data-testid="stExpanderDetails"] label span,
        div[data-testid="stExpanderDetails"] p,
        div[data-testid="stExpanderDetails"] span {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        div[data-testid="stExpanderDetails"] textarea,
        div[data-testid="stExpanderDetails"] input {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            background-color: #2E1065 !important;
            border: 1.5px solid #7C3AED !important;
        }
    }

    [data-theme="dark"] details[data-testid="stExpander"] summary,
    [data-theme="dark"] div[data-testid="stExpander"] summary,
    [data-theme="dark"] [data-testid="stExpander"] summary {
        background: #2E1065 !important;
        background-color: #2E1065 !important;
        border-bottom: 1.5px solid #4C1D95 !important;
    }

    [data-theme="dark"] details[data-testid="stExpander"] summary *,
    [data-theme="dark"] div[data-testid="stExpander"] summary *,
    [data-theme="dark"] [data-testid="stExpander"] summary * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    [data-theme="dark"] div[data-testid="stExpanderDetails"],
    [data-theme="dark"] div[data-testid="stExpanderDetails"] * {
        background-color: #1E1B4B !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    [data-theme="dark"] div[data-testid="stExpanderDetails"] textarea,
    [data-theme="dark"] div[data-testid="stExpanderDetails"] input {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        background-color: #2E1065 !important;
        border: 1.5px solid #7C3AED !important;
    }

    /* =======================================================
       BADGE DE SESIONES DIDÁCTICAS: COLOR OSCURO Y PROFUNDO (#111111)
       ======================================================= */
    .badge-sesiones-count,
    span.badge-sesiones-count {
        background-color: #DDD6FE !important;
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        font-weight: 800 !important;
        font-size: 0.82rem !important;
        padding: 3px 12px !important;
        border-radius: 9999px !important;
        border: 1px solid #7C3AED !important;
        display: inline-block !important;
        white-space: nowrap !important;
        letter-spacing: -0.1px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08) !important;
    }

    /* =======================================================
       CALENDARIO SEP 2026: REDISEÑO MINIMALISTA Y COMPACTO
       ======================================================= */
    .cal-minimal-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 0.85rem 1rem;
        margin: 0.4rem 0 0.8rem 0;
        box-shadow: 0 1px 6px rgba(0, 0, 0, 0.03);
    }
    .cal-mini-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid #F1F5F9;
    }
    .cal-mini-wrap {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 0.55rem 0.7rem;
    }
    .cal-mini-title {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.78rem;
        font-weight: 700;
        color: #374151;
        letter-spacing: 0.4px;
        margin-bottom: 5px;
    }
    .cal-mini-badge {
        background: #EDE9FE;
        color: #6D28D9;
        font-size: 0.70rem;
        font-weight: 700;
        padding: 1px 6px;
        border-radius: 4px;
        border: 1px solid #DDD6FE;
    }
    .cal-mini-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 2.5px;
        text-align: center;
        margin: 0;
    }
    .cal-mini-table th {
        font-size: 0.68rem;
        font-weight: 600;
        color: #64748B;
        padding: 1px 0;
    }
    .cal-mini-table td {
        font-size: 0.72rem;
        padding: 3.5px 0;
        border-radius: 4px;
        color: #1E293B;
        background: #FFFFFF;
        border: 1px solid #F1F5F9;
        min-width: 20px;
        line-height: 1.1;
    }
    .cal-mini-active {
        background: #7C3AED !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 700 !important;
        border-color: #6D28D9 !important;
        box-shadow: 0 1px 4px rgba(124, 58, 237, 0.35) !important;
    }
    .cal-mini-wend {
        color: #94A3B8 !important;
        -webkit-text-fill-color: #94A3B8 !important;
        background: #F8FAFC !important;
        border-color: transparent !important;
    }
    .cal-mini-empty {
        background: transparent !important;
        border: none !important;
        color: #CBD5E1 !important;
        -webkit-text-fill-color: #CBD5E1 !important;
        opacity: 0.3;
    }
    .cal-mini-vac {
        background: #FEF3C7 !important;
        color: #92400E !important;
        -webkit-text-fill-color: #92400E !important;
        border: 1px dashed #F59E0B !important;
        border-radius: 4px !important;
        font-size: 0.70rem !important;
    }
    .cal-mini-cte {
        background: #FCE7F3 !important;
        color: #9D174D !important;
        -webkit-text-fill-color: #9D174D !important;
        border: 1px solid #F472B6 !important;
        font-weight: 700 !important;
        border-radius: 4px !important;
        font-size: 0.70rem !important;
    }
    @media (prefers-color-scheme: dark) {
        .cal-mini-vac {
            background: #78350F !important;
            color: #FEF3C7 !important;
            -webkit-text-fill-color: #FEF3C7 !important;
            border-color: #D97706 !important;
        }
        .cal-mini-cte {
            background: #831843 !important;
            color: #FCE7F3 !important;
            -webkit-text-fill-color: #FCE7F3 !important;
            border-color: #DB2777 !important;
        }
    }
    [data-theme="dark"] .cal-mini-vac {
        background: #78350F !important;
        color: #FEF3C7 !important;
        -webkit-text-fill-color: #FEF3C7 !important;
        border-color: #D97706 !important;
    }
    [data-theme="dark"] .cal-mini-cte {
        background: #831843 !important;
        color: #FCE7F3 !important;
        -webkit-text-fill-color: #FCE7F3 !important;
        border-color: #DB2777 !important;
    }

    .cal-mini-legend {
        display: flex;
        gap: 8px;
        font-size: 0.67rem;
        color: #64748B;
        margin-top: 5px;
        justify-content: center;
    }
    .cal-mini-legend span {
        display: inline-flex;
        align-items: center;
        gap: 3px;
    }
    .cal-mini-legend-dot {
        width: 6px;
        height: 6px;
        border-radius: 2px;
    }

    /* Clases retrocompatibles */
    .cal-wrapper {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 0.75rem;
    }
    .cal-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 3px;
        text-align: center;
    }
    .cal-table th {
        background: #EDE9FE;
        color: #4C1D95 !important;
        font-size: 0.75rem;
        padding: 4px;
    }
    .cal-table td {
        background: #FAF5FF;
        color: #1F2937 !important;
        font-size: 0.78rem;
        padding: 4px;
    }
    .cal-cell-active {
        background: #7C3AED !important;
        color: #FFFFFF !important;
        font-weight: bold;
    }
    .cal-cell-weekend {
        color: #94A3B8 !important;
        background: #F8FAFC !important;
    }
    .cal-cell-empty {
        background: transparent !important;
        color: transparent !important;
    }

    @media (prefers-color-scheme: dark) {
        .cal-minimal-box {
            background: #111827;
            border-color: #374151;
            box-shadow: none;
        }
        .cal-mini-header {
            border-bottom-color: #1F2937;
        }
        .cal-mini-wrap {
            background: #1F2937;
            border-color: #374151;
        }
        .cal-mini-title {
            color: #E5E7EB;
        }
        .cal-mini-table td {
            background: #111827;
            border-color: #374151;
            color: #E5E7EB;
        }
        .cal-mini-active {
            background: #7C3AED !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        .cal-mini-wend {
            background: #1F2937 !important;
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
        }
    }
    [data-theme="dark"] .cal-minimal-box {
        background: #111827;
        border-color: #374151;
        box-shadow: none;
    }
    [data-theme="dark"] .cal-mini-header {
        border-bottom-color: #1F2937;
    }
    [data-theme="dark"] .cal-mini-wrap {
        background: #1F2937;
        border-color: #374151;
    }
    [data-theme="dark"] .cal-mini-title {
        color: #E5E7EB;
    }
    [data-theme="dark"] .cal-mini-table td {
        background: #111827;
        border-color: #374151;
        color: #E5E7EB;
    }
    [data-theme="dark"] .cal-mini-active {
        background: #7C3AED !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    [data-theme="dark"] .cal-mini-wend {
        background: #1F2937 !important;
        color: #64748B !important;
        -webkit-text-fill-color: #64748B !important;
    }

    /* CÍRCULO / PUNTO MORADO DECORATIVO */
    .purple-dot,
    span.purple-dot,
    span[style*="#7C3AED"],
    span[style*="rgb(124, 58, 237)"] {
        color: #7C3AED !important;
        -webkit-text-fill-color: #7C3AED !important;
        display: inline-block;
        font-weight: bold;
    }

    /* =======================================================
       4. BOTONES Y SELECTORES: MORADO VIBRANTE Y TEXTO BLANCO
       ======================================================= */
    div.stButton > button,
    div.stDownloadButton > button,
    div[data-testid="stFormSubmitButton"] > button,
    button[kind="primary"],
    button[kind="secondary"],
    button[data-testid="baseButton-primary"],
    button[data-testid="baseButton-secondary"],
    [data-testid="stSidebar"] div.stButton > button,
    [data-testid="stForm"] div.stButton > button,
    .st-key-btn_generar_web button,
    div[class*="st-key-btn_generar_web"] button,
    .st-key-btn_ddgs_buscar button,
    div[class*="st-key-btn_ddgs_buscar"] button,
    .st-key-btn_nueva_planeacion button,
    div[class*="st-key-btn_nueva_planeacion"] button,
    .st-key-btn_limpiar_busqueda button,
    div[class*="st-key-btn_limpiar_busqueda"] button,
    div[data-testid="stNumberInput"] button,
    div[data-testid="stNumberInputStepDown"] button,
    div[data-testid="stNumberInputStepUp"] button,
    div[data-testid="stNumberInputStepDown"],
    div[data-testid="stNumberInputStepUp"],
    div[data-testid="stMultiSelect"] [data-baseweb="tag"],
    .stMultiSelect [data-baseweb="tag"],
    [data-baseweb="tag"] {
        background: #7C3AED !important;
        background-color: #7C3AED !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border: 1px solid #7C3AED !important;
        border-radius: 12px !important;
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
        padding: 0.55rem 1.25rem !important;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.35) !important;
        transition: all 0.25s ease !important;
    }

    /* Píldoras del selector de días (st.multiselect) */
    div[data-testid="stMultiSelect"] [data-baseweb="tag"],
    .stMultiSelect [data-baseweb="tag"],
    [data-baseweb="tag"] {
        padding: 3px 10px !important;
        margin: 2px !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 6px rgba(124, 58, 237, 0.25) !important;
    }

    /* Botones del selector de semanas (st.number_input) */
    div[data-testid="stNumberInput"] button,
    div[data-testid="stNumberInputStepDown"] button,
    div[data-testid="stNumberInputStepUp"] button {
        padding: 0.2rem 0.55rem !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }

    /* Hover universal sin fondo negro */
    div.stButton > button:hover,
    div.stDownloadButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover,
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover,
    button[data-testid="baseButton-primary"]:hover,
    button[data-testid="baseButton-secondary"]:hover,
    [data-testid="stSidebar"] div.stButton > button:hover,
    [data-testid="stForm"] div.stButton > button:hover,
    div[data-testid="stNumberInput"] button:hover,
    div[data-testid="stNumberInputStepDown"] button:hover,
    div[data-testid="stNumberInputStepUp"] button:hover,
    div[data-testid="stMultiSelect"] [data-baseweb="tag"]:hover,
    [data-baseweb="tag"]:hover {
        background: #6D28D9 !important;
        background-color: #6D28D9 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border-color: #6D28D9 !important;
        box-shadow: 0 6px 20px rgba(109, 40, 217, 0.45) !important;
        transform: translateY(-1px) !important;
    }

    /* Active y Focus universal sin fondo negro residual */
    div.stButton > button:active,
    div.stButton > button:focus,
    div.stButton > button:focus:not(:focus-visible),
    div.stDownloadButton > button:active,
    div.stDownloadButton > button:focus,
    div[data-testid="stFormSubmitButton"] > button:active,
    div[data-testid="stFormSubmitButton"] > button:focus,
    button[kind="primary"]:active,
    button[kind="primary"]:focus,
    button[kind="secondary"]:active,
    button[kind="secondary"]:focus,
    button[data-testid="baseButton-primary"]:active,
    button[data-testid="baseButton-primary"]:focus,
    button[data-testid="baseButton-secondary"]:active,
    button[data-testid="baseButton-secondary"]:focus,
    [data-testid="stSidebar"] div.stButton > button:active,
    [data-testid="stSidebar"] div.stButton > button:focus,
    div[data-testid="stNumberInput"] button:active,
    div[data-testid="stNumberInput"] button:focus,
    div[data-testid="stNumberInputStepDown"] button:active,
    div[data-testid="stNumberInputStepUp"] button:active,
    div[data-testid="stMultiSelect"] [data-baseweb="tag"]:active,
    [data-baseweb="tag"]:active {
        background: #5B21B6 !important;
        background-color: #5B21B6 !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        border-color: #5B21B6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.4) !important;
    }

    /* Texto e iconos en blanco puro dentro de todos los botones y píldoras */
    button p,
    button span,
    button div,
    div.stButton > button *,
    div.stDownloadButton > button *,
    div[data-testid="stFormSubmitButton"] > button *,
    div[data-testid="stNumberInput"] button *,
    div[data-testid="stMultiSelect"] [data-baseweb="tag"] *,
    [data-baseweb="tag"] *,
    [data-baseweb="tag"] span,
    [data-baseweb="tag"] svg {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    [data-baseweb="tag"] [role="button"],
    [data-baseweb="tag"] [role="presentation"] {
        background: transparent !important;
        background-color: transparent !important;
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
    }

    /* Pestañas de visualización (Tabs) */
    button[data-baseweb="tab"] {
        border-radius: 8px 8px 0 0 !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.1rem !important;
        color: #7C3AED !important;
        -webkit-text-fill-color: #7C3AED !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #F3E8FF !important;
        border-bottom: 3px solid #7C3AED !important;
        color: #5B21B6 !important;
        -webkit-text-fill-color: #5B21B6 !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: #7C3AED !important;
    }

    /* Tarjetas de sección (NEM Cards) */
    .nem-card {
        background-color: #FFFFFF !important;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1.5px solid #EDE9FE;
        box-shadow: 0 4px 16px rgba(124, 58, 237, 0.05);
        margin-bottom: 1.5rem;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .nem-card:hover {
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.1);
        border-color: #8B5CF6;
    }

    .nem-card-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        border-bottom: 2px solid #EDE9FE;
        padding-bottom: 0.75rem;
        margin-bottom: 1.25rem;
    }

    /* Píldoras de Ejes Articuladores */
    .eje-pill {
        display: inline-block;
        background-color: #F3E8FF;
        border: 1px solid #8B5CF6;
        border-radius: 20px;
        padding: 4px 12px;
        margin: 4px;
        font-size: 0.85rem;
        color: #5B21B6 !important;
        font-weight: 600;
    }

    /* Insignias / Badges */
    .badge-sep {
        background: #F3E8FF;
        color: #5B21B6;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.8rem;
        border: 1px solid #8B5CF6;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }

    /* Status de API Key */
    .key-status-ok {
        background-color: #F3E8FF;
        color: #5B21B6;
        border: 1px solid #8B5CF6;
        padding: 0.35rem 0.75rem;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        display: inline-block;
    }

    .key-status-warn {
        background-color: #FDF2F8;
        color: #9D174D;
        border: 1px solid #FBCFE8;
        padding: 0.35rem 0.75rem;
        border-radius: 8px;
        font-size: 0.82rem;
        font-weight: 600;
        display: inline-block;
    }

    /* Área de arrastre de archivos (file_uploader) */
    section[data-testid="stFileUploadDropzone"],
    div[data-testid="stFileUploader"] section {
        border: 2px dashed #8B5CF6 !important;
        border-radius: 14px !important;
        background-color: #F3E8FF !important;
        transition: all 0.3s ease !important;
    }

    section[data-testid="stFileUploadDropzone"]:hover,
    div[data-testid="stFileUploader"] section:hover {
        border-color: #7C3AED !important;
        background-color: #FAF5FF !important;
        box-shadow: 0 0 16px rgba(124, 58, 237, 0.2) !important;
    }

    /* Reproductor de YouTube embebido (st.components.v1.iframe) */
    [data-testid="stSidebar"] [data-testid="stIFrame"],
    [data-testid="stSidebar"] iframe.stIFrame,
    [data-testid="stSidebar"] iframe {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1.5px solid #8B5CF6 !important;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.18) !important;
        margin-top: 0.35rem !important;
        margin-bottom: 0.5rem !important;
        background-color: #000000 !important;
        display: block !important;
        width: 100% !important;
    }

    /* =======================================================
       5. OPTIMIZACIÓN Y DISEÑO RESPONSIVO MÓVIL (SMARTPHONES Y TABLETS)
       ======================================================= */

    /* Fluidez global y prevención estricta de barras de desplazamiento horizontal */
    html, body, .stApp, [data-testid="stAppViewContainer"] {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }

    /* Tablas responsivas con desplazamiento táctil horizontal suave */
    .nem-card table,
    div[data-testid="stMarkdownContainer"] table,
    table {
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        border-collapse: collapse !important;
        margin-bottom: 1rem !important;
    }

    /* Pestañas (Tabs) con desplazamiento táctil horizontal fluido */
    div[data-baseweb="tab-list"] {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        flex-wrap: nowrap !important;
        gap: 0.35rem !important;
    }

    button[data-baseweb="tab"] {
        white-space: nowrap !important;
        flex-shrink: 0 !important;
    }

    /* --- PANTALLAS MEDIANAS Y TABLETS (<= 992px) --- */
    @media (max-width: 992px) {
        .block-container,
        [data-testid="stMainBlockContainer"] {
            padding-left: 1.25rem !important;
            padding-right: 1.25rem !important;
            max-width: 100% !important;
        }

        .nem-card {
            padding: 1.25rem !important;
        }
    }

    /* --- SMARTPHONES Y PANTALLAS PEQUEÑAS (<= 768px) --- */
    @media (max-width: 768px) {
        /* 1. Ancho completo al 100% sin desbordamiento */
        .block-container,
        [data-testid="stMainBlockContainer"] {
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            max-width: 100% !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }

        /* Formularios, tarjetas y cuadros al 100% de ancho */
        [data-testid="stForm"],
        .nem-card {
            width: 100% !important;
            max-width: 100% !important;
            padding: 1rem 0.85rem !important;
            border-radius: 14px !important;
            box-sizing: border-box !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }

        /* Apilado automático de columnas en pantallas móviles */
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 0.65rem !important;
        }

        div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }

        /* Insignias escolares en móviles */
        .badge-sep {
            width: 100% !important;
            display: flex !important;
            align-items: center !important;
            box-sizing: border-box !important;
            padding: 0.45rem 0.75rem !important;
            font-size: 0.84rem !important;
            margin-bottom: 0.25rem !important;
        }

        /* 2. Barra lateral responsiva en dispositivos móviles */
        [data-testid="stSidebar"] {
            max-width: 88vw !important;
            width: 88vw !important;
            box-sizing: border-box !important;
        }

        [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
        }

        /* Reproductor Sound en barra lateral móvil */
        [data-testid="stSidebar"] [data-testid="stIFrame"],
        [data-testid="stSidebar"] iframe.stIFrame,
        [data-testid="stSidebar"] iframe {
            width: 100% !important;
            max-width: 100% !important;
            height: 160px !important;
            box-sizing: border-box !important;
        }

        /* 3. Tipografías adaptativas para evitar encimamientos */
        h1 {
            font-size: 1.5rem !important;
            line-height: 1.25 !important;
            margin-bottom: 0.65rem !important;
        }

        h2, .login-header-title {
            font-size: 1.3rem !important;
            line-height: 1.3 !important;
        }

        h3, .nem-card-title {
            font-size: 1.15rem !important;
            line-height: 1.3 !important;
        }

        h4 {
            font-size: 1.02rem !important;
            line-height: 1.3 !important;
        }

        p, span, label, div {
            line-height: 1.45 !important;
        }

        /* Inputs y campos con tamaño táctil cómodo (16px evita auto-zoom en iOS Safari) */
        input,
        textarea,
        select,
        div.stTextInput input,
        div.stTextArea textarea,
        div[data-testid="stTextInput"] input,
        div[data-testid="stTextArea"] textarea,
        div[data-baseweb="input"] input,
        div[data-baseweb="select"] input {
            font-size: 16px !important;
            min-height: 46px !important;
            box-sizing: border-box !important;
        }

        /* Botones táctiles principales con altura y padding generoso (área táctil >= 48px) */
        div.stButton > button,
        div.stDownloadButton > button,
        div[data-testid="stFormSubmitButton"] > button {
            min-height: 48px !important;
            padding: 0.75rem 1.15rem !important;
            font-size: 0.98rem !important;
            width: 100% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            touch-action: manipulation !important;
            box-sizing: border-box !important;
        }

        /* Píldoras de multiselect fáciles de pulsar */
        div[data-testid="stMultiSelect"] [data-baseweb="tag"],
        .stMultiSelect [data-baseweb="tag"],
        [data-baseweb="tag"] {
            padding: 6px 12px !important;
            font-size: 0.88rem !important;
            min-height: 32px !important;
            margin: 3px !important;
            display: inline-flex !important;
            align-items: center !important;
        }

        /* Pestañas adaptadas para pantalla táctil */
        button[data-baseweb="tab"] {
            padding: 0.65rem 0.95rem !important;
            font-size: 0.88rem !important;
            min-height: 44px !important;
        }
    }

    /* --- PANTALLAS EXTRA PEQUEÑAS (<= 480px) --- */
    @media (max-width: 480px) {
        .block-container,
        [data-testid="stMainBlockContainer"] {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }

        h1 {
            font-size: 1.35rem !important;
        }

        .login-header-title {
            font-size: 1.25rem !important;
        }

        .nem-card {
            padding: 0.85rem 0.65rem !important;
        }
    }

    /* =======================================================
       MENSAJE DE ESTADO: HISTORIAL VACÍO Y GESTOR DE ARCHIVOS
       Garantiza contraste óptimo y nitidez en temas claros (#374151) y oscuros (#F3E8FF)
       ======================================================= */
    .empty-history-box {
        background-color: #F8FAFC !important;
        border: 1.5px solid #CBD5E1 !important;
        border-left: 4px solid #7C3AED !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        margin: 8px 0 !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    }

    .empty-history-box * {
        background-color: transparent !important;
    }

    .empty-history-title {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        font-weight: 700 !important;
        font-size: 0.84rem !important;
        margin-bottom: 3px !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
    }

    .empty-history-text {
        color: #374151 !important;
        -webkit-text-fill-color: #374151 !important;
        font-size: 0.78rem !important;
        font-weight: 500 !important;
        line-height: 1.45 !important;
    }

    /* En expanders oscuros de la barra lateral (#1E1B4B), estilo de tarjeta oscura con alto contraste */
    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] .empty-history-box {
        background: #2D1B4E !important;
        background-color: #2D1B4E !important;
        border: 1.5px solid #8B5CF6 !important;
        border-left: 4px solid #C084FC !important;
        box-shadow: 0 4px 16px rgba(124, 58, 237, 0.22) !important;
    }

    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] .empty-history-title,
    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] .empty-history-title * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] .empty-history-text,
    [data-testid="stSidebar"] div[data-testid="stExpanderDetails"] .empty-history-text * {
        color: #F3E8FF !important;
        -webkit-text-fill-color: #F3E8FF !important;
    }

    /* Soporte modo oscuro global */
    @media (prefers-color-scheme: dark) {
        .empty-history-box {
            background: linear-gradient(135deg, #2E1065 0%, #1E1B4B 100%) !important;
            background-color: #2E1065 !important;
            border-color: #8B5CF6 !important;
            border-left: 4px solid #C084FC !important;
        }
        .empty-history-title, .empty-history-title * {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        .empty-history-text, .empty-history-text * {
            color: #F3E8FF !important;
            -webkit-text-fill-color: #F3E8FF !important;
        }
    }

    [data-theme="dark"] .empty-history-box {
        background: linear-gradient(135deg, #2E1065 0%, #1E1B4B 100%) !important;
        background-color: #2E1065 !important;
        border-color: #8B5CF6 !important;
        border-left: 4px solid #C084FC !important;
    }
    [data-theme="dark"] .empty-history-title, [data-theme="dark"] .empty-history-title * {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    /* =======================================================
       REDISEÑO MINIMALISTA: PESTAÑAS DÍA POR DÍA Y TOOLBAR COMPACTA
       ======================================================= */
    /* Barra de navegación de pestañas con scroll horizontal táctil suave */
    div[data-baseweb="tab-list"],
    .stTabs [data-baseweb="tab-list"] {
        overflow-x: auto !important;
        flex-wrap: nowrap !important;
        scrollbar-width: thin !important;
        -webkit-overflow-scrolling: touch !important;
        border-bottom: 2px solid #E2E8F0 !important;
        gap: 6px !important;
        padding-bottom: 4px !important;
        margin-bottom: 12px !important;
    }

    button[data-baseweb="tab"] {
        white-space: nowrap !important;
        flex-shrink: 0 !important;
        padding: 8px 16px !important;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        border-radius: 8px 8px 0 0 !important;
        color: #4B5563 !important;
        transition: all 0.2s ease !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #EDE9FE !important;
        color: #6D28D9 !important;
        -webkit-text-fill-color: #6D28D9 !important;
        border-bottom: 3px solid #7C3AED !important;
        font-weight: 700 !important;
    }

    /* Tarjeta contenedor de la barra de acciones (Toolbar) */
    .action-toolbar-box {
        background: linear-gradient(180deg, #FFFFFF 0%, #FAF5FF 100%) !important;
        border: 1.5px solid #C4B5FD !important;
        border-radius: 14px !important;
        padding: 16px 18px !important;
        box-shadow: 0 4px 18px rgba(124, 58, 237, 0.08) !important;
        margin: 16px 0 !important;
    }

    /* Tarjeta modular por día (Día por Día) */
    .day-card-container {
        background: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04) !important;
    }

    .day-moment-box {
        background: #F8FAFC !important;
        border-left: 4px solid #7C3AED !important;
        border-radius: 8px !important;
        padding: 12px 14px !important;
        margin: 8px 0 !important;
    }

    .day-moment-title {
        font-weight: 700 !important;
        font-size: 0.86rem !important;
        color: #4C1D95 !important;
        margin-bottom: 4px !important;
        display: flex !important;
        align-items: center !important;
        gap: 6px !important;
    }

    .day-moment-text {
        font-size: 0.84rem !important;
        color: #334151 !important;
        line-height: 1.5 !important;
    }

    /* Adaptación modo oscuro */
    @media (prefers-color-scheme: dark) {
        div[data-baseweb="tab-list"],
        .stTabs [data-baseweb="tab-list"] {
            border-bottom-color: #4C1D95 !important;
        }
        button[data-baseweb="tab"] {
            color: #C4B5FD !important;
            -webkit-text-fill-color: #C4B5FD !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            background-color: #2E1065 !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            border-bottom-color: #A78BFA !important;
        }
        .action-toolbar-box {
            background: linear-gradient(180deg, #1E1B4B 0%, #2E1065 100%) !important;
            border-color: #7C3AED !important;
            box-shadow: 0 4px 18px rgba(124, 58, 237, 0.25) !important;
        }
        .day-card-container {
            background: #1E1B4B !important;
            border-color: #4C1D95 !important;
        }
        .day-moment-box {
            background: #2D1B4E !important;
            border-left-color: #C084FC !important;
        }
        .day-moment-title {
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        .day-moment-text {
            color: #F3E8FF !important;
            -webkit-text-fill-color: #F3E8FF !important;
        }
    }

    [data-theme="dark"] .action-toolbar-box {
        background: linear-gradient(180deg, #1E1B4B 0%, #2E1065 100%) !important;
        border-color: #7C3AED !important;
    }
    [data-theme="dark"] .day-card-container {
        background: #1E1B4B !important;
        border-color: #4C1D95 !important;
    }
    [data-theme="dark"] .day-moment-box {
        background: #2D1B4E !important;
        border-left-color: #C084FC !important;
    }
    [data-theme="dark"] .day-moment-title {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    [data-theme="dark"] .day-moment-text {
        color: #F3E8FF !important;
        -webkit-text-fill-color: #F3E8FF !important;
    }

    /* =======================================================
       TARJETAS Y JERARQUÍA VISUAL: CUADERNILLO PROFA KEMPIS
       Textos en #1F2937 con alto contraste y soporte modo oscuro
       ======================================================= */
    .kempis-header-card {
        background: linear-gradient(135deg, #FAF5FF 0%, #F5F3FF 100%) !important;
        border: 1.5px solid #DDD6FE !important;
        border-left: 5px solid #7C3AED !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        margin-bottom: 16px !important;
        box-shadow: 0 2px 10px rgba(124, 58, 237, 0.05) !important;
    }

    .kempis-act-card {
        background: #FFFFFF !important;
        border: 1.5px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 16px 18px !important;
        margin-bottom: 14px !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    }

    .kempis-act-card:hover {
        border-color: #C4B5FD !important;
        box-shadow: 0 4px 14px rgba(124, 58, 237, 0.1) !important;
    }

    .kempis-anexo-box {
        background: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-left: 3.5px solid #7C3AED !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        margin: 10px 0 !important;
    }

    .kempis-efemeride-card {
        background: #FFFBEB !important;
        border: 1.5px solid #FDE68A !important;
        border-left: 5px solid #D97706 !important;
        border-radius: 12px !important;
        padding: 16px 18px !important;
        margin-top: 10px !important;
        margin-bottom: 14px !important;
    }

    @media (prefers-color-scheme: dark) {
        .kempis-header-card {
            background: linear-gradient(135deg, #2E1065 0%, #1E1B4B 100%) !important;
            border-color: #7C3AED !important;
        }
        .kempis-act-card {
            background: #1E1B4B !important;
            border-color: #4C1D95 !important;
        }
        .kempis-act-card * {
            color: #F9FAFB !important;
            -webkit-text-fill-color: #F9FAFB !important;
        }
        .kempis-anexo-box {
            background: #2D1B4E !important;
            border-color: #6D28D9 !important;
            border-left-color: #C084FC !important;
        }
        .kempis-anexo-box * {
            color: #F3E8FF !important;
            -webkit-text-fill-color: #F3E8FF !important;
        }
        .kempis-efemeride-card {
            background: #3B2A10 !important;
            border-color: #B45309 !important;
            border-left-color: #F59E0B !important;
        }
        .kempis-efemeride-card * {
            color: #FEF3C7 !important;
            -webkit-text-fill-color: #FEF3C7 !important;
        }
    }

    [data-theme="dark"] .kempis-header-card {
        background: linear-gradient(135deg, #2E1065 0%, #1E1B4B 100%) !important;
        border-color: #7C3AED !important;
    }
    [data-theme="dark"] .kempis-act-card {
        background: #1E1B4B !important;
        border-color: #4C1D95 !important;
    }
    [data-theme="dark"] .kempis-act-card * {
        color: #F9FAFB !important;
        -webkit-text-fill-color: #F9FAFB !important;
    }
    [data-theme="dark"] .kempis-anexo-box {
        background: #2D1B4E !important;
        border-color: #6D28D9 !important;
        border-left-color: #C084FC !important;
    }
    [data-theme="dark"] .kempis-anexo-box * {
        color: #F3E8FF !important;
        -webkit-text-fill-color: #F3E8FF !important;
    }
    [data-theme="dark"] .kempis-efemeride-card {
        background: #3B2A10 !important;
        border-color: #B45309 !important;
        border-left-color: #F59E0B !important;
    }
    [data-theme="dark"] .kempis-efemeride-card * {
        color: #FEF3C7 !important;
        -webkit-text-fill-color: #FEF3C7 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# GESTIÓN DE ESTADO (SESSION STATE)
# ==========================================
if "widget_key" not in st.session_state:
    st.session_state.widget_key = 0

if "planeacion_generada" not in st.session_state:
    st.session_state.planeacion_generada = None

if "prompt_enviado" not in st.session_state:
    st.session_state.prompt_enviado = None

if "archivos_procesados" not in st.session_state:
    st.session_state.archivos_procesados = {}

if "programa_sintetico_texto" not in st.session_state:
    st.session_state.programa_sintetico_texto = ""

if "query_busqueda" not in st.session_state:
    st.session_state.query_busqueda = ""

if "resultados_busqueda_gratis" not in st.session_state:
    st.session_state.resultados_busqueda_gratis = []

if "contexto_url" not in st.session_state:
    st.session_state.contexto_url = ""

MESES_2026 = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]
DIAS_HABIL_NOMBRES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

# ==========================================
# CALENDARIO OFICIAL SEP: 37 SEMANAS LECTIVAS (185 DÍAS), PERIODOS VACACIONALES Y CTE
# ==========================================
PERIODOS_VACACIONALES_SEP = [
    {
        "nombre": "Vacaciones de Invierno",
        "inicio": datetime.date(2026, 12, 21),
        "fin": datetime.date(2027, 1, 8),
        "tipo": "invierno",
        "icono": "❄️"
    },
    {
        "nombre": "Vacaciones de Semana Santa",
        "inicio": datetime.date(2027, 3, 22),
        "fin": datetime.date(2027, 4, 2),
        "tipo": "semana_santa",
        "icono": "🌿"
    },
    {
        "nombre": "Receso de Verano",
        "inicio": datetime.date(2027, 7, 16),
        "fin": datetime.date(2027, 8, 27),
        "tipo": "verano",
        "icono": "🏖️"
    }
]

FECHAS_CTE_OFICIALES = {
    datetime.date(2026, 9, 25): "1ª Sesión Ordinaria CTE",
    datetime.date(2026, 10, 30): "2ª Sesión Ordinaria CTE",
    datetime.date(2026, 11, 27): "3ª Sesión Ordinaria CTE",
    datetime.date(2027, 1, 29): "4ª Sesión Ordinaria CTE",
    datetime.date(2027, 2, 26): "5ª Sesión Ordinaria CTE",
    datetime.date(2027, 3, 26): "6ª Sesión Ordinaria CTE",
    datetime.date(2027, 5, 28): "7ª Sesión Ordinaria CTE",
    datetime.date(2027, 6, 25): "8ª Sesión Ordinaria CTE"
}

def es_fecha_vacaciones(d_obj: datetime.date):
    for v in PERIODOS_VACACIONALES_SEP:
        if v["inicio"] <= d_obj <= v["fin"]:
            return v
    return None

def construir_catalogo_sep_2026():
    """
    Construye las 37 semanas escolares oficiales (185 días lectivos de clase)
    del ciclo escolar SEP 2026-2027.
    Sincroniza periodos lectivos, vacaciones oficiales (Invierno, Semana Santa y Verano)
    y sesiones de Consejo Técnico Escolar (CTE).
    Mapea bi-direccionalmente:
      - número de semana (1 a 37) -> fechas, mes y sesión CTE
      - fecha (mes, día) y (año, mes, día) -> número de semana (1 a 37)
    """
    catalogo_por_semana = {}
    catalogo_por_fecha = {}

    lunes_inicio_ciclo = datetime.date(2026, 8, 31)
    curr = lunes_inicio_ciclo
    s_num = 1

    while s_num <= 37:
        viernes = curr + datetime.timedelta(days=4)
        # Si la semana completa cae en periodo vacacional oficial SEP, saltarla
        if es_fecha_vacaciones(curr) and es_fecha_vacaciones(viernes):
            curr += datetime.timedelta(weeks=1)
            continue

        dias_semana = []
        tiene_cte = False
        cte_nombre = ""

        for i, nom in enumerate(DIAS_HABIL_NOMBRES):
            d_obj = curr + datetime.timedelta(days=i)
            m_nom = MESES_2026[d_obj.month - 1]
            es_cte = d_obj in FECHAS_CTE_OFICIALES
            if es_cte:
                tiene_cte = True
                cte_nombre = FECHAS_CTE_OFICIALES[d_obj]

            dias_semana.append({
                "nombre_dia": nom,
                "date": d_obj,
                "dia_num": d_obj.day,
                "mes_num": d_obj.month,
                "mes_nombre": m_nom,
                "año": d_obj.year,
                "es_cte": es_cte,
                "cte_nombre": FECHAS_CTE_OFICIALES.get(d_obj, ""),
                "fecha_corta": f"{nom} {d_obj.day}/{m_nom[:3]}",
                "fecha_completa": f"{nom} {d_obj.day} de {m_nom} de {d_obj.year}"
            })
            catalogo_por_fecha[(d_obj.month, d_obj.day)] = s_num
            catalogo_por_fecha[(d_obj.year, d_obj.month, d_obj.day)] = s_num

        m_rep = MESES_2026[curr.month - 1]
        catalogo_por_semana[s_num] = {
            "semana": s_num,
            "lunes": curr,
            "viernes": viernes,
            "mes_idx": curr.month,
            "mes_nombre": m_rep,
            "año": curr.year,
            "tiene_cte": tiene_cte,
            "cte_nombre": cte_nombre,
            "rango_str": f"{curr.day} {MESES_2026[curr.month-1][:3]} al {viernes.day} {MESES_2026[viernes.month-1][:3]}",
            "dias_habil": dias_semana
        }

        s_num += 1
        curr += datetime.timedelta(weeks=1)

    return catalogo_por_semana, catalogo_por_fecha

CATALOGO_SEMANAS_SEP, CATALOGO_FECHAS_SEP = construir_catalogo_sep_2026()

_hoy = datetime.date.today()
_sem_detectada_hoy = (
    CATALOGO_FECHAS_SEP.get((_hoy.year, _hoy.month, _hoy.day))
    or CATALOGO_FECHAS_SEP.get((_hoy.month, _hoy.day))
    or 8
)
_sem_init = max(1, min(37, int(_sem_detectada_hoy)))
_info_init = CATALOGO_SEMANAS_SEP.get(_sem_init, CATALOGO_SEMANAS_SEP[1])
_mes_init = _info_init["mes_nombre"]
_dias_map = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes"}
_dia_init = _dias_map.get(_hoy.weekday(), "Lunes")

if "cal_mes_nombre" not in st.session_state:
    st.session_state.cal_mes_nombre = _mes_init

if "cal_semana_escolar" not in st.session_state:
    st.session_state.cal_semana_escolar = _sem_init

if "cal_sem_idx" not in st.session_state:
    st.session_state.cal_sem_idx = 0

if "semana_activa_previa" not in st.session_state:
    st.session_state.semana_activa_previa = _sem_init

if "dia_activo_pestaña" not in st.session_state:
    st.session_state.dia_activo_pestaña = _dia_init

if "dias_seleccionados" not in st.session_state or not st.session_state.dias_seleccionados:
    st.session_state.dias_seleccionados = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

if "dias_fechas" not in st.session_state or not st.session_state.dias_fechas:
    st.session_state.dias_fechas = {
        d["nombre_dia"]: d["fecha_completa"].upper() for d in _info_init["dias_habil"]
    }

def limpiar_estado_planeacion(nueva_semana=None, reset_completo=False):
    """
    Limpia por completo el estado de generación, actividades previas y textos de la sesión
    para evitar el arrastre de datos entre semanas o al iniciar una nueva planeación.
    Garantiza que la nueva ejecución tome exclusivamente los datos institucionales oficiales
    (Escuela Revolución Social de 1910, 6° 'A', problematizaciones y los 4 Campos Formativos).
    """
    # 1. Limpieza de actividades generadas y prompts previos
    st.session_state.planeacion_generada = None
    st.session_state.prompt_enviado = None

    # 2. Limpieza de archivos procesados, referencias web y búsquedas
    st.session_state.archivos_procesados = {}
    st.session_state.programa_sintetico_texto = ""
    st.session_state["programa_sintetico_subido"] = False
    st.session_state["nombre_archivo_programa"] = ""
    st.session_state["es_programa_oficial_fase5"] = False
    st.session_state["pda_extraidos_programa"] = []
    st.session_state.query_busqueda = ""
    st.session_state.resultados_busqueda_gratis = []
    st.session_state.query_busqueda_gratis = ""
    st.session_state.query_busqueda_enriquecida = ""
    st.session_state.contexto_url = ""

    # 3. Limpieza de redacciones manuales y borradores
    st.session_state["contenidos"] = ""
    st.session_state["contenido_custom"] = ""
    st.session_state["custom_pda"] = ""
    st.session_state["directrices"] = ""
    st.session_state["url_referencia"] = ""

    if reset_completo:
        st.session_state.widget_key += 1
        # Limpiar cualquier clave existente en session_state vinculada con widgets dinámicos
        for k in list(st.session_state.keys()):
            for prefix in [
                "dias_", "campos_", "ejes_", "libros_", "pda_",
                "contenidos_", "custom_contenido_", "custom_pda_",
                "directrices_", "url_referencia_", "uploader_",
                "semana_", "periodo_", "chk_dia_", "chk_pda_manual_"
            ]:
                if k.startswith(prefix) and k != "semana_activa_previa":
                    del st.session_state[k]
        st.session_state.cal_mes_nombre = _mes_init
        st.session_state.cal_semana_escolar = _sem_init
        st.session_state.cal_sem_idx = 0
        st.session_state.semana_activa_previa = _sem_init
        st.session_state.dia_activo_pestaña = _dia_init
        st.session_state.dias_seleccionados = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        st.session_state.dias_fechas = {
            d["nombre_dia"]: d["fecha_completa"].upper() for d in _info_init["dias_habil"]
        }
        st.session_state["aviso_nueva_planeacion"] = True
    elif nueva_semana is not None:
        sem_val = max(1, min(37, int(nueva_semana)))
        st.session_state.cal_semana_escolar = sem_val
        st.session_state.semana_activa_previa = sem_val
        info_n = CATALOGO_SEMANAS_SEP.get(sem_val, CATALOGO_SEMANAS_SEP[1])
        st.session_state.cal_mes_nombre = info_n["mes_nombre"]
        st.session_state.dias_seleccionados = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        st.session_state.dias_fechas = {
            d["nombre_dia"]: d["fecha_completa"].upper() for d in info_n["dias_habil"]
        }
        if "dia_activo_pestaña" not in st.session_state or st.session_state.dia_activo_pestaña not in st.session_state.dias_seleccionados:
            st.session_state.dia_activo_pestaña = "Lunes"
        # Limpiar claves de widgets que guardan redacciones manuales, selecciones o archivos
        for k in list(st.session_state.keys()):
            for prefix in [
                "contenidos_", "custom_contenido_", "custom_pda_",
                "url_referencia_", "uploader_", "chk_pda_manual_",
                "directrices_", "pda_", "chk_dia_"
            ]:
                if k.startswith(prefix):
                    del st.session_state[k]

def limpiar_todo_callback():
    """Reinicia todas las variables de estado y rota las llaves dinámicas para empezar desde cero."""
    limpiar_estado_planeacion(reset_completo=True)

def cargar_planeacion_guardada(planeacion_id: int) -> bool:
    """
    Restaura por completo una planeación previamente guardada en SQLite,
    recuperando la semana escolar, días, campos formativos, metodología,
    ejes articuladores, PDA, libros de texto, directrices del programa analítico
    y la redacción de secuencias didácticas generadas sin pérdida de datos.
    """
    plan = obtener_planeacion_por_id(planeacion_id)
    if not plan:
        return False
    
    # 1. Limpiar claves de widgets dinámicos anteriores antes de asignar los nuevos
    for k in list(st.session_state.keys()):
        for prefix in [
            "dias_", "campos_", "ejes_", "libros_", "pda_",
            "contenidos_", "custom_contenido_", "custom_pda_",
            "directrices_", "url_referencia_", "uploader_",
            "semana_", "periodo_", "chk_dia_", "chk_pda_manual_",
            "inp_nombre_archivo_", "sel_categoria_ruta_"
        ]:
            if k.startswith(prefix) and k != "semana_activa_previa":
                del st.session_state[k]

    # 2. Incrementar la llave de widgets para forzar regeneración limpia de la UI
    st.session_state.widget_key += 1
    wk = st.session_state.widget_key

    # 3. Restaurar semana y calendario oficial
    sem = int(plan["semana"])
    st.session_state.cal_semana_escolar = sem
    st.session_state.semana_activa_previa = sem
    info_sem = CATALOGO_SEMANAS_SEP.get(sem, {})
    if info_sem:
        st.session_state.cal_mes_nombre = info_sem.get("mes_nombre", "Octubre")
    
    # 4. Restaurar días y fechas
    dias_rest = plan.get("dias_seleccionados") or ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    st.session_state.dias_seleccionados = dias_rest
    st.session_state.dias_fechas = plan.get("dias_fechas") or {}

    # 5. Restaurar planeación generada y prompt
    st.session_state.planeacion_generada = plan.get("planeacion_generada") or None
    st.session_state.prompt_enviado = plan.get("prompt_enviado") or None

    # 6. Restaurar textos de referencia, directrices y metadatos de archivo
    st.session_state["directrices"] = plan.get("directrices") or ""
    st.session_state["url_referencia"] = plan.get("url_referencia") or ""
    st.session_state.archivos_procesados = {}
    if plan.get("contenidos_pda"):
        st.session_state["pda_cargados"] = plan["contenidos_pda"]

    nom_arch = plan.get("nombre_archivo") or f"Planeacion_Semana_{sem}"
    cat_arch = plan.get("categoria_ruta") or ("Trimestre 1 (Diagnóstico e Inicio)" if sem <= 13 else ("Trimestre 2 (Desarrollo y Proyectos)" if sem <= 26 else "Trimestre 3 (Consolidación y Cierre)"))
    st.session_state["nombre_archivo_actual"] = nom_arch
    st.session_state["categoria_ruta_actual"] = cat_arch

    # 7. Asignar valores cargados a los widgets con la nueva widget_key
    st.session_state[f"modo_cal_sel_{wk}"] = "Semana SEP (1 a 37)"
    st.session_state[f"sel_semana_sep_{wk}"] = sem
    st.session_state[f"inp_nombre_archivo_{wk}"] = nom_arch
    st.session_state[f"sel_categoria_ruta_{wk}"] = cat_arch
    st.session_state[f"directrices_{wk}"] = plan.get("directrices") or ""
    st.session_state[f"metodologia_{wk}"] = plan.get("metodologia") or "Aprendizaje Basado en Proyectos Comunitarios"
    st.session_state[f"num_sesiones_{wk}"] = int(plan.get("num_sesiones", len(dias_rest)))
    st.session_state[f"libros_{wk}"] = plan.get("libros_seleccionados") or []
    st.session_state[f"campos_{wk}"] = plan.get("campos_formativos") or CAMPOS_FORMATIVOS
    st.session_state[f"ejes_{wk}"] = plan.get("ejes_articuladores") or ["Pensamiento crítico", "Apropiación de las culturas a través de la lectura y la escritura", "Vida saludable"]
    for nom_d in DIAS_HABIL_NOMBRES:
        st.session_state[f"chk_dia_{nom_d}_{wk}"] = (nom_d in dias_rest)

    if plan.get("contenidos_pda") and len(plan["contenidos_pda"]) == 1:
        first_pda = plan["contenidos_pda"][0]
        if first_pda.get("contenido"):
            st.session_state[f"contenidos_{wk}"] = first_pda.get("contenido", "")
        if first_pda.get("pda"):
            st.session_state[f"custom_pda_{wk}"] = first_pda.get("pda", "")

    # 8. Sincronizar hash para evitar re-escritura inmediata
    st.session_state["ultimo_hash_guardado"] = plan.get("hash_contenido")
    st.session_state["aviso_planeacion_cargada"] = f"📄 {nom_arch} — Semana {sem} ({cat_arch})"
    return True

# ==========================================
# ==========================================
# GESTIÓN Y CARGA DE CREDENCIALES (STREAMLIT SECRETS)
# ==========================================
def cargar_credenciales():
    """
    Carga credenciales desde st.secrets de manera flexible y mutable,
    garantizando compatibilidad total con Streamlit Cloud y entornos locales.
    """
    credentials = {"usernames": {}}
    cookie_config = {
        "name": "planeaciones_nem_auth_cookie",
        "key": "nem_auth_secret_signing_key_2026",
        "expiry_days": 30.0
    }

    if hasattr(st, "secrets"):
        # Formato estándar de streamlit-authenticator: [credentials.usernames.<usuario>]
        if "credentials" in st.secrets and "usernames" in st.secrets["credentials"]:
            for uname, udata in st.secrets["credentials"]["usernames"].items():
                credentials["usernames"][str(uname).lower()] = {
                    "name": udata.get("name", str(uname)),
                    "email": udata.get("email", ""),
                    "password": str(udata.get("password", ""))
                }
        # Formato directo: [auth] con username, name, email, password
        elif "auth" in st.secrets:
            auth_sec = st.secrets["auth"]
            uname = str(auth_sec.get("username", "docente")).lower()
            credentials["usernames"][uname] = {
                "name": auth_sec.get("name", "Docente Primaria"),
                "email": auth_sec.get("email", "docente@escuela.gob.mx"),
                "password": str(auth_sec.get("password", ""))
            }
        # Formato plano en raíz de st.secrets: username, name, email, password
        elif "username" in st.secrets and "password" in st.secrets:
            uname = str(st.secrets.get("username", "docente")).lower()
            credentials["usernames"][uname] = {
                "name": st.secrets.get("name", "Docente Primaria"),
                "email": st.secrets.get("email", "docente@escuela.gob.mx"),
                "password": str(st.secrets.get("password", ""))
            }

        # Configuración de cookie si existe en st.secrets
        if "cookie" in st.secrets:
            cookie_sec = st.secrets["cookie"]
            cookie_config["name"] = cookie_sec.get("name", cookie_config["name"])
            cookie_config["key"] = cookie_sec.get("key", cookie_config["key"])
            cookie_config["expiry_days"] = float(cookie_sec.get("expiry_days", cookie_config["expiry_days"]))

    # Fallback de respaldo por si no se han cargado secrets aún
    if not credentials["usernames"]:
        credentials["usernames"]["docente"] = {
            "name": "Aday Domínguez Domínguez",
            "email": "docente@escuela.gob.mx",
            "password": "$2b$12$Ma3bauQBClsLcIEaCIJHLu/LiGJg3NrGbfGgBbMlfck3TV5o6KVWC"
        }

    return credentials, cookie_config

# Instanciar el autenticador con las credenciales cargadas desde st.secrets
credentials, cookie_config = cargar_credenciales()

authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name=cookie_config["name"],
    cookie_key=cookie_config["key"],
    cookie_expiry_days=cookie_config["expiry_days"]
)

# Renderizar pantalla de login cuando no hay sesión autenticada
if not st.session_state.get("authentication_status"):
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem; margin-bottom: 1.5rem;">
            <div style="display: inline-block; background: linear-gradient(135deg, #7C3AED, #6D28D9); width: 68px; height: 68px; border-radius: 50%; line-height: 68px; font-size: 2.2rem; color: #FFFFFF; box-shadow: 0 6px 18px rgba(124, 58, 237, 0.28);">
                •
            </div>
            <h2 class="login-header-title">
                Planeaciones Escolares NEM
            </h2>
            <p class="login-header-desc">
                Sistema Integral de Intervención Docente • Educación Primaria
            </p>
        </div>
        """, unsafe_allow_html=True)

        authenticator.login(
            location="main",
            fields={
                "Form name": "Acceso al Sistema",
                "Username": "Usuario",
                "Password": "Contraseña",
                "Login": "Iniciar Sesión"
            }
        )

        if st.session_state.get("authentication_status") is False:
            st.error("Usuario o contraseña incorrectos")
        elif st.session_state.get("authentication_status") is None:
            st.info("Por favor ingresa tus credenciales registradas para acceder a la aplicación.")

authentication_status = st.session_state.get("authentication_status")

if authentication_status:
    # BARRA LATERAL (CONFIGURACIÓN INSTITUCIONAL Y GEMINI)
    # ==========================================
    with st.sidebar:
        # Información del docente y botón de cerrar sesión
        st.markdown(f'### <span style="color: #7C3AED; font-size: 1.2rem;">•</span> **{st.session_state.get("name", "Docente")}**', unsafe_allow_html=True)
        st.caption(f"Usuario activo: @{st.session_state.get('username', '')}")
        authenticator.logout('Cerrar sesión', 'sidebar', use_container_width=True)
        st.markdown('---')
        st.button(
            "Nueva Planeación (Limpiar Todo)",
            on_click=limpiar_todo_callback,
            key="btn_nueva_planeacion",
            use_container_width=True,
            type="primary",
            help="Reinicia todos los campos, documentos cargados, búsquedas y selecciones para comenzar una nueva planeación desde cero."
        )

        # Estado de Autoguardado en tiempo real (SQLite)
        user_actual_sb = st.session_state.get("username", "docente")
        stats_cubiertas_sb = obtener_resumen_semanas_cubiertas(user_actual_sb)
        hora_auto_sb = st.session_state.get("ultimo_autoguardado_hora")
        sem_auto_sb = st.session_state.get("ultimo_autoguardado_semana", st.session_state.get("cal_semana_escolar", 20))
        if hora_auto_sb:
            st.markdown(
                f"<div style='background: #ECFDF5; border: 1px solid #10B981; border-radius: 6px; padding: 6px 10px; font-size: 0.78rem; color: #065F46; margin: 6px 0;'>"
                f"🟢 <b>Autoguardado:</b> {hora_auto_sb} (Sem. {sem_auto_sb})<br>"
                f"<span style='font-size: 0.71rem; color: #047857;'>Cambios asegurados en SQLite en tiempo real.</span>"
                f"</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; padding: 6px 10px; font-size: 0.78rem; color: #475569; margin: 6px 0;'>"
                f"💾 <b>Autoguardado activo:</b> Registra en tiempo real en SQLite."
                f"</div>",
                unsafe_allow_html=True
            )

        # Gestor de Archivos / Historial en la barra lateral
        with st.expander("📂 Gestor de Archivos y Planeaciones", expanded=False):
            st.markdown(
                f"<div style='font-size: 0.78rem; margin-bottom: 6px; color: #E0E7FF; font-weight: 500;'>"
                f"📊 <b>Cobertura:</b> {stats_cubiertas_sb['semanas_completas']} de 37 semanas ({stats_cubiertas_sb['porcentaje_avance']}%)"
                f"</div>",
                unsafe_allow_html=True
            )
            lista_historial_sb = listar_planeaciones(user_actual_sb)
            if not lista_historial_sb:
                st.markdown(
                    "<div class='empty-history-box' style='background: #2D1B4E; border: 1.5px solid #8B5CF6; border-left: 4px solid #C084FC; border-radius: 8px; padding: 10px 12px; margin: 8px 0;'>"
                    "<div class='empty-history-title' style='color: #FFFFFF; font-weight: 700; font-size: 0.82rem; margin-bottom: 3px; display: flex; align-items: center; gap: 6px;'>"
                    "<span>📁</span> <span style='color: #FFFFFF;'>No hay planeaciones guardadas aún</span>"
                    "</div>"
                    "<div class='empty-history-text' style='color: #F3E8FF; font-size: 0.77rem; font-weight: 500; line-height: 1.45;'>"
                    "Se guardarán automáticamente con su nombre de archivo al configurar o generar cualquier semana."
                    "</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            else:
                dict_sb_planes = {p["id"]: p for p in lista_historial_sb}
                st.markdown("<div style='font-size:0.75rem; font-weight:700; color:#E0E7FF; margin-top:2px; margin-bottom:2px;'>Cargar Archivo por Nombre:</div>", unsafe_allow_html=True)
                sel_sb_pid = st.selectbox(
                    "Selecciona un archivo guardado:",
                    options=list(dict_sb_planes.keys()),
                    format_func=lambda pid: f"📄 {dict_sb_planes[pid]['nombre_archivo']} (Sem. {dict_sb_planes[pid]['semana']})",
                    key=f"sel_sb_plan_{st.session_state.widget_key}",
                    label_visibility="collapsed"
                )
                if st.button("📂 Abrir Archivo", key=f"btn_sb_open_sel_{st.session_state.widget_key}", use_container_width=True, type="primary"):
                    if sel_sb_pid:
                        cargar_planeacion_guardada(sel_sb_pid)
                        st.rerun()

                st.markdown("<hr style='margin: 8px 0; border: none; border-top: 1px solid #4C1D95;'>", unsafe_allow_html=True)
                st.markdown("<div style='font-size:0.73rem; font-weight:700; color:#C7D2FE; margin-bottom:4px;'>Historial de Archivos Guardados:</div>", unsafe_allow_html=True)
                for p_item in lista_historial_sb:
                    p_id = p_item["id"]
                    tag_estado = "🟢 Lista" if p_item["tiene_plan"] else "📝 Borrador"
                    ver_tag = f" [{p_item['version_nombre']}]" if not p_item["es_autoguardado"] else ""
                    st.markdown(
                        f"<div style='font-size:0.78rem; font-weight:600; margin-top:4px; color:#FFFFFF;'>"
                        f"📄 {p_item['nombre_archivo']}<br>"
                        f"<span style='font-size:0.7rem; color:#DDD6FE; font-weight:bold;'>📁 {p_item['categoria_ruta']}</span> • "
                        f"<span style='font-size:0.7rem; color:#34D399;'>Sem. {p_item['semana']}{ver_tag} ({tag_estado})</span>"
                        f"</div>"
                        f"<div style='font-size:0.68rem; color:#CBD5E1;'>Guardado: {p_item['fecha_guardado']}</div>",
                        unsafe_allow_html=True
                    )
                    col_h1, col_h2 = st.columns([2.2, 1])
                    with col_h1:
                        if st.button("📂 Abrir", key=f"btn_sb_load_{p_id}_{st.session_state.widget_key}", use_container_width=True, help=f"Cargar {p_item['nombre_archivo']}"):
                            cargar_planeacion_guardada(p_id)
                            st.rerun()
                    with col_h2:
                        if st.button("🗑️", key=f"btn_sb_del_{p_id}_{st.session_state.widget_key}", use_container_width=True, help="Eliminar planeación"):
                            eliminar_planeacion_por_id(p_id)
                            st.rerun()
                    st.markdown("<hr style='margin: 4px 0; border: none; border-top: 1px dashed #4C1D95;'>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown('### <span style="color: #7C3AED; font-size: 1.2rem;">•</span> Datos de la Escuela y Docente', unsafe_allow_html=True)
        st.caption("Configuración oficial predeterminada de la Escuela Primaria Revolución Social de 1910 (Durango - Ciclo 2026-2027).")
    
        escuela_nombre = st.text_input(
            "Nombre de la Escuela:",
            value=DATOS_PREDETERMINADOS["nombre_escuela"],
            help="Nombre oficial de la institución escolar.",
            key=f"escuela_{st.session_state.widget_key}"
        )
    
        col_cct, col_turno = st.columns(2)
        with col_cct:
            cct = st.text_input("C.C.T.:", value=DATOS_PREDETERMINADOS["cct"], key=f"cct_{st.session_state.widget_key}")
        with col_turno:
            turno = st.text_input("Turno:", value=DATOS_PREDETERMINADOS["turno"], key=f"turno_{st.session_state.widget_key}")

        col_zona, col_sector = st.columns(2)
        with col_zona:
            zona_escolar = st.text_input("Zona Escolar:", value=DATOS_PREDETERMINADOS["zona_escolar"], key=f"zona_{st.session_state.widget_key}")
        with col_sector:
            sector = st.text_input("Sector:", value=DATOS_PREDETERMINADOS["sector"], key=f"sector_{st.session_state.widget_key}")

        entidad = st.text_input(
            "Entidad / Estado:",
            value=DATOS_PREDETERMINADOS.get("entidad", "Durango"),
            key=f"entidad_{st.session_state.widget_key}"
        )
    
        docente = st.text_input(
            "Docente Titular:",
            value=DATOS_PREDETERMINADOS["docente"],
            help="Nombre de la o el docente frente a grupo.",
            key=f"docente_{st.session_state.widget_key}"
        )
    
        director = st.text_input(
            "Director Escolar:",
            value=DATOS_PREDETERMINADOS["director"],
            help="Nombre del director de la institución escolar.",
            key=f"director_{st.session_state.widget_key}"
        )
    
        col_g, col_gr = st.columns(2)
        with col_g:
            grado_sel = st.selectbox(
                "Grado Escolar:",
                options=["1° de Primaria", "2° de Primaria", "3° de Primaria", "4° de Primaria", "5° de Primaria", "6° de Primaria"],
                index=5,
                key=f"grado_{st.session_state.widget_key}"
            )
        with col_gr:
            grupo_sel = st.text_input("Grupo:", value=DATOS_PREDETERMINADOS["grupo"], key=f"grupo_{st.session_state.widget_key}")
    
        # Determinación automática y dinámica de Fase NEM por grado seleccionado
        grado_seleccionado = grado_sel
        fase_correspondiente = determinar_fase_nem(grado_seleccionado)
        fase_auto = fase_correspondiente
    
        st.markdown(f"**Fase Curricular (NEM):** `{fase_correspondiente}`")
    
        col_fase, col_ciclo = st.columns(2)
        with col_fase:
            st.markdown(f"**Fase Curricular:** `{fase_correspondiente}`")
        with col_ciclo:
            ciclo_input_raw = st.text_input(
                "Ciclo Escolar:",
                value="2026-2027",
                help="Ciclo Escolar Oficial SEP 2026-2027.",
                key=f"ciclo_{st.session_state.widget_key}"
            )
            ciclo_sel = "2026-2027"

        semana_seleccionada = int(st.session_state.get("cal_semana_escolar", 20))
        if semana_seleccionada > 37:
            semana_seleccionada = 20
            st.session_state.cal_semana_escolar = 20
        periodo_sel = f"Semana {semana_seleccionada} de 37"
        dias_seleccionados = st.session_state.get("dias_seleccionados", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])

        # Píldora de estado unificado del Calendario Oficial SEP (Ciclo Escolar 185 Días / 37 Semanas)
        st.markdown(
            f"<div style='background: #EDE9FE; border: 1.5px solid #8B5CF6; border-radius: 8px; padding: 0.65rem 0.85rem; margin: 0.6rem 0; font-size: 0.86rem; color: #4C1D95;'>"
            f"📅 <b>Dosificación Calendario SEP (1 a 37):</b><br>"
            f"<b>{periodo_sel}</b> ({len(dias_seleccionados)} días activos)<br>"
            f"<span style='font-size: 0.78rem; color: #6D28D9;'>La semana escolar (1 a 37) y los días lectivos se definen en el Calendario Oficial interactivo central.</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        st.info("Importante: Asegúrate de que la plantilla de Word que usas como base NO tenga las tablas de los días pre-dibujadas. La aplicación las creará automáticamente según los días que elijas.")
    
        st.markdown("---")
        st.markdown('### <span style="color: #7C3AED; font-size: 1.2rem;">•</span> Motor de IA Gemini', unsafe_allow_html=True)
        st.caption("SDK oficial de Google GenAI con modelos de última generación.")
    
        # Resolver API Key
        env_api_key = os.getenv("GEMINI_API_KEY", "")
        secret_key = ""
        try:
            secret_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            pass
    
        default_key = env_api_key or secret_key
        user_api_key = st.text_input(
            "Google Gemini API Key:",
            value=default_key,
            type="password",
            help="Ingresa tu clave de API de Google AI Studio. También puedes definir GEMINI_API_KEY en variables de entorno o st.secrets.",
            key=f"api_key_{st.session_state.widget_key}"
        )
    
        active_api_key = user_api_key.strip() if user_api_key else ""
    
        if active_api_key:
            st.markdown('<span class="key-status-ok">✓ API Key Configurada</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="key-status-warn">⚠️ API Key no detectada</span>', unsafe_allow_html=True)
            st.caption("👉 Puedes obtener una gratuita en [Google AI Studio](https://aistudio.google.com/). También puedes probar la app con la plantilla precargada de 6° grado.")
    
        modelo_sel = st.selectbox(
            "Modelo de Gemini:",
            options=AVAILABLE_MODELS,
            index=0,
            help="Selecciona el modelo oficial de Google GenAI a utilizar.",
            key=f"modelo_{st.session_state.widget_key}"
        )
    
        st.markdown("---")
        st.markdown('### <span style="color: #7C3AED; font-size: 1.2rem;">•</span> Recursos SEP (Nueva Escuela Mexicana)', unsafe_allow_html=True)
    
        # A) Libros de Texto Dinámicos (Scraping en tiempo real CONALITEG + Fallback)
        catalogo_conaliteg, conaliteg_online = get_cached_conaliteg_books()
        # Usar catálogo dinámico de CONALITEG; si está vacío o no disponible, usar el diccionario interno de respaldo (fallback)
        if catalogo_conaliteg and isinstance(catalogo_conaliteg, dict) and catalogo_conaliteg.get(grado_sel):
            libros_raw = catalogo_conaliteg[grado_sel]
        else:
            libros_raw = LIBROS_SEP_POR_GRADO.get(grado_sel, LIBROS_SEP_POR_GRADO.get("6° de Primaria", []))
    
        # Sanitizar y normalizar ortografía estrictamente a 'Múltiples lenguajes'
        libros_disponibles = []
        for l in libros_raw:
            l_clean = str(l).strip()
            l_clean = l_clean.replace("MÃºltiples", "Múltiples").replace("mÃºltiples", "múltiples")
            l_clean = l_clean.replace("MÃº", "Mú").replace("mÃº", "mú")
            l_clean = l_clean.replace("Mltiples", "Múltiples")
            l_clean = re.sub(r'Múltiples\s+Lenguajes', 'Múltiples lenguajes', l_clean, flags=re.IGNORECASE)
            libros_disponibles.append(l_clean)
    
        if conaliteg_online:
            st.markdown("<span style='color:#166534; font-size:0.8rem; font-weight:600;'>🟢 Catálogo CONALITEG 2026-2027 (En vivo)</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color:#92400E; font-size:0.8rem; font-weight:600;'>🟡 Catálogo SEP NEM (Modo Respaldo)</span>", unsafe_allow_html=True)
    
        libros_sel = st.multiselect(
            "Libros de Texto SEP:",
            options=libros_disponibles,
            default=libros_disponibles[:min(3, len(libros_disponibles))],
            help=f"Libros oficiales de la SEP extraídos para {grado_sel}. Se actualizan dinámicamente desde CONALITEG al cambiar de grado.",
            key=f"libros_{st.session_state.widget_key}"
        )
    
        # B) Guías del Consejo Técnico Escolar (CTE)
        guia_cte_sel = st.selectbox(
            "Guía de Consejo Técnico Escolar (CTE):",
            options=list(GUIAS_CTE_CATALOGO.keys()),
            index=0,
            help="Orientaciones pedagógicas mensuales de la SEP para alinear la planeación.",
            key=f"cte_{st.session_state.widget_key}"
        )
        cte_info = GUIAS_CTE_CATALOGO[guia_cte_sel]
        with st.expander("📋 Ver directrices de esta sesión CTE...", expanded=False):
            st.markdown(
                f"""
                <div style="background-color: #1E1B4B; border: 1px solid #7C3AED; border-radius: 8px; padding: 12px; margin-top: 4px;">
                    <div style="margin-bottom: 8px;">
                        <span style="color: #FFFFFF; font-weight: 700; font-size: 0.88rem;">🎯 Enfoque Pedagógico:</span>
                        <div style="color: #F3E8FF; font-size: 0.85rem; line-height: 1.45; margin-top: 2px;">{cte_info['enfoque']}</div>
                    </div>
                    <div>
                        <span style="color: #FFFFFF; font-weight: 700; font-size: 0.88rem;">📌 Directrices (Evaluación formativa, retroalimentación y BAP):</span>
                        <div style="color: #F3E8FF; font-size: 0.85rem; line-height: 1.45; margin-top: 2px;">{cte_info['directrices']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("---")
        st.markdown('### <span style="color: #7C3AED; font-size: 1.2rem;">•</span> Recursos Multimedia y Música', unsafe_allow_html=True)

        CANALES_MUSICA_DEFAULT = {
            "🎵 Lista Oficial NEM (Educación Primaria)": EMBED_PLAYLIST_OFICIAL_YOUTUBE,
            "Lo-Fi Hip Hop (Relax / Estudio)": "https://www.youtube.com/embed/jfKfPfyJRdk",
            "Piano Clásico Relajante": "https://www.youtube.com/embed/4xDzrJKXOOY",
            "Café Jazz Instrumental": "https://www.youtube.com/embed/DXUAyRRkI6k",
            "Sonidos de la Naturaleza y Lluvia": "https://www.youtube.com/embed/mPZkdNFkNps",
            "Ondas Alfa (Enfoque Profundo)": "https://www.youtube.com/embed/WPni755-Krg",
            "Enlace Personalizado de YouTube": ""
        }

        estilo_musica_sel = st.selectbox(
            "Ambiente Musical y Videos:",
            options=list(CANALES_MUSICA_DEFAULT.keys()),
            index=0,
            help="Selecciona la lista oficial o una atmósfera musical relajante para acompañar el diseño de tus planeaciones.",
            key=f"musica_preset_{st.session_state.widget_key}"
        )

        url_custom_youtube = st.text_input(
            "Enlace personalizado de YouTube (opcional):",
            value="",
            placeholder=URL_PLAYLIST_OFICIAL_YOUTUBE,
            help="Pega aquí el enlace de cualquier video o playlist de YouTube para reproducirlo. Por defecto se reproduce la lista oficial.",
            key=f"musica_url_{st.session_state.widget_key}"
        )

        # Resolver la URL del reproductor
        if url_custom_youtube.strip():
            url_embed_activa = extraer_embed_youtube(url_custom_youtube.strip())
        elif CANALES_MUSICA_DEFAULT.get(estilo_musica_sel):
            url_embed_activa = CANALES_MUSICA_DEFAULT[estilo_musica_sel]
        else:
            url_embed_activa = EMBED_PLAYLIST_OFICIAL_YOUTUBE

        # Garantizar que la URL activa sea estrictamente formato embed oficial
        url_embed_activa = extraer_embed_youtube(url_embed_activa)

        # Reproductor seguro de YouTube incrustado mediante st.components.v1.iframe
        st.components.v1.iframe(
            src=url_embed_activa,
            height=160,
            scrolling=False
        )

        st.markdown(f"""
        <div style="font-size: 0.78rem; margin-top: 4px; display: flex; justify-content: space-between; align-items: center;">
            <a href="{URL_PLAYLIST_OFICIAL_YOUTUBE}" target="_blank" style="color: #A78BFA; text-decoration: none; font-weight: 600;">
                ▶️ Abrir Lista Oficial en YouTube
            </a>
            <span style="color: #94A3B8; font-size: 0.72rem;">Predeterminada</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Empaquetar datos de escuela
    datos_escuela_actual = {
        "nombre_escuela": escuela_nombre,
        "cct": cct,
        "zona_escolar": zona_escolar,
        "sector": sector,
        "entidad": entidad,
        "docente": docente,
        "director": director,
        "grado": grado_sel,
        "fase": fase_auto,
        "grupo": grupo_sel,
        "matricula": 26,
        "estilos_aprendizaje": "Kinestésico y Visual",
        "contexto_escolar": CONTEXTO_ESCOLAR_PREDETERMINADO,
        "contexto_grupal": CONTEXTO_GRUPAL_PREDETERMINADO,
        "problematizaciones": PROBLEMATIZACIONES_PREDETERMINADAS,
        "periodo": periodo_sel,
        "semana": semana_seleccionada,
        "semana_seleccionada": semana_seleccionada,
        "ciclo_escolar": ciclo_sel,
        "turno": turno,
        "dias_seleccionados": dias_seleccionados,
        "dias_planeados": dias_seleccionados,
        "dias_fechas": st.session_state.get("dias_fechas", {})
    }
    
    # ==========================================
    # ENCABEZADO PRINCIPAL
    # ==========================================
    st.title("Planeaciones Escolares Educación Primaria")
    
    # Metadatos en píldoras rápidas
    cols_meta = st.columns(4)
    with cols_meta[0]:
        st.markdown(f"<div class='badge-sep'><span style='color: #7C3AED; font-size: 1.1rem;'>•</span> {escuela_nombre}</div>", unsafe_allow_html=True)
    with cols_meta[1]:
        st.markdown(f"<div class='badge-sep'><span style='color: #7C3AED; font-size: 1.1rem;'>•</span> C.C.T. {cct} | {zona_escolar} | {sector} ({entidad})</div>", unsafe_allow_html=True)
    with cols_meta[2]:
        st.markdown(f"<div class='badge-sep'><span style='color: #7C3AED; font-size: 1.1rem;'>•</span> Docente: {docente} | Dir: {director}</div>", unsafe_allow_html=True)
    with cols_meta[3]:
        st.markdown(f"<div class='badge-sep'><span style='color: #7C3AED; font-size: 1.1rem;'>•</span> {grado_sel} “{grupo_sel}” ({fase_auto}) • {periodo_sel} • Ciclo {ciclo_sel}</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # Notificaciones de reinicio de estado y cambio de semana
    if st.session_state.get("aviso_nueva_planeacion"):
        st.success("✨ **Nueva Planeación iniciada:** Se ha limpiado el estado de la sesión por completo. Los datos institucionales oficiales de la Escuela Primaria Revolución Social de 1910 (6° 'A') y el Ciclo 2026-2027 están listos para generar desde cero.")
        if hasattr(st, "toast"):
            st.toast("✨ Nueva Planeación iniciada: Sistema listo desde cero con datos institucionales.", icon="📋")
        del st.session_state["aviso_nueva_planeacion"]

    if st.session_state.get("aviso_cambio_semana"):
        sem_aviso = st.session_state.get("aviso_cambio_semana")
        st.info(f"🔄 **Cambio a {sem_aviso}:** Se reiniciaron las actividades generadas, archivos y borradores para evitar arrastre de datos. La planeación se generará desde cero.")
        if hasattr(st, "toast"):
            st.toast(f"🔄 Cambio a {sem_aviso}: Estado previo reiniciado.", icon="🧹")
        del st.session_state["aviso_cambio_semana"]

    if st.session_state.get("aviso_planeacion_cargada"):
        plan_aviso = st.session_state.get("aviso_planeacion_cargada")
        st.success(f"📂 **Planeación cargada con éxito:** Se restauraron todos los datos, campos y actividades de **{plan_aviso}** para continuar con su edición.")
        if hasattr(st, "toast"):
            st.toast(f"📂 Planeación cargada: {plan_aviso}", icon="✅")
        del st.session_state["aviso_planeacion_cargada"]
    
    # ==========================================
    # SECCIÓN 1: CARGA DE ARCHIVOS Y TEXTOS DE REFERENCIA
    # ==========================================
    st.markdown("""
    <div class="nem-card-header">
        <span style="color: #7C3AED; font-size: 1.5rem; line-height: 1;">•</span>
        <h3 class="nem-card-title">1. Carga de Archivos y Textos de Referencia</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_archivos, col_texto = st.columns([1.1, 1.2])
    
    with col_archivos:
        st.markdown(f'#### <span style="color: #7C3AED; font-size: 1.2rem;">•</span> Cargar Programa Sintético ({fase_correspondiente})', unsafe_allow_html=True)
        st.caption(f"Sube el documento del Programa Sintético oficial ({fase_correspondiente} - {grado_seleccionado}) para que Gemini extraiga automáticamente los Contenidos, los PDA, los 4 Campos Formativos y los 7 Ejes Articuladores.")
    
        uploaded_prog = st.file_uploader(
            f"Cargar Programa Sintético ({fase_correspondiente})",
            type=["pdf", "docx", "txt"],
            key=f"uploader_programa_sintetico_{st.session_state.widget_key}",
            help=f"Procesa el documento del Programa Sintético de {fase_correspondiente} ({grado_seleccionado}) para que Gemini identifique los PDA y Ejes vinculados."
        )
    
        if uploaded_prog:
            bytes_p = uploaded_prog.getvalue()
            ext_p = uploaded_prog.name.lower().split(".")[-1]
            if ext_p == "pdf":
                texto_extraido = extract_text_from_pdf(bytes_p)
            elif ext_p in ["docx", "doc"]:
                texto_extraido = extract_text_from_docx(bytes_p)
            else:
                texto_extraido = extract_text_from_txt(bytes_p)
            st.session_state.programa_sintetico_texto = texto_extraido
            st.session_state["programa_sintetico_subido"] = True
            st.session_state["nombre_archivo_programa"] = uploaded_prog.name
            st.session_state["es_programa_oficial_fase5"] = True
            programa_sintetico = texto_extraido
            pda_extraidos = extraer_contenidos_pda_fase5(texto_extraido)
            st.session_state["pda_extraidos_programa"] = pda_extraidos
            st.success(
                f"🟢 Base de Datos Principal y Oficial Reconocida: '{uploaded_prog.name}'. "
                f"Configurado como la fuente oficial para extraer Contenidos, PDA (6° Grado), "
                f"Campos Formativos y Ejes Articuladores ({len(texto_extraido):,} caracteres extraídos)."
            )
        else:
            st.session_state.programa_sintetico_texto = ""
            st.session_state["programa_sintetico_subido"] = False
            st.session_state["nombre_archivo_programa"] = ""
            st.session_state["es_programa_oficial_fase5"] = False
            st.session_state["pda_extraidos_programa"] = []
            programa_sintetico = ""
            st.info(f"ℹ️ **Modo de Respaldo SEP:** Al no subir un archivo, el sistema ejecutará automáticamente una búsqueda de respaldo en portales oficiales de la SEP (`site:sep.gob.mx OR site:conaliteg.sep.gob.mx`) para la {fase_correspondiente}. Si el scraping no está disponible, se activará la directriz curricular oficial de la Nueva Escuela Mexicana para la Fase {fase_correspondiente.replace('Fase', '').strip()} y Semana {semana_seleccionada}.")
    
    
        if st.session_state.programa_sintetico_texto:
            with st.expander(f"Ver extracto de Programa Sintético cargado ({fase_correspondiente})", expanded=False):
                st.caption("Texto del Programa Sintético que se enviará en el prompt de Gemini:")
                st.text_area(
                    f"Contenido del Programa Sintético ({fase_correspondiente}):",
                    value=st.session_state.programa_sintetico_texto[:2500] + ("..." if len(st.session_state.programa_sintetico_texto) > 2500 else ""),
                    height=130,
                    disabled=True,
                    key="preview_prog_sintetico_text"
                )
    
        st.markdown("---")
        st.info("Importante: Asegúrate de que la plantilla de Word que usas como base NO tenga las tablas de los días pre-dibujadas. La aplicación las creará automáticamente según los días que elijas.")
        st.markdown("**Subir Libros de Texto, Guías o Planeaciones Previas de Referencia:**")
        uploaded_files = st.file_uploader(
            "Cargar archivos de referencia adicionales (.pdf, .docx, .txt):",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=True,
            help="Carga documentos de apoyo adicionales para nutrir el contexto.",
            key=f"uploader_archivos_{st.session_state.widget_key}"
        )
    
        if uploaded_files:
            st.session_state.archivos_procesados = process_uploaded_files(uploaded_files)
            st.success(f"✓ Se procesaron {len(uploaded_files)} archivo(s) de referencia.")
            for fname, cont in st.session_state.archivos_procesados.items():
                chars = len(cont)
                st.caption(f"**{fname}**: ~{chars:,} caracteres extraídos.")
    
        url_referencia = st.text_input(
            "URL de Referencia para Planeaciones (Ej. materialeducativo.org):",
            value="",
            placeholder="https://materialeducativo.org/...",
            help="Ingresa la URL de una página educativa para extraer su contenido e incorporarlo a la planeación.",
            key=f"url_referencia_{st.session_state.widget_key}"
        )
        contexto_url = ""
        if url_referencia and url_referencia.strip():
            contexto_url = extraer_texto_url(url_referencia.strip())
            st.session_state.contexto_url = contexto_url
            if contexto_url:
                st.success(f"✓ Contenido web extraído con éxito ({len(contexto_url):,} caracteres).")
                with st.expander("Ver extracto de contenido web extraído", expanded=False):
                    st.text_area(
                        "Texto extraído de la URL:",
                        value=contexto_url[:2000] + ("..." if len(contexto_url) > 2000 else ""),
                        height=120,
                        disabled=True,
                        key="preview_contexto_url"
                    )
            else:
                st.warning("⚠️ No se pudo extraer texto de la URL proporcionada o el enlace no contiene párrafos de texto accesibles.")
        else:
            st.session_state.contexto_url = ""
    
        col_btn_ej1, col_btn_ej2 = st.columns(2)
        with col_btn_ej1:
            if st.button(f"Recargar Programa ({fase_correspondiente})", help=f"Carga el extracto oficial de Programa Sintético {fase_correspondiente}"):
                try:
                    with open("sample_data/programa_sintetico_fase5_ejemplo.txt", "r", encoding="utf-8") as f:
                        texto_ej = f.read()
                        st.session_state.programa_sintetico_texto = texto_ej
                        st.session_state["programa_sintetico_subido"] = True
                        st.session_state["nombre_archivo_programa"] = "Programa_Sintetico_Fase_5.pdf"
                        st.session_state["es_programa_oficial_fase5"] = True
                        programa_sintetico = texto_ej
                        st.session_state["pda_extraidos_programa"] = extraer_contenidos_pda_fase5(texto_ej)
                    st.success(f"🟢 Base de Datos Principal y Oficial Reconocida: 'Programa_Sintetico_Fase_5.pdf'. Configurado como la fuente oficial para extraer Contenidos, PDA ({grado_seleccionado}), Campos Formativos y Ejes Articuladores.")
                except Exception as e:
                    st.error(f"Error al cargar ejemplo: {e}")
    
        with col_btn_ej2:
            if st.button("Cargar Guía CTE 6° (.docx)", help="Carga la guía escolar de ejemplo en Word"):
                try:
                    with open("sample_data/guia_5to_grado_ejemplo.docx", "rb") as f:
                        st.session_state.archivos_procesados["Guia_Escolar_5to.docx"] = extract_text_from_docx(f.read())
                    st.info("Guía de Consejo Técnico Escolar en .docx cargada.")
                except Exception as e:
                    st.error(f"Error al cargar ejemplo: {e}")
    
    with col_texto:
        st.markdown('#### <span style="color: #7C3AED; font-size: 1.2rem;">•</span> Programa Analítico y Diagnóstico (Ciclo 2026-2027)', unsafe_allow_html=True)
        st.caption("Precarga oficial: Contexto comunitario (Durango), diagnóstico del grupo (26 alumnos, estilos kinestésico y visual) y ejes de trabajo priorizados.")

        # Píldora de estado del Programa Analítico Oficial
        st.markdown(
            f"<div style='background: #EDE9FE; border: 1.5px solid #8B5CF6; border-radius: 8px; padding: 0.65rem 0.85rem; margin-bottom: 0.75rem; font-size: 0.84rem; color: #3730A3;'>"
            f"🏛️ <b>Institución:</b> {escuela_nombre} (C.C.T. {cct}) — {zona_escolar}, {sector}, {entidad}.<br>"
            f"👤 <b>Titular:</b> {docente} | <b>Dirección:</b> {director} | <b>{grado_sel} “{grupo_sel}”</b> ({fase_auto})<br>"
            f"👥 <b>Matrícula:</b> 26 alumnos (Estilos Kinestésico y Visual predominantes)<br>"
            f"🎯 <b>Ejes de Trabajo:</b> Comprensión lectora, velocidad lectora, ortografía, fomento a la lectura y acceso/uso reflexivo de tecnologías."
            f"</div>",
            unsafe_allow_html=True
        )

        tab_analitico_prompt, tab_contexto_det, tab_problemas_det = st.tabs([
            "📋 Programa Analítico (Prompt IA)",
            "🏘️ Contexto Escolar y Grupal",
            "🎯 Problematizaciones Priorizadas"
        ])

        with tab_analitico_prompt:
            directrices_input = st.text_area(
                "Directrices oficiales del Programa Analítico y acuerdos de CTE para Gemini:",
                value=EJEMPLO_PROBLEMICA_ANALITICO,
                height=210,
                help="Texto precargado oficial del Programa Analítico (Ciclo 2026-2027). La IA utilizará estos datos para diseñar y fundamentar las secuencias didácticas, rutinas de inicio y evaluación formativa.",
                key=f"directrices_{st.session_state.widget_key}"
            )

        with tab_contexto_det:
            st.markdown(
                f"""
                <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; padding: 12px; font-size: 0.84rem; color: #1E293B; line-height: 1.5;">
                    <b style="color: #4338CA;">🏛️ Contexto Escolar y Comunitario (Durango):</b><br>
                    {CONTEXTO_ESCOLAR_PREDETERMINADO}<br><br>
                    <b style="color: #4338CA;">👥 Diagnóstico del Grupo (6° "A" - 26 Alumnos):</b><br>
                    {CONTEXTO_GRUPAL_PREDETERMINADO}
                </div>
                """,
                unsafe_allow_html=True
            )

        with tab_problemas_det:
            st.markdown(
                f"""
                <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 6px; padding: 12px; font-size: 0.84rem; color: #1E293B; line-height: 1.5;">
                    <b style="color: #4338CA;">🎯 Problemáticas Identificadas y Ejes de Trabajo del Programa Analítico:</b><br>
                    {PROBLEMATIZACIONES_PREDETERMINADAS}
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
    
    # ==========================================
    # GESTOR DE ARCHIVOS E HISTORIAL DE PLANEACIONES (37 SEMANAS)
    # ==========================================
    docente_usuario_main = st.session_state.get("username", "docente")
    stats_cubiertas_main = obtener_resumen_semanas_cubiertas(docente_usuario_main)
    lista_guardadas_main = listar_planeaciones(docente_usuario_main)

    with st.expander(f"🗂️ Gestor de Archivos y Planeaciones Guardadas ({len(lista_guardadas_main)} registradas • {stats_cubiertas_main['semanas_completas']} de 37 semanas completas)", expanded=False):
        c_m1, c_m2, c_m3, c_m4 = st.columns(4)
        with c_m1:
            st.metric("Total Guardadas", len(lista_guardadas_main))
        with c_m2:
            st.metric("Semanas con Plan", f"{stats_cubiertas_main['semanas_completas']} / 37")
        with c_m3:
            st.metric("Avance del Ciclo", f"{stats_cubiertas_main['porcentaje_avance']}%")
        with c_m4:
            hora_act = st.session_state.get("ultimo_autoguardado_hora", "En vivo")
            st.metric("Autoguardado", hora_act)

        tab_g_archivos, tab_g_sem, tab_g_fecha, tab_g_campo, tab_g_backup = st.tabs([
            "📂 Por Nombre y Carpeta / Ruta",
            "📅 Por Semana (1 a 37)",
            "🕒 Por Fecha de Guardado",
            "🎨 Por Campo Formativo / Asignatura",
            "💾 Respaldos y Versiones"
        ])

        with tab_g_archivos:
            st.markdown("#### 📂 Gestor de Archivos por Nombre y Carpeta / Destino")
            st.caption("Administra, organiza por carpetas (Trimestre, Proyectos, CTE) y abre tus planeaciones guardadas con su nombre personalizado.")
            
            if not lista_guardadas_main:
                st.markdown(
                    "<div class='empty-history-box' style='background-color: #F8FAFC; border: 1.5px solid #CBD5E1; border-left: 4px solid #7C3AED; border-radius: 8px; padding: 12px 14px; margin: 10px 0;'>"
                    "<div class='empty-history-title' style='color: #111827; font-weight: 700; font-size: 0.86rem; margin-bottom: 4px; display: flex; align-items: center; gap: 6px;'>"
                    "<span>ℹ️</span> <span style='color: #111827;'>No hay planeaciones guardadas aún</span>"
                    "</div>"
                    "<div class='empty-history-text' style='color: #374151; font-size: 0.82rem; font-weight: 500; line-height: 1.5;'>"
                    "Configura una semana o genera una planeación y se guardará automáticamente con su nombre de archivo personalizado."
                    "</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            else:
                # 1. Menú desplegable / selector rápido de archivos
                c_sel_arch, c_btn_arch = st.columns([2.5, 1])
                with c_sel_arch:
                    dict_planes_main = {p["id"]: p for p in lista_guardadas_main}
                    def format_main_arch_opt(pid):
                        p = dict_planes_main[pid]
                        tag = "🟢 Lista" if p["tiene_plan"] else "📝 Borrador"
                        return f"📄 {p['nombre_archivo']} — Sem. {p['semana']} [{p['categoria_ruta']}] ({tag})"
                    
                    id_sel_main = st.selectbox(
                        "Selecciona un archivo guardado para cargar:",
                        options=list(dict_planes_main.keys()),
                        format_func=format_main_arch_opt,
                        key=f"sel_main_arch_{st.session_state.widget_key}"
                    )
                with c_btn_arch:
                    st.markdown("<div style='height: 1.7rem;'></div>", unsafe_allow_html=True)
                    if st.button("📂 Abrir y Cargar Archivo", key=f"btn_main_load_arch_{st.session_state.widget_key}", use_container_width=True, type="primary"):
                        if id_sel_main:
                            cargar_planeacion_guardada(id_sel_main)
                            st.rerun()

                st.markdown("<hr style='margin: 12px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

                # 2. Organización y filtro por Categoría / Carpeta
                categorias_existentes = sorted(list(set(p["categoria_ruta"] for p in lista_guardadas_main)))
                filtro_cat = st.selectbox(
                    "📁 Filtrar por Carpeta / Categoría:",
                    options=["Todas las Carpetas"] + categorias_existentes,
                    key=f"flt_cat_gestor_{st.session_state.widget_key}"
                )
                
                archivos_filtrados = [
                    p for p in lista_guardadas_main
                    if filtro_cat == "Todas las Carpetas" or p["categoria_ruta"] == filtro_cat
                ]

                st.markdown(f"<div style='font-size:0.82rem; color:#475569; margin-bottom:8px;'>Mostrando <b>{len(archivos_filtrados)}</b> planeaciones en <b>{filtro_cat}</b>:</div>", unsafe_allow_html=True)

                for p_arch in archivos_filtrados:
                    p_id = p_arch["id"]
                    col_a1, col_a2, col_a3 = st.columns([2.8, 1, 1.2])
                    with col_a1:
                        c_list_str = ", ".join(p_arch["campos_formativos"][:2]) + ("..." if len(p_arch["campos_formativos"]) > 2 else "")
                        st.markdown(
                            f"**📄 {p_arch['nombre_archivo']}**<br>"
                            f"<span style='font-size:0.75rem; color:#6D28D9; font-weight:600;'>📁 {p_arch['categoria_ruta']}</span> • "
                            f"<span style='font-size:0.75rem; color:#475569;'>Semana {p_arch['semana']} ({p_arch['periodo']})</span><br>"
                            f"<span style='font-size:0.72rem; color:#64748B;'>{c_list_str} • {p_arch['num_sesiones']} sesiones • {p_arch['fecha_guardado']}</span>",
                            unsafe_allow_html=True
                        )
                    with col_a2:
                        if p_arch["tiene_plan"]:
                            st.markdown("<span style='background:#DCFCE7; color:#15803D; padding:3px 8px; border-radius:6px; font-size:0.75rem; font-weight:700;'>🟢 Lista (Word/PDF)</span>", unsafe_allow_html=True)
                        else:
                            st.markdown("<span style='background:#FEF3C7; color:#B45309; padding:3px 8px; border-radius:6px; font-size:0.75rem; font-weight:700;'>📝 Borrador</span>", unsafe_allow_html=True)
                    with col_a3:
                        col_sub_btn1, col_sub_btn2 = st.columns([1.5, 1])
                        with col_sub_btn1:
                            if st.button("📂 Abrir", key=f"btn_arch_open_{p_id}_{st.session_state.widget_key}", use_container_width=True):
                                cargar_planeacion_guardada(p_id)
                                st.rerun()
                        with col_sub_btn2:
                            if st.button("🗑️", key=f"btn_arch_del_{p_id}_{st.session_state.widget_key}", use_container_width=True, help="Eliminar planeación"):
                                eliminar_planeacion_por_id(p_id)
                                st.rerun()
                    st.markdown("<hr style='margin: 4px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

        with tab_g_sem:
            dict_guardadas_por_sem = {p["semana"]: p for p in lista_guardadas_main if p["es_autoguardado"]}
            st.markdown("<div style='font-size:0.83rem; color:#475569; margin-bottom: 8px;'>Selecciona cualquier semana para restaurar todos sus campos, actividades y continuar su edición sin perder datos:</div>", unsafe_allow_html=True)
            
            semanas_con_datos = sorted(list(set(p["semana"] for p in lista_guardadas_main)))
            filtro_sem_main = st.multiselect(
                "Filtrar por semanas específicas (o dejar vacío para ver todas):",
                options=list(range(1, 38)),
                default=semanas_con_datos if semanas_con_datos else [st.session_state.get("cal_semana_escolar", 20)],
                format_func=lambda s: f"Semana {s} ({CATALOGO_SEMANAS_SEP[s]['mes_nombre'][:3]} {CATALOGO_SEMANAS_SEP[s]['año']})" if s in CATALOGO_SEMANAS_SEP else f"Semana {s}",
                key=f"flt_sem_gestor_{st.session_state.widget_key}"
            )
            semanas_a_mostrar = filtro_sem_main if filtro_sem_main else list(range(1, 38))

            for s_num in semanas_a_mostrar:
                p_s = dict_guardadas_por_sem.get(s_num)
                inf_s = CATALOGO_SEMANAS_SEP.get(s_num, {})
                rango_s = inf_s.get("rango_str", "")
                mes_s = inf_s.get("mes_nombre", "")
                cte_tag = " [📌 CTE]" if inf_s.get("tiene_cte") else ""
                
                col_c1, col_c2, col_c3, col_c4 = st.columns([1.2, 1.8, 1.2, 1.3])
                with col_c1:
                    st.markdown(f"**Semana {s_num} de 37**{cte_tag}<br><span style='font-size:0.75rem; color:#6B7280;'>{rango_s} ({mes_s})</span>", unsafe_allow_html=True)
                with col_c2:
                    if p_s:
                        campos_txt = ", ".join(p_s["campos_formativos"][:2]) + ("..." if len(p_s["campos_formativos"]) > 2 else "")
                        st.markdown(f"<span style='font-size:0.8rem; color:#1E293B;'>{campos_txt}</span><br><span style='font-size:0.72rem; color:#64748B;'>{p_s['num_sesiones']} sesiones • {p_s['metodologia'][:28]}...</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='font-size:0.78rem; color:#94A3B8;'>Sin planeación guardada</span>", unsafe_allow_html=True)
                with col_c3:
                    if p_s and p_s["tiene_plan"]:
                        st.markdown("<span style='background:#DCFCE7; color:#15803D; padding:2px 8px; border-radius:6px; font-size:0.75rem; font-weight:700;'>🟢 Lista (Word/PDF)</span>", unsafe_allow_html=True)
                    elif p_s:
                        st.markdown("<span style='background:#FEF3C7; color:#B45309; padding:2px 8px; border-radius:6px; font-size:0.75rem; font-weight:700;'>📝 Borrador Configurado</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span style='background:#F1F5F9; color:#64748B; padding:2px 8px; border-radius:6px; font-size:0.75rem;'>⚪ Pendiente</span>", unsafe_allow_html=True)
                with col_c4:
                    if p_s:
                        if st.button("📂 Abrir y Cargar", key=f"btn_gest_open_{p_s['id']}_{st.session_state.widget_key}", use_container_width=True):
                            cargar_planeacion_guardada(p_s["id"])
                            st.rerun()
                    else:
                        if st.button("➕ Iniciar Semana", key=f"btn_gest_init_{s_num}_{st.session_state.widget_key}", use_container_width=True):
                            limpiar_estado_planeacion(nueva_semana=s_num, reset_completo=False)
                            st.rerun()
                st.markdown("<hr style='margin: 3px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

        with tab_g_fecha:
            if not lista_guardadas_main:
                st.markdown(
                    "<div class='empty-history-box' style='background-color: #F8FAFC; border: 1.5px solid #CBD5E1; border-left: 4px solid #7C3AED; border-radius: 8px; padding: 12px 14px; margin: 10px 0;'>"
                    "<div class='empty-history-title' style='color: #111827; font-weight: 700; font-size: 0.86rem; margin-bottom: 4px; display: flex; align-items: center; gap: 6px;'>"
                    "<span>ℹ️</span> <span style='color: #111827;'>No hay planeaciones guardadas aún en el sistema</span>"
                    "</div>"
                    "<div class='empty-history-text' style='color: #374151; font-size: 0.82rem; font-weight: 500;'>"
                    "Las planeaciones guardadas aparecerán aquí ordenadas cronológicamente por fecha de guardado."
                    "</div>"
                    "</div>",
                    unsafe_allow_html=True
                )
            else:
                for p_rec in sorted(lista_guardadas_main, key=lambda x: x["timestamp"], reverse=True):
                    col_f1, col_f2, col_f3 = st.columns([2.5, 1.2, 1.3])
                    with col_f1:
                        v_lbl = f" — *{p_rec['version_nombre']}*" if not p_rec["es_autoguardado"] else ""
                        st.markdown(f"**Semana {p_rec['semana']}** ({p_rec['periodo']}){v_lbl}<br><span style='font-size:0.75rem; color:#6B7280;'>Guardado: {p_rec['fecha_guardado']} • {', '.join(p_rec['campos_formativos'])}</span>", unsafe_allow_html=True)
                    with col_f2:
                        st.markdown("🟢 **Completa**" if p_rec["tiene_plan"] else "📝 **Borrador**")
                    with col_f3:
                        c_sub1, c_sub2 = st.columns([2, 1])
                        with c_sub1:
                            if st.button("📂 Abrir", key=f"btn_f_open_{p_rec['id']}_{st.session_state.widget_key}", use_container_width=True):
                                cargar_planeacion_guardada(p_rec["id"])
                                st.rerun()
                        with c_sub2:
                            if st.button("🗑️", key=f"btn_f_del_{p_rec['id']}_{st.session_state.widget_key}", use_container_width=True):
                                eliminar_planeacion_por_id(p_rec["id"])
                                st.rerun()
                    st.markdown("<hr style='margin: 3px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

        with tab_g_campo:
            campo_filtro = st.selectbox(
                "Filtrar por Campo Formativo / Asignatura:",
                options=CAMPOS_FORMATIVOS,
                key=f"sel_campo_filtro_{st.session_state.widget_key}"
            )
            planes_por_campo = [p for p in lista_guardadas_main if campo_filtro in p["campos_formativos"]]
            if not planes_por_campo:
                st.info(f"No hay planeaciones registradas que incluyan el campo formativo '{campo_filtro}'.")
            else:
                for p_c in planes_por_campo:
                    col_cp1, col_cp2, col_cp3 = st.columns([2.5, 1, 1.2])
                    with col_cp1:
                        st.markdown(f"**Semana {p_c['semana']}** ({p_c['periodo']})<br><span style='font-size:0.75rem; color:#6B7280;'>Metodología: {p_c['metodologia']} • Fecha: {p_c['fecha_guardado']}</span>", unsafe_allow_html=True)
                    with col_cp2:
                        st.markdown("🟢 **Lista**" if p_c["tiene_plan"] else "📝 **Borrador**")
                    with col_cp3:
                        if st.button("📂 Cargar", key=f"btn_cp_open_{p_c['id']}_{st.session_state.widget_key}", use_container_width=True):
                            cargar_planeacion_guardada(p_c["id"])
                            st.rerun()
                    st.markdown("<hr style='margin: 3px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

        with tab_g_backup:
            st.markdown("#### 💾 Respaldos de Planeaciones y Versiones")
            st.caption("Crea una copia etiquetada de la planeación actual o descarga el historial completo del ciclo en formato JSON.")
            c_v1, c_v2 = st.columns([2, 1])
            with c_v1:
                ver_nombre_custom = st.text_input(
                    "Nombre de versión o etiqueta:",
                    value=f"Semana {semana_seleccionada} - Versión Especial",
                    key=f"inp_custom_ver_{st.session_state.widget_key}"
                )
            with c_v2:
                st.markdown("<div style='height: 1.7rem;'></div>", unsafe_allow_html=True)
                if st.button("💾 Guardar como Versión", key=f"btn_save_custom_ver_{st.session_state.widget_key}", use_container_width=True):
                    data_version_save = {
                        "semana": semana_seleccionada,
                        "periodo": periodo_sel,
                        "titulo": f"Semana {semana_seleccionada} — {ver_nombre_custom}",
                        "grado": grado_sel,
                        "grupo": grupo_sel,
                        "campos_formativos": CAMPOS_FORMATIVOS,
                        "metodologia": "Aprendizaje Basado en Proyectos Comunitarios",
                        "ejes_articuladores": ["Pensamiento crítico", "Apropiación de las culturas a través de la lectura y la escritura", "Vida saludable"],
                        "contenidos_pda": [],
                        "libros_seleccionados": [],
                        "guia_cte": "",
                        "dias_seleccionados": dias_seleccionados,
                        "dias_fechas": st.session_state.get("dias_fechas", {}),
                        "directrices": st.session_state.get("directrices", ""),
                        "num_sesiones": len(dias_seleccionados),
                        "planeacion_generada": st.session_state.get("planeacion_generada") or "",
                        "prompt_enviado": st.session_state.get("prompt_enviado") or "",
                        "url_referencia": st.session_state.get("url_referencia", "")
                    }
                    guardar_planeacion(
                        username=docente_usuario_main,
                        data=data_version_save,
                        es_autoguardado=False,
                        version_nombre=ver_nombre_custom
                    )
                    st.success(f"✓ ¡Versión '{ver_nombre_custom}' guardada exitosamente!")
                    st.rerun()

            # Inicialización previa garantizada para evitar NameError
            all_records_full = []
            json_backup = "[]"

            if lista_guardadas_main:
                try:
                    all_records_full = [
                        obtener_planeacion_por_id(p["id"])
                        for p in lista_guardadas_main
                        if p and isinstance(p, dict) and "id" in p
                    ]
                    all_records_full = [r for r in all_records_full if r is not None]
                    if 'all_records_full' in locals() and all_records_full:
                        json_backup = json.dumps(all_records_full, ensure_ascii=False, indent=2)
                except Exception as err_dumps:
                    all_records_full = []
                    json_backup = "[]"

            if 'all_records_full' in locals() and all_records_full and json_backup != "[]":
                st.download_button(
                    label="📥 Exportar Todo el Historial a JSON",
                    data=json_backup,
                    file_name=f"Historial_Planeaciones_{docente_usuario_main}_2026_2027.json",
                    mime="application/json",
                    use_container_width=True
                )
            else:
                st.markdown(
                    "<div class='empty-history-box' style='background-color: #F8FAFC; border: 1.5px solid #CBD5E1; border-left: 4px solid #7C3AED; border-radius: 8px; padding: 12px 14px; margin: 10px 0;'>"
                    "<div class='empty-history-text' style='color: #374151; font-size: 0.82rem; font-weight: 500;'>"
                    "ℹ️ Aún no hay planeaciones guardadas en el historial para exportar."
                    "</div>"
                    "</div>",
                    unsafe_allow_html=True
                )

            # Módulo seguro de importación / restauración desde archivo JSON
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            with st.expander("📤 Restaurar o Importar Planeaciones desde archivo JSON"):
                st.caption("Carga un archivo de respaldo JSON generado previamente para sincronizarlo o restaurarlo en tu historial.")
                archivo_json_subido = st.file_uploader(
                    "Selecciona el archivo JSON de respaldo:",
                    type=["json"],
                    key=f"uploader_backup_json_{st.session_state.widget_key}"
                )
                if archivo_json_subido is not None:
                    try:
                        contenido_raw = archivo_json_subido.read().decode("utf-8", errors="ignore").strip()
                        if not contenido_raw:
                            st.warning("⚠️ El archivo JSON seleccionado está vacío o no contiene datos.")
                        else:
                            datos_importados = json.loads(contenido_raw)
                            if isinstance(datos_importados, dict):
                                datos_importados = [datos_importados]
                            if isinstance(datos_importados, list) and len(datos_importados) > 0:
                                count_ok = 0
                                for item_imp in datos_importados:
                                    if isinstance(item_imp, dict) and "semana" in item_imp:
                                        guardar_planeacion(
                                            username=docente_usuario_main,
                                            data=item_imp,
                                            es_autoguardado=False,
                                            version_nombre=item_imp.get("version_nombre", "Importado JSON")
                                        )
                                        count_ok += 1
                                if count_ok > 0:
                                    st.success(f"✓ ¡Se importaron exitosamente {count_ok} planeaciones del respaldo JSON!")
                                    st.rerun()
                                else:
                                    st.warning("⚠️ No se encontraron planeaciones estructuradas válidas en el archivo JSON.")
                            else:
                                st.warning("⚠️ El formato del archivo JSON debe contener una lista o registro de planeaciones.")
                    except Exception as err_json_read:
                        st.error(f"❌ Error al procesar el archivo JSON: {err_json_read}")

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    
    # ==========================================
    # CALENDARIO INTERACTIVO OFICIAL SEP (37 SEMANAS / 185 DÍAS LECTIVOS)
    # ==========================================
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.4rem; margin-bottom: 0.5rem; padding-bottom: 0.4rem; border-bottom: 1px solid #E2E8F0;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #7C3AED;"></span>
            <span style="font-weight: 700; font-size: 1.02rem; color: #1E1B4B; letter-spacing: -0.2px;">Calendario Oficial SEP 2026 y Dosificación Temporal</span>
            <span style="font-size: 0.72rem; background: #EDE9FE; color: #6D28D9; padding: 2px 8px; border-radius: 9999px; font-weight: 700; border: 1px solid #C4B5FD;">Semanas 1 a 37 SEP (185 Días Lectivos)</span>
        </div>
        <span style="font-size: 0.78rem; color: #6B7280;">Sincronizado con secuencias didácticas y CTE</span>
    </div>
    """, unsafe_allow_html=True)

    # Variables de control inicial
    semana_actual_init = int(st.session_state.get("cal_semana_escolar", _sem_init))
    if semana_actual_init not in CATALOGO_SEMANAS_SEP:
        semana_actual_init = max(1, min(37, semana_actual_init))

    # Layout de proporción minimalista: Selectores de dosificación (izq) y Calendario compacto (der)
    col_ctrls, col_visual = st.columns([1.18, 0.82])

    with col_ctrls:
        c_modo, c_sel = st.columns([0.85, 1.15])
        with c_modo:
            modo_navegacion = st.selectbox(
                "Dosificar por:",
                options=["Semana SEP (1 a 37)", "Mes del Año 2026"],
                key=f"modo_cal_sel_{st.session_state.widget_key}",
                help="Elige si prefieres dosificar buscando directamente el número de semana SEP (1 a 37) o navegando por los meses del año 2026."
            )

        with c_sel:
            if modo_navegacion == "Semana SEP (1 a 37)":
                def format_sem_sep_label(s: int) -> str:
                    inf = CATALOGO_SEMANAS_SEP[s]
                    cte_tag = f" [📌 CTE]" if inf["tiene_cte"] else ""
                    return f"Semana {s} de 37 — {inf['rango_str']} ({inf['mes_nombre'][:3]} {inf['año']}){cte_tag}"

                semana_sep_sel = st.selectbox(
                    "🏫 Semana Escolar SEP (1 a 37):",
                    options=list(range(1, 38)),
                    index=semana_actual_init - 1,
                    format_func=format_sem_sep_label,
                    key=f"sel_semana_sep_{st.session_state.widget_key}",
                    help="Semana oficial del ciclo escolar SEP (185 días efectivos de clase)."
                )
                info_semana = CATALOGO_SEMANAS_SEP[semana_sep_sel]
                cal_mes_actual = info_semana["mes_nombre"]
                m_idx = info_semana["mes_idx"]
                cal_año_actual = info_semana["año"]
                rango_fechas_str = info_semana["rango_str"]
                active_week_dates = [d["date"] for d in info_semana["dias_habil"]]
                st.session_state.cal_semana_escolar = semana_sep_sel
                st.session_state.cal_mes_nombre = cal_mes_actual
                semana_seleccionada = semana_sep_sel
                periodo_sel = f"Semana {semana_seleccionada} de 37"
            else:
                idx_mes_actual = MESES_2026.index(st.session_state.get("cal_mes_nombre", "Octubre"))
                cal_mes_actual = st.selectbox(
                    "📅 Mes del Ciclo Escolar (2026-2027):",
                    options=MESES_2026,
                    index=idx_mes_actual,
                    key=f"sel_mes_cal_{st.session_state.widget_key}"
                )
                st.session_state.cal_mes_nombre = cal_mes_actual
                m_idx = MESES_2026.index(cal_mes_actual) + 1
                # En el ciclo 2026-2027: Agosto a Diciembre corresponden a 2026; Enero a Julio corresponden a 2027
                cal_año_actual = 2026 if cal_mes_actual in ["Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"] else 2027
                cal_obj = calendar.Calendar(firstweekday=0)
                month_weeks = cal_obj.monthdatescalendar(cal_año_actual, m_idx)

                # Filtrar semanas con presencia en este mes
                valid_week_indices = []
                for idx_w, w_d in enumerate(month_weeks):
                    if sum(1 for d in w_d[:5] if d.month == m_idx) >= 3:
                        valid_week_indices.append(idx_w)
                if not valid_week_indices:
                    valid_week_indices = list(range(len(month_weeks)))

                def format_sem_label(idx_w: int) -> str:
                    w_d = month_weeks[idx_w]
                    lun = w_d[0]
                    vie = w_d[4]
                    vac_info = es_fecha_vacaciones(lun) and es_fecha_vacaciones(vie)
                    sem_num = (
                        CATALOGO_FECHAS_SEP.get((lun.year, lun.month, lun.day))
                        or CATALOGO_FECHAS_SEP.get((lun.month, lun.day))
                        or CATALOGO_FECHAS_SEP.get((vie.year, vie.month, vie.day))
                        or CATALOGO_FECHAS_SEP.get((vie.month, vie.day))
                    )
                    tiene_cte = any(d in FECHAS_CTE_OFICIALES for d in w_d[:5])
                    cte_tag = " [📌 CTE]" if tiene_cte else ""
                    if vac_info:
                        vac = es_fecha_vacaciones(lun)
                        return f"🏖️ {vac['nombre']} ({lun.day}-{vie.day} {MESES_2026[lun.month-1][:3]} {lun.year})"
                    elif sem_num:
                        return f"Semana {sem_num} de 37 ({lun.day} al {vie.day} {MESES_2026[lun.month-1][:3]} {lun.year}){cte_tag}"
                    else:
                        return f"Bloque {idx_w + 1} ({lun.day}-{vie.day} {MESES_2026[lun.month-1][:3]} {lun.year}){cte_tag}"

                current_sem_idx = st.session_state.get("cal_sem_idx", valid_week_indices[0])
                if current_sem_idx not in valid_week_indices:
                    current_sem_idx = valid_week_indices[0]

                cal_sem_idx = st.selectbox(
                    "📆 Bloque Semanal en el Mes:",
                    options=valid_week_indices,
                    format_func=format_sem_label,
                    index=valid_week_indices.index(current_sem_idx),
                    key=f"sel_sem_mes_{st.session_state.widget_key}"
                )
                st.session_state.cal_sem_idx = cal_sem_idx
                active_week_full = month_weeks[cal_sem_idx]
                active_week_dates = active_week_full[:5]
                lun_d = active_week_dates[0]
                vie_d = active_week_dates[4]
                sem_detectada = (
                    CATALOGO_FECHAS_SEP.get((lun_d.year, lun_d.month, lun_d.day))
                    or CATALOGO_FECHAS_SEP.get((lun_d.month, lun_d.day))
                    or CATALOGO_FECHAS_SEP.get((vie_d.year, vie_d.month, vie_d.day))
                    or CATALOGO_FECHAS_SEP.get((vie_d.month, vie_d.day))
                    or 1
                )
                semana_sep_sel = sem_detectada
                info_semana = CATALOGO_SEMANAS_SEP[semana_sep_sel]
                st.session_state.cal_semana_escolar = semana_sep_sel
                semana_seleccionada = semana_sep_sel
                periodo_sel = f"Semana {semana_seleccionada} de 37"
                rango_fechas_str = f"{lun_d.day} {MESES_2026[lun_d.month-1][:3]} al {vie_d.day} {MESES_2026[vie_d.month-1][:3]}"

        # Detección de cambio de semana o bloque escolar para evitar arrastre de estados previos
        semana_previa = st.session_state.get("semana_activa_previa")
        if semana_previa is not None and semana_previa != semana_sep_sel:
            limpiar_estado_planeacion(nueva_semana=semana_sep_sel, reset_completo=False)
            st.session_state["aviso_cambio_semana"] = f"Semana {semana_sep_sel} de 37"
            st.rerun()
        else:
            st.session_state["semana_activa_previa"] = semana_sep_sel

        fechas_bloque = {
            nom: active_week_dates[i] for i, nom in enumerate(DIAS_HABIL_NOMBRES)
        }

        # Botones rápidos / atajos de selección en una sola línea compacta
        st.markdown("<div style='font-size: 0.78rem; font-weight: 600; color: #4B5563; margin-top: 0.35rem; margin-bottom: 0.15rem;'>⚡ Atajos de Días:</div>", unsafe_allow_html=True)
        col_q1, col_q2, col_q3, col_q4 = st.columns(4)
        with col_q1:
            if st.button("Lun-Vie", key=f"btn_cal_all_{st.session_state.widget_key}", help="Seleccionar los 5 días hábiles"):
                st.session_state.dias_seleccionados = DIAS_HABIL_NOMBRES.copy()
                st.rerun()
        with col_q2:
            if st.button("Lun, Mié, Vie", key=f"btn_cal_lmv_{st.session_state.widget_key}", help="Seleccionar Lunes, Miércoles y Viernes"):
                st.session_state.dias_seleccionados = ["Lunes", "Miércoles", "Viernes"]
                st.rerun()
        with col_q3:
            if st.button("Mar y Jue", key=f"btn_cal_mj_{st.session_state.widget_key}", help="Seleccionar Martes y Jueves"):
                st.session_state.dias_seleccionados = ["Martes", "Jueves"]
                st.rerun()
        with col_q4:
            if st.button("Solo Lun", key=f"btn_cal_lun_{st.session_state.widget_key}", help="Seleccionar únicamente Lunes"):
                st.session_state.dias_seleccionados = ["Lunes"]
                st.rerun()

        # Casillas compactas para días
        col_dias_chk = st.columns(5)
        dias_elegidos = []
        dias_fechas_calculadas = {}
        dias_previos = st.session_state.get("dias_seleccionados", DIAS_HABIL_NOMBRES)

        for idx_d, nom_d in enumerate(DIAS_HABIL_NOMBRES):
            dt_obj = fechas_bloque[nom_d]
            mes_dt_nom = MESES_2026[dt_obj.month - 1]
            chk_label = f"**{nom_d[:3]}** {dt_obj.day}"
            fecha_completa = f"{nom_d} {dt_obj.day} de {mes_dt_nom} de {dt_obj.year}"
            with col_dias_chk[idx_d]:
                is_checked = st.checkbox(
                    chk_label,
                    value=(nom_d in dias_previos),
                    key=f"chk_dia_{nom_d}_{st.session_state.widget_key}"
                )
                if is_checked:
                    dias_elegidos.append(nom_d)
                    dias_fechas_calculadas[nom_d] = fecha_completa

        if not dias_elegidos:
            dias_elegidos = ["Lunes"]
            dt_lun = fechas_bloque["Lunes"]
            dias_fechas_calculadas["Lunes"] = f"Lunes {dt_lun.day} de {MESES_2026[dt_lun.month - 1]} de {dt_lun.year}"

        dias_seleccionados = dias_elegidos
        st.session_state.dias_seleccionados = dias_seleccionados
        st.session_state.dias_fechas = dias_fechas_calculadas

        # Actualizar datos_escuela_actual y proyecto de la semana
        proyecto_semana_actual = obtener_proyecto_semana(semana_seleccionada, mes=cal_mes_actual)
        st.session_state["proyecto_semana_actual"] = proyecto_semana_actual
        datos_escuela_actual["dias_seleccionados"] = dias_seleccionados
        datos_escuela_actual["dias_planeados"] = dias_seleccionados
        datos_escuela_actual["dias_fechas"] = dias_fechas_calculadas
        datos_escuela_actual["semana"] = semana_seleccionada
        datos_escuela_actual["semana_seleccionada"] = semana_seleccionada
        datos_escuela_actual["mes"] = cal_mes_actual
        datos_escuela_actual["año"] = cal_año_actual
        datos_escuela_actual["proyecto_semana"] = proyecto_semana_actual
        datos_escuela_actual["periodo"] = periodo_sel

    # Visualización gráfica compacta del mes actual en col_visual
    with col_visual:
        cal_obj_vis = calendar.Calendar(firstweekday=0)
        vis_year = cal_año_actual if 'cal_año_actual' in locals() else 2026
        month_weeks_vis = cal_obj_vis.monthdatescalendar(vis_year, m_idx)
        fechas_activas_set = set(fechas_bloque[d] for d in dias_seleccionados)
        cal_html_rows = []
        for w in month_weeks_vis:
            cells = []
            for d in w:
                if d.month != m_idx:
                    cells.append(f'<td class="cal-mini-empty">{d.day}</td>')
                elif d in fechas_activas_set:
                    cells.append(f'<td class="cal-mini-active" title="Día seleccionado: {d.day} de {cal_mes_actual}"><strong>{d.day}</strong></td>')
                elif d in FECHAS_CTE_OFICIALES:
                    cte_desc = FECHAS_CTE_OFICIALES[d]
                    cells.append(f'<td class="cal-mini-cte" title="{cte_desc}">📌{d.day}</td>')
                elif es_fecha_vacaciones(d):
                    vac = es_fecha_vacaciones(d)
                    vac_nom = vac["nombre"]
                    cells.append(f'<td class="cal-mini-vac" title="{vac_nom}">{d.day}</td>')
                elif d.weekday() >= 5:
                    cells.append(f'<td class="cal-mini-wend">{d.day}</td>')
                else:
                    cells.append(f'<td>{d.day}</td>')
            cal_html_rows.append('<tr>' + ''.join(cells) + '</tr>')

        cal_tabla_html = f"""
        <div class="cal-mini-wrap">
            <div class="cal-mini-title">
                <span>{cal_mes_actual.upper()} {vis_year}</span>
                <span class="cal-mini-badge">Semana {semana_seleccionada} de 37</span>
            </div>
            <table class="cal-mini-table">
                <thead><tr><th>L</th><th>M</th><th>M</th><th>J</th><th>V</th><th>S</th><th>D</th></tr></thead>
                <tbody>{''.join(cal_html_rows)}</tbody>
            </table>
            <div class="cal-mini-legend">
                <span><span class="cal-mini-legend-dot" style="background: #7C3AED;"></span>Activo</span>
                <span><span class="cal-mini-legend-dot" style="background: #FFFFFF; border: 1px solid #CBD5E1;"></span>Hábil</span>
                <span><span class="cal-mini-legend-dot" style="background: #FEF3C7; border: 1px solid #F59E0B;"></span>Vacaciones</span>
                <span><span class="cal-mini-legend-dot" style="background: #FCE7F3; border: 1px solid #F472B6;"></span>CTE</span>
                <span><span class="cal-mini-legend-dot" style="background: #94A3B8;"></span>Fin sem</span>
            </div>
        </div>
        """
        st.markdown(cal_tabla_html, unsafe_allow_html=True)

    # Resumen inferior con contraste reforzado y texto oscuro #111111 en la píldora de sesiones
    cte_aviso_html = ""
    if info_semana.get("tiene_cte"):
        cte_aviso_html = f"<span style='background: #FCE7F3; color: #9D174D; border: 1px solid #F472B6; padding: 2px 8px; border-radius: 9999px; font-size: 0.76rem; font-weight: 700; margin-left: 6px;'>📌 {info_semana['cte_nombre']}</span>"

    st.markdown(
        f"""
        <div style="background: #F5F3FF; border: 1px solid #DDD6FE; border-radius: 10px; padding: 0.55rem 0.9rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-top: 0.6rem;">
            <div style="font-size: 0.86rem; color: #4C1D95; font-weight: 600;">
                🗓️ <b>Semana {semana_seleccionada} de 37 SEP</b> ({rango_fechas_str} {info_semana.get('año', 2026)}) {cte_aviso_html} <span style="color: #6D28D9; font-weight: normal; margin-left: 6px;">| Días activos: {', '.join(dias_seleccionados)}</span>
            </div>
            <div>
                <span class="badge-sesiones-count" style="background-color: #DDD6FE !important; color: #111111 !important; -webkit-text-fill-color: #111111 !important; font-weight: 800 !important; font-size: 0.82rem !important; padding: 3px 12px !important; border-radius: 9999px !important; border: 1px solid #7C3AED !important; display: inline-block !important;">
                    {len(dias_seleccionados)} Sesión(es) Didáctica(s)
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    # ==========================================
    # SECCIÓN 2: CAMPOS EDITABLES DE CONFIGURACIÓN CURRICULAR (SEP - NEM)
    # ==========================================
    st.markdown("""
    <div class="nem-card-header">
        <span style="color: #7C3AED; font-size: 1.5rem; line-height: 1;">•</span>
        <h3 class="nem-card-title">2. Configuración Curricular Oficial (SEP - México)</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_campos, col_metodo = st.columns([1, 1.2])
    
    with col_campos:
        st.markdown("**Campos Formativos Involucrados:**")
        campos_sel = st.multiselect(
            "Selecciona uno o más Campos Formativos:",
            options=CAMPOS_FORMATIVOS,
            default=CAMPOS_FORMATIVOS,
            help="La NEM promueve la interdisciplinariedad articulando los 4 Campos Formativos en un proyecto integrador.",
            key=f"campos_{st.session_state.widget_key}"
        )
    
        st.markdown("**Ejes Articuladores en Acción:**")
        ejes_sel = st.multiselect(
            "Selecciona los Ejes Articuladores que guían el proyecto:",
            options=EJES_ARTICULADORES,
            default=["Pensamiento crítico", "Vida saludable", "Apropiación de las culturas a través de la lectura y la escritura"],
            help="Los ejes articuladores conectan los contenidos con la realidad cotidiana de los alumnos y la comunidad.",
            key=f"ejes_{st.session_state.widget_key}"
        )
    
    with col_metodo:
        st.markdown("**Metodología Sociocrítica Oficial:**")
        metodologia_sel = st.selectbox(
            "Selecciona la metodología de trabajo pedagógico:",
            options=list(METODOLOGIAS_SOCIOCRITICAS.keys()),
            index=0,
            help="Metodologías oficiales propuestas por la SEP para cada campo formativo.",
            key=f"metodologia_{st.session_state.widget_key}"
        )
    
        # Mostrar información didáctica de la metodología elegida
        metodo_info = METODOLOGIAS_SOCIOCRITICAS.get(metodologia_sel, {})
        with st.expander("Ver descripción y fases metodológicas de esta metodología", expanded=True):
            st.markdown(f"*{metodo_info.get('descripcion', '')}*")
            st.markdown("**Fases y Momentos oficiales:**")
            for f in metodo_info.get("fases_oficiales", []):
                st.markdown(f"- {f}")
    
    # ==========================================
    # CUADERNILLO DE ACTIVIDADES: SEMANAS 6 Y 7 (PROFA KEMPIS)
    # ==========================================
    es_kempis_pertinente = detectar_relevancia_kempis(
        semana=semana_seleccionada,
        directrices_o_texto=st.session_state.get(f"directrices_{st.session_state.widget_key}", "")
    )
    sem_kempis_sug = 7 if (semana_seleccionada == 7) else 6
    kempis_data_sug = obtener_recursos_kempis_por_semana(sem_kempis_sug)

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    with st.expander(
        f"📘 Cuadernillo de Actividades y Recursos de Apoyo (Semanas 6 y 7 — Profa Kempis)" + (" ⭐ [Sugerido para esta semana]" if semana_seleccionada in [6, 7] else ""),
        expanded=(semana_seleccionada in [6, 7] or es_kempis_pertinente)
    ):
        st.markdown(
            f"""
            <div style="background-color: #F5F3FF; border: 1.5px solid #8B5CF6; border-radius: 8px; padding: 12px 16px; margin-bottom: 12px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span style="font-size: 1.3rem;">🌟</span>
                    <span style="font-weight: 700; font-size: 1rem; color: #4C1D95;">Cuadernillo Didáctico Oficial: {kempis_data_sug['titulo_general']}</span>
                </div>
                <div style="font-size: 0.86rem; color: #1F2937; line-height: 1.45;">
                    Contenidos y temas integrados: <b>Textos literarios, cuentos, lectura dramatizada, alimentos procesados, grasas, sellos NOM-051, múltiplos y submúltiplos del gramo, Plato del Bien Comer, servicios públicos, impuestos, IVA (16%), calidad de vida, resolución pacífica de conflictos, convivencia sana, Descubrimiento de América y Día Mundial de la Alimentación</b>.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        col_k1, col_k2 = st.columns(2)
        campos_sug_items = list(kempis_data_sug["campos"].items())
        with col_k1:
            st.markdown(f"**📚 Actividades y Fichas Imprimibles (Bloque A):**")
            for c_nom, c_val in campos_sug_items[:2]:
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid #7C3AED; border-radius: 8px; padding: 10px 12px; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                    <div style="font-weight: 700; font-size: 0.88rem; color: #1F2937;">{c_nom}: <span style="font-weight: 600; color: #374151;">{c_val['tema']}</span></div>
                    <div style="font-size: 0.80rem; color: #1F2937; margin-top: 4px;"><b>Ficha:</b> <code style="color: #6D28D9; background: #EDE9FE; padding: 2px 6px; border-radius: 4px;">{c_val['anexo_nombre']}</code></div>
                </div>
                """, unsafe_allow_html=True)

        with col_k2:
            st.markdown(f"**📚 Actividades y Fichas Imprimibles (Bloque B):**")
            for c_nom, c_val in campos_sug_items[2:]:
                st.markdown(f"""
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 4px solid #059669; border-radius: 8px; padding: 10px 12px; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.03);">
                    <div style="font-weight: 700; font-size: 0.88rem; color: #1F2937;">{c_nom}: <span style="font-weight: 600; color: #374151;">{c_val['tema']}</span></div>
                    <div style="font-size: 0.80rem; color: #1F2937; margin-top: 4px;"><b>Ficha:</b> <code style="color: #047857; background: #D1FAE5; padding: 2px 6px; border-radius: 4px;">{c_val['anexo_nombre']}</code></div>
                </div>
                """, unsafe_allow_html=True)
            ef_info = kempis_data_sug.get("efemeride_principal", {})
            if ef_info:
                st.markdown(f"""
                <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-left: 4px solid #D97706; border-radius: 8px; padding: 10px 12px; margin-bottom: 8px;">
                    <div style="font-weight: 700; font-size: 0.88rem; color: #1F2937;">🇲🇽 {ef_info.get('nombre', '')}</div>
                    <div style="font-size: 0.80rem; color: #92400E; margin-top: 2px;">Ficha: <code>{ef_info.get('anexo_nombre', '')}</code></div>
                </div>
                """, unsafe_allow_html=True)

        vincular_kempis_sel = st.checkbox(
            f"✅ Vincular e integrar automáticamente el Cuadernillo Profa Kempis (Semana {sem_kempis_sug}) en las secuencias didácticas (Inicio, Desarrollo, Cierre), Recursos y descargable en Word",
            value=True,
            key=f"chk_kempis_{st.session_state.widget_key}",
            help="Al mantener marcada esta casilla, las secuencias didácticas, los retos de cálculo mental/gramos/IVA, las preguntas de inicio, las fichas y el Word incluirán estas actividades."
        )

    # Articulación Curricular: Contenidos y PDA (100% Dinámico por Grado y Fase)
    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    st.markdown('#### <span style="color: #7C3AED; font-size: 1.2rem;">•</span> Articulación Curricular: Contenidos y Procesos de Desarrollo de Aprendizaje (PDA)', unsafe_allow_html=True)
    
    # Subtítulo y encabezado dinámicos según el grado y fase seleccionados
    st.subheader(f"Selecciona los Contenidos y PDA de {grado_seleccionado} recomendados para tu planeación (puedes personalizarlos abajo):")
    st.markdown(f"**Banco curricular sugerido para {fase_correspondiente} / {grado_seleccionado}:**")
    
    # Extraer el banco de contenidos y PDA correspondiente exclusivamente al grado activo
    banco_grado_activo = CONTENIDOS_PDA_POR_GRADO.get(
        grado_seleccionado,
        CONTENIDOS_PDA_POR_GRADO.get("6° de Primaria", {})
    )
    
    # Pre-poblar según los campos formativos elegidos para el grado activo
    sugerencias_pda = []

    # Función auxiliar para normalizar nombres de campos formativos
    def normalizar_campo_nombre(c_str: str) -> str:
        c_low = (c_str or "").strip().lower()
        for cf in CAMPOS_FORMATIVOS:
            if cf.lower() in c_low or c_low in cf.lower():
                return cf
        return c_str

    # 1. Integración de Contenidos y PDA del Programa Sintético Subido (Base de Datos Oficial Fase 5 - 5° y 6° Grado)
    pda_doc_subido = st.session_state.get("pda_extraidos_programa", [])
    if pda_doc_subido:
        for item in pda_doc_subido:
            c_item = normalizar_campo_nombre(item.get("campo", "Lenguajes"))
            if not campos_sel or c_item in campos_sel:
                sugerencias_pda.append({
                    "campo": c_item,
                    "contenido": item.get("contenido", ""),
                    "pda": item.get("pda", ""),
                    "grado": item.get("grado", grado_seleccionado),
                    "origen": "Programa Sintético Fase 5 (Oficial Subido)"
                })

    for campo in campos_sel:
        if campo in banco_grado_activo:
            for item in banco_grado_activo[campo]:
                if not any(s["contenido"] == item["contenido"] and s["pda"] == item["pda"] for s in sugerencias_pda):
                    sugerencias_pda.append({
                        "campo": campo,
                        "contenido": item["contenido"],
                        "pda": item["pda"],
                        "grado": grado_seleccionado,
                        "origen": "Banco Curricular SEP"
                    })

    if st.session_state.get("programa_sintetico_subido"):
        nom_db = st.session_state.get("nombre_archivo_programa") or "Programa_Sintetico_Fase_5.pdf"
        st.markdown(
            f"<div style='background-color: #ECFDF5; border: 1.5px solid #10B981; border-radius: 8px; padding: 0.65rem 1rem; margin-bottom: 0.8rem; color: #065F46; font-weight: 600; font-size: 0.95rem;'>"
            f"🟢 <b>Base de Datos Principal y Oficial Activa:</b> <code>{nom_db}</code>. Contenidos y PDA de {grado_seleccionado} vinculados prioritariamente."
            f"</div>",
            unsafe_allow_html=True
        )

    if sugerencias_pda:
        opciones_display = []
        for item in sugerencias_pda:
            if "Programa Sintético Fase 5" in item.get("origen", ""):
                opciones_display.append(f"⭐ [Oficial {grado_seleccionado[:2]} - {item['campo']}] {item['contenido'][:55]}... — PDA: {item['pda'][:65]}...")
            else:
                opciones_display.append(f"[{item['campo']}] {item['contenido'][:60]}... — PDA: {item['pda'][:70]}...")

        # Predeterminar un PDA representativo de cada uno de los Campos Formativos seleccionados para transversalidad plena
        default_indices_pda = []
        pda_guardados = st.session_state.get("pda_cargados")
        if pda_guardados:
            matched_indices = []
            for item_p in pda_guardados:
                c_nom = (item_p.get("contenido") or "").strip().lower()
                p_nom = (item_p.get("pda") or "").strip().lower()
                for idx_s, sug in enumerate(sugerencias_pda):
                    s_c = sug.get("contenido", "").strip().lower()
                    s_p = sug.get("pda", "").strip().lower()
                    if (c_nom and (c_nom[:30] in s_c or s_c[:30] in c_nom)) or (p_nom and (p_nom[:30] in s_p or s_p[:30] in p_nom)):
                        if idx_s not in matched_indices:
                            matched_indices.append(idx_s)
                        break
            if matched_indices:
                default_indices_pda = matched_indices

        if not default_indices_pda:
            # Si corresponde a Semana 6 o 7 o temas Kempis, priorizar PDA afines
            if semana_seleccionada in [6, 7] or es_kempis_pertinente:
                kempis_keywords = ["texto literario", "cuento", "dramatiz", "alimento", "gramo", "proporcionalidad", "iva", "servicio", "paz", "conflicto", "estilos de vida", "12 de octubre", "1910"]
                campos_vistos = set()
                for idx_sug, sug_item in enumerate(sugerencias_pda):
                    c_sug = sug_item.get("campo")
                    c_txt = (sug_item.get("contenido", "") + " " + sug_item.get("pda", "")).lower()
                    if c_sug not in campos_vistos and any(kw in c_txt for kw in kempis_keywords):
                        campos_vistos.add(c_sug)
                        default_indices_pda.append(idx_sug)

            if not default_indices_pda:
                campos_vistos = set()
                for idx_sug, sug_item in enumerate(sugerencias_pda):
                    c_sug = sug_item.get("campo")
                    if c_sug not in campos_vistos:
                        campos_vistos.add(c_sug)
                        default_indices_pda.append(idx_sug)
                    if len(default_indices_pda) >= (len(campos_sel) if campos_sel else 4):
                        break

        if not default_indices_pda and sugerencias_pda:
            default_indices_pda = list(range(min(4, len(sugerencias_pda))))

        pda_seleccionados_indices = st.multiselect(
            f"Contenidos y PDA oficiales disponibles para {grado_seleccionado}:",
            options=range(len(sugerencias_pda)),
            format_func=lambda x: opciones_display[x],
            default=default_indices_pda,
            key=f"pda_{st.session_state.widget_key}",
            help=f"Mostrando los Contenidos y PDA oficiales del programa sintético para {grado_seleccionado} ({fase_correspondiente})."
        )
        items_pda_final = [sugerencias_pda[i] for i in pda_seleccionados_indices]

    else:
        items_pda_final = []
        st.info(f"No hay Contenidos y PDA precargados para los campos formativos seleccionados en {grado_seleccionado}. Puedes redactarlos abajo.")
    
    # Área para agregar o editar Contenido y PDA manuales
    tiene_pda_custom_cargado = bool(st.session_state.get(f"contenidos_{st.session_state.widget_key}"))
    with st.expander(f"Personalizar o escribir Contenidos y PDA manualmente para {grado_seleccionado}", expanded=(len(items_pda_final) == 0 or tiene_pda_custom_cargado)):
        val_cont_def = items_pda_final[0]["contenido"] if items_pda_final else (sugerencias_pda[0]["contenido"] if sugerencias_pda else f"Contenido sintético para {grado_seleccionado}.")
        val_pda_def = items_pda_final[0]["pda"] if items_pda_final else (sugerencias_pda[0]["pda"] if sugerencias_pda else f"Procesos de Desarrollo de Aprendizaje para {grado_seleccionado}.")
        activar_pda_manual = st.checkbox(
            "✍️ Reemplazar Contenidos y PDA oficiales por redacción manual personalizada",
            value=(len(items_pda_final) == 0 or tiene_pda_custom_cargado),
            key=f"chk_pda_manual_{st.session_state.widget_key}",
            help="Marca esta casilla si deseas ignorar los Contenidos y PDA oficiales seleccionados arriba y redactar tus propios contenidos específicos."
        )
        contenido_custom = st.text_area(
            f"Contenido Sintético personalizado ({grado_seleccionado}):",
            value="",
            placeholder=val_cont_def,
            height=80,
            key=f"contenidos_{st.session_state.widget_key}"
        )
        pda_custom = st.text_area(
            f"Procesos de Desarrollo de Aprendizaje (PDA) personalizados ({grado_seleccionado}):",
            value="",
            placeholder=val_pda_def,
            height=100,
            key=f"custom_pda_{st.session_state.widget_key}"
        )
        if activar_pda_manual and (contenido_custom.strip() or pda_custom.strip()):
            items_pda_final = [{
                "campo": campos_sel[0] if campos_sel else "Lenguajes",
                "contenido": contenido_custom.strip() if contenido_custom.strip() else val_cont_def,
                "pda": pda_custom.strip() if pda_custom.strip() else val_pda_def
            }]
        elif len(items_pda_final) == 0:
            items_pda_final = [{
                "campo": campos_sel[0] if campos_sel else "Lenguajes",
                "contenido": contenido_custom.strip() if contenido_custom.strip() else val_cont_def,
                "pda": pda_custom.strip() if pda_custom.strip() else val_pda_def
            }]
    
    col_sesiones, col_espacio = st.columns([1, 2])
    with col_sesiones:
        num_sesiones = st.slider(
            "Número de Sesiones Didácticas a desarrollar:",
            min_value=1,
            max_value=10,
            value=max(1, len(dias_seleccionados)) if dias_seleccionados else 1,
            step=1,
            help="Calculado automáticamente según los días de la semana seleccionados a planear.",
            key=f"num_sesiones_{st.session_state.widget_key}"
        )
    
    # ==========================================
    # SECCIÓN 2.5: PLANIFICACIÓN Y CAPTURA DÍA POR DÍA (PESTAÑAS)
    # ==========================================
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="nem-card-header">
        <span style="color: #7C3AED; font-size: 1.5rem; line-height: 1;">•</span>
        <h3 class="nem-card-title">Secuencia y Captura Pedagógica Día por Día</h3>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Organización modular en pestañas independientes para cada día. Consulta y ajusta la rutina matutina y los momentos de la clase (Inicio, Desarrollo y Cierre) de forma limpia y enfocada, sin saturar la pantalla.")

    dias_activos_tabs = dias_seleccionados if dias_seleccionados else DIAS_HABIL_NOMBRES
    tabs_dias_captura = st.tabs([f"📅 {d}" for d in dias_activos_tabs])

    dias_fechas_map = st.session_state.get("dias_fechas", {})
    plan_guardado_actual = st.session_state.get("planeacion_generada")
    parsed_actual = parse_plan_sections(plan_guardado_actual) if plan_guardado_actual else {}

    proyecto_semana_actual = obtener_proyecto_semana(semana_seleccionada, mes=st.session_state.get('cal_mes_nombre'))
    st.session_state["proyecto_semana_actual"] = proyecto_semana_actual

    for idx_dia, (tab_d, nom_dia) in enumerate(zip(tabs_dias_captura, dias_activos_tabs)):
        with tab_d:
            fecha_dia_label = dias_fechas_map.get(nom_dia, f"{nom_dia} (Semana {semana_seleccionada})")
            anexo_del_dia = obtener_anexos_por_semana_y_dia(semana_seleccionada, nom_dia, mes=st.session_state.get('cal_mes_nombre'))
            
            # Obtener datos de rutina y sesión correspondientes a este día
            r_dia = parsed_actual.get("rutinas_por_dia", {}).get(nom_dia)
            if not r_dia and idx_dia < len(parsed_actual.get("rutinas", [])):
                r_dia = parsed_actual["rutinas"][idx_dia]

            s_dia = parsed_actual.get("sesiones_por_dia", {}).get(nom_dia)
            if not s_dia and idx_dia < len(parsed_actual.get("sesiones", [])):
                s_dia = parsed_actual["sesiones"][idx_dia]

            # Pre-cargar con el catálogo dinámico de la semana si aún no hay planeación generada
            if not r_dia:
                r_dictados = proyecto_semana_actual.get("rutinas_matutinas", {}).get("dictado", {})
                r_calc = proyecto_semana_actual.get("rutinas_matutinas", {}).get("calculo_mental", {})
                r_prob = proyecto_semana_actual.get("rutinas_matutinas", {}).get("problemas_razonados", {})
                dictado_val = r_dictados.get(nom_dia, f"Palabras clave reflexivas para {nom_dia} sobre {proyecto_semana_actual['proyecto']}.")
                calc_val = r_calc.get(nom_dia, f"Operaciones de cálculo mental contextualizadas para {nom_dia}.")
                prob_val = r_prob.get(nom_dia, f"Problema razonado de situaciones comunitarias en Durango.")
            else:
                dictado_val = r_dia.get("dictado", "")
                calc_val = r_dia.get("calculo", "")
                prob_val = r_dia.get("problema", "")

            if not s_dia:
                sec_dia = proyecto_semana_actual.get("secuencias_por_dia", {}).get(nom_dia, {})
                ini_val = sec_dia.get("inicio", f"Activación diagnóstica y planteamiento de detonadores para el proyecto '{proyecto_semana_actual['proyecto']}'.")
                des_val = sec_dia.get("desarrollo", f"Indagación práctica, análisis en comunidades de aprendizaje y resolución del {anexo_del_dia}.")
                cie_val = sec_dia.get("cierre", f"Puesta en común, balance de avances y reflexión comunitaria en asamblea.")
                rec_val = sec_dia.get("recursos", f"Libros de Texto Gratuitos (LTG), {anexo_del_dia}, libreta y materiales del aula.")
            else:
                ini_val = s_dia.get("inicio", "")
                des_val = s_dia.get("desarrollo", "")
                cie_val = s_dia.get("cierre", "")
                rec_val = s_dia.get("recursos", "")

            # Header visual del día con vinculación al proyecto y anexo
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #FAF5FF 0%, #F5F3FF 100%); border: 1.5px solid #DDD6FE; border-radius: 10px; padding: 10px 14px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                <div>
                    <div style="font-weight: 700; color: #4C1D95; font-size: 0.94rem;">
                        🗓️ <b>{fecha_dia_label}</b> — Sesión {idx_dia + 1} de {len(dias_activos_tabs)}
                    </div>
                    <div style="font-size: 0.8rem; color: #6D28D9; margin-top: 2px;">
                        🎯 <b>Proyecto:</b> {proyecto_semana_actual['proyecto']} • 📑 <b>Anexo:</b> {anexo_del_dia}
                    </div>
                </div>
                <div style="font-size: 0.76rem; background: #EDE9FE; color: #6D28D9; padding: 2px 8px; border-radius: 9999px; font-weight: 600;">
                    Semana {semana_seleccionada} SEP • {st.session_state.get('cal_mes_nombre', 'Octubre')}
                </div>
            </div>
            """, unsafe_allow_html=True)

            col_fijar, _ = st.columns([0.45, 0.55])
            with col_fijar:
                es_activo = (st.session_state.get("dia_activo_pestaña") == nom_dia)
                txt_btn = f"✓ Día Activo en Pestañas: {nom_dia}" if es_activo else f"🎯 Fijar {nom_dia} para Búsqueda Contextual"
                if st.button(txt_btn, key=f"btn_fijar_dia_{nom_dia}_{st.session_state.widget_key}", disabled=es_activo, use_container_width=True):
                    st.session_state.dia_activo_pestaña = nom_dia
                    st.rerun()

            col_dia_rutina, col_dia_secuencia = st.columns([1, 1.35])
            with col_dia_rutina:
                st.markdown(f"""
                <div class="day-moment-box">
                    <div class="day-moment-title">🌅 Rutina Matutina Permanente (15-20 min)</div>
                    <div class="day-moment-text">
                        <b>✍️ Dictado:</b> {dictado_val}<br><br>
                        <b>🔢 Cálculo Mental:</b> {calc_val}<br><br>
                        <b>🧩 Problema Razonado:</b> {prob_val}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_dia_secuencia:
                st.markdown(f"""
                <div class="day-moment-box" style="border-left-color: #059669;">
                    <div class="day-moment-title" style="color: #065F46;">🎯 Secuencia Didáctica (Inicio, Desarrollo y Cierre)</div>
                    <div class="day-moment-text">
                        <span style="color: #047857; font-weight: 700;">🟢 Inicio (15-20 min):</span><br>{ini_val}<br><br>
                        <span style="color: #B45309; font-weight: 700;">🟡 Desarrollo (50-60 min):</span><br>{des_val}<br><br>
                        <span style="color: #4C1D95; font-weight: 700;">🔴 Cierre (15-20 min):</span><br>{cie_val}<br><br>
                        <span style="color: #374151; font-weight: 700;">📦 Recursos:</span><br>{rec_val}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with st.expander(f"✏️ Notas y Ajustes Didácticos para {nom_dia}", expanded=False):
                st.text_area(
                    f"Ajuste personalizado para {nom_dia}:",
                    value="",
                    placeholder=f"Escribe aquí cualquier indicación específica o adecuación particular para la clase del {nom_dia}...",
                    key=f"nota_dia_{nom_dia}_{st.session_state.widget_key}",
                    height=70
                )

    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # ==========================================
    # AUTOGUARDADO EN TIEMPO REAL (SQLITE)
    # ==========================================
    docente_usuario_act = st.session_state.get("username", "docente")
    
    # Metadatos de guardado: nombre personalizado de archivo y carpeta/categoría
    default_campo_slug = re.sub(r'[^a-zA-Z0-9]', '', str(campos_sel[0])) if campos_sel else "Lenguajes"
    nombre_archivo_actual = st.session_state.get("nombre_archivo_actual")
    if not nombre_archivo_actual:
        nombre_archivo_actual = f"Planeacion_Semana_{semana_seleccionada}_{default_campo_slug}"
    
    default_cat_semana = (
        "Trimestre 1 (Diagnóstico e Inicio)" if semana_seleccionada <= 13
        else ("Trimestre 2 (Desarrollo y Proyectos)" if semana_seleccionada <= 26
        else "Trimestre 3 (Consolidación y Cierre)")
    )
    categoria_ruta_actual = st.session_state.get("categoria_ruta_actual", default_cat_semana)

    data_actual_para_guardar = {
        "semana": semana_seleccionada,
        "periodo": periodo_sel,
        "titulo": f"Semana {semana_seleccionada} ({periodo_sel}) — {', '.join(campos_sel[:2]) if campos_sel else 'NEM'}",
        "grado": grado_sel,
        "grupo": grupo_sel,
        "campos_formativos": campos_sel,
        "metodologia": metodologia_sel,
        "ejes_articuladores": ejes_sel,
        "contenidos_pda": items_pda_final,
        "libros_seleccionados": libros_sel,
        "guia_cte": guia_cte_sel,
        "dias_seleccionados": dias_seleccionados,
        "dias_fechas": st.session_state.get("dias_fechas", {}),
        "directrices": directrices_input,
        "num_sesiones": num_sesiones,
        "planeacion_generada": st.session_state.get("planeacion_generada") or "",
        "prompt_enviado": st.session_state.get("prompt_enviado") or "",
        "url_referencia": url_referencia if 'url_referencia' in locals() else "",
        "nombre_archivo": nombre_archivo_actual,
        "categoria_ruta": categoria_ruta_actual,
        "vincular_cuadernillo_kempis": vincular_kempis_sel if 'vincular_kempis_sel' in locals() else True
    }
    datos_escuela_actual["vincular_cuadernillo_kempis"] = data_actual_para_guardar["vincular_cuadernillo_kempis"]
    hash_actual_form = calcular_hash_planeacion(data_actual_para_guardar)
    if hash_actual_form != st.session_state.get("ultimo_hash_guardado"):
        guardar_planeacion(
            username=docente_usuario_act,
            data=data_actual_para_guardar,
            es_autoguardado=True,
            nombre_archivo=nombre_archivo_actual,
            categoria_ruta=categoria_ruta_actual
        )
        st.session_state["ultimo_hash_guardado"] = hash_actual_form
        st.session_state["ultimo_autoguardado_hora"] = datetime.datetime.now().strftime("%H:%M:%S")
        st.session_state["ultimo_autoguardado_semana"] = semana_seleccionada
    
    # ==========================================
    # FUNCIÓN DE MODO DE RESPALDO: PLANTILLA BASE SIN IA
    # ==========================================
    def generar_plantilla_base_sin_ia(
        datos_escuela: dict,
        campos_formativos: list,
        metodologia: str,
        ejes: list,
        contenidos_pda: list,
        libros_seleccionados: list,
        dias_seleccionados: list = None,
        directrices: str = "",
        num_sesiones: int = None
    ) -> str:
        """
        Genera la estructura oficial de la planeación sin invocar a la API de Gemini,
        prellenando todos los datos curriculares e institucionales seleccionados,
        incorporando los contenidos del Cuadernillo Profa Kempis si corresponde a Semanas 6 o 7,
        y estructurada estrictamente para los días seleccionados.
        """
        escuela = datos_escuela.get('nombre_escuela', 'Escuela Primaria “Revolución Social de 1910”')
        cct = datos_escuela.get('cct', '10EPR0361N')
        docente = datos_escuela.get('docente', 'Maestra Aday Domínguez Domínguez')
        director = datos_escuela.get('director', 'Guillermo Gerardo Borjas Díaz')
        grado = datos_escuela.get('grado', '6° de Primaria')
        fase = datos_escuela.get('fase', 'Fase 5')
        grupo = datos_escuela.get('grupo', 'A')
        periodo = datos_escuela.get('periodo', f"Semana {semana_seleccionada} de 37")
        ciclo = datos_escuela.get('ciclo_escolar', '2026-2027')
        turno = datos_escuela.get('turno', 'Matutino')
    
        if dias_seleccionados is None:
            dias_seleccionados = datos_escuela.get('dias_seleccionados') or datos_escuela.get('dias_planeados') or ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        if not dias_seleccionados:
            dias_seleccionados = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    
        if num_sesiones is None:
            num_sesiones = len(dias_seleccionados)
    
        libros_txt = ", ".join(str(libro) for libro in libros_seleccionados) if libros_seleccionados else "Libros de Texto Gratuitos (SEP - CONALITEG)"
        campos_txt = ", ".join(campos_formativos) if campos_formativos else "Campos Formativos por definir"
        ejes_txt = ", ".join(ejes) if ejes else "Ejes articuladores por definir"
        problemica_txt = directrices.strip() if directrices and directrices.strip() else EJEMPLO_PROBLEMICA_ANALITICO
    
        # Detección y vinculación dinámica del proyecto y anexos de la semana oficial SEP
        proyecto_info = obtener_proyecto_semana(semana_seleccionada, mes=st.session_state.get('cal_mes_nombre'))
        nombre_proyecto_def = f"{proyecto_info['proyecto']} — {proyecto_info.get('fase_metodologica', 'Proyecto Integrador Comunitario')}"

        # Preparar texto de contenidos y pda sintetizados para la tabla inicial
        if contenidos_pda:
            resumen_cont = " // ".join(f"[{item.get('campo', '')}] {item.get('contenido', '')}" for item in contenidos_pda)
            resumen_pda = " // ".join(f"[{item.get('campo', '')}] {item.get('pda', '')}" for item in contenidos_pda)
        else:
            resumen_cont = "[Redactar Contenido Sintético oficial del programa analítico]"
            resumen_pda = "[Redactar Procesos de Desarrollo de Aprendizaje (PDA)]"
    
        # Construir tabla curricular NEM
        filas_curricular = []
        if contenidos_pda:
            for item in contenidos_pda:
                c_campo = item.get("campo", campos_formativos[0] if campos_formativos else "Lenguajes")
                c_cont = item.get("contenido", "[Redactar contenido sintético]")
                c_pda = item.get("pda", "[Redactar PDA]")
                filas_curricular.append(f"| **{c_campo}** | {c_cont} | {c_pda} | {libros_txt} | Comprensión lectora, velocidad, ortografía y comunidad |")
        else:
            filas_curricular.append(f"| **{campos_txt}** | [Redactar Contenido Sintético aquí] | [Redactar PDA aquí] | {libros_txt} | [Articular problemáticas del Programa Analítico] |")
        
        tabla_curricular_md = "\n".join(filas_curricular)
    
        # Rutinas matutinas y secuencias didácticas generadas estrictamente para los días seleccionados
        dias_fechas = datos_escuela.get("dias_fechas", {}) if isinstance(datos_escuela, dict) else {}
        rutinas_md = ""
        secuencias_md = ""

        for s, nombre_dia in enumerate(dias_seleccionados, 1):
            fecha_dia = dias_fechas.get(nombre_dia, nombre_dia)
            anexo_dia = obtener_anexos_por_semana_y_dia(semana_seleccionada, nombre_dia, mes=st.session_state.get('cal_mes_nombre'))
            r_dictados = proyecto_info.get("rutinas_matutinas", {}).get("dictado", {})
            r_calculo = proyecto_info.get("rutinas_matutinas", {}).get("calculo_mental", {})
            r_problemas = proyecto_info.get("rutinas_matutinas", {}).get("problemas_razonados", {})

            dictado_txt = r_dictados.get(nombre_dia, f"Palabras clave reflexivas para {nombre_dia} con desafío ortográfico.")
            calculo_txt = r_calculo.get(nombre_dia, f"Operaciones de cálculo mental contextualizadas para {nombre_dia}.")
            problema_txt = r_problemas.get(nombre_dia, f"Problema razonado de situaciones comunitarias en Durango.")

            rutinas_md += f"""
### Sesión {s} ({fecha_dia}):
- **Dictado Ortográfico:** {dictado_txt}
- **Cálculo Mental:** {calculo_txt}
- **Problema Razonado:** {problema_txt}
"""
            sec_dia = proyecto_info.get("secuencias_por_dia", {}).get(nombre_dia, {})
            inicio_txt = sec_dia.get("inicio", f"Activación de conocimientos previos y planteamiento detonador para {nombre_dia}.")
            desarrollo_txt = sec_dia.get("desarrollo", f"Indagación práctica, análisis en comunidades de aprendizaje y resolución del anexo de la sesión: {anexo_dia}.")
            cierre_txt = sec_dia.get("cierre", "Puesta en común, balance de avances y reflexión comunitaria en asamblea de aula.")
            recursos_s = f"{libros_txt}, {anexo_dia} y libreta del alumno."
            evidencia_s = f"Ficha de trabajo completada: {anexo_dia}."

            secuencias_md += f"""
### Sesión {s} (**Día: {fecha_dia}**) - {proyecto_info['proyecto']} ({nombre_dia})
- **Tiempo estimado:** 90 minutos
- **Inicio (15-20 min):** {inicio_txt}
- **Desarrollo (50-60 min):** {desarrollo_txt}
- **Cierre (15-20 min):** {cierre_txt}
- **Recursos didácticos y materiales:** {recursos_s}
- **Evidencia / Producto de la sesión:** {evidencia_s}
"""
    
        dias_str = ", ".join(dias_fechas.get(d, d) for d in dias_seleccionados)
    
        return f"""# I. DATOS DE IDENTIFICACIÓN Y DOSIFICADOR GENERAL DEL PROYECTO
    
- **Nombre del Proyecto:** {nombre_proyecto_def}
- **Escuela:** {escuela} | **C.C.T.:** {cct} | **Turno:** {turno}
- **Docente:** Prof(a). {docente} | **Director:** Prof. {director}
- **Fase y Grado:** {fase} — {grado} Grupo '{grupo}'
- **Temporalidad:** {periodo} ({num_sesiones} sesiones: {dias_str}) | **Ciclo Escolar:** {ciclo}
- **Escenario:** Aula / Escolar / Comunitario
- **Metodología Sociocrítica:** {metodologia}
- **Ejes Articuladores:** {ejes_txt}
- **Libros de Texto Gratuitos (LTG):** {libros_txt}
- **Problemática del Plan Analítico:** {problemica_txt}
- **Propósito:** [Redactar el propósito formativo del proyecto aquí]
- **Contenido Sintético:** {resumen_cont}
- **PDA:** {resumen_pda}

---

# II. ARTICULACIÓN CURRICULAR TRANSVERSAL (TABLA NEM - 4 CAMPOS FORMATIVOS)

| Campo Formativo | Contenido Sintético | Procesos de Desarrollo de Aprendizaje (PDA) | Vinculación con Libros SEP (LTG) | Problemática Analítica Atendida |
| :--- | :--- | :--- | :--- | :--- |
{tabla_curricular_md}

---

# III. ACTIVIDADES DE INICIO DEL DÍA (RUTINA MATUTINA - SESIONES 1 A {num_sesiones})
{rutinas_md}

---

# IV. SECUENCIA DIDÁCTICA DETALLADA (PLANO DIDÁCTICO POR SESIONES)
{secuencias_md}

---

    
    # V. INSTRUMENTO DE EVALUACIÓN FORMATIVA
    
    ### Rúbrica Analítica de Desempeño ({fase} - {grado})
    
    | Criterio / Indicador de Logro | Nivel Sobresaliente | Nivel Satisfactorio | Nivel Básico | Requiere Apoyo |
    | :--- | :--- | :--- | :--- | :--- |
    | [Redactar criterio 1 de evaluación formativa] | [Desempeño sobresaliente] | [Desempeño satisfactorio] | [Desempeño básico] | [Requiere apoyo docente] |
    | [Redactar criterio 2 de evaluación formativa] | [Desempeño sobresaliente] | [Desempeño satisfactorio] | [Desempeño básico] | [Requiere apoyo docente] |
    
    ---
    
    # VI. AJUSTES RAZONABLES Y ATENCIÓN A LA DIVERSIDAD (BAP - DUA)
    - [Redactar ajustes razonables, apoyos visuales y adecuaciones DUA aquí]
    
    ---
    
    # VII. OBSERVACIONES GENERALES Y ESPACIO DE SEGUIMIENTO
    - [Espacio para notas del diario de clase y seguimiento directivo]
    """
    
    # ==========================================
    # SECCIÓN: BUSCADOR DE RECURSOS
    # ==========================================
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="nem-card-header">
        <span style="color: #7C3AED; font-size: 1.5rem; line-height: 1;">•</span>
        <h3 class="nem-card-title">Buscador de Recursos</h3>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Herramienta de consulta libre y directa en internet. Encuentra material didáctico, dinámicas, lecturas y recursos pedagógicos sin consumir tokens de Gemini ni requerir API Key.")
    
    dias_disponibles_busqueda = dias_seleccionados if dias_seleccionados else DIAS_HABIL_NOMBRES
    dia_actual_pestaña = st.session_state.get("dia_activo_pestaña", dias_disponibles_busqueda[0])
    dia_idx_sel = dias_disponibles_busqueda.index(dia_actual_pestaña) if dia_actual_pestaña in dias_disponibles_busqueda else 0

    col_q_dia, col_q_txt = st.columns([0.38, 0.62])
    with col_q_dia:
        dia_busqueda_sel = st.selectbox(
            "🗓️ Día para Búsqueda Contextual:",
            options=dias_disponibles_busqueda,
            index=dia_idx_sel,
            key=f"sel_dia_busqueda_{st.session_state.widget_key}",
            help="Selecciona el día específico para cruzarlo con el proyecto y el anexo correspondiente de la semana escolar 2026-2027."
        )
        st.session_state.dia_activo_pestaña = dia_busqueda_sel

    with col_q_txt:
        query_tema = st.text_input(
            "Tema, Contenido o PDA que deseas investigar:",
            placeholder="Escribe aquí el tema, Contenido o PDA (Ej. Alimentos procesados y sellos NOM-051, cálculo mental lúdico...)",
            key="query_busqueda"
        )

    anexo_dia_busqueda = obtener_anexos_por_semana_y_dia(semana_seleccionada, dia_busqueda_sel, mes=cal_mes_actual)
    # Badge dinámico contextual de fecha, proyecto y anexo
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%); border: 1.5px solid #CBD5E1; border-radius: 8px; padding: 7px 12px; margin-bottom: 8px; font-size: 0.82rem; color: #334155; display: flex; flex-wrap: wrap; gap: 10px; align-items: center;">
        <span>🏫 <b>Semana {semana_seleccionada} de 37 (SEP)</b></span>
        <span>📅 <b>Mes: {cal_mes_actual} {cal_año_actual}</b></span>
        <span>🗓️ <b>Día: {dia_busqueda_sel}</b></span>
        <span>🎯 <b>Proyecto:</b> {proyecto_semana_actual['proyecto']}</span>
        <span>📑 <b>Anexo Asignado:</b> {anexo_dia_busqueda}</span>
    </div>
    """, unsafe_allow_html=True)
    
    def limpiar_busqueda_callback():
        st.session_state.query_busqueda = ""
        st.session_state.resultados_busqueda_gratis = []
        st.session_state.query_busqueda_gratis = ""
    
    col_buscar, col_limpiar = st.columns([1, 1])
    with col_buscar:
        btn_buscar_gratis = st.button("Buscar en la Web", key="btn_ddgs_buscar", use_container_width=True)
    with col_limpiar:
        st.button("Limpiar Búsqueda", on_click=limpiar_busqueda_callback, key="btn_limpiar_busqueda", use_container_width=True)
    
    if btn_buscar_gratis:
        query_val = st.session_state.get("query_busqueda", "")
        if not query_val or not query_val.strip():
            st.warning("Por favor escribe el tema, Contenido o PDA que deseas investigar.")
        else:
            campo_formativo = campos_sel[0] if (campos_sel and len(campos_sel) > 0) else ""
            pda_o_contenido = query_val.strip()
            # Búsqueda contextualizada sin consultas estáticas
            query_busqueda = (
                f"actividades didácticas primaria Nueva Escuela Mexicana {grado_seleccionado} {campo_formativo} "
                f"Semana {semana_seleccionada} SEP {cal_mes_actual} {cal_año_actual} {dia_busqueda_sel} "
                f"proyecto '{proyecto_semana_actual['proyecto']}' {anexo_dia_busqueda} {pda_o_contenido}"
            )
            with st.spinner(f"Buscando recursos para {dia_busqueda_sel} (Semana {semana_seleccionada} SEP - {proyecto_semana_actual['proyecto']})..."):
                try:
                    try:
                        from duckduckgo_search import DDGS
                    except ImportError:
                        from ddgs import DDGS
    
                    ddgs_client = DDGS()
                    resultados_ddgs = list(ddgs_client.text(query_busqueda, max_results=8))
                    if not resultados_ddgs:
                        from ddgs import DDGS as DDGS_FALLBACK
                        resultados_ddgs = list(DDGS_FALLBACK().text(query_busqueda, max_results=8))
    
                    st.session_state.resultados_busqueda_gratis = resultados_ddgs
                    st.session_state.query_busqueda_gratis = query_val.strip()
                    st.session_state.query_busqueda_enriquecida = query_busqueda
                except Exception as e:
                    st.error(f"Error al realizar la búsqueda web gratuita: {str(e)}")
    
    if "resultados_busqueda_gratis" in st.session_state and st.session_state.resultados_busqueda_gratis:
        st.markdown(f"**Resultados web encontrados para:** *{st.session_state.get('query_busqueda_gratis', '')}*")
        for idx, item in enumerate(st.session_state.resultados_busqueda_gratis[:10], 1):
            r_title = item.get("title", "Recurso educativo")
            r_url = item.get("href") or item.get("link", "#")
            r_body = item.get("body") or item.get("snippet", "Sin descripción disponible.")
            
            st.markdown(f"""
            <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.9rem 1.2rem; margin-bottom: 0.75rem;">
                <div style="font-weight: 600; font-size: 0.98rem; color: #1E293B;">
                    {idx}. <a href="{r_url}" target="_blank" style="color: #691C32; text-decoration: underline;">{r_title}</a>
                </div>
                <div style="font-size: 0.88rem; color: #475569; margin: 0.35rem 0; line-height: 1.45;">
                    {r_body}
                </div>
                <div style="font-size: 0.8rem; color: #0284C7; word-break: break-all;">
                    🔗 <a href="{r_url}" target="_blank" style="color: #0284C7;">{r_url}</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    # ==========================================
    # SECCIÓN 3: BARRA DE ACCIONES Y GENERACIÓN (TOOLBAR MINIMALISTA)
    # ==========================================
    st.markdown("""
    <div class="nem-card-header">
        <span style="color: #7C3AED; font-size: 1.5rem; line-height: 1;">•</span>
        <h3 class="nem-card-title">3. Acciones Principales y Generación del Plano Didáctico</h3>
    </div>
    """, unsafe_allow_html=True)

    # Configuración de Archivo en Expander Compacto
    with st.expander("📁 Destino y Nombre de Archivo Personalizado", expanded=False):
        c_nom_arch, c_cat_ruta = st.columns([1.3, 1.2])
        with c_nom_arch:
            nombre_archivo_input = st.text_input(
                "Nombre personalizado del archivo (ej. Planeacion_Semana_20_Matematicas):",
                value=st.session_state.get(f"inp_nombre_archivo_{st.session_state.widget_key}", nombre_archivo_actual),
                key=f"inp_nombre_archivo_{st.session_state.widget_key}",
                help="Escribe el nombre con el que deseas guardar y organizar este archivo en tu historial y en la carpeta local de respaldos."
            )
            st.session_state["nombre_archivo_actual"] = nombre_archivo_input
            data_actual_para_guardar["nombre_archivo"] = nombre_archivo_input

        with c_cat_ruta:
            cat_index_sel = CATEGORIAS_RUTAS_DEFAULT.index(categoria_ruta_actual) if categoria_ruta_actual in CATEGORIAS_RUTAS_DEFAULT else 1
            categoria_ruta_input = st.selectbox(
                "Carpeta / Categoría de Destino:",
                options=CATEGORIAS_RUTAS_DEFAULT,
                index=cat_index_sel,
                key=f"sel_categoria_ruta_{st.session_state.widget_key}",
                help="Selecciona la carpeta organizativa donde se archivará la planeación (por trimestre, tipo de proyecto o CTE)."
            )
            st.session_state["categoria_ruta_actual"] = categoria_ruta_input
            data_actual_para_guardar["categoria_ruta"] = categoria_ruta_input

        st.caption(f"📍 Destino en disco: `guardados/{sanitizar_nombre_ruta(categoria_ruta_input)}/{sanitizar_nombre_ruta(nombre_archivo_input)}.json`")

    # Si no se abrió el expander, asegurar que las variables existan en locals
    if 'nombre_archivo_input' not in locals():
        nombre_archivo_input = st.session_state.get("nombre_archivo_actual", nombre_archivo_actual)
    if 'categoria_ruta_input' not in locals():
        categoria_ruta_input = st.session_state.get("categoria_ruta_actual", categoria_ruta_actual)

    # Barra de Herramientas Compacta (Toolbar 2x3)
    st.markdown("""
    <div class="action-toolbar-box">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 6px;">
            <div style="font-weight: 700; color: #4C1D95; font-size: 0.95rem; display: flex; align-items: center; gap: 6px;">
                ⚡ <b>Barra de Acciones Rápidas</b>
            </div>
            <span style="font-size: 0.78rem; background: #EDE9FE; color: #6D28D9; padding: 2px 10px; border-radius: 9999px; font-weight: 600;">
                Ciclo Escolar 2026-2027 • Fase 5
            </span>
        </div>
    """, unsafe_allow_html=True)

    col_tb1, col_tb2, col_tb3 = st.columns(3)
    with col_tb1:
        btn_generar = st.button("🚀 Generar con Gemini", type="primary", use_container_width=True, help="Genera la planeación oficial completa con IA considerando el Programa Analítico y la NEM.")
    with col_tb2:
        btn_save_named = st.button("💾 Guardar Archivo", key=f"btn_save_named_{st.session_state.widget_key}", use_container_width=True, help="Guarda inmediatamente tu planeación en el historial y en la carpeta seleccionada.")
    with col_tb3:
        btn_busqueda_web = st.button("🌐 Generar con Web", key="btn_generar_web", use_container_width=True, help="Consulta la web en tiempo real con Google Search Grounding para enriquecer la secuencia didáctica con dinámicas, noticias y ejemplos prácticos recientes.")

    col_tb4, col_tb5, col_tb6 = st.columns(3)
    with col_tb4:
        btn_demo = st.button(f"👁️ Cargar Demo ({grado_sel})", use_container_width=True, help=f"Muestra una planeación oficial completa para {grado_sel} sin consumir cuota de API.")
    with col_tb5:
        btn_plantilla_base = st.button("📄 Plantilla Base (Sin IA)", use_container_width=True, help="Genera directamente la plantilla oficial en Word (.docx) y PDF con tus datos escolares y curriculares prellenados, sin realizar llamadas a la IA.")
    with col_tb6:
        if st.session_state.get("planeacion_generada"):
            quick_docx = build_docx_planeacion(datos_escuela=datos_escuela_actual, plan_text=st.session_state.planeacion_generada)
            st.download_button("📥 Descargar Word (.docx)", data=quick_docx, file_name=f"{sanitizar_nombre_ruta(nombre_archivo_input)}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True, key=f"btn_quick_word_{st.session_state.widget_key}")
        else:
            st.button("⚙️ Vista Previa en Espera", disabled=True, use_container_width=True, help="Genera una planeación o carga un demo para habilitar la descarga directa desde la barra.")

    st.markdown("</div>", unsafe_allow_html=True)

    if btn_save_named:
        data_actual_para_guardar["nombre_archivo"] = nombre_archivo_input
        data_actual_para_guardar["categoria_ruta"] = categoria_ruta_input
        guardar_planeacion(
            username=docente_usuario_act,
            data=data_actual_para_guardar,
            es_autoguardado=False,
            version_nombre=nombre_archivo_input,
            nombre_archivo=nombre_archivo_input,
            categoria_ruta=categoria_ruta_input
        )
        st.success(f"✓ ¡Planeación guardada como '{nombre_archivo_input}' en '{categoria_ruta_input}'!")
        st.rerun()
    
    if btn_generar:
        if not verificar_conexion_internet():
            st.error("No hay conexión a internet. Por favor, revisa tu red e inténtalo de nuevo.")
        elif not active_api_key:
            st.error(f"⚠️ Para generar con Gemini necesitas ingresar tu API Key en la barra lateral izquierda. Si aún no la tienes, puedes hacer clic en 'Cargar Ejemplo Completo ({grado_sel})' para explorar el resultado y descargar el Word oficial.")
        elif not dias_seleccionados:
            st.warning("Por favor selecciona al menos un día de la semana a planear.")
        elif not campos_sel:
            st.warning("Por favor selecciona al menos un Campo Formativo.")
        elif not ejes_sel:
            st.warning("Por favor selecciona al menos un Eje Articulador.")
        else:
            with st.spinner("Analizando archivos y generando planeación con Gemini... por favor espera."):
                try:
                    # 1. Extraer automáticamente el texto de los archivos cargados (PyPDF2 y python-docx)
                    archivos_para_procesar = dict(st.session_state.archivos_procesados)
                    if uploaded_files:
                        nuevos_archivos = process_uploaded_files(uploaded_files)
                        archivos_para_procesar.update(nuevos_archivos)
                        st.session_state.archivos_procesados = archivos_para_procesar
    
                    # 2. Combinar el texto extraído con las opciones seleccionadas en el formulario y directrices NEM
                    contexto_archivos_str = format_context_for_prompt(archivos_para_procesar)
    
                    # Extraer texto de la URL de referencia si no se ha extraído aún
                    if url_referencia and url_referencia.strip() and not contexto_url:
                        contexto_url = extraer_texto_url(url_referencia.strip())
    
                    # FUNCIÓN DE RESPALDO (WEB SCRAPING SEP):
                    # Si el usuario NO subió un archivo del Programa Sintético (file_uploader está vacío)
                    prog_sintetico_contexto = ""
                    scraping_fallido = False
    
                    dia_contexto_sep = st.session_state.get("dia_activo_pestaña", dias_seleccionados[0] if dias_seleccionados else "Lunes")
                    if not uploaded_prog:
                        with st.status(f"🔍 Búsqueda de Respaldo SEP: Rastreando Programa Sintético oficial ({fase_correspondiente} - Semana {semana_seleccionada} - {dia_contexto_sep})...", expanded=True) as status_box:
                            st.write(f"Buscando en portales oficiales de la SEP para Semana {semana_seleccionada} ({cal_mes_actual} 2026), día {dia_contexto_sep}...")
                            resumen_scraping, scraping_exitoso = buscar_programa_sintetico_sep(
                                fase=fase_correspondiente,
                                semana=semana_seleccionada,
                                mes=cal_mes_actual,
                                dia=dia_contexto_sep,
                                proyecto=proyecto_semana_actual["proyecto"]
                            )
                            if scraping_exitoso and resumen_scraping:
                                status_box.update(label=f"✓ Contenido del Programa Sintético obtenido de la SEP ({len(resumen_scraping):,} caracteres)", state="complete")
                                prog_sintetico_contexto = resumen_scraping
                                scraping_fallido = False
                            else:
                                fase_num = fase_correspondiente.replace("Fase", "").strip() or "5"
                                status_box.update(label=f"ℹ️ Conexión directa no disponible. Activando fallback curricular SEP (Fase {fase_num} - Semana {semana_seleccionada})...", state="complete")
                                prog_sintetico_contexto = ""
                                scraping_fallido = True
                    else:
                        prog_sintetico_contexto = st.session_state.programa_sintetico_texto
                        scraping_fallido = False
    
                    # 3. Enviar todo el bloque de información estructurada a la API de Gemini (modelo gemini-3.8-flash)
                    plan_generado, prompt_utilizado = generate_planeacion(
                        datos_escuela=datos_escuela_actual,
                        campos_formativos=campos_sel,
                        metodologia=metodologia_sel,
                        ejes_articuladores=ejes_sel,
                        contenidos_pda=items_pda_final,
                        directrices_docente=directrices_input,
                        contexto_archivos=contexto_archivos_str,
                        libros_seleccionados=libros_sel,
                        guia_cte=guia_cte_sel,
                        programa_sintetico=prog_sintetico_contexto,
                        dias_seleccionados=dias_seleccionados,
                        semana_seleccionada=semana_seleccionada,
                        mes_seleccionado=cal_mes_actual,
                        año_seleccionado=cal_año_actual,
                        proyecto_semana=proyecto_semana_actual,
                        dia_especifico_pestaña=dia_contexto_sep,
                        fase_seleccionada=fase_correspondiente,
                        fallback_programa_sintetico=scraping_fallido,
                        num_sesiones=num_sesiones,
                        api_key=active_api_key,
                        modelo="gemini-3.8-flash",
                        guia_cte_detalle=cte_info,
                        busqueda_web=False,
                        contexto_url=contexto_url,
                        vincular_cuadernillo_kempis=vincular_kempis_sel if 'vincular_kempis_sel' in locals() else True
                    )
                    st.session_state.planeacion_generada = plan_generado
                    st.session_state.prompt_enviado = prompt_utilizado
                    data_gen_save = dict(data_actual_para_guardar)
                    data_gen_save["planeacion_generada"] = plan_generado
                    data_gen_save["prompt_enviado"] = prompt_utilizado
                    guardar_planeacion(username=docente_usuario_act, data=data_gen_save, es_autoguardado=True)
                    st.session_state["ultimo_hash_guardado"] = calcular_hash_planeacion(data_gen_save)
                    st.session_state["ultimo_autoguardado_hora"] = datetime.datetime.now().strftime("%H:%M:%S")
                    st.session_state["ultimo_autoguardado_semana"] = semana_seleccionada
                    st.success("🎉 ¡Planeación didáctica generada exitosamente con Gemini 3.8 Flash!")
                except (
                    ConnectionError,
                    TimeoutError,
                    socket.timeout,
                    socket.gaierror,
                    socket.error,
                    requests.exceptions.RequestException,
                    *( [httpx.RequestError, httpx.TimeoutException] if httpx else [] )
                ) as conn_err:
                    st.error("No hay conexión a internet. Por favor, revisa tu red e inténtalo de nuevo.")
                    st.info("💡 **Consejo de respaldo:** Si tu conexión a internet falló a mitad del proceso, puedes generar inmediatamente tu planeación oficial en Word (.docx) y PDF con tus datos curriculares prellenados presionando el botón **'Descargar Plantilla Base (Sin IA)'**.")
                except Exception as e:
                    error_str = str(e)
                    is_conn_error = any(term in error_str.lower() for term in [
                        "connection", "conexión", "timed out", "timeout", "connecterror",
                        "readtimeout", "network", "unreachable", "getaddrinfo", "econnreset",
                        "econnrefused", "temporary failure in name resolution"
                    ])
                    if is_conn_error:
                        st.error("No hay conexión a internet. Por favor, revisa tu red e inténtalo de nuevo.")
                        st.info("💡 **Consejo de respaldo:** Si tu red se desconectó a mitad del proceso, puedes generar tu planeación con el botón **'Descargar Plantilla Base (Sin IA)'** sin depender de internet.")
                    elif "503" in error_str:
                        st.info("💡 **Modo de Respaldo Recomendado:** Los servidores de IA están saturados temporalmente tras los 3 reintentos automáticos. Para no perder tu avance, puedes presionar el botón **'Descargar Plantilla Base (Sin IA)'** para generar de inmediato tu documento oficial en Word (.docx) y PDF con todos tus datos curriculares prellenados.")
                    else:
                        st.error(f"Ocurrió un error al consultar la API de Gemini: {error_str}")
                        st.info("Tip: Verifica que tu clave de API sea válida y tenga permisos activos para los modelos de Gemini.")
    
    if btn_busqueda_web:
        if not verificar_conexion_internet():
            st.error("No hay conexión a internet. Por favor, revisa tu red e inténtalo de nuevo.")
        elif not active_api_key:
            st.error("⚠️ Para generar con Búsqueda Web necesitas ingresar tu API Key en la barra lateral izquierda. Si aún no la tienes, puedes hacer clic en 'Descargar Plantilla Base (Sin IA)' o 'Cargar Ejemplo Completo 6° Grado'.")
        elif not dias_seleccionados:
            st.warning("Por favor selecciona al menos un día de la semana a planear.")
        elif not campos_sel:
            st.warning("Por favor selecciona al menos un Campo Formativo.")
        elif not ejes_sel:
            st.warning("Por favor selecciona al menos un Eje Articulador.")
        else:
            with st.spinner("Buscando en la web en tiempo real y generando planeación con Gemini... por favor espera."):
                try:
                    # 1. Extraer automáticamente el texto de los archivos cargados (PyPDF2 y python-docx)
                    archivos_para_procesar = dict(st.session_state.archivos_procesados)
                    if uploaded_files:
                        nuevos_archivos = process_uploaded_files(uploaded_files)
                        archivos_para_procesar.update(nuevos_archivos)
                        st.session_state.archivos_procesados = archivos_para_procesar
    
                    # 2. Combinar el texto extraído con las opciones seleccionadas en el formulario y directrices NEM
                    contexto_archivos_str = format_context_for_prompt(archivos_para_procesar)
    
                    # Extraer texto de la URL de referencia si no se ha extraído aún
                    if url_referencia and url_referencia.strip() and not contexto_url:
                        contexto_url = extraer_texto_url(url_referencia.strip())
    
                    # FUNCIÓN DE RESPALDO (WEB SCRAPING SEP):
                    # Si el usuario NO subió un archivo del Programa Sintético (file_uploader está vacío)
                    prog_sintetico_contexto = ""
                    scraping_fallido = False
    
                    dia_contexto_web = st.session_state.get("dia_activo_pestaña", dias_seleccionados[0] if dias_seleccionados else "Lunes")
                    if not uploaded_prog:
                        with st.status(f"🔍 Búsqueda de Respaldo SEP: Rastreando Programa Sintético oficial ({fase_correspondiente} - Semana {semana_seleccionada} - {dia_contexto_web})...", expanded=True) as status_box:
                            st.write(f"Buscando en portales oficiales de la SEP para Semana {semana_seleccionada} ({cal_mes_actual} 2026), día {dia_contexto_web}...")
                            resumen_scraping, scraping_exitoso = buscar_programa_sintetico_sep(
                                fase=fase_correspondiente,
                                semana=semana_seleccionada,
                                mes=cal_mes_actual,
                                dia=dia_contexto_web,
                                proyecto=proyecto_semana_actual["proyecto"]
                            )
                            if scraping_exitoso and resumen_scraping:
                                status_box.update(label=f"✓ Contenido del Programa Sintético obtenido de la SEP ({len(resumen_scraping):,} caracteres)", state="complete")
                                prog_sintetico_contexto = resumen_scraping
                                scraping_fallido = False
                            else:
                                fase_num = fase_correspondiente.replace("Fase", "").strip() or "5"
                                status_box.update(label=f"ℹ️ Conexión directa no disponible. Activando fallback curricular SEP (Fase {fase_num} - Semana {semana_seleccionada})...", state="complete")
                                prog_sintetico_contexto = ""
                                scraping_fallido = True
                    else:
                        prog_sintetico_contexto = st.session_state.programa_sintetico_texto
                        scraping_fallido = False
    
                    # 3. Enviar a Gemini con Google Search Grounding habilitado y parámetros dinámicos
                    plan_generado, prompt_utilizado = generate_planeacion(
                        datos_escuela=datos_escuela_actual,
                        campos_formativos=campos_sel,
                        metodologia=metodologia_sel,
                        ejes_articuladores=ejes_sel,
                        contenidos_pda=items_pda_final,
                        directrices_docente=directrices_input,
                        contexto_archivos=contexto_archivos_str,
                        libros_seleccionados=libros_sel,
                        guia_cte=guia_cte_sel,
                        programa_sintetico=prog_sintetico_contexto,
                        dias_seleccionados=dias_seleccionados,
                        semana_seleccionada=semana_seleccionada,
                        mes_seleccionado=cal_mes_actual,
                        año_seleccionado=cal_año_actual,
                        proyecto_semana=proyecto_semana_actual,
                        dia_especifico_pestaña=dia_contexto_web,
                        fase_seleccionada=fase_correspondiente,
                        fallback_programa_sintetico=scraping_fallido,
                        num_sesiones=num_sesiones,
                        api_key=active_api_key,
                        modelo="gemini-3.8-flash",
                        guia_cte_detalle=cte_info,
                        busqueda_web=True,
                        contexto_url=contexto_url,
                        vincular_cuadernillo_kempis=vincular_kempis_sel if 'vincular_kempis_sel' in locals() else True
                    )
                    st.session_state.planeacion_generada = plan_generado
                    st.session_state.prompt_enviado = prompt_utilizado
                    data_gen_save = dict(data_actual_para_guardar)
                    data_gen_save["planeacion_generada"] = plan_generado
                    data_gen_save["prompt_enviado"] = prompt_utilizado
                    guardar_planeacion(username=docente_usuario_act, data=data_gen_save, es_autoguardado=True)
                    st.session_state["ultimo_hash_guardado"] = calcular_hash_planeacion(data_gen_save)
                    st.session_state["ultimo_autoguardado_hora"] = datetime.datetime.now().strftime("%H:%M:%S")
                    st.session_state["ultimo_autoguardado_semana"] = semana_seleccionada
                    st.success("🎉 ¡Planeación didáctica enriquecida con búsqueda web en vivo generada exitosamente con Gemini!")
                except (
                    ConnectionError,
                    TimeoutError,
                    socket.timeout,
                    socket.gaierror,
                    socket.error,
                    requests.exceptions.RequestException,
                    *( [httpx.RequestError, httpx.TimeoutException] if httpx else [] )
                ) as conn_err:
                    st.error("No hay conexión a internet. Por favor, revisa tu red e inténtalo de nuevo.")
                    st.info("💡 **Consejo de respaldo:** Si tu conexión a internet falló a mitad del proceso con búsqueda web, puedes generar tu planeación con el botón **'Descargar Plantilla Base (Sin IA)'** sin depender de internet.")
                except Exception as e:
                    error_str = str(e)
                    is_conn_error = any(term in error_str.lower() for term in [
                        "connection", "conexión", "timed out", "timeout", "connecterror",
                        "readtimeout", "network", "unreachable", "getaddrinfo", "econnreset",
                        "econnrefused", "temporary failure in name resolution"
                    ])
                    if is_conn_error:
                        st.error("No hay conexión a internet. Por favor, revisa tu red e inténtalo de nuevo.")
                        st.info("💡 **Consejo de respaldo:** Si tu conexión falló durante la búsqueda web, puedes utilizar el botón **'Descargar Plantilla Base (Sin IA)'** para continuar sin perder tus datos curriculares.")
                    elif "503" in error_str:
                        st.info("💡 **Modo de Respaldo Recomendado:** Los servidores de IA están saturados temporalmente tras los 3 reintentos automáticos. Para no perder tu avance, puedes presionar el botón **'Descargar Plantilla Base (Sin IA)'** para generar de inmediato tu documento oficial en Word (.docx) y PDF con todos tus datos curriculares prellenados.")
                    else:
                        st.error(f"Ocurrió un error al consultar la API de Gemini con Búsqueda Web: {error_str}")
                        st.info("Tip: Verifica que tu clave de API sea válida y tenga permisos activos para los modelos de Gemini.")
    
    if btn_plantilla_base:
        with st.spinner("Generando plantilla oficial base sin IA (Word y PDF)... por favor espera."):
            plantilla_base_text = generar_plantilla_base_sin_ia(
                datos_escuela=datos_escuela_actual,
                campos_formativos=campos_sel,
                metodologia=metodologia_sel,
                ejes=ejes_sel,
                contenidos_pda=items_pda_final,
                libros_seleccionados=libros_sel,
                dias_seleccionados=dias_seleccionados,
                directrices=directrices_input,
                num_sesiones=num_sesiones
            )
            st.session_state.planeacion_generada = plantilla_base_text
            st.session_state.prompt_enviado = "Modo de Respaldo: Plantilla Oficial Base generada sin llamadas a la API de Gemini."
            data_gen_save = dict(data_actual_para_guardar)
            data_gen_save["planeacion_generada"] = plantilla_base_text
            data_gen_save["prompt_enviado"] = st.session_state.prompt_enviado
            guardar_planeacion(username=docente_usuario_act, data=data_gen_save, es_autoguardado=True)
            st.session_state["ultimo_hash_guardado"] = calcular_hash_planeacion(data_gen_save)
            st.session_state["ultimo_autoguardado_hora"] = datetime.datetime.now().strftime("%H:%M:%S")
            st.session_state["ultimo_autoguardado_semana"] = semana_seleccionada
            st.success("📄 ¡Plantilla base generada con éxito! Puedes descargar tu archivo en Word (.docx) o PDF inmediatamente en los botones de abajo.")
    
    if btn_demo:
        with st.spinner(f"Cargando plantilla pedagógica institucional de {grado_sel}..."):
            demo_plan = generate_sample_fallback(
                datos_escuela=datos_escuela_actual,
                campos_formativos=campos_sel if campos_sel else CAMPOS_FORMATIVOS,
                metodologia=metodologia_sel,
                ejes=ejes_sel if ejes_sel else ["Pensamiento crítico", "Apropiación de las culturas a través de la lectura y la escritura", "Vida saludable"],
                dias_seleccionados=dias_seleccionados,
                directrices=directrices_input,
                semana_seleccionada=semana_seleccionada,
                vincular_cuadernillo_kempis=vincular_kempis_sel if 'vincular_kempis_sel' in locals() else True
            )
            st.session_state.planeacion_generada = demo_plan
            data_gen_save = dict(data_actual_para_guardar)
            data_gen_save["planeacion_generada"] = demo_plan
            guardar_planeacion(username=docente_usuario_act, data=data_gen_save, es_autoguardado=True)
            st.session_state["ultimo_hash_guardado"] = calcular_hash_planeacion(data_gen_save)
            st.session_state["ultimo_autoguardado_hora"] = datetime.datetime.now().strftime("%H:%M:%S")
            st.session_state["ultimo_autoguardado_semana"] = semana_seleccionada
            st.info(f"Plantilla de demostración completa ({fase_auto} - {grado_sel}) cargada.")
    
    # ==========================================
    # SECCIÓN 4: RESULTADO Y EXPORTACIÓN
    # ==========================================
    if st.session_state.planeacion_generada:
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="nem-card-header">
            <span style="color: #7C3AED; font-size: 1.5rem; line-height: 1;">•</span>
            <h3 class="nem-card-title">4. Estructura Oficial de la Planeación (Plano Didáctico)</h3>
        </div>
        """, unsafe_allow_html=True)
    
        # Generar archivos descargables en memoria
        docx_buffer = build_docx_planeacion(
            datos_escuela=datos_escuela_actual,
            plan_text=st.session_state.planeacion_generada
        )
        pdf_buffer = build_pdf_planeacion(
            datos_escuela=datos_escuela_actual,
            plan_text=st.session_state.planeacion_generada
        )
    
        # Botones de descarga y exportación interactiva (DOCX, PDF, MD)
        col_d1, col_d2, col_d3 = st.columns(3)
        if 'nombre_archivo_input' in locals() and nombre_archivo_input:
            nombre_base = sanitizar_nombre_ruta(nombre_archivo_input).replace(".json", "")
        elif st.session_state.get("nombre_archivo_actual"):
            nombre_base = sanitizar_nombre_ruta(st.session_state["nombre_archivo_actual"]).replace(".json", "")
        else:
            nombre_base = f"Planeacion_{escuela_nombre.replace(' ', '_')}_{grado_sel[:2]}_{periodo_sel.replace(' ', '_')}"
        
        with col_d1:
            st.download_button(
                label="📄 Descargar Word (.docx)",
                data=docx_buffer,
                file_name=f"{nombre_base}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                help="Plantilla oficial editable con Horario Escolar, Dosificador General, tablas por día (Inicio/Desarrollo/Cierre) y firmas institucionales."
            )
    
        with col_d2:
            st.download_button(
                label="📑 Descargar PDF (.pdf)",
                data=pdf_buffer,
                file_name=f"{nombre_base}.pdf",
                mime="application/pdf",
                use_container_width=True,
                help="Documento formateado con membrete SEP, tablas de Horario Escolar, rutinas matutinas y firmas institucionales listo para imprimir."
            )
    
        with col_d3:
            st.download_button(
                label="📝 Markdown (.md)",
                data=st.session_state.planeacion_generada,
                file_name=f"{nombre_base}.md",
                mime="text/markdown",
                use_container_width=True,
                help="Texto estructurado oficial con encabezados y tablas en Markdown."
            )
    
        st.caption("✓ **Replicación exacta del formato:** Conserva el membrete, el Horario Escolar, el Dosificador General de Proyectos, las tablas diarias (Dictado, Cálculo, Problema, Inicio, Desarrollo, Cierre), Recursos, Evaluación y los espacios para las firmas oficiales de **Aday Domínguez Domínguez** (Docente) y **José Guillermo Borjas Díaz** (Director).")

        kempis_activo_vista = (vincular_kempis_sel if 'vincular_kempis_sel' in locals() else True)
        if kempis_activo_vista:
            kempis_info_banner = obtener_recursos_kempis_por_semana(semana_seleccionada)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #F3E8FF 0%, #EDE9FE 100%); border-left: 5px solid #7C3AED; border-radius: 8px; padding: 12px 18px; margin: 10px 0 16px 0;">
                <span style="font-weight: 700; color: #4C1D95; font-size: 0.95rem;">📘 Proyecto y Cuadernillo Integrado (Semana {semana_seleccionada} de 37 SEP):</span><br>
                <span style="color: #1F2937; font-size: 0.88rem; line-height: 1.45;">
                    El archivo <b>Word (.docx)</b> descargable incluye la sección oficial de <b>Anexos Imprimibles y Fichas de Trabajo</b> correspondientes al proyecto <b>"{kempis_info_banner.get('titulo_general', proyecto_semana_actual['proyecto'])}"</b> para la semana {semana_seleccionada} ({kempis_info_banner.get('periodo_sugerido', cal_mes_actual)}), con orientaciones vivenciales y actividades estructuradas.
                </span>
            </div>
            """, unsafe_allow_html=True)
    
        st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    
        parsed_resultado = parse_plan_sections(st.session_state.planeacion_generada)
        dias_para_mostrar = dias_seleccionados if dias_seleccionados else DIAS_HABIL_NOMBRES

        # Pestañas interactivas para revisar la planeación
        tab_dias_ver, tab_completa, tab_dosificador, tab_evaluacion, tab_ajustes, tab_kempis = st.tabs([
            "📅 Vista Día por Día (Lunes a Viernes)",
            "📄 Documento Completo Oficial",
            "📋 Dosificador y Articulación",
            "📊 Instrumentos de Evaluación",
            "♿ Inclusión (BAP/DUA)",
            "📘 Cuadernillo Profa Kempis"
        ])

        with tab_dias_ver:
            st.markdown("""
            <div style="margin-bottom: 10px;">
                <span style="font-weight: 700; color: #4C1D95; font-size: 0.96rem;">🗓️ Navegación Modular Día por Día</span>
                <p style="color: #64748B; font-size: 0.84rem; margin: 2px 0 8px 0;">
                    Visualiza de forma clara e independiente la Rutina Matutina y la Secuencia Didáctica (Inicio, Desarrollo y Cierre) de cada día sin saturar la pantalla.
                </p>
            </div>
            """, unsafe_allow_html=True)

            subtabs_dias = st.tabs([f"🗓️ {d}" for d in dias_para_mostrar])
            dias_fechas_map_ver = st.session_state.get("dias_fechas", {})

            for idx_d, (st_dia, nom_dia) in enumerate(zip(subtabs_dias, dias_para_mostrar)):
                with st_dia:
                    f_label = dias_fechas_map_ver.get(nom_dia, f"{nom_dia} (Semana {semana_seleccionada})")
                    r_item = parsed_resultado.get("rutinas_por_dia", {}).get(nom_dia)
                    if not r_item and idx_d < len(parsed_resultado.get("rutinas", [])):
                        r_item = parsed_resultado["rutinas"][idx_d]
                    
                    s_item = parsed_resultado.get("sesiones_por_dia", {}).get(nom_dia)
                    if not s_item and idx_d < len(parsed_resultado.get("sesiones", [])):
                        s_item = parsed_resultado["sesiones"][idx_d]

                    r_dictado = r_item.get("dictado", "Palabras clave ortográficas y de vocabulario.") if r_item else "Palabras clave ortográficas y de vocabulario."
                    r_calculo = r_item.get("calculo", "Operaciones combinadas de cálculo mental rápido.") if r_item else "Operaciones combinadas de cálculo mental rápido."
                    r_problema = r_item.get("problema", "Problema razonado de situaciones de la vida cotidiana.") if r_item else "Problema razonado de situaciones de la vida cotidiana."

                    s_inicio = s_item.get("inicio", "Recuperación de saberes previos y planteamiento de pregunta detonadora.") if s_item else "Recuperación de saberes previos y planteamiento de pregunta detonadora."
                    s_desarrollo = s_item.get("desarrollo", "Actividades de indagación y aplicación colaborativa con LTG.") if s_item else "Actividades de indagación y aplicación colaborativa con LTG."
                    s_cierre = s_item.get("cierre", "Socialización de hallazgos, síntesis de aprendizajes y coevaluación.") if s_item else "Socialización de hallazgos, síntesis de aprendizajes y coevaluación."
                    s_recursos = s_item.get("recursos", "Libro de texto gratuito, libreta de notas y materiales del aula.") if s_item else "Libro de texto gratuito, libreta de notas y materiales del aula."

                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #FAF5FF 0%, #F5F3FF 100%); border: 1.5px solid #DDD6FE; border-radius: 10px; padding: 10px 14px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                        <div style="font-weight: 700; color: #4C1D95; font-size: 0.94rem;">
                            🗓️ <b>{f_label}</b> — Sesión {idx_d + 1} de {len(dias_para_mostrar)}
                        </div>
                        <div style="font-size: 0.76rem; background: #EDE9FE; color: #6D28D9; padding: 3px 10px; border-radius: 9999px; font-weight: 600;">
                            08:00 - 13:00 • 90 min de sesión
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    c_ver_rut, c_ver_sec = st.columns([1, 1.35])
                    with c_ver_rut:
                        st.markdown(f"""
                        <div class="day-moment-box">
                            <div class="day-moment-title">🌅 Rutina Matutina Permanente (15-20 min)</div>
                            <div class="day-moment-text">
                                <b>✍️ Dictado:</b> {r_dictado}<br><br>
                                <b>🔢 Cálculo Mental:</b> {r_calculo}<br><br>
                                <b>🧩 Problema Razonado:</b> {r_problema}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with c_ver_sec:
                        st.markdown(f"""
                        <div class="day-moment-box" style="border-left-color: #059669;">
                            <div class="day-moment-title" style="color: #065F46;">🎯 Secuencia Didáctica (Inicio, Desarrollo y Cierre)</div>
                            <div class="day-moment-text">
                                <span style="color: #047857; font-weight: 700;">🟢 Inicio (15-20 min):</span><br>{s_inicio}<br><br>
                                <span style="color: #B45309; font-weight: 700;">🟡 Desarrollo (50-60 min):</span><br>{s_desarrollo}<br><br>
                                <span style="color: #4C1D95; font-weight: 700;">🔴 Cierre (15-20 min):</span><br>{s_cierre}<br><br>
                                <span style="color: #374151; font-weight: 700;">📦 Recursos y Materiales:</span><br>{s_recursos}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

        with tab_completa:
            st.markdown(st.session_state.planeacion_generada)
    
        with tab_dosificador:
            st.markdown("### Dosificación General y Articulación Curricular (NEM)")
            # Extraer secciones de articulación si están disponibles
            partes = st.session_state.planeacion_generada.split("# ")
            for p in partes:
                if p.startswith("I. ") or p.startswith("II. "):
                    st.markdown("# " + p)
    
        with tab_evaluacion:
            st.markdown("### Instrumentos de Evaluación Formativa")
            partes = st.session_state.planeacion_generada.split("# ")
            encontrado = False
            for p in partes:
                if "EVALUACIÓN FORMATIVA" in p or "V. " in p:
                    st.markdown("# " + p)
                    encontrado = True
            if not encontrado:
                st.info("Revisa la pestaña de 'Documento Completo' para consultar la rúbrica/lista de cotejo.")
    
        with tab_ajustes:
            st.markdown("### Estrategias de Inclusión, BAP y DUA")
            partes = st.session_state.planeacion_generada.split("# ")
            for p in partes:
                if "AJUSTES RAZONABLES" in p or "VI. " in p or "VII. " in p:
                    st.markdown("# " + p)

        with tab_kempis:
            kempis_data_vista = obtener_recursos_kempis_por_semana(semana_seleccionada)
            if kempis_data_vista:
                st.markdown(f"""
                <div class="kempis-header-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 8px;">
                        <div style="font-weight: 800; font-size: 1.05rem; color: #4C1D95; display: flex; align-items: center; gap: 8px;">
                            📘 <b>Cuadernillo Didáctico y Anexos de Actividades (Semana {semana_seleccionada} de 37 SEP)</b>
                        </div>
                        <span style="font-size: 0.78rem; background: #EDE9FE; color: #6D28D9; padding: 3px 10px; border-radius: 9999px; font-weight: 700;">
                            {kempis_data_vista.get('periodo_sugerido', cal_mes_actual)} • Fase 5 (6° Primaria)
                        </span>
                    </div>
                    <div style="font-size: 0.88rem; font-weight: 700; color: #1F2937; margin-bottom: 4px;">
                        {kempis_data_vista.get('titulo_general', '')}
                    </div>
                    <div style="font-size: 0.84rem; color: #374151; line-height: 1.5;">
                        {kempis_data_vista.get('descripcion', '')} Fichas de trabajo, retos de cálculo y dinámicas estructuradas listas para aplicar en el aula e integradas en el Word descargable.
                    </div>
                </div>
                """, unsafe_allow_html=True)

                campos_items = list(kempis_data_vista["campos"].items())
                col_kempis_left, col_kempis_right = st.columns(2)

                iconos_campos = {
                    "Lenguajes": ("🗣️", "#7C3AED", "#EDE9FE", "#6D28D9"),
                    "Saberes y Pensamiento Científico": ("🔬", "#059669", "#D1FAE5", "#065F46"),
                    "Ética, Naturaleza y Sociedades": ("🌍", "#2563EB", "#DBEAFE", "#1D4ED8"),
                    "De lo Humano y lo Comunitario": ("🤝", "#D97706", "#FEF3C7", "#B45309")
                }

                for idx_k, (cf_nombre, cf_detalles) in enumerate(campos_items):
                    col_target = col_kempis_left if (idx_k % 2 == 0) else col_kempis_right
                    c_icono, c_border, c_bg_pill, c_txt_pill = iconos_campos.get(cf_nombre, ("📚", "#7C3AED", "#EDE9FE", "#6D28D9"))
                    
                    with col_target:
                        st.markdown(f"""
                        <div class="kempis-act-card" style="border-top: 4px solid {c_border};">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; flex-wrap: wrap; gap: 6px;">
                                <span style="font-weight: 800; font-size: 0.95rem; color: #1F2937;">{c_icono} {cf_nombre}</span>
                                <span style="font-size: 0.74rem; background: {c_bg_pill}; color: {c_txt_pill}; padding: 2px 8px; border-radius: 9999px; font-weight: 700;">
                                    {cf_detalles['anexo_nombre'].split(':')[0]}
                                </span>
                            </div>
                            <div style="font-size: 0.88rem; font-weight: 700; color: #1F2937; margin-bottom: 6px; line-height: 1.4;">
                                📌 <b>Tema:</b> <span style="font-weight: 600; color: #374151;">{cf_detalles['tema']}</span>
                            </div>
                            <div style="font-size: 0.80rem; color: #4B5563; margin-bottom: 8px;">
                                <b>PDA:</b> {cf_detalles['pda_vinculado']}
                            </div>
                            <div class="kempis-anexo-box">
                                <div style="font-size: 0.84rem; font-weight: 700; color: #1F2937; margin-bottom: 3px;">
                                    📝 <b>{cf_detalles['anexo_nombre']}</b>
                                </div>
                                <div style="font-size: 0.80rem; color: #374151; line-height: 1.45;">
                                    {cf_detalles['anexo_descripcion']}
                                </div>
                            </div>
                            <div style="font-size: 0.82rem; color: #1F2937; line-height: 1.5; margin-top: 8px;">
                                <div style="font-weight: 700; color: #1F2937; margin-bottom: 4px;">🎯 Secuencia Didáctica de Intervención:</div>
                                <div style="margin-bottom: 3px;"><span style="color: #047857; font-weight: 700;">🟢 Inicio:</span> {cf_detalles['inicio']}</div>
                                <div style="margin-bottom: 3px;"><span style="color: #B45309; font-weight: 700;">🟡 Desarrollo:</span> {cf_detalles['desarrollo']}</div>
                                <div><span style="color: #4C1D95; font-weight: 700;">🔴 Cierre:</span> {cf_detalles['cierre']}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                ef_info_tab = kempis_data_vista.get("efemeride_principal", {})
                if ef_info_tab:
                    st.markdown(f"""
                    <div class="kempis-efemeride-card">
                        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px; flex-wrap: wrap;">
                            <span style="font-size: 1.25rem;">🇲🇽</span>
                            <span style="font-weight: 800; font-size: 0.95rem; color: #1F2937;">
                                Conmemoración Cívica e Histórica: <b>{ef_info_tab.get('nombre', '')}</b> ({ef_info_tab.get('fecha', '')})
                            </span>
                        </div>
                        <div style="font-size: 0.85rem; color: #1F2937; line-height: 1.5; margin-bottom: 8px;">
                            <b>🎯 Actividad Comunitaria:</b> {ef_info_tab.get('actividad', '')}
                        </div>
                        <div style="font-size: 0.83rem; color: #1F2937;">
                            <b>📄 Ficha Imprimible de Apoyo:</b> <code style="background: #FEF3C7; color: #92400E; padding: 2px 8px; border-radius: 4px; font-weight: 600;">{ef_info_tab.get('anexo_nombre', '')}</code> — <i>{ef_info_tab.get('anexo_descripcion', 'Análisis reflexivo y contextualizado.')}</i>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
# ==========================================
# PIE DE PÁGINA INSTITUCIONAL
# ==========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 1.5rem 0;">
    Desarrollado para la labor pedagógica
</div>
""", unsafe_allow_html=True)
