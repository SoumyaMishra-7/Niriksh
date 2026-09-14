from abc import ABC,abstractmethod
from typing import Any
from niriksh_edge.models import Detection,Track
class Tracker(ABC):
    @abstractmethod
    def update(self,detections:list[Detection],frame:Any=None,timestamp:float|None=None)->list[Track]:...
    @abstractmethod
    def reset(self)->None:...
