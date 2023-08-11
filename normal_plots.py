import math
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import probscale

from scipy.stats import norm, probplot
from cycler import cycler

from getter import get_wafer, get_structures, get_sessions, get_coords, connexion
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
    VBDs_sessions = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        VBDs = []
        for structure in structures:
            if wafer[session]. get(structure) is not None:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if matrix.get("VBD") is not None and coordinates in dies and not math.isnan(matrix["VBD"]) and matrix["VBD"] >= 0:
                        VBDs.append(matrix["VBD"])
        if len(VBDs) > 0:
            VBDs_sessions.append(VBDs)

    color_cycler = cycler(color=plt.cm.tab20.colors)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_prop_cycle(color_cycler)

    if len(VBDs_sessions) > 0:
        for VBDs in VBDs_sessions:
            VBDs = pd.Series(VBDs)

            data_sorted = np.sort(VBDs)
            p = 100. * np.arange(len(VBDs)) / (len(VBDs) - 1)

            # Calcul de la moyenne et de l'écart-type des données
            mu, std_dev = norm.fit(VBDs)

            # Calcul des valeurs pour les courbes de confiance
            conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
            lower_confidence_bound = mu - conf_interval * std_dev
            upper_confidence_bound = mu + conf_interval * std_dev

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
    VBDs_sessions = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        VBDs = []
        for structure in structures:
            if wafer[session].get(structure) is not None:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and not math.isnan(matrix["VBD"]) and matrix["VBD"] <= 0:
                        VBDs.append(matrix["VBD"])
        if len(VBDs) > 0:
            VBDs_sessions.append(VBDs)

    color_cycler = cycler(color=plt.cm.tab20.colors)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_prop_cycle(color_cycler)

    if len(VBDs_sessions) > 0:
        for VBDs in VBDs_sessions:
            VBDs = pd.Series(VBDs)

            data_sorted = np.sort(VBDs)
            p = 100. * np.arange(len(VBDs)) / (len(VBDs) - 1)

            # Calcul de la moyenne et de l'écart-type des données
            mu, std_dev = norm.fit(VBDs)

            # Calcul des valeurs pour les courbes de confiance
            conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
            lower_confidence_bound = mu - conf_interval * std_dev
            upper_confidence_bound = mu + conf_interval * std_dev

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
    Leaks_Sessions = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        Leaks = []
        for structure in structures:
            if wafer[session].get(structure) is not None:
                if structure in wafer[session]:
                    for matrix in wafer[session][structure]['matrices']:
                        coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                        if coordinates in dies and matrix.get("Leak") is not None and not math.isnan(float(matrix["Leak"])) and float(matrix["Leak"]) >= 0:
                            Leaks.append(float(matrix["Leak"]))
        if len(Leaks) > 0:
            Leaks_Sessions.append(Leaks)

    color_cycler = cycler(color=plt.cm.tab20.colors)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_prop_cycle(color_cycler)

    if len(Leaks_Sessions) > 0:
        for Leaks in Leaks_Sessions:
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
    Leaks_sessions = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        Leaks = []
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("Leak") is not None and not math.isnan(float(matrix["Leak"])) and float(matrix["Leak"]) <= 0:
                        Leaks.append(float(matrix["Leak"]))
        if len(Leaks) > 0:
            Leaks_sessions.append(Leaks)

    color_cycler = cycler(color=plt.cm.tab20.colors)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_prop_cycle(color_cycler)

    if len(Leaks_sessions) > 0:
        for Leaks in Leaks_sessions:
            Leaks = pd.Series(Leaks)

            data_sorted = np.sort(Leaks)

            # Calcul de la moyenne et de l'écart-type des données
            mu, std_dev = np.mean(data_sorted), np.std(data_sorted)

            # Calcul des valeurs pour les courbes de confiance
            conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
            lower_confidence_bound = mu - conf_interval * std_dev
            upper_confidence_bound = mu + conf_interval * std_dev

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
    Cs_sessions = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        Cs =[]
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("Cap") is not None and matrix["Cap"].get("C") is not None and not math.isnan(float(matrix["Cap"]["C"])) and float(matrix["Cap"]["C"]) <= 0:
                        Cs.append(float(matrix["Cap"]["C"]))
        if len(Cs) > 0:
            Cs_sessions.append(Cs)

    color_cycler = cycler(color=plt.cm.tab20.colors)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_prop_cycle(color_cycler)

    if len(Cs_sessions) > 0:
        for Cs in Cs_sessions:
            Cs = pd.Series(Cs)

            data_sorted = np.sort(Cs)
            mu, std_dev = np.mean(data_sorted), np.std(data_sorted)

            # Calcul des valeurs pour les courbes de confiance
            conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
            lower_confidence_bound = mu - conf_interval * std_dev
            upper_confidence_bound = mu + conf_interval * std_dev

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
    Cs_sessions = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        Cs = []
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("Cap") is not None and matrix["Cap"].get("C") is not None and not math.isnan(float(matrix["Cap"]["C"])) and float(matrix["Cap"]["C"]) >= 0:
                        Cs.append(float(matrix["Cap"]["C"]))
        if len(Cs) > 0:
            Cs_sessions.append(Cs)

    color_cycler = cycler(color=plt.cm.tab20.colors)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_prop_cycle(color_cycler)

    if len(Cs_sessions) > 0:
        for Cs in Cs_sessions:
            Cs = pd.Series(Cs)

            data_sorted = np.sort(Cs)
            mu, std_dev = np.mean(data_sorted), np.std(data_sorted)

            # Calcul des valeurs pour les courbes de confiance
            conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
            lower_confidence_bound = mu - conf_interval * std_dev
            upper_confidence_bound = mu + conf_interval * std_dev

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
    Cmes_sessions = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        Cmes = []
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("Cap") is not None and matrix["Cap"].get("Cmes") is not None and not math.isnan(float(matrix["Cap"]["Cmes"])) and float(matrix["Cap"]["Cmes"]) <= 0:
                        Cmes.append(float(matrix["Cap"]["Cmes"]))
        if len(Cmes) > 0:
            Cmes_sessions.append(Cmes)

    color_cycler = cycler(color=plt.cm.tab20.colors)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_prop_cycle(color_cycler)

    if len(Cmes_sessions) > 0:
        for Cmes in Cmes_sessions:
            Cmes = pd.Series(Cmes)

            data_sorted = np.sort(Cmes)
            mu, std_dev = np.mean(data_sorted), np.std(data_sorted)

            # Calcul des valeurs pour les courbes de confiance
            conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
            lower_confidence_bound = mu - conf_interval * std_dev
            upper_confidence_bound = mu + conf_interval * std_dev

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
    Cmes_sessions = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        Cmes = []
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("Cap") is not None and matrix["Cap"].get("Cmes") is not None and not math.isnan(float(matrix["Cap"]["Cmes"])) and float(matrix["Cap"]["Cmes"]) >= 0:
                        Cmes.append(float(matrix["Cap"]["Cmes"]))
        if len(Cmes) > 0:
            Cmes_sessions.append(Cmes)

    color_cycler = cycler(color=plt.cm.tab20.colors)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_prop_cycle(color_cycler)

    if len(Cmes_sessions) > 0:
        for Cmes in Cmes_sessions:
            Cmes = pd.Series(Cmes)

            data_sorted = np.sort(Cmes)
            mu, std_dev = np.mean(data_sorted), np.std(data_sorted)

            # Calcul des valeurs pour les courbes de confiance
            conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
            lower_confidence_bound = mu - conf_interval * std_dev
            upper_confidence_bound = mu + conf_interval * std_dev

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
    Rs_sessions = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        Rs = []
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("R") is not None and not math.isnan(float(matrix["R"])) and float(matrix["R"]) >= 0:
                        Rs.append(float(matrix["R"]))
        if len(Rs) > 0:
            Rs_sessions.append(Rs)

    color_cycler = cycler(color=plt.cm.tab20.colors)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_prop_cycle(color_cycler)

    if len(Rs_sessions) > 0:
        for Rs in Rs_sessions:
            Rs = pd.Series(Rs)

            data_sorted = np.sort(Rs)
            mu, std_dev = np.mean(data_sorted), np.std(data_sorted)

            # Calcul des valeurs pour les courbes de confiance
            conf_interval = 1.96  # correspond à 95% de confiance pour une distribution normale
            lower_confidence_bound = mu - conf_interval * std_dev
            upper_confidence_bound = mu + conf_interval * std_dev

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
    Rs_sessions = []
    wafer = get_wafer(wafer_id)

    for session in sessions:
        Rs = []
        for structure in structures:
            if structure in wafer[session]:
                for matrix in wafer[session][structure]['matrices']:
                    coordinates = f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})'
                    if coordinates in dies and matrix.get("R") is not None and not math.isnan(float(matrix["R"])) and float(matrix["R"]) <= 0:
                        Rs.append(float(matrix["R"]))
        if len(Rs) > 0:
            Rs_sessions.append(Rs)

    color_cycler = cycler(color=plt.cm.tab20.colors)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_prop_cycle(color_cycler)

    if len(Rs_sessions) > 0:
        for Rs in Rs_sessions:
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
    collection = connexion()

    VBD = collection.find_one({"wafer_id": wafer_id,
                              "sessions.structures.matrices": {
                                  "$elemMatch": {
                                      "VBD": {"$exists": True}
                                  }
                              }
                           })
    if VBD is not None:
        values.add("VBD")

    Leak = collection.find_one({"wafer_id": wafer_id, "matrices.Leak": {"$exists": True}})
    if Leak is not None:
        values.add("Leak")

    R = collection.find_one({"wafer_id": wafer_id, "matrices.R": {"$exists": True}})
    if R is not None:
        values.add("R")

    C = collection.find_one({"wafer_id": wafer_id, "matrices.Cap.C": {"$exists": True}})
    if C is not None:
        values.add("C")

    Cmes = collection.find_one({"wafer_id": wafer_id, "matrices.Cap.Cmes": {"$exists": True}})
    if Cmes is not None:
        values.add("Cmes")

    return list(values)

