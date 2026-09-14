import numpy as np
from niriksh_edge.events.buffer import EventBuffer
from niriksh_edge.models import ObservationEvent
from niriksh_edge.privacy import CameraHealth
def test_event_serialization_and_dedup(tmp_path):
 e=ObservationEvent('shelf.observation','CAM-02','store-hyd',{'availability_percent':18});b=EventBuffer(tmp_path/'e.db');b.add(e);b.add(e);assert b.count()==1;assert b.pending()[0][1]['event_id']==e.event_id
def test_camera_health_heuristics():
 h=CameraHealth();dark=np.zeros((20,20),dtype=np.uint8);assert h.assess(dark)['status']=='low_light';assert h.assess(dark,dark)['status']=='frozen';assert h.assess(None)['status']=='offline'
def test_no_raw_frame_fields():
 event=ObservationEvent('footfall.observation','CAM-01','store-hyd',{'entries':2});assert 'frame' not in str(event.as_dict()) and 'track_id' not in str(event.as_dict())
