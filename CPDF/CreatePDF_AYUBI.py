import random
import string
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from num2words import num2words
from dateutil.relativedelta import relativedelta

class CreatePDFAyubi(FPDF):
    def __init__(self, path_Receipts, file_ReportPDF, name_coord):
        super().__init__()  # Llama al constructor de FPDF
        self.path_Receipts = path_Receipts
        self.file_ReportPDF = file_ReportPDF
        self.name_coord = name_coord

    def clean_csv(self) -> str:
        # file Read
        df = pd.read_csv(self.file_ReportPDF, sep=',', encoding='latin1')

        # Transformación de df principal
        df['Importe'] = pd.to_numeric(df['Importe'].astype(str).str.replace(',', '', regex=False), errors='coerce').fillna(0).abs().round(2)

        # Filter type discount and add name the coordinator
        df_filter = df[(df['Nombre'] == 'FUNDACION AYUDAME A VIVIR') & (df['Status'] == 'ok')].copy()
        df_filter['Coordinador'] = self.name_coord

        # Name folder
        carpeta = self.path_Receipts

        for _, fila in df_filter.iterrows():
            generar_comprobante(fila, carpeta)


    def convertir_numero_a_letras(self, numero):
        entero = int(numero)
        # Convertimos el número a string y separamos la parte decimal
        parte_decimal = str(numero).split(".")[1]

        # Tomamos los dos últimos dígitos
        ultimos_dos = parte_decimal[-2:]

        decimal = int(ultimos_dos)
        parte_entera = num2words(entero, lang='es').capitalize()
        parte_decimal = num2words(decimal, lang='es')
        return f"{parte_entera} con {parte_decimal}"


    def agregar_cuerpo(self, Soc, Proveedor, Nombre, N_doc, Usuario, Texto, Fe_contab, Importe, ML, Key, Nom_Soc, Acount_Deudor1, Acount_Deudor2, Coordinador):
        meses = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }

        # Obtener fecha actual
        hoy = datetime.now()
        fecha_formateada = f"{hoy.day} de {meses[hoy.month]} de {hoy.year}"

        # Obtener mont previos

        # Calcular mes anterior
        fecha_mes_anterior = hoy - relativedelta(months=1)
        Mes_anterior = meses[fecha_mes_anterior.month].upper()
        Year_MesAnterior = fecha_mes_anterior.year

        # Name Society and Acronym
        self.set_fill_color(146, 208, 80)
        self.rect(10, 10, 190, 15, 'F')
        self.set_xy(10, 10)
        self.set_font("Arial", "B", 14)
        self.cell(190, 15, f"{Soc} >> {Nom_Soc}", 0, 0, "C")

        # Cuadricular
        self.rect(10, 10, 190, 150)  # General
        self.rect(10, 10, 190, 15)  # Título Sociedad
        self.rect(10, 60, 190, 60)  # Acreedor
        self.rect(10, 120, 190, 40)  # Vo Bo

        # Text Create check 1
        self.set_xy(10, 40)
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 8, "Señor: Gerent@ de Tesorería sírvase emitir cheque", 0)

        # Text Create check 1
        self.set_xy(10, 70)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, "A favor de:", 0)

        # Creditor name
        self.set_xy(60, 70)
        self.set_font("Courier", "B", 15)
        self.cell(0, 8, f"{Nombre}", 0, 1)

        # Text Value
        self.set_xy(150, 30)
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, "VALOR", 0, 1, "L")

        # Formatea Valor
        formateado = f"{Importe:,.2f}"

        # Value
        self.set_fill_color(220, 220, 220)
        self.set_xy(150, 40)
        self.set_font("Arial", "B", 11)
        self.cell(40, 10, f"Q      {formateado}", 1, 0, "C", fill=True)

        # Text value1
        self.set_xy(10, 80)
        self.set_font("Arial", "", 11)
        self.cell(0, 10, "Cantidad en Letras:", 0, 1)

        # Text value2
        self.set_xy(60, 80)
        self.set_font("Arial", "", 11)
        self.cell(0, 10, f"{self.convertir_numero_a_letras(Importe)} /100", 0, 1)

        # Text Concept :
        self.set_xy(10, 90)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, "Por concepto de:", 0)

        # Text Concept Employee1
        self.set_xy(60, 90)
        self.set_font("Arial", "B", 11)
        self.multi_cell(0, 8, f"PAGO {Nombre.upper()} {Mes_anterior} - {Year_MesAnterior}", 0)

        # Text City and Date Now
        self.set_xy(60, 110)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, f"Guatemala >>>>  {fecha_formateada}", 0)

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
        self.set_xy(130, 140)
        self.set_font("Arial", "B", 8)
        self.cell(70, 10, f"{Coordinador}", 1, 0, "C", fill=True)

        # Text Vo Bo Area
        self.set_fill_color(220, 220, 220)
        self.set_xy(130, 150)
        self.set_font("Arial", "B", 6)
        self.cell(70, 10, "COORDINADOR DE NOMINAS", 1, 0, "C", fill=True)

        # Text Type discount
        self.set_xy(10, 170)
        self.set_font("Arial", "B", 6)
        self.cell(0, 10, f"Número Documento >>> {N_doc}", 0, 1)

        # Text Process
        self.set_xy(10, 175)
        self.set_font("Arial", "B", 6)
        self.cell(0, 10, f"Documento Procesado por >>> {Usuario}", 0, 1)

        # Code Creditor
        self.set_xy(10, 180)
        self.set_font("Arial", "B", 6)
        self.cell(0, 10, f"ACREEDOR.>> {Proveedor}", 0, 1)

        # Text Value
        self.set_xy(10, 185)
        self.set_font("Arial", "B", 6)
        self.cell(0, 10, f"40 {Acount_Deudor1}  Q   {formateado}", 0, 1)

        # Número aleatorio entre 000 y 99 con ceros a la izquierda
        numero = f"{random.randint(0, 999):03}"

        # Letras aleatorias (3 letras mayúsculas)
        letras = ''.join(random.choices(string.ascii_uppercase, k=3))

        # Key
        self.set_xy(10, 190)
        self.set_font("Arial", "B", 6)
        self.cell(0, 10, f"Key >>> {Key}_{numero}{letras} ", 0, 1)

#    Función para generar un comprobante
def generar_comprobante(datos, carpeta):
    pdf = CreatePDFAyubi(path_Receipts=carpeta, file_ReportPDF="", name_coord="")
    pdf.add_page()
    pdf.agregar_cuerpo(
        datos["Soc"],
        datos["Proveedor"],
        datos["Nombre"],
        datos["N_doc"],
        datos["Usuario"],
        datos["Texto"],
        datos["Fe_contab"],
        datos["Importe"],
        datos["ML"],
        datos["Key"],
        datos["Nom_Soc"],
        datos["Acount_Deudor1"],
        datos["Deudor_Inter1"],
        datos["Coordinador"]
    )
    nombre_archivo = f"{carpeta}/Comprobante_{datos['Nombre']}_{datos['Soc']}.pdf"
    pdf.output(nombre_archivo)
