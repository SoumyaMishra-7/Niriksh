from datetime import datetime,timezone
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException,Query
from sqlalchemy import func,select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.seed import STORE,reset_database
from app.models.domain import Store,Zone,Shelf,Queue,ShopperMetric,Alert,Prediction,Recommendation,ActionTask,Activity,EdgeState,Camera,EdgeEventRecord
from app.schemas.domain import StoreOut,ZoneOut,ShelfOut,QueueOut,AlertOut,RecommendationOut,ActionOut,Assignment,Completion,Connectivity,EdgeEvent,ShelfObservation,QueueObservation
from app.services.actions import transition
from app.intelligence import predict_shelf,predict_queue
from app.simulators.demo import simulator
from app.websocket.manager import manager
from pydantic import ValidationError
Db=Annotated[Session,Depends(get_db)]
router=APIRouter(prefix='/api/v1')
def one(db,model,id):
    obj=db.get(model,id)
    if not obj:raise HTTPException(404,detail=f'{model.__name__} not found')
    return obj
def store(db,id):return one(db,Store,id)
@router.get('/stores',tags=['Stores'],response_model=list[StoreOut],summary='List stores')
def stores(db:Db):return db.scalars(select(Store)).all()
@router.get('/stores/{store_id}',tags=['Stores'],response_model=StoreOut,summary='Get store')
def get_store(store_id:str,db:Db):return store(db,store_id)
@router.get('/stores/{store_id}/overview',tags=['Stores'],summary='Get live command center summary')
def overview(store_id:str,db:Db):
    store(db,store_id);low=db.scalar(select(func.count()).select_from(Shelf).where(Shelf.store_id==store_id,Shelf.availability_percent<30));critical=db.scalar(select(func.count()).select_from(Queue).where(Queue.store_id==store_id,Queue.congestion_risk=='critical'));alerts=db.scalar(select(func.count()).select_from(Alert).where(Alert.store_id==store_id,Alert.status=='open'));recs=db.scalar(select(func.count()).select_from(Recommendation).where(Recommendation.store_id==store_id,Recommendation.status=='recommended'));foot=db.scalar(select(func.max(ShopperMetric.footfall)).where(ShopperMetric.store_id==store_id)) or 0;active=db.scalar(select(func.sum(Zone.occupancy)).where(Zone.store_id==store_id)) or 0
    return {'live_footfall':foot,'active_customers':active,'low_stock_count':low,'critical_queue_count':critical,'open_alerts':alerts,'active_recommendations':recs,'system_health':'healthy'}
@router.get('/stores/{store_id}/zones',tags=['Stores'],response_model=list[ZoneOut],summary='List store zones')
def zones(store_id:str,db:Db):store(db,store_id);return db.scalars(select(Zone).where(Zone.store_id==store_id)).all()
@router.get('/zones/{zone_id}',tags=['Stores'],response_model=ZoneOut,summary='Get zone')
def zone(zone_id:str,db:Db):return one(db,Zone,zone_id)
@router.get('/stores/{store_id}/shelves',tags=['Shelves'],response_model=list[ShelfOut],summary='Search shelves')
def shelves(store_id:str,db:Db,status:str|None=None,zone:str|None=None,search:Annotated[str|None,Query(max_length=100)]=None):
    store(db,store_id);q=select(Shelf).where(Shelf.store_id==store_id)
    if status:q=q.where(Shelf.status==status)
    if zone:q=q.where(Shelf.zone_id==zone)
    if search:q=q.where((Shelf.product_name.ilike(f'%{search}%'))|(Shelf.shelf_code.ilike(f'%{search}%')))
    return db.scalars(q).all()
