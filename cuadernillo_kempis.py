"""
Módulo de Integración Curricular y Didáctica:
Catálogo Oficial de Proyectos, Recursos y Cuadernillos Didácticos (37 Semanas SEP - Ciclo 2026-2027).

Integra, indexa y dosifica los proyectos integradores, fichas vivenciales, rutinas matutinas
y anexos imprimibles para cada una de las 37 semanas lectivas oficiales del Ciclo Escolar 2026-2027 (Fase 5 / 6° Grado),
articulados con los 4 Campos Formativos de la Nueva Escuela Mexicana (NEM) e integrando con máxima fidelidad
los Cuadernillos de la Profa Kempis (Semanas 6 y 7).
"""

from typing import Dict, List, Any, Optional, Union

# Diccionario especializado para Semanas 6 y 7 (Profa Kempis)
CUADERNILLO_KEMPIS_DATA: Dict[int, Dict[str, Any]] = {
    6: {
        "semana": 6,
        "titulo_general": "Cuadernillo de Actividades Didácticas — Semana 6 (Profa Kempis)",
        "titulo_proyecto": "Cuadernillo Profa Kempis: Alimentos Procesados, Sellos y Textos Literarios",
        "periodo_sugerido": "Semana 6 de 37 (Octubre - Ciclo 2026-2027)",
        "mes_correspondiente": "Octubre",
        "año": 2026,
        "trimestre": 1,
        "descripcion": "Recursos didácticos, anexos imprimibles y fichas de trabajo para el desarrollo de proyectos en Lenguajes, Ciencias, Formación Ética y Convivencia.",
        "efemeride_principal": {
            "nombre": "Descubrimiento de América y Encuentro de Dos Mundos (12 de Octubre)",
            "fecha": "12 de Octubre",
            "anexo_nombre": "Anexo 6.5: Línea del tiempo y análisis crítico del 12 de Octubre",
            "anexo_descripcion": "Ficha de trabajo para el análisis reflexivo y contextualizado del intercambio cultural y respeto a los pueblos originarios.",
            "actividad": "Elaborar una línea del tiempo ilustrada sobre los viajes de Cristóbal Colón y reflexionar en asamblea sobre el intercambio cultural y el respeto a los pueblos originarios."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Textos literarios: El cuento y sus partes (planteamiento, nudo, desenlace y tipos de narrador)",
                "pda_vinculado": "Lee y analiza textos literarios e identifica la estructura de la narración, las relaciones de causalidad y temporalidad, y describe personajes y escenarios.",
                "inicio": "Presentar una caja sorpresa con títulos de cuentos clásicos y contemporáneos. Recuperar saberes previos: ¿Qué distingue a un cuento de una noticia o un texto informativo?",
                "desarrollo": "Lectura guiada del cuento seleccionado. En equipos, completar el organizador gráfico del Anexo 6.1 clasificando inicio/planteamiento, nudo/conflicto y desenlace, identificando adjetivos calificativos y nexos temporales.",
                "cierre": "Puesta en común en plenaria. Los alumnos comparten el esquema de su cuento y argumentan qué cambio le harían al final de la historia.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 6.1: Estructura del Cuento), libro Múltiples Lenguajes (6° grado) y libreta.",
                "anexo_nombre": "Anexo 6.1: Organizador Gráfico de Textos Literarios y Partes del Cuento",
                "anexo_descripcion": "Ficha imprimible para esquematizar inicio, nudo, desenlace, caracterización de personajes principales/secundarios y tipo de narrador."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Alimentos procesados, grasas, sellos de advertencia (NOM-051) y múltiplos y submúltiplos del gramo",
                "pda_vinculado": "Analiza etiquetas de alimentos empaquetados e interpreta sellos de advertencia; resuelve situaciones problemáticas que implican conversiones con múltiplos y submúltiplos del gramo.",
                "inicio": "Exhibir 4 empaques reales de alimentos ultraprocesados. Preguntar: ¿Qué significan los octágonos negros en el empaque y por qué indican exceso de grasas o azúcares?",
                "desarrollo": "En binas, analizar tablas nutrimentales de empaques comerciales. Aplicar la tabla de conversión del Anexo 6.2 (método de la escalera) para convertir gramos a miligramos y kilogramos.",
                "cierre": "Construir en el pizarrón el 'Semáforo de las Grasas' (saludables vs. saturadas/trans) y reflexionar sobre la salud familiar.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 6.2: Múltiplos y Submúltiplos del Gramo y Sellos NOM-051), empaques vacíos y báscula.",
                "anexo_nombre": "Anexo 6.2: Laboratorio de Etiquetas y Conversión de Múltiplos del Gramo",
                "anexo_descripcion": "Ficha práctica de conversión de unidades de masa (kg, g, mg) con problemas de aplicación en empaques comerciales y tabla de sellos NOM-051."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Servicios públicos, recaudación de impuestos y cálculo del IVA (16%)",
                "pda_vinculado": "Comprende la función de los servicios públicos en la satisfacción de necesidades colectivas, la responsabilidad ciudadana en el pago de impuestos y el cálculo de porcentajes aplicados al IVA.",
                "inicio": "Lluvia de ideas guiada: ¿De dónde proviene el agua potable, el alumbrado y quién limpia los parques en Durango? ¿Quién financia esos servicios?",
                "desarrollo": "Explicar el concepto del Impuesto al Valor Agregado (16%) y su función social. En equipos, resolver los ejercicios del Anexo 6.3 calculando y desglosando el 16% de IVA en tickets simulados.",
                "cierre": "Debate reflexivo: '¿Por qué pagar impuestos es un acto de corresponsabilidad ética y ciudadana?'. Redacción de compromisos cívicos.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 6.3: Servicios Públicos, Impuestos y Cálculo del IVA), tickets simulados de compra.",
                "anexo_nombre": "Anexo 6.3: Ficha de Servicios Públicos y Práctica Financiera del IVA",
                "anexo_descripcion": "Actividad de vinculación comunitaria: mapa de servicios públicos y ejercicios matemáticos de cálculo y desglose del 16% de IVA."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Resolución pacífica de conflictos y convivencia escolar sana y pacífica",
                "pda_vinculado": "Aplica estrategias de mediación, negociación y diálogo reflexivo para resolver desacuerdos en el aula y promover una cultura de paz.",
                "inicio": "Dinámica kinestésica 'El nudo humano': los 26 alumnos forman un círculo tomados de las manos y deben desatarse usando exclusivamente el diálogo pacífico.",
                "desarrollo": "Analizar en parejas los casos hipotéticos de conflicto del Anexo 6.4. Identificar las 4 vías de solución pacífica: negociación, mediación, conciliación y arbitraje.",
                "cierre": "Dramatización breve de los casos con mediación dialógica. Firma colectiva del 'Pacto de Convivencia Sana y Pacífica de 6° A'.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 6.4: Casos Prácticos de Mediación y Convivencia Escolar).",
                "anexo_nombre": "Anexo 6.4: Taller de Mediación Escolar y Acuerdos de Paz",
                "anexo_descripcion": "Tarjetas de casos prácticos para dramatización y rúbrica de resolución dialógica de controversias escolares."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 6.1: Organizador Gráfico de Textos Literarios y Partes del Cuento", "campo": "Lenguajes", "descripcion": "Ficha para esquematizar inicio, nudo y desenlace, tipos de narrador y personajes.", "tema": "Textos literarios: Cuento y narración", "actividad": "Lectura guiada y clasificación de la estructura narrativa con adjetivos y nexos temporales."},
            {"dia": "Martes", "nombre": "Anexo 6.2: Laboratorio de Etiquetas y Conversión de Múltiplos del Gramo", "campo": "Saberes y Pensamiento Científico", "descripcion": "Conversión de unidades de masa (kg, g, mg) y análisis de sellos NOM-051.", "tema": "Alimentos ultraprocesados y múltiplos del gramo", "actividad": "Análisis nutrimental de empaques y conversión mediante método de la escalera."},
            {"dia": "Miércoles", "nombre": "Anexo 6.3: Ficha de Servicios Públicos y Práctica Financiera del IVA (16%)", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Cálculo y desglose del 16% de IVA en compras cotidianas y mapa de servicios comunitarios.", "tema": "Servicios públicos y recaudación de impuestos", "actividad": "Desglose de subtotal, IVA y total en compras cotidianas y reflexión cívica."},
            {"dia": "Jueves", "nombre": "Anexo 6.4: Taller de Mediación Escolar y Acuerdos de Paz", "campo": "De lo Humano y lo Comunitario", "descripcion": "Tarjetas de casos prácticos y técnicas de negociación, mediación y conciliación.", "tema": "Resolución pacífica de conflictos", "actividad": "Dramatización vivencial de controversias y aplicación de mediación dialógica."},
            {"dia": "Viernes", "nombre": "Anexo 6.5: Línea del Tiempo y Análisis Crítico del 12 de Octubre", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Línea temporal ilustrada y reflexión sobre el respeto a los pueblos originarios.", "tema": "Descubrimiento de América y Encuentro de Dos Mundos", "actividad": "Línea del tiempo de los viajes de Colón y asamblea reflexiva de diversidad cultural."}
        ],
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
        "titulo_proyecto": "Cuadernillo Profa Kempis: Plato del Bien Comer y Lectura Dramatizada",
        "periodo_sugerido": "Semana 7 de 37 (Octubre - Ciclo 2026-2027)",
        "mes_correspondiente": "Octubre",
        "año": 2026,
        "trimestre": 1,
        "descripcion": "Especialización en lectura dramatizada, Plato del Bien Comer actualizado, calidad de vida comunitaria y conmemoración del Día Mundial de la Alimentación.",
        "efemeride_principal": {
            "nombre": "Día Mundial de la Alimentación (16 de Octubre)",
            "fecha": "16 de Octubre",
            "anexo_nombre": "Anexo 7.5: Campaña 'Cero Desperdicio de Alimentos' y Decálogo Saludable",
            "anexo_descripcion": "Ficha y organizador para el diseño de carteles y compromisos sobre el derecho humano a la alimentación adecuada.",
            "actividad": "Elaborar un tríptico o cartel comunitario sobre el derecho humano a la alimentación adecuada, los riesgos del desperdicio de comida y propuestas prácticas para aprovechar sobras nutritivas en el hogar."
        },
        "campos": {
            "Lenguajes": {
                "tema": "La lectura dramatizada y el guión teatral (acotaciones, parlamentos y modulación)",
                "pda_vinculado": "Interpreta y representa lecturas dramatizadas empleando adecuadamente acotaciones, volumen, tono y modulación de la voz.",
                "inicio": "Juego de modulación de voz: leer la misma frase ('¡Ya llegaron los libros!') con distintas emociones (alegría, misterio, enojo). Analizar la importancia de las acotaciones.",
                "desarrollo": "En equipos de 4, leer el guión breve del Anexo 7.1. Identificar personajes, parlamentos y acotaciones. Distribuir roles y ensayar entonación y expresión corporal.",
                "cierre": "Representación en atril o escenario del aula frente al grupo. Coevaluación con lista de cotejo de dicción, volumen y expresividad.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 7.1: Guión Teatral y Ficha de Acotaciones), atril o espacio de aula.",
                "anexo_nombre": "Anexo 7.1: Guión Teatral Didáctico y Rúbrica de Lectura Dramatizada",
                "anexo_descripcion": "Texto dramático adaptado para educación primaria con acotaciones visuales y guía de modulación expresiva de la voz."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "El Plato del Bien Comer actualizado, la Jarra del Buen Beber y balance calórico",
                "pda_vinculado": "Diseña menús basados en el Plato del Bien Comer y la Jarra del Buen Beber, relacionando la masa en gramos de las porciones con los requerimientos energéticos saludables.",
                "inicio": "Presentar silueta del nuevo Plato del Bien Comer. Preguntar: ¿Cuáles son los 3 grupos principales y por qué las verduras y frutas deben ocupar la mitad del plato?",
                "desarrollo": "Utilizando el Anexo 7.2, recortar y clasificar alimentos en: 1) Verduras y frutas, 2) Granos y cereales, 3) Leguminosas y alimentos de origen animal. Calcular la masa aproximada en gramos de cada porción.",
                "cierre": "Exposición de menús saludables creados por los alumnos. Diseñar el compromiso personal de hidratación: 6 a 8 vasos de agua simple al día.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 7.2: Plato del Bien Comer recortable y registro de gramos), tijeras, pegamento y colores.",
                "anexo_nombre": "Anexo 7.2: Taller Interactivo del Plato del Bien Comer y Menú Semanal",
                "anexo_descripcion": "Esquema interactivo a color para recortar y armar porciones nutricionales en gramos y niveles de hidratación de la Jarra del Buen Beber."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Calidad de vida: Factores determinantes, justicia social y desigualdades en la comunidad",
                "pda_vinculado": "Analiza los factores que influyen en la calidad de vida de las familias en su comunidad y entidad (Durango), reconociendo brechas de equidad y propuestas de mejora.",
                "inicio": "¿Qué necesita una familia para vivir bien? Lluvia de respuestas: salud, casa, trabajo, seguridad, áreas verdes, agua potable.",
                "desarrollo": "Analizar la infografía del Anexo 7.3 sobre las dimensiones de calidad de vida. En equipos, responder la encuesta diagnóstica sobre fortalezas y carencias de su colonia en Durango.",
                "cierre": "Construir en cartulina el 'Mural Comunitario de la Calidad de Vida' con propuestas ciudadanas para mejorar los espacios públicos de su entorno.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 7.3: Encuesta y Dimensiones de la Calidad de Vida), plumones y cartulinas.",
                "anexo_nombre": "Anexo 7.3: Diagnóstico Comunitario de Indicadores de Calidad de Vida",
                "anexo_descripcion": "Instrumento de indagación comunitaria para evaluar acceso a servicios, salud y medio ambiente en el entorno escolar."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Estilos de vida activos, prevención de enfermedades crónicas y bienestar compartido",
                "pda_vinculado": "Organiza y participa en circuitos motrices y dinámicas de actividad física para valorar el impacto del ejercicio continuo en el bienestar integral.",
                "inicio": "Toma de pulso cardíaco en reposo. Breve calentamiento motriz en el aula para activar la oxigenación cerebral y el entusiasmo kinestésico.",
                "desarrollo": "En el patio cívico, organizar 4 estaciones del circuito saludable del Anexo 7.4: 1) Salto de cuerda, 2) Desplazamiento en zigzag, 3) Lanzamiento y recepción, 4) Equilibrio y estiramiento. Tomar pulso posterior.",
                "cierre": "Reflexión en asamblea sobre la importancia de combinar al menos 60 minutos diarios de juego activo con la alimentación balanceada.",
                "recursos": "Cuadernillo Profa Kempis (Anexo 7.4: Circuito Motriz y Bitácora de Salud), cuerdas, aros y conos.",
                "anexo_nombre": "Anexo 7.4: Bitácora del Circuito de Actividad Física y Bienestar Integral",
                "anexo_descripcion": "Registro diario de minutos de actividad física, horas de sueño y consumo de agua simple para los alumnos de 6° grado."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 7.1: Guión Teatral Didáctico y Rúbrica de Lectura Dramatizada", "campo": "Lenguajes", "descripcion": "Texto dramático adaptado con acotaciones visuales y rúbrica de entonación.", "tema": "Lectura dramatizada y teatro escolar", "actividad": "Lectura en atril de guiones teatrales con identificación de acotaciones y modulación de voz."},
            {"dia": "Martes", "nombre": "Anexo 7.2: Taller Interactivo del Plato del Bien Comer y Menú Semanal", "campo": "Saberes y Pensamiento Científico", "descripcion": "Esquema interactivo recortable con registro de gramos y Jarra del Buen Beber.", "tema": "Plato del Bien Comer y balance calórico", "actividad": "Diseño y cálculo de porciones en gramos para un almuerzo escolar balanceado."},
            {"dia": "Miércoles", "nombre": "Anexo 7.3: Diagnóstico Comunitario de Indicadores de Calidad de Vida", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Encuesta comunitaria de acceso a servicios básicos y medio ambiente en Durango.", "tema": "Dimensiones de la calidad de vida comunitaria", "actividad": "Aplicación de instrumento de indagación comunitaria y elaboración del mural de calidad de vida."},
            {"dia": "Jueves", "nombre": "Anexo 7.4: Bitácora del Circuito de Actividad Física y Bienestar Integral", "campo": "De lo Humano y lo Comunitario", "descripcion": "Registro de circuito motriz de 4 estaciones, pulsaciones cardíacas y minutos activos.", "tema": "Estilos de vida activos y circuitos motrices", "actividad": "Estaciones de salto, zigzag, lanzamiento y equilibrio en el patio cívico con toma de pulso."},
            {"dia": "Viernes", "nombre": "Anexo 7.5: Campaña 'Cero Desperdicio de Alimentos' y Decálogo Saludable", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha y organizador para carteles sobre el derecho humano a la alimentación adecuada.", "tema": "Día Mundial de la Alimentación (16 de Octubre)", "actividad": "Elaboración de carteles y compromisos comunitarios para evitar el desperdicio de alimentos."}
        ],
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

CATALOGO_PROYECTOS_SEP_37_SEMANAS: Dict[int, Dict[str, Any]] = {
    6: CUADERNILLO_KEMPIS_DATA[6],
    7: CUADERNILLO_KEMPIS_DATA[7],
    1: {
        "semana": 1,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 1 (Nos reconocemos y construimos nuestra comunidad de aula)",
        "titulo_proyecto": "Nos reconocemos y construimos nuestra comunidad de aula",
        "periodo_sugerido": "Semana 1 de 37 (Septiembre 2026 - Ciclo 2026-2027)",
        "mes_correspondiente": "Septiembre",
        "año": 2026,
        "trimestre": 1,
        "descripcion": "Diagnóstico integral de lectura, cálculo y estilos de aprendizaje kinestésico/visual con acuerdos de aula.",
        "efemeride_principal": {
            "nombre": "Inicio del Ciclo Escolar 2026-2027",
            "fecha": "31 de Agosto",
            "anexo_nombre": "Anexo 1.5: Decálogo y Firma Colectiva del Pacto de Aula 6° 'A'",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Inicio del Ciclo Escolar 2026-2027.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Evaluación Diagnóstica de Lectura y Comprensión Inferencial",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 1.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 1.1 y libreta.",
                "anexo_nombre": "Anexo 1.1: Evaluación Diagnóstica de Lectura y Comprensión Inferencial",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Evaluación Diagnóstica de Lectura y Comprensión Inferencial."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Reto de Operaciones y Cálculo Mental Diagnóstico",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 1.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 1.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 1.2: Reto de Operaciones y Cálculo Mental Diagnóstico",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Reto de Operaciones y Cálculo Mental Diagnóstico."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Identificación de Estilos de Aprendizaje Kinestésico y Visual",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 1.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 1.4.",
                "anexo_nombre": "Anexo 1.4: Identificación de Estilos de Aprendizaje Kinestésico y Visual",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Identificación de Estilos de Aprendizaje Kinestésico y Visual."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Cartografía Emocional y Dinámicas de Integración Grupal",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 1.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 1.3 y patio cívico.",
                "anexo_nombre": "Anexo 1.3: Cartografía Emocional y Dinámicas de Integración Grupal",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 1.1: Evaluación Diagnóstica de Lectura y Comprensión Inferencial", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Evaluación Diagnóstica de Lectura y Comprensión Inferencial.", "tema": "Evaluación Diagnóstica de Lectura y Comprensión Inferencial", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 1.2: Reto de Operaciones y Cálculo Mental Diagnóstico", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Reto de Operaciones y Cálculo Mental Diagnóstico.", "tema": "Reto de Operaciones y Cálculo Mental Diagnóstico", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 1.3: Cartografía Emocional y Dinámicas de Integración Grupal", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Cartografía Emocional y Dinámicas de Integración Grupal.", "tema": "Cartografía Emocional y Dinámicas de Integración Grupal", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 1.4: Identificación de Estilos de Aprendizaje Kinestésico y Visual", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Identificación de Estilos de Aprendizaje Kinestésico y Visual.", "tema": "Identificación de Estilos de Aprendizaje Kinestésico y Visual", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 1.5: Decálogo y Firma Colectiva del Pacto de Aula 6° 'A'", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Decálogo y Firma Colectiva del Pacto de Aula 6° 'A'.", "tema": "Decálogo y Firma Colectiva del Pacto de Aula 6° 'A'", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. nos (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    2: {
        "semana": 2,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 2 (Mi historia en mi comunidad: Crónicas y Autobiografías)",
        "titulo_proyecto": "Mi historia en mi comunidad: Crónicas y Autobiografías",
        "periodo_sugerido": "Semana 2 de 37 (Septiembre 2026 - Ciclo 2026-2027)",
        "mes_correspondiente": "Septiembre",
        "año": 2026,
        "trimestre": 1,
        "descripcion": "Redacción de textos autobiográficos, nexos temporales y cronología familiar en Durango.",
        "efemeride_principal": {
            "nombre": "Día Internacional de la Alfabetización",
            "fecha": "8 de Septiembre",
            "anexo_nombre": "Anexo 2.5: Edición y Rúbrica de la Antología Autobiográfica",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día Internacional de la Alfabetización.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Organizador Gráfico de la Línea de Vida",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 2.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 2.1 y libreta.",
                "anexo_nombre": "Anexo 2.1: Organizador Gráfico de la Línea de Vida",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Organizador Gráfico de la Línea de Vida."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Taller de Conectores Temporales y Causales",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 2.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 2.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 2.2: Taller de Conectores Temporales y Causales",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Taller de Conectores Temporales y Causales."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Entrevista a Personas Adultas Mayores de Durango",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 2.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 2.4.",
                "anexo_nombre": "Anexo 2.4: Entrevista a Personas Adultas Mayores de Durango",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Entrevista a Personas Adultas Mayores de Durango."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Lapsos Temporales: Lustros, Décadas y Siglos",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 2.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 2.3 y patio cívico.",
                "anexo_nombre": "Anexo 2.3: Lapsos Temporales: Lustros, Décadas y Siglos",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 2.1: Organizador Gráfico de la Línea de Vida", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Organizador Gráfico de la Línea de Vida.", "tema": "Organizador Gráfico de la Línea de Vida", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 2.2: Taller de Conectores Temporales y Causales", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Taller de Conectores Temporales y Causales.", "tema": "Taller de Conectores Temporales y Causales", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 2.3: Lapsos Temporales: Lustros, Décadas y Siglos", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Lapsos Temporales: Lustros, Décadas y Siglos.", "tema": "Lapsos Temporales: Lustros, Décadas y Siglos", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 2.4: Entrevista a Personas Adultas Mayores de Durango", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Entrevista a Personas Adultas Mayores de Durango.", "tema": "Entrevista a Personas Adultas Mayores de Durango", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 2.5: Edición y Rúbrica de la Antología Autobiográfica", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Edición y Rúbrica de la Antología Autobiográfica.", "tema": "Edición y Rúbrica de la Antología Autobiográfica", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. mi (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    3: {
        "semana": 3,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 3 (Gesta heroica y libertad comunitaria: Independencia de México)",
        "titulo_proyecto": "Gesta heroica y libertad comunitaria: Independencia de México",
        "periodo_sugerido": "Semana 3 de 37 (Septiembre 2026 - Ciclo 2026-2027)",
        "mes_correspondiente": "Septiembre",
        "año": 2026,
        "trimestre": 1,
        "descripcion": "Análisis crítico de las causas de la Independencia de 1810, Sentimientos de la Nación y soberanía.",
        "efemeride_principal": {
            "nombre": "Conmemoración del Grito de Independencia",
            "fecha": "16 de Septiembre",
            "anexo_nombre": "Anexo 3.5: Periódico Mural Cívico y Crónica Insurgente",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Conmemoración del Grito de Independencia.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Causas Sociales y Económicas de la Independencia",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 3.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 3.1 y libreta.",
                "anexo_nombre": "Anexo 3.1: Causas Sociales y Económicas de la Independencia",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Causas Sociales y Económicas de la Independencia."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Lectura Reflexiva de los Sentimientos de la Nación",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 3.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 3.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 3.2: Lectura Reflexiva de los Sentimientos de la Nación",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Lectura Reflexiva de los Sentimientos de la Nación."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Heroínas Insurgentes: Josefa Ortiz y Leona Vicario",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 3.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 3.4.",
                "anexo_nombre": "Anexo 3.4: Heroínas Insurgentes: Josefa Ortiz y Leona Vicario",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Heroínas Insurgentes: Josefa Ortiz y Leona Vicario."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Distancias a Escala en las Campañas Militares",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 3.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 3.3 y patio cívico.",
                "anexo_nombre": "Anexo 3.3: Distancias a Escala en las Campañas Militares",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 3.1: Causas Sociales y Económicas de la Independencia", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Causas Sociales y Económicas de la Independencia.", "tema": "Causas Sociales y Económicas de la Independencia", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 3.2: Lectura Reflexiva de los Sentimientos de la Nación", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Lectura Reflexiva de los Sentimientos de la Nación.", "tema": "Lectura Reflexiva de los Sentimientos de la Nación", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 3.3: Distancias a Escala en las Campañas Militares", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Distancias a Escala en las Campañas Militares.", "tema": "Distancias a Escala en las Campañas Militares", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 3.4: Heroínas Insurgentes: Josefa Ortiz y Leona Vicario", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Heroínas Insurgentes: Josefa Ortiz y Leona Vicario.", "tema": "Heroínas Insurgentes: Josefa Ortiz y Leona Vicario", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 3.5: Periódico Mural Cívico y Crónica Insurgente", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Periódico Mural Cívico y Crónica Insurgente.", "tema": "Periódico Mural Cívico y Crónica Insurgente", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. gesta (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    4: {
        "semana": 4,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 4 (Guardianes de la salud escolar: Sistema inmunológico y prevención)",
        "titulo_proyecto": "Guardianes de la salud escolar: Sistema inmunológico y prevención",
        "periodo_sugerido": "Semana 4 de 37 (Septiembre 2026 - Ciclo 2026-2027)",
        "mes_correspondiente": "Septiembre",
        "año": 2026,
        "trimestre": 1,
        "descripcion": "Textos de divulgación científica, vacunas, gráficas estadísticas y 1ª Sesión Ordinaria de CTE.",
        "efemeride_principal": {
            "nombre": "1ª Sesión Ordinaria de Consejo Técnico Escolar (CTE)",
            "fecha": "25 de Septiembre",
            "anexo_nombre": "Anexo 4.5: Autoevaluación Formativa y Balance 1er Mes CTE",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a 1ª Sesión Ordinaria de Consejo Técnico Escolar (CTE).",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Infografía de Glóbulos Blancos y Barreras de Inmunidad",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 4.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 4.1 y libreta.",
                "anexo_nombre": "Anexo 4.1: Infografía de Glóbulos Blancos y Barreras de Inmunidad",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Infografía de Glóbulos Blancos y Barreras de Inmunidad."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Ficha Científica: Historia y Función de las Vacunas",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 4.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 4.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 4.2: Ficha Científica: Historia y Función de las Vacunas",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Ficha Científica: Historia y Función de las Vacunas."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Decálogo de Higiene y Prevención en la Escuela",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 4.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 4.4.",
                "anexo_nombre": "Anexo 4.4: Decálogo de Higiene y Prevención en la Escuela",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Decálogo de Higiene y Prevención en la Escuela."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Gráficas Porcentuales de Cobertura de Vacunación",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 4.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 4.3 y patio cívico.",
                "anexo_nombre": "Anexo 4.3: Gráficas Porcentuales de Cobertura de Vacunación",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 4.1: Infografía de Glóbulos Blancos y Barreras de Inmunidad", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Infografía de Glóbulos Blancos y Barreras de Inmunidad.", "tema": "Infografía de Glóbulos Blancos y Barreras de Inmunidad", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 4.2: Ficha Científica: Historia y Función de las Vacunas", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Ficha Científica: Historia y Función de las Vacunas.", "tema": "Ficha Científica: Historia y Función de las Vacunas", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 4.3: Gráficas Porcentuales de Cobertura de Vacunación", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Gráficas Porcentuales de Cobertura de Vacunación.", "tema": "Gráficas Porcentuales de Cobertura de Vacunación", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 4.4: Decálogo de Higiene y Prevención en la Escuela", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Decálogo de Higiene y Prevención en la Escuela.", "tema": "Decálogo de Higiene y Prevención en la Escuela", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 4.5: Autoevaluación Formativa y Balance 1er Mes CTE", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Autoevaluación Formativa y Balance 1er Mes CTE.", "tema": "Autoevaluación Formativa y Balance 1er Mes CTE", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. guardianes (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    5: {
        "semana": 5,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 5 (El tesoro natural de nuestra entidad: Ecosistemas de Durango)",
        "titulo_proyecto": "El tesoro natural de nuestra entidad: Ecosistemas de Durango",
        "periodo_sugerido": "Semana 5 de 37 (Octubre 2026 - Ciclo 2026-2027)",
        "mes_correspondiente": "Octubre",
        "año": 2026,
        "trimestre": 1,
        "descripcion": "Biodiversidad de la Sierra Madre Occidental, redes tróficas y conservación sustentable.",
        "efemeride_principal": {
            "nombre": "Día Mundial del Hábitat",
            "fecha": "5 de Octubre",
            "anexo_nombre": "Anexo 5.5: Catálogo Ilustrado de Especies Endémicas de Durango",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día Mundial del Hábitat.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Mapa Biogeográfico de Zonas Naturales de Durango",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 5.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 5.1 y libreta.",
                "anexo_nombre": "Anexo 5.1: Mapa Biogeográfico de Zonas Naturales de Durango",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Mapa Biogeográfico de Zonas Naturales de Durango."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Cadenas y Redes Tróficas del Bosque Templado",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 5.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 5.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 5.2: Cadenas y Redes Tróficas del Bosque Templado",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Cadenas y Redes Tróficas del Bosque Templado."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Causas de Pérdida de Biodiversidad en la Entidad",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 5.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 5.4.",
                "anexo_nombre": "Anexo 5.4: Causas de Pérdida de Biodiversidad en la Entidad",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Causas de Pérdida de Biodiversidad en la Entidad."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Cálculo de Áreas y Densidad Poblacional en Reservas",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 5.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 5.3 y patio cívico.",
                "anexo_nombre": "Anexo 5.3: Cálculo de Áreas y Densidad Poblacional en Reservas",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 5.1: Mapa Biogeográfico de Zonas Naturales de Durango", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Mapa Biogeográfico de Zonas Naturales de Durango.", "tema": "Mapa Biogeográfico de Zonas Naturales de Durango", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 5.2: Cadenas y Redes Tróficas del Bosque Templado", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Cadenas y Redes Tróficas del Bosque Templado.", "tema": "Cadenas y Redes Tróficas del Bosque Templado", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 5.3: Cálculo de Áreas y Densidad Poblacional en Reservas", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Cálculo de Áreas y Densidad Poblacional en Reservas.", "tema": "Cálculo de Áreas y Densidad Poblacional en Reservas", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 5.4: Causas de Pérdida de Biodiversidad en la Entidad", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Causas de Pérdida de Biodiversidad en la Entidad.", "tema": "Causas de Pérdida de Biodiversidad en la Entidad", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 5.5: Catálogo Ilustrado de Especies Endémicas de Durango", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Catálogo Ilustrado de Especies Endémicas de Durango.", "tema": "Catálogo Ilustrado de Especies Endémicas de Durango", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. el (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    8: {
        "semana": 8,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 8 (Debatiendo por el futuro de Durango: Argumentos y Proporcionalidad)",
        "titulo_proyecto": "Debatiendo por el futuro de Durango: Argumentos y Proporcionalidad",
        "periodo_sugerido": "Semana 8 de 37 (Octubre 2026 - Ciclo 2026-2027)",
        "mes_correspondiente": "Octubre",
        "año": 2026,
        "trimestre": 1,
        "descripcion": "Estructura del texto argumentativo, mesas de debate escolar, proporcionalidad directa y energías limpias.",
        "efemeride_principal": {
            "nombre": "Día de las Naciones Unidas (ONU)",
            "fecha": "24 de Octubre",
            "anexo_nombre": "Anexo 8.5: Rúbrica Analítica de Desempeño en Debate Público",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día de las Naciones Unidas (ONU).",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Esquema de Tesis, Argumentos y Contraargumentos",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 8.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 8.1 y libreta.",
                "anexo_nombre": "Anexo 8.1: Esquema de Tesis, Argumentos y Contraargumentos",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Esquema de Tesis, Argumentos y Contraargumentos."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Tablas de Proporcionalidad Directa y Constante k",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 8.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 8.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 8.2: Tablas de Proporcionalidad Directa y Constante k",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Tablas de Proporcionalidad Directa y Constante k."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Roles de Participación y Guion de Debate Escolar",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 8.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 8.4.",
                "anexo_nombre": "Anexo 8.4: Roles de Participación y Guion de Debate Escolar",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Roles de Participación y Guion de Debate Escolar."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Energías Renovables en el Norte de México",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 8.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 8.3 y patio cívico.",
                "anexo_nombre": "Anexo 8.3: Energías Renovables en el Norte de México",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 8.1: Esquema de Tesis, Argumentos y Contraargumentos", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Esquema de Tesis, Argumentos y Contraargumentos.", "tema": "Esquema de Tesis, Argumentos y Contraargumentos", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 8.2: Tablas de Proporcionalidad Directa y Constante k", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Tablas de Proporcionalidad Directa y Constante k.", "tema": "Tablas de Proporcionalidad Directa y Constante k", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 8.3: Energías Renovables en el Norte de México", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Energías Renovables en el Norte de México.", "tema": "Energías Renovables en el Norte de México", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 8.4: Roles de Participación y Guion de Debate Escolar", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Roles de Participación y Guion de Debate Escolar.", "tema": "Roles de Participación y Guion de Debate Escolar", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 8.5: Rúbrica Analítica de Desempeño en Debate Público", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Rúbrica Analítica de Desempeño en Debate Público.", "tema": "Rúbrica Analítica de Desempeño en Debate Público", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. debatiendo (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    9: {
        "semana": 9,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 9 (Nuestras raíces vivas: Día de Muertos y Poesía Popular)",
        "titulo_proyecto": "Nuestras raíces vivas: Día de Muertos y Poesía Popular",
        "periodo_sugerido": "Semana 9 de 37 (Octubre 2026 - Ciclo 2026-2027)",
        "mes_correspondiente": "Octubre",
        "año": 2026,
        "trimestre": 1,
        "descripcion": "Calaveritas literarias, métrica, rima, significado del altar tradicional y 2ª Sesión CTE.",
        "efemeride_principal": {
            "nombre": "2ª Sesión Ordinaria de Consejo Técnico Escolar (CTE)",
            "fecha": "30 de Octubre",
            "anexo_nombre": "Anexo 9.5: Muestra de Calaveritas y Evaluación Formativa CTE",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a 2ª Sesión Ordinaria de Consejo Técnico Escolar (CTE).",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Taller de Métrica y Rima en Calaveritas Literarias",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 9.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 9.1 y libreta.",
                "anexo_nombre": "Anexo 9.1: Taller de Métrica y Rima en Calaveritas Literarias",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Taller de Métrica y Rima en Calaveritas Literarias."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Elementos Simbólicos del Altar Tradicional Mexicano",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 9.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 9.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 9.2: Elementos Simbólicos del Altar Tradicional Mexicano",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Elementos Simbólicos del Altar Tradicional Mexicano."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Patrimonio Cultural Inmaterial y Memoria Comunitaria",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 9.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 9.4.",
                "anexo_nombre": "Anexo 9.4: Patrimonio Cultural Inmaterial y Memoria Comunitaria",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Patrimonio Cultural Inmaterial y Memoria Comunitaria."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Presupuesto y Proporcionalidad de Materiales del Altar",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 9.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 9.3 y patio cívico.",
                "anexo_nombre": "Anexo 9.3: Presupuesto y Proporcionalidad de Materiales del Altar",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 9.1: Taller de Métrica y Rima en Calaveritas Literarias", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Taller de Métrica y Rima en Calaveritas Literarias.", "tema": "Taller de Métrica y Rima en Calaveritas Literarias", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 9.2: Elementos Simbólicos del Altar Tradicional Mexicano", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Elementos Simbólicos del Altar Tradicional Mexicano.", "tema": "Elementos Simbólicos del Altar Tradicional Mexicano", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 9.3: Presupuesto y Proporcionalidad de Materiales del Altar", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Presupuesto y Proporcionalidad de Materiales del Altar.", "tema": "Presupuesto y Proporcionalidad de Materiales del Altar", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 9.4: Patrimonio Cultural Inmaterial y Memoria Comunitaria", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Patrimonio Cultural Inmaterial y Memoria Comunitaria.", "tema": "Patrimonio Cultural Inmaterial y Memoria Comunitaria", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 9.5: Muestra de Calaveritas y Evaluación Formativa CTE", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Muestra de Calaveritas y Evaluación Formativa CTE.", "tema": "Muestra de Calaveritas y Evaluación Formativa CTE", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. nuestras (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    10: {
        "semana": 10,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 10 (Cartografía de mi comunidad: Coordenadas, Escalas y Prevención)",
        "titulo_proyecto": "Cartografía de mi comunidad: Coordenadas, Escalas y Prevención",
        "periodo_sugerido": "Semana 10 de 37 (Noviembre 2026 - Ciclo 2026-2027)",
        "mes_correspondiente": "Noviembre",
        "año": 2026,
        "trimestre": 1,
        "descripcion": "Planos a escala, coordenadas cartesianas, rutas de evacuación y mapa de riesgos del barrio.",
        "efemeride_principal": {
            "nombre": "Día Nacional del Libro",
            "fecha": "12 de Noviembre",
            "anexo_nombre": "Anexo 10.5: Mapa Comunitario Interactivo de la Primaria Revolución",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día Nacional del Libro.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Lectura e Interpretación de Planos a Escala",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 10.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 10.1 y libreta.",
                "anexo_nombre": "Anexo 10.1: Lectura e Interpretación de Planos a Escala",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Lectura e Interpretación de Planos a Escala."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Ubicación de Puntos en el Plano Cartesiano",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 10.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 10.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 10.2: Ubicación de Puntos en el Plano Cartesiano",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Ubicación de Puntos en el Plano Cartesiano."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Diseño de Señalética y Rutas de Evacuación Segura",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 10.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 10.4.",
                "anexo_nombre": "Anexo 10.4: Diseño de Señalética y Rutas de Evacuación Segura",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Diseño de Señalética y Rutas de Evacuación Segura."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Identificación de Zonas de Riesgo en el Entorno Escolar",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 10.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 10.3 y patio cívico.",
                "anexo_nombre": "Anexo 10.3: Identificación de Zonas de Riesgo en el Entorno Escolar",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 10.1: Lectura e Interpretación de Planos a Escala", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Lectura e Interpretación de Planos a Escala.", "tema": "Lectura e Interpretación de Planos a Escala", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 10.2: Ubicación de Puntos en el Plano Cartesiano", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Ubicación de Puntos en el Plano Cartesiano.", "tema": "Ubicación de Puntos en el Plano Cartesiano", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 10.3: Identificación de Zonas de Riesgo en el Entorno Escolar", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Identificación de Zonas de Riesgo en el Entorno Escolar.", "tema": "Identificación de Zonas de Riesgo en el Entorno Escolar", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 10.4: Diseño de Señalética y Rutas de Evacuación Segura", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Diseño de Señalética y Rutas de Evacuación Segura.", "tema": "Diseño de Señalética y Rutas de Evacuación Segura", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 10.5: Mapa Comunitario Interactivo de la Primaria Revolución", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Mapa Comunitario Interactivo de la Primaria Revolución.", "tema": "Mapa Comunitario Interactivo de la Primaria Revolución", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. cartografía (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    11: {
        "semana": 11,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 11 (Viajeros del cosmos: El sistema solar y divulgación científica)",
        "titulo_proyecto": "Viajeros del cosmos: El sistema solar y divulgación científica",
        "periodo_sugerido": "Semana 11 de 37 (Noviembre 2026 - Ciclo 2026-2027)",
        "mes_correspondiente": "Noviembre",
        "año": 2026,
        "trimestre": 1,
        "descripcion": "Textos de divulgación científica, astronomía, gravedad y magnitudes exponenciales.",
        "efemeride_principal": {
            "nombre": "Día Mundial de la Ciencia para la Paz",
            "fecha": "10 de Noviembre",
            "anexo_nombre": "Anexo 11.5: Galería Interactiva del Universo y Exposición Guiada",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día Mundial de la Ciencia para la Paz.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Estructura y Cuerpos Celestes del Sistema Solar",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 11.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 11.1 y libreta.",
                "anexo_nombre": "Anexo 11.1: Estructura y Cuerpos Celestes del Sistema Solar",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Estructura y Cuerpos Celestes del Sistema Solar."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Notación Científica y Distancias Planetarias",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 11.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 11.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 11.2: Notación Científica y Distancias Planetarias",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Notación Científica y Distancias Planetarias."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Redacción de un Artículo de Divulgación Escolar",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 11.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 11.4.",
                "anexo_nombre": "Anexo 11.4: Redacción de un Artículo de Divulgación Escolar",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Redacción de un Artículo de Divulgación Escolar."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "La Fuerza de Gravedad y Órbitas Elípticas",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 11.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 11.3 y patio cívico.",
                "anexo_nombre": "Anexo 11.3: La Fuerza de Gravedad y Órbitas Elípticas",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 11.1: Estructura y Cuerpos Celestes del Sistema Solar", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Estructura y Cuerpos Celestes del Sistema Solar.", "tema": "Estructura y Cuerpos Celestes del Sistema Solar", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 11.2: Notación Científica y Distancias Planetarias", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Notación Científica y Distancias Planetarias.", "tema": "Notación Científica y Distancias Planetarias", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 11.3: La Fuerza de Gravedad y Órbitas Elípticas", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para La Fuerza de Gravedad y Órbitas Elípticas.", "tema": "La Fuerza de Gravedad y Órbitas Elípticas", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 11.4: Redacción de un Artículo de Divulgación Escolar", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Redacción de un Artículo de Divulgación Escolar.", "tema": "Redacción de un Artículo de Divulgación Escolar", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 11.5: Galería Interactiva del Universo y Exposición Guiada", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Galería Interactiva del Universo y Exposición Guiada.", "tema": "Galería Interactiva del Universo y Exposición Guiada", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. viajeros (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    12: {
        "semana": 12,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 12 (1910: Voces revolucionarias y justicia social en Durango)",
        "titulo_proyecto": "1910: Voces revolucionarias y justicia social en Durango",
        "periodo_sugerido": "Semana 12 de 37 (Noviembre 2026 - Ciclo 2026-2027)",
        "mes_correspondiente": "Noviembre",
        "año": 2026,
        "trimestre": 1,
        "descripcion": "Movimiento revolucionario de 1910, ideales agrarios, Francisco Villa y memoria de la escuela.",
        "efemeride_principal": {
            "nombre": "Conmemoración del Inicio de la Revolución Mexicana (1910)",
            "fecha": "20 de Noviembre",
            "anexo_nombre": "Anexo 12.5: Periódico Histórico Ilustrado y Dramatización Revolucionaria",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Conmemoración del Inicio de la Revolución Mexicana (1910).",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Causas Económicas y Sociales del Estallido de 1910",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 12.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 12.1 y libreta.",
                "anexo_nombre": "Anexo 12.1: Causas Económicas y Sociales del Estallido de 1910",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Causas Económicas y Sociales del Estallido de 1910."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Líderes Revolucionarios y el Agrarismo en Durango",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 12.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 12.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 12.2: Líderes Revolucionarios y el Agrarismo en Durango",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Líderes Revolucionarios y el Agrarismo en Durango."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Historia de la Escuela Primaria 'Revolución Social de 1910'",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 12.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 12.4.",
                "anexo_nombre": "Anexo 12.4: Historia de la Escuela Primaria 'Revolución Social de 1910'",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Historia de la Escuela Primaria 'Revolución Social de 1910'."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Análisis Literario y Métrica de Corridos Revolucionarios",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 12.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 12.3 y patio cívico.",
                "anexo_nombre": "Anexo 12.3: Análisis Literario y Métrica de Corridos Revolucionarios",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 12.1: Causas Económicas y Sociales del Estallido de 1910", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Causas Económicas y Sociales del Estallido de 1910.", "tema": "Causas Económicas y Sociales del Estallido de 1910", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 12.2: Líderes Revolucionarios y el Agrarismo en Durango", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Líderes Revolucionarios y el Agrarismo en Durango.", "tema": "Líderes Revolucionarios y el Agrarismo en Durango", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 12.3: Análisis Literario y Métrica de Corridos Revolucionarios", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Análisis Literario y Métrica de Corridos Revolucionarios.", "tema": "Análisis Literario y Métrica de Corridos Revolucionarios", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 12.4: Historia de la Escuela Primaria 'Revolución Social de 1910'", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Historia de la Escuela Primaria 'Revolución Social de 1910'.", "tema": "Historia de la Escuela Primaria 'Revolución Social de 1910'", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 12.5: Periódico Histórico Ilustrado y Dramatización Revolucionaria", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Periódico Histórico Ilustrado y Dramatización Revolucionaria.", "tema": "Periódico Histórico Ilustrado y Dramatización Revolucionaria", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. 1910: (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    13: {
        "semana": 13,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 13 (Feria de saberes: Cierre y consolidación del Primer Trimestre)",
        "titulo_proyecto": "Feria de saberes: Cierre y consolidación del Primer Trimestre",
        "periodo_sugerido": "Semana 13 de 37 (Noviembre 2026 - Ciclo 2026-2027)",
        "mes_correspondiente": "Noviembre",
        "año": 2026,
        "trimestre": 1,
        "descripcion": "Portafolio de evidencias formativas, retos matemáticos de integración y 3ª Sesión CTE.",
        "efemeride_principal": {
            "nombre": "3ª Sesión Ordinaria de Consejo Técnico Escolar (CTE)",
            "fecha": "27 de Noviembre",
            "anexo_nombre": "Anexo 13.5: Muestra Pedagógica Comunitaria y Cierre de Trimestre 1",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a 3ª Sesión Ordinaria de Consejo Técnico Escolar (CTE).",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Curaduría y Autoselección del Portafolio de Lenguajes",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 13.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 13.1 y libreta.",
                "anexo_nombre": "Anexo 13.1: Curaduría y Autoselección del Portafolio de Lenguajes",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Curaduría y Autoselección del Portafolio de Lenguajes."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Rally Matemático de Desafíos Integradores Trimestre 1",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 13.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 13.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 13.2: Rally Matemático de Desafíos Integradores Trimestre 1",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Rally Matemático de Desafíos Integradores Trimestre 1."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Coevaluación en Asamblea con Rúbricas Analíticas DUA",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 13.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 13.4.",
                "anexo_nombre": "Anexo 13.4: Coevaluación en Asamblea con Rúbricas Analíticas DUA",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Coevaluación en Asamblea con Rúbricas Analíticas DUA."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Rendición de Cuentas y Logros en Proyectos de Aula",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 13.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 13.3 y patio cívico.",
                "anexo_nombre": "Anexo 13.3: Rendición de Cuentas y Logros en Proyectos de Aula",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 13.1: Curaduría y Autoselección del Portafolio de Lenguajes", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Curaduría y Autoselección del Portafolio de Lenguajes.", "tema": "Curaduría y Autoselección del Portafolio de Lenguajes", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 13.2: Rally Matemático de Desafíos Integradores Trimestre 1", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Rally Matemático de Desafíos Integradores Trimestre 1.", "tema": "Rally Matemático de Desafíos Integradores Trimestre 1", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 13.3: Rendición de Cuentas y Logros en Proyectos de Aula", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Rendición de Cuentas y Logros en Proyectos de Aula.", "tema": "Rendición de Cuentas y Logros en Proyectos de Aula", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 13.4: Coevaluación en Asamblea con Rúbricas Analíticas DUA", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Coevaluación en Asamblea con Rúbricas Analíticas DUA.", "tema": "Coevaluación en Asamblea con Rúbricas Analíticas DUA", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 13.5: Muestra Pedagógica Comunitaria y Cierre de Trimestre 1", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Muestra Pedagógica Comunitaria y Cierre de Trimestre 1.", "tema": "Muestra Pedagógica Comunitaria y Cierre de Trimestre 1", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. feria (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    14: {
        "semana": 14,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 14 (Laboratorio cotidiano: Mezclas, soluciones y textos expositivos)",
        "titulo_proyecto": "Laboratorio cotidiano: Mezclas, soluciones y textos expositivos",
        "periodo_sugerido": "Semana 14 de 37 (Diciembre 2026 - Ciclo 2026-2027)",
        "mes_correspondiente": "Diciembre",
        "año": 2026,
        "trimestre": 2,
        "descripcion": "Métodos de separación de mezclas, concentración en porcentajes y redacción expositiva formal.",
        "efemeride_principal": {
            "nombre": "Día Internacional de las Personas con Discapacidad",
            "fecha": "3 de Diciembre",
            "anexo_nombre": "Anexo 14.5: Reporte Científico Formal de Práctica de Laboratorio",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día Internacional de las Personas con Discapacidad.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Estructura del Texto Expositivo: Causa-Efecto",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 14.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 14.1 y libreta.",
                "anexo_nombre": "Anexo 14.1: Estructura del Texto Expositivo: Causa-Efecto",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Estructura del Texto Expositivo: Causa-Efecto."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Separación de Mezclas: Filtración, Decantación e Imantación",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 14.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 14.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 14.2: Separación de Mezclas: Filtración, Decantación e Imantación",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Separación de Mezclas: Filtración, Decantación e Imantación."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Experimento Vivencial: Filtro Casero de Purificación",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 14.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 14.4.",
                "anexo_nombre": "Anexo 14.4: Experimento Vivencial: Filtro Casero de Purificación",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Experimento Vivencial: Filtro Casero de Purificación."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Cálculo de Porcentajes de Concentración Soluto/Solvente",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 14.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 14.3 y patio cívico.",
                "anexo_nombre": "Anexo 14.3: Cálculo de Porcentajes de Concentración Soluto/Solvente",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 14.1: Estructura del Texto Expositivo: Causa-Efecto", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Estructura del Texto Expositivo: Causa-Efecto.", "tema": "Estructura del Texto Expositivo: Causa-Efecto", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 14.2: Separación de Mezclas: Filtración, Decantación e Imantación", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Separación de Mezclas: Filtración, Decantación e Imantación.", "tema": "Separación de Mezclas: Filtración, Decantación e Imantación", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 14.3: Cálculo de Porcentajes de Concentración Soluto/Solvente", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Cálculo de Porcentajes de Concentración Soluto/Solvente.", "tema": "Cálculo de Porcentajes de Concentración Soluto/Solvente", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 14.4: Experimento Vivencial: Filtro Casero de Purificación", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Experimento Vivencial: Filtro Casero de Purificación.", "tema": "Experimento Vivencial: Filtro Casero de Purificación", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 14.5: Reporte Científico Formal de Práctica de Laboratorio", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Reporte Científico Formal de Práctica de Laboratorio.", "tema": "Reporte Científico Formal de Práctica de Laboratorio", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. laboratorio (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    15: {
        "semana": 15,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 15 (Todos somos iguales: Inclusión (DUA), derechos y equidad)",
        "titulo_proyecto": "Todos somos iguales: Inclusión (DUA), derechos y equidad",
        "periodo_sugerido": "Semana 15 de 37 (Diciembre 2026 - Ciclo 2026-2027)",
        "mes_correspondiente": "Diciembre",
        "año": 2026,
        "trimestre": 2,
        "descripcion": "Derechos humanos universales, barreras para el aprendizaje (BAP), no discriminación e igualdad de género.",
        "efemeride_principal": {
            "nombre": "Día de los Derechos Humanos",
            "fecha": "10 de Diciembre",
            "anexo_nombre": "Anexo 15.5: Decálogo de Inclusión y Empatía de 6° 'A'",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día de los Derechos Humanos.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Los 30 Artículos de la Declaración Universal de DDHH",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 15.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 15.1 y libreta.",
                "anexo_nombre": "Anexo 15.1: Los 30 Artículos de la Declaración Universal de DDHH",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Los 30 Artículos de la Declaración Universal de DDHH."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Identificación y Derribo de BAP en el Espacio Escolar",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 15.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 15.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 15.2: Identificación y Derribo de BAP en el Espacio Escolar",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Identificación y Derribo de BAP en el Espacio Escolar."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Estudio de Casos Éticos de Mediación y Respeto",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 15.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 15.4.",
                "anexo_nombre": "Anexo 15.4: Estudio de Casos Éticos de Mediación y Respeto",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Estudio de Casos Éticos de Mediación y Respeto."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Estadísticas de Equidad de Género y Oportunidades",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 15.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 15.3 y patio cívico.",
                "anexo_nombre": "Anexo 15.3: Estadísticas de Equidad de Género y Oportunidades",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 15.1: Los 30 Artículos de la Declaración Universal de DDHH", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Los 30 Artículos de la Declaración Universal de DDHH.", "tema": "Los 30 Artículos de la Declaración Universal de DDHH", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 15.2: Identificación y Derribo de BAP en el Espacio Escolar", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Identificación y Derribo de BAP en el Espacio Escolar.", "tema": "Identificación y Derribo de BAP en el Espacio Escolar", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 15.3: Estadísticas de Equidad de Género y Oportunidades", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Estadísticas de Equidad de Género y Oportunidades.", "tema": "Estadísticas de Equidad de Género y Oportunidades", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 15.4: Estudio de Casos Éticos de Mediación y Respeto", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Estudio de Casos Éticos de Mediación y Respeto.", "tema": "Estudio de Casos Éticos de Mediación y Respeto", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 15.5: Decálogo de Inclusión y Empatía de 6° 'A'", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Decálogo de Inclusión y Empatía de 6° 'A'.", "tema": "Decálogo de Inclusión y Empatía de 6° 'A'", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. todos (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    16: {
        "semana": 16,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 16 (Compartir en comunidad: Tradiciones decembrinas y consumo responsable)",
        "titulo_proyecto": "Compartir en comunidad: Tradiciones decembrinas y consumo responsable",
        "periodo_sugerido": "Semana 16 de 37 (Diciembre 2026 - Ciclo 2026-2027)",
        "mes_correspondiente": "Diciembre",
        "año": 2026,
        "trimestre": 2,
        "descripcion": "Cartas de agradecimiento, presupuesto navideño familiar, consumo sustentable y receso de invierno.",
        "efemeride_principal": {
            "nombre": "Inicio del Receso Vacacional de Invierno",
            "fecha": "18 de Diciembre",
            "anexo_nombre": "Anexo 16.5: Convivio Fraterno Escolar y Metas de Cierre 2026",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Inicio del Receso Vacacional de Invierno.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Redacción de Cartas de Agradecimiento y Solidaridad",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 16.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 16.1 y libreta.",
                "anexo_nombre": "Anexo 16.1: Redacción de Cartas de Agradecimiento y Solidaridad",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Redacción de Cartas de Agradecimiento y Solidaridad."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Presupuesto Familiar: Gasto Inteligente vs. Desperdicio",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 16.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 16.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 16.2: Presupuesto Familiar: Gasto Inteligente vs. Desperdicio",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Presupuesto Familiar: Gasto Inteligente vs. Desperdicio."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Campaña Comunitaria de Donación de Ropa Abrigadora",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 16.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 16.4.",
                "anexo_nombre": "Anexo 16.4: Campaña Comunitaria de Donación de Ropa Abrigadora",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Campaña Comunitaria de Donación de Ropa Abrigadora."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Gastronomía Tradicional y Costumbres de Durango",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 16.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 16.3 y patio cívico.",
                "anexo_nombre": "Anexo 16.3: Gastronomía Tradicional y Costumbres de Durango",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 16.1: Redacción de Cartas de Agradecimiento y Solidaridad", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Redacción de Cartas de Agradecimiento y Solidaridad.", "tema": "Redacción de Cartas de Agradecimiento y Solidaridad", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 16.2: Presupuesto Familiar: Gasto Inteligente vs. Desperdicio", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Presupuesto Familiar: Gasto Inteligente vs. Desperdicio.", "tema": "Presupuesto Familiar: Gasto Inteligente vs. Desperdicio", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 16.3: Gastronomía Tradicional y Costumbres de Durango", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Gastronomía Tradicional y Costumbres de Durango.", "tema": "Gastronomía Tradicional y Costumbres de Durango", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 16.4: Campaña Comunitaria de Donación de Ropa Abrigadora", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Campaña Comunitaria de Donación de Ropa Abrigadora.", "tema": "Campaña Comunitaria de Donación de Ropa Abrigadora", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 16.5: Convivio Fraterno Escolar y Metas de Cierre 2026", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Convivio Fraterno Escolar y Metas de Cierre 2026.", "tema": "Convivio Fraterno Escolar y Metas de Cierre 2026", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. compartir (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    17: {
        "semana": 17,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 17 (Construyendo mi ruta de éxito: Metas 2027 y textos instructivos)",
        "titulo_proyecto": "Construyendo mi ruta de éxito: Metas 2027 y textos instructivos",
        "periodo_sugerido": "Semana 17 de 37 (Enero 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Enero",
        "año": 2027,
        "trimestre": 2,
        "descripcion": "Reinicio lectivo 2027, textos instructivos, diagramas de flujo y gestión del tiempo personal.",
        "efemeride_principal": {
            "nombre": "Reinicio de Clases del Ciclo 2026-2027",
            "fecha": "11 de Enero",
            "anexo_nombre": "Anexo 17.5: Manual de Rutinas Efectivas de Estudio para 6° Grado",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Reinicio de Clases del Ciclo 2026-2027.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Diagnóstico de Compromisos y Metas Personales 2027",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 17.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 17.1 y libreta.",
                "anexo_nombre": "Anexo 17.1: Diagnóstico de Compromisos y Metas Personales 2027",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Diagnóstico de Compromisos y Metas Personales 2027."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Estructura y Lenguaje Imperativo en Instructivos",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 17.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 17.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 17.2: Estructura y Lenguaje Imperativo en Instructivos",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Estructura y Lenguaje Imperativo en Instructivos."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Distribución Fraccionaria del Tiempo Diario",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 17.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 17.4.",
                "anexo_nombre": "Anexo 17.4: Distribución Fraccionaria del Tiempo Diario",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Distribución Fraccionaria del Tiempo Diario."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Diagramas de Flujo y Algoritmos de Resolución",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 17.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 17.3 y patio cívico.",
                "anexo_nombre": "Anexo 17.3: Diagramas de Flujo y Algoritmos de Resolución",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 17.1: Diagnóstico de Compromisos y Metas Personales 2027", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Diagnóstico de Compromisos y Metas Personales 2027.", "tema": "Diagnóstico de Compromisos y Metas Personales 2027", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 17.2: Estructura y Lenguaje Imperativo en Instructivos", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Estructura y Lenguaje Imperativo en Instructivos.", "tema": "Estructura y Lenguaje Imperativo en Instructivos", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 17.3: Diagramas de Flujo y Algoritmos de Resolución", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Diagramas de Flujo y Algoritmos de Resolución.", "tema": "Diagramas de Flujo y Algoritmos de Resolución", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 17.4: Distribución Fraccionaria del Tiempo Diario", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Distribución Fraccionaria del Tiempo Diario.", "tema": "Distribución Fraccionaria del Tiempo Diario", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 17.5: Manual de Rutinas Efectivas de Estudio para 6° Grado", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Manual de Rutinas Efectivas de Estudio para 6° Grado.", "tema": "Manual de Rutinas Efectivas de Estudio para 6° Grado", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. construyendo (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    18: {
        "semana": 18,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 18 (Cerebro sano, cuerpo activo: Sistema nervioso y prevención de adicciones)",
        "titulo_proyecto": "Cerebro sano, cuerpo activo: Sistema nervioso y prevención de adicciones",
        "periodo_sugerido": "Semana 18 de 37 (Enero 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Enero",
        "año": 2027,
        "trimestre": 2,
        "descripcion": "Sistema nervioso central y periférico, neuronas, efectos de sustancias nocivas y toma de decisiones asertiva.",
        "efemeride_principal": {
            "nombre": "Campaña Nacional de Prevención de Adicciones",
            "fecha": "18 de Enero",
            "anexo_nombre": "Anexo 18.5: Diseño de Trípticos Preventivos de la Campaña Escolar",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Campaña Nacional de Prevención de Adicciones.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Anatomía del Sistema Nervioso y Sinapsis Neuronal",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 18.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 18.1 y libreta.",
                "anexo_nombre": "Anexo 18.1: Anatomía del Sistema Nervioso y Sinapsis Neuronal",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Anatomía del Sistema Nervioso y Sinapsis Neuronal."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Impacto Biológico de Sustancias Nocivas en el Cerebro",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 18.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 18.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 18.2: Impacto Biológico de Sustancias Nocivas en el Cerebro",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Impacto Biológico de Sustancias Nocivas en el Cerebro."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Toma de Decisiones Asertivas Frente a la Presión Social",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 18.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 18.4.",
                "anexo_nombre": "Anexo 18.4: Toma de Decisiones Asertivas Frente a la Presión Social",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Toma de Decisiones Asertivas Frente a la Presión Social."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Interpretación de Estadísticas de Salud en Adolescentes",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 18.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 18.3 y patio cívico.",
                "anexo_nombre": "Anexo 18.3: Interpretación de Estadísticas de Salud en Adolescentes",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 18.1: Anatomía del Sistema Nervioso y Sinapsis Neuronal", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Anatomía del Sistema Nervioso y Sinapsis Neuronal.", "tema": "Anatomía del Sistema Nervioso y Sinapsis Neuronal", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 18.2: Impacto Biológico de Sustancias Nocivas en el Cerebro", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Impacto Biológico de Sustancias Nocivas en el Cerebro.", "tema": "Impacto Biológico de Sustancias Nocivas en el Cerebro", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 18.3: Interpretación de Estadísticas de Salud en Adolescentes", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Interpretación de Estadísticas de Salud en Adolescentes.", "tema": "Interpretación de Estadísticas de Salud en Adolescentes", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 18.4: Toma de Decisiones Asertivas Frente a la Presión Social", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Toma de Decisiones Asertivas Frente a la Presión Social.", "tema": "Toma de Decisiones Asertivas Frente a la Presión Social", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 18.5: Diseño de Trípticos Preventivos de la Campaña Escolar", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Diseño de Trípticos Preventivos de la Campaña Escolar.", "tema": "Diseño de Trípticos Preventivos de la Campaña Escolar", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. cerebro (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    19: {
        "semana": 19,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 19 (Nuestra Carta Magna: 110 años de legalidad, democracia y justicia)",
        "titulo_proyecto": "Nuestra Carta Magna: 110 años de legalidad, democracia y justicia",
        "periodo_sugerido": "Semana 19 de 37 (Enero 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Enero",
        "año": 2027,
        "trimestre": 2,
        "descripcion": "Constitución de 1917, artículos 3°, 27° y 123°, jerarquía de leyes y 4ª Sesión Ordinaria CTE.",
        "efemeride_principal": {
            "nombre": "4ª Sesión Ordinaria de Consejo Técnico Escolar (CTE)",
            "fecha": "29 de Enero",
            "anexo_nombre": "Anexo 19.5: Constitución Infantil de 6° 'A' y Evaluación CTE",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a 4ª Sesión Ordinaria de Consejo Técnico Escolar (CTE).",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Contexto del Congreso Constituyente de Querétaro 1917",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 19.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 19.1 y libreta.",
                "anexo_nombre": "Anexo 19.1: Contexto del Congreso Constituyente de Querétaro 1917",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Contexto del Congreso Constituyente de Querétaro 1917."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Artículos Clave: 3° (Educación) y 123° (Trabajo)",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 19.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 19.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 19.2: Artículos Clave: 3° (Educación) y 123° (Trabajo)",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Artículos Clave: 3° (Educación) y 123° (Trabajo)."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Debate Escolar: 'Los Derechos de la Infancia en la Carta Magna'",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 19.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 19.4.",
                "anexo_nombre": "Anexo 19.4: Debate Escolar: 'Los Derechos de la Infancia en la Carta Magna'",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Debate Escolar: 'Los Derechos de la Infancia en la Carta Magna'."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Resolución de Problemas con Fechas y Plazos Jurídicos",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 19.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 19.3 y patio cívico.",
                "anexo_nombre": "Anexo 19.3: Resolución de Problemas con Fechas y Plazos Jurídicos",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 19.1: Contexto del Congreso Constituyente de Querétaro 1917", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Contexto del Congreso Constituyente de Querétaro 1917.", "tema": "Contexto del Congreso Constituyente de Querétaro 1917", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 19.2: Artículos Clave: 3° (Educación) y 123° (Trabajo)", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Artículos Clave: 3° (Educación) y 123° (Trabajo).", "tema": "Artículos Clave: 3° (Educación) y 123° (Trabajo)", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 19.3: Resolución de Problemas con Fechas y Plazos Jurídicos", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Resolución de Problemas con Fechas y Plazos Jurídicos.", "tema": "Resolución de Problemas con Fechas y Plazos Jurídicos", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 19.4: Debate Escolar: 'Los Derechos de la Infancia en la Carta Magna'", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Debate Escolar: 'Los Derechos de la Infancia en la Carta Magna'.", "tema": "Debate Escolar: 'Los Derechos de la Infancia en la Carta Magna'", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 19.5: Constitución Infantil de 6° 'A' y Evaluación CTE", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Constitución Infantil de 6° 'A' y Evaluación CTE.", "tema": "Constitución Infantil de 6° 'A' y Evaluación CTE", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. nuestra (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    20: {
        "semana": 20,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 20 (Nuestra escuela, espacio democrático: Elección y participación ciudadana)",
        "titulo_proyecto": "Nuestra escuela, espacio democrático: Elección y participación ciudadana",
        "periodo_sugerido": "Semana 20 de 37 (Febrero 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Febrero",
        "año": 2027,
        "trimestre": 2,
        "descripcion": "Democracia participativa vs. representativa, simulación de casillas electorales y civismo escolar.",
        "efemeride_principal": {
            "nombre": "Aniversario de la Constitución Política de 1917",
            "fecha": "5 de Febrero",
            "anexo_nombre": "Anexo 20.5: Plan de Intervención para la Mejora de Espacios Escolares",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Aniversario de la Constitución Política de 1917.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Principios de la Democracia Participativa en el Aula",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 20.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 20.1 y libreta.",
                "anexo_nombre": "Anexo 20.1: Principios de la Democracia Participativa en el Aula",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Principios de la Democracia Participativa en el Aula."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Diseño de Planillas y Propuestas Electorales Estudiantiles",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 20.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 20.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 20.2: Diseño de Planillas y Propuestas Electorales Estudiantiles",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Diseño de Planillas y Propuestas Electorales Estudiantiles."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Toma de Protesta y Compromisos de la Directiva Infantil",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 20.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 20.4.",
                "anexo_nombre": "Anexo 20.4: Toma de Protesta y Compromisos de la Directiva Infantil",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Toma de Protesta y Compromisos de la Directiva Infantil."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Conteo de Votos, Porcentajes y Gráficas de Resultados",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 20.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 20.3 y patio cívico.",
                "anexo_nombre": "Anexo 20.3: Conteo de Votos, Porcentajes y Gráficas de Resultados",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 20.1: Principios de la Democracia Participativa en el Aula", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Principios de la Democracia Participativa en el Aula.", "tema": "Principios de la Democracia Participativa en el Aula", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 20.2: Diseño de Planillas y Propuestas Electorales Estudiantiles", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Diseño de Planillas y Propuestas Electorales Estudiantiles.", "tema": "Diseño de Planillas y Propuestas Electorales Estudiantiles", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 20.3: Conteo de Votos, Porcentajes y Gráficas de Resultados", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Conteo de Votos, Porcentajes y Gráficas de Resultados.", "tema": "Conteo de Votos, Porcentajes y Gráficas de Resultados", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 20.4: Toma de Protesta y Compromisos de la Directiva Infantil", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Toma de Protesta y Compromisos de la Directiva Infantil.", "tema": "Toma de Protesta y Compromisos de la Directiva Infantil", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 20.5: Plan de Intervención para la Mejora de Espacios Escolares", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Plan de Intervención para la Mejora de Espacios Escolares.", "tema": "Plan de Intervención para la Mejora de Espacios Escolares", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. nuestra (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    21: {
        "semana": 21,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 21 (Palabras que conectan: Epistolario de la amistad y la empatía)",
        "titulo_proyecto": "Palabras que conectan: Epistolario de la amistad y la empatía",
        "periodo_sugerido": "Semana 21 de 37 (Febrero 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Febrero",
        "año": 2027,
        "trimestre": 2,
        "descripcion": "Cartas formales e informales, correo postal, convivencia armónica y prevención del acoso escolar.",
        "efemeride_principal": {
            "nombre": "Día del Amor y la Amistad Comunitaria",
            "fecha": "14 de Febrero",
            "anexo_nombre": "Anexo 21.5: Buzón de la Amistad y Muestra de Epistolarios de Aula",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día del Amor y la Amistad Comunitaria.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Estructura Formal de la Carta: Encabezado, Cuerpo y Cierre",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 21.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 21.1 y libreta.",
                "anexo_nombre": "Anexo 21.1: Estructura Formal de la Carta: Encabezado, Cuerpo y Cierre",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Estructura Formal de la Carta: Encabezado, Cuerpo y Cierre."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "El Correo Postal en México y Códigos Postales de Durango",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 21.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 21.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 21.2: El Correo Postal en México y Códigos Postales de Durango",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para El Correo Postal en México y Códigos Postales de Durango."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Resolución de Conflictos: La Carta como Herramienta Dialógica",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 21.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 21.4.",
                "anexo_nombre": "Anexo 21.4: Resolución de Conflictos: La Carta como Herramienta Dialógica",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Resolución de Conflictos: La Carta como Herramienta Dialógica."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Cálculo de Tarifas Postales y Distancias Intermunicipales",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 21.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 21.3 y patio cívico.",
                "anexo_nombre": "Anexo 21.3: Cálculo de Tarifas Postales y Distancias Intermunicipales",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 21.1: Estructura Formal de la Carta: Encabezado, Cuerpo y Cierre", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Estructura Formal de la Carta: Encabezado, Cuerpo y Cierre.", "tema": "Estructura Formal de la Carta: Encabezado, Cuerpo y Cierre", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 21.2: El Correo Postal en México y Códigos Postales de Durango", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para El Correo Postal en México y Códigos Postales de Durango.", "tema": "El Correo Postal en México y Códigos Postales de Durango", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 21.3: Cálculo de Tarifas Postales y Distancias Intermunicipales", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Cálculo de Tarifas Postales y Distancias Intermunicipales.", "tema": "Cálculo de Tarifas Postales y Distancias Intermunicipales", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 21.4: Resolución de Conflictos: La Carta como Herramienta Dialógica", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Resolución de Conflictos: La Carta como Herramienta Dialógica.", "tema": "Resolución de Conflictos: La Carta como Herramienta Dialógica", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 21.5: Buzón de la Amistad y Muestra de Epistolarios de Aula", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Buzón de la Amistad y Muestra de Epistolarios de Aula.", "tema": "Buzón de la Amistad y Muestra de Epistolarios de Aula", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. palabras (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    22: {
        "semana": 22,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 22 (Leyes para un México laico: El legado cívico de Benito Juárez)",
        "titulo_proyecto": "Leyes para un México laico: El legado cívico de Benito Juárez",
        "periodo_sugerido": "Semana 22 de 37 (Febrero 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Febrero",
        "año": 2027,
        "trimestre": 2,
        "descripcion": "Leyes de Reforma, Estado laico, libertad de culto, derechos civiles y cronología del siglo XIX.",
        "efemeride_principal": {
            "nombre": "Aniversario Luctuoso de Vicente Guerrero",
            "fecha": "14 de Febrero",
            "anexo_nombre": "Anexo 22.5: Gaceta Cívica Escolar sobre el Estado Laico en México",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Aniversario Luctuoso de Vicente Guerrero.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Pugna entre Liberales y Conservadores en el Siglo XIX",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 22.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 22.1 y libreta.",
                "anexo_nombre": "Anexo 22.1: Pugna entre Liberales y Conservadores en el Siglo XIX",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Pugna entre Liberales y Conservadores en el Siglo XIX."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Las Leyes de Reforma y la Creación del Registro Civil",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 22.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 22.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 22.2: Las Leyes de Reforma y la Creación del Registro Civil",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Las Leyes de Reforma y la Creación del Registro Civil."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Análisis Filosófico de la Frase del Respeto al Derecho Ajeno",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 22.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 22.4.",
                "anexo_nombre": "Anexo 22.4: Análisis Filosófico de la Frase del Respeto al Derecho Ajeno",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Análisis Filosófico de la Frase del Respeto al Derecho Ajeno."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Cálculo de Lapsos Históricos en Líneas de Tiempo Complejas",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 22.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 22.3 y patio cívico.",
                "anexo_nombre": "Anexo 22.3: Cálculo de Lapsos Históricos en Líneas de Tiempo Complejas",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 22.1: Pugna entre Liberales y Conservadores en el Siglo XIX", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Pugna entre Liberales y Conservadores en el Siglo XIX.", "tema": "Pugna entre Liberales y Conservadores en el Siglo XIX", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 22.2: Las Leyes de Reforma y la Creación del Registro Civil", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Las Leyes de Reforma y la Creación del Registro Civil.", "tema": "Las Leyes de Reforma y la Creación del Registro Civil", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 22.3: Cálculo de Lapsos Históricos en Líneas de Tiempo Complejas", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Cálculo de Lapsos Históricos en Líneas de Tiempo Complejas.", "tema": "Cálculo de Lapsos Históricos en Líneas de Tiempo Complejas", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 22.4: Análisis Filosófico de la Frase del Respeto al Derecho Ajeno", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Análisis Filosófico de la Frase del Respeto al Derecho Ajeno.", "tema": "Análisis Filosófico de la Frase del Respeto al Derecho Ajeno", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 22.5: Gaceta Cívica Escolar sobre el Estado Laico en México", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Gaceta Cívica Escolar sobre el Estado Laico en México.", "tema": "Gaceta Cívica Escolar sobre el Estado Laico en México", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. leyes (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    23: {
        "semana": 23,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 23 (Símbolos que nos unen: Identidad, historia y respeto a la Bandera)",
        "titulo_proyecto": "Símbolos que nos unen: Identidad, historia y respeto a la Bandera",
        "periodo_sugerido": "Semana 23 de 37 (Febrero 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Febrero",
        "año": 2027,
        "trimestre": 2,
        "descripcion": "Evolución de la Bandera Nacional, geometría de proporciones (4 a 7), Escudo y 5ª Sesión CTE.",
        "efemeride_principal": {
            "nombre": "Día de la Bandera Nacional y 5ª Sesión CTE",
            "fecha": "24 y 26 de Febrero",
            "anexo_nombre": "Anexo 23.5: Ceremonia Demostrativa y Balance Pedagógico 5ª Sesión CTE",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día de la Bandera Nacional y 5ª Sesión CTE.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Evolución Histórica de los Estandartes y Banderas de México",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 23.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 23.1 y libreta.",
                "anexo_nombre": "Anexo 23.1: Evolución Histórica de los Estandartes y Banderas de México",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Evolución Histórica de los Estandartes y Banderas de México."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Geometría de Proporciones (4:7) en Lienzos Patrios",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 23.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 23.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 23.2: Geometría de Proporciones (4:7) en Lienzos Patrios",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Geometría de Proporciones (4:7) en Lienzos Patrios."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Poesía Cívica y Análisis de las Estrofas del Himno Nacional",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 23.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 23.4.",
                "anexo_nombre": "Anexo 23.4: Poesía Cívica y Análisis de las Estrofas del Himno Nacional",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Poesía Cívica y Análisis de las Estrofas del Himno Nacional."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Significado Cívico y Mitológico del Escudo Nacional",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 23.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 23.3 y patio cívico.",
                "anexo_nombre": "Anexo 23.3: Significado Cívico y Mitológico del Escudo Nacional",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 23.1: Evolución Histórica de los Estandartes y Banderas de México", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Evolución Histórica de los Estandartes y Banderas de México.", "tema": "Evolución Histórica de los Estandartes y Banderas de México", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 23.2: Geometría de Proporciones (4:7) en Lienzos Patrios", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Geometría de Proporciones (4:7) en Lienzos Patrios.", "tema": "Geometría de Proporciones (4:7) en Lienzos Patrios", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 23.3: Significado Cívico y Mitológico del Escudo Nacional", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Significado Cívico y Mitológico del Escudo Nacional.", "tema": "Significado Cívico y Mitológico del Escudo Nacional", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 23.4: Poesía Cívica y Análisis de las Estrofas del Himno Nacional", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Poesía Cívica y Análisis de las Estrofas del Himno Nacional.", "tema": "Poesía Cívica y Análisis de las Estrofas del Himno Nacional", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 23.5: Ceremonia Demostrativa y Balance Pedagógico 5ª Sesión CTE", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Ceremonia Demostrativa y Balance Pedagógico 5ª Sesión CTE.", "tema": "Ceremonia Demostrativa y Balance Pedagógico 5ª Sesión CTE", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. símbolos (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    24: {
        "semana": 24,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 24 (Cuentas claras, futuro seguro: Educación financiera comunitaria)",
        "titulo_proyecto": "Cuentas claras, futuro seguro: Educación financiera comunitaria",
        "periodo_sugerido": "Semana 24 de 37 (Marzo 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Marzo",
        "año": 2027,
        "trimestre": 2,
        "descripcion": "Presupuesto personal, porcentajes, descuentos comerciales, tasa de IVA y economía familiar.",
        "efemeride_principal": {
            "nombre": "Semana Nacional de Educación Financiera",
            "fecha": "Primeros días de Marzo",
            "anexo_nombre": "Anexo 24.5: Feria de Simulación de Compras Inteligentes en el Aula",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Semana Nacional de Educación Financiera.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Ingresos, Gastos Fijos y Cultura del Ahorro Familiar",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 24.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 24.1 y libreta.",
                "anexo_nombre": "Anexo 24.1: Ingresos, Gastos Fijos y Cultura del Ahorro Familiar",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Ingresos, Gastos Fijos y Cultura del Ahorro Familiar."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Cálculo Rápido de Porcentajes de Descuento en Tiendas",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 24.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 24.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 24.2: Cálculo Rápido de Porcentajes de Descuento en Tiendas",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Cálculo Rápido de Porcentajes de Descuento en Tiendas."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "El Impacto del Crédito y Deudas en el Bienestar del Hogar",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 24.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 24.4.",
                "anexo_nombre": "Anexo 24.4: El Impacto del Crédito y Deudas en el Bienestar del Hogar",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre El Impacto del Crédito y Deudas en el Bienestar del Hogar."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Comparación de Precios de la Canasta Básica en Durango",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 24.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 24.3 y patio cívico.",
                "anexo_nombre": "Anexo 24.3: Comparación de Precios de la Canasta Básica en Durango",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 24.1: Ingresos, Gastos Fijos y Cultura del Ahorro Familiar", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Ingresos, Gastos Fijos y Cultura del Ahorro Familiar.", "tema": "Ingresos, Gastos Fijos y Cultura del Ahorro Familiar", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 24.2: Cálculo Rápido de Porcentajes de Descuento en Tiendas", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Cálculo Rápido de Porcentajes de Descuento en Tiendas.", "tema": "Cálculo Rápido de Porcentajes de Descuento en Tiendas", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 24.3: Comparación de Precios de la Canasta Básica en Durango", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Comparación de Precios de la Canasta Básica en Durango.", "tema": "Comparación de Precios de la Canasta Básica en Durango", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 24.4: El Impacto del Crédito y Deudas en el Bienestar del Hogar", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para El Impacto del Crédito y Deudas en el Bienestar del Hogar.", "tema": "El Impacto del Crédito y Deudas en el Bienestar del Hogar", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 24.5: Feria de Simulación de Compras Inteligentes en el Aula", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Feria de Simulación de Compras Inteligentes en el Aula.", "tema": "Feria de Simulación de Compras Inteligentes en el Aula", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. cuentas (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    25: {
        "semana": 25,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 25 (Mujeres transformadoras de nuestra historia y comunidad)",
        "titulo_proyecto": "Mujeres transformadoras de nuestra historia y comunidad",
        "periodo_sugerido": "Semana 25 de 37 (Marzo 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Marzo",
        "año": 2027,
        "trimestre": 2,
        "descripcion": "Día Internacional de la Mujer, biografías de líderes mexicanas y duranguenses, equidad y respeto.",
        "efemeride_principal": {
            "nombre": "Día Internacional de la Mujer (8 de Marzo)",
            "fecha": "8 de Marzo",
            "anexo_nombre": "Anexo 25.5: Mural Comunitario 'Voces de Mujeres que Transforman'",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día Internacional de la Mujer (8 de Marzo).",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Historia de la Lucha por la Igualdad Laboral y Educativa",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 25.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 25.1 y libreta.",
                "anexo_nombre": "Anexo 25.1: Historia de la Lucha por la Igualdad Laboral y Educativa",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Historia de la Lucha por la Igualdad Laboral y Educativa."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Biografías de Sor Juana, Leona Vicario y Hermila Galindo",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 25.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 25.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 25.2: Biografías de Sor Juana, Leona Vicario y Hermila Galindo",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Biografías de Sor Juana, Leona Vicario y Hermila Galindo."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Entrevistas a Mujeres Destacadas de la Comunidad Local",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 25.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 25.4.",
                "anexo_nombre": "Anexo 25.4: Entrevistas a Mujeres Destacadas de la Comunidad Local",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Entrevistas a Mujeres Destacadas de la Comunidad Local."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Estadísticas de Acceso Femenino a Carreras Científicas",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 25.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 25.3 y patio cívico.",
                "anexo_nombre": "Anexo 25.3: Estadísticas de Acceso Femenino a Carreras Científicas",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 25.1: Historia de la Lucha por la Igualdad Laboral y Educativa", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Historia de la Lucha por la Igualdad Laboral y Educativa.", "tema": "Historia de la Lucha por la Igualdad Laboral y Educativa", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 25.2: Biografías de Sor Juana, Leona Vicario y Hermila Galindo", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Biografías de Sor Juana, Leona Vicario y Hermila Galindo.", "tema": "Biografías de Sor Juana, Leona Vicario y Hermila Galindo", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 25.3: Estadísticas de Acceso Femenino a Carreras Científicas", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Estadísticas de Acceso Femenino a Carreras Científicas.", "tema": "Estadísticas de Acceso Femenino a Carreras Científicas", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 25.4: Entrevistas a Mujeres Destacadas de la Comunidad Local", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Entrevistas a Mujeres Destacadas de la Comunidad Local.", "tema": "Entrevistas a Mujeres Destacadas de la Comunidad Local", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 25.5: Mural Comunitario 'Voces de Mujeres que Transforman'", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Mural Comunitario 'Voces de Mujeres que Transforman'.", "tema": "Mural Comunitario 'Voces de Mujeres que Transforman'", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. mujeres (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    26: {
        "semana": 26,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 26 (Soberanía y recursos estratégicos: Cierre del Segundo Trimestre)",
        "titulo_proyecto": "Soberanía y recursos estratégicos: Cierre del Segundo Trimestre",
        "periodo_sugerido": "Semana 26 de 37 (Marzo 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Marzo",
        "año": 2027,
        "trimestre": 2,
        "descripcion": "Expropiación Petrolera (18 de Marzo), Natalicio de Juárez (21 de Marzo) y 6ª Sesión CTE.",
        "efemeride_principal": {
            "nombre": "Expropiación Petrolera y 6ª Sesión Ordinaria CTE",
            "fecha": "18 y 26 de Marzo",
            "anexo_nombre": "Anexo 26.5: Asamblea de Cierre de Trimestre 2 y Sesión CTE Pre-Vacacional",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Expropiación Petrolera y 6ª Sesión Ordinaria CTE.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "18 de Marzo de 1938: Lázaro Cárdenas y la Soberanía Petrolera",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 26.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 26.1 y libreta.",
                "anexo_nombre": "Anexo 26.1: 18 de Marzo de 1938: Lázaro Cárdenas y la Soberanía Petrolera",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de 18 de Marzo de 1938: Lázaro Cárdenas y la Soberanía Petrolera."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Derivados del Petróleo y Alternativas de Transición Verde",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 26.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 26.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 26.2: Derivados del Petróleo y Alternativas de Transición Verde",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Derivados del Petróleo y Alternativas de Transición Verde."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Portafolio de Logros Curriculares de los 4 Campos NEM",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 26.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 26.4.",
                "anexo_nombre": "Anexo 26.4: Portafolio de Logros Curriculares de los 4 Campos NEM",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Portafolio de Logros Curriculares de los 4 Campos NEM."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Evaluación Formativa Integradora del Segundo Trimestre",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 26.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 26.3 y patio cívico.",
                "anexo_nombre": "Anexo 26.3: Evaluación Formativa Integradora del Segundo Trimestre",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 26.1: 18 de Marzo de 1938: Lázaro Cárdenas y la Soberanía Petrolera", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para 18 de Marzo de 1938: Lázaro Cárdenas y la Soberanía Petrolera.", "tema": "18 de Marzo de 1938: Lázaro Cárdenas y la Soberanía Petrolera", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 26.2: Derivados del Petróleo y Alternativas de Transición Verde", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Derivados del Petróleo y Alternativas de Transición Verde.", "tema": "Derivados del Petróleo y Alternativas de Transición Verde", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 26.3: Evaluación Formativa Integradora del Segundo Trimestre", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Evaluación Formativa Integradora del Segundo Trimestre.", "tema": "Evaluación Formativa Integradora del Segundo Trimestre", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 26.4: Portafolio de Logros Curriculares de los 4 Campos NEM", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Portafolio de Logros Curriculares de los 4 Campos NEM.", "tema": "Portafolio de Logros Curriculares de los 4 Campos NEM", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 26.5: Asamblea de Cierre de Trimestre 2 y Sesión CTE Pre-Vacacional", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Asamblea de Cierre de Trimestre 2 y Sesión CTE Pre-Vacacional.", "tema": "Asamblea de Cierre de Trimestre 2 y Sesión CTE Pre-Vacacional", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. soberanía (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    27: {
        "semana": 27,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 27 (Cada gota cuenta: Cuidado del agua y sustentabilidad en Durango)",
        "titulo_proyecto": "Cada gota cuenta: Cuidado del agua y sustentabilidad en Durango",
        "periodo_sugerido": "Semana 27 de 37 (Abril 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Abril",
        "año": 2027,
        "trimestre": 3,
        "descripcion": "Ciclo del agua, huella hídrica, cuencas de Durango, medición de litros y prevención de sequías.",
        "efemeride_principal": {
            "nombre": "Regreso de Vacaciones de Semana Santa",
            "fecha": "5 de Abril",
            "anexo_nombre": "Anexo 27.5: Campaña y Brigada Escolar de Detección de Fugas de Agua",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Regreso de Vacaciones de Semana Santa.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "El Ciclo Hidrológico y Fuentes de Abastecimiento en Durango",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 27.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 27.1 y libreta.",
                "anexo_nombre": "Anexo 27.1: El Ciclo Hidrológico y Fuentes de Abastecimiento en Durango",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de El Ciclo Hidrológico y Fuentes de Abastecimiento en Durango."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Cálculo de la Huella Hídrica Diaria Personal y Escolar",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 27.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 27.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 27.2: Cálculo de la Huella Hídrica Diaria Personal y Escolar",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Cálculo de la Huella Hídrica Diaria Personal y Escolar."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Diseño de un Sistema Escolar de Cosecha de Lluvia",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 27.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 27.4.",
                "anexo_nombre": "Anexo 27.4: Diseño de un Sistema Escolar de Cosecha de Lluvia",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Diseño de un Sistema Escolar de Cosecha de Lluvia."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Causas y Efectos de la Sequía en el Norte de México",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 27.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 27.3 y patio cívico.",
                "anexo_nombre": "Anexo 27.3: Causas y Efectos de la Sequía en el Norte de México",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 27.1: El Ciclo Hidrológico y Fuentes de Abastecimiento en Durango", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para El Ciclo Hidrológico y Fuentes de Abastecimiento en Durango.", "tema": "El Ciclo Hidrológico y Fuentes de Abastecimiento en Durango", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 27.2: Cálculo de la Huella Hídrica Diaria Personal y Escolar", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Cálculo de la Huella Hídrica Diaria Personal y Escolar.", "tema": "Cálculo de la Huella Hídrica Diaria Personal y Escolar", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 27.3: Causas y Efectos de la Sequía en el Norte de México", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Causas y Efectos de la Sequía en el Norte de México.", "tema": "Causas y Efectos de la Sequía en el Norte de México", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 27.4: Diseño de un Sistema Escolar de Cosecha de Lluvia", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Diseño de un Sistema Escolar de Cosecha de Lluvia.", "tema": "Diseño de un Sistema Escolar de Cosecha de Lluvia", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 27.5: Campaña y Brigada Escolar de Detección de Fugas de Agua", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Campaña y Brigada Escolar de Detección de Fugas de Agua.", "tema": "Campaña y Brigada Escolar de Detección de Fugas de Agua", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. cada (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    28: {
        "semana": 28,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 28 (Palabras con ritmo y sentimiento: Taller de poesía infantil)",
        "titulo_proyecto": "Palabras con ritmo y sentimiento: Taller de poesía infantil",
        "periodo_sugerido": "Semana 28 de 37 (Abril 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Abril",
        "año": 2027,
        "trimestre": 3,
        "descripcion": "Poesía, estrofas, figuras retóricas (metáfora, símil), declamación y textos de Múltiples Lenguajes.",
        "efemeride_principal": {
            "nombre": "Día Mundial de la Tierra",
            "fecha": "22 de Abril",
            "anexo_nombre": "Anexo 28.5: Recital Poético de Aula con Declamación en Atril",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día Mundial de la Tierra.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Métrica, Estrofas y Conteo Silábico en Poemas",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 28.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 28.1 y libreta.",
                "anexo_nombre": "Anexo 28.1: Métrica, Estrofas y Conteo Silábico en Poemas",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Métrica, Estrofas y Conteo Silábico en Poemas."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Figuras Retóricas: Metáforas, Símiles y Personificación",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 28.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 28.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 28.2: Figuras Retóricas: Metáforas, Símiles y Personificación",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Figuras Retóricas: Metáforas, Símiles y Personificación."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Poemas a la Naturaleza y la Tierra de Autores Mexicanos",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 28.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 28.4.",
                "anexo_nombre": "Anexo 28.4: Poemas a la Naturaleza y la Tierra de Autores Mexicanos",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Poemas a la Naturaleza y la Tierra de Autores Mexicanos."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Patrones Rítmicos Matemáticos en la Composición Poética",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 28.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 28.3 y patio cívico.",
                "anexo_nombre": "Anexo 28.3: Patrones Rítmicos Matemáticos en la Composición Poética",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 28.1: Métrica, Estrofas y Conteo Silábico en Poemas", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Métrica, Estrofas y Conteo Silábico en Poemas.", "tema": "Métrica, Estrofas y Conteo Silábico en Poemas", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 28.2: Figuras Retóricas: Metáforas, Símiles y Personificación", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Figuras Retóricas: Metáforas, Símiles y Personificación.", "tema": "Figuras Retóricas: Metáforas, Símiles y Personificación", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 28.3: Patrones Rítmicos Matemáticos en la Composición Poética", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Patrones Rítmicos Matemáticos en la Composición Poética.", "tema": "Patrones Rítmicos Matemáticos en la Composición Poética", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 28.4: Poemas a la Naturaleza y la Tierra de Autores Mexicanos", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Poemas a la Naturaleza y la Tierra de Autores Mexicanos.", "tema": "Poemas a la Naturaleza y la Tierra de Autores Mexicanos", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 28.5: Recital Poético de Aula con Declamación en Atril", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Recital Poético de Aula con Declamación en Atril.", "tema": "Recital Poético de Aula con Declamación en Atril", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. palabras (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    29: {
        "semana": 29,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 29 (Viajeros entre páginas: Feria del libro y maratón lector)",
        "titulo_proyecto": "Viajeros entre páginas: Feria del libro y maratón lector",
        "periodo_sugerido": "Semana 29 de 37 (Abril 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Abril",
        "año": 2027,
        "trimestre": 3,
        "descripcion": "Día Mundial del Libro (23 de Abril), reseña literaria crítica, velocidad lectora y fomento a la lectura.",
        "efemeride_principal": {
            "nombre": "Día Internacional del Libro y Derechos de Autor",
            "fecha": "23 de Abril",
            "anexo_nombre": "Anexo 29.5: Tianguis del Libro: Intercambio Escolar y Maratón de Lectura",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día Internacional del Libro y Derechos de Autor.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Historia de la Imprenta y el Libro como Bien Cultural",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 29.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 29.1 y libreta.",
                "anexo_nombre": "Anexo 29.1: Historia de la Imprenta y el Libro como Bien Cultural",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Historia de la Imprenta y el Libro como Bien Cultural."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Estructura y Redacción de Reseñas Críticas de Lectura",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 29.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 29.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 29.2: Estructura y Redacción de Reseñas Críticas de Lectura",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Estructura y Redacción de Reseñas Críticas de Lectura."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Diseño de Separadores Literarios y Pasaportes Lectores",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 29.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 29.4.",
                "anexo_nombre": "Anexo 29.4: Diseño de Separadores Literarios y Pasaportes Lectores",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Diseño de Separadores Literarios y Pasaportes Lectores."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Registro y Gráfica de Fluidez Lectora (Palabras por Minuto)",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 29.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 29.3 y patio cívico.",
                "anexo_nombre": "Anexo 29.3: Registro y Gráfica de Fluidez Lectora (Palabras por Minuto)",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 29.1: Historia de la Imprenta y el Libro como Bien Cultural", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Historia de la Imprenta y el Libro como Bien Cultural.", "tema": "Historia de la Imprenta y el Libro como Bien Cultural", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 29.2: Estructura y Redacción de Reseñas Críticas de Lectura", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Estructura y Redacción de Reseñas Críticas de Lectura.", "tema": "Estructura y Redacción de Reseñas Críticas de Lectura", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 29.3: Registro y Gráfica de Fluidez Lectora (Palabras por Minuto)", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Registro y Gráfica de Fluidez Lectora (Palabras por Minuto).", "tema": "Registro y Gráfica de Fluidez Lectora (Palabras por Minuto)", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 29.4: Diseño de Separadores Literarios y Pasaportes Lectores", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Diseño de Separadores Literarios y Pasaportes Lectores.", "tema": "Diseño de Separadores Literarios y Pasaportes Lectores", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 29.5: Tianguis del Libro: Intercambio Escolar y Maratón de Lectura", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Tianguis del Libro: Intercambio Escolar y Maratón de Lectura.", "tema": "Tianguis del Libro: Intercambio Escolar y Maratón de Lectura", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. viajeros (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    30: {
        "semana": 30,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 30 (El juego como derecho y aprendizaje: Celebrando nuestra niñez)",
        "titulo_proyecto": "El juego como derecho y aprendizaje: Celebrando nuestra niñez",
        "periodo_sugerido": "Semana 30 de 37 (Abril 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Abril",
        "año": 2027,
        "trimestre": 3,
        "descripcion": "Día de la Niñez (30 de Abril), derechos infantiles de UNICEF, juegos tradicionales y probabilidad.",
        "efemeride_principal": {
            "nombre": "Día de la Niña y del Niño (30 de Abril)",
            "fecha": "30 de Abril",
            "anexo_nombre": "Anexo 30.5: Festival Lúdico de Juegos Tradicionales en el Patio Cívico",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día de la Niña y del Niño (30 de Abril).",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Los 10 Derechos Fundamentales de las Niñas y Niños",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 30.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 30.1 y libreta.",
                "anexo_nombre": "Anexo 30.1: Los 10 Derechos Fundamentales de las Niñas y Niños",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Los 10 Derechos Fundamentales de las Niñas y Niños."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Juegos Tradicionales de México: Reglas y Convivencia",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 30.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 30.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 30.2: Juegos Tradicionales de México: Reglas y Convivencia",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Juegos Tradicionales de México: Reglas y Convivencia."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Entrevista Intergeneracional sobre Juegos de Antes y Hoy",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 30.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 30.4.",
                "anexo_nombre": "Anexo 30.4: Entrevista Intergeneracional sobre Juegos de Antes y Hoy",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Entrevista Intergeneracional sobre Juegos de Antes y Hoy."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Probabilidad Frecuencial en Juegos Didácticos de Azar",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 30.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 30.3 y patio cívico.",
                "anexo_nombre": "Anexo 30.3: Probabilidad Frecuencial en Juegos Didácticos de Azar",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 30.1: Los 10 Derechos Fundamentales de las Niñas y Niños", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Los 10 Derechos Fundamentales de las Niñas y Niños.", "tema": "Los 10 Derechos Fundamentales de las Niñas y Niños", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 30.2: Juegos Tradicionales de México: Reglas y Convivencia", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Juegos Tradicionales de México: Reglas y Convivencia.", "tema": "Juegos Tradicionales de México: Reglas y Convivencia", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 30.3: Probabilidad Frecuencial en Juegos Didácticos de Azar", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Probabilidad Frecuencial en Juegos Didácticos de Azar.", "tema": "Probabilidad Frecuencial en Juegos Didácticos de Azar", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 30.4: Entrevista Intergeneracional sobre Juegos de Antes y Hoy", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Entrevista Intergeneracional sobre Juegos de Antes y Hoy.", "tema": "Entrevista Intergeneracional sobre Juegos de Antes y Hoy", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 30.5: Festival Lúdico de Juegos Tradicionales en el Patio Cívico", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Festival Lúdico de Juegos Tradicionales en el Patio Cívico.", "tema": "Festival Lúdico de Juegos Tradicionales en el Patio Cívico", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. el (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    31: {
        "semana": 31,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 31 (Zaragoza y los valientes de Puebla: Soberanía nacional y 5 de Mayo)",
        "titulo_proyecto": "Zaragoza y los valientes de Puebla: Soberanía nacional y 5 de Mayo",
        "periodo_sugerido": "Semana 31 de 37 (Mayo 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Mayo",
        "año": 2027,
        "trimestre": 3,
        "descripcion": "Batalla de Puebla de 1862, resistencia frente al ejército francés, crónicas bélicas y cartografía.",
        "efemeride_principal": {
            "nombre": "Conmemoración de la Batalla de Puebla (5 de Mayo)",
            "fecha": "5 de Mayo",
            "anexo_nombre": "Anexo 31.5: Periódico Mural Cívico y Telegrama Histórico de Victoria",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Conmemoración de la Batalla de Puebla (5 de Mayo).",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Causas de la Intervención Francesa y Suspensión de Pagos",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 31.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 31.1 y libreta.",
                "anexo_nombre": "Anexo 31.1: Causas de la Intervención Francesa y Suspensión de Pagos",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Causas de la Intervención Francesa y Suspensión de Pagos."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Estrategia Militar de Ignacio Zaragoza y los Zacapoaxtlas",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 31.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 31.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 31.2: Estrategia Militar de Ignacio Zaragoza y los Zacapoaxtlas",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Estrategia Militar de Ignacio Zaragoza y los Zacapoaxtlas."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Redacción de una Crónica Periodística de la Batalla",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 31.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 31.4.",
                "anexo_nombre": "Anexo 31.4: Redacción de una Crónica Periodística de la Batalla",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Redacción de una Crónica Periodística de la Batalla."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Cálculo de Tiempos y Posiciones en Planos Topográficos",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 31.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 31.3 y patio cívico.",
                "anexo_nombre": "Anexo 31.3: Cálculo de Tiempos y Posiciones en Planos Topográficos",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 31.1: Causas de la Intervención Francesa y Suspensión de Pagos", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Causas de la Intervención Francesa y Suspensión de Pagos.", "tema": "Causas de la Intervención Francesa y Suspensión de Pagos", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 31.2: Estrategia Militar de Ignacio Zaragoza y los Zacapoaxtlas", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Estrategia Militar de Ignacio Zaragoza y los Zacapoaxtlas.", "tema": "Estrategia Militar de Ignacio Zaragoza y los Zacapoaxtlas", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 31.3: Cálculo de Tiempos y Posiciones en Planos Topográficos", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Cálculo de Tiempos y Posiciones en Planos Topográficos.", "tema": "Cálculo de Tiempos y Posiciones en Planos Topográficos", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 31.4: Redacción de una Crónica Periodística de la Batalla", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Redacción de una Crónica Periodística de la Batalla.", "tema": "Redacción de una Crónica Periodística de la Batalla", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 31.5: Periódico Mural Cívico y Telegrama Histórico de Victoria", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Periódico Mural Cívico y Telegrama Histórico de Victoria.", "tema": "Periódico Mural Cívico y Telegrama Histórico de Victoria", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. zaragoza (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    32: {
        "semana": 32,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 32 (Tributo a quienes nos forman: Familia, afecto y educación)",
        "titulo_proyecto": "Tributo a quienes nos forman: Familia, afecto y educación",
        "periodo_sugerido": "Semana 32 de 37 (Mayo 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Mayo",
        "año": 2027,
        "trimestre": 3,
        "descripcion": "Día de la Madre (10 de Mayo), Día del Maestro (15 de Mayo), redes familiares de apoyo y gratitud.",
        "efemeride_principal": {
            "nombre": "Día de la Madre y Día del Maestro",
            "fecha": "10 y 15 de Mayo",
            "anexo_nombre": "Anexo 32.5: Asamblea y Festival Comunitario de Gratitud Escolar",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día de la Madre y Día del Maestro.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "El Rol de la Familia en el Desarrollo Emocional Infantil",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 32.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 32.1 y libreta.",
                "anexo_nombre": "Anexo 32.1: El Rol de la Familia en el Desarrollo Emocional Infantil",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de El Rol de la Familia en el Desarrollo Emocional Infantil."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Historia de la Educación Pública y los Maestros en México",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 32.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 32.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 32.2: Historia de la Educación Pública y los Maestros en México",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Historia de la Educación Pública y los Maestros en México."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Redacción Epistolar de Agradecimiento con Acentuación Cuidada",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 32.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 32.4.",
                "anexo_nombre": "Anexo 32.4: Redacción Epistolar de Agradecimiento con Acentuación Cuidada",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Redacción Epistolar de Agradecimiento con Acentuación Cuidada."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Problemas de Proporcionalidad en Presupuestos de Festejos",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 32.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 32.3 y patio cívico.",
                "anexo_nombre": "Anexo 32.3: Problemas de Proporcionalidad en Presupuestos de Festejos",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 32.1: El Rol de la Familia en el Desarrollo Emocional Infantil", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para El Rol de la Familia en el Desarrollo Emocional Infantil.", "tema": "El Rol de la Familia en el Desarrollo Emocional Infantil", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 32.2: Historia de la Educación Pública y los Maestros en México", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Historia de la Educación Pública y los Maestros en México.", "tema": "Historia de la Educación Pública y los Maestros en México", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 32.3: Problemas de Proporcionalidad en Presupuestos de Festejos", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Problemas de Proporcionalidad en Presupuestos de Festejos.", "tema": "Problemas de Proporcionalidad en Presupuestos de Festejos", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 32.4: Redacción Epistolar de Agradecimiento con Acentuación Cuidada", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Redacción Epistolar de Agradecimiento con Acentuación Cuidada.", "tema": "Redacción Epistolar de Agradecimiento con Acentuación Cuidada", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 32.5: Asamblea y Festival Comunitario de Gratitud Escolar", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Asamblea y Festival Comunitario de Gratitud Escolar.", "tema": "Asamblea y Festival Comunitario de Gratitud Escolar", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. tributo (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    33: {
        "semana": 33,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 33 (Geometría en nuestra tierra: Cuerpos geométricos y arquitectura de Durango)",
        "titulo_proyecto": "Geometría en nuestra tierra: Cuerpos geométricos y arquitectura de Durango",
        "periodo_sugerido": "Semana 33 de 37 (Mayo 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Mayo",
        "año": 2027,
        "trimestre": 3,
        "descripcion": "Cuerpos geométricos (prismas, pirámides), volumen, aristas y arquitectura histórica de Durango.",
        "efemeride_principal": {
            "nombre": "Día del Estudiante",
            "fecha": "23 de Mayo",
            "anexo_nombre": "Anexo 33.5: Exposición de Maquetas Urbanas Sustentables a Escala",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día del Estudiante.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Clasificación de Poliedros: Caras, Aristas y Vértices",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 33.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 33.1 y libreta.",
                "anexo_nombre": "Anexo 33.1: Clasificación de Poliedros: Caras, Aristas y Vértices",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Clasificación de Poliedros: Caras, Aristas y Vértices."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Fórmulas y Cálculo de Volumen en Prismas Rectangulares",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 33.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 33.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 33.2: Fórmulas y Cálculo de Volumen en Prismas Rectangulares",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Fórmulas y Cálculo de Volumen en Prismas Rectangulares."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Armado de Maquetas con Plantillas Bidimensionales",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 33.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 33.4.",
                "anexo_nombre": "Anexo 33.4: Armado de Maquetas con Plantillas Bidimensionales",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Armado de Maquetas con Plantillas Bidimensionales."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Elementos Geométricos en Monumentos Históricos de Durango",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 33.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 33.3 y patio cívico.",
                "anexo_nombre": "Anexo 33.3: Elementos Geométricos en Monumentos Históricos de Durango",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 33.1: Clasificación de Poliedros: Caras, Aristas y Vértices", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Clasificación de Poliedros: Caras, Aristas y Vértices.", "tema": "Clasificación de Poliedros: Caras, Aristas y Vértices", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 33.2: Fórmulas y Cálculo de Volumen en Prismas Rectangulares", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Fórmulas y Cálculo de Volumen en Prismas Rectangulares.", "tema": "Fórmulas y Cálculo de Volumen en Prismas Rectangulares", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 33.3: Elementos Geométricos en Monumentos Históricos de Durango", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Elementos Geométricos en Monumentos Históricos de Durango.", "tema": "Elementos Geométricos en Monumentos Históricos de Durango", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 33.4: Armado de Maquetas con Plantillas Bidimensionales", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Armado de Maquetas con Plantillas Bidimensionales.", "tema": "Armado de Maquetas con Plantillas Bidimensionales", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 33.5: Exposición de Maquetas Urbanas Sustentables a Escala", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Exposición de Maquetas Urbanas Sustentables a Escala.", "tema": "Exposición de Maquetas Urbanas Sustentables a Escala", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. geometría (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    34: {
        "semana": 34,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 34 (México multilingüe: Lenguas y culturas originarias de nuestra tierra)",
        "titulo_proyecto": "México multilingüe: Lenguas y culturas originarias de nuestra tierra",
        "periodo_sugerido": "Semana 34 de 37 (Mayo 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Mayo",
        "año": 2027,
        "trimestre": 3,
        "descripcion": "Diversidad lingüística, pueblos o'dam, wixárika y nahuas de Durango, préstamos léxicos y 7ª Sesión CTE.",
        "efemeride_principal": {
            "nombre": "7ª Sesión Ordinaria de Consejo Técnico Escolar (CTE)",
            "fecha": "28 de Mayo",
            "anexo_nombre": "Anexo 34.5: Diccionario Bilingüe Escolar y Evaluación Formativa CTE",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a 7ª Sesión Ordinaria de Consejo Técnico Escolar (CTE).",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "El Mapa Lingüístico Nacional y las 68 Lenguas Originarias",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 34.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 34.1 y libreta.",
                "anexo_nombre": "Anexo 34.1: El Mapa Lingüístico Nacional y las 68 Lenguas Originarias",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de El Mapa Lingüístico Nacional y las 68 Lenguas Originarias."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Pueblos Indígenas de Durango: Tepehuanos y Huicholes",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 34.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 34.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 34.2: Pueblos Indígenas de Durango: Tepehuanos y Huicholes",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Pueblos Indígenas de Durango: Tepehuanos y Huicholes."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Tradición Oral: Mitos y Leyendas Cosmocéntricas del Norte",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 34.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 34.4.",
                "anexo_nombre": "Anexo 34.4: Tradición Oral: Mitos y Leyendas Cosmocéntricas del Norte",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Tradición Oral: Mitos y Leyendas Cosmocéntricas del Norte."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Nahuatlismos en el Español Cotidiano de México",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 34.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 34.3 y patio cívico.",
                "anexo_nombre": "Anexo 34.3: Nahuatlismos en el Español Cotidiano de México",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 34.1: El Mapa Lingüístico Nacional y las 68 Lenguas Originarias", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para El Mapa Lingüístico Nacional y las 68 Lenguas Originarias.", "tema": "El Mapa Lingüístico Nacional y las 68 Lenguas Originarias", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 34.2: Pueblos Indígenas de Durango: Tepehuanos y Huicholes", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Pueblos Indígenas de Durango: Tepehuanos y Huicholes.", "tema": "Pueblos Indígenas de Durango: Tepehuanos y Huicholes", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 34.3: Nahuatlismos en el Español Cotidiano de México", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Nahuatlismos en el Español Cotidiano de México.", "tema": "Nahuatlismos en el Español Cotidiano de México", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 34.4: Tradición Oral: Mitos y Leyendas Cosmocéntricas del Norte", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Tradición Oral: Mitos y Leyendas Cosmocéntricas del Norte.", "tema": "Tradición Oral: Mitos y Leyendas Cosmocéntricas del Norte", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 34.5: Diccionario Bilingüe Escolar y Evaluación Formativa CTE", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Diccionario Bilingüe Escolar y Evaluación Formativa CTE.", "tema": "Diccionario Bilingüe Escolar y Evaluación Formativa CTE", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. méxico (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    35: {
        "semana": 35,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 35 (Escuela verde: Huerto escolar, compostaje y reciclaje creativo)",
        "titulo_proyecto": "Escuela verde: Huerto escolar, compostaje y reciclaje creativo",
        "periodo_sugerido": "Semana 35 de 37 (Junio 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Junio",
        "año": 2027,
        "trimestre": 3,
        "descripcion": "Día Mundial del Medio Ambiente (5 de Junio), economía circular, composta, medición de cultivos.",
        "efemeride_principal": {
            "nombre": "Día Mundial del Medio Ambiente (5 de Junio)",
            "fecha": "5 de Junio",
            "anexo_nombre": "Anexo 35.5: Feria Escolar de Reciclaje Creativo y Cosecha Verde",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Día Mundial del Medio Ambiente (5 de Junio).",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Las 5 'R' de la Sustentabilidad: Reducir y Reutilizar",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 35.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 35.1 y libreta.",
                "anexo_nombre": "Anexo 35.1: Las 5 'R' de la Sustentabilidad: Reducir y Reutilizar",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Las 5 'R' de la Sustentabilidad: Reducir y Reutilizar."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Taller de Elaboración de Composta con Residuos del Aula",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 35.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 35.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 35.2: Taller de Elaboración de Composta con Residuos del Aula",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Taller de Elaboración de Composta con Residuos del Aula."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Redacción de Señalética Ecológica para el Huerto",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 35.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 35.4.",
                "anexo_nombre": "Anexo 35.4: Redacción de Señalética Ecológica para el Huerto",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Redacción de Señalética Ecológica para el Huerto."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Registro y Gráficas de Crecimiento de Hortalizas Escolares",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 35.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 35.3 y patio cívico.",
                "anexo_nombre": "Anexo 35.3: Registro y Gráficas de Crecimiento de Hortalizas Escolares",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 35.1: Las 5 'R' de la Sustentabilidad: Reducir y Reutilizar", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Las 5 'R' de la Sustentabilidad: Reducir y Reutilizar.", "tema": "Las 5 'R' de la Sustentabilidad: Reducir y Reutilizar", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 35.2: Taller de Elaboración de Composta con Residuos del Aula", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Taller de Elaboración de Composta con Residuos del Aula.", "tema": "Taller de Elaboración de Composta con Residuos del Aula", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 35.3: Registro y Gráficas de Crecimiento de Hortalizas Escolares", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Registro y Gráficas de Crecimiento de Hortalizas Escolares.", "tema": "Registro y Gráficas de Crecimiento de Hortalizas Escolares", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 35.4: Redacción de Señalética Ecológica para el Huerto", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Redacción de Señalética Ecológica para el Huerto.", "tema": "Redacción de Señalética Ecológica para el Huerto", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 35.5: Feria Escolar de Reciclaje Creativo y Cosecha Verde", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Feria Escolar de Reciclaje Creativo y Cosecha Verde.", "tema": "Feria Escolar de Reciclaje Creativo y Cosecha Verde", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. escuela (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    36: {
        "semana": 36,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 36 (Rumbo a la Secundaria: Proyecto de vida y orientación vocacional)",
        "titulo_proyecto": "Rumbo a la Secundaria: Proyecto de vida y orientación vocacional",
        "periodo_sugerido": "Semana 36 de 37 (Junio 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Junio",
        "año": 2027,
        "trimestre": 3,
        "descripcion": "Transición a la educación secundaria, mapa curricular, técnicas de estudio avanzado y gestión de emociones.",
        "efemeride_principal": {
            "nombre": "Semana de Orientación Educativa",
            "fecha": "Primeros días de Junio",
            "anexo_nombre": "Anexo 36.5: Carta a mi 'Yo del Futuro': Metas y Compromisos Personales",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Semana de Orientación Educativa.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Emociones, Retos y Expectativas ante el Egreso de Primaria",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 36.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 36.1 y libreta.",
                "anexo_nombre": "Anexo 36.1: Emociones, Retos y Expectativas ante el Egreso de Primaria",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Emociones, Retos y Expectativas ante el Egreso de Primaria."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Conocimiento de las Modalidades de Educación Secundaria",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 36.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 36.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 36.2: Conocimiento de las Modalidades de Educación Secundaria",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Conocimiento de las Modalidades de Educación Secundaria."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Resolución de Desafíos Matemáticos de Ingreso a Secundaria",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 36.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 36.4.",
                "anexo_nombre": "Anexo 36.4: Resolución de Desafíos Matemáticos de Ingreso a Secundaria",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Resolución de Desafíos Matemáticos de Ingreso a Secundaria."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Técnicas de Estudio Avanzado: Resumen, Cornell y Esquemas",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 36.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 36.3 y patio cívico.",
                "anexo_nombre": "Anexo 36.3: Técnicas de Estudio Avanzado: Resumen, Cornell y Esquemas",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 36.1: Emociones, Retos y Expectativas ante el Egreso de Primaria", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Emociones, Retos y Expectativas ante el Egreso de Primaria.", "tema": "Emociones, Retos y Expectativas ante el Egreso de Primaria", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 36.2: Conocimiento de las Modalidades de Educación Secundaria", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Conocimiento de las Modalidades de Educación Secundaria.", "tema": "Conocimiento de las Modalidades de Educación Secundaria", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 36.3: Técnicas de Estudio Avanzado: Resumen, Cornell y Esquemas", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Técnicas de Estudio Avanzado: Resumen, Cornell y Esquemas.", "tema": "Técnicas de Estudio Avanzado: Resumen, Cornell y Esquemas", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 36.4: Resolución de Desafíos Matemáticos de Ingreso a Secundaria", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Resolución de Desafíos Matemáticos de Ingreso a Secundaria.", "tema": "Resolución de Desafíos Matemáticos de Ingreso a Secundaria", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 36.5: Carta a mi 'Yo del Futuro': Metas y Compromisos Personales", "campo": "De lo Humano y lo Comunitario", "descripcion": "Ficha imprimible para Carta a mi 'Yo del Futuro': Metas y Compromisos Personales.", "tema": "Carta a mi 'Yo del Futuro': Metas y Compromisos Personales", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. rumbo (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
    37: {
        "semana": 37,
        "titulo_general": "Proyecto Pedagógico Integrador — Semana 37 (Memoria viva de nuestra primaria: Graduación y clausura 2026-2027)",
        "titulo_proyecto": "Memoria viva de nuestra primaria: Graduación y clausura 2026-2027",
        "periodo_sugerido": "Semana 37 de 37 (Junio 2027 - Ciclo 2026-2027)",
        "mes_correspondiente": "Junio",
        "año": 2027,
        "trimestre": 3,
        "descripcion": "Clausura de proyectos anuales, revista de generación de 6° 'A', discurso de egreso y 8ª Sesión CTE.",
        "efemeride_principal": {
            "nombre": "Clausura del Ciclo Escolar 2026-2027 y 8ª Sesión Ordinaria CTE",
            "fecha": "18 y 25 de Junio",
            "anexo_nombre": "Anexo 37.5: Asamblea Solemne de Clausura, Entrega de Diplomas y 8ª CTE",
            "anexo_descripcion": "Ficha didáctica y de análisis reflexivo vinculada a Clausura del Ciclo Escolar 2026-2027 y 8ª Sesión Ordinaria CTE.",
            "actividad": "Actividad integradora comunitaria: elaboración de producto cívico o evidencias de aprendizaje en asamblea de aula."
        },
        "campos": {
            "Lenguajes": {
                "tema": "Edición Final de la Revista de Generación de 6° 'A'",
                "pda_vinculado": "Aplica estrategias de lectura, redacción reflexiva, análisis crítico y expresión oral fundamentada en proyectos escolares.",
                "inicio": "Planteamiento de preguntas detonadoras y exploración de saberes previos con el grupo de 26 alumnos de 6° 'A'.",
                "desarrollo": "Lectura guiada, trabajo colaborativo en binas y resolución de la ficha del Anexo 37.1.",
                "cierre": "Puesta en común plenaria, síntesis colectiva y metacognición en el cuaderno de notas.",
                "recursos": "Libros de Texto Gratuitos (Proyectos de Aula / Escolares), Anexo 37.1 y libreta.",
                "anexo_nombre": "Anexo 37.1: Edición Final de la Revista de Generación de 6° 'A'",
                "anexo_descripcion": "Ficha imprimible para la práctica reflexiva de Edición Final de la Revista de Generación de 6° 'A'."
            },
            "Saberes y Pensamiento Científico": {
                "tema": "Estadísticas Finales de Aprendizaje y Logros Curriculares",
                "pda_vinculado": "Resuelve situaciones problemáticas vinculadas a su contexto mediante indagación científica, cálculo mental y modelos matemáticos.",
                "inicio": "Presentación de una situación problemática de la vida cotidiana en Durango para motivar la curiosidad científica.",
                "desarrollo": "Experimentación vivencial, análisis de datos y resolución práctica de ejercicios del Anexo 37.2.",
                "cierre": "Construcción de conclusiones científicas en el pizarrón y registro en la libreta.",
                "recursos": "Libro Nuestros Saberes, Anexo 37.2 y materiales concretos del aula.",
                "anexo_nombre": "Anexo 37.2: Estadísticas Finales de Aprendizaje y Logros Curriculares",
                "anexo_descripcion": "Ficha práctica de investigación y aplicación matemática para Estadísticas Finales de Aprendizaje y Logros Curriculares."
            },
            "Ética, Naturaleza y Sociedades": {
                "tema": "Exposición Plenaria de Productos de Intervención Comunitaria",
                "pda_vinculado": "Comprende la importancia de los derechos, la justicia social, la memoria histórica y la responsabilidad ciudadana en Durango.",
                "inicio": "Lluvia de ideas guiada sobre la convivencia ética y el contexto comunitario de Durango.",
                "desarrollo": "Análisis de casos prácticos, lectura de fuentes históricas y resolución del Anexo 37.4 en equipos.",
                "cierre": "Asamblea de aula para formular compromisos ciudadanos y normas compartidas.",
                "recursos": "Libro Cartografía de México o Múltiples Lenguajes, Anexo 37.4.",
                "anexo_nombre": "Anexo 37.4: Exposición Plenaria de Productos de Intervención Comunitaria",
                "anexo_descripcion": "Ficha de indagación comunitaria y análisis ético sobre Exposición Plenaria de Productos de Intervención Comunitaria."
            },
            "De lo Humano y lo Comunitario": {
                "tema": "Redacción y Ensayo del Discurso de Despedida Escolar",
                "pda_vinculado": "Promueve estilos de vida activos, convivencia pacífica, empatía y trabajo solidario en la escuela y la comunidad.",
                "inicio": "Dinámica activa de activación kinestésica y coordinación corporal en el aula o patio.",
                "desarrollo": "Desarrollo de dinámicas vivenciales y registro reflexivo en el Anexo 37.3.",
                "cierre": "Círculo de diálogo reflexivo sobre aprendizajes socioemocionales y acuerdos.",
                "recursos": "Materiales didácticos del aula, Anexo 37.3 y patio cívico.",
                "anexo_nombre": "Anexo 37.3: Redacción y Ensayo del Discurso de Despedida Escolar",
                "anexo_descripcion": "Ficha de registro de actividad vivencial y compromiso socioemocional."
            }
        },
        "anexos": [
            {"dia": "Lunes", "nombre": "Anexo 37.1: Edición Final de la Revista de Generación de 6° 'A'", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Edición Final de la Revista de Generación de 6° 'A'.", "tema": "Edición Final de la Revista de Generación de 6° 'A'", "actividad": "Actividad diagnóstica y formativa de inicio de semana."},
            {"dia": "Martes", "nombre": "Anexo 37.2: Estadísticas Finales de Aprendizaje y Logros Curriculares", "campo": "Saberes y Pensamiento Científico", "descripcion": "Ficha imprimible para Estadísticas Finales de Aprendizaje y Logros Curriculares.", "tema": "Estadísticas Finales de Aprendizaje y Logros Curriculares", "actividad": "Indagación científica y modelación matemática práctica."},
            {"dia": "Miércoles", "nombre": "Anexo 37.3: Redacción y Ensayo del Discurso de Despedida Escolar", "campo": "Lenguajes", "descripcion": "Ficha imprimible para Redacción y Ensayo del Discurso de Despedida Escolar.", "tema": "Redacción y Ensayo del Discurso de Despedida Escolar", "actividad": "Desarrollo socioemocional y vinculación comunitaria."},
            {"dia": "Jueves", "nombre": "Anexo 37.4: Exposición Plenaria de Productos de Intervención Comunitaria", "campo": "Ética, Naturaleza y Sociedades", "descripcion": "Ficha imprimible para Exposición Plenaria de Productos de Intervención Comunitaria.", "tema": "Exposición Plenaria de Productos de Intervención Comunitaria", "actividad": "Reflexión ética, cívica y memoria histórica."},
            {"dia": "Viernes", "nombre": "Anexo 37.5: Asamblea Solemne de Clausura, Entrega de Diplomas y 8ª CTE", "campo": "Conmemoración Cívica e Histórica", "descripcion": "Ficha imprimible para Asamblea Solemne de Clausura, Entrega de Diplomas y 8ª CTE.", "tema": "Asamblea Solemne de Clausura, Entrega de Diplomas y 8ª CTE", "actividad": "Síntesis integradora, producto semanal y evaluación formativa."}
        ],
        "rutinas_matutinas_sugeridas": {
            "dictado": [
                "1. memoria (reto ortográfico)",
                "2. comunidad (regla ortográfica)",
                "3. aprendizaje (grafía j/g)",
                "4. investigación (terminación -ción)",
                "5. colaboración (terminación -ción)"
            ],
            "calculo_mental": [
                "1. ¿El 25% de 200 es? (50)",
                "2. 12 x 8 = (96)",
                "3. Si un recorrido dura 45 min y han pasado 20 min, ¿cuánto falta? (25 min)",
                "4. 3.5 + 4.25 = (7.75)",
                "5. La mitad de 750 = (375)"
            ],
            "problemas_razonados": [
                "Problema 1: En la Primaria Revolución Social de 1910, los 26 alumnos de 6° 'A' recolectaron material para su proyecto semanal. Si cada uno aportó 4 piezas, ¿cuántas reunieron en total?",
                "Problema 2: En la cooperativa escolar se prepararon 130 porciones de fruta. Si se distribuyen equitativamente entre los 26 alumnos del grupo, ¿cuántas porciones recibe cada estudiante?"
            ]
        }
    },
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
    semana: Optional[Union[int, str]] = None,
    contenidos_pda: Optional[List[Dict[str, Any]]] = None,
    directrices_o_texto: str = "",
    campos: Optional[List[str]] = None
) -> bool:
    """
    Determina si los recursos de proyectos y anexos didácticos están disponibles y pertinentes.
    Para cualquier semana oficial (1 a 37) o coincidencia de palabras clave, retorna True.
    """
    try:
        if semana is not None:
            s_clean = int(str(semana).replace("Semana", "").strip())
            if 1 <= s_clean <= 37:
                return True
    except Exception:
        pass

    corpus_busqueda = (directrices_o_texto or "").lower()
    if contenidos_pda:
        for item in contenidos_pda:
            corpus_busqueda += " " + str(item.get("contenido", "")).lower()
            corpus_busqueda += " " + str(item.get("pda", "")).lower()
            corpus_busqueda += " " + str(item.get("campo", "")).lower()

    for kw in PALABRAS_CLAVE_KEMPIS:
        if kw in corpus_busqueda:
            return True

    return True


def obtener_proyecto_semana(semana: Union[int, str], mes: Optional[str] = None) -> Dict[str, Any]:
    """
    Retorna los metadatos completos del proyecto, tema curricular y anexos para la semana oficial SEP (1 a 37).
    Elimina cualquier valor quemado; si la semana está fuera de rango, la ajusta al intervalo [1, 37].
    Garantiza compatibilidad total con claves canónicas: 'proyecto', 'mes', 'rutinas_matutinas',
    'secuencias_por_dia' y 'anexos_por_dia'.
    """
    try:
        s_num = int(str(semana).replace("Semana", "").strip())
        s_num = max(1, min(37, s_num))
    except (ValueError, TypeError):
        s_num = 1

    base_data = CATALOGO_PROYECTOS_SEP_37_SEMANAS.get(s_num) or CATALOGO_PROYECTOS_SEP_37_SEMANAS[1]
    data = dict(base_data)

    data["proyecto"] = data.get("titulo_proyecto") or data.get("titulo_general", f"Proyecto Semana {s_num}")
    data["mes"] = data.get("mes_correspondiente") or mes or "Octubre"
    data["fase_metodologica"] = data.get("fase_metodologica") or "Proyecto Integrador Comunitario"

    anexos = data.get("anexos", [])
    data["anexos_por_dia"] = {a["dia"]: a["nombre"] for a in anexos if "dia" in a and "nombre" in a}

    r_sug = data.get("rutinas_matutinas_sugeridas", {})
    dictados_list = r_sug.get("dictado", [])
    calc_list = r_sug.get("calculo_mental", [])
    prob_list = r_sug.get("problemas_razonados", [])
    dias_h = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    r_dict_map = {d: dictados_list[i % len(dictados_list)] if dictados_list else f"Palabras clave para {d}." for i, d in enumerate(dias_h)}
    r_calc_map = {d: calc_list[i % len(calc_list)] if calc_list else f"Cálculo mental para {d}." for i, d in enumerate(dias_h)}
    r_prob_map = {d: prob_list[i % len(prob_list)] if prob_list else f"Problema razonado para {d}." for i, d in enumerate(dias_h)}

    data["rutinas_matutinas"] = {
        "dictado": r_dict_map,
        "calculo_mental": r_calc_map,
        "problemas_razonados": r_prob_map
    }

    data["secuencias_por_dia"] = {
        a["dia"]: {
            "inicio": f"Activación colectiva y recuperación de saberes para {a.get('tema', data['proyecto'])}.",
            "desarrollo": a.get("actividad", f"Indagación práctica y aplicación de {a.get('nombre')}."),
            "cierre": "Puesta en común, balance de avances y evaluación formativa en asamblea.",
            "recursos": f"Libros de Texto Gratuitos (LTG), {a.get('nombre')} y libreta del alumno."
        }
        for a in anexos if "dia" in a
    }

    return data


def obtener_anexos_por_semana_y_dia(semana: Union[int, str], dia: Optional[str] = None, mes: Optional[str] = None) -> Any:
    """
    Retorna los anexos correspondientes a la semana oficial (1 a 37).
    Si se especifica el día (Lunes, Martes, Miércoles, Jueves, Viernes), devuelve el nombre exacto
    del anexo de ese día. Si dia es None, devuelve la lista completa de anexos de la semana.
    """
    proyecto_data = obtener_proyecto_semana(semana, mes=mes)
    anexos = proyecto_data.get("anexos", [])
    if dia and str(dia).strip():
        dia_norm = str(dia).strip().capitalize()
        for a in anexos:
            if a.get("dia", "").capitalize() == dia_norm:
                return a.get("nombre", "")
        return f"Anexo de {dia_norm} (Semana {proyecto_data.get('semana', semana)})"
    return anexos


def obtener_recursos_kempis_por_semana(semana: Union[int, str]) -> Optional[Dict[str, Any]]:
    """
    Devuelve los metadatos del proyecto y anexos didácticos para la semana solicitada (1 a 37).
    """
    try:
        s_num = int(str(semana).replace("Semana", "").strip())
        if 1 <= s_num <= 37:
            return CATALOGO_PROYECTOS_SEP_37_SEMANAS.get(s_num)
    except (ValueError, TypeError):
        pass
    return CATALOGO_PROYECTOS_SEP_37_SEMANAS.get(1)


def formatear_kempis_para_prompt(
    semana: Union[int, str],
    campos_formativos: Optional[List[str]] = None,
    dias_seleccionados: Optional[List[str]] = None,
    mes: Optional[str] = None,
    año: int = 2026
) -> str:
    """
    Genera un bloque de texto estructurado para inyectar como directriz obligatoria en el prompt de Gemini.
    Cruza el día de la semana específico con el proyecto y los anexos de la semana exacta (1 a 37).
    """
    data = obtener_proyecto_semana(semana)
    sem_num = data["semana"]
    mes_str = mes or data.get("mes_correspondiente", "Octubre")
    año_num = año or data.get("año", 2026)
    dias_activos = dias_seleccionados or ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

    lineas = [
        f"=== PROYECTO DIDÁCTICO INTEGRADOR Y ANEXOS IMPRIMIBLES (SEMANA {sem_num} DE 37 — {mes_str.upper()} {año_num}) ===",
        f"La planeación didáctica DEBE estructurarse e incorporar obligatoriamente el proyecto y los anexos de esta semana exacta:",
        f"- Proyecto Oficial: {data.get('titulo_proyecto', data.get('titulo_general', ''))}",
        f"- Temporalidad: Semana {sem_num} de 37 del Ciclo Escolar 2026-2027 (Mes: {mes_str} {año_num})",
        f"- Propósito / Enfoque: {data.get('descripcion', '')}",
        f"- Efeméride vinculada: {data['efemeride_principal']['nombre']} ({data['efemeride_principal']['fecha']}) -> {data['efemeride_principal']['actividad']}",
        "",
        "CRUCE OBLIGATORIO DÍA POR DÍA CON EL PROYECTO Y SUS ANEXOS:"
    ]

    anexos_semana = data.get("anexos", [])
    anexos_por_dia = {a.get("dia"): a for a in anexos_semana if a.get("dia")}

    for dia_nom in dias_activos:
        anexo_info = anexos_por_dia.get(dia_nom)
        if anexo_info:
            lineas.append(f"• Día {dia_nom}:")
            lineas.append(f"  - Momento/Tema: {anexo_info.get('tema', anexo_info.get('nombre'))}")
            lineas.append(f"  - Anexo Imprimible asignado: {anexo_info.get('nombre')} ({anexo_info.get('descripcion')})")
            lineas.append(f"  - Campo formativo rector: {anexo_info.get('campo', 'Lenguajes')}")
            lineas.append(f"  - Actividad vinculada: {anexo_info.get('actividad', '')}")
            lineas.append("")

    campos = campos_formativos or ["Lenguajes", "Saberes y Pensamiento Científico", "Ética, Naturaleza y Sociedades", "De lo Humano y lo Comunitario"]
    lineas.append("DESGLOSE CURRICULAR POR CAMPOS FORMATIVOS PARA ESTA SEMANA:")
    for cf in campos:
        if cf in data.get("campos", {}):
            c_info = data["campos"][cf]
            lineas.append(f"• Campo Formativo: {cf}")
            lineas.append(f"  - Tema: {c_info['tema']}")
            lineas.append(f"  - PDA Vinculado: {c_info.get('pda_vinculado', '')}")
            lineas.append(f"  - Inicio sugerido: {c_info['inicio']}")
            lineas.append(f"  - Desarrollo sugerido: {c_info['desarrollo']}")
            lineas.append(f"  - Cierre sugerido: {c_info['cierre']}")
            lineas.append(f"  - Anexo del campo: {c_info.get('anexo_nombre', '')}")
            lineas.append("")

    rutinas = data.get("rutinas_matutinas_sugeridas", {})
    if rutinas:
        lineas.append("RUTINAS MATUTINAS OFICIALES SUGERIDAS:")
        lineas.append(f"- Dictado Ortográfico: {', '.join(rutinas.get('dictado', [])[:3])}")
        lineas.append(f"- Cálculo Mental: {', '.join(rutinas.get('calculo_mental', [])[:2])}")
        if rutinas.get("problemas_razonados"):
            lineas.append(f"- Problema Razonado: {rutinas['problemas_razonados'][0]}")
        lineas.append("")

    lineas.append("REGLA MANDATORIA DE CITA: En la columna de 'Recursos didácticos y materiales' y en el Desarrollo de cada sesión didáctica, cita obligatoriamente el Anexo correspondiente al día (ejemplo: 'Anexo X.Y' y fichas de trabajo del proyecto).")
    lineas.append("================================================================================")

    return "\n".join(lineas)


def obtener_anexos_kempis_para_docx(semana: Union[int, str]) -> List[Dict[str, Any]]:
    """
    Retorna la lista de anexos imprimibles y fichas de trabajo del proyecto para incrustar en Word (.docx).
    Garantiza que cualquier semana (1 a 37) proporcione sus anexos oficiales correspondientes.
    """
    proyecto_data = obtener_proyecto_semana(semana)
    anexos_raw = proyecto_data.get("anexos", [])
    if anexos_raw:
        return anexos_raw

    # Fallback si no tiene lista de anexos
    anexos = []
    for campo_nom, c_data in proyecto_data.get("campos", {}).items():
        anexos.append({
            "campo": campo_nom,
            "nombre": c_data.get("anexo_nombre", f"Anexo de {campo_nom}"),
            "descripcion": c_data.get("anexo_descripcion", ""),
            "tema": c_data.get("tema", ""),
            "actividad": c_data.get("desarrollo", "")
        })

    ef = proyecto_data.get("efemeride_principal", {})
    if ef:
        anexos.append({
            "campo": "Conmemoración Cívica e Histórica",
            "nombre": ef.get("anexo_nombre", "Anexo Cívico"),
            "descripcion": ef.get("anexo_descripcion", ""),
            "tema": ef.get("nombre", ""),
            "actividad": ef.get("actividad", "")
        })

    return anexos


# ==========================================
# ALIASES Y COMPATIBILIDAD DE EXPORTACIÓN
# ==========================================
obtener_kempis_por_semana = obtener_recursos_kempis_por_semana
obtener_anexos_kempis = obtener_anexos_kempis_para_docx
obtener_anexos_semana = obtener_anexos_por_semana_y_dia
obtener_proyecto = obtener_proyecto_semana
formatear_kempis = formatear_kempis_para_prompt
formatear_directrices_kempis = formatear_kempis_para_prompt
detectar_kempis = detectar_relevancia_kempis

# Exportaciones oficiales del módulo
__all__ = [
    # Diccionarios y Catálogos principales
    "CUADERNILLO_KEMPIS_DATA",
    "CATALOGO_PROYECTOS_SEP_37_SEMANAS",
    "PALABRAS_CLAVE_KEMPIS",
    # Funciones de consulta, filtrado y generación
    "detectar_relevancia_kempis",
    "obtener_recursos_kempis_por_semana",
    "obtener_proyecto_semana",
    "obtener_anexos_por_semana_y_dia",
    "formatear_kempis_para_prompt",
    "obtener_anexos_kempis_para_docx",
    # Aliases de compatibilidad
    "obtener_kempis_por_semana",
    "obtener_anexos_kempis",
    "obtener_anexos_semana",
    "obtener_proyecto",
    "formatear_kempis",
    "formatear_directrices_kempis",
    "detectar_kempis",
]
