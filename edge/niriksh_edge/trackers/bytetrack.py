import time
from niriksh_edge.models import Detection,Track
from niriksh_edge.trackers.base import Tracker
def iou(a,b):
    x1=max(a[0],b[0]);y1=max(a[1],b[1]);x2=min(a[2],b[2]);y2=min(a[3],b[3]);inter=max(0,x2-x1)*max(0,y2-y1);union=(a[2]-a[0])*(a[3]-a[1])+(b[2]-b[0])*(b[3]-b[1])-inter;return inter/union if union else 0
class ByteTrackAdapter(Tracker):
    """Dependency-free IoU association fallback with ByteTrack-compatible output.

    Production deployments can inject Supervision/ByteTrack without changing domain modules.
    IDs are in-memory only and expire after track_buffer seconds.
    """
    def __init__(self,match_threshold=.3,track_buffer=2.):self.match_threshold=match_threshold;self.track_buffer=track_buffer;self.tracks={};self.next_id=1
    def update(self,detections:list[Detection],frame=None,timestamp=None):
        now=timestamp or time.monotonic();people=[d for d in detections if d.class_name=='person'];used=set()
        for d in people:
            candidates=[(iou(d.bbox,t.bbox),tid) for tid,t in self.tracks.items() if tid not in used];score,tid=max(candidates,default=(0,None))
            if tid is None or score<self.match_threshold:tid=self.next_id;self.next_id+=1;self.tracks[tid]=Track(tid,d.bbox,d.confidence,last_seen=now)
            else:
                t=self.tracks[tid];t.bbox=d.bbox;t.confidence=d.confidence;t.age+=1;t.last_seen=now
            used.add(tid)
        for tid in list(self.tracks):
            if now-self.tracks[tid].last_seen>self.track_buffer:del self.tracks[tid]
        return [self.tracks[x] for x in used]
    def reset(self):self.tracks.clear();self.next_id=1
