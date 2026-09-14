import argparse
from pathlib import Path
def main():
 import cv2
 p=argparse.ArgumentParser();p.add_argument('video');p.add_argument('output');p.add_argument('--every',type=int,default=30);a=p.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True);cap=cv2.VideoCapture(a.video);i=saved=0
 while True:
  ok,frame=cap.read()
  if not ok:break
  if i%a.every==0:cv2.imwrite(str(out/f'frame_{saved:06}.jpg'),frame);saved+=1
  i+=1
 cap.release();print(f'Extracted {saved} frames')
if __name__=='__main__':main()
