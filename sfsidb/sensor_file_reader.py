import json
from collections import OrderedDict


def read_json_sensor_file(ffp):
    """
    Reads the sensor file and stores it as a dictionary.
    :param exp:
    :return:
    """
    sensor_path = ffp
    si = json.load(open(sensor_path))
    for mtype in si:  # Convert keys from strings to integers
        si[mtype] = {int(k): v for k, v in si[mtype].items()}
    return si


def _read_xlsx_sensor_file(full_path):
    """
    Read information about sensors from xlsx file.
    :param full_path: Path to xlsx file.
    :param mtype: can chose to only read one sensor type
    :return: OrderedDict object of sensor information
    """
    import openpyxl

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    wb2 = openpyxl.load_workbook(full_path, data_only=True)
    mtypes = ["ACC", "DISP", "PPT", "STRS", "STRV", "TAU", "SIG"]
    #for mtype in mtypes:
    xi = wb2.get_sheet_by_name("ALL")
    si = OrderedDict()
    sensor_dict = {}
    for mtype in mtypes:
        si[mtype] = OrderedDict()
        sensor_dict[mtype] = OrderedDict()
    titles = []
    for i in range(xi.max_column):
        col = alphabet[i]
        titles.append(xi["%s1" % col].value)
    i = 0
    for row in xi.rows:
        i += 1
        if i < 2:
            continue
        if row[0].value is None:
            break
        sensor_type = row[1].value
        if sensor_type not in sensor_dict:
            sensor_dict[sensor_type] = OrderedDict()
            si[sensor_type] = OrderedDict()
        sensor_dict[sensor_type][int(row[0].value)] = OrderedDict()

        for c in range(len(row) - 1):
            sensor_dict[sensor_type][row[0].value][titles[c]] = row[c].value
    # order sensors
    for mtype in sensor_dict:
        si[mtype] = OrderedDict(sorted(sensor_dict[mtype].items()))

    return si


def build_json_sensor_file(xlsx_ffp, json_ffp):
    """
    Converts the xlsx sensor file into a json file.
    :param xlsx_ffp: full file path to xlsx sensor file
    :param json_ffp: full file path to the output json sensor file
    :return: None
    """

    si = _read_xlsx_sensor_file(xlsx_ffp)
    para = json.dumps(si, indent=4)
    a = open(json_ffp, "w")
    a.write(para)
    a.close()
