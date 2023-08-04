import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import probscale

from scipy.stats import norm, probplot


from getter import get_wafer, get_structures, get_sessions
from VBD import fig_to_base64


def VBD_normal_distrib_pos(wafer_id, sessions, structures, dies):
    """
    Used to plot the normal distribution of positive values of VBD inside a wafer, following selected filters.
    We first get data inside the database and then plot it in a figure. We use a probability scale, and plot the reference line and the 90% confidence interval

    :param wafer_id: ID of the wafer
    :param sessions: Selected sessions
    :param structures: Selected structures
    :param dies: Selected dies

    :return: The plot, converted into base64
    """
    VBDs = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        for structure in structures:
            for matrix in wafer[session][structure]['matrices']:
                coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                if matrix.get("VBD") is not None and coordinates in dies and not math.isnan(matrix["VBD"]) and matrix["VBD"] >= 0:
                    VBDs.append(matrix["VBD"])

    VBDs = np.array(VBDs)
    VBDs = pd.Series(VBDs)

    data_sorted = np.sort(VBDs)
    p = 100. * np.arange(len(VBDs)) / (len(VBDs) - 1)

    # Calcul de la moyenne et de l'écart-type des données
    mu, std_dev = norm.fit(VBDs)

    # Calcul des valeurs pour les courbes de confiance
    conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
    lower_confidence_bound = mu - conf_interval * std_dev
    upper_confidence_bound = mu + conf_interval * std_dev

    fig, ax = plt.subplots(figsize=(10, 5))

    # Tracer les données
    probscale.probplot(data_sorted, ax=ax, plottype='prob', problabel='Percentiles', datalabel='Data', probax='y')

    # Tracer la ligne de référence
    ax.plot(data_sorted, norm.cdf(data_sorted, mu, std_dev) * 100, label='Reference line')

    # Tracer les courbes de confiance
    ax.plot(data_sorted, norm.cdf(data_sorted, lower_confidence_bound, std_dev) * 100,
            label='Lower confidence bound', linestyle='--')
    ax.plot(data_sorted, norm.cdf(data_sorted, upper_confidence_bound, std_dev) * 100,
            label='Upper confidence bound', linestyle='--')

    ax.legend(loc='upper left')

    title = f"Probability Plot of positives VBDs: Mean = {mu:.2f}, Std Dev = {std_dev:.2f}"
    ax.set_title(title)

    fig = plt.gcf()

    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str


def VBD_normal_distrib_neg(wafer_id, sessions, structures, dies):
    """
    Used to plot the normal distribution of negative values of VBD inside a wafer, following selected filters.
    We first get data inside the database and then plot it in a figure. We use a probability scale, and plot the reference line and the 90% confidence interval

    :param wafer_id: ID of the wafer
    :param sessions: Selected sessions
    :param structures: Selected structures
    :param dies: Selected dies

    :return: The plot, converted into base64
    """
    VBDs = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        for structure in structures:
            for matrix in wafer[session][structure]['matrices']:
                coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                if coordinates in dies and not math.isnan(matrix["VBD"]) and matrix["VBD"] <= 0:
                    VBDs.append(matrix["VBD"])

    VBDs = np.array(VBDs)
    VBDs = pd.Series(VBDs)

    data_sorted = np.sort(VBDs)
    p = 100. * np.arange(len(VBDs)) / (len(VBDs) - 1)

    # Calcul de la moyenne et de l'écart-type des données
    mu, std_dev = norm.fit(VBDs)

    # Calcul des valeurs pour les courbes de confiance
    conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
    lower_confidence_bound = mu - conf_interval * std_dev
    upper_confidence_bound = mu + conf_interval * std_dev

    fig, ax = plt.subplots(figsize=(10, 5))

    # Tracer les données
    probscale.probplot(data_sorted, ax=ax, plottype='prob', problabel='Percentiles', datalabel='Data', probax='y')

    # Tracer la ligne de référence
    ax.plot(data_sorted, norm.cdf(data_sorted, mu, std_dev) * 100, label='Reference line')

    # Tracer les courbes de confiance
    ax.plot(data_sorted, norm.cdf(data_sorted, lower_confidence_bound, std_dev) * 100,
            label='Lower confidence bound', linestyle='--')
    ax.plot(data_sorted, norm.cdf(data_sorted, upper_confidence_bound, std_dev) * 100,
            label='Upper confidence bound', linestyle='--')

    ax.legend(loc='upper left')

    title = f"Probability Plot of negatives VBDs: Mean = {mu:.2f}, Std Dev = {std_dev:.2f}"
    ax.set_title(title)

    fig = plt.gcf()

    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str


