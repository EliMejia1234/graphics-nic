import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # We don't draw running header on page 1 (cover)
        if self._pageNumber > 1:
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(40, letter[1] - 40, letter[0] - 40, letter[1] - 40)
            self.drawString(40, letter[1] - 34, "Centro Cultural y Tecnológico José Coronel Urtecho · INATEC")
            self.drawRightString(letter[0] - 40, letter[1] - 34, "Propuesta Institucional: Graphics Nic")

        # Running footer on all pages
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(40, 42, letter[0] - 40, 42)
        
        self.drawString(40, 30, "Documento Oficial de Propuesta Institucional · Talento Creativo Urtecho")
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(letter[0] - 40, 30, page_str)
        self.restoreState()

def create_proposal_pdf(output_filename="propuesta_institucional_graphics_nic.pdf"):
    # Page setup: letter size = 612 x 792 pt
    # Margins: 38 pt left/right (~0.53 inch), 48 pt top/bottom
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=38,
        rightMargin=38,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    # Primary colors
    c_primary = colors.HexColor("#1e1b4b")   # Deep Indigo
    c_accent = colors.HexColor("#4f46e5")    # Indigo Accent
    c_dark = colors.HexColor("#0f172a")      # Slate 900
    c_body = colors.HexColor("#334155")      # Slate 700
    c_sub = colors.HexColor("#64748b")       # Slate 500
    c_bg_light = colors.HexColor("#f8fafc")  # Slate 50
    c_border = colors.HexColor("#e2e8f0")    # Slate 200

    title_inst = ParagraphStyle(
        'InstTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=c_primary,
        textTransform='uppercase'
    )
    
    sub_inst = ParagraphStyle(
        'InstSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=c_accent
    )
    
    tag_inst = ParagraphStyle(
        'InstTag',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=c_sub
    )

    badge_style = ParagraphStyle(
        'DocBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#3730a3"),
        alignment=2 # Right
    )

    h1_hero = ParagraphStyle(
        'HeroTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=colors.white
    )

    p_hero = ParagraphStyle(
        'HeroDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#e0e7ff")
    )

    tag_hero = ParagraphStyle(
        'HeroTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#a5b4fc"),
        textTransform='uppercase'
    )

    meta_lbl = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9,
        textColor=c_accent,
        textTransform='uppercase'
    )

    meta_val = ParagraphStyle(
        'MetaValue',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=c_dark
    )

    meta_sub = ParagraphStyle(
        'MetaSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=c_body
    )

    sec_title = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=4,
        textTransform='uppercase'
    )

    body_p = ParagraphStyle(
        'BodyP',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=c_body,
        alignment=4 # Justify
    )

    box_title_danger = ParagraphStyle(
        'BoxTitleDanger',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#991b1b")
    )

    box_title_success = ParagraphStyle(
        'BoxTitleSuccess',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.HexColor("#166534")
    )

    box_p = ParagraphStyle(
        'BoxP',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=c_body
    )

    tbl_head = ParagraphStyle(
        'TblHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    tbl_cell = ParagraphStyle(
        'TblCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=c_body
    )

    tbl_cell_bold = ParagraphStyle(
        'TblCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=c_dark
    )

    story = []

    usable_width = 612 - 76 # 536 pt

    # ==================== PAGE 1 ====================
    # 1. Header with Logo & Institution
    logo_path = "img/inatec_tecnologico_nacional.png"
    img = Image(logo_path, width=1.4*inch, height=0.7*inch)

    inst_text = Paragraph(
        "<b>CENTRO CULTURAL Y TECNOLÓGICO JOSÉ CORONEL URTECHO</b><br/>"
        "<font color='#4f46e5'><b>Instituto Nacional Tecnológico (INATEC) · GRUN</b></font><br/>"
        "<font color='#64748b'>Especialidad de Diseño Gráfico · Área de Innovación y Vinculación</font>",
        inst_text_style := ParagraphStyle(
            'InstHeader',
            fontName='Helvetica',
            fontSize=8,
            leading=11,
            textColor=c_dark
        )
    )

    badge_cell = Paragraph(
        "<b>PROPUESTA DE INNOVACIÓN</b><br/>"
        "<font color='#64748b'>Fecha: Octubre 2026</font><br/>"
        "<font color='#4f46e5'><b>Versión Ejecutiva Oficial</b></font>",
        badge_style
    )

    hdr_table = Table(
        [[img, inst_text, badge_cell]],
        colWidths=[1.5*inch, 4.3*inch, 1.6*inch]
    )
    hdr_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(hdr_table)
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=4, spaceAfter=8))

    # 2. Hero Box
    hero_inner = [
        [Paragraph("✦ INICIATIVA INSTITUCIONAL · TALENTO CREATIVO URTECHO", tag_hero)],
        [Paragraph("Plataforma Web de Empleabilidad: <i>Graphics Nic</i>", h1_hero)],
        [Paragraph(
            "Una solución tecnológica institucional, para proyectar "
            "profesionalmente a técnicos egresados de la carrera en Diseño Gráfico, "
            "impartida en el centro José Coronel Urtecho con el fin de conectarlos con empresas "
            "y clientes que buscan servicios de diseño especializado.",
            p_hero
        )]
    ]
    hero_table = Table(hero_inner, colWidths=[usable_width])
    hero_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#1e1b4b")),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(hero_table)
    story.append(Spacer(1, 8))

    # 3. Metadata Presentation Cards
    meta_left = [
        Paragraph("DIRIGIDO A", meta_lbl),
        Paragraph("Cra. Alexandra López Quintanilla", meta_val),
        Paragraph("Subdirectora Técnico Docente<br/>Centro Cultural y Tecnológico José Coronel Urtecho · INATEC", meta_sub)
    ]
    meta_right = [
        Paragraph("ELABORADO POR", meta_lbl),
        Paragraph("Cro. Eli Francisco Mejia Ponce", meta_val),
        Paragraph("Docente de la Especialidad Diseño Gráfico y Desarrollo de Software<br/>Iniciativa de Innovación Tecnológica Educativa", meta_sub)
    ]
    meta_table = Table([[meta_left, meta_right]], colWidths=[usable_width/2 - 4, usable_width/2 - 4])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('INNERGRID', (0,0), (-1,-1), 8, colors.white),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 6))

    # 4. Resumen Ejecutivo
    story.append(Paragraph("1. Resumen Ejecutivo y Contexto Institucional", sec_title))
    story.append(Paragraph(
        "El <b>Centro Cultural y Tecnológico José Coronel Urtecho</b> forma técnicos profesionales de alto nivel en "
        "la especialidad de <b>Diseño Gráfico</b>, desarrollando competencias creativas, comunicacionales y técnicas de gran valor para la economía nacional. "
        "Sin embargo, el paso de la formación académica al ejercicio laboral y productivo presenta un desafío común: la falta de una vitrina "
        "oficial y centralizada donde empresas, instituciones y clientes puedan explorar de manera ágil los perfiles y proyectos de los talentos egresados.",
        body_p
    ))
    story.append(Paragraph(
        "La presente propuesta plantea la creación de <b>Graphics Nic</b>, una plataforma web oficial y moderna orientada a la <b>empleabilidad, "
        "el emprendimiento y la proyección profesional</b> de nuestros estudiantes. Esta herramienta se alinea directamente con la misión del <b>INATEC</b> "
        "de transformar la educación técnica en bienestar, desarrollo comunitario e inserción laboral efectiva, fortaleciendo el rol del Centro como motor de innovación.",
        body_p
    ))
    story.append(Spacer(1, 4))

    # 5. El Reto vs La Solución
    story.append(Paragraph("2. Diagnóstico del Reto y Solución Propuesta", sec_title))
    col_reto = [
        Paragraph("El Reto Actual (Diagnóstico)", box_title_danger),
        Spacer(1, 2),
        Paragraph("• <b>Dispersión de obras:</b> Los proyectos estudiantiles quedan dispersos en carpetas personales, redes sociales o archivos académicos sin catalogación.", box_p),
        Paragraph("• <b>Baja visibilidad laboral:</b> El descubrimiento de nuevos diseñadores depende de recomendaciones informales o contactos individuales aislados.", box_p),
        Paragraph("• <b>Falta de puente directo:</b> No existe un canal institucional central que comunique la oferta de talento del Centro con la demanda del sector productivo.", box_p),
    ]
    col_solucion = [
        Paragraph("La Solución al Reto Planteado (Graphics Nic)", box_title_success),
        Spacer(1, 2),
        Paragraph("• <b>Vitrina centralizada oficial:</b> Espacio digital institucional con perfiles y portafolios organizados, desde donde las personas interesadas puedan descubrir los trabajos que han realizado los estudiantes y egresados de la carrera en Diseño Gráfico.", box_p),
        Paragraph("• <b>Navegación por especialidad:</b> Búsqueda ágil y categorizada para que clientes encuentren exactamente el perfil requerido (branding, editorial, empaques).", box_p),
        Paragraph("• <b>Canal de contacto concertado:</b> Vínculo transparente y profesional que facilita contrataciones formales y alianzas con empresas y MIPYMES.", box_p),
    ]

    reto_sol_table = Table([[col_reto, col_solucion]], colWidths=[usable_width/2 - 4, usable_width/2 - 4])
    reto_sol_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#fef2f2")),
        ('BOX', (0,0), (0,0), 0.75, colors.HexColor("#fecaca")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#f0fdf4")),
        ('BOX', (1,0), (1,0), 0.75, colors.HexColor("#bbf7d0")),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(reto_sol_table)

    # ==================== PAGE 2 ====================
    story.append(PageBreak())

    # Section 3: Modelo Operativo de Funcionamiento
    story.append(Paragraph("3. Modelo Operativo de Funcionamiento (4 Pilares)", sec_title))
    story.append(Paragraph(
        "La plataforma se concibe como una vitrina fácil de recorrer, donde cada perfil presentará el trabajo creativo, "
        "y las personas interesadas pueden encontrar talento según sus necesidades:",
        body_p
    ))
    story.append(Spacer(1, 4))

    p1 = [
        Paragraph("<b>01 · Perfil y Portafolio Curado</b>", ParagraphStyle('P1', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_primary)),
        Spacer(1, 2),
        Paragraph("El estudiante o egresado presentará su portafolio con sus mejores proyectos, sus especialidades y enlaces profesionales.", box_p)
    ]
    p2 = [
        Paragraph("<b>02 · Exploración y Filtro por Áreas</b>", ParagraphStyle('P2', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_primary)),
        Spacer(1, 2),
        Paragraph("Empresas, emprendedores y organismos recorren el catálogo filtrando por especialidades (redes, empaques, ilustración, editorial). Esto permite evaluar directamente piezas reales de trabajo adaptadas a la necesidad de su negocio.", box_p)
    ]
    p3 = [
        Paragraph("<b>03 · Vinculación y Contacto Responsable</b>", ParagraphStyle('P3', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_primary)),
        Spacer(1, 2),
        Paragraph("La plataforma contará con un enlace para que los interesados puedan contactar a los estudiantes o egresados de forma directa y autorizada.", box_p)
    ]
    p4 = [
        Paragraph("<b>04 · Métricas y Seguimiento Institucional</b>", ParagraphStyle('P4', fontName='Helvetica-Bold', fontSize=8.5, textColor=c_primary)),
        Spacer(1, 2),
        Paragraph("Módulo de analítica institucional que recopila métricas agregadas: volumen de visitas, proyectos más consultados y solicitudes canalizadas, facilitando al cuerpo docente la retroalimentación continua del plan formativo.", box_p)
    ]

    pillars_table = Table([[p1, p2], [p3, p4]], colWidths=[usable_width/2 - 4, usable_width/2 - 4])
    pillars_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('INNERGRID', (0,0), (-1,-1), 6, colors.white),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(pillars_table)
    story.append(Spacer(1, 8))

    # Section 4: Especialidades Técnicas Contempladas
    story.append(Paragraph("4. Áreas de Especialidad y Aplicaciones en el Mercado", sec_title))
    story.append(Paragraph(
        "Las instituciones podrán revisar los servicios y especialidades de cada egresado, con paneles como los que se detallan a continuación:",
        body_p
    ))
    story.append(Spacer(1, 3))

    spec_data = [
        [
            Paragraph("Especialidad", tbl_head),
            Paragraph("Competencias y Alcance Formativo", tbl_head),
            Paragraph("Aplicación y Valor Comercial", tbl_head)
        ],
        [
            Paragraph("<b>Redes e Identidad Digital</b><br/><font color='#6366f1'>Branding & Social Media</font>", tbl_cell_bold),
            Paragraph("Creación de identidades visuales completas, manuales de marca, diseño de publicaciones para redes sociales y piezas de pauta digital.", tbl_cell),
            Paragraph("Permite a MIPYMES y emprendedores modernizar su imagen comercial y captar clientes en entornos digitales.", tbl_cell)
        ],
        [
            Paragraph("<b>Packaging y Empaques</b><br/><font color='#0d9488'>Diseño de Empaques</font>", tbl_cell_bold),
            Paragraph("Diseño estructural y gráfico de etiquetas, cajas, envases y mockups 3D con cumplimiento de normativas de rotulado.", tbl_cell),
            Paragraph("Agrega valor competitivo e identidad visual a productos de productores nacionales, artesanías y alimentos procesados.", tbl_cell)
        ],
        [
            Paragraph("<b>Ilustración Creativa</b><br/><font color='#d97706'>Arte & Concepto Visual</font>", tbl_cell_bold),
            Paragraph("Desarrollo de arte conceptual, ilustración vectorial, infografías pedagógicas y narrativa visual para diversos soportes.", tbl_cell),
            Paragraph("Aporte distintivo para campañas de comunicación institucional, libros educativos, afiches y proyectos culturales.", tbl_cell)
        ],
        [
            Paragraph("<b>Revistas y Publicaciones</b><br/><font color='#7c3aed'>Diseño Editorial</font>", tbl_cell_bold),
            Paragraph("Maquetación tipográfica avanzada, diagramación de memorias institucionales, catálogos comerciales y revistas digitales.", tbl_cell),
            Paragraph("Servicio altamente demandado por ministerios, organismos gubernamentales, editoriales y corporaciones.", tbl_cell)
        ]
    ]

    spec_table = Table(spec_data, colWidths=[1.6*inch, 3.2*inch, 2.6*inch])
    spec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
    ]))
    story.append(spec_table)
    story.append(Spacer(1, 8))

    # Section 5: Matriz de Beneficios
    story.append(Paragraph("5. Matriz de Impacto y Beneficios Compartidos", sec_title))
    beneficios_data = [
        [
            Paragraph("Estudiantes y Egresados", tbl_head),
            Paragraph("Empresas y Clientes", tbl_head),
            Paragraph("Centro Cultural y Tecnológico (INATEC)", tbl_head)
        ],
        [
            Paragraph(
                "• Vitrina formal avalada institucionalmente.<br/>"
                "• Enlace directo a portafolio profesional para CV.<br/>"
                "• Oportunidades reales de empleo y contratos freelance.<br/>"
                "• Estímulo permanente a la excelencia en las aulas.",
                tbl_cell
            ),
            Paragraph(
                "• Acceso inmediato a un catálogo verificado de creadores.<br/>"
                "• Reducción de tiempos y costos en reclutamiento.<br/>"
                "• Visualización de muestras de trabajo antes de contactar.<br/>"
                "• Apoyo directo a la economía y al talento joven nicaragüense.",
                tbl_cell
            ),
            Paragraph(
                "• Evidencia tangible de los resultados formativos del Centro.<br/>"
                "• Fortalecimiento del vínculo con el sector productivo nacional.<br/>"
                "• Trazabilidad y seguimiento del impacto de los egresados.<br/>"
                "• Posicionamiento como centro referente en educación e innovación.",
                tbl_cell
            )
        ]
    ]
    beneficios_table = Table(beneficios_data, colWidths=[usable_width/3, usable_width/3, usable_width/3])
    beneficios_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#312e81")),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('INNERGRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,1), (-1,1), c_bg_light),
    ]))
    story.append(beneficios_table)

    # ==================== PAGE 3 ====================
    story.append(PageBreak())

    # Section 6: Plan de Implementación
    story.append(Paragraph("6. Ruta Metodológica de Implementación (Fase Piloto)", sec_title))
    story.append(Paragraph(
        "Con el fin de asegurar una ejecución ordenada, controlada y validada por las autoridades académicas, "
        "se propone una ruta de tres etapas progresivas:",
        body_p
    ))
    story.append(Spacer(1, 4))

    fase1 = [
        Paragraph("<b>FASE 1: PREPARACIÓN</b><br/><font color='#4f46e5'><b>Semanas 1 a 3</b></font>", ParagraphStyle('F1', fontName='Helvetica-Bold', fontSize=8, textColor=c_primary)),
        Spacer(1, 2),
        Paragraph("• Sesiones de coordinación con la Subdirección Técnico Docente.<br/>"
                  "• Establecimiento de criterios de selección de obras y estándares visuales.<br/>"
                  "• Levantamiento de firmas de consentimiento informado y autorización de publicación.<br/>"
                  "• Homologación de formatos de ficha y datos de contacto.", box_p)
    ]
    fase2 = [
        Paragraph("<b>FASE 2: PILOTO Y MONTAJE</b><br/><font color='#0d9488'><b>Semanas 4 a 7</b></font>", ParagraphStyle('F2', fontName='Helvetica-Bold', fontSize=8, textColor=c_primary)),
        Spacer(1, 2),
        Paragraph("• Integración de una cohorte piloto inicial de 15 a 25 portafolios destacados.<br/>"
                  "• Curaduría y carga de material gráfico en alta fidelidad.<br/>"
                  "• Pruebas técnicas de velocidad de carga, diseño responsivo y compatibilidad móvil.<br/>"
                  "• Sesión interna de validación con los docentes del área gráfica.", box_p)
    ]
    fase3 = [
        Paragraph("<b>FASE 3: DIFUSIÓN Y EVALUACIÓN</b><br/><font color='#d97706'><b>Semanas 8 a 10</b></font>", ParagraphStyle('F3', fontName='Helvetica-Bold', fontSize=8, textColor=c_primary)),
        Spacer(1, 2),
        Paragraph("• Presentación de la vitrina ante empresas aliadas, cámaras y emprendedores.<br/>"
                  "• Medición del tráfico web, solicitudes de información y oportunidades generadas.<br/>"
                  "• Elaboración de informe ejecutivo de impacto para la Subdirección.<br/>"
                  "• Definición de mecanismos para incorporar a futuras promociones.", box_p)
    ]

    fases_table = Table([[fase1, fase2, fase3]], colWidths=[usable_width/3 - 4, usable_width/3 - 4, usable_width/3 - 4])
    fases_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_bg_light),
        ('BOX', (0,0), (-1,-1), 0.75, c_border),
        ('INNERGRID', (0,0), (-1,-1), 6, colors.white),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(fases_table)
    story.append(Spacer(1, 8))

    # Section 7: Factibilidad y Seguridad
    story.append(Paragraph("7. Viabilidad Técnica, Legal y de Recursos", sec_title))
    fact_p1 = Paragraph(
        "<b>Viabilidad Técnica:</b> La plataforma ha sido diseñada bajo estándares web modernos, ligeros y de código abierto "
        "(HTML5 semántico, CSS3 responsivo y JavaScript puro). No requiere licencias propietarias ni infraestructura compleja de servidores, "
        "garantizando un despliegue inmediato con costos operativos nulos para la institución.",
        body_p
    )
    fact_p2 = Paragraph(
        "<b>Seguridad y Propiedad Intelectual:</b> Cada estudiante conserva la autoría inalienable de sus proyectos. La plataforma actúa como "
        "canal de difusión institucional con el debido consentimiento firmado. Asimismo, se promueven canales de contacto directos "
        "sin almacenamiento de información bancaria ni intermediación monetaria en la web.",
        body_p
    )
    story.append(fact_p1)
    story.append(Spacer(1, 3))
    story.append(fact_p2)
    story.append(Spacer(1, 8))

    # Section 8: Solicitud de Valoración
    story.append(Paragraph("8. Solicitud de Valoración y Acuerdos para Inicio", sec_title))
    story.append(Paragraph(
        "Habiendo fundamentado el valor social, pedagógico e institucional del proyecto, se somete cordialmente a consideración de la "
        "<b>Subdirección Técnico Docente</b> la aprobación de <b>Graphics Nic</b> para dar inicio formal a la <b>Fase 1 (Preparación y Criterios)</b>. "
        "Agradezco de antemano el respaldo institucional para hacer de esta iniciativa una realidad que potencie el talento de nuestra juventud creativa.",
        body_p
    ))
    story.append(Spacer(1, 35))

    # Signatures Table
    sign_p_eli = [
        Paragraph("____________________________________________", ParagraphStyle('Line1', fontName='Helvetica', fontSize=9, alignment=1, textColor=c_dark)),
        Spacer(1, 3),
        Paragraph("<b>Cro. Eli Francisco Mejia Ponce</b>", ParagraphStyle('Name1', fontName='Helvetica-Bold', fontSize=8.5, alignment=1, textColor=c_dark)),
        Paragraph("Docente de la Especialidad Diseño Gráfico y Desarrollo de Software<br/>Proponente de la Iniciativa Tecnológica", ParagraphStyle('Cargo1', fontName='Helvetica', fontSize=7.5, leading=9.5, alignment=1, textColor=c_sub))
    ]

    sign_p_alexandra = [
        Paragraph("____________________________________________", ParagraphStyle('Line2', fontName='Helvetica', fontSize=9, alignment=1, textColor=c_dark)),
        Spacer(1, 3),
        Paragraph("<b>Cra. Alexandra López Quintanilla</b>", ParagraphStyle('Name2', fontName='Helvetica-Bold', fontSize=8.5, alignment=1, textColor=c_dark)),
        Paragraph("Subdirectora Técnico Docente<br/>Centro Cultural y Tecnológico José Coronel Urtecho · INATEC", ParagraphStyle('Cargo2', fontName='Helvetica', fontSize=7.5, leading=9.5, alignment=1, textColor=c_sub))
    ]

    signs_table = Table([[sign_p_eli, sign_p_alexandra]], colWidths=[usable_width/2, usable_width/2])
    signs_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    
    story.append(signs_table)

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully built: {output_filename}")

if __name__ == "__main__":
    create_proposal_pdf()
