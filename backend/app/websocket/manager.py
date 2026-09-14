from collections import defaultdict
from datetime import datetime,timezone
from fastapi import WebSocket
class ConnectionManager:
    def __init__(self): self.connections:dict[str,set[WebSocket]]=defaultdict(set)
    async def connect(self,store_id:str,ws:WebSocket): await ws.accept();self.connections[store_id].add(ws)
    def disconnect(self,store_id:str,ws:WebSocket): self.connections[store_id].discard(ws)
    async def publish(self,store_id:str,event:str,payload:dict):
        message={'event':event,'timestamp':datetime.now(timezone.utc).isoformat(),'payload':payload}
        dead=[]
        for ws in self.connections[store_id]:
            try: await ws.send_json(message)
            except Exception: dead.append(ws)
        for ws in dead:self.disconnect(store_id,ws)
manager=ConnectionManager()
