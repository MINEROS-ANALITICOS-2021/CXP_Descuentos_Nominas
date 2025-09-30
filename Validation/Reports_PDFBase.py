import pandas as pd
import os

class ReportsPDFBase:
    def __init__(self, path_folder, path_fileEnd, path_discount, path_fileFBL1N):
        self.path_folder = path_folder
        self.path_fileEnd = path_fileEnd
        self.path_discount = path_discount
        self.path_fileFBL1N = path_fileFBL1N

    def summaryvsFBL1N(self) -> str:
        # Leer archivos
        df = pd.read_csv(self.path_fileEnd, sep=',', encoding='latin1')
        df_discount = pd.read_csv(self.path_discount, sep=',', encoding='latin1', dtype=str)
        df_FBL1N = pd.read_csv(self.path_fileFBL1N, sep=',', encoding='latin1', dtype=str)

        # Limpieza y transformación de df_FBL1N
        df_FBL1N['Importe'] = pd.to_numeric(df_FBL1N['Importe'].str.replace(',', '', regex=False), errors='coerce').fillna(0).abs().round(2)
        df_FBL1N['Proveedor'] = df_FBL1N['Proveedor'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else '')
        df_FBL1N['Key'] = df_FBL1N.apply(lambda row: f"{row['Soc']}_{row['Proveedor']}_{row['Nombre']}_{row['Importe']}", axis=1)

        # Limpieza de Tipo_Descuento
        df_discount['Tipo_Descuento'] = (
            df_discount['Tipo_Descuento'].astype(str)
            .str.replace('. ', '_', regex=False)
            .str.replace(' ', '_', regex=False)
            .str.replace('Ã©', 'e', regex=False)
        )

        # Transformación de df principal
        df['Importe'] = pd.to_numeric(df['Importe'].astype(str).str.replace(',', '', regex=False), errors='coerce').fillna(0).abs().round(2)
        df_filAcreeNoNull = df[df['Acreedor'].notna()]
        df_groupby = df_filAcreeNoNull.groupby(['Soc', 'NombredesociedadGL', 'Acreedor', 'Tipo_Descuento'], as_index=False)['Importe'].sum()
        df_groupby = df_groupby.sort_values(by=['Tipo_Descuento', 'Soc', 'Importe'], ignore_index=True)
        df_groupby['Acreedor'] = df_groupby['Acreedor'].apply(lambda x: str(int(float(x))) if pd.notnull(x) else '')

        # Consolidación con descuentos
        df_consolidate = df_groupby.merge(df_discount[['Tipo_Descuento', 'Nom_1']], on='Tipo_Descuento', how='left')
        df_consolidate['Imp_Ajustado'] = df_consolidate.apply(
            lambda row: round(row['Importe'] * 2, 2) if row['Nom_1'] == 'FONDO UNIDO DE GUATEMALA' else round(row['Importe'], 2),
            axis=1
        )
        df_consolidate['Key'] = df_consolidate.apply(lambda row: f"{row['Soc']}_{row['Acreedor']}_{row['Nom_1']}_{row['Imp_Ajustado']}", axis=1)

        # Validación de claves
        df_FBL1N['Status'] = df_FBL1N['Key'].apply(lambda x: 'ok' if x in df_consolidate['Key'].values else '')

        # Crear un diccionario de Sociedad NombredesociedadGL
        soc_dict = df_consolidate.set_index('Soc')['NombredesociedadGL'].to_dict()

        # Asignar la columna al df_FBL1N
        df_FBL1N['Nom_Soc'] = df_FBL1N['Soc'].map(soc_dict)

        # Unión final y selección de columnas
        df_consolidateFBL1N = df_FBL1N.merge(df_discount, left_on='Nombre', right_on='Nom_1', how='left')

        # Title File Report PDF
        columnas_finales = [
            'Soc', 'Proveedor', 'Nombre', 'Asignacion', 'Referencia', 'Lib_mayor', 'N_doc', 'Clase', 'Ejerc_mes',
            'Usuario', 'Texto', 'Fe_contab', 'Fecha doc.', 'Importe', 'ML', 'Key', 'Status', 'Nom_Soc',
            'Acount_Deudor1', 'Acount_Deudor2', 'Acount_Acreedor', 'Deudor_Inter1'
        ]

        # Title File Treasury
        columnas_treasury = [
            'Soc', 'Proveedor', 'Nombre', 'Asignacion', 'Referencia', 'Lib_mayor', 'N_doc', 'Clase', 'Ejerc_mes',
            'Usuario', 'Texto', 'Fe_contab', 'Fecha doc.', 'Importe', 'ML', 'Status', 'Payment'
        ]

        # Data Filter file Treasury
        df_treasury = df_consolidateFBL1N[columnas_treasury]
        df_treasury = df_treasury[df_treasury['Status'] == 'ok'].copy()

        df_consolidateFBL1N = df_consolidateFBL1N[columnas_finales]

        # Guardar resultados
        df_consolidateFBL1N.to_csv(os.path.join(self.path_folder, "01_ReportPDF.csv"), index=False)
        df_treasury.to_excel(os.path.join(self.path_folder, "01_Filetreasury.xlsx"), index=False)

        return "Se generó archivo con datos" if not df_consolidateFBL1N.empty else "Se generó archivo vacío"
