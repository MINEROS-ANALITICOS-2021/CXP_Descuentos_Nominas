import csv
from fpdf import FPDF
from datetime import datetime
from num2words import num2words

class CreatePDF1(FPDF):
    def __init__(self, path_Directory, file_Discount):
        super().__init__()  # Llama al constructor de FPDF
        self.path_Directory = path_Directory
        self.file_Discount = file_Discount

    # Función para leer CSV y procesar comprobantes
    def procesar_csv(self) -> str:
        carpeta = self.path_Directory
        with open(self.file_Discount, newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                generar_comprobante(fila, carpeta)

    def convertir_numero_a_letras1(self, numero):
        return num2words(numero, lang='es').upper()

    def agregar_cuerpo(self, Empleado, NombreEmp, Soc, NombreSoc, Importe, Tipo_Descuento, Codigo_Acreedor, Nombre_Acreedor, Folio, Pais, Cuenta, Resp_Nomina, Nombre_RespNomina):
        meses = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        # Obtener fecha actual
        hoy = datetime.now()
        fecha_formateada = f"{hoy.day} de {meses[hoy.month]} de {hoy.year}"
        # Name Society and Acronym
        self.set_fill_color(173, 216, 230)
        self.rect(10, 10, 190, 15, 'F')
        self.set_xy(10, 10)
        self.set_font("Arial", "B", 14)
        self.cell(190, 15, f"{Soc} >> {NombreSoc}", 0, 0, "C")

        # Cuadricular
        self.rect(10, 10, 190, 150)  # General
        self.rect(10, 10, 190, 15)  # Titulo Sociedad
        self.rect(10, 60, 190, 60)  # Acreedor
        self.rect(10, 120, 190, 40)  # Vo Bo

        # Text Creat check 1
        self.set_xy(10, 40)
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 8, "Señor@: Gerent@ de Tesorería sirvase emitir cheque", 0)

        # Text Creat check 1
        self.set_xy(10, 70)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, "A favor de:", 0)

        # Creditor name
        self.set_xy(60, 70)
        self.set_font("Arial", "B", 11)
        self.cell(0, 8, f"{Nombre_Acreedor}", 0, 1)

        # Text Value
        self.set_xy(150, 30)
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "VALOR", 0, 1, "L")

        # Value
        self.set_fill_color(220, 220, 220)
        self.set_xy(150, 40)
        self.set_font("Arial", "B", 11)
        self.cell(40, 10, f"{Importe}", 1, 0, "C", fill=True)

        # Code Creditor
        self.set_xy(150, 60)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, "Codigo acreedor", 0, "R")

        # Code Creditor
        self.set_xy(150, 70)
        self.set_font("Arial", "B", 11)
        self.multi_cell(0, 8, f"{Codigo_Acreedor}", 0, "R")

        # Text value1
        self.set_xy(10, 80)
        self.set_font("Arial", "", 11)
        self.cell(0, 10, "Cantidad en Letras:", 0, 1)

        # Text value2
        self.set_xy(60, 80)
        self.set_font("Arial", "", 11)
        self.cell(0, 10, f"{self.convertir_numero_a_letras1(Importe)} CON 00/100", 0, 1)

        # Text Concept :
        self.set_xy(10, 90)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, "Por concepto de:", 0)

        # Text Concept Employee1
        self.set_xy(60, 90)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, f"{Tipo_Descuento}, {Folio} (1) >>Pensión Alimenticia<<", 0)

        # Text Concept Employee2
        self.set_xy(60, 100)
        self.set_font("Arial", "B", 11)
        self.multi_cell(0, 8, f"descontado a {NombreEmp} >> {Empleado}", 0)

        # Text City and Date Now
        self.set_xy(60, 110)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, f"{Pais} >>>>  {fecha_formateada}", 0)

        # Text Account
        self.set_xy(10, 120)
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "Cuenta:", 0, 1)

        # Text Value
        self.set_xy(60, 120)
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, f"{Cuenta}", 0, 1)

        # Text Vo Bo
        self.set_xy(140, 130)
        self.set_font("Arial", "", 8)
        self.cell(0, 10, "Vo Bo.", 0, 1)

        # Text Vo Bo
        self.set_xy(150, 130)
        self.set_font("Arial", "", 8)
        self.cell(0, 10, "_____________________", 0, 1)

        # Text Vo Bo
        self.set_fill_color(220, 220, 220)
        self.set_xy(150, 140)
        self.set_font("Arial", "B", 8)
        self.cell(40, 10, f"{Nombre_RespNomina}", 1, 0, "C", fill=True)

        # Text Vo Bo Area
        self.set_fill_color(220, 220, 220)
        self.set_xy(150, 150)
        self.set_font("Arial", "B", 6)
        self.cell(40, 10, f"{Resp_Nomina}", 1, 0, "C", fill=True)

        # Text Type discount
        self.set_xy(10, 148)
        self.set_font("Arial", "", 6)
        self.cell(0, 10, f"TIPO DE DESCUENTO >>>>{Tipo_Descuento}", 0, 1)

        # Text Process
        self.set_xy(10, 150)
        self.set_font("Arial", "", 6)
        self.cell(0, 10, "Documento Procesado por Bot APEX23", 0, 1)

# Función para generar un comprobante
def generar_comprobante(datos, carpeta):
    pdf = CreatePDF1(path_Directory=carpeta, file_Discount="")
    pdf.add_page()
    pdf.agregar_cuerpo(
        datos["Empleado"],
        datos["Nombre_Empleado"],
        datos["Soc"],
        datos["NombredesociedadGL"],
        datos["Importe"],
        datos["Tipo_Descuento"],
        datos["Codigo_Acreedor"],
        datos["Nombre_Acreedor"],
        datos["Folio"],
        datos["Pais"],
        datos["Cuenta"],
        datos["Resp_Nomina"],
        datos["Nombre_RespNomina"]
    )
    nombre_archivo = f"{carpeta}/Comprobante_{datos['Nombre_Empleado']}_{datos['Soc']}.pdf"
    pdf.output(nombre_archivo)
