from datetime import datetime,timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.domain import ActionTask,Activity
TRANSITIONS={'recommended':{'assigned','dismissed'},'assigned':{'accepted','cancelled'},'accepted':{'in_progress','cancelled'},'in_progress':{'completed','cancelled'},'completed':set(),'dismissed':set(),'cancelled':set()}
def transition(db:Session,task:ActionTask,target:str,note:str|None=None)->ActionTask:
    if target not in TRANSITIONS.get(task.status,set()): raise HTTPException(409,detail=f'Invalid action transition: {task.status} → {target}')
    stamp=datetime.now(timezone.utc);task.status=target
    if target=='accepted':task.accepted_at=stamp
    if target=='in_progress':task.started_at=stamp
    if target=='completed':task.completed_at=stamp;task.resolution_note=note
    db.add(Activity(store_id=task.store_id,event=f'action.{target}',message=f'{task.id}: {task.title} {target}'))
    db.commit();db.refresh(task);return task
