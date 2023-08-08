import glob
import json
import math

from pymongo import MongoClient
from flask_cors import CORS
from flask_socketio import SocketIO
from flask import Flask, request, jsonify, send_from_directory
import os
import timeit

from excel import wanted_excel, excel_VBD, excel_normal_R, excel_normal_Leak, excel_normal_VBD, excel_normal_Cmes, excel_normal_C
from new_manage_DB import create_db, setCompliance, create_db_tbl, get_db_name, create_db_lim
from plot_and_powerpoint import plot_wanted_matrices, wanted_ppt
from converter import handle_file, tbl_to_txt
from getter import get_types, get_temps, get_filenames, get_coords, get_compliance, get_sessions, get_wafer, \
    get_structures, get_map_sessions, connexion, get_map_structures, get_Leak_structures, get_Leak_sessions, \
    get_R_sessions, get_R_structures, get_C_sessions, get_C_structures, get_Cmes_sessions, get_Cmes_structures

from filter import filter_by_meas, filter_by_temp, filter_by_coord, filter_by_filename, filter_by_session
from VBD import create_wafer_map
from normal_plots import *
from WaferMaps import *

all_files = []

app = Flask(__name__, static_folder="my-app/build")
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
UPLOAD_FOLDER = '.\DataFiles\\'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    """
        Used for set up the app
    """
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/static/js/<path:path>')
def send_js(path):
    """
        Used for set up the app
    """
    return send_from_directory(os.path.join(app.static_folder, 'static', 'js'), path)


