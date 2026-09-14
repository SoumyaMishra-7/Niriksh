import numpy as np,cv2
from niriksh_edge.detectors.classical import ContourProductDetector
from niriksh_edge.shelf import GenericShelfOccupancy
def test_classical_shelf_observation_is_frame_derived():
    frame=np.zeros((200,300,3),dtype=np.uint8);cv2.rectangle(frame,(30,40),(110,170),(230,230,230),-1);cv2.rectangle(frame,(150,40),(230,170),(180,180,180),-1)
    detections=ContourProductDetector(min_area=100).predict(frame);result=GenericShelfOccupancy((0,0,300,200),coverage_at_full=.5).measure(detections);assert result.visible_items>=2 and result.availability_percent>0
