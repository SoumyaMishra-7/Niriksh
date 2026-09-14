from dataclasses import dataclass
from datetime import datetime,timezone
from typing import Any
from uuid import uuid4
@dataclass(frozen=True)
class Detection:
    class_id:int;class_name:str;confidence:float;x1:float;y1:float;x2:float;y2:float
    @property
    def bbox(self):return self.x1,self.y1,self.x2,self.y2
    @property
    def centroid(self):return ((self.x1+self.x2)/2,(self.y1+self.y2)/2)
    @property
    def foot_point(self):return ((self.x1+self.x2)/2,self.y2)
    @property
    def area(self):return max(0,self.x2-self.x1)*max(0,self.y2-self.y1)
    def normalized(self,width:int,height:int):return Detection(self.class_id,self.class_name,self.confidence,self.x1/width,self.y1/height,self.x2/width,self.y2/height)
    def pixels(self,width:int,height:int):return Detection(self.class_id,self.class_name,self.confidence,self.x1*width,self.y1*height,self.x2*width,self.y2*height)
@dataclass
class Track:
    track_id:int;bbox:tuple[float,float,float,float];confidence:float;age:int=1;last_seen:float=0
    @property
    def centroid(self):x1,y1,x2,y2=self.bbox;return ((x1+x2)/2,(y1+y2)/2)
    @property
    def foot_point(self):x1,_,x2,y2=self.bbox;return ((x1+x2)/2,y2)
@dataclass(frozen=True)
class ObservationEvent:
    event_type:str;camera_id:str;store_id:str;payload:dict[str,Any];event_id:str='';timestamp:str=''
    def __post_init__(self):
        if not self.event_id:object.__setattr__(self,'event_id',str(uuid4()))
        if not self.timestamp:object.__setattr__(self,'timestamp',datetime.now(timezone.utc).isoformat())
    def as_dict(self):return {'event_id':self.event_id,'event_type':self.event_type,'camera_id':self.camera_id,'timestamp':self.timestamp,'payload':self.payload}