@router.get('/shelves/{shelf_id}',tags=['Shelves'],response_model=ShelfOut,summary='Get shelf detail')
def shelf(shelf_id:str,db:Db):return one(db,Shelf,shelf_id)
@router.get('/stores/{store_id}/queues',tags=['Queues'],response_model=list[QueueOut],summary='List checkout queues')
def queues(store_id:str,db:Db):store(db,store_id);return db.scalars(select(Queue).where(Queue.store_id==store_id)).all()
@router.get('/queues/{queue_id}',tags=['Queues'],response_model=QueueOut,summary='Get queue')
def queue(queue_id:str,db:Db):return one(db,Queue,queue_id)
@router.get('/stores/{store_id}/shopper-analytics',tags=['Analytics'],summary='Get anonymous aggregate shopper analytics')
def analytics(store_id:str,db:Db,start:datetime|None=None,end:datetime|None=None,zone:str|None=None):
    store(db,store_id);q=select(ShopperMetric).where(ShopperMetric.store_id==store_id)
    if start:q=q.where(ShopperMetric.timestamp_window>=start)
    if end:q=q.where(ShopperMetric.timestamp_window<=end)
    if zone:q=q.where(ShopperMetric.zone_id==zone)
    rows=db.scalars(q).all();return {'privacy':'anonymous_aggregate_only','windows':[{'timestamp':x.timestamp_window,'zone_id':x.zone_id,'footfall':x.footfall,'entries':x.entries,'exits':x.exits,'occupancy':x.occupancy,'average_dwell_seconds':x.average_dwell_seconds,'peak_occupancy':x.peak_occupancy} for x in rows]}
@router.get('/stores/{store_id}/alerts',tags=['Alerts'],response_model=list[AlertOut],summary='List alerts')
def get_alerts(store_id:str,db:Db):store(db,store_id);return db.scalars(select(Alert).where(Alert.store_id==store_id).order_by(Alert.created_at.desc())).all()
@router.post('/alerts/{id}/acknowledge',tags=['Alerts'],response_model=AlertOut,summary='Acknowledge alert')
async def acknowledge(id:str,db:Db):
    a=one(db,Alert,id);a.status='acknowledged';a.acknowledged_at=datetime.now(timezone.utc);db.commit();db.refresh(a);await manager.publish(a.store_id,'alert.updated',{'id':a.id,'status':a.status});return a
@router.post('/alerts/{id}/dismiss',tags=['Alerts'],response_model=AlertOut,summary='Dismiss alert')
async def dismiss_alert(id:str,db:Db):a=one(db,Alert,id);a.status='dismissed';db.commit();db.refresh(a);await manager.publish(a.store_id,'alert.updated',{'id':a.id,'status':a.status});return a
@router.get('/stores/{store_id}/recommendations',tags=['Recommendations'],response_model=list[RecommendationOut],summary='List recommendations')
def recommendations(store_id:str,db:Db):store(db,store_id);return db.scalars(select(Recommendation).where(Recommendation.store_id==store_id)).all()
@router.post('/recommendations/{id}/assign',tags=['Recommendations'],response_model=ActionOut,summary='Assign recommendation')
async def assign_rec(id:str,body:Assignment,db:Db):
    r=one(db,Recommendation,id);r.status='assigned';task=ActionTask(id=f'ACT-{1000+db.query(ActionTask).count()+1}',recommendation_id=r.id,store_id=r.store_id,assigned_to=body.assigned_to,title=r.title,description=r.reason,type='recommended_action',priority=r.priority,location='Store floor',status='assigned');db.add(task);db.add(Activity(store_id=r.store_id,event='action.assigned',message=f'{task.id} assigned to {body.assigned_to}'));db.commit();db.refresh(task);await manager.publish(r.store_id,'action.assigned',ActionOut.model_validate(task).model_dump(mode='json'));return task
@router.post('/recommendations/{id}/dismiss',tags=['Recommendations'],response_model=RecommendationOut,summary='Dismiss recommendation')
def dismiss_rec(id:str,db:Db):r=one(db,Recommendation,id);r.status='dismissed';db.commit();db.refresh(r);return r
@router.get('/stores/{store_id}/actions',tags=['Actions'],response_model=list[ActionOut],summary='List shared manager/staff tasks')
def actions(store_id:str,db:Db):store(db,store_id);return db.scalars(select(ActionTask).where(ActionTask.store_id==store_id).order_by(ActionTask.created_at.desc())).all()
@router.get('/actions/{id}',tags=['Actions'],response_model=ActionOut,summary='Get action')
def action(id:str,db:Db):return one(db,ActionTask,id)
async def move(id,target,db,note=None):
    t=transition(db,one(db,ActionTask,id),target,note);await manager.publish(t.store_id,f'action.{target}',ActionOut.model_validate(t).model_dump(mode='json'));return t
