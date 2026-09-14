import asyncio,logging
import httpx
from niriksh_edge.events.buffer import EventBuffer
from niriksh_edge.models import ObservationEvent
log=logging.getLogger('niriksh.edge.events')
class NirikshEventClient:
    def __init__(self,base_url='http://localhost:8000',buffer_path='edge_events.db',token=None):self.url=base_url.rstrip('/')+'/api/v1/edge/events';self.buffer=EventBuffer(buffer_path);self.queue=asyncio.Queue(maxsize=1000);self.token=token;self.running=False
    def emit_nowait(self,event:ObservationEvent):
        try:self.queue.put_nowait(event)
        except asyncio.QueueFull:self.buffer.add(event);log.warning('event_buffered',extra={'event_id':event.event_id})
    async def run(self):
        self.running=True
        async with httpx.AsyncClient(timeout=5) as client:
            while self.running:
                await self.flush(client)
                try:event=await asyncio.wait_for(self.queue.get(),timeout=1)
                except asyncio.TimeoutError:continue
                if not await self._post(client,event.as_dict()):self.buffer.add(event)
    async def _post(self,client,body):
        try:
            headers={'Authorization':f'Bearer {self.token}'} if self.token else {};response=await client.post(self.url,json=body,headers=headers);return response.status_code in (200,201,202,409)
        except httpx.HTTPError:return False
    async def flush(self,client):
        for event_id,body in self.buffer.pending():
            if await self._post(client,body):self.buffer.remove(event_id)
            else:break
    def stop(self):self.running=False