def Leakage_normal_distrib_pos(wafer_id, sessions, structures, dies):
    """
    Used to plot the normal distribution of positive values of Leakage inside a wafer, following selected filters.
    We first get data inside the database and then plot it in a figure. We use a probability scale, and plot the reference line and the 90% confidence interval

    :param wafer_id: ID of the wafer
    :param sessions: Selected sessions
    :param structures: Selected structures
    :param dies: Selected dies

    :return: The plot, converted into base64
    """
    Leaks = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("Leak") is not None and not math.isnan(float(matrix["Leak"])) and float(matrix["Leak"]) >= 0:
                        Leaks.append(float(matrix["Leak"]))

    Leaks = np.array(Leaks)
    Leaks = pd.Series(Leaks)

    fig, ax = plt.subplots()

    data_sorted = np.sort(Leaks)

    # Calcul de la moyenne et de l'écart-type des données
    mu, std_dev = np.mean(data_sorted), np.std(data_sorted)

    # Calcul des valeurs pour les courbes de confiance
    conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
    lower_confidence_bound = mu - conf_interval * std_dev
    upper_confidence_bound = mu + conf_interval * std_dev

    fig, ax = plt.subplots(figsize=(10, 5))

    # Tracer les données
    probscale.probplot(data_sorted, ax=ax, plottype='prob', problabel='Percentiles', datalabel='Data', probax='y')

    # Tracer la ligne de référence
    ax.plot(data_sorted, norm.cdf(data_sorted, mu, std_dev) * 100, label='Reference line')

    # Tracer les courbes de confiance
    ax.plot(data_sorted, norm.cdf(data_sorted, lower_confidence_bound, std_dev) * 100,
            label='Lower confidence bound', linestyle='--')
    ax.plot(data_sorted, norm.cdf(data_sorted, upper_confidence_bound, std_dev) * 100,
            label='Upper confidence bound', linestyle='--')

    ax.legend(loc='upper left')

    title = f"Probability Plot of Positives Leakages: Mean = {mu}, Std Dev = {std_dev}"
    ax.set_title(title)

    fig = plt.gcf()

    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str


def Leakage_normal_distrib_neg(wafer_id, sessions, structures, dies):
    """
    Used to plot the normal distribution of negative values of Leakage inside a wafer, following selected filters.
    We first get data inside the database and then plot it in a figure. We use a probability scale, and plot the reference line and the 90% confidence interval

    :param wafer_id: ID of the wafer
    :param sessions: Selected sessions
    :param structures: Selected structures
    :param dies: Selected dies

    :return: The plot, converted into base64
    """
    Leaks = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("Leak") is not None and not math.isnan(float(matrix["Leak"])) and float(matrix["Leak"]) <= 0:
                        Leaks.append(float(matrix["Leak"]))

    Leaks = np.array(Leaks)
    Leaks = pd.Series(Leaks)

    data_sorted = np.sort(Leaks)

    # Calcul de la moyenne et de l'écart-type des données
    mu, std_dev = np.mean(data_sorted), np.std(data_sorted)

    # Calcul des valeurs pour les courbes de confiance
    conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
    lower_confidence_bound = mu - conf_interval * std_dev
    upper_confidence_bound = mu + conf_interval * std_dev

    fig, ax = plt.subplots(figsize=(10, 5))

    # Tracer les données
    probscale.probplot(data_sorted, ax=ax, plottype='prob', problabel='Percentiles', datalabel='Data', probax='y')

    # Tracer la ligne de référence
    ax.plot(data_sorted, norm.cdf(data_sorted, mu, std_dev) * 100, label='Reference line')

    # Tracer les courbes de confiance
    ax.plot(data_sorted, norm.cdf(data_sorted, lower_confidence_bound, std_dev) * 100,
            label='Lower confidence bound', linestyle='--')
    ax.plot(data_sorted, norm.cdf(data_sorted, upper_confidence_bound, std_dev) * 100,
            label='Upper confidence bound', linestyle='--')

    ax.legend(loc='upper left')

    title = f"Probability Plot of negatives Leakages: Mean = {mu}, Std Dev = {std_dev}"
    ax.set_title(title)
    plt.figtext(0.5, 0.01, "WARNING: These are negative values", ha='center', color='red', fontsize=15)

    fig = plt.gcf()

    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str


