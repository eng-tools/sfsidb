from sfsidb import load


def get_surface_height(si):
    for mtype in si:
        for m_number in si[mtype]:
            if si[mtype][m_number]["Y-CODE"] == "S":
                return si[mtype][m_number]["y"]
    return None


def get_depth_by_code(si, sensor_code):
    mtype, sensor_number = load.get_mtype_and_number_from_code(si, sensor_code)
    if sensor_number is None:
        raise KeyError("Depth not found for sensor_code: %s" % sensor_code)
    max_depth = get_surface_height(si)
    return max_depth - si[mtype][sensor_number]['y']


