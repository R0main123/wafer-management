from pymongo import MongoClient
from flask_cors import CORS
from flask_socketio import SocketIO
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
import os
import timeit
import numpy as np

from excel import writeExcel, excel_structure
from manage_DB import create_db, register_compliance, register_VBD
from plot_and_powerpoint import writeppt, ppt_structure, ppt_matrix
from converter import handle_file
from getter import get_types, get_temps, get_filenames, get_coords, get_compliance, get_VBDs, get_matrices_with_I, \
    get_all_infos_matrices
from filter import filter_by_meas, filter_by_temp, filter_by_coord, filter_by_filename
from VBD import calculate_breakdown, get_vectors_in_matrix, create_wafer_map, create_personal_wafer_map

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
    for file in files:

        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        processed_file = handle_file(file_path)

        if processed_file is not None:
            all_files.append(processed_file)


    return jsonify({'result': 'success'}), 200

@app.route('/options/<checkbox_checked>', methods=['GET', 'POST'])
def options(checkbox_checked):
    if request.method == 'POST':
        start_time = timeit.default_timer()

        for file in all_files:

            filename = file.split("\\")[-1]
            socketio.emit('message', {'data': f"Creating database for file {filename}"})
            data_list = create_db(file, checkbox_checked)

            socketio.emit('message', {'data': f"Processing {filename}"})

            if os.path.isfile(file):
                os.remove(file)

        all_files.clear()

        if os.path.isdir("DataFiles"):
            if not os.listdir("DataFiles"):
                os.rmdir("DataFiles")

        socketio.emit('message', {'data': "Finished processing."})

        end_time = timeit.default_timer()
        print(f"Finished in {end_time - start_time} seconds")

        return jsonify({'result': 'success'})

    else:
        return jsonify({'result': 'success'})


@app.route('/open')
def open():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]

    wafers = collection.find({})
    wafer_ids = []
    for wafer in wafers:
        wafer_ids.append(wafer["wafer_id"])

    return jsonify(wafer_ids)


@app.route('/get_structures/<wafer_id>', methods=['GET'])
def get_structures(wafer_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    wafer = db.Wafers.find_one({'wafer_id': wafer_id})
    structures = []
    for structure in wafer["structures"]:
        structures.append(structure["structure_id"])
    return jsonify(structures), 200


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


@app.route('/get_matrices/<wafer_id>/<structure_id>', methods=['GET'])
def get_matrices(wafer_id, structure_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    collection = db["Wafers"]
    wafer = collection.find_one({"wafer_id": wafer_id})
    structure = [s for s in wafer["structures"] if s["structure_id"] == structure_id][0]
    matrices = []
    for matrix in structure["matrices"]:
        matrices.append(f'({matrix["coordinates"]["x"]},{matrix["coordinates"]["y"]})')
    return jsonify(matrices)

@app.route('/plot_matrix/<wafer_id>/<coordinates>', methods=['GET'])
def plot_matrix(wafer_id=str, coordinates=str):
    return jsonify(ppt_matrix(wafer_id, coordinates))

@app.route('/excel_structure/<wafer_id>/<structure_ids>/<file_name>', methods=['GET'])
def excel_structure_route(wafer_id, structure_ids, file_name):
    structure_ids = structure_ids.split(',')
    excel_structure(wafer_id, structure_ids, file_name)
    return jsonify({'result': 'success'})

@app.route('/ppt_structure/<wafer_id>/<structure_ids>/<file_name>', methods=['GET'])
def ppt_structure_route(wafer_id, structure_ids, file_name):
    print(wafer_id, structure_ids, file_name)
    structure_ids = structure_ids.split(',')
    ppt_structure(wafer_id, structure_ids, file_name)
    print("Here")
    return jsonify({'result': 'success'})

@app.route('/delete_wafer/<wafer_id>', methods=['DELETE'])
def delete_wafer(wafer_id):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['Measurements']
    db.Wafers.delete_one({'wafer_id': wafer_id})
    return jsonify({'result': 'success'}), 200

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


@app.route("/get_breakdown/<wafer_id>/<structure_id>/<x>/<y>/", methods=["GET"])
def flask_get_breakdown(wafer_id, structure_id, x, y):
    return jsonify(get_VBDs(wafer_id, structure_id, x, y))


@app.route("/get_vectors_in_matrix/<waferId>/<structureId>/<x>/<y>")
def get_vectors_for_matrix(waferId, structureId, x, y):
    return jsonify(get_vectors_in_matrix(waferId, structureId, x, y))


@app.route("/get_compl/<waferId>/<structureId>")
def get_compl(waferId, structureId):
    compliance = get_compliance(waferId, structureId)
    if compliance is None:
        return jsonify("")
    else:
        return jsonify(compliance)


@app.route("/create_wafer_map/<waferId>/<structureId>")
def wafer_map(waferId, structureId):
    image = create_wafer_map(waferId, structureId)
    return jsonify({"image": image})


@app.route("/create_personal_wafer_map/<waferId>/<structureId>/<compliances>")
def personal_wafer_map(waferId, structureId, compliances):
    image = create_personal_wafer_map(waferId, structureId, compliances)
    return jsonify({"image": image})


@app.route("/get_matrices_and_compliances/<wafer_id>/<structure_id>")
def getAllInfos(wafer_id, structure_id):
    return jsonify(get_all_infos_matrices(wafer_id, structure_id))


@app.route("/set_compl/<waferId>/<structureId>/<compliance>")
def set_compl(waferId, structureId, compliance):
    register_compliance(waferId, structureId, compliance)
    return jsonify({'result': 'success'}), 200


@app.route("/reg_vbd/<waferId>/<structureId>/<x>/<y>/<compliance>/<VBD>")
def reg_VBD(waferId, structureId, x, y, compliance, VBD):
    register_VBD(waferId, structureId, x, y, compliance, VBD)
    return jsonify({'result': 'success'}), 200"""


if __name__ == '__main__':
    app.run(debug=True, port=3000)