@router.post('/actions/{id}/accept',tags=['Actions'],response_model=ActionOut,summary='Accept task')
async def accept(id:str,db:Db):return await move(id,'accepted',db)
@router.post('/actions/{id}/start',tags=['Actions'],response_model=ActionOut,summary='Start task')
async def start(id:str,db:Db):return await move(id,'in_progress',db)
@router.post('/actions/{id}/complete',tags=['Actions'],response_model=ActionOut,summary='Complete task')
async def complete(id:str,body:Completion,db:Db):return await move(id,'completed',db,body.resolution_note)
@router.post('/actions/{id}/reassign',tags=['Actions'],response_model=ActionOut,summary='Reassign task')
async def reassign(id:str,body:Assignment,db:Db):t=one(db,ActionTask,id);t.assigned_to=body.assigned_to;db.commit();db.refresh(t);await manager.publish(t.store_id,'action.assigned',ActionOut.model_validate(t).model_dump(mode='json'));return t
@router.get('/stores/{store_id}/activity',tags=['Stores'],summary='Get operational audit history')
def activity(store_id:str,db:Db):store(db,store_id);return db.scalars(select(Activity).where(Activity.store_id==store_id).order_by(Activity.created_at.desc()).limit(100)).all()
@router.get('/stores/{store_id}/edge-health',tags=['Edge'],summary='Get edge and privacy health')
def edge(store_id:str,db:Db):
    store(db,store_id);x=one(db,EdgeState,store_id);online=db.scalar(select(func.count()).select_from(Camera).where(Camera.store_id==store_id,Camera.status=='online'));return {'edge_status':'healthy','connectivity':'online' if x.online else 'offline','analytics_running':x.analytics_running,'cameras_online':online,'metadata_sync_status':x.metadata_sync_status,'pending_events':x.pending_events,'local_storage_percent':x.storage_percent,'cpu_percent':x.cpu_percent,'npu_percent':x.npu_percent,'device_temperature_c':x.temperature_c,'last_cloud_sync':x.last_cloud_sync,'raw_video_uploaded_mb':0,'persistent_customer_identities':0,'metadata_only_sync':True}
