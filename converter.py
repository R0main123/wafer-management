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


def traducer(line):
    """
    Used for converting tbl files into txt files. Parse a line and returns information into the format used in txt files.
    This function is called in tbl_to_txt.

    :param <str> line: Line to be parsed

    :return: Line converted to the format used in the txt files
    """
    if 'date' in line:
        info = ''.join(line.split('" ')[0].replace('"', '').replace('(', '').split())
        value = line.split('" ')[1].replace('"', '').replace(')', '')

    else:
        info = line.split('" ')[0].replace('"', '').replace('(', '').replace(' ', '')
        value = line.split('" ')[1].replace('"', '').replace(')', '').replace(' ', '')

    return f"{info} : {value}"


def tbl_to_txt(path):
    """
    Converts a tbl file into a txt file. The file is read, all information is converted and saved in a list and then we write all at once in an empty txt file.

    :param path: Path of the file to be converted
    """
    if not os.path.exists("Converted Files\\"):
        os.makedirs("Converted Files\\")

    filename = path.split('@@@')[-1]
    filename = "".join(filename.split('.')[:-1]) + '.txt'
    filename = filename.split("\\")[-1]
    filename = "Converted Files\\"+filename

    translated = []
    with open(path, 'r') as input:
        while True:
            line = next((l for l in input if l.split() == ['(record']), None)
            if line is None:
                break

            while ')' not in line:
                line = next((l for l in input), None)
                if line is None:
                    break

            while line.split() != [')']:
                translated.append(traducer(line))
                line = next((l for l in input), None)
                if line is None:
                    break

            while '(' not in line:
                line = next((l for l in input), None)
                if line is None:
                    break

            while ')' not in line:
                line = next((l for l in input), None)
                if line is None:
                    break

            while ')' in line:
                translated.append(traducer(line))
                line = next((l for l in input), None)
                if line is None:
                    break

            while ')' not in line:
                line = next((l for l in input), None)
                if line is None:
                    break

            while line.split() != ['("session"']:
                info = line.split('" "')[1].replace('"', '').replace(')', '').replace('\n', '')
                line = next((l for l in input), None)

                unit = line.split('" "')[1].replace('"', '').replace(')', '')

                if 'none' in unit:
                    unit = '\n'
                line = next((l for l in input), None)

                value = line.split('" ')[1].replace('"', '').replace(')', '').replace('\n', '')

                translated.append(f"{info} : {value} {unit if unit != 'none' else ''}")

                line = next((l for l in input), None)
                if line is None:
                    break

                while '(' not in line:
                    line = next((l for l in input), None)
                    if line is None:
                        break

                if line.split() == ['("session"']:
                    break

                while ')' not in line:
                    line = next((l for l in input), None)
                    if line is None:
                        break

            while ')' not in line:
                line = next((l for l in input), None)
                if line is None:
                    break

            while line.split() != [')']:
                translated.append(traducer(line))
                line = next((l for l in input), None)
                if line is None:
                    break

            while '(' not in line:
                line = next((l for l in input), None)
                if line is None:
                    break

            while ')' not in line:
                line = next((l for l in input), None)
                if line is None:
                    break

            nrCurves = int(line.split('" ')[1].replace('"', '').replace(')', ''))
            line = next((l for l in input), None)
            if line is None:
                break

            infos = line.split()[1:nrCurves+1]
            final = ''
            for item in infos:
                item = item.replace('"', '').replace(')', '')
                final += item + ' '
            translated.append(f"curveValue : {final[:-1]}\nBOD\n")


            line = next((l for l in input if 'sweepValue' in l), None)
            values = line.replace(')', '')
            values = values.split()[1:]

            line = next((l for l in input), None)
            i = 0
            results = [f"\t{value}" for value in line.split()[1:nrCurves+1]]
            translated.append(f"{values[i]}{''.join(results)}\n")

            line = next((l for l in input), None)
            i += 1

            while ')' not in line:
                results = [f"\t{value}" for value in line.split()[0:nrCurves]]
                translated.append(f"{values[i]}{''.join(results)}\n")

                line = next((l for l in input), None)
                i += 1

            results = [f"\t{value}" for value in line.split()[0:nrCurves]]
            results[-1] = results[-1].replace(')', '')
            translated.append(f"{values[i]}{''.join(results)}\nEOD\n")

    with open(filename, 'w') as output:
        for line in translated:
            output.write(line)



