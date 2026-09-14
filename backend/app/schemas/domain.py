from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field
class ORM(BaseModel): model_config=ConfigDict(from_attributes=True)
class StoreOut(ORM): id:str;name:str;location:str;status:str;created_at:datetime
class ZoneOut(ORM): id:str;store_id:str;name:str;type:str;status:str;occupancy:int;average_dwell_seconds:int
class ShelfOut(ORM): id:str;store_id:str;zone_id:str;shelf_code:str;product_name:str;sku:str;availability_percent:float;status:str;depletion_rate:float;predicted_oos_minutes:int|None;confidence:float;updated_at:datetime
class QueueOut(ORM): id:str;store_id:str;counter_name:str;status:str;current_length:int;estimated_wait_minutes:float;arrival_rate:float;service_rate:float;predicted_length:int;prediction_window_minutes:int;congestion_risk:str;updated_at:datetime
class AlertOut(ORM): id:str;store_id:str;source_type:str;source_id:str;severity:str;title:str;message:str;status:str;created_at:datetime;acknowledged_at:datetime|None
class RecommendationOut(ORM): id:str;store_id:str;prediction_id:str|None;title:str;action:str;reason:str;priority:str;expected_outcome:str;status:str
class ActionOut(ORM): id:str;recommendation_id:str|None;store_id:str;assigned_to:str|None;title:str;description:str;type:str;priority:str;location:str;status:str;created_at:datetime;accepted_at:datetime|None;started_at:datetime|None;completed_at:datetime|None;resolution_note:str|None
class Assignment(BaseModel): assigned_to:str=Field(min_length=2,max_length=80)
class Completion(BaseModel): resolution_note:str=Field(min_length=2,max_length=500)
class Connectivity(BaseModel): online:bool
class EdgeEvent(BaseModel): event_id:str=Field(min_length=8,max_length=80);event_type:Literal['shelf.observation','queue.observation','zone.occupancy','camera.health','footfall.observation'];camera_id:str|None=None;timestamp:datetime;payload:dict[str,Any]
class ShelfObservation(BaseModel): shelf_id:str;availability_percent:float=Field(ge=0,le=100);confidence:float=Field(ge=0,le=1)
class QueueObservation(BaseModel): queue_id:str;current_length:int=Field(ge=0);arrival_rate:float=Field(ge=0);service_rate:float=Field(ge=0)
