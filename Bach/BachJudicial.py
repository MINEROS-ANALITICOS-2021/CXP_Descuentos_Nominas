import pandas as pd
import os
from datetime import datetime

class Createbachjudicial:
    def __init__(self, path_Directory, path_FileReportJudicial, path_FileParaJudicial, path_FileTipoDescuento, FinMesAnt, dateBach):
        self.path_Directory = path_Directory
        self.path_FileReportJudicial = path_FileReportJudicial
        self.path_FileParaJudicial = path_FileParaJudicial
        self.path_FileTipoDescuento = path_FileTipoDescuento
        self.FinMesAnt = FinMesAnt
        self.dateBach = dateBach

    def bachJudicial(self) -> str:

        def addCreditor(texto, dfParaJudiciales):
            for row1 in dfParaJudiciales.itertuples(index=False):
                if str(row1.Code_Employee) == texto:
                    return row1.Acount_Acreedor
            return None

        # Leer archivo Reporte Segmentado Judicial
        df1 = pd.read_csv(self.path_FileReportJudicial, sep=',', encoding='latin1')

        # Leer archivo Reporte Parametricas Judicial
        df2 = pd.read_csv(self.path_FileParaJudicial, sep=',', encoding='latin1')

        # Leer archivo Reporte Tipos
        df3 = pd.read_csv(self.path_FileTipoDescuento, sep=',', encoding='latin1', dtype=str)

        # Remove spaces and special characters - Parametrics
        df3['Tipo_Descuento'] =df3['Tipo_Descuento']. astype(str).str.replace('. ', '_', regex=False)
        df3['Tipo_Descuento'] =df3['Tipo_Descuento']. astype(str).str.replace(' ', '_', regex=False)
        df3['Tipo_Descuento'] =df3['Tipo_Descuento']. astype(str).str.replace('Ã©', 'e', regex=False)

        # Add Acreedor
        df1['Acount_Acreedor'] = df1['Empleado'].apply(lambda x: addCreditor(str(x), df2))

        # Columns de Paramétricas
        columnas_deseadas = [
            'Acount_Deudor1', 'Deudor_Inter1', 'Deudor_Inter2', 'Soc_inter', 'Add_Soc_Inter',
            'CLdeudor1', 'CLdeudor2', 'CLdeudor3', 'CLAcreedor1', 'CLAcreedor2',
            'Summary'
        ]

        # Realizar el cruce de datos usando merge
        resultado = pd.merge(df1, df3[['Tipo_Descuento'] + columnas_deseadas], on='Tipo_Descuento', how='left')

        # Filter dDataset no null
        df_End = resultado[resultado['Acount_Acreedor'].notna()]

        # Obtener la fecha actual
        # fecha_actual = datetime.now()
        # fecha_formateada = fecha_actual.strftime("%d.%m.%Y")
        fecha_formateada = self.dateBach
        fecha_finMes = self.FinMesAnt

        # Celdas Vacias
        vacio = ''

        # Columnas Bach
        columnas = ['DOC', 'FECHA_DOC', 'FECHA_CONT.', 'CDOC', 'SOCIEDAD', 'MONEDA', 'REFERENCIA',
                           'TEXTO_DOC', 'CL_C', 'CUENTA', 'ME', 'IMPORTE', 'IVA', 'REF0', 'FECHA_VALOR', 'CeCo',
                           'Orden', 'CeBe', 'ASIGNACION', 'TEXTO_POS', 'CANT', 'UM', 'MATERIAL', 'CLIENTE',
                           'REF1', 'REF2', 'REF3', 'CENTRO', 'MES']


        # Construir los datos para el nuevo DataFrame
        datos = []

        for row in df_End.itertuples(index=False):
            if row.Soc == row.Soc_inter:
                '''Ajustado'''
                # Fila Deudor - Intercompany 1 GOO1
                filaDeudor= [
                    'X', fecha_formateada, fecha_formateada, 'GL', row.Add_Soc_Inter, 'GTQ',
                    f"{row.Summary}_{fecha_finMes}_01", f"{row.Nombre_Empleado} {row.Empleado}",
                    row.CLdeudor2, row.Deudor_Inter1, vacio, round(float(row.Importe), 2), vacio, vacio, vacio, vacio,
                    vacio, vacio, row.Empleado,
                    f"{row.Nombre_Empleado} {row.Empleado}", vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio,
                    vacio
                ]
                # Agrega Fila al Data Frame Deudor
                datos.append(filaDeudor)
                '''Ajustado'''
                # Fila Acreedor InterCompany 1 G001
                filaAcreedor= [
                    vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio, row.CLAcreedor1, row.Acount_Acreedor, vacio,
                    round(float(row.Importe), 2), vacio, vacio, vacio, vacio, vacio, vacio, row.Empleado,
                    f"{row.Nombre_Empleado} {row.Empleado}",
                    vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio
                ]
                # Agrega Fila al Data Frame Acreedor
                datos.append(filaAcreedor)
                '''Ajustado'''
                # Fila Deudor - Intercompany 2 GO22
                filaDeudor= [
                    'X', fecha_formateada, fecha_formateada, 'GL', row.Soc, 'GTQ', f"{row.Summary}_{fecha_finMes}_01",
                    f"{row.Nombre_Empleado} {row.Empleado}", row.CLdeudor3, row.Deudor_Inter2, vacio,
                    round(float(row.Importe), 2), vacio, vacio, vacio, vacio, vacio, vacio, row.Empleado,
                    f"{row.Nombre_Empleado} {row.Empleado}", vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio,
                    vacio
                ]
                # Agrega Fila al Data Frame Deudor
                datos.append(filaDeudor)
                '''Ajustado'''
                # Fila Acreedor InterCompany 2 G022
                filaAcreedor= [
                    vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio, row.CLAcreedor2, row.Acount_Acreedor, vacio,
                    round(float(row.Importe), 2), vacio, vacio, vacio, vacio, vacio, vacio, row.Empleado,
                    f"{row.Nombre_Empleado} {row.Empleado}",
                    vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio
                ]
                # Agrega Fila al Data Frame Acreedor
                datos.append(filaAcreedor)
            else:
                '''Ajustado'''
                # Fila Deudor
                filaDeudor= [
                    'X', fecha_formateada, fecha_formateada, 'PL', row.Soc, 'GTQ', row.Empleado,
                    f"{row.Nombre_Empleado} {row.Empleado}", row.CLdeudor1, row.Acount_Deudor1, vacio,
                    round(float(row.Importe), 2), vacio, vacio, vacio, vacio, vacio, vacio, row.Empleado,
                    f"{row.Nombre_Empleado} {row.Empleado}", vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio,
                    vacio
                ]
                # Agrega Fila al Data Frame Deudor
                datos.append(filaDeudor)
                '''Ajustado'''
                # Fila Acreedor
                filaAcreedor= [
                    vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio, row.CLAcreedor1, row.Acount_Acreedor, vacio,
                    round(float(row.Importe), 2), vacio, vacio, vacio, vacio, vacio, vacio,
                    row.Empleado, f"{row.Nombre_Empleado} {row.Empleado}",
                    vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio, vacio
                ]
                # Agrega Fila al Data Frame Acreedor
                datos.append(filaAcreedor)

        # Crear el nuevo DataFrame
        df_BachJudicial = pd.DataFrame(datos, columns=columnas)


        # Filtrar por CL_C en ['40', '21', '11']
        filtroDeudor = df_BachJudicial[
            df_BachJudicial['CL_C'].isin(['40', '21', '11']) &
            df_BachJudicial['TEXTO_DOC'].notna() &
            (df_BachJudicial['TEXTO_DOC'].astype(str).str.strip() != '')
        ]

        # Sumar la columna IMPORTE
        suma_deudor = filtroDeudor['IMPORTE'].sum()

        # Filtrar por CL_C en ['31', '21']
        filtroAcreedor = df_BachJudicial[
            df_BachJudicial['CL_C'].isin(['31', '21']) &
            df_BachJudicial['TEXTO_DOC'].notna() &
            (df_BachJudicial['TEXTO_DOC'].astype(str).str.strip() == '')]

        # Sumar la columna IMPORTE
        suma_acreedor = filtroAcreedor['IMPORTE'].sum()

        # Valida creación BACH
        valida = f"Diferencia >>> {suma_acreedor - suma_deudor}"

        # Guardar resultado General
        output_path = os.path.join(self.path_Directory, "0001_Bach_Judiciales.csv")
        df_BachJudicial.to_csv(output_path, index=False)

        return f"Se genero archivo con datos >> valida {valida} " if not df_BachJudicial.empty else "Se genero archivo vacio"
