from niriksh_edge.spatial.geometry import point_in_polygon,crossed_line
def test_roi_inclusion():assert point_in_polygon((5,5),[(0,0),(10,0),(10,10),(0,10)]) and not point_in_polygon((12,5),[(0,0),(10,0),(10,10),(0,10)])
def test_line_crossing_direction():assert crossed_line((5,-1),(5,1),(0,0),(10,0))==1
