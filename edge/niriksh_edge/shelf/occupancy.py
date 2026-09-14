from dataclasses import dataclass
from niriksh_edge.models import Detection
from niriksh_edge.spatial.geometry import bbox_intersection_area
@dataclass(frozen=True)
class ShelfObservation:
    availability_percent:float;visible_items:int;confidence:float
class GenericShelfOccupancy:
    def __init__(self,roi:tuple[float,float,float,float],min_confidence=.45,coverage_at_full=0.65):self.roi=roi;self.min_confidence=min_confidence;self.coverage_at_full=coverage_at_full
    def measure(self,detections:list[Detection])->ShelfObservation:
        valid=[d for d in detections if d.class_name!='person' and d.confidence>=self.min_confidence];roi_area=(self.roi[2]-self.roi[0])*(self.roi[3]-self.roi[1]);occupied=sum(bbox_intersection_area(d.bbox,self.roi) for d in valid);availability=min(100,occupied/max(1,roi_area*self.coverage_at_full)*100);confidence=sum(d.confidence for d in valid)/len(valid) if valid else .5;return ShelfObservation(round(availability,1),len(valid),round(confidence,2))
class SKUAwareShelfAnalyzer:
    """Extension point for retailer-trained SKU detectors/classifiers."""
    def measure(self,detections:list[Detection]):raise NotImplementedError('Configure a retailer-specific SKU model')
