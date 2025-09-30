import pandas as pd
import os
from datetime import datetime
import unicodedata

class Createbachprestamo:
    def __init__(self, path_Directory, path_FileReportDescuento, path_FileParametrica, Month, Year, FinMesAnt, dateBach):
        self.path_Directory = path_Directory
        self.path_FileReportDescuento = path_FileReportDescuento
        self.path_FileParametrica = path_FileParametrica
        self.Month = Month
        self.Year = Year
        self.FinMesAnt = FinMesAnt
        self.dateBach = dateBach

    def bachPrestamos(self) -> str:

        """
        Crear csv para Bach
        Apadrinamiento AYUVI
        Préstamo Bco Industria
        Préstamo Bco CHN

        """

        # File Read
        filereportDescuento = self.path_FileReportDescuento
        fileParametrica = self.path_FileParametrica

        # Leer archivo Reporte Segmentado Judicial
        df1 = pd.read_csv(filereportDescuento, sep=',', encoding='latin1')

        # Leer archivo Reporte Parametricas Judicial
        df2 = pd.read_csv(fileParametrica, sep=',', encoding='latin1', dtype=str)

        # Quita datos especiales
        df2['Tipo_Descuento'] =df2['Tipo_Descuento']. astype(str).str.replace('. ', '_', regex=False)
        df2['Tipo_Descuento'] =df2['Tipo_Descuento']. astype(str).str.replace(' ', '_', regex=False)
        df2['Tipo_Descuento'] =df2['Tipo_Descuento']. astype(str).str.replace('Ã©', 'e', regex=False)

        # Columnas de Paramétricas
        columnas_deseadas = [
            'Acount_Deudor1', 'Acount_Deudor2', 'Acount_Acreedor',
            'Deudor_Inter1', 'Deudor_Inter2', 'Soc_inter', 'Add_Soc_Inter',
            'CLdeudor1', 'CLdeudor2', 'CLdeudor3', 'CLAcreedor1', 'CLAcreedor2',
            'Summary', 'Text_Ref', 'Payment'
        ]

        # Realizar el cruce de datos usando merge
        resultado = pd.merge(df1, df2[['Tipo_Descuento'] + columnas_deseadas], on='Tipo_Descuento', how='left')

        # Name file
        arr_namefile = df1['Tipo_Descuento'].dropna().unique()
        for name in arr_namefile:
            namefile = name
        namefile1 = namefile.replace(' ', '_')

        # Agrupa por sociedades
        column_agrupaSoc = ['Soc', 'Acount_Deudor1', 'Acount_Acreedor',
                            'Deudor_Inter1', 'Deudor_Inter2', 'Soc_inter', 'Add_Soc_Inter',
                            'CLdeudor1', 'CLdeudor2', 'CLdeudor3', 'CLAcreedor1', 'CLAcreedor2',
                            'Summary', 'Text_Ref', 'Payment']

        # Limpieza y conversión de Importe
        resultado['Importe'] = pd.to_numeric(
            resultado['Importe'].astype(str).str.replace(',', '', regex=False),
            errors='coerce'
        ).fillna(0).abs().round(2)

        # Agrupa por Sociedad
        df_agrupaSoc = resultado.groupby(column_agrupaSoc, as_index=False)['Importe'].sum()

        '''CREACIÓN DEL BACH'''
        # Obtener la fecha actual
        # fecha_actual = datetime.now()
        # fecha_formateada = fecha_actual.strftime("%d.%m.%Y")
        fecha_formateada =  self.dateBach
        fecha_finMes = self.FinMesAnt
        fecha_Month = self.Month
        fecha_Year = self.Year

        # Celdas Vacias
        vacio = ''

        # Columnas Bach
        columnas = ['DOC', 'FECHA_DOC', 'FECHA_CONT.', 'CDOC', 'SOCIEDAD', 'MONEDA', 'REFERENCIA',
                    'TEXTO_DOC', 'CL_C', 'CUENTA', 'ME', 'IMPORTE', 'IVA', 'REF0', 'FECHA_VALOR', 'CeCo',
                    'Orden', 'CeBe', 'ASIGNACION', 'TEXTO_POS', 'CANT', 'UM', 'MATERIAL', 'CLIENTE',
                    'REF1', 'REF2', 'REF3', 'CENTRO', 'MES']

        # Construir los datos para el nuevo DataFrame
        datos = []

        for row in df_agrupaSoc.itertuples(index=False):
            if row.Soc == row.Soc_inter:
                # Fila Deudor
                filaDeudor = [
                    'X', fecha_formateada, fecha_formateada, 'PL', row.Soc, 'GTQ',
                    f"{row.Text_Ref} {fecha_Month}-{fecha_Year}",
                    f"{row.Text_Ref} {fecha_Month}-{fecha_Year}", row.CLdeudor1, row.Acount_Deudor1, vacio,
                    round(float(row.Importe), 2), vacio, vacio, vacio, vacio, vacio, vacio,
                    f"{row.Text_Ref} {fecha_Month}-{fecha_Year}",
                    f"{row.Text_Ref} {fecha_Month}-{fecha_Year}", vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio,
                    vacio
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
        output_path = os.path.join(self.path_Directory, f"0001_Bach_{namefile1}.csv")
        df_Bach.to_csv(output_path, index=False)

        return f"Se generó archivo con datos >> valida {namefile1} " if not df1.empty else "Se generó archivo vacío"
