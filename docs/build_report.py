from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "informe_automataspaint.pdf"
DIAGRAMS = ROOT / "docs" / "diagrams"


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(HexColor("#52616b"))
    canvas.drawString(2 * cm, 1.25 * cm, "AutomatasPaint - Informe tecnico")
    canvas.drawRightString(A4[0] - 2 * cm, 1.25 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=1.8*cm, bottomMargin=1.9*cm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=23, leading=28, textColor=HexColor("#102a43"), spaceAfter=14))
    styles.add(ParagraphStyle(name="Heading", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=HexColor("#102a43"), spaceBefore=12, spaceAfter=7))
    styles.add(ParagraphStyle(name="Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.5, leading=15, spaceAfter=7))
    story = []
    story += [Paragraph("Informe tecnico AutomatasPaint", styles["TitleCustom"]),
              Paragraph("Aplicacion de escritorio para construir, visualizar, convertir y probar automatas finitos deterministas y no deterministas.", styles["Body"]),
              Paragraph("Objetivo", styles["Heading"]),
              Paragraph("AutomatasPaint resuelve la construccion interactiva de AFD y AFN en una interfaz grafica Python. El usuario configura el alfabeto, los estados y la tabla de transiciones, observa el diagrama resultante y comprueba si una cadena es aceptada.", styles["Body"]),
              Paragraph("Alcance funcional", styles["Heading"])]
    data = [["Funcion", "Implementacion"],
            ["Definicion", "Campos para alfabeto, estados, estado inicial y estados de aceptacion."],
            ["Tabla", "Tabla dinamica; los destinos multiples y epsilon estan disponibles para AFN."],
            ["Conversion", "Construccion por subconjuntos con clausura epsilon para convertir AFN a AFD."],
            ["Validacion", "Verifica estados, simbolos y restricciones de determinismo antes de operar."],
            ["Simulacion", "Procesa la cadena simbolo a simbolo, informa aceptacion y resalta estados activos."],
            ["Visualizacion", "Lienzo tipo Paint con estados, transiciones, flecha inicial y dobles circulos finales."]]
    table = Table(data, colWidths=[3.4*cm, 12.4*cm], repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,0), HexColor("#243b53")), ("TEXTCOLOR", (0,0), (-1,0), HexColor("#ffffff")), ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), ("FONTNAME", (0,1), (-1,-1), "Helvetica"), ("FONTSIZE", (0,0), (-1,-1), 9), ("LEADING", (0,0), (-1,-1), 12), ("GRID", (0,0), (-1,-1), .4, HexColor("#d9d9d9")), ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("BACKGROUND", (0,1), (-1,-1), HexColor("#f7fafc")), ("ROWBACKGROUNDS", (0,1), (-1,-1), [HexColor("#ffffff"), HexColor("#edf2f7")]), ("TOPPADDING", (0,0), (-1,-1), 7), ("BOTTOMPADDING", (0,0), (-1,-1), 7), ("LEFTPADDING", (0,0), (-1,-1), 7), ("RIGHTPADDING", (0,0), (-1,-1), 7)]))
    story += [table, Paragraph("Diseno", styles["Heading"]), Paragraph("El nucleo es la clase Automaton. Esta concentra las transiciones, la validacion, la simulacion y la conversion. AutomataApp utiliza Tkinter para construir la tabla, coordinar las acciones del usuario y presentar el automata en un Canvas.", styles["Body"]), Spacer(1, 4)]
    image = Image(str(DIAGRAMS / "class_diagram.png"), width=15.5*cm, height=14.5*cm)
    story += [image, Paragraph("Figura 1. Diagrama de clases generado con PlantUML.", styles["Body"]), PageBreak(), Paragraph("Interaccion del usuario", styles["Heading"]), Paragraph("El flujo inicia al elegir AFD o AFN y definir sus componentes. Luego se actualiza la tabla, se escriben transiciones y el lienzo refleja la configuracion. Para un AFN, la conversion produce un AFD equivalente. Finalmente se introduce una cadena para mostrar su recorrido y resultado.", styles["Body"]), Spacer(1, 5)]
    story += [Image(str(DIAGRAMS / "use_case_diagram.png"), width=15.5*cm, height=13.3*cm), Paragraph("Figura 2. Diagrama de casos de uso generado con PlantUML.", styles["Body"]), Paragraph("Pruebas realizadas", styles["Heading"]), Paragraph("Se verifico mediante pruebas unitarias ligeras que un AFN con transicion epsilon acepta aaab y rechaza aaa. Tambien se verifico que la conversion entrega un AFD. El proyecto compila con py_compile antes de la entrega.", styles["Body"]), Paragraph("Ejecucion", styles["Heading"]), Paragraph("Con Python 3.10 o superior y Tkinter, ejecutar python main.py desde la raiz del proyecto. El ejemplo inicial reconoce cadenas binarias que terminan en 1.", styles["Body"])]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
