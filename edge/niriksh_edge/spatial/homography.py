from pathlib import Path
import json
class Homography:
    def __init__(self,matrix):self.matrix=matrix
    @classmethod
    def calibrate(cls,image_points,floor_points):
        import cv2,numpy as np
        matrix,_=cv2.findHomography(np.asarray(image_points,dtype='float32'),np.asarray(floor_points,dtype='float32'));return cls(matrix)
    def transform(self,point):
        import numpy as np
        p=np.array([point[0],point[1],1.]);out=self.matrix@p;return float(out[0]/out[2]),float(out[1]/out[2])
    def save(self,path:str):Path(path).write_text(json.dumps(self.matrix.tolist()),encoding='utf-8')
