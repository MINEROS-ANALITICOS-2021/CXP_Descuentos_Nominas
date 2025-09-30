import os
import pandas as pd

class Bachfinality:
    def __init__(self, path_Directory, case):
        self.path_Directory = path_Directory
        self.case = case

    def consolidate_Bach(self) -> str:
        def tiene_filas_diligenciadas(ruta_archivo):
            try:
                df_1 = pd.read_csv(ruta_archivo, encoding='utf-8', engine='python')
                return df_1.dropna(how='all').shape[0] >= 1
            except Exception as er:
                print(f"Error al leer el archivo {ruta_archivo}: {er}")
                return False
        archivos_validos = [
            os.path.join(self.path_Directory, archivo)
            for archivo in os.listdir(self.path_Directory)
            if "0001_Bach" in archivo and archivo.endswith('.csv')
        ]

        dataframes = []
        for ruta in archivos_validos:
            if tiene_filas_diligenciadas(ruta):
                try:
                    df = pd.read_csv(ruta, encoding='utf-8', engine='python')
                    dataframes.append(df)
                except Exception as e:
                    print(f"Error al procesar {ruta}: {e}")

        if not dataframes:
            print("No se encontraron archivos válidos para consolidar.")
            return "sin datos"

        df_consolidado = pd.concat(dataframes, ignore_index=True)

        df_consolidado['CUENTA'] = df_consolidado['CUENTA'].astype(str).apply(lambda x: x.replace('.0', '') if x.endswith('.0') else x)

        Num_items = df_consolidado[df_consolidado['DOC'] == "X"].shape[0]

        output_file = os.path.join(self.path_Directory, 'BACH_DescuentoNomina_' + self.case + '.txt')
        df_consolidado.to_csv(output_file, sep='\t', header=False, index=False)

        return str(Num_items)
