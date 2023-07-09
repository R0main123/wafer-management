import os
import pandas as pd
from openpyxl.reader.excel import load_workbook
from pymongo import MongoClient


def writeExcel(wafer):
    """
    This function takes a wafer_id in argument and writes Excel files with the measurements of the wafer in it.
    One file is created per type of Measurements. In a file, there is one sheet per die and the header of a column is structured as follows:

    Name of the structure
    Unit (V or A, A/cm^2, CS, RS, It)
    Values

    Files are registred in a folder named ExcelFiles, which is created if it doesn't exist.

    :param <wafer>: name of the wafer_id
    :return: None
    """
    if not os.path.exists("ExcelFiles"):
        os.makedirs("ExcelFiles")

    client = MongoClient('mongodb://localhost:27017/')  # Connexion to the database
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer})
    list_of_sheets = []  # List of sheets that already exist in the file, so we don't overwite an existing sheet
    df_dict = {}  # Dictionary which will store all values, so we just write all data once in the file

    wafer_id = wafer["wafer_id"]
    df_dict["I"] = {}  # We Create one dictionary per type of Measurements
    df_dict["J"] = {}
    df_dict["C"] = {}
    df_dict["It"] = {}

    for structure in wafer["structures"]:  # We browse all structures in the wafer
        structure_id = structure["structure_id"]

        for matrix in structure["matrices"]:  # We browse all matrices in the structure
            coord = "(" + matrix["coordinates"]["x"] + ',' + matrix["coordinates"]["y"] + ')'
            if coord not in df_dict.keys():
                df_dict[coord] = pd.DataFrame()

            for element in matrix["results"]:
                if element == "I":
                    if os.path.exists(f"ExcelFiles\\{wafer_id}_IV.xlsx"):
                        continue
                    if coord not in df_dict["I"]:
                        df_dict["I"][coord] = pd.DataFrame()

                    voltages = ['Voltage (V)']
                    I = ['I (A)']
                    for double in matrix["results"][element]["Values"]:  # We get all values
                        voltages.append(double["V"])
                        I.append(double["I"])

                    new_df = pd.DataFrame(list(zip(voltages, I)), columns=[structure_id, structure_id + " "])
                    df_dict["I"][coord] = df_dict["I"][coord].merge(new_df, left_index=True, right_index=True,
                                                                    how='outer')  # We add the new colums to the existing columns
                    I.clear()
                    voltages.clear()

                elif element == "J":
                    if coord not in df_dict["J"]:
                        df_dict["J"][coord] = pd.DataFrame()
                    if os.path.exists(f"ExcelFiles\\{wafer_id}_JV.xlsx"):
                        continue
                    voltages = ['Voltage (V)']
                    J = ['J (A/cm^2)']
                    for double in matrix["results"][element]["Values"]:
                        voltages.append(double["V"])
                        J.append(double["J"])

                    new_df = pd.DataFrame(list(zip(voltages, J)), columns=[structure_id, structure_id + " "])
                    df_dict["J"][coord] = df_dict["J"][coord].merge(new_df, left_index=True, right_index=True,
                                                                    how='outer')
                    J.clear()
                    voltages.clear()

                elif element == "C":
                    if os.path.exists(f"ExcelFiles\\{wafer_id}_CV.xlsx"):
                        continue

                    if coord not in df_dict["C"]:
                        df_dict["C"][coord] = pd.DataFrame()
                    voltages = ['Voltage (V)']
                    CS = ['CS (Ω)']
                    RS = ['RS (Ω)']
                    for double in matrix["results"][element]["Values"]:
                        voltages.append(double["V"])
                        CS.append(double["CS"])
                        RS.append(double["RS"])

                    new_df = pd.DataFrame(list(zip(voltages, CS, RS)),
                                          columns=[structure_id, structure_id + " ", structure_id + "  "])
                    df_dict["C"][coord] = df_dict["C"][coord].merge(new_df, left_index=True, right_index=True,
                                                                    how='outer')
                    voltages.clear()
                    CS.clear()
                    RS.clear()

                elif element == "It":
                    if os.path.exists(f"ExcelFiles\\{wafer_id}_TDDB.xlsx"):
                        continue
                    if coord not in df_dict["It"]:
                        df_dict["It"][coord] = pd.DataFrame()
                    voltages = ['Voltage (V)']
                    It = ['TDDB']
                    for double in matrix["results"][element]["Values"]:
                        voltages.append(double["V"])
                        It.append(double["TDDB"])

                    new_df = pd.DataFrame(list(zip(voltages, It)), columns=[structure_id, structure_id + " "])
                    df_dict["It"][coord] = df_dict["It"][coord].merge(new_df, left_index=True, right_index=True,
                                                                      how='outer')
                    voltages.clear()
                    It.clear()

    for element in ["I", "J", "C", "It"]:
        if df_dict[element] != {}:
            filename = 'ExcelFiles\\' + wafer_id + "_" + element + 'V.xlsx'  # We create the file

            pd.DataFrame().to_excel(filename, index=False)
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a',
                                if_sheet_exists='overlay') as writer:  # We write in the file
                for coord, df in df_dict[element].items():
                    sheetName = coord
                    if sheetName in list_of_sheets:
                        df.to_excel(writer, sheet_name=sheetName, index=False,
                                    startcol=writer.sheets[sheetName].max_column)
                    else:
                        df.to_excel(writer, sheet_name=sheetName, index=False)
                        list_of_sheets.append(sheetName)
            df_dict[element].clear()
            list_of_sheets.clear()

            wb = load_workbook(filename)
            if 'Sheet1' in wb.sheetnames:
                del wb['Sheet1']
            wb.save(filename)


