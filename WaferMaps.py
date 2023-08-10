from VBD import get_all_x, get_all_y, fig_to_base64
import numpy as np
import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
import matplotlib.colors as colors
from getter import get_wafer
import math


def R_wafer_map(wafer_id, session, structure_id):
    """
    This function returns a plot converted to base64, so it can be sent to the User Interface. The plot shows the wafer map based on R.
    R are taken from the database. If an R is a broken value, like 999999 or 999997, it's colored in black.

    :param <str> wafer_id: the name of the wafer
    :param <str> session: Selected session
    :param <str> structure_id: the name of the structure

    :return <list>: Plot converted to base64
    """

    X = np.array(get_all_x(wafer_id, session, structure_id))
    Y = np.array(get_all_y(wafer_id, session, structure_id))

    min_x, max_x, min_y, max_y = np.min(X), np.max(X), np.min(Y), np.max(Y)

    len_x = int(max_x - min_x + 1)
    len_y = int(max_y - min_y + 1)

    Rs = np.zeros((len_y, len_x))

    wafer = get_wafer(wafer_id)
    for matrix in wafer[session][structure_id]['matrices']:
        R = matrix["R"]

        if R < 500000:
            Rs[int(float(matrix["coordinates"]["y"]) - min_y), int(float(matrix["coordinates"]["x"]) - min_x)] = R

        else:
            Rs[int(float(matrix["coordinates"]["y"]) - min_y), int(float(matrix["coordinates"]["x"]) - min_x)] = np.inf


    Rs[Rs == 0] = np.nan

    x_ticks = np.linspace(min_x, max_x, Rs.shape[1])
    y_ticks = np.linspace(min_y, max_y, Rs.shape[0])

    if np.all(~np.isfinite(Rs)):
        color_matrix = np.zeros(Rs.shape + (3,))

        color_matrix[np.isnan(Rs)] = [1, 1, 1]
        color_matrix[np.isinf(Rs)] = [0, 0, 0]

        plt.imshow(color_matrix)
        fig = plt.gcf()

        base64_str = fig_to_base64(fig)

        plt.close(fig)

        return base64_str

    cmap = plt.cm.coolwarm
    cmap.set_bad(color='white')
    cmap.set_over(color='black')


    vmin = np.min(Rs[np.isfinite(Rs)])
    vmax = np.max(Rs[np.isfinite(Rs)])
    norm = colors.Normalize(vmin=vmin, vmax=vmax)

    max_abs_val = max(abs(np.min(Rs[np.isfinite(Rs)])), abs(np.max(Rs[np.isfinite(Rs)])))
    Rs[Rs == np.inf] = max_abs_val + math.ceil(max_abs_val * 0.1)

    x_interval = max(1, int(len_x/5))
    y_interval = max(1, int(len_y/5))

    plt.xticks(np.arange(0, Rs.shape[1], x_interval), x_ticks[::x_interval])
    plt.yticks(np.arange(0, Rs.shape[0], y_interval), y_ticks[::y_interval])

    plt.title(f"Wafer map of R of {structure_id} in {wafer_id}", pad=30)
    plt.imshow(Rs, cmap=cmap, norm=norm, interpolation="none")
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.colorbar()
    plt.axis('equal')

    fig = plt.gcf()
    plt.savefig(f"{wafer_id}\\WaferMap_Resistance_{session}_{structure_id}.png")

    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str


def Leak_wafer_map(wafer_id, session, structure_id):
    """
    This function returns a plot converted to base64, so it can be sent to the User Interface. The plot shows the wafer map based on Leak.
    Leak are taken from the database.

    :param <str> wafer_id: the name of the wafer
    :param <str> session: Selected session
    :param <str> structure_id: the name of the structure

    :return <list>: Plot converted to base64
    """

    X = np.array(get_all_x(wafer_id, session, structure_id))
    Y = np.array(get_all_y(wafer_id, session, structure_id))

    min_x, max_x, min_y, max_y = np.min(X), np.max(X), np.min(Y), np.max(Y)

    len_x = int(max_x - min_x + 1)
    len_y = int(max_y - min_y + 1)

    Leaks = np.zeros((len_y, len_x))

    wafer = get_wafer(wafer_id)
    for matrix in wafer[session][structure_id]['matrices']:
        Leaks[int(float(matrix["coordinates"]["y"]) - min_y), int(float(matrix["coordinates"]["x"]) - min_x)] = matrix["Leak"]

    Leaks[Leaks == 0] = np.nan

    x_ticks = np.linspace(min_x, max_x, Leaks.shape[1])
    y_ticks = np.linspace(min_y, max_y, Leaks.shape[0])


    cmap = plt.cm.coolwarm
    cmap.set_bad(color='white')
    cmap.set_over(color='black')

    vmin = np.min(Leaks[np.isfinite(Leaks)])
    vmax = np.max(Leaks[np.isfinite(Leaks)])
    norm = colors.Normalize(vmin=vmin, vmax=vmax)

    max_abs_val = max(abs(np.min(Leaks[np.isfinite(Leaks)])), abs(np.max(Leaks[np.isfinite(Leaks)])))
    Leaks[Leaks == np.inf] = max_abs_val + math.ceil(max_abs_val * 0.1)

    x_interval = max(1, int(len_x/5))
    y_interval = max(1, int(len_y/5))

    plt.xticks(np.arange(0, Leaks.shape[1], x_interval), x_ticks[::x_interval])
    plt.yticks(np.arange(0, Leaks.shape[0], y_interval), y_ticks[::y_interval])

    plt.title(f"Wafer map of R of {structure_id} in {wafer_id}", pad=30)
    plt.imshow(Leaks, cmap=cmap, norm=norm, interpolation="none")
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.colorbar()
    plt.axis('equal')

    fig = plt.gcf()
    plt.savefig(f"{wafer_id}\\WaferMap_Leakage_{session}_{structure_id}.png")
    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str


