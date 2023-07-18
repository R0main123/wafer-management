import gc
import io

import pymongo
from pymongo import MongoClient
from split_data import spliter, dataSpliter, C_spliter, converter_split, converter_split_session


def get_db_name(db_name="New Wafers"):
    return db_name


def create_db(path=str, is_JV=bool):

    """
    This function create a database or open it if it already exists, and fill it with measurement information
    We put all the file's information in a dictionary and then we write all the dictionary in the database, so we just call the db once>
    This is much faster

    :param <str> path: path of the file
    :param <bool> is_JV: True if the user wants to register J-V measurements, False otherwise
    :return <list>: a list containing all wafers that have been registered
    """

    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    db_name = get_db_name()

    db[db_name].create_index('wafer_id')
    db[db_name].create_index('session')
    db[db_name].create_index('testDeviceID')
    db[db_name].create_index('matrices.coordinates')
    db[db_name].create_index('results.Filename')
    db[db_name].create_index('results.Temperature')
    db[db_name].create_index('results.Values')
    db[db_name].create_index([('wafer_id', pymongo.ASCENDING), ('matrices.coordinates', pymongo.ASCENDING)])

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
                    JV=True
            elif "cv" in procedure: CV = True
            elif "it" in procedure: It = True
            else:
                IV = True
                if is_JV:
                    JV = True

            if session is None:
                line = next((l for l in file if 'date' in l), None)
                if not line:
                    break
                session = spliter(line)
                session = session.split(' ')
                for x in session.copy():
                    if ":" in x:
                        session.remove(x)
                session = ' '.join(session)
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
                result_it = [{"V": v, "It": it} for v, it in result_it_values]

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
                wafer[session]['Compliance'] = 1e-3
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
                (m for m in wafer[session][testdeviceID]["matrices"] if m["coordinates"]["x"] == chipX and m["coordinates"]["y"] == chipY),
                None)

            # If the matrix does not exist in the structure, create a new matrix
            if matrix is None:
                matrix = {"matrix_id": matrix_id, "coordinates": {"x": chipX, "y": chipY}, "results": {}}
                wafer[session][testdeviceID]["matrices"].append(matrix)


            # Now, matrix refers to the matrix we want to update/add in the structure
            # Update/add the results in the matrix
            if IV:
                if JV:
                    matrix["results"]["I"] = {"Type of meas": "I-V", "Temperature": temperature, "Filename": filename, "Values": result_1}
                    matrix["results"]["J"] = {"Type of meas": "J-V", "Temperature": temperature, "Filename": filename, "Values": result_2}
                else:
                    matrix["results"]["I"] = {"Type of meas": "I-V", "Temperature": temperature, "Filename": filename, "Values": result_1}
            elif CV:
                matrix["results"]["C"] = {"Type of meas": f"V-{V1}-{V2}","Temperature": temperature, "Filename": filename, "Values": result_c}
            elif It:
                matrix["results"]["It"] = {"Type of meas": "V-TDDB","Temperature": temperature, "Filename": filename, "Values": result_it}

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


def connexion():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db[get_db_name()]
    return collection


def setCompliance(waferId, session, compliance):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db[get_db_name()]

    compliance=float(compliance)

    result = collection.update_one(
        {"wafer_id": waferId},
        {"$set": {f"{session}.Compliance": compliance}}
    )

    client.close()

