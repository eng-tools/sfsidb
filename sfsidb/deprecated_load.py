import numpy as np
import warnings


def deprecation(message):
    warnings.warn(message, stacklevel=3)


def create_motion_code(test_name, sensor_code):
    return "%s-%s" % (test_name, sensor_code)


def create_sensor_code(si, mtype, sensor_number):
    return "%s-%s-%s-%s" % (mtype, si[mtype][sensor_number]['X-CODE'],
                                   si[mtype][sensor_number]['Y-CODE'],
                                   si[mtype][sensor_number]['Z-CODE'])


def get_mtype_and_number_from_code(si, code):
    mtype, x, y, z = code.split("-")
    for i in range(1, len(si[mtype]) + 1):
        if create_sensor_code(si, mtype, i) == code:
            return mtype, i
    return None, None


def get_sensor_by_number(sensor_folder_path, si, mtype, sensor_number):
    sensor_code = create_sensor_code(si, mtype, sensor_number)
    return get_sensor_by_code(sensor_folder_path, sensor_code)


def get_sensor_by_code(sensor_folder_path, sensor_code):

    motion_code = create_motion_code(sensor_code)

    suffix = '_filtered'
    fname = "%s%s.txt" % (motion_code, suffix)
    return load_record(sensor_folder_path + fname)


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


def load_record_only(ffp, dbset, quiet=False):
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
    return series


def load_record_and_time(ffp, dbset, quiet=False):
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


def load_record_and_dt(ffp, dbset, quiet=False):
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
    return series, dt


def sensor_code_to_name(code):
    codes = {
        "ACCX": "Horizontal acceleration",
        "PPT": "Pore pressure"
    }
    return codes[code]


def x_location_to_name(x_loc):
    xcodes = {
        "UB1": "Under building",
        "FFS": "Free-field (South)"
    }
    return xcodes[x_loc]


def y_location_to_name(y_loc):
    ycodes = {
        "S": "Surface",
        "L2C": "Centre Layer 2"
    }
    return ycodes[y_loc]
