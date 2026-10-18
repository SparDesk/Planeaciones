"""
Catálogo curricular oficial de la Nueva Escuela Mexicana (NEM) - SEP México.
Contiene Fases, Metodologías sociocríticas, Ejes articuladores,
y un banco curricular de referencia para Primaria (con énfasis en Fase 5 / 5° Grado).
"""

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
    "periodo": "Semana 20 de 37",
    "ciclo_escolar": "2026-2027",
    "turno": "Matutino"
}

FASES_GRADOS = {
    "Fase 3": ["1° de Primaria", "2° de Primaria"],
    "Fase 4": ["3° de Primaria", "4° de Primaria"],
    "Fase 5": ["5° de Primaria", "6° de Primaria"]
}

DICCIONARIO_FASES_NEM = {
    "1° de Primaria": "Fase 3",
    "2° de Primaria": "Fase 3",
    "3° de Primaria": "Fase 4",
    "4° de Primaria": "Fase 4",
    "5° de Primaria": "Fase 5",
    "6° de Primaria": "Fase 5"
}

def determinar_fase_nem(grado: str) -> str:
    """Determina la Fase oficial de la Nueva Escuela Mexicana según el grado seleccionado."""
    g_str = str(grado)
    for g_key, f_val in DICCIONARIO_FASES_NEM.items():
        if g_key in g_str:
            return f_val
    if "1" in g_str or "2" in g_str:
        return "Fase 3"
    elif "3" in g_str or "4" in g_str:
        return "Fase 4"
    return "Fase 5"

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

LIBROS_SEP_POR_GRADO = {
    "1° de Primaria": [
        "Proyectos de Aula (1° grado)",
        "Proyectos Escolares (1° grado)",
        "Proyectos Comunitarios (1° grado)",
        "Nuestros Saberes: Libro para alumnos, maestros y familia (1° grado)",
        "Múltiples Lenguajes (1° grado)",
        "Múltiples Lenguajes: Trazos y palabras (1° grado)"
    ],
    "2° de Primaria": [
        "Proyectos de Aula (2° grado)",
        "Proyectos Escolares (2° grado)",
        "Proyectos Comunitarios (2° grado)",
        "Nuestros Saberes: Libro para alumnos, maestros y familia (2° grado)",
        "Múltiples Lenguajes (2° grado)"
    ],
    "3° de Primaria": [
        "Proyectos de Aula (3° grado)",
        "Proyectos Escolares (3° grado)",
        "Proyectos Comunitarios (3° grado)",
        "Nuestros Saberes: Libro para alumnos, maestros y familia (3° grado)",
        "Múltiples Lenguajes (3° grado)"
    ],
    "4° de Primaria": [
        "Proyectos de Aula (4° grado)",
        "Proyectos Escolares (4° grado)",
        "Proyectos Comunitarios (4° grado)",
        "Nuestros Saberes: Libro para alumnos, maestros y familia (4° grado)",
        "Múltiples Lenguajes (4° grado)",
        "Cartografía de México y el mundo (Fases 4 y 5)"
    ],
    "5° de Primaria": [
        "Proyectos de Aula (5° grado)",
        "Proyectos Escolares (5° grado)",
        "Proyectos Comunitarios (5° grado)",
        "Nuestros Saberes: Libro para alumnos, maestros y familia (5° grado)",
        "Múltiples Lenguajes (5° grado)",
        "Cartografía de México y el mundo (5° grado)"
    ],
    "6° de Primaria": [
        "Proyectos de Aula (6° grado)",
        "Proyectos Escolares (6° grado)",
        "Proyectos Comunitarios (6° grado)",
        "Nuestros Saberes: Libro para alumnos, maestros y familia (6° grado)",
        "Múltiples Lenguajes (6° grado)",
        "Cartografía de México y el mundo (6° grado)"
    ]
}

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

LIBROS_SEP_RECOMENDADOS = LIBROS_SEP_POR_GRADO["5° de Primaria"]

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
