import pandas as pd
import os

class Formats:
    def __init__(self, path_Filereport: str, path_TypeDiscount, folder_path: str):
        self.path_Filereport = path_Filereport
        self.path_TypeDiscount = path_TypeDiscount
        self.folder_path = folder_path

    def ajustReportZHR43(self) -> str:
        # File Read
        def descuento_normaliza(texto, lista_descuentos):
            for descuento in lista_descuentos:
                if descuento in texto:
                    return descuento
            return None

        def agrupacion(texto, df_group):
            for row in df_group.itertuples(index=False):
                if row.Tipo_Descuento == texto:
                    return row.Group
            return None

        # Busca el inicio de la tabla
        with open(self.path_Filereport, 'r', encoding='latin1') as file:
            for i, linea in enumerate(file):
                if 'Nº pers.' in linea:
                    linea_inicio = i
                    break
                else:
                    continue  # File sin data

        # Leer archivo desde la cabeza REPORT ZHR43
        df = pd.read_csv(self.path_Filereport, sep='\t', skiprows=linea_inicio, encoding='latin1')

        # Renombrar columna si es necesario
        if 'Nº pers.' in df.columns:
            df.rename(columns={'Nº pers.': 'Empleado'}, inplace=True)

        if 'Soc.' in df.columns:
            df.rename(columns={'Soc.': 'Soc'}, inplace=True)

        if 'Nombre del empleado o candidato' in df.columns:
            df.rename(columns={'Nombre del empleado o candidato': 'Nombre_Empleado'}, inplace=True)

        # Leer archivo de Tipos de Descuentos
        df_descuentos = pd.read_csv(self.path_TypeDiscount, sep=',', encoding='latin1')

        # Quita datos especiales
        df_descuentos['Tipo_Descuento'] =df_descuentos['Tipo_Descuento']. astype(str).str.replace('. ', '_', regex=False)
        df_descuentos['Tipo_Descuento'] =df_descuentos['Tipo_Descuento']. astype(str).str.replace(' ', '_', regex=False)
        df_descuentos['Tipo_Descuento'] =df_descuentos['Tipo_Descuento']. astype(str).str.replace('Ã©', 'e', regex=False)

        # Lista de descuentos
        lista_descuentos = df_descuentos['Tipo_Descuento'].dropna().unique()

        df_group = df_descuentos[['Tipo_Descuento', 'Group']]

        # Remove spaces from Titles columns
        df.columns = [col.strip().replace(' ', '') for col in df.columns]

        # Drop empty column
        df.dropna(axis=1, how='all', inplace=True)

        # Change column in float and positive
        df['Importe'] = (
            df['Importe'].astype(str)
            .str.replace(',', '', regex=False)
            .astype(float)
            .abs()
        )

        # Redondear a 2 decimales
        df['Importe'] = df['Importe'].round(2)

        # Quitar las tildes
        df['Textoexpl.CC-nómina'] = df['Textoexpl.CC-nómina']. astype(str).str.replace('. ', '_', regex=False)
        df['Textoexpl.CC-nómina'] = df['Textoexpl.CC-nómina']. astype(str).str.replace(' ', '_', regex=False)
        df['Textoexpl.CC-nómina'] = df['Textoexpl.CC-nómina']. astype(str).str.replace('é', 'e', regex=False)

        # Quitar 1Q o 2Q
        df['Tipo_Descuento']= df['Textoexpl.CC-nómina'].apply(lambda x: descuento_normaliza(str(x), lista_descuentos))

        # Agrupación
        df['Agrupacion']= df['Tipo_Descuento'].apply(lambda x: agrupacion(str(x), df_group))

        # Column Dataframe Finality
        columns_Finality = ['Empleado', 'Nombre_Empleado', 'Soc', 'NombredesociedadGL', 'Importe', 'Tipo_Descuento', 'Agrupacion']
        columns_agrupa = ['Empleado', 'Nombre_Empleado', 'Soc', 'NombredesociedadGL', 'Tipo_Descuento', 'Agrupacion']

        # Agrupación df
        df_agrupado = df.groupby(columns_agrupa, as_index=False).sum(numeric_only=True)

        df_Ajustado= df_agrupado[columns_Finality]
        df_Ajustado['Importe'] = df_Ajustado['Importe'].round(2)

        lista_DescripDescuentos = df_Ajustado['Tipo_Descuento'].dropna().unique()

        # Guardar resultado General
        output_path = os.path.join(self.folder_path, "01_ReportZHR43Adjust.csv")
        df_Ajustado.to_csv(output_path, index=False)

        for lista in lista_DescripDescuentos:
            # Guardar resultado
            df_filter = df_Ajustado[df_Ajustado['Tipo_Descuento'] == lista]
            output_path = os.path.join(self.folder_path, "001_" + lista + "_RepZHR43Seg.csv")
            df_filter.to_csv(output_path, index=False)

        return "Se genero archivo con datos" if not df.empty else "Se genero archivo vacio"
