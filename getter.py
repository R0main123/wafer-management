import math
from VBD import calculate_breakdown, get_vectors_in_matrix
from new_manage_DB import connexion


def get_wafer(wafer_id):
    """
    This function finds the wafer specified in the database

    :param <str> wafer_id: name of the wafer_id
    :return <dict>: the wafer
    """
    collection = connexion("New Wafers")
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


def get_VBDs(wafer_id, structure_id, x, y):
    """
        This function finds the couples of VBDs and compliance from the specified die in the database
        If the die has no VBD registered, it returns the calculated VBD with registered compliance.
        If the structure has no compliance registered, it calculates VBD based on default value (1e-3)

        :param <str> wafer_id: name of the wafer_id
        :param <str> structure_id: name of the structure
        :param <str> x: the horizontal coordinate of the matrix
        :param <str> y: the vertical coordinate of the matrix

        :return <str>: The VBD found or calculated
        """
    wafer = get_wafer(wafer_id)
    VBD = None

    sessions = get_sessions(wafer_id)

    for session in sessions:
        structures = get_structures(wafer_id, session)
        for structure in structures:
            for matrix in wafer[session][structure]["matrices"]:
                if matrix["coordinates"]["x"] == x and matrix["coordinates"]["y"] == y:
                    VBD = matrix["results"]["I"].get("VBDs")

    if VBD is None:
        VBDs = [str(calculate_breakdown(get_vectors_in_matrix(wafer_id, structure_id, x, y)[0],
                                        get_vectors_in_matrix(wafer_id, structure_id, x, y)[1],
                                        get_compliance(wafer_id, structure_id))[0])]
        compliances = ["1e-3"]
    else:
        compliances = [couple["Compliance"] for couple in VBD]
        VBDs = [str(couple["VBD"]) if not math.isnan(couple["VBD"]) else "Nan" for couple in VBD ]

    return compliances, VBDs


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


def get_all_infos_matrices(wafer_id, structure_id):
    wafer = get_wafer(wafer_id)
    list_of_infos = []

    sessions = get_sessions(wafer_id)
    for session in sessions:
        structures = get_structures(wafer_id, session)
        for structure in structures:
            for matrix in wafer[session][structure]["matrices"]:
                x = matrix["coordinates"]["x"]
                y = matrix["coordinates"]["y"]
                compliance = get_compliance(wafer_id, structure_id)
                list_of_infos.append({"x": x,
                                      "y": y,
                                      "compliance": compliance if compliance is not None else [get_VBDs(wafer_id, structure_id, x, y)[0]]})

    return list_of_infos


def get_sessions(wafer_id):
    wafer = get_wafer(wafer_id)
    return [session for session in wafer][2:]

def get_structures(wafer_id, session):
    return [structure for structure in get_wafer(wafer_id)[session]][1:]