def C_normal_distrib_neg(wafer_id, sessions, structures, dies):
    """
    Used to plot the normal distribution of negatives values of C inside a wafer, following selected filters.
    We first get data inside the database and then plot it in a figure. We use a probability scale, and plot the reference line and the 90% confidence interval

    :param wafer_id: ID of the wafer
    :param sessions: Selected sessions
    :param structures: Selected structures
    :param dies: Selected dies

    :return: The plot, converted into base64
    """
    Cs = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("Cap") is not None and matrix["Cap"].get("C") is not None and not math.isnan(float(matrix["Cap"]["C"])) and float(matrix["Cap"]["C"]) <= 0:
                        Cs.append(float(matrix["Cap"]["C"]))

    Cs = np.array(Cs)
    Cs = pd.Series(Cs)

    data_sorted = np.sort(Cs)
    mu, std_dev = np.mean(data_sorted), np.std(data_sorted)

    # Calcul des valeurs pour les courbes de confiance
    conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
    lower_confidence_bound = mu - conf_interval * std_dev
    upper_confidence_bound = mu + conf_interval * std_dev

    fig, ax = plt.subplots(figsize=(10, 5))

    # Tracer les données
    probscale.probplot(data_sorted, ax=ax, plottype='prob', problabel='Percentiles', datalabel='Data', probax='y')

    # Tracer la ligne de référence
    ax.plot(data_sorted, norm.cdf(data_sorted, mu, std_dev) * 100, label='Reference line')

    # Tracer les courbes de confiance
    ax.plot(data_sorted, norm.cdf(data_sorted, lower_confidence_bound, std_dev) * 100,
            label='Lower confidence bound', linestyle='--')
    ax.plot(data_sorted, norm.cdf(data_sorted, upper_confidence_bound, std_dev) * 100,
            label='Upper confidence bound', linestyle='--')

    ax.legend(loc='upper left')

    title = f"Probability Plot of negatives C: Mean = {mu}, Std Dev = {std_dev}"
    ax.set_title(title)
    plt.figtext(0.5, 0.01, "WARNING: These are negative values", ha='center', color='red', fontsize=15)

    fig = plt.gcf()

    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str


def C_normal_distrib_pos(wafer_id, sessions, structures, dies):
    """
    Used to plot the normal distribution of positive values of C inside a wafer, following selected filters.
    We first get data inside the database and then plot it in a figure. We use a probability scale, and plot the reference line and the 90% confidence interval

    :param wafer_id: ID of the wafer
    :param sessions: Selected sessions
    :param structures: Selected structures
    :param dies: Selected dies

    :return: The plot, converted into base64
    """
    Cs = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("Cap") is not None and matrix["Cap"].get("C") is not None and not math.isnan(float(matrix["Cap"]["C"])) and float(matrix["Cap"]["C"]) >= 0:
                        Cs.append(float(matrix["Cap"]["C"]))

    Cs = np.array(Cs)
    Cs = pd.Series(Cs)

    data_sorted = np.sort(Cs)
    mu, std_dev = np.mean(data_sorted), np.std(data_sorted)

    # Calcul des valeurs pour les courbes de confiance
    conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
    lower_confidence_bound = mu - conf_interval * std_dev
    upper_confidence_bound = mu + conf_interval * std_dev

    fig, ax = plt.subplots(figsize=(10, 5))

    # Tracer les données
    probscale.probplot(data_sorted, ax=ax, plottype='prob', problabel='Percentiles', datalabel='Data', probax='y')

    # Tracer la ligne de référence
    ax.plot(data_sorted, norm.cdf(data_sorted, mu, std_dev) * 100, label='Reference line')

    # Tracer les courbes de confiance
    ax.plot(data_sorted, norm.cdf(data_sorted, lower_confidence_bound, std_dev) * 100,
            label='Lower confidence bound', linestyle='--')
    ax.plot(data_sorted, norm.cdf(data_sorted, upper_confidence_bound, std_dev) * 100,
            label='Upper confidence bound', linestyle='--')

    ax.legend(loc='upper left')

    title = f"Probability Plot of positives C: Mean = {mu}, Std Dev = {std_dev}"
    ax.set_title(title)

    fig = plt.gcf()

    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str


