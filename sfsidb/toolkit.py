from sfsidb import load


def get_surface_height(si):
    mtype = "ACC"
    if "ACCX" in si:  # support for old sensor files.
        mtype = "ACCX"
    for i in range(1, len(si[mtype]) + 1):
        if si[mtype][i]["Y-CODE"] == "S":
            return si[mtype][i]["y"]
    return None


def get_depth_by_code(si, sensor_code):
    mtype, sensor_number = load.get_mtype_and_number_from_code(si, sensor_code)
    if sensor_number is None:
        raise KeyError("Depth not found for sensor_code: %s" % sensor_code)
    max_depth = get_surface_height(si)
    return max_depth - si[mtype][sensor_number]['y']