@app.route('/static/css/<path:path>')
def send_css(path):
    """
        Used for set up the app
    """
    return send_from_directory(os.path.join(app.static_folder, 'static', 'css'), path)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """
        Used for set up the app
    """
    if path != "" and os.path.exists("my-app/build/" + path):
        return send_from_directory("my-app/build", path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/static/<path:path>')
def send_static_files(path):
    """
        Used for set up the app
    """
    return send_from_directory('my-app/build/static', path)


@app.route('/upload', methods=['POST'])
def upload():
    """
    Used for collect files dropped by user. We create an Upload Folder and then handle each file:
    Step 1: uncompress file if it is a compressed file
    Step 2: Manage lim files and file without extension
    """
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    files = request.files.getlist("file")

    for file in files:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        processed_file = handle_file(file_path)

        if processed_file is not None:
            all_files.append(processed_file)

    files.clear()

    for file in all_files:
        file_name, file_extension = os.path.splitext(file)
        if file_extension == "":
            file_to_check = file_name.split("\\")[-1] + ".lim"
            if file_to_check not in os.listdir("DataFiles\\"):
                os.remove(f"{file_name}")
                return None

        if file_extension == ".lim":
            file_to_check = file_name.split("\\")[-1]
            if file_to_check not in os.listdir("DataFiles\\"):
                os.remove(f"{file_name}.lim")
                return None


    return jsonify({'result': 'success'}), 200


@app.route('/options/<checkbox_checked>', methods=['GET', 'POST'])
def options(checkbox_checked):
    """
    Used for registering data in the database. We check if the user wants to register J-V measures.
    Then, we use the correct function for each type of file (txt, tbl or lim)
    tbl files are converted into txt.
    Finally, Upload Folder is cleared
    """
    if request.method == 'POST':
        start_time = timeit.default_timer()

        for file in all_files:

            filename = file.split("\\")[-1]
            socketio.emit('message', {'data': f"Creating database for file {filename}"})
            if file.split('.')[-1] == 'txt':
                create_db(file, checkbox_checked)

            elif file.split('.')[-1] == 'tbl':
                create_db_tbl(file, checkbox_checked)
                tbl_to_txt(file)

            elif file.split('.')[-1] == 'lim':
                create_db_lim(file)

            elif len(file.split('.')) == 1:
                continue

            socketio.emit('message', {'data': f"Processing {filename}"})

        all_files.clear()

        if os.path.isdir("DataFiles"):
            for f in glob.glob("DataFiles\*"):
                os.remove(f)


        socketio.emit('message', {'data': "Finished processing."})

        end_time = timeit.default_timer()
        print(f"Finished in {end_time - start_time} seconds")

        return jsonify({'result': 'success'})

    else:
        return jsonify({'result': 'success'})


@app.route('/open')
def open():
    """
    Used for displaying all registered wafers.
    """
    collection = connexion()
    wafers = collection.find({})
    wafer_ids = []
    for wafer in wafers:
        wafer_ids.append(wafer["wafer_id"])

    return jsonify(wafer_ids)


@app.route('/get_structures/<wafer_id>/<session>', methods=['GET'])
def get_structures_json(wafer_id, session):
    """
    Used for getting all structures inside a given session in a wafer.
    """
    return jsonify(get_structures(wafer_id, session)), 200


@app.route('/get_all_structures/<wafer_id>', methods=['GET'])
def get_all_structures(wafer_id):
    """
    Used for getting all structures in all sessions in a wafer.
    """
    all_structures = []
    sessions = get_sessions(wafer_id)
    for session in sessions:
        structures = get_structures(wafer_id, session)
        for structure in structures:
            all_structures.append(structure)
    return jsonify(list(set(all_structures))), 200


@app.route('/get_sessions/<wafer_id>', methods=['GET'])
def get_sessions_server(wafer_id):
    """
    Used for getting all sessions inside a given wafer.
    """
    return jsonify(get_sessions(wafer_id)), 200


@app.route('/get_all_types/<wafer_id>', methods=['GET'])
def get_all_types(wafer_id):
    """
    Used for getting all types of measures inside a given wafer.
    """
    return jsonify(get_types(wafer_id)), 200


@app.route('/get_all_temps/<wafer_id>', methods=['GET'])
def get_all_temps(wafer_id):
    """
    Used for getting all temperatures inside a given wafer.
    """
    return jsonify(get_temps(wafer_id)), 200


@app.route('/get_all_coords/<wafer_id>', methods=['GET'])
def get_all_coords(wafer_id):
    """
    Used for getting all coordinates inside a given wafer.
    """
    return jsonify(get_coords(wafer_id)), 200


@app.route('/get_all_filenames/<wafer_id>', methods=['GET'])
def get_all_filenames(wafer_id):
    """
    Used for getting all filenames inside a given wafer.
    """
    return jsonify(get_filenames(wafer_id)), 200


@app.route('/filter_by_Meas/<wafer_id>/<selectedMeasurement>', methods=['GET'])
def filter_by_Meas(wafer_id, selectedMeasurement):
    """
    Used for displaying all structures that contain the selected type of measure inside the given wafer.
    """
    return jsonify(filter_by_meas(selectedMeasurement, wafer_id)), 200


@app.route('/filter_by_Temps/<wafer_id>/<selectedMeasurement>', methods=['GET'])
def filter_by_Temps(wafer_id, selectedMeasurement):
    """
    Used for displaying all structures that contain the selected temperature inside the given wafer.
    """
    return jsonify(filter_by_temp(selectedMeasurement, wafer_id)), 200


@app.route('/filter_by_Coords/<wafer_id>/<selectedMeasurement>', methods=['GET'])
def filter_by_Coords(wafer_id, selectedMeasurement):
    """
    Used for displaying all structures that contain the selected coordinates inside the given wafer.
    """
    return jsonify(filter_by_coord(selectedMeasurement, wafer_id)), 200


@app.route('/filter_by_Filenames/<wafer_id>/<selectedMeasurement>', methods=['GET'])
def filter_by_Filenames(wafer_id, selectedMeasurement):
    """
    Used for displaying all structures that contain the selected filename inside the given wafer.
    """
    return jsonify(filter_by_filename(selectedMeasurement, wafer_id)), 200


@app.route('/filter_by_Session/<wafer_id>/<selectedMeasurement>', methods=['GET'])
def filter_by_Session(wafer_id, selectedMeasurement):
    """
    Used for displaying all structures that contain the selected session inside the given wafer.
    """
    return jsonify(filter_by_session(selectedMeasurement, wafer_id)), 200


@app.route('/get_matrices/<wafer_id>/<structure_id>', methods=['GET'])
def get_matrices(wafer_id, structure_id):
    """
    Used for getting all dies in the structure selected
    """
    wafer = get_wafer(wafer_id)
    matrices = []

    sessions = get_sessions(wafer_id)
    for session in sessions:
        for matrix in wafer[session][structure_id]["matrices"]:
            matrices.append(f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})')
    return jsonify(matrices)


