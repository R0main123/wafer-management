import os
import shutil
import patoolib


def handle_file(file_path):
    """
    This function takes the path of a file and uncompress and convert it into a txt file.
    Files that can be handled: .tbl.Z, .tbl and .txt
    After conversion, the original file is deleted from the DataFiles folder

    :param <str> file_path: path of the file to be converted


    :return <str>: path of the converted file
    """
    file_name, file_extension = os.path.splitext(file_path)

    if file_extension == ".Z":
        # Decompress the file
        patoolib.extract_archive(file_path, outdir=".\DataFiles\\")
        file_path = file_name
        file_name, file_extension = os.path.splitext(file_path)

    if file_extension == ".tbl":
        # Rename .tbl to .txt
        new_file_path = file_name + ".txt"
        os.rename(file_path, new_file_path)
        file_path = new_file_path

    for filename in os.listdir(".\DataFiles\\"):
        if not filename.endswith('.txt'):
            file_path = os.path.join(".\DataFiles\\", filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))

    # If file extension is .txt, do nothing
    if file_path.endswith(".txt"):
        return file_path
