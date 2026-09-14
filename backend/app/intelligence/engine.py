from dataclasses import dataclass
from math import ceil
@dataclass(frozen=True)
class IntelligenceResult:
    should_alert:bool; prediction_value:int|None; priority:str|None; recommendation:str|None; explanation:str
def predict_shelf(availability:float,depletion_rate:float,historical_velocity:float=0)->IntelligenceResult:
    if not 0<=availability<=100: raise ValueError('availability must be between 0 and 100')
    velocity=max(depletion_rate,historical_velocity*.6)
    minutes=ceil(availability/velocity) if velocity>0 else None
    urgent=availability<20 or (minutes is not None and minutes<=30)
    priority='critical' if availability<10 else 'high' if urgent else None
    return IntelligenceResult(urgent,minutes,priority,'Replenish shelf' if urgent else None,f'Rule estimate using {velocity:.2f}% depletion per minute')
def predict_queue(current:int,arrival_rate:float,service_rate:float,window:int=7)->IntelligenceResult:
    if current<0: raise ValueError('queue length cannot be negative')
    predicted=max(0,round(current+(arrival_rate-service_rate)*window))
    urgent=predicted>=10
    priority='critical' if predicted>=12 else 'high' if urgent else None
    return IntelligenceResult(urgent,predicted,priority,'Open Counter 4' if urgent else None,'Deterministic flow balance: current + (arrivals - service) × window')
