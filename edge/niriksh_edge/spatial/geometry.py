from typing import Iterable
Point=tuple[float,float]
def point_in_polygon(point:Point,polygon:list[Point])->bool:
    x,y=point;inside=False;j=len(polygon)-1
    for i,(xi,yi) in enumerate(polygon):
        xj,yj=polygon[j]
        if ((yi>y)!=(yj>y)) and x<(xj-xi)*(y-yi)/(yj-yi)+xi:inside=not inside
        j=i
    return inside
def side(point:Point,a:Point,b:Point)->float:return (b[0]-a[0])*(point[1]-a[1])-(b[1]-a[1])*(point[0]-a[0])
def crossed_line(previous:Point,current:Point,a:Point,b:Point)->int:
    before,after=side(previous,a,b),side(current,a,b)
    if before==0 or after==0 or before*after>=0:return 0
    return 1 if before<after else -1
def bbox_intersection_area(box:tuple[float,float,float,float],rect:tuple[float,float,float,float])->float:
    x1=max(box[0],rect[0]);y1=max(box[1],rect[1]);x2=min(box[2],rect[2]);y2=min(box[3],rect[3]);return max(0,x2-x1)*max(0,y2-y1)
def roi_bounds(points:Iterable[Point])->tuple[int,int,int,int]:
    pts=list(points);return int(min(x for x,_ in pts)),int(min(y for _,y in pts)),int(max(x for x,_ in pts)),int(max(y for _,y in pts))
