from getter import get_sessions, get_structures, get_wafer


def filter_by_meas(meas, wafer_id):
    """
    This function browse the database to find all structures that have the types of measurements specified.

    :param <list> meas: List of str, contains all Measurements that wants to be matched
    :param <str> wafer_id: Name of the wafer_id

    :return <list>: A list of structures that contains the specified measurements
    """
    wafer = get_wafer(wafer_id)
    if wafer is None:
        return []

    list_of_structures = set()
    sessions = get_sessions(wafer_id)
    for session in sessions:
        structures = get_structures(wafer_id, session)
        for structure in structures:
            results = [result for matrix in wafer[session][structure]["matrices"] for result in matrix["results"]]

            if meas in results:
                list_of_structures.add(structure)

    return list(list_of_structures)


def filter_by_temp(temps, wafer_id):
    """
        This function browse the database to find all structures that have the temperature specified.

        :param <list> temps: List of str, contains all temperatures that wants to be matched
        :param <str> wafer_id: Name of the wafer_id

        :return <list>: A list of structures that contains the specified temperatures
        """
    wafer = get_wafer(wafer_id)
    if wafer is None:
        return []
    list_of_structures = set()
    results = set()

    sessions = get_sessions(wafer_id)
    for session in sessions:
        structures = get_structures(wafer_id, session)
        for structure in structures:
            for matrix in wafer[session][structure]["matrices"]:
                for result in matrix["results"]:
                    results.add(matrix["results"][result]["Temperature"])
            if temps in list(results):
                list_of_structures.add(structure)

    return list(list_of_structures)


def filter_by_coord(coords, wafer_id):
    """
        This function browse the database to find all structures that have a matrix with the couple of coordinates specified.

        :param <list> coords: List of str, contains all couples of coordinates that want to be matched
        :param <str> wafer_id: Name of the wafer_id

        :return <list>: A list of structures that contains the specified coordinates
        """
    coords = tuple((coords.split(',')[0][1:], coords.split(',')[-1][:-1]))

    wafer = get_wafer(wafer_id)
    list_of_structures = set()
    sessions = get_sessions(wafer_id)

    for session in sessions:
        structures = get_structures(wafer_id, session)
        for structure in structures:
            for matrix in wafer[session][structure]["matrices"]:
                if matrix["coordinates"]["x"] == coords[0] and matrix["coordinates"]["y"] == coords[1]:
                    list_of_structures.add(structure)
    return list(list_of_structures)


def filter_by_filename(file=str, wafer_id=str):
    """
        This function browse the database to find all structures that have measurements from thr file specified.

        :param <list> file: List of str, contains all files that wants to be matched
        :param <str> wafer_id: Name of the wafer_id

        :return <list>: A list of structures that contains the specified files
        """
    wafer = get_wafer(wafer_id)
    list_of_structures = set()

    sessions = get_sessions(wafer_id)

    for session in sessions:
        structures = get_structures(wafer_id, session)
        for structure in structures:
            for matrix in wafer[session][structure]["matrices"]:
                for result in matrix["results"]:
                    if matrix["results"][result]["Filename"] == file:
                        list_of_structures.add(structure)
    return list(list_of_structures)


def filter_by_session(session=str, wafer_id=str):
    """
        This function browse the database to find all structures that have measurements from thr file specified.

        :param <list> session: List of str, contains all files that wants to be matched
        :param <str> wafer_id: Name of the wafer_id

        :return <list>: A list of structures that contains the specified session
        """
    return get_structures(wafer_id, session)