def Cmes_normal_distrib_neg(wafer_id, sessions, structures, dies):
    """
    Used to plot the normal distribution of negative values of Cmes inside a wafer, following selected filters.
    We first get data inside the database and then plot it in a figure. We use a probability scale, and plot the reference line and the 90% confidence interval

    :param wafer_id: ID of the wafer
    :param sessions: Selected sessions
    :param structures: Selected structures
    :param dies: Selected dies

    :return: The plot, converted into base64
    """
    Cmes = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("Cap") is not None and matrix["Cap"].get("Cmes") is not None and not math.isnan(float(matrix["Cap"]["Cmes"])) and float(matrix["Cap"]["Cmes"]) <= 0:
                        Cmes.append(float(matrix["Cap"]["Cmes"]))

    Cmes = np.array(Cmes)
    Cmes = pd.Series(Cmes)

    data_sorted = np.sort(Cmes)
    mu, std_dev = np.mean(data_sorted), np.std(data_sorted)

    # Calcul des valeurs pour les courbes de confiance
    conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
    lower_confidence_bound = mu - conf_interval * std_dev
    upper_confidence_bound = mu + conf_interval * std_dev

    fig, ax = plt.subplots(figsize=(10, 5))

    # Tracer les données
    probscale.probplot(data_sorted, ax=ax, plottype='prob', problabel='Percentiles', datalabel='Data', probax='y')

    # Tracer la ligne de référence
    ax.plot(data_sorted, norm.cdf(data_sorted, mu, std_dev) * 100, label='Reference line')

    # Tracer les courbes de confiance
    ax.plot(data_sorted, norm.cdf(data_sorted, lower_confidence_bound, std_dev) * 100,
            label='Lower confidence bound', linestyle='--')
    ax.plot(data_sorted, norm.cdf(data_sorted, upper_confidence_bound, std_dev) * 100,
            label='Upper confidence bound', linestyle='--')

    ax.legend(loc='upper left')

    title = f"Probability Plot of negatives Cmes: Mean = {mu}, Std Dev = {std_dev}"
    ax.set_title(title)

    plt.figtext(0.5, 0.01, "WARNING: These are negative values", ha='center', color='red', fontsize=15)
    fig = plt.gcf()

    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str


def Cmes_normal_distrib_pos(wafer_id, sessions, structures, dies):
    """
    Used to plot the normal distribution of positive values of Cmes inside a wafer, following selected filters.
    We first get data inside the database and then plot it in a figure. We use a probability scale, and plot the reference line and the 90% confidence interval

    :param wafer_id: ID of the wafer
    :param sessions: Selected sessions
    :param structures: Selected structures
    :param dies: Selected dies

    :return: The plot, converted into base64
    """
    Cmes = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("Cap") is not None and matrix["Cap"].get("Cmes") is not None and not math.isnan(float(matrix["Cap"]["Cmes"])) and float(matrix["Cap"]["Cmes"]) >= 0:
                        Cmes.append(float(matrix["Cap"]["Cmes"]))

    Cmes = np.array(Cmes)
    Cmes = pd.Series(Cmes)

    data_sorted = np.sort(Cmes)
    mu, std_dev = np.mean(data_sorted), np.std(data_sorted)

    # Calcul des valeurs pour les courbes de confiance
    conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
    lower_confidence_bound = mu - conf_interval * std_dev
    upper_confidence_bound = mu + conf_interval * std_dev

    fig, ax = plt.subplots(figsize=(10, 5))

    # Tracer les données
    probscale.probplot(data_sorted, ax=ax, plottype='prob', problabel='Percentiles', datalabel='Data', probax='y')

    # Tracer la ligne de référence
    ax.plot(data_sorted, norm.cdf(data_sorted, mu, std_dev) * 100, label='Reference line')

    # Tracer les courbes de confiance
    ax.plot(data_sorted, norm.cdf(data_sorted, lower_confidence_bound, std_dev) * 100,
            label='Lower confidence bound', linestyle='--')
    ax.plot(data_sorted, norm.cdf(data_sorted, upper_confidence_bound, std_dev) * 100,
            label='Upper confidence bound', linestyle='--')

    ax.legend(loc='upper left')

    title = f"Probability Plot of positives Cmes: Mean = {mu}, Std Dev = {std_dev}"
    ax.set_title(title)

    fig = plt.gcf()

    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str


