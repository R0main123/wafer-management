import gc
import io
import re

import pymongo
from pymongo import MongoClient

from getter import get_db_name
from split_data import spliter, dataSpliter, C_spliter, converter_split, converter_split_session
from VBD import calculate_breakdown, get_vectors_in_matrix


def create_db(path, is_JV):
    """
    Used to get information from .txt files.
    This function creates a database or open it if it already exists, and fill it with measurement information
    We put all the file's information in a dictionary, and then we write all the dictionary in the database, so we just call the db once.
    This is much faster.
    Also, indexes are created if they don't already exist, so searching in the database in faster

    :param <str> path: path of the file
    :param <bool> is_JV: True if the user wants to register J-V measurements, False otherwise

    :return <list>: a list containing all wafers that have been registered
    """

    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    db_name = get_db_name()

    db[db_name].create_index('wafer_id')

    collection = db[db_name]

    filename = path.split("\\")[-1].split(".")[0]

    session = None


    if not filename.startswith("AL"): #We parse the filename to get the wafer_id and the original filename
        wafer_id = filename.split("@@@")[-1].split("_")[0] + "_" + filename.split("@@@")[-1].split("_")[1]
        temperature = filename.split("@@@")[-1].split("_")[-1]
        filename = filename.split("@@@")[0]
    else:
        wafer_id = filename.split("_")[0] + "_" + filename.split("_")[1]
        temperature = filename.split("_")[-1]
        filename = '_'.join(filename.split("_")[:-1])

    list_of_wafers = set()
    print(f"Creating/opening database for {filename}")

    db_buffer = {} #We create a dictionary to store all datas, so we write just once in the database, this is much faster

    with io.open(path, 'r', 128*128) as file: #We read the file and clear the memory every 128ko so there is no preasure on the memory
        for reader in file:
            if 'SaMPy' in reader:
                create_db_it(path)
                return
            if 'BOD' in reader:
                break

    with io.open(path, 'r', 128 * 128) as file:  # We read the file and clear the memory every 128ko so there is no preasure on the memory
        i = 1
        while True:
            IV = False
            JV = False
            CV = False
            It = False

            if wafer_id not in list_of_wafers:
                list_of_wafers.add(wafer_id)
                print(list_of_wafers)

            line = next((l for l in file if 'chipX' in l), None) # We get all needed information
            if not line:
                break
            chipX = spliter(line)

            line = next((l for l in file if 'chipY' in l), None)
            if not line:
                break
            chipY = spliter(line)

            line = next((l for l in file if 'testdeviceID' in l), None)
            if not line:
                break
            testdeviceID = spliter(line)

            if testdeviceID.startswith('TDDB_') or testdeviceID.startswith('TDDB-'):
                testdeviceID = testdeviceID[5:]

            if re.search(r'-BEOL.{1,3}$', testdeviceID):
                testdeviceID = re.sub(r'-BEOL.{1,3}$', '', testdeviceID)

            if is_JV:
                line = next((l for l in file if 'testdeviceArea' in l), None)
                if not line:
                    break
                area = float(spliter(line))

            line = next((l for l in file if 'procedureName' in l), None)
            if not line:
                break
            procedure = spliter(line)

            if procedure == "oxide_breakdown":
                IV = True
                if is_JV:
                    JV = True
            elif "cv" in procedure: CV = True
            elif "it" in procedure: It = True
            else:
                IV = True
                if is_JV:
                    JV = True

            if It:
                line = next((l for l in file if 'voltage' in l), None)
                if not line:
                    break
                volt = float(spliter(line).split()[0])

                line = next((l for l in file if 'current compliance' in l), None)
                if not line:
                    break
                curr_compl = float(spliter(line).split()[0])


            if session is None:
                line = next((l for l in file if 'date' in l), None)
                if not line:
                    break
                session = spliter(line)
                session = session.split(' ')
                for x in session.copy():
                    if ":" in x:
                        session.remove(x)
                session = ' '.join(session[1:])
                session = f'{filename} {session}'

            if IV:
                result1_values = []
                result2_values = []
                line = next((l for l in file if 'BOD' in l), None)
                if not line:
                    break

                # Collecting measures values
                for line in file:
                    if 'EOD' in line:
                        break
                    data = dataSpliter(line)
                    result1_values.append((data[0], data[1]))

                result_1 = [{"V": v, "I": i} for v, i in result1_values]

                if JV:
                    for double in result1_values:
                        result2_values.append((float(double[0]), float(double[1]) / area))
                    result_2 = [{"V": v, "J": j} for v, j in result2_values]

            elif CV:
                line = next((l for l in file if 'curveValue' in l), None)
                if not line:
                    break
                V1 = C_spliter(line)[0]
                V2 = C_spliter(line)[-1]

                result_c_values = []
                line = next((l for l in file if 'BOD' in l), None)
                if not line:
                    break

                # Collecting measures values
                for line in file:
                    if 'EOD' in line:
                        break
                    data = dataSpliter(line)
                    result_c_values.append((data[0], data[1], data[2]))
                result_c = [{"V": v, f"{V1}": cs, f"{V2}": rs} for v, cs, rs in result_c_values]

            elif It:
                result_it_values = []
                line = next((l for l in file if 'BOD' in l), None)
                if not line:
                    break

                # Collecting measures values
                for line in file:
                    if 'EOD' in line:
                        break
                    data = dataSpliter(line)
                    result_it_values.append((data[0], data[1]))
                result_it = [{"t (s)": v, "It": abs(it)} for v, it in result_it_values]
                It0 = result_it_values[0][1]

                for doublets in reversed(result_it):
                    if doublets["It"] < curr_compl:
                        TTF = doublets['t (s)']
                        ITTF = doublets['It']
                        break

            # We search for the wafer we are studying. If it doesn't exist, we create it
            if wafer_id not in db_buffer:
                wafer_checker = collection.find_one({"wafer_id": wafer_id})
                if wafer_checker is None:
                    db_buffer[wafer_id] = {"wafer_id": wafer_id}
                else:
                    db_buffer[wafer_id] = wafer_checker

            wafer = db_buffer[wafer_id]

            date = wafer.get(session)

            if date is None:
                wafer[session] = {}
                if IV:
                    wafer[session]['Compliance'] = 1e-3
                wafer[session][testdeviceID] = {"matrices": []}
                matrix_id = "die_1"

            else:
                if IV and wafer[session].get("Compliance") is None:
                    wafer[session]["Compliance"] = 1e-3

                structure = wafer[session].get(testdeviceID)

                # If the structure does not exist in the wafer, create a new structure
                if structure is None:
                    wafer[session][testdeviceID] = {"matrices": []}
                    matrix_id = "die_1"
                else:
                    # If the structure already exists, calculate the new matrix_id
                    matrix_ids = [int(matrix["matrix_id"].split('_')[-1]) for matrix in structure["matrices"]]
                    matrix_id = f"die_{max(matrix_ids) + 1}"

            # Now, structure refers to the structure we want to update/add in the wafer
            # Try to find the matrix we want to update/add in the structure
            matrix = next(
                (m for m in wafer[session][testdeviceID]["matrices"] if m["coordinates"]["x"] == chipX and m["coordinates"]["y"] == chipY),
                None)

            # If the matrix does not exist in the structure, create a new matrix
            if matrix is None:
                if IV:
                    matrix = {"matrix_id": matrix_id, 'VBD': calculate_breakdown([result["V"] for result in result_1], [result["I"] for result in result_1], 1e-3)[0], "coordinates": {"x": chipX, "y": chipY}, "results": {}}
                elif It:
                    matrix = {"matrix_id": matrix_id, "stress voltage": volt, "current compliance": curr_compl, "It0": It0, "TTF": TTF, "ITTF": ITTF, "coordinates": {"x": chipX, "y": chipY}, "results": {}}
                else:
                    matrix = {"matrix_id": matrix_id, "coordinates": {"x": chipX, "y": chipY}, "results": {}}
                wafer[session][testdeviceID]["matrices"].append(matrix)


            # Now, matrix refers to the matrix we want to update/add in the structure
            # Update/add the results in the matrix
            if IV:
                if JV:
                    if matrix.get('VBD') is None:
                        matrix['VBD'] = calculate_breakdown([result["V"] for result in result_1], [result["I"] for result in result_1], 1e-3)[0]

                    matrix["results"]["I"] = {"Type of meas": "I-V", "Temperature": temperature, "Filename": filename, "Values": result_1}
                    matrix["results"]["J"] = {"Type of meas": "J-V", "Temperature": temperature, "Filename": filename, "Values": result_2}
                else:
                    if matrix.get('VBD') is None:
                        matrix['VBD'] = calculate_breakdown([result["V"] for result in result_1], [result["I"] for result in result_1], 1e-3)[0]

                    matrix["results"]["I"] = {"Type of meas": "I-V", "Temperature": temperature, "Filename": filename, "Values": result_1}
            elif CV:
                matrix["results"]["C"] = {"Type of meas": f"V-{V1}-{V2}", "Temperature": temperature, "Filename": filename, "Values": result_c}
            elif It:
                matrix["results"]["It"] = {"Type of meas": "V-TDDB", "Temperature": temperature, "Filename": filename, "Values": result_it}

            # Finally, replace the existing wafer document in the database with our updated wafer document
            # Or if the wafer did not exist in the database, this will create a new wafer document
            db_buffer[wafer_id] = wafer

            i += 1
            gc.collect()
    print("Finished procesing file")

    for wafer_id, wafer in db_buffer.items():
        collection.replace_one({"wafer_id": wafer_id}, wafer, upsert=True)

    print("Finish writing in the db")

    print(f"Sucessfully created database for {filename}")
    return list_of_wafers


