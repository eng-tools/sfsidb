import numpy as np
import pytest

from sfsidb import load as sload
from sfsidb import sensor_file_reader as sfr
from tests.conftest import TEST_DATA_DIR
from tests import dbset_for_tests as dbset


def test_get_sensor_code_by_number():
    sensor_ffp = TEST_DATA_DIR + "test-sensor-file.json"
    si = sfr.read_json_sensor_file(sensor_ffp)
    mtype = "ACC"
    sensor_number = 2
    code = sload.get_sensor_code_by_number(si, mtype, sensor_number)
    print(code)
    assert code == "ACCX-NFF-S-M"

    mtype = "DISP"
    sensor_number = 4
    code = sload.get_sensor_code_by_number(si, mtype, sensor_number)
    assert code == "DISPY-UNB2-S-M"
    print(code)


def test_get_sensor_code_by_number_out_of_bounds():
    sensor_ffp = TEST_DATA_DIR + "test-sensor-file.json"
    si = sfr.read_json_sensor_file(sensor_ffp)
    mtype = "ACC"
    sensor_number = 1000
    with pytest.raises(KeyError):
        sload.get_sensor_code_by_number(si, mtype, sensor_number, quiet=False)
    sload.get_sensor_code_by_number(si, mtype, sensor_number, quiet=True)


def test_load_record():

    expected_acc = np.arange(1, 5)
    expected_dt = 0.01
    max_time = 0.04

    db_fp = TEST_DATA_DIR
    soil_profile = 2
    m_id = 3
    sensor_code = "ACCX-FFS-L2C-M"
    local_path_ext = dbset.build_local_path_extension(soil_profile, m_id)
    test_name = dbset.build_test_name(m_id)
    sload.create_motion_name(test_name, sensor_code, dbset.CODE_SUFFIX)

    acc = sload.load_record_only(db_fp, local_path_ext, test_name, sensor_code, dbset, quiet=False)
    for i in range(len(expected_acc)):
        assert acc[i] == expected_acc[i], i

    acc2, dt = sload.load_record_and_dt(db_fp, local_path_ext, test_name, sensor_code, dbset, quiet=False)
    for i in range(len(expected_acc)):
        assert acc2[i] == expected_acc[i], i
    assert dt == expected_dt

    acc, time = sload.load_record_and_time(db_fp, local_path_ext, test_name, sensor_code, dbset, quiet=False)
    for i in range(len(expected_acc)):
        assert acc[i] == expected_acc[i], i
    assert time[-1] == max_time, time[-1]


def test_load_record_with_wild():
    expected_acc = np.arange(1, 5)

    db_fp = TEST_DATA_DIR
    soil_profile = 2
    m_id = 3
    sensor_code = "ACCX-*-L2C-M"
    local_path_ext = dbset.build_local_path_extension(soil_profile, m_id)
    test_name = dbset.build_test_name(m_id)
    sload.create_motion_name(test_name, sensor_code, dbset.CODE_SUFFIX)

    acc = sload.load_record_only(db_fp, local_path_ext, test_name, sensor_code, dbset, quiet=False)
    for i in range(len(expected_acc)):
        assert acc[i] == expected_acc[i], i

    accs = sload.load_record_only(db_fp, local_path_ext, test_name, sensor_code, dbset, quiet=False, first=False)
    acc = accs[0]
    for i in range(len(expected_acc)):
        assert acc[i] == expected_acc[i], i

    accs, dts = sload.load_record_and_dt(db_fp, local_path_ext, test_name, sensor_code, dbset, quiet=False, first=False)
    acc = accs[0]
    for i in range(len(expected_acc)):
        assert acc[i] == expected_acc[i], i

    accs, times = sload.load_record_and_time(db_fp, local_path_ext, test_name, sensor_code, dbset, quiet=False, first=False)
    acc = accs[0]
    for i in range(len(expected_acc)):
        assert acc[i] == expected_acc[i], i


def test_sensor_code_to_name():
    sensor_code = "ACCX-FFS-L2C-M"
    sname = sload.sensor_code_to_name(sensor_code, part="sensor")
    assert sname == "Horizontal acceleration", sname
    xname = sload.sensor_code_to_name(sensor_code, part="xloc")
    assert xname == "Free-field (South)", xname
    yname = sload.sensor_code_to_name(sensor_code, part="yloc")
    assert yname == "Centre Layer 2", yname




if __name__ == '__main__':
    test_load_record_with_wild()
    # test_load_record()
