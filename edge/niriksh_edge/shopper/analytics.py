from collections import defaultdict
from dataclasses import dataclass,field
from niriksh_edge.models import Track
from niriksh_edge.spatial.geometry import crossed_line,point_in_polygon
@dataclass
class FootfallCounter:
    line_a:tuple[float,float];line_b:tuple[float,float];positions:dict[int,tuple[float,float]]=field(default_factory=dict);counted:set[tuple[int,int]]=field(default_factory=set);entries:int=0;exits:int=0
    def update(self,tracks:list[Track]):
        for t in tracks:
            p=t.foot_point;previous=self.positions.get(t.track_id)
            if previous:
                direction=crossed_line(previous,p,self.line_a,self.line_b)
                if direction and (t.track_id,direction) not in self.counted:
                    self.counted.add((t.track_id,direction));self.entries+=direction>0;self.exits+=direction<0
            self.positions[t.track_id]=p
        return self.entries,self.exits
@dataclass
class ZoneAnalytics:
    zones:dict[str,list[tuple[float,float]]];hysteresis_seconds:float=.5;active:dict[int,tuple[str,float]]=field(default_factory=dict);dwell:dict[str,list[float]]=field(default_factory=lambda:defaultdict(list))
    def update(self,tracks:list[Track],timestamp:float):
        visible=set()
        for t in tracks:
            visible.add(t.track_id);zone=next((name for name,poly in self.zones.items() if point_in_polygon(t.foot_point,poly)),None);old=self.active.get(t.track_id)
            if zone and (not old or old[0]!=zone):
                if old and timestamp-old[1]>=self.hysteresis_seconds:self.dwell[old[0]].append(timestamp-old[1])
                self.active[t.track_id]=(zone,timestamp)
        for tid in list(self.active):
            if tid not in visible:
                zone,start=self.active.pop(tid);duration=timestamp-start
                if duration>=self.hysteresis_seconds:self.dwell[zone].append(duration)
        return {z:{'occupancy':sum(v[0]==z for v in self.active.values()),'average_dwell_seconds':round(sum(self.dwell[z])/len(self.dwell[z]),1) if self.dwell[z] else 0} for z in self.zones}
class Heatmap:
    def __init__(self,width=8,height=6,decay=.95):self.width=width;self.height=height;self.decay=decay;self.grid=[[0.]*width for _ in range(height)]
    def update(self,points,frame_width,frame_height):
        self.grid=[[v*self.decay for v in row] for row in self.grid]
        for x,y in points:
            col=min(self.width-1,max(0,int(x/frame_width*self.width)));row=min(self.height-1,max(0,int(y/frame_height*self.height)));self.grid[row][col]+=1
        return [[round(v,2) for v in row] for row in self.grid]
