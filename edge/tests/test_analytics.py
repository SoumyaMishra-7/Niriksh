from niriksh_edge.models import Detection,Track
from niriksh_edge.trackers import ByteTrackAdapter
from niriksh_edge.shopper import FootfallCounter,ZoneAnalytics
from niriksh_edge.queue import QueueAnalyzer
def t(i,x,y):return Track(i,(x-1,y-2,x+1,y),.9,last_seen=0)
def test_ephemeral_tracker_timeout():
 tr=ByteTrackAdapter(track_buffer=1);ids=tr.update([Detection(0,'person',.9,0,0,10,10)],timestamp=1);assert len(ids)==1;tr.update([],timestamp=3);assert not tr.tracks
def test_footfall_no_duplicates():
 c=FootfallCounter((0,5),(10,5));c.update([t(1,5,4)]);c.update([t(1,5,6)]);c.update([t(1,5,7)]);assert c.entries==1
def test_zone_dwell_aggregation():
 z=ZoneAnalytics({'a':[(0,0),(10,0),(10,10),(0,10)]},hysteresis_seconds=.1);z.update([t(1,5,5)],0);z.update([],4);assert z.dwell['a']==[4]
def test_queue_count_and_wait():
 q=QueueAnalyzer([(0,0),(10,0),(10,10),(0,10)]);assert q.update([t(1,5,5),t(2,6,5)],0)['current_length']==2;result=q.update([],10);assert result['average_wait_seconds']==10