@app.route('/excel_structure/<waferId>/<sessions>/<structures>/<types>/<temps>/<files>/<coords>/<file_name>', methods=['GET'])
def excel_structure_route(waferId, sessions, structures, types, temps, files, coords, file_name):
    """
    Used for creating an Excel with selected parameters. We first refactor received information and then call the function
    """
    sessions = sessions.split(',')
    structures = structures.split(',')
    types = types.split(',')
    temps = temps.split(',')
    files = files.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")
    wanted_excel(waferId, sessions, structures, types, temps, files, coords, file_name)
    return jsonify({'result': 'success'})


@app.route('/ppt_structure/<waferId>/<sessions>/<structures>/<types>/<temps>/<files>/<coords>/<file_name>', methods=['GET'])
def ppt_structure_route(waferId, sessions, structures, types, temps, files, coords, file_name):
    """
    Used for creating a Powerpoint with selected parameters. We first refactor received information and then call the function
    """
    sessions = sessions.split(',')
    structures = structures.split(',')
    types = types.split(',')
    temps = temps.split(',')
    files = files.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")
    wanted_ppt(waferId, sessions, structures, types, temps, files, coords, file_name)
    return jsonify({'result': 'success'})


@app.route('/delete_wafer/<wafer_id>', methods=['DELETE'])
def delete_wafer(wafer_id):
    """
    Used for deleting a wafer
    """
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    db[get_db_name()].delete_one({'wafer_id': wafer_id})
    return jsonify({'result': 'success'}), 200


@app.route("/get_compl/<waferId>/<session>", methods=["GET"])
def get_compl(waferId, session):
    """
    Used for getting the compliance of the selected session
    """
    return jsonify(get_compliance(waferId, session))


@app.route("/set_compl/<waferId>/<session>/<compliance>")
def set_compl(waferId, session, compliance):
    """
    Used for setting the compliance of the selected session
    """
    setCompliance(waferId, session, compliance)
    return jsonify({'result': 'success'}), 200


@app.route("/create_wafer_map/<waferId>/<session>/<structure>", methods=["GET"])
def personal_wafer_map(waferId, session, structure):
    """
    Used for plotting the wafer map of the selected structure
    """
    image = create_wafer_map(waferId, session, structure)
    return jsonify(image)


@app.route("/plot_selected_matrices/<waferId>/<sessions>/<structures>/<types>/<temps>/<files>/<coords>", methods=["GET"])
def plot_we_want(waferId, sessions, structures, types, temps, files, coords):
    """
    Used for plotting the dies selected with selected parameters. We first refactor received information and then call the function
    """
    sessions = sessions.split(',')
    structures = structures.split(',')
    types = types.split(',')
    temps = temps.split(',')
    files = files.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")

    return jsonify(plot_wanted_matrices(waferId, sessions, structures, types, temps, files, coords))


@app.route('/get_map_sessions/<wafer_id>', methods=['GET'])
def get_map_sessions_server(wafer_id):
    """
        Used for getting all sessions that contain I-V measurements (for the wafer map)
    """
    return jsonify(get_map_sessions(wafer_id)), 200


@app.route('/get_map_structures/<wafer_id>/<session>', methods=['GET'])
def get_map_structures_server(wafer_id, session):
    """
        Used for getting all structures that contain I-V measurements (for the wafer map)
    """
    return jsonify(get_map_structures(wafer_id, session)), 200


@app.route('/register_excel_VBD/<waferId>/<sessions>/<structures>/<temps>/<files>/<coords>/<file_name>', methods=['GET'])
def reg_excel_VBD(waferId, sessions, structures, temps, files, coords, file_name):
    """
        Used for saving selected VBDs in an excel file.
        We first refactor received information and then call the function
    """
    sessions = sessions.split(',')
    sessions = list(set(sessions) & set(get_map_sessions(waferId)))
    structures = structures.split(',')
    temps = temps.split(',')
    files = files.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")
    excel_VBD(waferId, sessions, structures, temps, files, coords, file_name)
    return jsonify({'result': 'success'}), 200