@router.post('/edge/events',tags=['Edge'],summary='Ingest structured CV observation')
async def ingest(body:EdgeEvent,db:Db):
    if db.get(EdgeEventRecord,body.event_id):return {'accepted':True,'duplicate':True,'event_type':body.event_type}
    try:
        if body.event_type=='shelf.observation':
            o=ShelfObservation(**body.payload);s=one(db,Shelf,o.shelf_id);s.availability_percent=o.availability_percent;s.confidence=o.confidence;r=predict_shelf(s.availability_percent,s.depletion_rate);s.predicted_oos_minutes=r.prediction_value;s.status='critical' if r.should_alert else 'normal';store_id=s.store_id
            if r.should_alert and not db.get(Recommendation,f'REC-{s.id}'):
                p=Prediction(id=f'PRED-{s.id}',type='stock_out',source_id=s.id,predicted_value=f'{r.prediction_value} min',prediction_window=r.prediction_value or 0,confidence=o.confidence,explanation=r.explanation);db.add(p);db.add(Alert(id=f'ALT-{s.id}',store_id=store_id,source_type='shelf',source_id=s.id,severity=r.priority or 'high',title=f'Shelf {s.shelf_code} low stock',message=f'Stock-out predicted in {r.prediction_value} minutes',status='open'));db.add(Recommendation(id=f'REC-{s.id}',store_id=store_id,prediction_id=p.id,title=f'Replenish Shelf {s.shelf_code}',action=f'Replenish Shelf {s.shelf_code}',reason=f'Availability is {s.availability_percent:.1f}%',priority=r.priority or 'high',expected_outcome='Prevent stock-out',status='recommended'))
        elif body.event_type=='queue.observation':
            o=QueueObservation(**body.payload);q=one(db,Queue,o.queue_id);q.current_length=o.current_length;q.arrival_rate=o.arrival_rate;q.service_rate=o.service_rate;r=predict_queue(q.current_length,q.arrival_rate,q.service_rate);q.predicted_length=r.prediction_value or 0;q.congestion_risk='critical' if r.should_alert else 'normal';store_id=q.store_id
            if r.should_alert and not db.get(Recommendation,f'REC-{q.id}'):
                p=Prediction(id=f'PRED-{q.id}',type='queue_congestion',source_id=q.id,predicted_value=str(r.prediction_value),prediction_window=7,confidence=.9,explanation=r.explanation);db.add(p);db.add(Alert(id=f'ALT-{q.id}',store_id=store_id,source_type='queue',source_id=q.id,severity=r.priority or 'high',title=f'{q.counter_name} congestion predicted',message=f'Expected queue: {r.prediction_value} in 7 min',status='open'));db.add(Recommendation(id=f'REC-{q.id}',store_id=store_id,prediction_id=p.id,title='Open Counter 4',action='Open Counter 4',reason='Arrival rate exceeds service rate',priority=r.priority or 'high',expected_outcome='Reduce checkout wait',status='recommended'))
        elif body.event_type=='zone.occupancy':
            z=one(db,Zone,str(body.payload.get('zone_id')));occupancy=int(body.payload.get('occupancy',0))
            if occupancy<0:raise HTTPException(422,detail='occupancy cannot be negative')
            z.occupancy=occupancy;z.average_dwell_seconds=int(body.payload.get('average_dwell_seconds',z.average_dwell_seconds));store_id=z.store_id
        elif body.event_type=='camera.health':
            c=one(db,Camera,body.camera_id);c.status=str(body.payload.get('status','online'));c.analytics_confidence=float(body.payload.get('confidence',c.analytics_confidence));c.last_seen_at=datetime.now(timezone.utc);store_id=c.store_id
        else:
            entries=int(body.payload.get('entries',0));exits=int(body.payload.get('exits',0))
            if entries<0 or exits<0:raise HTTPException(422,detail='footfall counts cannot be negative')
            db.add(ShopperMetric(store_id=STORE,zone_id='zone-ent',footfall=entries,entries=entries,exits=exits,occupancy=max(0,entries-exits),average_dwell_seconds=0,peak_occupancy=max(0,entries-exits)));store_id=STORE
    except ValidationError as exc: raise HTTPException(422,detail=exc.errors()) from exc
    db.add(EdgeEventRecord(event_id=body.event_id,store_id=store_id,event_type=body.event_type));db.commit();await manager.publish(store_id,body.event_type,body.payload);return {'accepted':True,'duplicate':False,'event_type':body.event_type}
@router.post('/demo/start',tags=['Demo'],summary='Start deterministic live simulator')
async def demo_start():return {'started':await simulator.start()}
@router.post('/demo/stop',tags=['Demo'],summary='Stop simulator')
async def demo_stop():await simulator.stop();return {'stopped':True}
@router.post('/demo/reset',tags=['Demo'],summary='Reset all demo scenarios')
async def demo_reset():await simulator.stop();reset_database();return {'reset':True}
@router.post('/demo/connectivity',tags=['Demo'],summary='Toggle edge connectivity')
async def connectivity(body:Connectivity,db:Db):
    x=one(db,EdgeState,STORE);x.online=body.online;x.metadata_sync_status='active' if body.online else 'paused';x.last_cloud_sync=datetime.now(timezone.utc) if body.online else x.last_cloud_sync
    if body.online:x.pending_events=0
    db.commit();await manager.publish(STORE,'edge.status_changed',{'online':body.online,'metadata_sync_status':x.metadata_sync_status});return {'online':x.online,'analytics_running':x.analytics_running,'metadata_sync_status':x.metadata_sync_status,'pending_events':x.pending_events}