def R_normal_distrib_pos(wafer_id, sessions, structures, dies):
    """
    Used to plot the normal distribution of positive values of R inside a wafer, following selected filters.
    We first get data inside the database and then plot it in a figure. We use a probability scale, and plot the reference line and the 90% confidence interval

    :param wafer_id: ID of the wafer
    :param sessions: Selected sessions
    :param structures: Selected structures
    :param dies: Selected dies

    :return: The plot, converted into base64
    """
    Rs = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("R") is not None and not math.isnan(float(matrix["R"])) and float(matrix["R"]) >= 0:
                        Rs.append(float(matrix["R"]))

    Rs = np.array(Rs)
    Rs = pd.Series(Rs)

    data_sorted = np.sort(Rs)
    mu, std_dev = np.mean(data_sorted), np.std(data_sorted)

    # Calcul des valeurs pour les courbes de confiance
    conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
    lower_confidence_bound = mu - conf_interval * std_dev
    upper_confidence_bound = mu + conf_interval * std_dev

    fig, ax = plt.subplots(figsize=(10, 5))

    # Tracer les données
    probscale.probplot(data_sorted, ax=ax, plottype='prob', problabel='Percentiles', datalabel='Data', probax='y')

    # Tracer la ligne de référence
    ax.plot(data_sorted, norm.cdf(data_sorted, mu, std_dev) * 100, label='Reference line')

    # Tracer les courbes de confiance
    ax.plot(data_sorted, norm.cdf(data_sorted, lower_confidence_bound, std_dev) * 100,
            label='Lower confidence bound', linestyle='--')
    ax.plot(data_sorted, norm.cdf(data_sorted, upper_confidence_bound, std_dev) * 100,
            label='Upper confidence bound', linestyle='--')

    ax.legend(loc='upper left')

    title = f"Probability Plot of positives R: Mean = {mu}, Std Dev = {std_dev}"
    ax.set_title(title)

    fig = plt.gcf()

    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str


def R_normal_distrib_neg(wafer_id, sessions, structures, dies):
    """
    Used to plot the normal distribution of negative values of R inside a wafer, following selected filters.
    We first get data inside the database and then plot it in a figure. We use a probability scale, and plot the reference line and the 90% confidence interval

    :param wafer_id: ID of the wafer
    :param sessions: Selected sessions
    :param structures: Selected structures
    :param dies: Selected dies

    :return: The plot, converted into base64
    """
    Rs = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("R") is not None and not math.isnan(float(matrix["R"])) and float(matrix["R"]) <= 0:
                        Rs.append(float(matrix["R"]))

    Rs = np.array(Rs)
    Rs = pd.Series(Rs)

    data_sorted = np.sort(Rs)
    mu, std_dev = np.mean(data_sorted), np.std(data_sorted)

    # Calcul des valeurs pour les courbes de confiance
    conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
    lower_confidence_bound = mu - conf_interval * std_dev
    upper_confidence_bound = mu + conf_interval * std_dev

    fig, ax = plt.subplots(figsize=(10, 5))

    # Tracer les données
    probscale.probplot(data_sorted, ax=ax, plottype='prob', problabel='Percentiles', datalabel='Data', probax='y')

    # Tracer la ligne de référence
    ax.plot(data_sorted, norm.cdf(data_sorted, mu, std_dev) * 100, label='Reference line')

    # Tracer les courbes de confiance
    ax.plot(data_sorted, norm.cdf(data_sorted, lower_confidence_bound, std_dev) * 100,
            label='Lower confidence bound', linestyle='--')
    ax.plot(data_sorted, norm.cdf(data_sorted, upper_confidence_bound, std_dev) * 100,
            label='Upper confidence bound', linestyle='--')

    ax.legend(loc='upper left')

    title = f"Probability Plot of negatives R: Mean = {mu}, Std Dev = {std_dev}"
    ax.set_title(title)

    plt.figtext(0.5, 0.01, "WARNING: These are negative values", ha='center', color='red', fontsize=15)

    fig = plt.gcf()

    base64_str = fig_to_base64(fig)

    plt.close(fig)

    return base64_str


def get_values(wafer_id):
    """
    Used to know which extracted value is inside a given wafer, so we display only available options to the user

    :param wafer_id: ID of the wafer

    :return: list of all Extracted values inside the wafer
    """
    values = set()
    wafer = get_wafer(wafer_id)
    for session in get_sessions(wafer_id):
        for structure in get_structures(wafer_id, session):
            for matrix in wafer[session][structure]['matrices']:
                if matrix.get('VBD') is not None:
                    values.add("VBD")

                if matrix.get('Leak') is not None:
                    values.add('Leak')

                if matrix.get('R') is not None:
                    values.add("R")

                if matrix.get('Cap') is not None:
                    if matrix['Cap'].get('C'):
                        values.add('C')

                    if matrix['Cap'].get('Cmes'):
                        values.add('Cmes')
                if len(list(values)) == 5:
                    return list(values)

    return list(values)