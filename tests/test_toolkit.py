from sfsidb import load as sload
from sfsidb import toolkit
from sfsidb import checking_tools as ct

from sfsidb import sensor_file_reader as sfr
from tests.conftest import TEST_DATA_DIR


def test_get_depth_from_sensor_code():
    sensor_ffp = TEST_DATA_DIR + "test-sensor-file.json"
    si = sfr.read_json_sensor_file(sensor_ffp)
    mtype = "ACC"
    sensor_number = 2
    code = sload.get_sensor_code_by_number(si, mtype, sensor_number)
    assert code == "ACCX-NFF-S-M"
    print(code)
    depth = toolkit.get_depth_by_code(si, code)
    assert depth == 0.0

    code = "ACCX-UB2-L2C-M"  # number = 4
    depth = toolkit.get_depth_by_code(si, code)
    assert ct.isclose(depth, 63.6)


def test_old_style_sensor_code_file():
    sensor_ffp = TEST_DATA_DIR + "test-old-sensor-file.json"
    si = sfr.read_json_sensor_file(sensor_ffp)
    sensor_code = "ACCX-NFF-L2C-M"
    depth = toolkit.get_depth_by_code(si, sensor_code)
    assert ct.isclose(depth, 63.6)


if __name__ == '__main__':
    test_old_style_sensor_code_file()