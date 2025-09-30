import pandas as pd
import os

class CreateReportsF:
    def __init__(self, path_Directory, path_FileReport, user, date_Process):
        self.path_Directory = path_Directory
        self.path_FileReport = path_FileReport
        self.user = user
        self.date_Process = date_Process

    def ajustReportFBL1N(self) -> str:
        try:
            # Validar existencia del archivo
            if not os.path.isfile(self.path_FileReport):
                return "Error: El archivo de reporte no existe."

            # Buscar línea de inicio de la tabla
            with open(self.path_FileReport, 'r', encoding='latin1') as file:
                linea_inicio = None
                for i, linea in enumerate(file):
                    if 'Soc.' in linea:
                        linea_inicio = i
                        break

            if linea_inicio is None:
                return "Error: No se encontró el inicio de la tabla en el archivo."

            # Leer el archivo como DataFrame
            df = pd.read_csv(self.path_FileReport, sep='\t', skiprows=linea_inicio, encoding='latin1')

            # Renombrar columnas con diccionario
            rename_dict = {
                'Soc.': 'Soc',
                'Asignación': 'Asignacion',
                'Lib.mayor': 'Lib_mayor',
                'Nº doc.': 'N_doc',
                'Ejerc./mes': 'Ejerc_mes',
                'Fe.contab.': 'Fe_contab',
                ' Importe en ML': 'Importe'
            }
            df.rename(columns={k: v for k, v in rename_dict.items() if k in df.columns}, inplace=True)

            # Eliminar columnas completamente vacías
            df.dropna(axis=1, how='all', inplace=True)

            # Procesar columna 'Importe'
            if 'Importe' in df.columns:
                df['Importe'] = (
                    df['Importe'].astype(str)
                    .str.replace(',', '', regex=False)
                    .astype(float)
                    .abs()
                    .round(2)
                )
            else:
                return "Error: La columna 'Importe' no está presente en el archivo."

            # Filtrar por usuario y fecha
            if 'Usuario' not in df.columns or 'Fe_contab' not in df.columns:
                return "Error: Columnas necesarias para el filtro no están presentes."

            df_filter = df[(df['Usuario'] == self.user) & (df['Fe_contab'] == self.date_Process)]

            # Ordenar por columnas si existen
            sort_cols = [col for col in ['Nombre', 'Soc'] if col in df_filter.columns]
            if sort_cols:
                df_filter = df_filter.sort_values(sort_cols)

            # Guardar resultado
            output_path = os.path.join(self.path_Directory, "01_ReportFBL1NAdjust.csv")
            df_filter.to_csv(output_path, index=False)

            return "Se genero archivo con datos." if not df_filter.empty else "Se genero archivo vacío."

        except Exception as e:
            return f"Error inesperado: {str(e)}"