def create_db_it(path):
    """
    Used to get information from .txt files that contain data for It measurements.
    This function creates a database or open it if it already exists, and fill it with measurement information
    We put all the file's information in a dictionary, and then we write all the dictionary in the database, so we just call the db once.
    This is much faster.
    Also, indexes are created if they don't already exist, so searching in the database in faster

    :param <str> path: path of the file

    :return <list>: a list containing all wafers that have been registered
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    db_name = get_db_name()

    db[db_name].create_index('wafer_id')

    collection = db[db_name]

    filename = path.split("\\")[-1].split(".")[0]

    session = None

    if not filename.startswith("AL"):  # We parse the filename to get the wafer_id and the original filename
        wafer_id = filename.split("@@@")[-1].split("_")[0] + "_" + filename.split("@@@")[-1].split("_")[1]
        temperature = filename.split("@@@")[-1].split("_")[-1]
        filename = filename.split("@@@")[0]
    else:
        wafer_id = filename.split("_")[0] + "_" + filename.split("_")[1]
        temperature = filename.split("_")[-1]
        filename = '_'.join(filename.split("_")[:-1])

    list_of_wafers = set()
    print(f"Creating/opening database for {filename}")

    db_buffer = {}  # We create a dictionary to store all datas, so we write just once in the database, this is much faster

    with io.open(path, 'r', 128 * 128) as file:
        while True:
            if wafer_id not in list_of_wafers:
                list_of_wafers.add(wafer_id)
                print(list_of_wafers)

            line = next((l for l in file if 'chipX' in l), None)  # We get all needed information
            if not line:
                break
            chipX = spliter(line)

            line = next((l for l in file if 'chipY' in l), None)
            if not line:
                break
            chipY = spliter(line)

            line = next((l for l in file if 'date' in l), None)
            if not line:
                break
            session = spliter(line)
            session = session.split()[0]
            session = session.split('-')
            calendar = {"1": "Jan", "2": "Feb", "3": "Mar", "4": "Apr", "5": "May", "6": "Jun", "7": "Jul", "8": "Aug", "9": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
            if session[1].startswith('0'):
                session[1] = session[1][1:]

            if session[2].startswith('0'):
                session[2] = session[2][1:]

            session = f'{filename} {calendar[session[1]]} {session[2]} {session[0]}'

            line = next((l for l in file if 'testdeviceID' in l), None)
            if not line:
                break
            testdeviceID = spliter(line)

            if testdeviceID.startswith('TDDB_') or testdeviceID.startswith('TDDB-'):
                testdeviceID = testdeviceID[5:]

            if re.search(r'-BEOL.{1,3}$', testdeviceID):
                testdeviceID = re.sub(r'-BEOL.{1,3}$', '', testdeviceID)

            line = next((l for l in file if 'compliance_value' in l), None)
            if not line:
                break
            curr_compl = float(spliter(line))

            line = next((l for l in file if 'nr_samples_after_compliance' in l), None)
            if not line:
                break
            nbr_sampl = int(spliter(line))

            line = next((l for l in file if l.split(' : ')[0] == 'voltage' in l), None)
            if not line:
                break
            volt = float(spliter(line).split()[0])

            result_it_values = []
            line = next((l for l in file if 'BOD' in l), None)
            if not line:
                break

            # Collecting measures values
            for line in file:
                if 'EOD' in line:
                    break
                data = dataSpliter(line)
                result_it_values.append((data[0], data[1]))
            result_it = [{"t (s)": v, "It": abs(it)} for v, it in result_it_values]
            It0 = result_it_values[0][1]

            TTF = result_it[-(nbr_sampl + 1)]['t (s)']
            ITTF = result_it[-(nbr_sampl + 1)]['It']

            if wafer_id not in db_buffer:
                wafer_checker = collection.find_one({"wafer_id": wafer_id})
                if wafer_checker is None:
                    db_buffer[wafer_id] = {"wafer_id": wafer_id}
                else:
                    db_buffer[wafer_id] = wafer_checker

            wafer = db_buffer[wafer_id]

            date = wafer.get(session)

            if date is None:
                wafer[session] = {}
                wafer[session][testdeviceID] = {"matrices": []}
                matrix_id = "die_1"

            else:
                structure = wafer[session].get(testdeviceID)

                # If the structure does not exist in the wafer, create a new structure
                if structure is None:
                    wafer[session][testdeviceID] = {"matrices": []}
                    matrix_id = "die_1"

                else:
                    # If the structure already exists, calculate the new matrix_id
                    matrix_ids = [int(matrix["matrix_id"].split('_')[-1]) for matrix in structure["matrices"]]
                    matrix_id = f"die_{max(matrix_ids) + 1}"

            # Now, structure refers to the structure we want to update/add in the wafer
            # Try to find the matrix we want to update/add in the structure
            matrix = next(
                (m for m in wafer[session][testdeviceID]["matrices"] if
                 m["coordinates"]["x"] == chipX and m["coordinates"]["y"] == chipY),
                None)

            # If the matrix does not exist in the structure, create a new matrix
            if matrix is None:
                matrix = {"matrix_id": matrix_id, "stress voltage": volt, "current compliance": curr_compl,
                          "It0": It0, "TTF": TTF, "ITTF": ITTF, "coordinates": {"x": chipX, "y": chipY}, "results": {}}
                wafer[session][testdeviceID]["matrices"].append(matrix)

            matrix["results"]["It"] = {"Type of meas": "V-TDDB", "Temperature": temperature, "Filename": filename,
                                       "Values": result_it}


            # Finally, replace the existing wafer document in the database with our updated wafer document
            # Or if the wafer did not exist in the database, this will create a new wafer document
            db_buffer[wafer_id] = wafer
            gc.collect()
        print("Finished procesing file")

        for wafer_id, wafer in db_buffer.items():
            collection.replace_one({"wafer_id": wafer_id}, wafer, upsert=True)

        print("Finish writing in the db")

        print(f"Sucessfully created database for {filename}")
        return list_of_wafers


def setCompliance(waferId, session, compliance):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db[get_db_name()]

    compliance = float(compliance)

    wafer = collection.find_one({"wafer_id": waferId})
    wafer[session]['Compliance'] = compliance
    for structure in wafer[session]:
        if structure == "Compliance":
            continue
        for matrix in wafer[session][structure]['matrices']:
            X, Y = get_vectors_in_matrix(waferId, session, structure, matrix['coordinates']['x'], matrix['coordinates']['y'])
            matrix['VBD'] = calculate_breakdown(X, Y, compliance)[0]

    collection.replace_one({"wafer_id": waferId}, wafer, upsert=True)

    client.close()


def create_db_tbl(path, is_JV):
    """
    Used to get information from .tbl files.
    This function creates a database or open it if it already exists, and fill it with measurement information
    We put all the file's information in a dictionary, and then we write all the dictionary in the database, so we just call the db once.
    This is much faster.
    Also, indexes are created if they don't already exist, so searching in the database in faster

    :param <str> path: path of the file
    :param <bool> is_JV: True if the user wants to register J-V measurements, False otherwise

    :return <list>: a list containing all wafers that have been registered
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    db_name = get_db_name()

    db[db_name].create_index('wafer_id')

    collection = db[db_name]

    filename = path.split("\\")[-1].split(".")[0]

    session = None

    if not filename.startswith("AL"):  # We parse the filename to get the wafer_id and the original filename
        wafer_id = filename.split("@@@")[-1].split("_")[0] + "_" + filename.split("@@@")[-1].split("_")[1]
        temperature = filename.split("@@@")[-1].split("_")[-1]
        filename = filename.split("@@@")[0]
    else:
        wafer_id = filename.split("_")[0] + "_" + filename.split("_")[1]
        temperature = filename.split("_")[-1]
        filename = '_'.join(filename.split("_")[:-1])

    list_of_wafers = set()
    print(f"Creating/opening database for {filename}")

    db_buffer = {}

    with io.open(path, 'r', 128 * 128) as file:
        i = 1
        while True:
            IV = False
            JV = False
            CV = False
            It = False

            if wafer_id not in list_of_wafers:
                list_of_wafers.add(wafer_id)
                print(list_of_wafers)

            line = next((l for l in file if '("chipX" ' in l), None)  # We get all needed information
            if not line:
                break
            chipX = converter_split(line)

            line = next((l for l in file if '("chipY" ' in l), None)
            if not line:
                break
            chipY = converter_split(line)

            line = next((l for l in file if '("testdeviceID" ' in l), None)
            if not line:
                break
            testdeviceID = converter_split(line)

            if testdeviceID.startswith('TDDB_') or testdeviceID.startswith('TDDB-'):
                testdeviceID = testdeviceID[5:]

            if re.search(r'-BEOL.{1,3}$', testdeviceID):
                testdeviceID = re.sub(r'-BEOL.{1,3}$', '', testdeviceID)

            if is_JV:
                line = next((l for l in file if '("testdeviceArea" ' in l), None)
                if not line:
                    break
                area = float(converter_split(line))

            line = next((l for l in file if '("procedureName" ' in l), None)
            if not line:
                break
            procedure = converter_split(line)

            if procedure == "oxide_breakdown":
                IV = True
                if is_JV:
                    JV = True
            elif "cv" in procedure:
                CV = True
            elif "it" in procedure:
                It = True
            else:
                IV = True
                if is_JV:
                    JV = True

            if session is None:
                line = next((l for l in file if 'date' in l), None)
                if not line:
                    break
                session = converter_split_session(line)

                for x in session.copy():
                    if ":" in x or x == '':
                        session.remove(x)

                session = ' '.join(session[2:])
                session = session[:-1]
                session = f'{filename} {session}'

            if IV:
                line = next((l for l in file if '"sweepValue" ' in l), None)
                if not line:
                    break

                voltages = line.split()[1:]
                voltages[-1] = voltages[-1][:-1]

                line = next((l for l in file), None)

                currents = []
                currents.append(line.split()[1])

                # Collecting measures values
                for line in file:
                    if line.split() == [')']:
                        break
                    currents.append(line.split()[0])

                result_1 = [{"V": float(voltages[i]), "I": float(currents[i])} for i in range(len(voltages))]

                if JV:
                    currents_densities = [float(current) / area for current in currents]
                    result_2 = [{"V": float(voltages[i]), "J": float(currents_densities[i])} for i in range(len(voltages))]

            elif CV:
                line = next((l for l in file if '"sweepValue" ' in l), None)
                if not line:
                    break

                voltages = line.split()[1:]
                voltages[-1] = voltages[-1][:-1]

                line = next((l for l in file), None)

                CS = []
                RS = []
                CS.append(line.split()[1])
                RS.append(line.split()[2])

                for line in file:
                    if line.split() == [')']:
                        break
                    CS.append(line.split()[0])
                    RS.append(line.split()[1])

                if RS[-1][-1] ==')':
                    RS[-1] = RS[-1][:-1]

                result_c = [{"V": float(voltages[i]), "CS": float(CS[i]), "RS": float(RS[i])} for i in range(len(voltages))]

            elif It:
                line = next((l for l in file if '"sweepValue" ' in l), None)
                if not line:
                    break

                voltages = line.split()[1:]
                voltages[-1] = voltages[-1][:-1]

                line = next((l for l in file), None)

                currents = []
                currents.append(line.split()[1])

                # Collecting measures values
                for line in file:
                    if line.split() == [')']:
                        break
                    currents.append(line.split()[0])

                result_it = [{"t (s)": float(voltages[i]), "It": float(currents[i])} for i in range(len(voltages))]

            # We search for the wafer we are studying. If it doesn't exist, we create it
            if wafer_id not in db_buffer:
                wafer_checker = collection.find_one({"wafer_id": wafer_id})
                if wafer_checker is None:
                    db_buffer[wafer_id] = {"wafer_id": wafer_id}
                else:
                    db_buffer[wafer_id] = wafer_checker

            wafer = db_buffer[wafer_id]

            # Try to find the structure we want to update/add in the wafer document
            date = wafer.get(session)

            if date is None:
                wafer[session] = {}
                if IV:
                    wafer[session]['Compliance'] = 1e-3
                wafer[session][testdeviceID] = {"matrices": []}
                matrix_id = "die_1"

            else:
                if IV and wafer[session].get("Compliance") is None:
                    wafer[session]["Compliance"] = 1e-3
                structure = wafer[session].get(testdeviceID)

                # If the structure does not exist in the wafer, create a new structure
                if structure is None:
                    wafer[session][testdeviceID] = {"matrices": []}
                    matrix_id = "die_1"
                else:
                    # If the structure already exists, calculate the new matrix_id
                    matrix_ids = [int(matrix["matrix_id"].split('_')[-1]) for matrix in structure["matrices"]]
                    matrix_id = f"die_{max(matrix_ids) + 1}"

            # Now, structure refers to the structure we want to update/add in the wafer
            # Try to find the matrix we want to update/add in the structure
            matrix = next(
                (m for m in wafer[session][testdeviceID]["matrices"] if
                 m["coordinates"]["x"] == chipX and m["coordinates"]["y"] == chipY),
                None)

            # If the matrix does not exist in the structure, create a new matrix
            if matrix is None:
                if IV:
                    matrix = {"matrix_id": matrix_id, "coordinates": {"x": chipX, "y": chipY},
                              'VBD': calculate_breakdown([result["V"] for result in result_1],
                                                         [result["I"] for result in result_1], 1e-3)[0], "results": {}}
                else:
                    matrix = {"matrix_id": matrix_id, "coordinates": {"x": chipX, "y": chipY}, "results": {}}
                wafer[session][testdeviceID]["matrices"].append(matrix)

            # Now, matrix refers to the matrix we want to update/add in the structure
            # Update/add the results in the matrix
            if IV:
                if JV:
                    if matrix.get('VBD') is None:
                        matrix['VBD'] = calculate_breakdown([result["V"] for result in result_1],
                                                            [result["I"] for result in result_1], 1e-3)[0]

                    matrix["results"]["I"] = {"Type of meas": "I-V", "Temperature": temperature, "Filename": filename,
                                              "Values": result_1}
                    matrix["results"]["J"] = {"Type of meas": "J-V", "Temperature": temperature, "Filename": filename,
                                              "Values": result_2}
                else:
                    if matrix.get('VBD') is None:
                        matrix['VBD'] = calculate_breakdown([result["V"] for result in result_1],
                                                            [result["I"] for result in result_1], 1e-3)[0]

                    matrix["results"]["I"] = {"Type of meas": "I-V", "Temperature": temperature, "Filename": filename,
                                              "Values": result_1}
            elif CV:
                matrix["results"]["C"] = {"Type of meas": f"V-CS-RS", "Temperature": temperature,
                                          "Filename": filename, "Values": result_c}
            elif It:
                matrix["results"]["It"] = {"Type of meas": "V-TDDB", "Temperature": temperature, "Filename": filename,
                                           "Values": result_it}

            # Finally, replace the existing wafer document in the database with our updated wafer document
            # Or if the wafer did not exist in the database, this will create a new wafer document
            db_buffer[wafer_id] = wafer

            i += 1
            gc.collect()
    print("Finished procesing file")

    for wafer_id, wafer in db_buffer.items():
        collection.replace_one({"wafer_id": wafer_id}, wafer, upsert=True)

    print("Finish writing in the db")

    print(f"Sucessfully created database for {filename}")
    return list_of_wafers


