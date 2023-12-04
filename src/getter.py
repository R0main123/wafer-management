from pymongo import MongoClient


def get_db_name(db_name="New Wafers"):
    """
    Used to know which database has to be opened. Default parameter can be changed manually, so a new database will be created if it doesn't exist yet.

    :param <str> db_name: Name of the database. Please change it to create a new database or switch to another existing
    :return: Name of the database
    """
    return db_name


def connexion():
    """
    Used to connect to the database, so we can manipulate data. /!\  Only use to read data, not to write data in the DB /!\

    :return: The collection.
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db[get_db_name()]
    return collection


def get_wafer(wafer_id):
    """
    This function finds the wafer specified in the database. /!\ Only use to read data, not to write data in the DB /!\

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


def get_temps(wafer_id):
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


def get_filenames(wafer_id):
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
    This function finds all matrices that contain I-V measurements. Used to display buttons in the right place in the UI

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
    """
    Used to get all sessions inside a given wafer.

    :param <str> wafer_id: ID of the wafer

    :return <list of str>: All sessions inside the wafer
    """
    wafer = get_wafer(wafer_id)
    sessions = [session for session in wafer]
    if "_id" in sessions:
        sessions.remove("_id")

    if "wafer_id" in sessions:
        sessions.remove("wafer_id")

    return sessions


def get_map_sessions(wafer_id):
    """
    Used to get all sessions that contain I-V measurements (for wafer maps) inside a wafer.

    :param <str> wafer_id: ID of the wafer

    :return <list of str>: All sessions with I-V measurements inside the wafer
    """
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
            break

    return list(set(sessions))


def get_map_structures(wafer_id, session):
    """
    Used to get all structures that contain I-V measurements (for wafer maps) inside the given session of a wafer.

    :param <str> wafer_id: ID of the wafer
    :param <str> session: Selected session

    :return <list of str>: All structures that contain I-V measurements inside the session
    """
    wafer = get_wafer(wafer_id)
    structures = []
    for structure in get_structures(wafer_id, session):
        for matrix in wafer[session][structure]['matrices']:
            if 'I' in matrix["results"]:
                structures.append(structure)
                break
    if "Compliance" in structures:
        structures.remove("Compliance")

    return list(set(structures))


def get_structures(wafer_id, session):
    """
    Used to get all structures  inside the given session of a wafer.

    :param <str> wafer_id: ID of the wafer
    :param <str> session: Selected session

    :return <list of str>: All structures inside the session
    """
    structures = [structure for structure in get_wafer(wafer_id)[session]]

    if "Compliance" in structures:
        structures.remove("Compliance")

    return list(set(structures))


def get_R_sessions(wafer_id):
    """
    Used to get all sessions that contain R values (for wafer maps)

    :param <str> wafer_id: ID of the wafer

    :return <list>: List of all sessions that contain R values
    """
    wafer = get_wafer(wafer_id)
    sessions = []
    for session in get_sessions(wafer_id):
        for structure in wafer[session]:
            if structure == "Compliance":
                continue
            for matrix in wafer[session][structure]['matrices']:
                if 'R' in matrix:
                    sessions.append(session)
                    break
            if session in sessions:
                break

    return list(set(sessions))


def get_Leak_sessions(wafer_id):
    """
    Used to get all sessions that contain Leak values (for wafer maps)

    :param <str> wafer_id: ID of the wafer

    :return <list>: List of all sessions that contain Leak values
    """
    wafer = get_wafer(wafer_id)
    sessions = []
    for session in get_sessions(wafer_id):
        for structure in wafer[session]:
            if structure == "Compliance":
                continue
            for matrix in wafer[session][structure]['matrices']:
                if 'Leak' in matrix:
                    sessions.append(session)
                    break
            if session in sessions:
                break

    return list(set(sessions))


def get_C_sessions(wafer_id):
    """
    Used to get all sessions that contain C values (for wafer maps)

    :param <str> wafer_id: ID of the wafer

    :return <list>: List of all sessions that contain C values
    """
    wafer = get_wafer(wafer_id)
    sessions = []
    for session in get_sessions(wafer_id):
        for structure in wafer[session]:
            if structure == "Compliance":
                continue
            for matrix in wafer[session][structure]['matrices']:
                if matrix.get('Cap') is not None:
                    if 'C' in matrix['Cap']:
                        sessions.append(session)
                    break
            if session in sessions:
                break

    return list(set(sessions))