@app.route("/normal_distrib_VBD/<waferId>/<sessions>/<structures>/<coords>", methods=["GET"])
def VBD_normal(waferId, sessions, structures, coords):
    """
        Used for plotting the normal plots of selected VBD.
        We first refactor received information and then call the function
    """
    sessions = sessions.split(',')
    sessions = list(set(sessions) & set(get_map_sessions(waferId)))
    if len(sessions) == 0:
        return jsonify(["There is no I-V measures in your selected sessions"])
    structures = structures.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")

    if "Compliance" in structures:
        structures.remove("Compliance")

    return jsonify([VBD_normal_distrib_pos(waferId, sessions, structures, coords), VBD_normal_distrib_neg(waferId, sessions, structures, coords)])

@app.route("/normal_distrib_R/<waferId>/<sessions>/<structures>/<coords>", methods=["GET"])
def R_normal(waferId, sessions, structures, coords):
    """
        Used for plotting the normal plots of R.
        We first refactor received information and then call the function
    """
    sessions = sessions.split(',')
    structures = structures.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")

    return jsonify([R_normal_distrib_pos(waferId, sessions, structures, coords), R_normal_distrib_neg(waferId, sessions, structures, coords)])


@app.route("/normal_distrib_Leak/<waferId>/<sessions>/<structures>/<coords>", methods=["GET"])
def Leak_normal(waferId, sessions, structures, coords):
    """
        Used for plotting the normal plots of Leak.
        We first refactor received information and then call the function
    """
    sessions = sessions.split(',')
    structures = structures.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")

    return jsonify([Leakage_normal_distrib_pos(waferId, sessions, structures, coords), Leakage_normal_distrib_neg(waferId, sessions, structures, coords)])


@app.route("/normal_distrib_C/<waferId>/<sessions>/<structures>/<coords>", methods=["GET"])
def C_normal(waferId, sessions, structures, coords):
    """
        Used for plotting the normal plots of C.
        We first refactor received information and then call the function
    """
    sessions = sessions.split(',')
    structures = structures.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")

    return jsonify([C_normal_distrib_pos(waferId, sessions, structures, coords), C_normal_distrib_neg(waferId, sessions, structures, coords)])


@app.route("/normal_distrib_Cmes/<waferId>/<sessions>/<structures>/<coords>", methods=["GET"])
def Cmes_normal(waferId, sessions, structures, coords):
    """
        Used for plotting the normal plots of Cmes.
        We first refactor received information and then call the function
    """
    sessions = sessions.split(',')
    structures = structures.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")

    return jsonify([Cmes_normal_distrib_pos(waferId, sessions, structures, coords), Cmes_normal_distrib_neg(waferId, sessions, structures, coords)])



@app.route("/R_wafer_map/<waferId>/<session>/<structure>", methods=["GET"])
def R_WM(waferId, session, structure):
    """
    Used to plot the wafer map based on resistance values
    """
    return jsonify(R_wafer_map(waferId, session, structure))


@app.route("/C_wafer_map/<waferId>/<session>/<structure>", methods=["GET"])
def C_WM(waferId, session, structure):
    """
    Used to plot the wafer map based on Capacitance values
    """
    return jsonify(C_wafer_map(waferId, session, structure))


@app.route("/Cmes_wafer_map/<waferId>/<session>/<structure>", methods=["GET"])
def Cmes_WM(waferId, session, structure):
    """
    Used to plot the wafer map based on Measured Capacitance values
    """
    return jsonify(Cmes_wafer_map(waferId, session, structure))


@app.route("/Leak_wafer_map/<waferId>/<session>/<structure>", methods=["GET"])
def Leak_WM(waferId, session, structure):
    """
    Used to plot the wafer map based on Leakage values
    """
    return jsonify(Leak_wafer_map(waferId, session, structure))

@app.route("/get_Leak_sessions/<waferId>", methods=["GET"])
def getLeakSess(waferId):
    """
    Used to get all session that contain Leakage values
    """
    return jsonify(get_Leak_sessions(waferId))

@app.route("/get_Leak_structures/<waferId>/<session>", methods=["GET"])
def getLeakStruct(waferId, session):
    """
    Used to get all structures that contain Leakage values
    """
    return jsonify(get_Leak_structures(waferId, session))


