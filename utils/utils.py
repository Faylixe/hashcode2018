def distance(ab, xy):
    return abs(ab[0] - xy[0]) - abs(ab[1] - xy[1])

def ride_start_pos(ride):
    return (ride[0], ride[1])

def ride_end_pos(ride):
    return (ride[2], ride[3])

def ride_step_range(ride):
    return (ride[4], ride[5])