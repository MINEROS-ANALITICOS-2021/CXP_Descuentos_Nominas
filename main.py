import sys
import json

from Calendar.CalendarGnr import Calendar
from Validation.FormatZHR43 import Formats
from Bach.BachJudicial import Createbachjudicial
from Bach.BachPrestamos import Createbachprestamo
from Bach.BachSindical import Createbachsindical
from Testing.testingscript import Test1
from Validation.LoadCSV import DownloadCSV
from Validation.Reports_ZHR43 import CreateReportsZ
from Validation.Reports_FBL1N import CreateReportsF
from Validation.Reports_PDFBase import ReportsPDFBase
from Bach.BachConsolidate import Bachfinality
from Bach.BachGeneric import CreateBachGeneric
from Bach.BachFondoUnido import CreateBachFondoUnido
from CPDF.CreatePDF_1 import CreatePDF1
from CPDF.CreatePDF_AYUBI import CreatePDFAyubi
from CPDF.CreatePDF_SITRAENSA import CreatePDFSINTRAENSA
from CPDF.CreatePDF_FONDOUNIDO import CreatePDFFondounido
from CPDF.CreatePDF_BCH import CreatePDFBCH
from CPDF.CreatePDF_BI import CreatePDFBI
from Validation.Validation_Empty import ValidationFileEmpty

