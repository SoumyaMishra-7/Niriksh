from dataclasses import dataclass
@dataclass
class CameraHealth:
    low_light_threshold:float=35;blur_threshold:float=40;frozen_threshold:float=.5
    def assess(self,current,previous=None):
        import cv2,numpy as np
        if current is None:return {'status':'offline','confidence':1.0}
        gray=cv2.cvtColor(current,cv2.COLOR_BGR2GRAY) if current.ndim==3 else current;brightness=float(gray.mean());blur=float(cv2.Laplacian(gray,cv2.CV_64F).var())
        if previous is not None:
            old=cv2.cvtColor(previous,cv2.COLOR_BGR2GRAY) if previous.ndim==3 else previous
            if old.shape==gray.shape and float(np.mean(cv2.absdiff(gray,old)))<self.frozen_threshold:return {'status':'frozen','confidence':.9}
        if brightness<self.low_light_threshold:return {'status':'low_light','confidence':round(min(1,(self.low_light_threshold-brightness)/self.low_light_threshold+.5),2)}
        if blur<self.blur_threshold:return {'status':'obstructed','confidence':round(min(1,(self.blur_threshold-blur)/self.blur_threshold+.5),2)}
        return {'status':'online','confidence':.95}
