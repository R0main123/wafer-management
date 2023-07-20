from pymongo import MongoClient


def get_db_name(db_name="New Wafers"):
    return db_name


def connexion():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db[get_db_name()]
    return collection


def get_wafer(wafer_id):
    """
    This function finds the wafer specified in the database

    :param <str> wafer_id: name of the wafer_id
    :return <dict>: the wafer
    """
    collection = connexion()
    return collection.find_one({"wafer_id": wafer_id})


def get_types(wafer_id):
    """
        This function finds all the types of measurements from the specified wafer in the database
        :param <str> wafer_id: name of the wafer_id
        :return <list>: the list of types in the wafer
    """
    wafer = get_wafer(wafer_id)
    list_of_types = set()

    sessions = get_sessions(wafer_id)

    for session in sessions:
        structures = get_structures(wafer_id, session)
        for structure in structures:
            for matrix in wafer[session][structure]["matrices"]:
                for result in matrix["results"]:
                    list_of_types.add(result)
                    if len(list_of_types) >= 4:
                        return list(list_of_types)
    return list(list_of_types)


def get_temps(wafer_id=str):
    """
        This function finds all the temperatures from the specified wafer in the database
        :param <str> wafer_id: name of the wafer_id
        :return <list>: the list of temperatures in the wafer
    """
    wafer = get_wafer(wafer_id)
    list_of_temps = set()

    sessions = get_sessions(wafer_id)

    for session in sessions:
        structures = get_structures(wafer_id, session)
        for structure in structures:
            for matrix in wafer[session][structure]["matrices"]:
                for result in matrix["results"]:
                    list_of_temps.add(matrix["results"][result]["Temperature"])
    return list(list_of_temps)


def get_coords(wafer_id):
    """
        This function finds all the coordinates from the specified wafer in the database
        :param <str> wafer_id: name of the wafer_id
        :return <list>: the list of coordinates in the wafer
    """
    wafer = get_wafer(wafer_id)
    list_of_coords = set()

    sessions = get_sessions(wafer_id)

    for session in sessions:
        structures = get_structures(wafer_id, session)
        for structure in structures:
            for matrix in wafer[session][structure]["matrices"]:
                list_of_coords.add(f"({matrix['coordinates']['x']},{matrix['coordinates']['y']})")
    return list(list_of_coords)


def get_filenames(wafer_id=str):
    """
        This function finds all the filenames in the specified wafer in the database
        :param <str> wafer_id: name of the wafer_id
        :return <list>: the list of filenames in the wafer
    """
    wafer = get_wafer(wafer_id)
    list_of_files = set()

    sessions = get_sessions(wafer_id)

    for session in sessions:
        structures = get_structures(wafer_id, session)
        for structure in structures:
            for matrix in wafer[session][structure]["matrices"]:
                for result in matrix["results"]:
                    list_of_files.add(matrix["results"][result]["Filename"])
    return list(list_of_files)


def get_compliance(wafer_id, session):
    """
        This function finds the compliance from the specified structure in the database
        Returns None if the structure has no compliance registered
        :param <str> wafer_id: name of the wafer_id
        :param <str> session: name of the session

        :return <str>: the compliance in the wafer
    """
    wafer = get_wafer(wafer_id)
    return wafer[session].get("Compliance")


def get_matrices_with_I(wafer_id, structure_id):
    """
    This function finds all matrices that contain I-V measurements. Used to display buttons in the right place in the User Interface

    :param <str> wafer_id: the name of the wafer
    :param <str> structure_id: the name of the structure

    :return <list>: List of matrices that contains I-V measurements
    """
    wafer = get_wafer(wafer_id)
    list_of_matrices = []

    sessions = get_sessions(wafer_id)
    for session in sessions:
        for matrix in wafer[session][structure_id]["matrices"]:
            if "I" in matrix["results"]:
                list_of_matrices.append(f"({matrix['coordinates']['x']},{matrix['coordinates']['y']})")

    return list_of_matrices


def get_sessions(wafer_id):
    wafer = get_wafer(wafer_id)
    sessions = [session for session in wafer]
    if "_id" in sessions:
        sessions.remove("_id")

    if "wafer_id" in sessions:
        sessions.remove("wafer_id")

    return sessions


def get_map_sessions(wafer_id):
    wafer = get_wafer(wafer_id)
    sessions = []
    for session in get_sessions(wafer_id):
        for structure in wafer[session]:
            if structure == "Compliance":
                continue
            for matrix in wafer[session][structure]['matrices']:
                if 'I' in matrix["results"]:
                    sessions.append(session)
                    break

    return list(set(sessions))


def get_map_structures(wafer_id, session):
    wafer = get_wafer(wafer_id)
    structures = []
    for structure in get_structures(wafer_id, session):
        for matrix in wafer[session][structure]['matrices']:
            if 'I' in matrix["results"]:
                structures.append(structure)
                break

    return structures


def get_structures(wafer_id, session):
    structures = [structure for structure in get_wafer(wafer_id)[session]]

    if "Compliance" in structures:
        structures.remove("Compliance")

    return structures