def create_db_lim(path):
    """
    Used to get information from .lim files.
    First, we read the lim file and get all information from it in a list.
    Then, we read the file without extension and merge information from both files.
    Finally, we write it in the database.

    :param <str> path: path of the file
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    db_name = get_db_name()

    db[db_name].create_index('wafer_id')

    collection = db[db_name]

    filename = path.split("\\")[-1].split(".")[0]

    session = None

    if not filename.startswith("AL"):  # We parse the filename to get the wafer_id and the original filename
        wafer_id = filename.split("@@@")[-1].split("_")[0] + "_" + filename.split("@@@")[-1].split("_")[1]
        temperature = filename.split("@@@")[-1].split("_")[-1]
    else:
        wafer_id = filename.split("_")[0] + "_" + filename.split("_")[1]
        temperature = filename.split("_")[-1]

    original_filename = filename.split('@@@')[0]

    list_of_wafers = set()
    print(f"Creating/opening database for {filename}")
    infos = []

    with io.open(path, 'r', 128 * 128) as file:  # We read the file and clear the memory every 128ko so there is no preasure on the memory
        for line in file:
            current_line = [element for element in line.split('  ') if element != '']
            testdeviceID = current_line[1]

            if testdeviceID.startswith('TDDB_') or testdeviceID.startswith('TDDB-'):
                testdeviceID = testdeviceID[5:]

            if re.search(r'-BEOL.{1,3}$', testdeviceID):
                testdeviceID = re.sub(r'-BEOL.{1,3}$', '', testdeviceID)

            if 'check_probecard' in current_line[0]:
                infos.append({'type': 'No', 'structure': testdeviceID})

            elif 'leakage' in current_line[0]:
                infos.append({'type': 'Leak', 'structure': testdeviceID})

            elif 'capacitor' in current_line[0]:
                if 'measured capacitance' in current_line[0]:
                    infos.append({'type': 'Cmes', 'structure': testdeviceID})
                else:
                    infos.append({'type': 'C', 'structure': testdeviceID})

            elif 'resistance' in current_line[0]:
                infos.append({'type': 'R', 'structure': testdeviceID})

            elif 'oxide_breakdown' in current_line[0]:
                return

    start_position = 0

    while infos[start_position]['type'] == 'No':
        start_position += 1

    wafer = collection.find_one({"wafer_id": wafer_id})
    if wafer is None:
        wafer = {'wafer_id': wafer_id}

    with io.open(f"DataFiles\\{filename}", 'r', 128 * 128) as file:
        line = next((l for l in file if 'SAS DATE' in l), None)
        original_date = line.split(' = ')[-1][:-1].split(':')[0]
        date = f"{original_date[2:5]} {original_date[:2] if original_date[0] !='0' else original_date[1]} {original_date[5:]}"
        session = f"{original_filename} {date}"


        date = wafer.get(session)
        if date is None:
            wafer[session] = {}

        line = next((l for l in file if 'BOD' in l), None)
        line = next((l for l in file), None)

        while 'EOD' not in line:
            datas = []
            x = line.split(' ')[0]
            y = line.split(' ')[1]
            line = next((l for l in file), None)

            while line.startswith(original_date):
                for data in line.split(' ')[1:]:
                    if data != '\n':
                        datas.append(float(data))

                line = next((l for l in file), None)

            for i in range(start_position, min(len(datas), len(infos))):
                structure = infos[i]['structure']
                typ = infos[i]['type']

                if typ != 'C' and typ != 'Cmes':
                    if wafer[session].get(structure) is None:
                        wafer[session][structure] = {}
                        wafer[session][structure]['matrices'] = []
                        matrix = {"matrix_id": 'die_1', typ: datas[i], "coordinates": {"x": x, "y": y}, "results": {}}
                        wafer[session][structure]['matrices'].append(matrix)

                    else:
                        found = False
                        for matrix in wafer[session][structure]['matrices']:
                            if matrix['coordinates']['x'] == x and matrix['coordinates']['y'] == y:
                                matrix[typ] = datas[i]
                                found = True
                                break
                        if not found:
                            matrix_ids = [int(matrix["matrix_id"].split('_')[-1]) for matrix in
                                          wafer[session][structure]["matrices"]]
                            matrix_id = f"die_{max(matrix_ids) + 1}"

                            matrix = {"matrix_id": matrix_id, "coordinates": {"x": x, "y": y}, typ: datas[i],
                                      "results": {}}

                            wafer[session][structure]['matrices'].append(matrix)

                else:
                    if wafer[session].get(structure) is None:
                        wafer[session][structure] = {}
                        wafer[session][structure]['matrices'] = []
                        matrix = {"matrix_id": 'die_1', "coordinates": {"x": x, "y": y}, 'Cap': {typ: datas[i]}}
                        wafer[session][structure]['matrices'].append(matrix)

                    else:
                        found = False
                        for matrix in wafer[session][structure]['matrices']:
                            if matrix['coordinates']['x'] == x and matrix['coordinates']['y'] == y:
                                if matrix.get('Cap') is None:
                                    matrix['Cap'] = {typ: datas[i]}
                                else:
                                    matrix['Cap'][typ] = datas[i]
                                found = True
                                break

                        if not found:
                            matrix_ids = [int(matrix["matrix_id"].split('_')[-1]) for matrix in
                                          wafer[session][structure]["matrices"]]
                            matrix_id = f"die_{max(matrix_ids) + 1}"

                            matrix = {"matrix_id": matrix_id, "coordinates": {"x": x, "y": y}, 'Cap': {typ: datas[i]}}

                            wafer[session][structure]['matrices'].append(matrix)

    collection.replace_one({"wafer_id": wafer_id}, wafer, upsert=True)
