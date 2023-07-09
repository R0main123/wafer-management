import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as colors
from pymongo import MongoClient
import seaborn as sns
from plot_and_powerpoint import fig_to_base64


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

def calculate_breakdown(X, Y, compliance=0.001):
    """
    This functions calculates Voltage breakdown for two vectors given, and a compliance. Default value of the compliance is set to 1e-3
    :param <list> X: Values of voltage. Will be converted to a np.array
    :param <list> Y: Values of current. Will be converted to a np.array and we will take the absolute value of the values
    :param <float> compliance: Value of compliance. By default is set to 1e-3

    :return <float> Breakd_Volt: Voltage Breakdown. Can be Nan
    :return <float> Breakd_Leak: Leakage Breakdown. Can be Nan
    :return <bool> reached_compl: True if the current reached compliance, False otherwise. If it's False, Breakd_Volt will be Nan
    :return <float> high_leak: Compliance if compliance is reached, highest value of the current otherwise

    """
    if compliance is None:
        compliance = 0.0001

    if type(compliance) == str:
        compliance = float(compliance)

    X = np.array(X)
    Y = np.absolute(np.array(Y))

    DiffY = np.gradient(Y, X)

    pos = []

    for i in range(1, Y.shape[0]):
        if Y[i] > compliance and -1e-10 < DiffY[i] < 1e-10:
            pos.append(X[i])


    if len(pos) > 0:
        pos0 = pos[0]

        idx = pos0 if pos0 <= 1 else pos0 - 1

        Breakd_Leak = Y[np.where(X == pos[0])]
        Breakd_Volt = pos[0]

    else:
        Breakd_Leak = np.nan
        Breakd_Volt = np.nan

    if np.any(Y >= compliance):
        reached_comp = 1
        high_leak = compliance

    else:
        reached_comp = 0
        high_leak = np.max(Y)

    return Breakd_Volt, Breakd_Leak, reached_comp, high_leak

def get_all_x(wafer_id, structure_id):
    """
    This function gets all coordinates x in a structure. Used to create the wafer map.
    :param <str> wafer_id: the name of the wafer
    :param <str> structure_id: the name of the structure

    :return <list>: List of x in the structure
    """
    all_x = []
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            for matrix in structure["matrices"]:
                all_x.append(matrix["coordinates"]["x"])

            all_x = list(map(float, all_x))
            all_x.sort()

            return list(set(all_x))

    return list(set(all_x))

def get_all_y(wafer_id, structure_id):
    """
    This function gets all coordinates y in a structure. Used to create the wafer map.
    :param <str> wafer_id: the name of the wafer
    :param <str> structure_id: the name of the structure

    :return <list>: List of y in the structure
    """
    all_y = []
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            for matrix in structure["matrices"]:
                all_y.append(matrix["coordinates"]["y"])

            all_y = list(map(float, all_y))
            all_y.sort()


            return list(set(all_y))

    return list(set(all_y))

def get_vectors_in_matrix(wafer_id, structure_id, x, y):
    """
    This function is used to get he values of voltages and current in a matrix. This function is always in parameters for calculate_breakdown
    :param <str> wafer_id: the name of the wafer
    :param <str> structure_id: the name of the structure
    :param <str> x: the horizontal coordinate of the matrix
    :param <str> y: the vertical coordinate of the matrix

    :return <list> X: The values of voltage
    :return <list> Y: The values of current
    """
    if type(x) != str:
        x = str(x)

    if type(y) != str:
        y = str(y)

    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            for matrix in structure["matrices"]:
                if matrix["coordinates"]["x"] == x and matrix["coordinates"]["y"] == y:
                    for result in matrix["results"]:
                        if result == "I":
                            X = []
                            Y = []
                            for double in matrix["results"][result]["Values"]:
                                X.append(double["V"])
                                Y.append(double["I"])
                    break
            break

    return X, Y