def shellHandler() -> None:
    """Interface for command shell class and scripts"""
    try:
        func_name = sys.argv[1]
        if func_name.strip() == "formatZHR43":
            path_Filereport = sys.argv[2]
            path_TypeDiscount = sys.argv[3]
            folder_path = sys.argv[4]

            formats= Formats(path_Filereport, path_TypeDiscount, folder_path)
            result = formats.ajustReportZHR43()
            print(json.dumps(result))

        elif func_name.strip() == "calendarGnr":
            calendar= Calendar()
            result = calendar.obtener_fechas()
            print(json.dumps(result))

        elif func_name.strip() == "bachjudiciales":
            path_Directory = sys.argv[2]
            path_FileReportJudicial = sys.argv[3]
            path_FileParaJudicial = sys.argv[4]
            path_FileTipoDescuento = sys.argv[5]
            FinMesAnt = sys.argv[6]
            dateBach = sys.argv[7]

            nonprejudicial= Createbachjudicial(path_Directory, path_FileReportJudicial, path_FileParaJudicial, path_FileTipoDescuento, FinMesAnt, dateBach)
            result = nonprejudicial.bachJudicial()
            print(json.dumps(result))

        elif func_name.strip() == "bachprestamos":
            path_Directory = sys.argv[2]
            path_FileReportDescuento = sys.argv[3]
            path_FileParametrica = sys.argv[4]
            Month = sys.argv[5]
            Year= sys.argv[6]
            FinMesAnt= sys.argv[7]
            dateBach = sys.argv[8]

            representational = Createbachprestamo(path_Directory, path_FileReportDescuento, path_FileParametrica, Month, Year, FinMesAnt, dateBach)
            result = representational.bachPrestamos()
            print(json.dumps(result))

        elif func_name.strip() == "bachfondounido":
            path_Directory = sys.argv[2]
            path_FileReportDescuento = sys.argv[3]
            path_FileParametrica = sys.argv[4]
            path_FileCeCo = sys.argv[5]
            Month = sys.argv[6]
            Year= sys.argv[7]
            FinMesAnt= sys.argv[8]
            dateBach = sys.argv[9]

            createbachfondounido = CreateBachFondoUnido(path_Directory, path_FileReportDescuento, path_FileParametrica, path_FileCeCo, Month, Year, FinMesAnt, dateBach)
            result = createbachfondounido.bachFondoUnido()
            print(json.dumps(result))

        elif func_name.strip() == "bachsindical":
            path_Directory = sys.argv[2]
            path_FileReportDescuento = sys.argv[3]
            path_FileParametrica = sys.argv[4]
            Month = sys.argv[5]
            Year= sys.argv[6]
            dateBach = sys.argv[7]

            createbachsindical= Createbachsindical(path_Directory, path_FileReportDescuento, path_FileParametrica, Month, Year, dateBach)
            result = createbachsindical.bachSindical()
            print(json.dumps(result))

        elif func_name.strip() == "testing":
            path_Directory = sys.argv[2]
            path_Filexlsx = sys.argv[3]

            test1= Test1(path_Directory, path_Filexlsx)
            result = test1.testingfile()
            print(json.dumps(result))

        elif func_name.strip() == "download_csv":
            path_Directory = sys.argv[2]
            path_Filexlsx = sys.argv[3]

            downloadCSV= DownloadCSV(path_Directory, path_Filexlsx)
            result = downloadCSV.loadCSV()
            print(json.dumps(result))

        elif func_name.strip() == "consolidateBach":
            path_Directory = sys.argv[2]
            case = sys.argv[3]

            bachfinality= Bachfinality(path_Directory, case)
            result = bachfinality.consolidate_Bach()
            print(json.dumps(result))

        elif func_name.strip() == "bachgeneric":
            path_Directory = sys.argv[2]
            file_Discount = sys.argv[3]
            file_parametrics = sys.argv[4]
            Month = sys.argv[5]
            Year= sys.argv[6]
            FinMesAnt= sys.argv[7]
            dateBach =sys.argv[8]

            createBachGeneric = CreateBachGeneric(path_Directory, file_Discount, file_parametrics, Month, Year, FinMesAnt, dateBach)
            result = createBachGeneric.bachGeneric()
            print(json.dumps(result))

        elif func_name.strip() == "createPDF1":
            path_Directory = sys.argv[2]
            file_Discount = sys.argv[3]

            createPDF1= CreatePDF1(path_Directory, file_Discount)
            result = createPDF1.procesar_csv()
            print(json.dumps(result))

        elif func_name.strip() == "createPDFAyubi":
            path_Receipts = sys.argv[2]
            file_ReportPDF = sys.argv[3]
            name_coord = sys.argv[4]

            createPDFAyubi= CreatePDFAyubi(path_Receipts, file_ReportPDF, name_coord)
            result = createPDFAyubi.clean_csv()
            print(json.dumps(result))

        elif func_name.strip() == "createPDFFondoUnido":
            path_Receipts = sys.argv[2]
            file_ReportPDF = sys.argv[3]
            name_coord = sys.argv[4]

            createPDFFondounido= CreatePDFFondounido(path_Receipts, file_ReportPDF, name_coord)
            result = createPDFFondounido.clean_csvFU()
            print(json.dumps(result))

        elif func_name.strip() == "createPDFSitraemsa":
            path_Receipts = sys.argv[2]
            file_report_FBL = sys.argv[3]
            file_Sintraemsa = sys.argv[4]
            NameCoordinador = sys.argv[5]

            createPDFSINTRAENSA= CreatePDFSINTRAENSA(path_Receipts, file_report_FBL, file_Sintraemsa, NameCoordinador)
            result = createPDFSINTRAENSA.clean_csv()
            print(json.dumps(result))

        elif func_name.strip() == "createPDFBCH":
            path_Receipts = sys.argv[2]
            file_ReportPDF = sys.argv[3]
            name_coord = sys.argv[4]

            createPDFBCH= CreatePDFBCH(path_Receipts, file_ReportPDF, name_coord)
            result = createPDFBCH.clean_csv()
            print(json.dumps(result))

        elif func_name.strip() == "createPDFBI":
            path_Receipts = sys.argv[2]
            file_ReportPDF = sys.argv[3]
            name_coord = sys.argv[4]

            createPDFBI= CreatePDFBI(path_Receipts, file_ReportPDF, name_coord)
            result = createPDFBI.clean_csv()
            print(json.dumps(result))

        elif func_name.strip() == "reportsZHR43":
            path_Directory = sys.argv[2]
            path_FileZHR43 = sys.argv[3]
            path_FileDiscount = sys.argv[4]
            path_FileJudicial = sys.argv[5]

            createReportsZ= CreateReportsZ(path_Directory, path_FileZHR43, path_FileDiscount, path_FileJudicial)
            result = createReportsZ.summaryReportZHR43()
            print(json.dumps(result))

        elif func_name.strip() == "reportsFBL1N":
            path_Directory = sys.argv[2]
            path_FileReport = sys.argv[3]
            user = sys.argv[4]
            date_Process = sys.argv[5]

            createReportsF= CreateReportsF(path_Directory, path_FileReport, user, date_Process)
            result = createReportsF.ajustReportFBL1N()
            print(json.dumps(result))

        elif func_name.strip() == "reportsPDF":
            fileValidation = sys.argv[2]
            path_fileEnd = sys.argv[3]
            path_discount = sys.argv[4]
            path_fileFBL1N = sys.argv[5]

            reportsPDFBase= ReportsPDFBase(fileValidation, path_fileEnd, path_discount, path_fileFBL1N)
            result = reportsPDFBase.summaryvsFBL1N()
            print(json.dumps(result))

        elif func_name.strip() == "validateEmpty":
            file_Validation = sys.argv[2]

            validationFileEmpty= ValidationFileEmpty(file_Validation)
            result = validationFileEmpty.validate_File_empty()
            print(json.dumps(result))

    except Exception as err:
        print(json.dumps({"error": True, "msj": "Error critico: "+str(err)}))


if __name__ == "__main__":
    shellHandler()