def C_wafer_map(wafer_id, session, structure_id):
    """
    This function returns a plot converted to base64, so it can be sent to the User Interface. The plot shows the wafer map based on C.
    C are taken from the database.

    :param <str> wafer_id: the name of the wafer
    :param <str> session: Selected session
    :param <str> structure_id: the name of the structure

    :return <list>: Plot converted to base64
    """

    X = np.array(get_all_x(wafer_id, session, structure_id))
    Y = np.array(get_all_y(wafer_id, session, structure_id))

    min_x, max_x, min_y, max_y = np.min(X), np.max(X), np.min(Y), np.max(Y)

    len_x = int(max_x - min_x + 1)
    len_y = int(max_y - min_y + 1)

    Cs = np.zeros((len_y, len_x))

    wafer = get_wafer(wafer_id)
    for matrix in wafer[session][structure_id]['matrices']:
        Cs[int(float(matrix["coordinates"]["y"]) - min_y), int(float(matrix["coordinates"]["x"]) - min_x)] = matrix["Cap"]["C"]

    Cs[Cs == 0] = np.nan

    x_ticks = np.linspace(min_x, max_x, Cs.shape[1])
    y_ticks = np.linspace(min_y, max_y, Cs.shape[0])


    cmap = plt.cm.coolwarm
    cmap.set_bad(color='white')
    cmap.set_over(color='black')

    vmin = np.min(Cs[np.isfinite(Cs)])
    vmax = np.max(Cs[np.isfinite(Cs)])
    norm = colors.Normalize(vmin=vmin, vmax=vmax)

    max_abs_val = max(abs(np.min(Cs[np.isfinite(Cs)])), abs(np.max(Cs[np.isfinite(Cs)])))
    Cs[Cs == np.inf] = max_abs_val + math.ceil(max_abs_val * 0.1)

    x_interval = max(1, int(len_x/5))
    y_interval = max(1, int(len_y/5))

    plt.xticks(np.arange(0, Cs.shape[1], x_interval), x_ticks[::x_interval])
    plt.yticks(np.arange(0, Cs.shape[0], y_interval), y_ticks[::y_interval])

    plt.title(f"Wafer map of R of {structure_id} in {wafer_id}", pad=30)
    plt.imshow(Cs, cmap=cmap, norm=norm, interpolation="none")
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.colorbar()
    plt.axis('equal')

    fig = plt.gcf()
    plt.savefig(f"{wafer_id}\\WaferMap_Capacitance_{session}_{structure_id}.png")
    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str


def Cmes_wafer_map(wafer_id, session, structure_id):
    """
    This function returns a plot converted to base64, so it can be sent to the User Interface. The plot shows the wafer map based on Cmes.
    Cmes are taken from the database.

    :param <str> wafer_id: the name of the wafer
    :param <str> session: Selected session
    :param <str> structure_id: the name of the structure

    :return <list>: Plot converted to base64
    """

    X = np.array(get_all_x(wafer_id, session, structure_id))
    Y = np.array(get_all_y(wafer_id, session, structure_id))

    min_x, max_x, min_y, max_y = np.min(X), np.max(X), np.min(Y), np.max(Y)

    len_x = int(max_x - min_x + 1)
    len_y = int(max_y - min_y + 1)

    Cmess = np.zeros((len_y, len_x))

    wafer = get_wafer(wafer_id)
    for matrix in wafer[session][structure_id]['matrices']:
        Cmess[int(float(matrix["coordinates"]["y"]) - min_y), int(float(matrix["coordinates"]["x"]) - min_x)] = matrix["Cap"]["Cmes"]

    Cmess[Cmess == 0] = np.nan

    x_ticks = np.linspace(min_x, max_x, Cmess.shape[1])
    y_ticks = np.linspace(min_y, max_y, Cmess.shape[0])


    cmap = plt.cm.coolwarm
    cmap.set_bad(color='white')
    cmap.set_over(color='black')

    vmin = np.min(Cmess[np.isfinite(Cmess)])
    vmax = np.max(Cmess[np.isfinite(Cmess)])
    norm = colors.Normalize(vmin=vmin, vmax=vmax)

    max_abs_val = max(abs(np.min(Cmess[np.isfinite(Cmess)])), abs(np.max(Cmess[np.isfinite(Cmess)])))
    Cmess[Cmess == np.inf] = max_abs_val + math.ceil(max_abs_val * 0.1)

    x_interval = max(1, int(len_x/5))
    y_interval = max(1, int(len_y/5))

    plt.xticks(np.arange(0, Cmess.shape[1], x_interval), x_ticks[::x_interval])
    plt.yticks(np.arange(0, Cmess.shape[0], y_interval), y_ticks[::y_interval])

    plt.title(f"Wafer map of R of {structure_id} in {wafer_id}", pad=30)
    plt.imshow(Cmess, cmap=cmap, norm=norm, interpolation="none")
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.colorbar()
    plt.axis('equal')

    fig = plt.gcf()
    plt.savefig(f"{wafer_id}\\WaferMap_Measured_Capacitance_{session}_{structure_id}.png")
    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str







