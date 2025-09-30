from calendar import monthrange
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class Calendar:

    def obtener_fechas(self) -> dict:
        # Fecha actual y mes actual
        fecha_actual = datetime.now()
        dia_actual = fecha_actual.day
        mes_actual = fecha_actual.month
        year_actual = fecha_actual.year

        # Calcular fechas hace 3 meses y 1 mes usando relativedelta
        fecha_3_meses = fecha_actual - relativedelta(months=3)
        fecha_1_mes = fecha_actual - relativedelta(months=1)
        mes_anterior = fecha_1_mes.month
        year_mes_anterior = fecha_1_mes.year

        # Diccionario de meses en español
        meses_es = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }

        # Calcular Mes_anteriorFol
        mes_anterior_fol = f"{mes_anterior:02d}_{meses_es[mes_anterior]}"

        # Nombre corto del mes anterior
        nombre_mes_anterior = fecha_1_mes.strftime("%b")  # Ejemplo: "Jul"

        # Calcular el 10 del siguiente mes
        siguiente_mes = fecha_actual + relativedelta(months=1)
        dia_diez_siguiente_mes = date(siguiente_mes.year, siguiente_mes.month, 10)

        # Obtener primer y último día de los meses calculados
        _, ultimo_dia_3m = monthrange(fecha_3_meses.year, fecha_3_meses.month)
        _, ultimo_dia_1m = monthrange(fecha_1_mes.year, fecha_1_mes.month)
        _, ultimo_dia_actual = monthrange(year_actual, mes_actual)

        # Último día del mes anterior
        _, ultimo_dia_mes_anterior = monthrange(year_mes_anterior, mes_anterior)
        fecha_fin_mes_anterior = date(year_mes_anterior, mes_anterior, ultimo_dia_mes_anterior)
        fecha_fin_mes_anterior_str = fecha_fin_mes_anterior.strftime("%d%m%Y")

        # Crear objetos date para los rangos de fechas
        fecha_inicio_actual = date(year_actual, mes_actual, 1)
        fecha_fin_actual = date(year_actual, mes_actual, ultimo_dia_actual)
        fecha_inicio_3m = date(fecha_3_meses.year, fecha_3_meses.month, 1)
        fecha_fin_3m = date(fecha_3_meses.year, fecha_3_meses.month, ultimo_dia_3m)
        fecha_inicio_1m = date(fecha_1_mes.year, fecha_1_mes.month, 1)
        fecha_fin_1m = date(fecha_1_mes.year, fecha_1_mes.month, ultimo_dia_1m)
        return {
            "fecha_actual": fecha_actual.strftime("%d.%m.%Y"),
            "primera_quincena": f"10.{mes_actual:02d}.{year_actual}",
            "segunda_quincena": f"20.{mes_actual:02d}.{year_actual}",
            "dia_quince": f"15.{mes_actual:02d}.{year_actual}",
            "inicio_tres_meses": fecha_inicio_3m.strftime("%d.%m.%Y"),
            "fin_tres_meses": fecha_fin_3m.strftime("%d.%m.%Y"),
            "inicio_mes_anterior": fecha_inicio_1m.strftime("%d.%m.%Y"),
            "fin_mes_anterior": fecha_fin_1m.strftime("%d.%m.%Y"),
            "inicio_mes_actual": fecha_inicio_actual.strftime("%d.%m.%Y"),
            "fin_mes_actual": fecha_fin_actual.strftime("%d.%m.%Y"),
            "mes_actual": f"{mes_actual:02d}",
            "year_actual": f"{year_actual}",
            "dia_actual": f"{dia_actual}",
            "dia_diez_siguiente_mes": dia_diez_siguiente_mes.strftime("%d.%m.%Y"),
            "mes_anterior_letras": nombre_mes_anterior,
            "fin_mes_anterior_ddmmyyyy": fecha_fin_mes_anterior_str,
            "year_mes_anterior": str(year_mes_anterior),
            "Mes_anteriorFol": mes_anterior_fol
        }

