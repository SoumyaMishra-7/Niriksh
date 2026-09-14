from dataclasses import dataclass,field
from niriksh_edge.models import Track
from niriksh_edge.spatial.geometry import point_in_polygon,crossed_line
@dataclass
class QueueAnalyzer:
    polygon:list[tuple[float,float]];service_line:tuple[tuple[float,float],tuple[float,float]]|None=None;entered:dict[int,float]=field(default_factory=dict);previous:dict[int,tuple[float,float]]=field(default_factory=dict);waits:list[float]=field(default_factory=list);served:int=0;started_at:float|None=None
    def update(self,tracks:list[Track],timestamp:float):
        if self.started_at is None:self.started_at=timestamp
        active=set()
        for t in tracks:
            p=t.foot_point
            if point_in_polygon(p,self.polygon):active.add(t.track_id);self.entered.setdefault(t.track_id,timestamp)
            if self.service_line and t.track_id in self.previous and crossed_line(self.previous[t.track_id],p,*self.service_line):self.served+=1
            self.previous[t.track_id]=p
        for tid in list(self.entered):
            if tid not in active:self.waits.append(timestamp-self.entered.pop(tid))
        ordered=sorted(self.waits);elapsed=max(1,timestamp-(self.started_at or timestamp));return {'current_length':len(active),'average_wait_seconds':round(sum(self.waits)/len(self.waits),1) if self.waits else 0,'p50_wait_seconds':ordered[len(ordered)//2] if ordered else 0,'p90_wait_seconds':ordered[min(len(ordered)-1,int(len(ordered)*.9))] if ordered else 0,'service_rate':round(self.served/(elapsed/60),2)}