def create_wafer_map(wafer_id, structure_id, compliance=None):
    """
    This function displays a wafer map from a wafer, a structure and a compliance. Zeros are display in white and other values are from Blue to red, like a heatmap
    By default, compliance is the one registered in the database. If there is not or if tis compliance is never reached, default value is 1e-3.
    :param <str> wafer_id: the name of the wafer
    :param <str> structure_id: the name of the structure

    :return <list>: List of x in the structure
    """
    if compliance is None:
        compliance = get_compliance(wafer_id, structure_id)

    X = np.array(get_all_x(wafer_id, structure_id))
    Y = np.array(get_all_y(wafer_id, structure_id))

    min_x, max_x, min_y, max_y = np.min(X), np.max(X), np.min(Y), np.max(Y)

    len_x = int(max_x - min_x + 1)
    len_y = int(max_y - min_y + 1)

    VBDs = np.zeros((len_y, len_x))


    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafer = collection.find_one({"wafer_id": wafer_id})
    for structure in wafer["structures"]:
        if structure["structure_id"] == structure_id:
            for matrix in structure["matrices"]:
                vec_X, vec_Y = get_vectors_in_matrix(wafer_id, structure_id, matrix["coordinates"]["x"], matrix["coordinates"]["y"])
                VBD = calculate_breakdown(vec_X, vec_Y, compliance)[0]

                if not (np.isnan(VBD)):
                    VBDs[int(float(matrix["coordinates"]["y"]) - min_y), int(float(matrix["coordinates"]["x"]) - min_x)] = VBD

                else:
                    VBDs[int(float(matrix["coordinates"]["y"]) - min_y), int(float(matrix["coordinates"]["x"]) - min_x)] = 0

    if np.all(VBDs == 0):
        return(create_wafer_map(wafer_id, structure_id, compliance=1e-3))

    else:
        VBDs[VBDs == 0] = np.nan

        x_ticks = np.linspace(min_x, max_x, VBDs.shape[1])
        y_ticks = np.linspace(min_y, max_y, VBDs.shape[0])

        cmap = colors.LinearSegmentedColormap.from_list(
            "mycmap", [(0, "blue"), (1, "red")]
        )

        sns.heatmap(VBDs, cmap=cmap)

        x_interval = max(1, int(len_x/5))
        y_interval = max(1, int(len_y/5))

        plt.xticks(np.arange(0, VBDs.shape[1], x_interval), x_ticks[::x_interval])
        plt.yticks(np.arange(0, VBDs.shape[0], y_interval), y_ticks[::y_interval])

        plt.title(f"{structure_id} in {wafer_id}. Compliance: {1e-3 if compliance is None else compliance}", pad=30)

        fig = plt.gcf()

        base64_str = fig_to_base64(fig)

        plt.close(fig)

        return base64_str

def create_personal_wafer_map(wafer_id, structure_id, compliances):
    """
    This function displays a wafer map from a wafer, a structure and a compliance. Zeros are display in white and other values are from Blue to red, like a heatmap
    :param <str> wafer_id: the name of the wafer
    :param <str> structure_id: the name of the structure

    :return <list>: List of x in the structure
    """

    X = np.array(get_all_x(wafer_id, structure_id))
    Y = np.array(get_all_y(wafer_id, structure_id))

    min_x, max_x, min_y, max_y = np.min(X), np.max(X), np.min(Y), np.max(Y)

    len_x = int(max_x - min_x + 1)
    len_y = int(max_y - min_y + 1)

    VBDs = np.zeros((len_y, len_x))

    for x, y, compliance in compliances:
        VBDs[y - min_y, x - min_x] = compliance

    VBDs[VBDs == 0] = np.nan

    x_ticks = np.linspace(min_x, max_x, VBDs.shape[1])
    y_ticks = np.linspace(min_y, max_y, VBDs.shape[0])

    cmap = colors.LinearSegmentedColormap.from_list(
        "mycmap", [(0, "blue"), (1, "red")]
    )

    sns.heatmap(VBDs, cmap=cmap)

    x_interval = max(1, int(len_x/5))
    y_interval = max(1, int(len_y/5))

    plt.xticks(np.arange(0, VBDs.shape[1], x_interval), x_ticks[::x_interval])
    plt.yticks(np.arange(0, VBDs.shape[0], y_interval), y_ticks[::y_interval])

    plt.title(f"{structure_id} in {wafer_id}")

    fig = plt.gcf()

    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str



