from niriksh_edge.models import Detection
from niriksh_edge.spatial.geometry import roi_bounds
def crop_roi(frame,polygon):
    x1,y1,x2,y2=roi_bounds(polygon);return frame[y1:y2,x1:x2],(x1,y1)
def remap_detections(detections:list[Detection],offset:tuple[int,int]):return [Detection(d.class_id,d.class_name,d.confidence,d.x1+offset[0],d.y1+offset[1],d.x2+offset[0],d.y2+offset[1]) for d in detections]
