import glob
import json
import math

from pymongo import MongoClient
from flask_cors import CORS
from flask_socketio import SocketIO
from flask import Flask, request, jsonify, send_from_directory
import os
import timeit

from excel import wanted_excel
from new_manage_DB import create_db, setCompliance, create_db_tbl, get_db_name, create_db_lim
from plot_and_powerpoint import plot_wanted_matrices, wanted_ppt
from converter import handle_file
from getter import get_types, get_temps, get_filenames, get_coords, get_compliance, get_sessions, get_wafer, \
    get_structures, get_map_sessions, connexion, get_map_structures

from filter import filter_by_meas, filter_by_temp, filter_by_coord, filter_by_filename, filter_by_session
from VBD import create_wafer_map

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
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory(os.path.join(app.static_folder, 'static', 'js'), path)


@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory(os.path.join(app.static_folder, 'static', 'css'), path)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("my-app/build/" + path):
        return send_from_directory("my-app/build", path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/static/<path:path>')
def send_static_files(path):
    return send_from_directory('my-app/build/static', path)


@app.route('/upload', methods=['POST'])
def upload():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    files = request.files.getlist("file")
    print(files)

    for file in files:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        processed_file = handle_file(file_path)

        if processed_file is not None:
            all_files.append(processed_file)
            
        print(all_files)

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
    if request.method == 'POST':
        start_time = timeit.default_timer()

        for file in all_files:

            filename = file.split("\\")[-1]
            socketio.emit('message', {'data': f"Creating database for file {filename}"})
            if file.split('.')[-1] == 'txt':
                create_db(file, checkbox_checked)

            elif file.split('.')[-1] == 'tbl':
                create_db_tbl(file, checkbox_checked)

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
    collection = connexion()
    wafers = collection.find({})
    wafer_ids = []
    for wafer in wafers:
        wafer_ids.append(wafer["wafer_id"])

    return jsonify(wafer_ids)


@app.route('/get_structures/<wafer_id>/<session>', methods=['GET'])
def get_structures_json(wafer_id, session):
    wafer = get_wafer(wafer_id)
    structures = []
    for structure in wafer[session]:
        structures.append(structure)
    return jsonify(structures), 200


@app.route('/get_all_structures/<wafer_id>', methods=['GET'])
def get_all_structures(wafer_id):
    all_structures = []
    sessions = get_sessions(wafer_id)
    for session in sessions:
        structures = get_structures(wafer_id, session)
        for structure in structures:
            all_structures.append(structure)
    return jsonify(list(set(all_structures))), 200


@app.route('/get_sessions/<wafer_id>', methods=['GET'])
def get_sessions_server(wafer_id):
    print(jsonify(get_sessions(wafer_id)))
    return jsonify(get_sessions(wafer_id)), 200


@app.route('/get_all_types/<wafer_id>', methods=['GET'])
def get_all_types(wafer_id):
    return jsonify(get_types(wafer_id)), 200


@app.route('/get_all_temps/<wafer_id>', methods=['GET'])
def get_all_temps(wafer_id):
    return jsonify(get_temps(wafer_id)), 200


@app.route('/get_all_coords/<wafer_id>', methods=['GET'])
def get_all_coords(wafer_id):
    return jsonify(get_coords(wafer_id)), 200


@app.route('/get_all_filenames/<wafer_id>', methods=['GET'])
def get_all_filenames(wafer_id):
    return jsonify(get_filenames(wafer_id)), 200


@app.route('/filter_by_Meas/<wafer_id>/<selectedMeasurement>', methods=['GET'])
def filter_by_Meas(wafer_id, selectedMeasurement):
    return jsonify(filter_by_meas(selectedMeasurement, wafer_id)), 200


@app.route('/filter_by_Temps/<wafer_id>/<selectedMeasurement>', methods=['GET'])
def filter_by_Temps(wafer_id, selectedMeasurement):
    return jsonify(filter_by_temp(selectedMeasurement, wafer_id)), 200


@app.route('/filter_by_Coords/<wafer_id>/<selectedMeasurement>', methods=['GET'])
def filter_by_Coords(wafer_id, selectedMeasurement):
    return jsonify(filter_by_coord(selectedMeasurement, wafer_id)), 200


@app.route('/filter_by_Filenames/<wafer_id>/<selectedMeasurement>', methods=['GET'])
def filter_by_Filenames(wafer_id, selectedMeasurement):
    return jsonify(filter_by_filename(selectedMeasurement, wafer_id)), 200


@app.route('/filter_by_Session/<wafer_id>/<selectedMeasurement>', methods=['GET'])
def filter_by_Session(wafer_id, selectedMeasurement):
    return jsonify(filter_by_session(selectedMeasurement, wafer_id)), 200


# TODO
@app.route('/get_matrices/<wafer_id>/<structure_id>', methods=['GET'])
def get_matrices(wafer_id, structure_id):
    wafer = get_wafer(wafer_id)
    matrices = []

    sessions = get_sessions(wafer_id)
    for session in sessions:
        for matrix in wafer[session][structure_id]["matrices"]:
            matrices.append(f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})')
    return jsonify(matrices)


