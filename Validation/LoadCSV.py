import pandas as pd
import os

class DownloadCSV:
    def __init__(self, path_Directory, path_Filexlsx):
        self.path_Directory = path_Directory
        self.path_Filexlsx = path_Filexlsx

    def loadCSV(self) -> str:
        try:
            if not os.path.exists(self.path_Filexlsx):
                return f"Error: El archivo '{self.path_Filexlsx}' no existe."

            xls = pd.ExcelFile(self.path_Filexlsx)
            available_sheets = xls.sheet_names

            mensajes = []

            def limpiar_dataframe(df):
                df = df.astype(str)
                return df.apply(lambda col: col.map(lambda x: x.replace('.0', '') if x.endswith('.0') else x))

            # Procesar hoja 1 si existe
            if 'Tipo_Descuentos' in available_sheets:
                df_1 = pd.read_excel(xls, sheet_name='Tipo_Descuentos')
                df_1 = limpiar_dataframe(df_1)

                df_1.to_csv(os.path.join(self.path_Directory, "Tipo_Descuento.csv"), index=False)
                mensajes.append("Hoja Tipo_Descuentos procesada correctamente.")
            else:
                mensajes.append("Hoja Tipo_Descuentos no encontrada.")

            # Procesar hoja 2 si existe
            if 'Descuentos_Judiciales' in available_sheets:
                df_2 = pd.read_excel(xls, sheet_name='Descuentos_Judiciales')
                df_2 = limpiar_dataframe(df_2)
                df_2.to_csv(os.path.join(self.path_Directory, "Descuentos_Judiciales.csv"), index=False)
                mensajes.append("Hoja Descuentos_Judiciales procesada correctamente.")
            else:
                mensajes.append("Hoja Descuentos_Judiciales no encontrada.")

            # Procesar hoja 2 si existe
            if 'Fondo_unido' in available_sheets:
                df_3 = pd.read_excel(xls, sheet_name='Fondo_unido')
                df_3 = limpiar_dataframe(df_3)
                df_3.to_csv(os.path.join(self.path_Directory, "Fondo_unido.csv"), index=False)
                mensajes.append("Hoja Fondo_unido procesada correctamente.")
            else:
                mensajes.append("Hoja Fondo_unido no encontrada.")

            return " | ".join(mensajes)

        except Exception as e:
            return f"Error inesperado: {str(e)}"


