"""
Planeaciones Escolares Educación Primaria
Aplicación web interactiva profesional para la generación automatizada de
Planeaciones Escolares de Primaria basadas en el modelo de la Nueva Escuela Mexicana (NEM - SEP).
"""

import os
import streamlit as st
import streamlit_authenticator as stauth
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

# ==========================================
# CATÁLOGOS CURRICULARES NEM Y DICCIONARIO DE RESPALDO (FALLBACK)
# ==========================================
DATOS_PREDETERMINADOS = {
    "nombre_escuela": "Primaria Revolucion Social 1910",
    "cct": "10EPR0361N",
    "docente": "Aday Domínguez Domínguez",
    "director": "José Guillermo Borjas Díaz",
    "grado": "5° de Primaria",
    "fase": "Fase 5",
    "grupo": "A",
    "periodo": "Semana 20",
    "ciclo_escolar": "2025-2026",
    "turno": "Matutino",
    "zona_escolar": "014",
    "sector": "03"
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

LIBROS_SEP_RECOMENDADOS = LIBROS_SEP_POR_GRADO["5° de Primaria"]

GUIAS_CTE_CATALOGO = {
    "Orientaciones CTE - 5ª Sesión Ordinaria (Febrero 2026 - Fase 5)": {
        "enfoque": "Evaluación formativa, retroalimentación dialógica y análisis de los avances en proyectos comunitarios.",
        "directrices": "Priorizar la evaluación como un proceso continuo y no punitivo; promover la autorreflexión de los alumnos y la coevaluación en asambleas de aula. Atender BAP mediante ajustes razonables en lectura y razonamiento lógico."
    },
    "Orientaciones CTE - 4ª Sesión Ordinaria (Enero 2026 - Fase 5)": {
        "enfoque": "Articulación curricular y codiseño del Plan Analítico en la Fase 5.",
        "directrices": "Vincular problemáticas del contexto escolar (alimentación, comprensión lectora, convivencia) con los contenidos sintéticos y PDA integrados."
    },
    "Orientaciones CTE - 3ª Sesión Ordinaria (Noviembre 2025 - Fase 5)": {
        "enfoque": "Compromiso con la comunidad y metodologías sociocríticas activas.",
        "directrices": "Desarrollar proyectos interdisciplinarios que trasciendan el salón de clases y vinculen a las familias y el entorno local."
    },
    "Orientaciones CTE - 2ª Sesión Ordinaria (Octubre 2025 - Fase 5)": {
        "enfoque": "Ejes articuladores y Diseño Universal para el Aprendizaje (DUA).",
        "directrices": "Garantizar la inclusión, el pensamiento crítico y la igualdad de género en todas las secuencias didácticas planeadas."
    },
    "Orientaciones CTE - 1ª Sesión Ordinaria (Septiembre 2025 - Fase 5)": {
        "enfoque": "Diagnóstico socioeducativo inicial e identificación de barreras de aprendizaje.",
        "directrices": "Fortalecer habilidades fundamentales en lectoescritura, cálculo mental reflexivo y resolución de problemas matemáticos contextualizados."
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
            }
        ]
    }
}

CONTENIDOS_PDA_EJEMPLO = CONTENIDOS_PDA_POR_GRADO["5° de Primaria"]

EJEMPLO_PROBLEMICA_ANALITICO = """Problemática comunitaria identificada en el Consejo Técnico Escolar (CTE):
En el diagnóstico integral de la Escuela Primaria Revolución Social 1910, se detectó una necesidad apremiante de fortalecer la comprensión lectora, la redacción propia y la resolución de problemas multiplicativos y fraccionarios contextualizados. Además, se observa en la convivencia escolar la necesidad de reforzar la empatía, el cuidado del entorno escolar y la resolución pacífica de conflictos mediante el diálogo."""
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
from docx_generator import build_docx_planeacion
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

