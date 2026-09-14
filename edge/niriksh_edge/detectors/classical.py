from typing import Any
from niriksh_edge.detectors.base import Detector
from niriksh_edge.models import Detection
class ContourProductDetector(Detector):
    """Training-free generic occupied-region detector for fixed shelf views.

    It detects visually bounded product-like regions, not SKUs. Tune minimum area and
    aspect ratio per camera; use a trained detector when accuracy requirements demand it.
    """
    def __init__(self,min_area=400,max_area_ratio=.35):self.min_area=min_area;self.max_area_ratio=max_area_ratio
    def predict(self,frame:Any)->list[Detection]:
        import cv2
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY);gray=cv2.GaussianBlur(gray,(5,5),0);edges=cv2.Canny(gray,40,120);edges=cv2.morphologyEx(edges,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_RECT,(7,7)))
        contours,_=cv2.findContours(edges,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);height,width=gray.shape;out=[]
        for contour in contours:
            x,y,w,h=cv2.boundingRect(contour);area=w*h;ratio=w/max(1,h)
            if self.min_area<=area<=width*height*self.max_area_ratio and .15<=ratio<=4:
                confidence=min(.9,.5+area/(width*height));out.append(Detection(0,'product_region',confidence,x,y,x+w,y+h))
        return out
