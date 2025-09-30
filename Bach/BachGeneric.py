import pandas as pd
import os


class CreateBachGeneric:
    def __init__(self, path_Directory, file_Discount, file_parametrics, Month, Year, FinMesAnt, dateBach):
        self.path_Directory = path_Directory
        self.file_Discount = file_Discount
        self.file_parametrics = file_parametrics
        self.Month = Month
        self.Year = Year
        self.FinMesAnt = FinMesAnt
        self.dateBach = dateBach

    def bachGeneric(self) -> str:
        # Read Discount types File
        df_1= pd.read_csv(self.file_Discount, sep=",", encoding='latin1',)

        # Name File
        namefile1 = df_1['Tipo_Descuento'].dropna().unique()
        name = namefile1[0]
        print(name)
        # Read Parametrics
        df_2 = pd.read_csv(self.file_parametrics, sep=',', encoding='latin1', dtype=str)

        # Remove spaces and special characters - Parametrics
        df_2['Tipo_Descuento'] =df_2['Tipo_Descuento']. astype(str).str.replace('. ', '_', regex=False)
        df_2['Tipo_Descuento'] =df_2['Tipo_Descuento']. astype(str).str.replace(' ', '_', regex=False)
        df_2['Tipo_Descuento'] =df_2['Tipo_Descuento']. astype(str).str.replace('Ã©', 'e', regex=False)

        # Columns Parametrics
        columnas_deseadas = [
            'Acount_Deudor1', 'Acount_Acreedor',
            'Deudor_Inter1', 'Deudor_Inter2', 'Soc_inter', 'Add_Soc_Inter',
            'CLdeudor1', 'CLdeudor2', 'CLdeudor3', 'CLAcreedor1', 'CLAcreedor2',
            'Summary', 'Text_Ref'
        ]

        # Perform data crossing
        joinData = pd.merge(df_1, df_2[['Tipo_Descuento'] + columnas_deseadas], on='Tipo_Descuento', how='left')

        # Group by Society
        column_agrupaSoc = ['Soc', 'Acount_Deudor1', 'Acount_Acreedor',
                            'Deudor_Inter1', 'Deudor_Inter2', 'Soc_inter', 'Add_Soc_Inter',
                            'CLdeudor1', 'CLdeudor2', 'CLdeudor3', 'CLAcreedor1', 'CLAcreedor2',
                            'Summary', 'Text_Ref']

        # Clean and amount conversion
        joinData['Importe'] = pd.to_numeric(
            joinData['Importe'].astype(str).str.replace(',', '', regex=False),
            errors='coerce'
        ).fillna(0).abs().round(2)

        # Group by society Df one
        df_groupby = joinData.groupby(column_agrupaSoc, as_index=False)['Importe'].sum()

        # Create BACH
        # Get current date
        # fecha_actual = datetime.now()
        # fecha_formateada = fecha_actual.strftime("%d.%m.%Y")
        fecha_formateada = self.dateBach
        fecha_finMes = self.FinMesAnt
        fecha_Month = self.Month
        fecha_Year = self.Year

        # Celdas Vacias
        vacio = ''

        # Columns Bach
        columnas = ['DOC', 'FECHA_DOC', 'FECHA_CONT.', 'CDOC', 'SOCIEDAD', 'MONEDA', 'REFERENCIA',
                    'TEXTO_DOC', 'CL_C', 'CUENTA', 'ME', 'IMPORTE', 'IVA', 'REF0', 'FECHA_VALOR', 'CeCo',
                    'Orden', 'CeBe', 'ASIGNACION', 'TEXTO_POS', 'CANT', 'UM', 'MATERIAL', 'CLIENTE',
                    'REF1', 'REF2', 'REF3', 'CENTRO', 'MES']

        # Construir los datos para el nuevo DataFrame
        datos = []

        for row in df_groupby.itertuples(index=False):
            if row.Soc == row.Soc_inter:

                '''Ajustado'''
                # Fila Deudor - Intercompany 1 GOO1
                filaDeudor = [
                    'X', fecha_formateada, fecha_formateada, 'GL', row.Add_Soc_Inter, 'GTQ',
                    f"{row.Summary}_{fecha_finMes}_01",
                    f"{row.Text_Ref} {fecha_Month}-{fecha_Year}", row.CLdeudor2, row.Deudor_Inter1, vacio,
                    round(float(row.Importe), 2), vacio, vacio, vacio, vacio, vacio, vacio,
                    f"{row.Summary}_{fecha_finMes}_01",
                    f"{row.Text_Ref} {fecha_Month}-{fecha_Year}", vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio,
                    vacio
                ]
                # Agrega Fila al Data Frame Deudor
                datos.append(filaDeudor)
                '''Ajustado'''
                # Fila Acreedor InterCompany 1 G001
                filaAcreedor = [
                    vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio, row.CLAcreedor1, row.Acount_Acreedor, vacio,
                    round(float(row.Importe), 2), vacio, vacio, vacio, vacio, vacio, vacio,
                    f"{row.Summary}_{fecha_finMes}_01",
                    f"{row.Text_Ref} {fecha_Month}-{fecha_Year}", vacio, vacio, vacio, vacio, vacio, vacio, vacio,
                    vacio, vacio
                ]
                # Agrega Fila al Data Frame Acreedor
                datos.append(filaAcreedor)
                '''Ajustado'''
                # Fila Deudor - Intercompany 2 GO22
                filaDeudor = [
                    'X', fecha_formateada, fecha_formateada, 'GL', row.Soc, 'GTQ', f"{row.Summary}_{fecha_finMes}_01",
                    f"{row.Text_Ref} {fecha_Month}-{fecha_Year}", row.CLdeudor3, row.Deudor_Inter2,
                    vacio, round(float(row.Importe), 2), vacio, vacio, vacio, vacio, vacio, vacio,
                    f"{row.Summary}_{fecha_finMes}_01", f"{row.Text_Ref} {fecha_Month}-{fecha_Year}",
                    vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio
                ]
                # Agrega Fila al Data Frame Deudor
                datos.append(filaDeudor)
                '''Ajustado'''
                # Fila Acreedor InterCompany 2 G022
                filaAcreedor = [
                    vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio, row.CLAcreedor2, row.Acount_Acreedor, vacio,
                    round(float(row.Importe), 2), vacio, vacio, vacio, vacio, vacio, vacio,
                    f"{row.Summary}_{fecha_finMes}_01", f"{row.Text_Ref} {fecha_Month}-{fecha_Year}",
                    vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio
                ]
                # Agrega Fila al Data Frame Acreedor
                datos.append(filaAcreedor)
            else:
                '''Ajustado'''
                # Fila Deudor
                filaDeudor = [
                    'X', fecha_formateada, fecha_formateada, 'PL', row.Soc, 'GTQ',
                    f"{row.Text_Ref} {fecha_Month}-{fecha_Year}",
                    f"{row.Text_Ref} {fecha_Month}-{fecha_Year}", row.CLdeudor1, row.Acount_Deudor1, vacio,
                    round(float(row.Importe), 2), vacio, vacio, vacio, vacio, vacio, vacio,
                    f"{row.Text_Ref} {fecha_Month}-{fecha_Year}", f"{row.Text_Ref} {fecha_Month}-{fecha_Year}",
                    vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio
                ]
                # Agrega Fila al Data Frame Deudor
                datos.append(filaDeudor)
                '''Ajustado'''
                # Fila Acreedor
                filaAcreedor = [
                    vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio, row.CLAcreedor1, row.Acount_Acreedor, vacio,
                    round(float(row.Importe), 2), vacio, vacio, vacio, vacio, vacio, vacio,
                    f"{row.Text_Ref} {fecha_Month}-{fecha_Year}", f"{row.Text_Ref} {fecha_Month}-{fecha_Year}",
                    vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio
                ]
                # Agrega Fila al Data Frame Acreedor
                datos.append(filaAcreedor)

        # Crear el nuevo DataFrame
        df_Bach = pd.DataFrame(datos, columns=columnas)

        # Guardar resultado General
        output_path = os.path.join(self.path_Directory, f"0001_Bach_{name}.csv")
        df_Bach.to_csv(output_path, index=False)

        return f"Se genero archivo con datos >> valida {name} " if not df_Bach.empty else "Se genero archivo vacio"
