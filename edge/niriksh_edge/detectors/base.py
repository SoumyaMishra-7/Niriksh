from abc import ABC,abstractmethod
from typing import Any
from niriksh_edge.models import Detection
class Detector(ABC):
    @abstractmethod
    def predict(self,frame:Any)->list[Detection]:...
class NullDetector(Detector):
    """Hardware-safe detector for pipeline/configuration testing."""
    def predict(self,frame:Any)->list[Detection]:return []