def create_db_tbl(path, is_JV):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    db_name = get_db_name()

    db[db_name].create_index('wafer_id')
    db[db_name].create_index('session')
    db[db_name].create_index('testDeviceID')
    db[db_name].create_index('matrices.coordinates')
    db[db_name].create_index('results.Filename')
    db[db_name].create_index('results.Temperature')
    db[db_name].create_index('results.Values')
    db[db_name].create_index([('wafer_id', pymongo.ASCENDING), ('matrices.coordinates', pymongo.ASCENDING)])

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

            if is_JV:
                line = next((l for l in file if '("testdeviceArea" ' in l), None)
                if not line:
                    break
                area = float(converter_split(line))

            line = next((l for l in file if '("procedureName" ' in l), None)
            if not line:
                break
            procedure = converter_split(line)
            print(procedure)

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
                session = ' '.join(session)
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
                    result_2 = [{"V": float(voltages[i]), "I": float(currents_densities[i])} for i in range(len(voltages))]


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

                result_it = [{"V": float(voltages[i]), "It": float(currents[i])} for i in range(len(voltages))]

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
                wafer[session]['Compliance'] = 1e-3
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
                matrix = {"matrix_id": matrix_id, "coordinates": {"x": chipX, "y": chipY}, "results": {}}
                wafer[session][testdeviceID]["matrices"].append(matrix)

            # Now, matrix refers to the matrix we want to update/add in the structure
            # Update/add the results in the matrix
            if IV:
                if JV:
                    matrix["results"]["I"] = {"Type of meas": "I-V", "Temperature": temperature, "Filename": filename,
                                              "Values": result_1}
                    matrix["results"]["J"] = {"Type of meas": "J-V", "Temperature": temperature, "Filename": filename,
                                              "Values": result_2}
                else:
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
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    db_name = get_db_name()

    db[db_name].create_index('wafer_id')
    db[db_name].create_index('session')
    db[db_name].create_index('testDeviceID')
    db[db_name].create_index('matrices.coordinates')
    db[db_name].create_index('results.Filename')
    db[db_name].create_index('results.Temperature')
    db[db_name].create_index('results.Values')
    db[db_name].create_index([('wafer_id', pymongo.ASCENDING), ('matrices.coordinates', pymongo.ASCENDING)])

    collection = db[db_name]

    filename = path.split("\\")[-1].split(".")[0]
    print(filename)

    session = None

    if not filename.startswith("AL"):  # We parse the filename to get the wafer_id and the original filename
        wafer_id = filename.split("@@@")[-1].split("_")[0] + "_" + filename.split("@@@")[-1].split("_")[1]
        temperature = filename.split("@@@")[-1].split("_")[-1]
        #filename = filename.split("@@@")[0]
    else:
        wafer_id = filename.split("_")[0] + "_" + filename.split("_")[1]
        temperature = filename.split("_")[-1]
        #filename = '_'.join(filename.split("_")[:-1])


    list_of_wafers = set()
    print(f"Creating/opening database for {filename}")
    infos = []

    db_buffer = {}  # We create a dictionary to store all datas, so we write just once in the database, this is much faster

    with io.open(path, 'r', 128 * 128) as file:  # We read the file and clear the memory every 128ko so there is no preasure on the memory
        for line in file:
            current_line = [element for element in line.split('  ') if element != '']
            if 'check_probecard' in current_line[0]:
                infos.append({'type': 'No', 'structure': current_line[1]})

            elif 'leakage' in current_line[0]:
                infos.append({'type': 'Leakage', 'structure': current_line[1]})

            elif 'capacitor' in current_line[0]:
                if 'measured capacitance' in current_line[0]:
                    infos.append({'type': 'C', 'structure': current_line[1]})
                else:
                    infos.append({'type': 'Cmes', 'structure': current_line[1]})

            elif 'resistance' in current_line[0]:
                infos.append({'type': 'R', 'structure': current_line[1]})

    start_position = 0
    while infos[start_position]['type'] == 'No':
        start_position+=1


    wafer = collection.find_one({"wafer_id": wafer_id})
    if wafer is None:
        wafer = {'wafer_id': wafer_id}

    date = wafer.get(session)

    if date is None:
        wafer[session] = {}
        wafer[session]['Compliance'] = 1e-3

    with io.open(f"DataFiles\\{filename}", 'r', 128 * 128) as file:
        datas = []
        line = next((l for l in file if 'SAS DATE' in l), None)
        date = line.split(' = ')[-1][:-1].split(':')[0]
        session = f"{filename} {date}"

        line = next((l for l in file if 'BOD' in l), None)

        while 'EOD' not in line:
            x = line.split(' ')[0]
            y = line.split(' ')[1]
            line = next((l for l in file), None)
            while line.startswith(date):
                for data in line.split(' ')[1:]:
                    datas.append(data)
                line = next((l for l in file), None)
                for i in range(start_position, min(len(datas), len(infos))):
                    structure = infos[i]['structure']
                    type = infos















create_db_lim("DataFiles\AL123456_D04@@@D04-BR-CapResLeak-t1.lim")



