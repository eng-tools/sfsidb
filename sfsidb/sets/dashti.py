import numpy as np
import glob

CODE_SUFFIX = '_filtered'
SENSOR_FILE_TYPE = ".txt"
SENSOR_DATA_DELIMITER = ","
SENSOR_DATA_SKIP_ROWS = 0


def build_local_path_extension(exp_number, in_stage, event_number):
    return "SHD0%i/records/%s/Trial-%i/" % (exp_number, in_stage, event_number)


def build_test_name(exp_number, event_number, **kwargs):
    return "E%i-T%i" % (exp_number, event_number)


def create_file_name(test_name, sensor_code, **kwargs):
    file_name = "%s-%s%s%s" % (test_name, sensor_code, CODE_SUFFIX, SENSOR_FILE_TYPE)
    return file_name


def load_a_record_and_dt(full_file_path):
    data = np.loadtxt(full_file_path,
                      dtype='float',
                      delimiter=SENSOR_DATA_DELIMITER,
                      skiprows=SENSOR_DATA_SKIP_ROWS)
    time = data[:, 0]
    dt = time[1] - time[0]
    series = data[:, 1]
    return series, dt


# Leave this as-is
def wild_load_record_and_dt(folder_path, test_name, sensor_code, quiet=False, first=True):
    file_name = create_file_name(test_name, sensor_code)
    full_wild_file_path = folder_path + file_name
    files = glob.glob(full_wild_file_path)
    files.sort()
    if first:
        if len(files) == 0:
            if quiet:
                return None
            else:
                raise FileNotFoundError("No matching %s" % full_wild_file_path)
        full_file_path = files[0]
        return load_a_record_and_dt(full_file_path)
    else:
        recs = []
        dts = []
        for full_file_path in files:
            rec, dt = load_a_record_and_dt(full_file_path)
            recs.append(rec)
            dts.append(dt)
        return np.array(recs), np.array(dts)

