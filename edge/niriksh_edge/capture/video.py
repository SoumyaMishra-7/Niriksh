import time
class VideoSource:
    def __init__(self,source,target_fps=5,adaptive=False):self.source=int(source) if str(source).isdigit() else source;self.target_fps=target_fps;self.adaptive=adaptive;self.capture=None;self.dropped=0
    def __enter__(self):
        import cv2
        self.capture=cv2.VideoCapture(self.source)
        if not self.capture.isOpened():raise RuntimeError(f'Unable to open configured source (credentials hidden)')
        return self
    def frames(self):
        import cv2
        interval=1/max(.1,self.target_fps);next_frame=time.monotonic();is_file=isinstance(self.source,str) and not self.source.lower().startswith(('rtsp://','http://','https://'));source_fps=self.capture.get(cv2.CAP_PROP_FPS) or self.target_fps;step=max(1,round(source_fps/self.target_fps));index=0
        while True:
            ok,frame=self.capture.read()
            if not ok:break
            now=time.monotonic()
            if is_file:
                if index%step:index+=1;self.dropped+=1;continue
                index+=1;yield frame,index/source_fps
            else:
                if now<next_frame:self.dropped+=1;continue
                next_frame=now+interval;yield frame,now
    def __exit__(self,*_):
        if self.capture:self.capture.release()
