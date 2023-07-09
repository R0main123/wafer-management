from pymongo import MongoClient
from VBD import calculate_breakdown, get_vectors_in_matrix


def get_wafer(wafer_id):
    """
    This function finds the wafer specified in the database

    :param <str> wafer_id: name of the wafer_id
    :return <dict>: the wafer
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]
    return collection.find_one({"wafer_id": wafer_id})


def get_types(wafer_id=str):
    """
        This function finds all the types of measurements from the specified wafer in the database
        :param <str> wafer_id: name of the wafer_id
        :return <list>: the list of types in the wafer
    """
    wafer = get_wafer(wafer_id)
    list_of_types = set()
    for structure in wafer["structures"]:
        for matrix in structure["matrices"]:
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
    return list(set(matrix["results"][result]["Temperature"] for structure in wafer["structures"] for matrix in
                    structure["matrices"] for result in matrix["results"]))


def get_coords(wafer_id=str):
    """
        This function finds all the coordinates from the specified wafer in the database
        :param <str> wafer_id: name of the wafer_id
        :return <list>: the list of coordinates in the wafer
    """
    wafer = get_wafer(wafer_id)
    return list(set(
        f"({matrix['coordinates']['x']},{matrix['coordinates']['y']})" for structure in wafer["structures"] for matrix
        in structure["matrices"]))


def get_filenames(wafer_id=str):
    """
        This function finds all the filenames in the specified wafer in the database
        :param <str> wafer_id: name of the wafer_id
        :return <list>: the list of filenames in the wafer
    """
    wafer = get_wafer(wafer_id)
    return list(set(
        matrix['results'][result]['Filename'] for structure in wafer["structures"] for matrix in structure["matrices"]
        for result in matrix["results"]))


def get_compliance(wafer_id=str, structure_id=str):
    """
        This function finds the compliance from the specified structure in the database
        Returns None if the structure has no compliance registered
        :param <str> wafer_id: name of the wafer_id
        :param <str> structure_id: name of the structure
        :return <str>: the compliance in the wafer
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            return structure.get("compliance")

    return None


def get_die_compliance(wafer_id=str, structure_id=str, x=str, y=str):
    """
        This function finds the compliance from the specified structure in the database
        Returns None if the structure has no compliance registered
        :param <str> wafer_id: name of the wafer_id
        :param <str> structure_id: name of the structure
        :return <str>: the compliance in the wafer
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            for matrix in structure["matrices"]:
                return structure.get("compliance")

    return None


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
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    VBD = None

    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            for matrix in structure["matrices"]:
                if matrix["coordinates"]["x"] == x and matrix["coordinates"]["y"] == y:
                    VBD = matrix["results"]["I"].get("VBDs")

    if VBD is None:
        VBDs = [str(calculate_breakdown(get_vectors_in_matrix(wafer_id, structure_id, x, y)[0],
                                        get_vectors_in_matrix(wafer_id, structure_id, x, y)[1],
                                        get_compliance(wafer_id, structure_id))[0])]
        compliances = ["1e-3"]
    else:
        compliances = [couple["Compliance"] for couple in VBD]
        VBDs = [couple["VBD"] for couple in VBD]

    return compliances, VBDs


def get_matrices_with_I(wafer_id, structure_id):
    """
    This function finds all matrices that contain I-V measurements. Used to display buttons in the right place in the User Interface

    :param <str> wafer_id: the name of the wafer
    :param <str> structure_id: the name of the structure

    :return <list>: List of matrices that contains I-V measurements
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    list_of_matrices = []

    wafer = collection.find_one({"wafer_id": wafer_id})
    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            for matrix in structure["matrices"]:
                if "I" in matrix["results"]:
                    list_of_matrices.append(f"({matrix['coordinates']['x']},{matrix['coordinates']['y']})")

    return list_of_matrices


def get_all_infos_matrices(wafer_id, structure_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    list_of_infos = []

    wafer = collection.find_one({"wafer_id": wafer_id})
    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            for matrix in structure["matrices"]:
                x = matrix["coordinates"]["x"]
                y = matrix["coordinates"]["y"]
                compliance = get_compliance(wafer_id, structure_id)
                list_of_infos.append({"x": x,
                                      "y": y,
                                      "compliance": compliance if compliance is not None else [get_VBDs(wafer_id, structure_id, x, y)[0]]})

    return list_of_infos