def get_Cmes_sessions(wafer_id):
    """
    Used to get all sessions that contain Cmes values (for wafer maps)

    :param <str> wafer_id: ID of the wafer

    :return <list>: List of all sessions that contain Cmes values
    """
    wafer = get_wafer(wafer_id)
    sessions = []
    for session in get_sessions(wafer_id):
        for structure in wafer[session]:
            if structure == "Compliance":
                continue
            for matrix in wafer[session][structure]['matrices']:
                if matrix.get('Cap') is not None:
                    if 'Cmes' in matrix['Cap']:
                        sessions.append(session)
                    break
            if session in sessions:
                break
    return list(set(sessions))


def get_R_structures(wafer_id, session):
    """
    Used to get all structures that contain R values (for wafer maps)

    :param <str> wafer_id: ID of the wafer
    :param <str> session: Name of the session

    :return <list>: List of all structures that contain R values
    """

    wafer = get_wafer(wafer_id)
    structures = []
    for structure in wafer[session]:
        if structure == "Compliance":
            continue
        for matrix in wafer[session][structure]['matrices']:
            if 'R' in matrix:
                structures.append(structure)
                break

    return list(set(structures))


def get_Leak_structures(wafer_id, session):
    """
    Used to get all structures that contain Leak values (for wafer maps)

    :param <str> wafer_id: ID of the wafer
    :param <str> session: Name of the session

    :return <list>: List of all structures that contain Leak values
    """
    wafer = get_wafer(wafer_id)
    structures = []
    for structure in wafer[session]:
        if structure == "Compliance":
            continue
        for matrix in wafer[session][structure]['matrices']:
            if 'Leak' in matrix:
                structures.append(structure)
                break
    return list(set(structures))


def get_C_structures(wafer_id, session):
    """
    Used to get all structures that contain C values (for wafer maps)

    :param <str> wafer_id: ID of the wafer
    :param <str> session: Name of the session

    :return <list>: List of all structures that contain C values
    """
    wafer = get_wafer(wafer_id)
    structures = []
    for structure in wafer[session]:
        if structure == "Compliance":
            continue
        for matrix in wafer[session][structure]['matrices']:
            if matrix.get('Cap') is not None:
                if 'C' in matrix['Cap']:
                    structures.append(structure)
                break

    return list(set(structures))


def get_Cmes_structures(wafer_id, session):
    """
    Used to get all structures that contain Cmes values (for wafer maps)

    :param <str> wafer_id: ID of the wafer
    :param <str> session: Name of the session

    :return <list>: List of all structures that contain Cmes values
    """
    wafer = get_wafer(wafer_id)
    structures = []
    for structure in wafer[session]:
        if structure == "Compliance":
            continue
        for matrix in wafer[session][structure]['matrices']:
            if matrix.get('Cap') is not None:
                if 'Cmes' in matrix['Cap']:
                    structures.append(structure)
                break

    return list(set(structures))


def get_plot_sessions(wafer_id):
    """
    Used to get all sessions that can be plot (i.e that conatin I-V, J-V and/or It Measurements) inside a wafer.

    :param <str> wafer_id: ID of the wafer

    :return <list of str>: All sessions with I-V measurements inside the wafer
    """
    wafer = get_wafer(wafer_id)
    sessions = []
    for session in get_sessions(wafer_id):
        for structure in wafer[session]:
            if structure == "Compliance":
                continue
            for matrix in wafer[session][structure]['matrices']:
                if matrix.get('results') is not None:
                    if 'I' in matrix['results'] or "J" in matrix['results'] or "It" in matrix['results']:
                        sessions.append(session)
                    break
            if session in sessions:
                break
    return list(set(sessions))


def get_plot_structures(wafer_id, session):
    """
    Used to get all structures that contain measurements that can be plot inside the given session of a wafer.

    :param <str> wafer_id: ID of the wafer
    :param <str> session: Selected session

    :return <list of str>: All structures that can be plot
    """
    wafer = get_wafer(wafer_id)
    structures = []
    for structure in get_structures(wafer_id, session):
        for matrix in wafer[session][structure]['matrices']:
            if 'I' in matrix['results'] or "J" in matrix['results'] or "It" in matrix['results']:
                structures.append(structure)
                break
    if "Compliance" in structures:
        structures.remove("Compliance")

    return list(set(structures))

