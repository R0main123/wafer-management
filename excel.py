import os
import pandas as pd
from openpyxl.reader.excel import load_workbook
from pymongo import MongoClient
from getter import get_wafer


def wanted_excel(wafer_id, sessions, structures, types, Temps, Files, coords, file_name):
    if not os.path.exists(wafer_id):
        os.makedirs(wafer_id)
    wafer = get_wafer(wafer_id)
    list_of_sheets = []
    df_dict = {}

    df_dict["I"] = {}
    df_dict["J"] = {}
    df_dict["C"] = {}
    df_dict["It"] = {}

    for session in sessions:
        for structure_id in structures:
            if wafer[session].get(structure_id) is None:
                continue
            for matrix in wafer[session][structure_id]["matrices"]:
                coord = "(" + matrix["coordinates"]["x"] + ',' + matrix["coordinates"]["y"] + ')'
                if coord in coords:
                    if coord not in df_dict.keys():
                        df_dict[coord] = pd.DataFrame()
                    for type in matrix["results"]:
                        columns = [
                                      f"{structure_id} {' '.join(session.split(' ')[1:])} {coord} {matrix['results'][type]['Temperature']} {matrix['results'][type]['Filename']}"] + [
                                      f"{structure_id} {' '.join(session.split(' ')[1:])} {coord} {matrix['results'][type]['Temperature']} {matrix['results'][type]['Filename']}" + " "]

                        if matrix["results"][type]["Filename"] in Files and matrix["results"][type]["Temperature"] in Temps:
                            if type == "I" and 'I' in types:
                                if os.path.exists(f"{wafer_id}\\{file_name}_I-V.xlsx"):
                                    continue
                                if coord not in df_dict["I"]:
                                    df_dict["I"][coord] = pd.DataFrame()

                                voltages = [session, matrix["results"][type]["Temperature"], matrix["results"][type]["Filename"], 'Voltage (V)']
                                I = [session, matrix["results"][type]["Temperature"], matrix["results"][type]["Filename"], 'I (A)']
                                for double in matrix["results"][type]["Values"]:
                                    voltages.append(double["V"])
                                    I.append(double["I"])

                                new_df = pd.DataFrame(list(zip(voltages, I)), columns=columns)
                                df_dict["I"][coord] = df_dict["I"][coord].merge(new_df, left_index=True, right_index=True,
                                                                                how='outer')
                                I.clear()
                                voltages.clear()

                            elif type == "J" and 'J' in types:
                                if coord not in df_dict["J"]:
                                    df_dict["J"][coord] = pd.DataFrame()
                                if os.path.exists(f"{wafer_id}\\{file_name}_J-V.xlsx"):
                                    continue
                                voltages = [session, matrix["results"][type]["Temperature"], matrix["results"][type]["Filename"], 'Voltage (V)']
                                J = [session, matrix["results"][type]["Temperature"], matrix["results"][type]["Filename"], 'J (A/cm^2)']
                                for double in matrix["results"][type]["Values"]:
                                    voltages.append(double["V"])
                                    J.append(double["J"])

                                new_df = pd.DataFrame(list(zip(voltages, J)), columns=columns)
                                df_dict["J"][coord] = df_dict["J"][coord].merge(new_df, left_index=True, right_index=True,
                                                                                how='outer')
                                J.clear()
                                voltages.clear()

                            elif type == "C" and 'C' in types:
                                if os.path.exists(f"{wafer_id}\\{file_name}_C-V.xlsx"):
                                    continue

                                if coord not in df_dict["C"]:
                                    df_dict["C"][coord] = pd.DataFrame()
                                voltages = [session, matrix["results"][type]["Temperature"], matrix["results"][type]["Filename"], 'Voltage (V)']
                                CS = [session, matrix["results"][type]["Temperature"], matrix["results"][type]["Filename"], 'CS (Ω)']
                                RS = [session, matrix["results"][type]["Temperature"], matrix["results"][type]["Filename"], 'RS (Ω)']
                                for double in matrix["results"][type]["Values"]:
                                    voltages.append(double["V"])
                                    CS.append(double["CS"])
                                    RS.append(double["RS"])

                                new_df = pd.DataFrame(list(zip(voltages, CS, RS)),
                                                      columns=columns)
                                df_dict["C"][coord] = df_dict["C"][coord].merge(new_df, left_index=True, right_index=True,
                                                                                how='outer')
                                voltages.clear()
                                CS.clear()
                                RS.clear()

                            elif type == "It" and 'It' in types:
                                if os.path.exists(f"{wafer_id}\\{file_name}_It-V.xlsx"):
                                    continue
                                if coord not in df_dict["It"]:
                                    df_dict["It"][coord] = pd.DataFrame()
                                voltages = [session, matrix["results"][type]["Temperature"], matrix["results"][type]["Filename"], 'Voltage (V)']
                                It = [session, matrix["results"][type]["Temperature"], matrix["results"][type]["Filename"], 'TDDB']
                                for double in matrix["results"][type]["Values"]:
                                    voltages.append(double["V"])
                                    It.append(double["TDDB"])

                                new_df = pd.DataFrame(list(zip(voltages, It)), columns=columns)
                                df_dict["It"][coord] = df_dict["It"][coord].merge(new_df, left_index=True, right_index=True,
                                                                                  how='outer')
                                voltages.clear()
                                It.clear()

    for element in types:
        if df_dict[element] != {}:
            filename = wafer_id + '\\' + file_name + "_" + element + '-V.xlsx'

            pd.DataFrame().to_excel(filename, index=False)
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
                for coord, df in df_dict[element].items():
                    # Créez une copie de df et modifiez les noms de colonnes de la copie
                    df_copy = df.copy()
                    df_copy.columns = [col.split(' ')[0] for col in df_copy.columns]

                    sheetName = coord
                    if sheetName in list_of_sheets:
                        df_copy.to_excel(writer, sheet_name=sheetName, index=False,
                                         startcol=writer.sheets[sheetName].max_column)
                    else:
                        df_copy.to_excel(writer, sheet_name=sheetName, index=False)
                    list_of_sheets.append(sheetName)
                df_dict[element].clear()
            list_of_sheets.clear()

            wb = load_workbook(filename)
            if 'Sheet1' in wb.sheetnames:
                del wb['Sheet1']
            wb.save(filename)