@app.route('/excel_structure/<waferId>/<sessions>/<structures>/<types>/<temps>/<files>/<coords>/<file_name>', methods=['GET'])
def excel_structure_route(waferId, sessions, structures, types, temps, files, coords, file_name):
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
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    db[get_db_name()].delete_one({'wafer_id': wafer_id})
    return jsonify({'result': 'success'}), 200


@app.route("/get_compl/<waferId>/<session>", methods=["GET"])
def get_compl(waferId, session):
    return jsonify(get_compliance(waferId, session))


@app.route("/set_compl/<waferId>/<session>/<compliance>")
def set_compl(waferId, session, compliance):
    setCompliance(waferId, session, compliance)
    return jsonify({'result': 'success'}), 200


@app.route("/create_wafer_map/<waferId>/<session>/<structure>", methods=["GET"])
def personal_wafer_map(waferId, session, structure):
    image = create_wafer_map(waferId, session, structure)
    return jsonify(image)


@app.route("/plot_selected_matrices/<waferId>/<sessions>/<structures>/<types>/<temps>/<files>/<coords>", methods=["GET"])
def plot_we_want(waferId, sessions, structures, types, temps, files, coords):
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
    return jsonify(get_map_sessions(wafer_id)), 200

@app.route('/get_map_structures/<wafer_id>/<session>', methods=['GET'])
def get_map_structures_server(wafer_id, session):
    return jsonify(get_map_structures(wafer_id, session)), 200

"""
@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/write_excel/<wafer_id>', methods=['POST'])
def write_excel_route(wafer_id):
    writeExcel(wafer_id)
    return render_template('done.html', message='Excel file successfully created!')


@app.route('/write_ppt/<wafer_id>', methods=['POST'])
def write_ppt_route(wafer_id):
    writeppt(wafer_id)
    return render_template('done.html', message='PowerPoint file successfully created!')


@app.route('/ppt_structure/<wafer_id>/<structure_ids>/<file_name>', methods=['GET'])
def ppt_structure_route(wafer_id, structure_ids, file_name):
    structure_ids = structure_ids.split(',')
    ppt_structure(wafer_id, structure_ids, file_name)
    return render_template('done.html', message='PowerPoint file successfully created!')


@app.route('/open')
def open():
    client = MongoClient('mongodb://localhost:27017/')

    db = client['Measurements']

    collection = db["Wafers"]

    wafers = collection.find({})

    return render_template('open.html', wafers=wafers)


@app.route('/upload', methods=['POST'])
def upload():
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

    return redirect(url_for('options'))  # Assurez-vous de rediriger vers la bonne route



@app.route("/get_matrices_with_I/<wafer_id>/<structure_id>", methods=["GET"])
def get_matrices_for_VBD(wafer_id, structure_id):
    return jsonify(get_matrices_with_I(wafer_id, structure_id))


@app.route("/calculate_breakdown/<wafer_id>/<structure_id>/<x>/<y>/<compliance>", methods=["GET"])
def flask_calculate_breakdown(wafer_id, structure_id, x, y, compliance):
    X, Y = get_vectors_in_matrix(wafer_id, structure_id, x, y)

    if compliance != 'null':
        Breakd_Volt, Breakd_Leak, reached_comp, high_leak = calculate_breakdown(X, Y, compliance)

    else:
        Breakd_Volt, Breakd_Leak, reached_comp, high_leak = calculate_breakdown(X, Y)

    if np.isnan(Breakd_Volt):
        return jsonify("NaN")
    else:
        return jsonify(Breakd_Volt)


@app.route("/calculate_breakdown/<wafer_id>/<structure_id>/<x>/<y>/", methods=["GET"])
def flask_calculate_breakdown_wout_compl(wafer_id, structure_id, x, y):
    X, Y = get_vectors_in_matrix(wafer_id, structure_id, x, y)

    Breakd_Volt, Breakd_Leak, reached_comp, high_leak = calculate_breakdown(X, Y)

    if np.isnan(Breakd_Volt):
        return jsonify("NaN")
    else:
        return jsonify(Breakd_Volt)


@app.route("/get_vectors_in_matrix/<waferId>/<structureId>/<x>/<y>")
def get_vectors_for_matrix(waferId, structureId, x, y):
    return jsonify(get_vectors_in_matrix(waferId, structureId, x, y))


@app.route("/create_wafer_map/<waferId>/<structureId>")
def wafer_map(waferId, structureId):
    image = create_wafer_map(waferId, structureId)
    return jsonify({"image": image})


@app.route("/create_wafer_map/<waferId>/<structureId>/<compliances>")
def personal_wafer_map(waferId, structureId, compliances):
    image = create_wafer_map(waferId, structureId, compliances)
    return jsonify({"image": image})


@app.route("/get_matrices_and_compliances/<wafer_id>/<structure_id>")
def getAllInfos(wafer_id, structure_id):
    return jsonify(get_all_infos_matrices(wafer_id, structure_id))

@app.route("/reg_vbd/<waferId>/<structureId>/<x>/<y>/<compliance>", methods=["GET"])
def reg_VBD(waferId, structureId, x, y, compliance):
    register_VBD(waferId, structureId, x, y, compliance)
    return jsonify({'result': 'success'}), 200

"""

if __name__ == '__main__':
    app.run(debug=True, port=3000)
