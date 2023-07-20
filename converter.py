import os
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

    print(f"File extension: {file_extension}")

    # If file extension is .txt, do nothing
    if file_extension == '.txt' or file_extension == '.tbl' or file_extension == '.lim' or file_extension == '':
        return file_path
