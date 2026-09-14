import os,yaml
from dataclasses import dataclass
@dataclass
class CameraConfig:
    camera_id:str;store_id:str;zone_id:str;role:str;source:str|int;target_fps:float;roi:list[list[float]];raw:dict
    @classmethod
    def load(cls,path:str):
        with open(path,encoding='utf-8') as f:data=yaml.safe_load(f)
        source=os.path.expandvars(str(data['source']));source=int(source) if source.isdigit() else source
        return cls(data['camera_id'],data['store_id'],data['zone_id'],data['role'],source,data.get('frame_sampling',{}).get('target_fps',5),data.get('roi',[]),data)
