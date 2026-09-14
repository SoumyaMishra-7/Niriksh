from pathlib import Path
from typing import Any
from niriksh_edge.detectors.base import Detector
from niriksh_edge.models import Detection
class YoloDetector(Detector):
    """Optional Ultralytics adapter. The domain pipeline depends only on Detector."""
    def __init__(self,model_path:str,confidence:float=.45,classes:list[int]|None=None):
        try:from ultralytics import YOLO
        except ImportError as exc:raise RuntimeError('Install optional ultralytics dependency to use YoloDetector') from exc
        if not Path(model_path).exists() and not model_path.endswith('.pt'):raise FileNotFoundError(model_path)
        self.model=YOLO(model_path);self.confidence=confidence;self.classes=classes
    def predict(self,frame:Any)->list[Detection]:
        result=self.model.predict(frame,conf=self.confidence,classes=self.classes,verbose=False)[0];names=result.names;out=[]
        for box in result.boxes:
            x1,y1,x2,y2=box.xyxy[0].tolist();cid=int(box.cls[0]);out.append(Detection(cid,names[cid],float(box.conf[0]),x1,y1,x2,y2))
        return out
