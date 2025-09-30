import random
import string
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from num2words import num2words
from dateutil.relativedelta import relativedelta

class CreatePDFSINTRAENSA(FPDF):
    def __init__(self, path_Receipts, file_report_FBL, file_Sintraemsa, NameCoordinador):
        super().__init__()  # Llama al constructor de FPDF
        self.path_Receipts = path_Receipts
        self.file_report_FBL = file_report_FBL
        self.file_Sintraemsa = file_Sintraemsa
        self.NameCoordinador = NameCoordinador

    def clean_csv(self) -> str:
        try:
            df = pd.read_csv(self.file_report_FBL, sep=',', encoding='latin1')
            df['Importe'] = pd.to_numeric(df['Importe'].astype(str).str.replace(',', '', regex=False), errors='coerce').fillna(0).abs().round(2)

            if 'Nombre' in df.columns and 'Status' in df.columns:
                df_filter = df[(df['Nombre'] == 'SITRAEMSA') & (df['Status'] == 'ok')].copy()
                df_filter['Coordinador'] = self.NameCoordinador

            else:
                print("Columnas 'Nombre' o 'Status' no existen en el archivo principal.")
                return

            if df_filter.empty:
                print("Sin datos filtrados para el descuento solicitado.")
                return

            df_Sintra = pd.read_csv(self.file_Sintraemsa, sep=',', encoding='latin1')
            df_Sintra['Importe'] = pd.to_numeric(df_Sintra['Importe'].astype(str).str.replace(',', '', regex=False), errors='coerce').fillna(0).abs().round(2)


            # Total fields added a env developer
            row_tabla = len(df_Sintra) * 3

            titles = ['Empleado', 'Nombre_Empleado', 'Importe']
            if not all(col in df_Sintra.columns for col in titles):
                print(f"Columnas {titles} no existen en el archivo de descuentos.")
                return

            df_Sintra = df_Sintra[titles]
            # Name folder
            carpeta = self.path_Receipts

            for _, fila in df_filter.iterrows():
                generar_comprobante(fila, carpeta, tabla_datos=df_Sintra, fieldAdd=row_tabla)

        except Exception as e:
            print(f"Error en el proceso: {e}")

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

    def agregar_tabla(self, datos_tabla, x=30, y=110, col_widths=[25, 90, 25], row_height=5):

        self.set_xy(x, y)
        self.set_font("Arial", "B", 9)
        # Si es DataFrame, obtener encabezados y convertir a lista
        if isinstance(datos_tabla, pd.DataFrame):
            headers = list(datos_tabla.columns)
            datos_tabla = datos_tabla.values.tolist()
        else:
            headers = ["Columna 1", "Columna 2", "Columna 3"]  # Fallback

        # Imprimir encabezado
        self.set_fill_color(0, 112, 192)
        self.set_x(x)
        for i in range(3):
            self.cell(col_widths[i], row_height, headers[i], border=1, fill=True, align="C")
        self.ln(row_height)

        # Imprimir filas
        self.set_font("Arial", "", 8)
        for fila in datos_tabla:
            self.set_x(x)
            for i in range(3):
                if i == 1:
                    texto = str(fila[i])
                    self.cell(col_widths[i], row_height, texto, border=0, align="L")
                else:
                    texto = str(fila[i])
                    self.cell(col_widths[i], row_height, texto, border=0, align="R")
            self.ln(row_height)

    def agregar_cuerpo(self, Soc, Proveedor, Nombre, N_doc, Usuario, Texto, Fe_contab, Importe, ML, Key, Nom_Soc, Acount_Deudor1, Acount_Deudor2, nameCoor, tabla, field):
        meses = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        # Obtener fecha actual
        hoy = datetime.now()
        fecha_formateada = f"{hoy.day} de {meses[hoy.month]} de {hoy.year}"

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
        self.rect(10, 10, 190, (160 + field))  # General
        self.rect(10, 10, 190, 15)  # Título Sociedad
        self.rect(10, 60, 190, (80 + field))  # Acreedor

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
        self.set_xy(60, 100)
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, f"Guatemala >>>>  {fecha_formateada}", 0)

        self.agregar_tabla(tabla)

        # Text value2
        self.set_fill_color(255, 255, 255)
        self.set_xy(145, (130 + field))
        self.set_font("Arial", "", 8)
        self.cell(25, 5, f"{formateado}", 1, 0, "R", fill=True)


        self.set_xy(105, (142 + field))
        self.set_font("Arial", "B", 8)
        self.cell(0, 10, "SOLICITADO POR", 0, 1, "L")

        self.set_xy(130, (142 + field))
        self.set_font("Arial", "", 8)
        self.cell(0, 10, "___________________________________________", 0, 1)

        self.set_fill_color(220, 220, 220)
        self.set_xy(130, (150 + field))
        self.set_font("Arial", "B", 8)
        self.cell(70, 10, f"{nameCoor}", 1, 0, "C", fill=True)

        self.set_fill_color(220, 220, 220)
        self.set_xy(130, (160 + field))
        self.set_font("Arial", "B", 6)
        self.cell(70, 10, "COORDINADOR DE NOMINAS", 1, 0, "C", fill=True)

        self.set_xy(10, (180 + field))
        self.set_font("Arial", "B", 6)
        self.cell(0, 10, f"Número Documento >>> {N_doc}", 0, 1)

        self.set_xy(10, (185 + field))
        self.set_font("Arial", "B", 6)
        self.cell(0, 10, f"Documento Procesado por >>> {Usuario}", 0, 1)

        self.set_xy(10, (190 + field))
        self.set_font("Arial", "B", 6)
        self.cell(0, 10, f"ACREEDOR >>> {Proveedor}", 0, 1)

        formateado = f"{Importe:,.2f}"
        self.set_xy(10, (195 + field))
        self.set_font("Arial", "B", 6)
        self.cell(0, 10, f"40 {Acount_Deudor1}  Q   {formateado}", 0, 1)

        numero = f"{random.randint(0, 999):03}"
        letras = ''.join(random.choices(string.ascii_uppercase, k=3))

        self.set_xy(10, (200 + field))
        self.set_font("Arial", "B", 6)
        self.cell(0, 10, f"Key >>> {Key}_{numero}{letras} ", 0, 1)

def generar_comprobante(datos, carpeta, tabla_datos=None, fieldAdd=None):
    pdf = CreatePDFSINTRAENSA(path_Receipts=carpeta, file_report_FBL="", file_Sintraemsa="", NameCoordinador="")
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
        datos["Coordinador"],
        tabla_datos if tabla_datos is not None else [["Empleado", "Nombre_Empleado", "Importe"]],
        fieldAdd
    )
    nombre_archivo = f"{carpeta}/Comprobante_{datos['Nombre']}_{datos['Soc']}.pdf"
    pdf.output(nombre_archivo)
