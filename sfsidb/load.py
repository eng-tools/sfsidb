import numpy as np
import warnings
from sfsidb import constants
import glob


def deprecation(message):
    warnings.warn(message, stacklevel=3)


def create_motion_name(test_name, sensor_code, code_suffix=""):
    """
    Builds the full name of the file

    :param test_name: str, test name
    :param sensor_code: str, a sensor code (e.g. ACCX-UB1-L2C-M)
    :param code_suffix: str, suffix
    :return:
    """
    return "%s-%s-%s" % (test_name, sensor_code, code_suffix)


def get_sensor_code_by_number(si, mtype, sensor_number, quiet=False):
    """
    Given a sensor number, get the full sensor code (e.g. ACCX-UB1-L2C-M)

    :param si: dict, sensor index json dictionary
    :param mtype: str, sensor type
    :param sensor_number: int, number of sensor
    :param quiet: bool, if true then return None if not found
    :return: str or None, sensor_code: a sensor code (e.g. ACCX-UB1-L2C-M)
    """
    try:
        if 'Orientation' in si[mtype][sensor_number]:
            orientation = si[mtype][sensor_number]['Orientation']
        else:
            orientation = ""
        return "%s%s-%s-%s-%s" % (mtype,
                                orientation,
                                si[mtype][sensor_number]['X-CODE'],
                                si[mtype][sensor_number]['Y-CODE'],
                                si[mtype][sensor_number]['Z-CODE'])
    except KeyError:
        if quiet:
            return None
        raise


def get_mtype_and_number_from_code(si, sensor_code):
    """
    Given a sensor sensor_code, get motion type and sensor number

    :param si: dict, sensor index json dictionary
    :param sensor_code: str, a sensor code (e.g. ACCX-UB1-L2C-M)
    :return:
    """
    mtype_and_ory, x, y, z = sensor_code.split("-")
    if mtype_and_ory[-1] in "XYZ":
        mtype = mtype_and_ory[:-1]
    else:
        mtype = mtype_and_ory
    for i in range(1, len(si[mtype]) + 1):
        if get_sensor_code_by_number(si, mtype, i) == sensor_code:
            return mtype, i
    return None, None


def load_record(ffp, dbset, quiet=False):
    deprecation('Deprecated, switch to load_record_and_time, load_record_and_dt')
    # raise Warning("Deprecated, switch to load_record_and_time, load_record_and_dt")
    if quiet:
        try:
            data = np.loadtxt(ffp + dbset.SENSOR_FILE_TYPE,
                              dtype='float',
                              delimiter=dbset.SENSOR_DATA_DELIMITER,
                              skiprows=dbset.SENSOR_DATA_SKIP_ROWS)
        except FileNotFoundError:
            print("File not found: ", ffp + dbset.SENSOR_FILE_TYPE)
            return None, None
        except IOError:
            print("File not found: ", ffp + dbset.SENSOR_FILE_TYPE)
            return None, None
    else:
        data = np.loadtxt(ffp + dbset.SENSOR_FILE_TYPE,
                              dtype='float',
                              delimiter=dbset.SENSOR_DATA_DELIMITER,
                              skiprows=dbset.SENSOR_DATA_SKIP_ROWS)
    time = data[:, 0]
    dt = time[1] - time[0]
    series = data[:, 1]
    return series, time


def get_available_sensor_codes(ffp, local_path_ext, wild_sensor_code, dbset):
    file_name = dbset.create_file_name("*", wild_sensor_code)
    full_wild_file_path = ffp + local_path_ext + file_name
    files = glob.glob(full_wild_file_path)
    files.sort()
    import re
    compiled = re.compile(wild_sensor_code)

    for ff in range(len(files)):
        ms = compiled.match(files[ff])
        # files[ff] = ms
        # sname = files[ff].split(local_path_ext)[-1]
        # sname = sname.split()
        # files[ff].replace(files[ff])
    return files



def load_record_only(db_fp, local_path_ext, test_name, sensor_code, dbset, quiet=False, first=True):
    """
    Finds the file and returns the time series of values

    :param db_fp: str, Database root directory
    :param local_path_ext: str, local path to sensor file from database root directory
    :param test_name: str, name of test used as prefix of file name
    :param sensor_code: str, a sensor code (e.g. ACCX-UB1-L2C-M)
    :param dbset: module, A database set module from sfsidb.sets
    :param quiet: bool, if True then return None
    :return:
    """
    folder_path = db_fp + local_path_ext
    rec_and_dt = dbset.wild_load_record_and_dt(folder_path, test_name, sensor_code, quiet, first)
    if rec_and_dt is None and quiet:
        return None
    return rec_and_dt[0]


def load_record_and_time(db_fp, local_path_ext, test_name, sensor_code, dbset, quiet=False, first=True):
    """
    Finds the file and returns the time series of values and the time series

    :param db_fp: str, Database root directory
    :param local_path_ext: str, local path to sensor file from database root directory
    :param test_name: str, name of test used as prefix of file name
    :param sensor_code: str, a sensor code (e.g. ACCX-UB1-L2C-M)
    :param dbset: module, A database set module from sfsidb.sets
    :param quiet: bool, if True then return None
    :return:
    """
    folder_path = db_fp + local_path_ext
    if first:
        rec, dt = dbset.wild_load_record_and_dt(folder_path, test_name, sensor_code, quiet, first=first)
        if rec is None and quiet:
            return None
        time = np.arange(1, len(rec) + 1) * dt
        return rec, time
    else:
        recs, dts = dbset.wild_load_record_and_dt(folder_path, test_name, sensor_code, quiet, first)
        times = []
        for i, dt in enumerate(dts):
            time = np.arange(1, len(recs[i]) + 1) * dt
            times.append(time)
        return recs, times


def load_record_and_dt(db_fp, local_path_ext, test_name, sensor_code, dbset, quiet=False, first=True):
    """
    Finds the file and returns the time series of values and the time step

    :param db_fp: str, Database root directory
    :param local_path_ext: str, local path to sensor file from database root directory
    :param test_name: str, name of test used as prefix of file name
    :param sensor_code: str, a sensor code (e.g. ACCX-UB1-L2C-M)
    :param dbset: module, A database set module from sfsidb.sets
    :param quiet: bool, if True then return None
    :return:
    """
    folder_path = db_fp + local_path_ext
    return dbset.wild_load_record_and_dt(folder_path, test_name, sensor_code, quiet, first)


def sensor_code_to_name(sensor_code, part="sensor"):
    """
    Converts a sensor code into written english.

    E.g. ACCX-UB1-L2C-M = Horizontal acceleration

    :param sensor_code: str, a sensor code (e.g. ACCX-UB1-L2C-M)
    :param part: str, what part of the code to convert
    :return: str
    """
    mtype_and_ory, x, y, z = sensor_code.split("-")

    if part == "sensor":
        return constants.sensor_type_codes[mtype_and_ory]
    elif part == "xloc":
        return constants.x_locations[x]
    elif part == "yloc":
        return constants.y_locations[y]

