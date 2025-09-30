import pandas as pd
import os

class CreateReportsZ:
    def __init__(self, path_Directory, path_FileZHR43, path_FileDiscount, path_FileJudicial):
        self.path_Directory = path_Directory
        self.path_FileZHR43 = path_FileZHR43
        self.path_FileDiscount = path_FileDiscount
        self.path_FileJudicial = path_FileJudicial

    def summaryReportZHR43(self) -> str:

        # Add Acount acreedor Discount
        def addAcreeedorGNR(texto, dfFileDiscount):
            for row_dfFD in dfFileDiscount.itertuples(index=False):

                if str(row_dfFD.Tipo_Descuento) == texto:
                    return row_dfFD.Acount_Acreedor
            return None

        # Add Acount acreedor Judicial
        def addAcreeedorJUD(texto, dfFileJudicial):
            for row_dfFileJudicial in dfFileJudicial.itertuples(index=False):
                if str(row_dfFileJudicial.Code_Employee) == texto:
                    return row_dfFileJudicial.Acount_Acreedor
            return None

        # Leer archivo Reporte ZHR43
        df1 = pd.read_csv(self.path_FileZHR43, sep=',', encoding='latin1')

        # Leer archivo Reporte Descuentos Generales
        df2 = pd.read_csv(self.path_FileDiscount, sep=',', encoding='latin1', dtype=str)

        # Leer archivo Reporte Judicial
        df3 = pd.read_csv(self.path_FileJudicial, sep=',', encoding='latin1', dtype=str)

        # Limpieza y conversión de Importe
        df1['Importe'] = pd.to_numeric(
            df1['Importe'].astype(str).str.replace(',', '', regex=False),
            errors='coerce'
        ).fillna(0).abs().round(2)

        # Remove spaces and special characters - Parametrics
        df2['Tipo_Descuento'] =df2['Tipo_Descuento']. astype(str).str.replace('. ', '_', regex=False)
        df2['Tipo_Descuento'] =df2['Tipo_Descuento']. astype(str).str.replace(' ', '_', regex=False)
        df2['Tipo_Descuento'] =df2['Tipo_Descuento']. astype(str).str.replace('Ã©', 'e', regex=False)

        # Aplicar lógica para obtener Acreedor
        def obtener_acreedor(row):
            if row['Tipo_Descuento'] == "DES_JUDICIAL":
                return addAcreeedorJUD(str(row['Empleado']), df3)
            else:
                return addAcreeedorGNR(str(row['Tipo_Descuento']), df2)

        # Llena Columna con data
        df1['Acreedor'] = df1.apply(obtener_acreedor, axis=1)

        # Deudores Con Acreedor
        df1_Acreedor = df1[df1['Acreedor'].notna()]

        # Deudores sin Acreedor
        df1_outAcreedor = df1[df1['Acreedor'].isna()]

        # Lista de Sociedades
        lista_Sociedad = df1_Acreedor['Soc'].dropna().unique()
        df_Sociedades = pd.DataFrame(lista_Sociedad, columns=['Sociedad'])

        # Lista de Cuentas Acreedor
        lista_CuentasAcreedor = df1_Acreedor['Acreedor'].dropna().unique()
        df_CuentasAcreedor = pd.DataFrame(lista_CuentasAcreedor, columns=['Acreedores'])

        # Column Dataframe
        agru_SocTipoDescuento = ['Soc', 'Tipo_Descuento']
        agru_TipoDescuento = ['Tipo_Descuento']

        # Agrupación df
        df1_AgrSocTipoDes = df1_Acreedor.groupby(agru_SocTipoDescuento, as_index=False)['Importe'].sum()
        df1_AgrTipoDes = df1_Acreedor.groupby(agru_TipoDescuento, as_index=False)['Importe'].sum()
        df1_AgrSocTipoDes = df1_AgrSocTipoDes.sort_values(by=['Tipo_Descuento', 'Soc'])
        df1_AgrTipoDes = df1_AgrTipoDes.sort_values(by=['Tipo_Descuento'])

        # Archivos Generados Adicionales
        # Create File PDF
        for row_TD in df2.itertuples(index=False):
            df_filterPDF = df1_Acreedor[df1_Acreedor['Tipo_Descuento'] == row_TD.Tipo_Descuento]
            if len(df_filterPDF) > 0:
                df_filterPDF = df_filterPDF.sort_values(by=['Soc'])
                output_path = os.path.join(self.path_Directory, f"PREPDF_{row_TD.Tipo_Descuento}.csv")
                df_filterPDF.to_csv(output_path, index=False)

        # Save Summary General
        output_path = os.path.join(self.path_Directory, f"01_Summary_Report_ZHR43.csv")
        df1.to_csv(output_path, index=False)

        # Save Summary Society and Discount

        output_path = os.path.join(self.path_Directory, f"01_Summary_Society_Discount.csv")
        df1_AgrSocTipoDes.to_csv(output_path, index=False, header=False)

        # Save Summary Type Discount
        output_path = os.path.join(self.path_Directory, f"01_Summary_Discount.csv")
        df1_AgrTipoDes.to_csv(output_path, index=False, header=False)

        # Guardar Deudores sin Acreedor
        output_path = os.path.join(self.path_Directory, f"Rep_DeudorSINAcreedor.csv")
        df1_outAcreedor.to_csv(output_path, index=False)

        # Guardar resultado Con Deudor y Acreedor Total
        output_path = os.path.join(self.path_Directory, f"Rep_DeudorCONAcreedor.csv")
        df1_Acreedor.to_csv(output_path, index=False)

        # Guardar resultado Sociedades

        # Asignar la primera fila como encabezados
        df_Sociedades.columns = df_Sociedades.iloc[0]
        df_Sociedades = df_Sociedades[1:].reset_index(drop=True)

        output_path = os.path.join(self.path_Directory, f"Rep_lista_Sociedad.csv")
        df_Sociedades.to_csv(output_path, index=False)

        # Asignar la primera fila como encabezados
        df_CuentasAcreedor.columns = df_CuentasAcreedor.iloc[0]
        df_CuentasAcreedor = df_CuentasAcreedor[1:].reset_index(drop=True)

        # Guardar resultado Acreedores
        output_path = os.path.join(self.path_Directory, f"Rep_lista_CuentasAcreedor.csv")
        df_CuentasAcreedor.to_csv(output_path, index=False)

        return f"Se genero archivo con datos >> valida  " if not df1.empty else "Se genero archivo vacío"