@app.route("/get_R_sessions/<waferId>", methods=["GET"])
def getRSess(waferId):
    """
    Used to get all session that contain Resistance values
    """
    return jsonify(get_R_sessions(waferId))

@app.route("/get_R_structures/<waferId>/<session>", methods=["GET"])
def getRStruct(waferId, session):
    """
    Used to get all structures that contain Resistance values
    """
    return jsonify(get_R_structures(waferId, session))


@app.route("/get_C_sessions/<waferId>", methods=["GET"])
def getCSess(waferId):
    """
    Used to get all session that contain Capacitance values
    """
    return jsonify(get_C_sessions(waferId))

@app.route("/get_C_structures/<waferId>/<session>", methods=["GET"])
def getCStruct(waferId, session):
    """
    Used to get all structures that contain Capacitance values
    """
    return jsonify(get_C_structures(waferId, session))


@app.route("/get_Cmes_sessions/<waferId>", methods=["GET"])
def getCmesSess(waferId):
    """
    Used to get all session that contain Measured Capacitance values
    """
    return jsonify(get_Cmes_sessions(waferId))

@app.route("/get_Cmes_structures/<waferId>/<session>", methods=["GET"])
def getCmesStruct(waferId, session):
    """
    Used to get all structures that contain Measured Capacitance values
    """
    return jsonify(get_Cmes_structures(waferId, session))

@app.route("/get_normal_values/<waferId>", methods=["GET"])
def get_normal_values(waferId):
    """
        Used for getting all extracted values in a wafer (Leak, R, C, Cmes and/or VBD)
    """
    return jsonify(get_values(waferId))

@app.route("/excel_normal_Cmes/<waferId>/<sessions>/<structures>/<coords>/<filename>", methods=["GET"])
def Cmes_excel_normal(waferId, sessions, structures, coords, filename):
    """
        Used for saving normal distribution of Cmes in an excel file.
        We first refactor received information and then call the function
    """
    sessions = sessions.split(',')
    structures = structures.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")

    excel_normal_Cmes(waferId, sessions, structures, coords, filename)

    return jsonify({'result': 'success'}), 200


@app.route("/excel_normal_C/<waferId>/<sessions>/<structures>/<coords>/<filename>", methods=["GET"])
def C_excel_normal(waferId, sessions, structures, coords, filename):
    """
        Used for saving normal distribution of C in an excel file.
        We first refactor received information and then call the function
    """
    sessions = sessions.split(',')
    structures = structures.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")

    excel_normal_C(waferId, sessions, structures, coords, filename)

    return jsonify({'result': 'success'}), 200


@app.route("/excel_normal_R/<waferId>/<sessions>/<structures>/<coords>/<filename>", methods=["GET"])
def R_excel_normal(waferId, sessions, structures, coords, filename):
    """
        Used for saving normal distribution of R in an excel file.
        We first refactor received information and then call the function
    """
    sessions = sessions.split(',')
    structures = structures.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")

    excel_normal_R(waferId, sessions, structures, coords, filename)

    return jsonify({'result': 'success'}), 200

@app.route("/excel_normal_Leak/<waferId>/<sessions>/<structures>/<coords>/<filename>", methods=["GET"])
def Leak_excel_normal(waferId, sessions, structures, coords, filename):
    """
        Used for saving normal distribution of Leakage in an excel file.
        We first refactor received information and then call the function
    """
    sessions = sessions.split(',')
    structures = structures.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")

    excel_normal_Leak(waferId, sessions, structures, coords, filename)

    return jsonify({'result': 'success'}), 200

@app.route("/excel_normal_VBD/<waferId>/<sessions>/<structures>/<coords>/<filename>", methods=["GET"])
def VBD_excel_normal(waferId, sessions, structures, coords, filename):
    """
        Used for saving normal distribution of VBD in an excel file.
        We first refactor received information and then call the function
    """
    sessions = sessions.split(',')
    structures = structures.split(',')
    coords = coords.replace("),(", ") (")
    coords = coords.split(" ")

    excel_normal_VBD(waferId, sessions, structures, coords, filename)

    return jsonify({'result': 'success'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=3000)