def extraer_embed_youtube(url_o_id: str) -> str:
    """
    Convierte cualquier enlace o identificador de YouTube al formato oficial de inserción embebida (embed).
    Asegura que los enlaces de formato 'watch?v=', 'youtu.be/', '/live/', '/shorts/', listas de reproducción
    o códigos iframe se transformen rigurosamente a 'https://www.youtube.com/embed/...' sin errores de disponibilidad ni bloqueos.
    """
    if not url_o_id or not str(url_o_id).strip():
        return "https://www.youtube.com/embed/jfKfPfyJRdk"
    
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

    # Fallback predeterminado seguro
    return "https://www.youtube.com/embed/jfKfPfyJRdk"

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

    /* Subtítulos y descripciones en contenedores claros */
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p,
    [data-testid="stSidebar"] .stCaption,
    .nem-card [data-testid="stCaptionContainer"] p,
    .nem-card .stCaption,
    [data-testid="stForm"] [data-testid="stCaptionContainer"] p {
        color: #1F2937 !important;
        -webkit-text-fill-color: #1F2937 !important;
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

    /* Contenedor desplegado (Details): Fondo claro con textos en #1F2937 */
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
       CALENDARIO INTERACTIVO DEL AÑO ACTUAL (2026)
       ======================================================= */
    .cal-wrapper {
        background: #FFFFFF;
        border: 1.5px solid #8B5CF6;
        border-radius: 14px;
        padding: 1.25rem;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(124, 58, 237, 0.10);
    }
    .cal-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 4px;
        margin: 0.75rem 0;
        text-align: center;
    }
    .cal-table th {
        background: #EDE9FE;
        color: #4C1D95 !important;
        -webkit-text-fill-color: #4C1D95 !important;
        font-weight: 700;
        padding: 8px 4px;
        border-radius: 8px;
        font-size: 0.88rem;
    }
    .cal-table td {
        padding: 9px 4px;
        font-size: 0.92rem;
        border-radius: 8px;
        color: #1F2937 !important;
        -webkit-text-fill-color: #1F2937 !important;
        background: #FAF5FF;
        transition: all 0.2s ease;
    }
    .cal-cell-active {
        background: #7C3AED !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(124, 58, 237, 0.4) !important;
    }
    .cal-cell-weekend {
        color: #6B7280 !important;
        -webkit-text-fill-color: #6B7280 !important;
        background: #F3F4F6 !important;
    }
    .cal-cell-empty {
        background: transparent !important;
        color: transparent !important;
    }

    @media (prefers-color-scheme: dark) {
        .cal-wrapper {
            background: #1E1B4B;
            border-color: #7C3AED;
        }
        .cal-table th {
            background: #2E1065;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        .cal-table td {
            background: #2E1065;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }
        .cal-cell-weekend {
            background: #1E1B4B !important;
            color: #9CA3AF !important;
            -webkit-text-fill-color: #9CA3AF !important;
        }
    }
    [data-theme="dark"] .cal-wrapper {
        background: #1E1B4B;
        border-color: #7C3AED;
    }
    [data-theme="dark"] .cal-table th {
        background: #2E1065;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    [data-theme="dark"] .cal-table td {
        background: #2E1065;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }
    [data-theme="dark"] .cal-cell-weekend {
        background: #1E1B4B !important;
        color: #9CA3AF !important;
        -webkit-text-fill-color: #9CA3AF !important;
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

def construir_catalogo_sep_2026():
    """
    Construye las 56 semanas escolares oficiales SEP del ciclo 2026.
    Semana 1 inicia el primer lunes hábil de 2026 (5 de enero de 2026).
    Mapea bi-direccionalmente:
      - número de semana (1 a 56) -> fechas y mes
      - fecha (mes, día) -> número de semana (1 a 56)
    """
    catalogo_por_semana = {}
    catalogo_por_fecha = {}

    lunes_base = datetime.date(2026, 1, 5)
    for s_num in range(1, 57):
        lunes = lunes_base + datetime.timedelta(weeks=s_num - 1)
        viernes = lunes + datetime.timedelta(days=4)
        
        dias_semana = []
        for i, nom in enumerate(DIAS_HABIL_NOMBRES):
            d_obj = lunes + datetime.timedelta(days=i)
            m_nom = MESES_2026[d_obj.month - 1] if d_obj.year == 2026 else ("Diciembre" if d_obj.year > 2026 else "Enero")
            dias_semana.append({
                "nombre_dia": nom,
                "date": d_obj,
                "dia_num": d_obj.day,
                "mes_num": d_obj.month,
                "mes_nombre": m_nom,
                "fecha_corta": f"{nom} {d_obj.day}/{m_nom[:3]}",
                "fecha_completa": f"{nom} {d_obj.day} de {m_nom} de {d_obj.year}"
            })
            if d_obj.year == 2026:
                catalogo_por_fecha[(d_obj.month, d_obj.day)] = s_num

        m_rep = MESES_2026[lunes.month - 1] if lunes.year == 2026 else "Diciembre"
        catalogo_por_semana[s_num] = {
            "semana": s_num,
            "lunes": lunes,
            "viernes": viernes,
            "mes_idx": lunes.month if lunes.year == 2026 else 12,
            "mes_nombre": m_rep,
            "rango_str": f"{lunes.day} {MESES_2026[lunes.month-1][:3]} al {viernes.day} {MESES_2026[viernes.month-1][:3]}",
            "dias_habil": dias_semana
        }

    return catalogo_por_semana, catalogo_por_fecha

CATALOGO_SEMANAS_SEP, CATALOGO_FECHAS_SEP = construir_catalogo_sep_2026()

if "cal_mes_nombre" not in st.session_state:
    st.session_state.cal_mes_nombre = "Octubre"

if "cal_semana_escolar" not in st.session_state:
    st.session_state.cal_semana_escolar = 20

if "cal_sem_idx" not in st.session_state:
    st.session_state.cal_sem_idx = 3

if "dias_seleccionados" not in st.session_state or not st.session_state.dias_seleccionados:
    st.session_state.dias_seleccionados = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

if "dias_fechas" not in st.session_state or not st.session_state.dias_fechas:
    st.session_state.dias_fechas = {
        "Lunes": "LUNES 19 DE OCTUBRE DE 2026",
        "Martes": "MARTES 20 DE OCTUBRE DE 2026",
        "Miércoles": "MIÉRCOLES 21 DE OCTUBRE DE 2026",
        "Jueves": "JUEVES 22 DE OCTUBRE DE 2026",
        "Viernes": "VIERNES 23 DE OCTUBRE DE 2026"
    }

def limpiar_todo_callback():
    """Reinicia todas las variables de estado y rota las llaves dinámicas para empezar desde cero."""
    st.session_state.widget_key += 1

    # Variables principales de generación y prompts
    st.session_state.planeacion_generada = None
    st.session_state.prompt_enviado = None
    st.session_state.archivos_procesados = {}
    st.session_state.programa_sintetico_texto = ""
    st.session_state["programa_sintetico_subido"] = False
    st.session_state["es_programa_oficial_fase5"] = False
    st.session_state.query_busqueda = ""
    st.session_state.resultados_busqueda_gratis = []
    st.session_state.query_busqueda_gratis = ""
    st.session_state.query_busqueda_enriquecida = ""
    st.session_state.contexto_url = ""
    st.session_state.cal_mes_nombre = "Octubre"
    st.session_state.cal_semana_escolar = 20
    st.session_state.cal_sem_idx = 3
    st.session_state.dias_seleccionados = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    st.session_state.dias_fechas = {
        "Lunes": "LUNES 19 DE OCTUBRE DE 2026",
        "Martes": "MARTES 20 DE OCTUBRE DE 2026",
        "Miércoles": "MIÉRCOLES 21 DE OCTUBRE DE 2026",
        "Jueves": "JUEVES 22 DE OCTUBRE DE 2026",
        "Viernes": "VIERNES 23 DE OCTUBRE DE 2026"
    }

    # Limpieza explícita de variables de selectores curriculares (listas vacías [])
    st.session_state["dias"] = []
    st.session_state["dias_seleccionados"] = []
    st.session_state["campos"] = []
    st.session_state["campos_formativos"] = []
    st.session_state["campos_sel"] = []
    st.session_state["ejes"] = []
    st.session_state["ejes_articuladores"] = []
    st.session_state["ejes_sel"] = []
    st.session_state["libros"] = []
    st.session_state["libros_sel"] = []
    st.session_state["libros_seleccionados"] = []
    st.session_state["pda"] = []
    st.session_state["pda_seleccionados"] = []

    # Limpieza explícita de variables de texto relacionadas (cadenas vacías "")
    st.session_state["contenidos"] = ""
    st.session_state["contenido_custom"] = ""
    st.session_state["custom_pda"] = ""
    st.session_state["directrices"] = ""
    st.session_state["url_referencia"] = ""

    # Limpiar cualquier clave existente en session_state vinculada con widgets dinámicos
    for k in list(st.session_state.keys()):
        for prefix in [
            "dias_", "campos_", "ejes_", "libros_", "pda_",
            "contenidos_", "custom_contenido_", "custom_pda_",
            "directrices_", "url_referencia_", "uploader_",
            "semana_", "periodo_"
        ]:
            if k.startswith(prefix):
                if isinstance(st.session_state[k], list):
                    st.session_state[k] = []
                elif isinstance(st.session_state[k], str):
                    st.session_state[k] = ""
                elif isinstance(st.session_state[k], dict):
                    st.session_state[k] = {}

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
        st.markdown("---")
        st.markdown('### <span style="color: #7C3AED; font-size: 1.2rem;">•</span> Datos de la Escuela', unsafe_allow_html=True)
        st.caption("Configuración oficial predeterminada de la Primaria Revolución Social 1910.")
    
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
                index=4 if st.session_state.widget_key == 0 else 0,
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
            ciclo_sel = st.text_input("Ciclo Escolar:", value=DATOS_PREDETERMINADOS["ciclo_escolar"], key=f"ciclo_{st.session_state.widget_key}")

        semana_seleccionada = int(st.session_state.get("cal_semana_escolar", 20))
        periodo_sel = f"Semana {semana_seleccionada}"
        dias_seleccionados = st.session_state.get("dias_seleccionados", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])

        # Píldora de estado unificado del Calendario Oficial SEP 2026
        st.markdown(
            f"<div style='background: #EDE9FE; border: 1.5px solid #8B5CF6; border-radius: 8px; padding: 0.65rem 0.85rem; margin: 0.6rem 0; font-size: 0.86rem; color: #4C1D95;'>"
            f"📅 <b>Dosificación Calendario SEP 2026:</b><br>"
            f"<b>{periodo_sel}</b> ({len(dias_seleccionados)} días activos)<br>"
            f"<span style='font-size: 0.78rem; color: #6D28D9;'>La semana escolar (1 a 56) y los días hábiles se definen directamente en el Calendario Oficial interactivo unificado del panel central.</span>"
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
            st.caption("👉 Puedes obtener una gratuita en [Google AI Studio](https://aistudio.google.com/). También puedes probar la app con la plantilla precargada de 5° grado.")
    
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
            libros_raw = LIBROS_SEP_POR_GRADO.get(grado_sel, LIBROS_SEP_POR_GRADO.get("5° de Primaria", []))
    
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
            st.markdown("<span style='color:#166534; font-size:0.8rem; font-weight:600;'>🟢 Catálogo CONALITEG 2025-2026 (En vivo)</span>", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color:#92400E; font-size:0.8rem; font-weight:600;'>🟡 Catálogo SEP NEM (Modo Respaldo)</span>", unsafe_allow_html=True)
    
        libros_sel = st.multiselect(
            "Libros de Texto SEP:",
            options=libros_disponibles,
            default=libros_disponibles[:min(3, len(libros_disponibles))] if st.session_state.widget_key == 0 else [],
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
        with st.expander("Ver directrices de esta sesión CTE", expanded=False):
            st.markdown(f"**Enfoque:** {cte_info['enfoque']}")
            st.markdown(f"**Directrices:** {cte_info['directrices']}")

        st.markdown("---")
        st.markdown('### <span style="color: #7C3AED; font-size: 1.2rem;">•</span> Sound', unsafe_allow_html=True)

        CANALES_MUSICA_DEFAULT = {
            "Lo-Fi Hip Hop (Relax / Estudio)": "https://www.youtube.com/embed/jfKfPfyJRdk",
            "Piano Clásico Relajante": "https://www.youtube.com/embed/4xDzrJKXOOY",
            "Café Jazz Instrumental": "https://www.youtube.com/embed/DXUAyRRkI6k",
            "Sonidos de la Naturaleza y Lluvia": "https://www.youtube.com/embed/mPZkdNFkNps",
            "Ondas Alfa (Enfoque Profundo)": "https://www.youtube.com/embed/WPni755-Krg",
            "Enlace Personalizado de YouTube": ""
        }

        estilo_musica_sel = st.selectbox(
            "Ambiente Musical:",
            options=list(CANALES_MUSICA_DEFAULT.keys()),
            index=0,
            help="Selecciona una atmósfera musical relajante para concentrarte al diseñar tus planeaciones.",
            key=f"musica_preset_{st.session_state.widget_key}"
        )

        url_custom_youtube = st.text_input(
            "Enlace personalizado de YouTube (opcional):",
            value="",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Pega aquí el enlace de cualquier video o playlist de YouTube para reproducirlo.",
            key=f"musica_url_{st.session_state.widget_key}"
        )

        # Resolver la URL del reproductor
        if url_custom_youtube.strip():
            url_embed_activa = extraer_embed_youtube(url_custom_youtube.strip())
        elif CANALES_MUSICA_DEFAULT.get(estilo_musica_sel):
            url_embed_activa = CANALES_MUSICA_DEFAULT[estilo_musica_sel]
        else:
            url_embed_activa = "https://www.youtube.com/embed/jfKfPfyJRdk"

        # Garantizar que la URL activa sea estrictamente formato embed oficial
        url_embed_activa = extraer_embed_youtube(url_embed_activa)

        # Reproductor seguro de YouTube incrustado mediante st.components.v1.iframe
        st.components.v1.iframe(
            src=url_embed_activa,
            height=160,
            scrolling=False
        )
    
    # Empaquetar datos de escuela
    datos_escuela_actual = {
        "nombre_escuela": escuela_nombre,
        "cct": cct,
        "docente": docente,
        "director": director,
        "grado": grado_sel,
        "fase": fase_auto,
        "grupo": grupo_sel,
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
        st.markdown(f"<div class='badge-sep'><span style='color: #7C3AED; font-size: 1.1rem;'>•</span> C.C.T. {cct}</div>", unsafe_allow_html=True)
    with cols_meta[2]:
        st.markdown(f"<div class='badge-sep'><span style='color: #7C3AED; font-size: 1.1rem;'>•</span> Docente: {docente}</div>", unsafe_allow_html=True)
    with cols_meta[3]:
        st.markdown(f"<div class='badge-sep'><span style='color: #7C3AED; font-size: 1.1rem;'>•</span> {grado_sel} ({fase_auto}) • {periodo_sel}</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
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
                f"Configurado como la fuente oficial para extraer Contenidos, PDA (5° Grado), "
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
                    st.success(f"🟢 Base de Datos Principal y Oficial Reconocida: 'Programa_Sintetico_Fase_5.pdf'. Configurado como la fuente oficial para extraer Contenidos, PDA (5° Grado), Campos Formativos y Ejes Articuladores.")
                except Exception as e:
                    st.error(f"Error al cargar ejemplo: {e}")
    
        with col_btn_ej2:
            if st.button("Cargar Guía CTE 5° (.docx)", help="Carga la guía escolar de ejemplo en Word"):
                try:
                    with open("sample_data/guia_5to_grado_ejemplo.docx", "rb") as f:
                        st.session_state.archivos_procesados["Guia_Escolar_5to.docx"] = extract_text_from_docx(f.read())
                    st.info("Guía de Consejo Técnico Escolar en .docx cargada.")
                except Exception as e:
                    st.error(f"Error al cargar ejemplo: {e}")
    
    with col_texto:
        st.markdown("**Problemática Comunitaria del Plan Analítico o Directrices Docentes:**")
        directrices_input = st.text_area(
            "Directrices del docente / acuerdos de Consejo Técnico Escolar (CTE):",
            value=EJEMPLO_PROBLEMICA_ANALITICO if st.session_state.widget_key == 0 else "",
            height=190,
            help="Pega aquí la problemática comunitaria detectada en el diagnóstico escolar, los intereses de tus alumnos o acuerdos pedagógicos.",
            key=f"directrices_{st.session_state.widget_key}"
        )
    
    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
    
    # ==========================================
    # CALENDARIO INTERACTIVO OFICIAL SEP 2026 Y SELECCIÓN UNIFICADA (DÍAS Y SEMANAS 1 A 56)
    # ==========================================
    st.markdown("""
    <div class="nem-card-header">
        <span style="color: #7C3AED; font-size: 1.5rem; line-height: 1;">•</span>
        <h3 class="nem-card-title">Calendario Oficial SEP 2026 y Dosificación Unificada (Semanas 1 a 56 y Días)</h3>
    </div>
    """, unsafe_allow_html=True)
    st.caption(
        "Módulo unificado de calendario oficial para el ciclo escolar 2026 en México. "
        "Define la semana escolar oficial de la SEP (1 a 56) y selecciona de forma visual o por casillas "
        "los días exactos que abarcará la planeación didáctica (lunes a viernes o jornadas particulares). "
        "Ambos selectores están conectados de forma bidireccional y alimentan estrictamente las secuencias didácticas."
    )

    # Modo de selección y sincronización bidireccional
    col_modo, col_info_sep = st.columns([1.2, 1.3])
    with col_modo:
        modo_navegacion = st.radio(
            "Método de Selección Temporal:",
            options=["Por Semana Escolar SEP (1 a 56)", "Por Mes del Calendario 2026"],
            horizontal=True,
            key=f"modo_cal_sel_{st.session_state.widget_key}",
            help="Elige si prefieres dosificar buscando directamente el número de semana SEP (1 a 56) o navegando por los meses del año 2026."
        )

    # Variables de control
    semana_actual_init = int(st.session_state.get("cal_semana_escolar", 20))
    if semana_actual_init not in CATALOGO_SEMANAS_SEP:
        semana_actual_init = 20

    col_ctrls, col_visual = st.columns([1.1, 1.2])

    with col_ctrls:
        if modo_navegacion == "Por Semana Escolar SEP (1 a 56)":
            semana_sep_sel = st.selectbox(
                "🏫 Semana Escolar Oficial SEP (1 a 56):",
                options=list(range(1, 57)),
                index=semana_actual_init - 1,
                format_func=lambda s: f"Semana {s} SEP — {CATALOGO_SEMANAS_SEP[s]['rango_str']} ({CATALOGO_SEMANAS_SEP[s]['mes_nombre']} 2026)",
                key=f"sel_semana_sep_{st.session_state.widget_key}",
                help="Selecciona la semana del calendario oficial de la SEP. Los días y meses se sincronizan automáticamente."
            )
            info_semana = CATALOGO_SEMANAS_SEP[semana_sep_sel]
            cal_mes_actual = info_semana["mes_nombre"]
            m_idx = info_semana["mes_idx"]
            rango_fechas_str = info_semana["rango_str"]
            active_week_dates = [d["date"] for d in info_semana["dias_habil"]]
            st.session_state.cal_semana_escolar = semana_sep_sel
            st.session_state.cal_mes_nombre = cal_mes_actual
            semana_seleccionada = semana_sep_sel
            periodo_sel = f"Semana {semana_seleccionada}"

            st.markdown(
                f"<div style='background-color: #F5F3FF; border: 1px solid #C4B5FD; border-radius: 8px; padding: 0.5rem 0.8rem; font-size: 0.88rem; color: #4C1D95; margin-top: 0.3rem;'>"
                f"📅 <b>Rango Calendario 2026 Sincronizado:</b> {rango_fechas_str} de {cal_mes_actual} de 2026"
                f"</div>",
                unsafe_allow_html=True
            )

        else: # "Por Mes del Calendario 2026"
            idx_mes_actual = MESES_2026.index(st.session_state.get("cal_mes_nombre", "Octubre"))
            cal_mes_actual = st.selectbox(
                "📅 Mes del Año Actual (2026):",
                options=MESES_2026,
                index=idx_mes_actual,
                help="Selecciona el mes del año 2026 para visualizar y dosificar tus sesiones escolares.",
                key=f"sel_mes_cal_{st.session_state.widget_key}"
            )
            st.session_state.cal_mes_nombre = cal_mes_actual
            m_idx = MESES_2026.index(cal_mes_actual) + 1

            cal_obj = calendar.Calendar(firstweekday=0)
            month_weeks = cal_obj.monthdatescalendar(2026, m_idx)

            def format_sem_label(idx_w: int) -> str:
                w_d = month_weeks[idx_w]
                m_fin = MESES_2026[w_d[4].month - 1]
                return f"Semana {idx_w + 1} ({w_d[0].day} al {w_d[4].day} de {m_fin})"

            cal_sem_idx = st.selectbox(
                "📆 Bloque Semanal en el Mes:",
                options=range(len(month_weeks)),
                format_func=format_sem_label,
                index=min(st.session_state.get("cal_sem_idx", 3), len(month_weeks) - 1),
                help="Selecciona el bloque semanal de trabajo dentro del mes elegido.",
                key=f"sel_sem_mes_{st.session_state.widget_key}"
            )
            st.session_state.cal_sem_idx = cal_sem_idx
            active_week_full = month_weeks[cal_sem_idx]
            active_week_dates = active_week_full[:5]

            # Detección automática dinámica de Semana SEP a partir de la fecha seleccionada
            lun_d = active_week_dates[0]
            vie_d = active_week_dates[4]
            sem_detectada = CATALOGO_FECHAS_SEP.get((lun_d.month, lun_d.day)) or CATALOGO_FECHAS_SEP.get((vie_d.month, vie_d.day)) or 20
            
            semana_sep_sel = st.number_input(
                "🏫 Semana Escolar SEP detectada automáticamente (1 a 56):",
                min_value=1,
                max_value=56,
                value=int(sem_detectada),
                step=1,
                help="Semana oficial detectada a partir de las fechas del calendario 2026 (puedes ajustarla si tu escuela maneja una numeración particular).",
                key=f"num_sem_detectada_{st.session_state.widget_key}"
            )
            st.session_state.cal_semana_escolar = semana_sep_sel
            semana_seleccionada = semana_sep_sel
            periodo_sel = f"Semana {semana_seleccionada}"
            rango_fechas_str = f"{lun_d.day} {MESES_2026[lun_d.month-1][:3]} al {vie_d.day} {MESES_2026[vie_d.month-1][:3]}"

            st.markdown(
                f"<div style='background-color: #ECFDF5; border: 1px solid #10B981; border-radius: 8px; padding: 0.5rem 0.8rem; font-size: 0.88rem; color: #065F46; margin-top: 0.3rem;'>"
                f"🟢 <b>Semana SEP Detectada:</b> Semana {semana_sep_sel} ({rango_fechas_str} 2026)"
                f"</div>",
                unsafe_allow_html=True
            )

    # Fechas del bloque hábil seleccionado (Lunes a Viernes)
    fechas_bloque = {
        nom: active_week_dates[i] for i, nom in enumerate(DIAS_HABIL_NOMBRES)
    }

    # Casillas interactivas para elegir días específicos del mes
    st.markdown("**Selección de Días Específicos a Planear en la Semana:**")
    st.caption("Marca las casillas de los días hábiles del mes en los que se impartirá clase para estructurar las secuencias didácticas:")

    col_btn_q1, col_btn_q2, col_btn_q3, col_btn_q4 = st.columns([1, 1, 1, 1])
    with col_btn_q1:
        if st.button("Semana Completa (Lun-Vie)", key=f"btn_cal_all_{st.session_state.widget_key}", help="Seleccionar los 5 días hábiles"):
            st.session_state.dias_seleccionados = DIAS_HABIL_NOMBRES.copy()
            st.rerun()
    with col_btn_q2:
        if st.button("Lun, Mié y Vie", key=f"btn_cal_lmv_{st.session_state.widget_key}", help="Seleccionar Lunes, Miércoles y Viernes"):
            st.session_state.dias_seleccionados = ["Lunes", "Miércoles", "Viernes"]
            st.rerun()
    with col_btn_q3:
        if st.button("Mar y Jue", key=f"btn_cal_mj_{st.session_state.widget_key}", help="Seleccionar Martes y Jueves"):
            st.session_state.dias_seleccionados = ["Martes", "Jueves"]
            st.rerun()
    with col_btn_q4:
        if st.button("Solo Lunes", key=f"btn_cal_lun_{st.session_state.widget_key}", help="Seleccionar únicamente el Lunes"):
            st.session_state.dias_seleccionados = ["Lunes"]
            st.rerun()

    col_dias_chk = st.columns(5)
    dias_elegidos = []
    dias_fechas_calculadas = {}
    dias_previos = st.session_state.get("dias_seleccionados", DIAS_HABIL_NOMBRES)

    for idx_d, nom_d in enumerate(DIAS_HABIL_NOMBRES):
        dt_obj = fechas_bloque[nom_d]
        mes_dt_nom = MESES_2026[dt_obj.month - 1]
        chk_label = f"**{nom_d}**\n{dt_obj.day} de {mes_dt_nom[:3]}"
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
        st.warning("⚠️ Debes seleccionar al menos un día hábil. Se considerará 'Lunes' automáticamente.")
        dias_elegidos = ["Lunes"]
        dt_lun = fechas_bloque["Lunes"]
        dias_fechas_calculadas["Lunes"] = f"Lunes {dt_lun.day} de {MESES_2026[dt_lun.month - 1]} de {dt_lun.year}"

    # Sincronización en session_state y variables de ejecución
    dias_seleccionados = dias_elegidos
    st.session_state.dias_seleccionados = dias_seleccionados
    st.session_state.dias_fechas = dias_fechas_calculadas

    # Actualizar inmediatamente datos_escuela_actual con las fechas y días sincronizados
    datos_escuela_actual["dias_seleccionados"] = dias_seleccionados
    datos_escuela_actual["dias_planeados"] = dias_seleccionados
    datos_escuela_actual["dias_fechas"] = dias_fechas_calculadas
    datos_escuela_actual["semana"] = semana_seleccionada
    datos_escuela_actual["semana_seleccionada"] = semana_seleccionada
    datos_escuela_actual["periodo"] = periodo_sel

    # Visualización gráfica del mes actual (2026) en col_visual
    with col_visual:
        st.markdown(f"**Vista Gráfica del Mes: {cal_mes_actual} 2026**")
        cal_obj_vis = calendar.Calendar(firstweekday=0)
        month_weeks_vis = cal_obj_vis.monthdatescalendar(2026, m_idx)
        fechas_activas_set = set(fechas_bloque[d] for d in dias_seleccionados)
        cal_html_rows = []
        for w in month_weeks_vis:
            cells = []
            for d in w:
                if d.month != m_idx:
                    cells.append(f'<td class="cal-cell-empty" style="opacity: 0.35;">{d.day}</td>')
                elif d in fechas_activas_set:
                    cells.append(f'<td class="cal-cell-active" title="Día seleccionado para planeación: {d.day} de {cal_mes_actual}"><strong>{d.day}</strong></td>')
                elif d.weekday() >= 5:
                    cells.append(f'<td class="cal-cell-weekend">{d.day}</td>')
                else:
                    cells.append(f'<td>{d.day}</td>')
            cal_html_rows.append('<tr>' + ''.join(cells) + '</tr>')

        cal_tabla_html = f"""
        <div class="cal-wrapper">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-weight: 700; color: #4C1D95; font-size: 0.95rem;">{cal_mes_actual.upper()} 2026</span>
                <span style="font-size: 0.8rem; color: #6D28D9; font-weight: 600;">Semana Escolar {semana_seleccionada} SEP</span>
            </div>
            <table class="cal-table">
                <thead><tr><th>Lun</th><th>Mar</th><th>Mié</th><th>Jue</th><th>Vie</th><th>Sáb</th><th>Dom</th></tr></thead>
                <tbody>{''.join(cal_html_rows)}</tbody>
            </table>
            <div style="display: flex; gap: 12px; font-size: 0.78rem; color: #4B5563; margin-top: 4px; justify-content: center;">
                <span><span style="display: inline-block; width: 10px; height: 10px; background: #7C3AED; border-radius: 3px; margin-right: 4px;"></span>Activo</span>
                <span><span style="display: inline-block; width: 10px; height: 10px; background: #FAF5FF; border: 1px solid #C4B5FD; border-radius: 3px; margin-right: 4px;"></span>Hábiles</span>
                <span><span style="display: inline-block; width: 10px; height: 10px; background: #F3F4F6; border-radius: 3px; margin-right: 4px;"></span>Fin de semana</span>
            </div>
        </div>
        """
        st.markdown(cal_tabla_html, unsafe_allow_html=True)

    fechas_resumen_txt = ", ".join(dias_fechas_calculadas.values())
    st.markdown(
        f"<div style='background: #EDE9FE; border: 1.5px solid #8B5CF6; border-radius: 8px; padding: 0.65rem 1rem; color: #4C1D95; font-size: 0.92rem; font-weight: 600; margin-top: 0.5rem;'>"
        f"🗓️ <b>Dosificación Oficial SEP 2026 Unificada:</b> Semana {semana_seleccionada} de 56 ({rango_fechas_str} 2026) | "
        f"<b>Días Activos:</b> {fechas_resumen_txt} "
        f"<span style='background: #7C3AED; color: #FFFFFF; padding: 2px 8px; border-radius: 12px; font-size: 0.82rem; margin-left: 8px;'>{len(dias_seleccionados)} Sesión(es) Didáctica(s)</span>"
        f"</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)

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
            default=["Lenguajes", "Saberes y Pensamiento Científico"] if st.session_state.widget_key == 0 else [],
            help="La NEM promueve la interdisciplinariedad articulando varios campos formativos en un mismo proyecto.",
            key=f"campos_{st.session_state.widget_key}"
        )
    
        st.markdown("**Ejes Articuladores en Acción:**")
        ejes_sel = st.multiselect(
            "Selecciona los Ejes Articuladores que guían el proyecto:",
            options=EJES_ARTICULADORES,
            default=["Pensamiento crítico", "Vida saludable", "Apropiación de las culturas a través de la lectura y la escritura"] if st.session_state.widget_key == 0 else [],
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
    
    # Articulación Curricular: Contenidos y PDA (100% Dinámico por Grado y Fase)
    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    st.markdown('#### <span style="color: #7C3AED; font-size: 1.2rem;">•</span> Articulación Curricular: Contenidos y Procesos de Desarrollo de Aprendizaje (PDA)', unsafe_allow_html=True)
    
    # Subtítulo y encabezado dinámicos según el grado y fase seleccionados
    st.subheader(f"Selecciona los Contenidos y PDA de {grado_seleccionado} recomendados para tu planeación (puedes personalizarlos abajo):")
    st.markdown(f"**Banco curricular sugerido para {fase_correspondiente} / {grado_seleccionado}:**")
    
    # Extraer el banco de contenidos y PDA correspondiente exclusivamente al grado activo
    banco_grado_activo = CONTENIDOS_PDA_POR_GRADO.get(
        grado_seleccionado,
        CONTENIDOS_PDA_POR_GRADO.get("5° de Primaria", {})
    )
    
    # Pre-poblar según los campos formativos elegidos para el grado activo
    sugerencias_pda = []

    # 1. Integración de Contenidos y PDA del Programa Sintético Subido (Base de Datos Oficial Fase 5 - 5° Grado)
    pda_doc_subido = st.session_state.get("pda_extraidos_programa", [])
    if pda_doc_subido:
        for item in pda_doc_subido:
            c_item = item.get("campo", "Lenguajes")
            if not campos_sel or c_item in campos_sel:
                sugerencias_pda.append({
                    "campo": c_item,
                    "contenido": item.get("contenido", ""),
                    "pda": item.get("pda", ""),
                    "grado": "5° de Primaria",
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
            f"🟢 <b>Base de Datos Principal y Oficial Activa:</b> <code>{nom_db}</code>. Contenidos y PDA de 5° de Primaria vinculados prioritariamente."
            f"</div>",
            unsafe_allow_html=True
        )

    if sugerencias_pda:
        opciones_display = []
        for item in sugerencias_pda:
            if item.get("origen") == "Programa Sintético Fase 5 (Oficial Subido)":
                opciones_display.append(f"⭐ [Oficial 5° - {item['campo']}] {item['contenido'][:55]}... — PDA: {item['pda'][:65]}...")
            else:
                opciones_display.append(f"[{item['campo']}] {item['contenido'][:60]}... — PDA: {item['pda'][:70]}...")

        pda_seleccionados_indices = st.multiselect(
            f"Contenidos y PDA oficiales disponibles para {grado_seleccionado}:",
            options=range(len(sugerencias_pda)),
            format_func=lambda x: opciones_display[x],
            default=[0, 1] if (st.session_state.widget_key == 0 and len(sugerencias_pda) >= 2) else ([0] if (st.session_state.widget_key == 0 and len(sugerencias_pda) == 1) else []),
            key=f"pda_{st.session_state.widget_key}",
            help=f"Mostrando los Contenidos y PDA oficiales del programa sintético para {grado_seleccionado} ({fase_correspondiente})."
        )
        items_pda_final = [sugerencias_pda[i] for i in pda_seleccionados_indices]
    else:
        items_pda_final = []
        st.info(f"No hay Contenidos y PDA precargados para los campos formativos seleccionados en {grado_seleccionado}. Puedes redactarlos abajo.")
    
    # Área para agregar o editar Contenido y PDA manuales
    with st.expander(f"Personalizar o escribir Contenidos y PDA manualmente para {grado_seleccionado}", expanded=(len(items_pda_final) == 0)):
        val_cont_def = items_pda_final[0]["contenido"] if items_pda_final else (sugerencias_pda[0]["contenido"] if sugerencias_pda else f"Contenido sintético para {grado_seleccionado}.")
        val_pda_def = items_pda_final[0]["pda"] if items_pda_final else (sugerencias_pda[0]["pda"] if sugerencias_pda else f"Procesos de Desarrollo de Aprendizaje para {grado_seleccionado}.")
        contenido_custom = st.text_area(
            f"Contenido Sintético personalizado ({grado_seleccionado}):",
            value=val_cont_def if st.session_state.widget_key == 0 else "",
            height=80,
            key=f"contenidos_{st.session_state.widget_key}"
        )
        pda_custom = st.text_area(
            f"Procesos de Desarrollo de Aprendizaje (PDA) personalizados ({grado_seleccionado}):",
            value=val_pda_def if st.session_state.widget_key == 0 else "",
            height=100,
            key=f"custom_pda_{st.session_state.widget_key}"
        )
        items_pda_final = [{
            "campo": campos_sel[0] if campos_sel else "Lenguajes",
            "contenido": contenido_custom,
            "pda": pda_custom
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
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
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
        prellenando todos los datos curriculares e institucionales seleccionados
        y colocando marcadores de posición explícitos para la redacción docente,
        estructurada estrictamente para los días seleccionados.
        """
        escuela = datos_escuela.get('nombre_escuela', 'Primaria Revolución Social 1910')
        cct = datos_escuela.get('cct', '10EPR0361N')
        docente = datos_escuela.get('docente', 'Aday Domínguez Domínguez')
        director = datos_escuela.get('director', 'José Guillermo Borjas Díaz')
        grado = datos_escuela.get('grado', '5° de Primaria')
        fase = datos_escuela.get('fase', 'Fase 5')
        grupo = datos_escuela.get('grupo', 'A')
        periodo = datos_escuela.get('periodo', 'Semana 20')
        ciclo = datos_escuela.get('ciclo_escolar', '2025-2026')
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
        problemica_txt = directrices.strip() if directrices and directrices.strip() else "[Redactar aquí la problemática identificada en el diagnóstico escolar o contexto comunitario]"
    
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
                filas_curricular.append(f"| **{c_campo}** | {c_cont} | {c_pda} | {libros_txt} |")
        else:
            filas_curricular.append(f"| **{campos_txt}** | [Redactar Contenido Sintético aquí] | [Redactar PDA aquí] | {libros_txt} |")
        
        tabla_curricular_md = "\n".join(filas_curricular)
    
        # Rutinas matutinas y secuencias didácticas generadas estrictamente para los días seleccionados
        dias_fechas = datos_escuela.get("dias_fechas", {}) if isinstance(datos_escuela, dict) else {}
        rutinas_md = ""
        secuencias_md = ""
        for s, nombre_dia in enumerate(dias_seleccionados, 1):
            fecha_dia = dias_fechas.get(nombre_dia, nombre_dia)
            rutinas_md += f"""
    ### Sesión {s} ({fecha_dia}):
    - **Dictado:** [Redactar 5 palabras clave para dictado reflexivo aquí]
    - **Cálculo Mental:** [Redactar 5 operaciones de cálculo mental aquí]
    - **Problema Razonado:** [Redactar situación problemática contextualizada aquí]
    """
            secuencias_md += f"""
    ### Sesión {s} (**Día: {fecha_dia}**) - [Nombre de la Sesión y Momento Metodológico]
    - **Tiempo estimado:** 90 minutos
    - **Inicio (15-20 min):** [Redactar actividades de inicio aquí]
    - **Desarrollo (50-60 min):** [Redactar actividades de desarrollo aquí]
    - **Cierre (15-20 min):** [Redactar actividades de cierre aquí]
    - **Recursos didácticos y materiales:** {libros_txt}, libreta de apuntes y materiales del aula.
    - **Evidencia / Producto de la sesión:** [Redactar producto o evidencia de aprendizaje aquí]
    """
    
        dias_str = ", ".join(dias_fechas.get(d, d) for d in dias_seleccionados)
    
        return f"""# I. DATOS DE IDENTIFICACIÓN Y DOSIFICADOR GENERAL DEL PROYECTO
    
    - **Nombre del Proyecto:** [Nombre del Proyecto de Intervención Docente]
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
    
    # II. ARTICULACIÓN CURRICULAR (TABLA NEM)
    
    | Campo Formativo | Contenido Sintético | Procesos de Desarrollo de Aprendizaje (PDA) | Vinculación con Libros SEP (LTG) |
    | :--- | :--- | :--- | :--- |
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
    
    query_tema = st.text_input(
        "Tema, Contenido o PDA que deseas investigar:",
        placeholder="Escribe aquí el tema, Contenido o PDA (Ej. Fotosíntesis 5° primaria, cálculo mental lúdico...)",
        key="query_busqueda"
    )
    
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
            query_busqueda = f"actividades didácticas escolares primaria Nueva Escuela Mexicana {grado_seleccionado} {campo_formativo} {pda_o_contenido}"
            with st.spinner("Buscando recursos educativos en la web (sin gastar tokens)..."):
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
    # SECCIÓN 3: BOTONES DE GENERACIÓN
    # ==========================================
    st.markdown("""
    <div class="nem-card-header">
        <span style="color: #7C3AED; font-size: 1.5rem; line-height: 1;">•</span>
        <h3 class="nem-card-title">3. Generación Automatizada del Plano Didáctico</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col_btn_gen, col_btn_demo = st.columns([1.5, 1.2])
    
    with col_btn_gen:
        btn_generar = st.button("Generar Planeación con Gemini", type="primary", use_container_width=True)
        btn_busqueda_web = st.button(
            "Generar Planeación con Búsqueda Web",
            key="btn_generar_web",
            use_container_width=True,
            help="Consulta la web en tiempo real con Google Search Grounding para enriquecer la secuencia didáctica con dinámicas, noticias y ejemplos prácticos recientes."
        )
        btn_plantilla_base = st.button(
            "Descargar Plantilla Base (Sin IA)",
            use_container_width=True,
            help="Genera directamente la plantilla oficial en Word (.docx) y PDF con tus datos escolares y curriculares prellenados, sin realizar llamadas a la IA."
        )
    
    with col_btn_demo:
        btn_demo = st.button(
            f"Cargar Ejemplo Completo ({grado_sel}) [Vista Previa Rápida]",
            use_container_width=True,
            help=f"Muestra una planeación oficial completa para {grado_sel} sin consumir cuota de API."
        )
    
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
    
                    if not uploaded_prog:
                        with st.status(f"🔍 Búsqueda de Respaldo SEP: Rastreando Programa Sintético oficial ({fase_correspondiente})...", expanded=True) as status_box:
                            st.write("Buscando en portales oficiales de la SEP (`site:sep.gob.mx OR site:conaliteg.sep.gob.mx`)...")
                            resumen_scraping, scraping_exitoso = buscar_programa_sintetico_sep(fase_correspondiente)
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
                        fase_seleccionada=fase_correspondiente,
                        fallback_programa_sintetico=scraping_fallido,
                        num_sesiones=num_sesiones,
                        api_key=active_api_key,
                        modelo="gemini-3.8-flash",
                        guia_cte_detalle=cte_info,
                        busqueda_web=False,
                        contexto_url=contexto_url
                    )
                    st.session_state.planeacion_generada = plan_generado
                    st.session_state.prompt_enviado = prompt_utilizado
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
            st.error("⚠️ Para generar con Búsqueda Web necesitas ingresar tu API Key en la barra lateral izquierda. Si aún no la tienes, puedes hacer clic en 'Descargar Plantilla Base (Sin IA)' o 'Cargar Ejemplo Completo 5° Grado'.")
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
    
                    if not uploaded_prog:
                        with st.status(f"🔍 Búsqueda de Respaldo SEP: Rastreando Programa Sintético oficial ({fase_correspondiente})...", expanded=True) as status_box:
                            st.write("Buscando en portales oficiales de la SEP (`site:sep.gob.mx OR site:conaliteg.sep.gob.mx`)...")
                            resumen_scraping, scraping_exitoso = buscar_programa_sintetico_sep(fase_correspondiente)
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
    
                    # 3. Enviar a Gemini con Google Search Grounding habilitado
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
                        fase_seleccionada=fase_correspondiente,
                        fallback_programa_sintetico=scraping_fallido,
                        num_sesiones=num_sesiones,
                        api_key=active_api_key,
                        modelo="gemini-3.8-flash",
                        guia_cte_detalle=cte_info,
                        busqueda_web=True,
                        contexto_url=contexto_url
                    )
                    st.session_state.planeacion_generada = plan_generado
                    st.session_state.prompt_enviado = prompt_utilizado
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
            st.success("📄 ¡Plantilla base generada con éxito! Puedes descargar tu archivo en Word (.docx) o PDF inmediatamente en los botones de abajo.")
    
    if btn_demo:
        with st.spinner(f"Cargando plantilla pedagógica institucional de {grado_sel}..."):
            demo_plan = generate_sample_fallback(
                datos_escuela=datos_escuela_actual,
                campos_formativos=campos_sel if campos_sel else ["Lenguajes", "Saberes y Pensamiento Científico"],
                metodologia=metodologia_sel,
                ejes=ejes_sel if ejes_sel else ["Pensamiento crítico", "Vida saludable"],
                dias_seleccionados=dias_seleccionados
            )
            st.session_state.planeacion_generada = demo_plan
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
        nombre_base = f"Planeacion_{escuela_nombre.replace(' ', '_')}_{grado_sel[:2]}_{periodo_sel.replace(' ', '_')}"
        
        with col_d1:
            st.download_button(
                label="Descargar Word (.docx) [Plantilla Oficial]",
                data=docx_buffer,
                file_name=f"{nombre_base}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                help="Generado con la estructura exacta del documento original: Horario Escolar, Dosificador General, tablas por día con Inicio/Desarrollo/Cierre y firmas."
            )
    
        with col_d2:
            st.download_button(
                label="Descargar PDF (.pdf) [Listo para Imprimir]",
                data=pdf_buffer,
                file_name=f"{nombre_base}.pdf",
                mime="application/pdf",
                use_container_width=True,
                help="Documento formateado con membrete SEP, tablas de Horario Escolar, rutinas matutinas y firmas institucionales."
            )
    
        with col_d3:
            st.download_button(
                label="Descargar Markdown (.md) [Texto]",
                data=st.session_state.planeacion_generada,
                file_name=f"{nombre_base}.md",
                mime="text/markdown",
                use_container_width=True,
                help="Texto estructurado oficial con encabezados y tablas en Markdown."
            )
    
        st.caption("✓ **Replicación exacta del formato:** Conserva el membrete, el Horario Escolar, el Dosificador General de Proyectos, las tablas diarias (Dictado, Cálculo, Problema, Inicio, Desarrollo, Cierre), Recursos, Evaluación y los espacios para las firmas oficiales de **Aday Domínguez Domínguez** (Docente) y **José Guillermo Borjas Díaz** (Director).")
    
        st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    
        # Pestañas interactivas para revisar la planeación
        tab_completa, tab_dosificador, tab_rutina, tab_sesiones, tab_evaluacion, tab_ajustes = st.tabs([
            "Documento Completo",
            "Dosificador y Articulación",
            "Rutina de Inicio del Día",
            "Secuencia por Sesiones",
            "Instrumentos de Evaluación",
            "Ajustes Razonables (BAP/DUA)"
        ])
    
        with tab_completa:
            st.markdown(st.session_state.planeacion_generada)
    
        with tab_dosificador:
            st.markdown("### Dosificación General y Articulación Curricular (NEM)")
            # Extraer secciones de articulación si están disponibles
            partes = st.session_state.planeacion_generada.split("# ")
            for p in partes:
                if p.startswith("I. ") or p.startswith("II. "):
                    st.markdown("# " + p)
    
        with tab_rutina:
            st.markdown("### Rutina Matutina Permanente (Dictado, Cálculo Mental y Problema Razonado)")
            partes = st.session_state.planeacion_generada.split("# ")
            encontrado = False
            for p in partes:
                if "ACTIVIDADES DE INICIO DEL DÍA" in p or "III. " in p:
                    st.markdown("# " + p)
                    encontrado = True
            if not encontrado:
                st.info("Revisa la pestaña de 'Documento Completo' para ver las actividades matutinas.")
    
        with tab_sesiones:
            st.markdown("### Secuencia Didáctica de Intervención Docente (Inicio, Desarrollo y Cierre)")
            partes = st.session_state.planeacion_generada.split("# ")
            encontrado = False
            for p in partes:
                if "SECUENCIA DIDÁCTICA" in p or "IV. " in p:
                    st.markdown("# " + p)
                    encontrado = True
            if not encontrado:
                st.info("Revisa la pestaña de 'Documento Completo' para ver el desglose de sesiones.")
    
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
    
# ==========================================
# PIE DE PÁGINA INSTITUCIONAL
# ==========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748B; font-size: 0.85rem; padding: 1.5rem 0;">
    Desarrollado para la labor pedagógica
</div>
""", unsafe_allow_html=True)
