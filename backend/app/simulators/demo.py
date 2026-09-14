import asyncio
from datetime import datetime,timezone
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.intelligence import predict_queue,predict_shelf
from app.models.domain import Shelf,Queue,Camera,Zone,Alert,Prediction,Recommendation,Activity,EdgeState
from app.websocket.manager import manager
STORE='store-hyd'
class DemoSimulator:
    def __init__(self):self.task:asyncio.Task|None=None;self.tick=0
    async def start(self):
        if self.task and not self.task.done():return False
        self.task=asyncio.create_task(self._run());return True
    async def stop(self):
        if self.task:self.task.cancel();self.task=None
    async def _run(self):
        while True:
            await self.step();await asyncio.sleep(3)
    async def step(self):
        self.tick+=1;db=SessionLocal()
        try:
            shelf=db.get(Shelf,'shelf-a3');queue=db.get(Queue,'queue-2');zone=db.get(Zone,'zone-gro');edge=db.get(EdgeState,STORE)
            shelf.availability_percent=max(0,shelf.availability_percent-5);shelf.depletion_rate=.7;shelf.updated_at=datetime.now(timezone.utc)
            queue.current_length=min(12,queue.current_length+1);queue.arrival_rate=2.1;queue.service_rate=1.4
            qr=predict_queue(queue.current_length,queue.arrival_rate,queue.service_rate);queue.predicted_length=qr.prediction_value or 0;queue.congestion_risk='critical' if qr.should_alert else 'normal'
            zone.occupancy+=1
            if self.tick==4:
                cam=db.get(Camera,'CAM-03');cam.status='obstructed';cam.visibility_score=61;cam.analytics_confidence=.68
                self._alert(db,'ALT-CAM-3','camera','CAM-03','high','Inspect Camera 3','Analytics confidence dropped due to partial obstruction.')
            sr=predict_shelf(shelf.availability_percent,shelf.depletion_rate)
            if sr.should_alert:self._intelligence(db,'shelf',shelf.id,f'{sr.prediction_value} min','Replenish Shelf A3','critical')
            if qr.should_alert:self._intelligence(db,'queue',queue.id,f'{qr.prediction_value} customers','Open Counter 4','critical')
            if edge and not edge.online:edge.pending_events+=3
            db.commit()
            await manager.publish(STORE,'shelf.updated',{'id':shelf.id,'availability_percent':shelf.availability_percent})
            await manager.publish(STORE,'queue.updated',{'id':queue.id,'current_length':queue.current_length,'predicted_length':queue.predicted_length})
            await manager.publish(STORE,'zone.occupancy_updated',{'id':zone.id,'occupancy':zone.occupancy})
        finally:db.close()
    def _alert(self,db:Session,id,source_type,source_id,severity,title,message):
        if not db.get(Alert,id):db.add(Alert(id=id,store_id=STORE,source_type=source_type,source_id=source_id,severity=severity,title=title,message=message,status='open'));db.add(Activity(store_id=STORE,event='alert.created',message=title))
    def _intelligence(self,db:Session,kind,source,value,title,priority):
        pid=f'PRED-{kind}';rid=f'REC-{kind}'
        if not db.get(Prediction,pid):db.add(Prediction(id=pid,type=f'{kind}_prediction',source_id=source,predicted_value=value,prediction_window=7,confidence=.92,explanation='Deterministic demo prediction'))
        if not db.get(Recommendation,rid):db.add(Recommendation(id=rid,store_id=STORE,prediction_id=pid,title=title,action=title,reason='Predicted operational threshold breach',priority=priority,expected_outcome='Reduce customer impact',status='recommended'))
simulator=DemoSimulator()