def excel_structure(wafer_id=str, structure_ids=list, file_name=str):
    """
    This function takes a wafer_id, a list of structures and a filename in argument and writes Excel files with the measurements of the structures selected.
    One file is created per type of Measurements. In a file, there is one sheet per die and the header of a column is structured as follows:

    Name of the structure
    Unit (V or A, A/cm^2, CS, RS, It)
    Values

    Files are registred in a folder named ExcelFiles, which is created if it doesn't exist.

    This function is used to write excel only for selected structures in the User Interface

    :param <str> wafer_id: name of the wafer_id
    :param <list> structure_ids: List of str, contains all structure_id of the selected structures
    :param <str> file_name: Name of file which will be created

    :return: None
    """
    if not os.path.exists(wafer_id):
        os.makedirs(wafer_id)

    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    list_of_sheets = []
    df_dict = {}

    df_dict["I"] = {}
    df_dict["J"] = {}
    df_dict["C"] = {}
    df_dict["It"] = {}

    for structure in wafer["structures"]:
        if structure["structure_id"] in structure_ids:
            structure_id = structure["structure_id"]

            for matrix in structure["matrices"]:
                coord = "(" + matrix["coordinates"]["x"] + ',' + matrix["coordinates"]["y"] + ')'
                if coord not in df_dict.keys():
                    df_dict[coord] = pd.DataFrame()

                for element in matrix["results"]:
                    if element == "I":
                        if os.path.exists(f"{wafer_id}\\{file_name}_I-V.xlsx"):
                            continue
                        if coord not in df_dict["I"]:
                            df_dict["I"][coord] = pd.DataFrame()

                        voltages = ['Voltage (V)']
                        I = ['I (A)']
                        for double in matrix["results"][element]["Values"]:
                            voltages.append(double["V"])
                            I.append(double["I"])

                        new_df = pd.DataFrame(list(zip(voltages, I)), columns=[structure_id, structure_id + " "])
                        df_dict["I"][coord] = df_dict["I"][coord].merge(new_df, left_index=True, right_index=True,
                                                                        how='outer')
                        I.clear()
                        voltages.clear()

                    elif element == "J":
                        if coord not in df_dict["J"]:
                            df_dict["J"][coord] = pd.DataFrame()
                        if os.path.exists(f"{wafer_id}\\{file_name}_J-V.xlsx"):
                            continue
                        voltages = ['Voltage (V)']
                        J = ['J (A/cm^2)']
                        for double in matrix["results"][element]["Values"]:
                            voltages.append(double["V"])
                            J.append(double["J"])

                        new_df = pd.DataFrame(list(zip(voltages, J)), columns=[structure_id, structure_id + " "])
                        df_dict["J"][coord] = df_dict["J"][coord].merge(new_df, left_index=True, right_index=True,
                                                                        how='outer')
                        J.clear()
                        voltages.clear()

                    elif element == "C":
                        if os.path.exists(f"{wafer_id}\\{file_name}_C-V.xlsx"):
                            continue

                        if coord not in df_dict["C"]:
                            df_dict["C"][coord] = pd.DataFrame()
                        voltages = ['Voltage (V)']
                        CS = ['CS (Ω)']
                        RS = ['RS (Ω)']
                        for double in matrix["results"][element]["Values"]:
                            voltages.append(double["V"])
                            CS.append(double["CS"])
                            RS.append(double["RS"])

                        new_df = pd.DataFrame(list(zip(voltages, CS, RS)),
                                              columns=[structure_id, structure_id + " ", structure_id + "  "])
                        df_dict["C"][coord] = df_dict["C"][coord].merge(new_df, left_index=True, right_index=True,
                                                                        how='outer')
                        voltages.clear()
                        CS.clear()
                        RS.clear()

                    elif element == "It":
                        if os.path.exists(f"{wafer_id}\\{file_name}_It-V.xlsx"):
                            continue
                        if coord not in df_dict["It"]:
                            df_dict["It"][coord] = pd.DataFrame()
                        voltages = ['Voltage (V)']
                        It = ['TDDB']
                        for double in matrix["results"][element]["Values"]:
                            voltages.append(double["V"])
                            It.append(double["TDDB"])

                        new_df = pd.DataFrame(list(zip(voltages, It)), columns=[structure_id, structure_id + " "])
                        df_dict["It"][coord] = df_dict["It"][coord].merge(new_df, left_index=True, right_index=True,
                                                                          how='outer')
                        voltages.clear()
                        It.clear()

    for element in ["I", "J", "C", "It"]:
        if df_dict[element] != {}:

            filename = wafer_id +'\\' + file_name + "_" + element + '-V.xlsx'

            pd.DataFrame().to_excel(filename, index=False)
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                for coord, df in df_dict[element].items():
                    sheetName = coord
                    if sheetName in list_of_sheets:
                        df.to_excel(writer, sheet_name=sheetName, index=False,
                                    startcol=writer.sheets[sheetName].max_column)
                    else:
                        df.to_excel(writer, sheet_name=sheetName, index=False)
                        list_of_sheets.append(sheetName)
            df_dict[element].clear()
            list_of_sheets.clear()

            wb = load_workbook(filename)
            if 'Sheet1' in wb.sheetnames:
                del wb['Sheet1']
            wb.save(filename)
