import logging,time
from niriksh_edge.capture import VideoSource
from niriksh_edge.config import CameraConfig
from niriksh_edge.detectors import Detector
from niriksh_edge.events import NirikshEventClient
from niriksh_edge.models import ObservationEvent
from niriksh_edge.privacy import CameraHealth
from niriksh_edge.queue import QueueAnalyzer
from niriksh_edge.shelf import GenericShelfOccupancy
from niriksh_edge.shopper import FootfallCounter,ZoneAnalytics,Heatmap
from niriksh_edge.trackers import ByteTrackAdapter
log=logging.getLogger('niriksh.edge.pipeline')
class EdgePipeline:
    def __init__(self,config:CameraConfig,detector:Detector,client:NirikshEventClient):
        self.c=config;self.detector=detector;self.client=client;self.tracker=ByteTrackAdapter();self.health=CameraHealth();self.previous=None;self.frames=0;self.started=time.monotonic()
        roi=config.roi;bounds=(min(x for x,_ in roi),min(y for _,y in roi),max(x for x,_ in roi),max(y for _,y in roi)) if roi else (0,0,1,1);self.shelf=GenericShelfOccupancy(bounds,min_confidence=config.raw.get('shelf',{}).get('min_confidence',.45));self.queue=QueueAnalyzer([tuple(x) for x in roi]) if roi else None
        zones={k:[tuple(x) for x in v['polygon']] for k,v in config.raw.get('zones',{}).items()};line=config.raw.get('entry_line',[[0,0],[1,0]]);self.footfall=FootfallCounter(tuple(line[0]),tuple(line[1]));self.zones=ZoneAnalytics(zones);self.heat=Heatmap()
    def process(self,frame,timestamp):
        start=time.perf_counter();health=self.health.assess(frame,self.previous);self.previous=frame.copy();detections=self.detector.predict(frame);infer_ms=(time.perf_counter()-start)*1000;tracks=self.tracker.update(detections,timestamp=timestamp);events=[]
        if self.c.role=='shelf':
            x=self.shelf.measure(detections);events.append(self._event('shelf.observation',{'shelf_id':self.c.raw.get('shelf_id','shelf-a3'),'availability_percent':x.availability_percent,'visible_items':x.visible_items,'confidence':x.confidence}))
        elif self.c.role=='checkout' and self.queue:
            x=self.queue.update(tracks,timestamp);events.append(self._event('queue.observation',{'queue_id':self.c.raw.get('queue_id','queue-2'),'arrival_rate':self.c.raw.get('arrival_rate',2.1),**x,'confidence':round(sum(t.confidence for t in tracks)/len(tracks),2) if tracks else .5}))
        else:
            entries,exits=self.footfall.update(tracks);zone=self.zones.update(tracks,timestamp);events.append(self._event('footfall.observation',{'entries':entries,'exits':exits,'window_seconds':60}));events.extend(self._event('zone.occupancy',{'zone_id':z,**m,'window_seconds':300,'grid':self.heat.update([t.foot_point for t in tracks],frame.shape[1],frame.shape[0])}) for z,m in zone.items())
        if health['status']!='online':events.append(self._event('camera.health',health))
        for event in events:self.client.emit_nowait(event)
        self.frames+=1;log.info('frame_processed',extra={'camera_id':self.c.camera_id,'role':self.c.role,'inference_ms':round(infer_ms,2),'events':len(events),'pipeline_fps':round(self.frames/max(.001,time.monotonic()-self.started),2)})
        return detections,tracks,events
    def _event(self,event_type,payload):return ObservationEvent(event_type,self.c.camera_id,self.c.store_id,payload)
    def run(self,visualize=False):
        import cv2
        with VideoSource(self.c.source,self.c.target_fps) as source:
            for frame,timestamp in source.frames():
                detections,tracks,_=self.process(frame,timestamp)
                if visualize:
                    for t in tracks:
                        x1,y1,x2,y2=map(int,t.bbox);cv2.rectangle(frame,(x1,y1),(x2,y2),(69,180,110),2);cv2.putText(frame,f'local #{t.track_id}',(x1,y1-5),cv2.FONT_HERSHEY_SIMPLEX,.4,(69,180,110),1)
                    cv2.imshow(f'Niriksh local preview — {self.c.camera_id}',frame)
                    if cv2.waitKey(1)&0xFF==27:break
        if visualize:cv2.destroyAllWindows()
