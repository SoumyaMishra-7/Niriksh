from contextlib import asynccontextmanager
from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router
from app.core.config import get_settings
from app.db.session import Base,engine,SessionLocal
from app.models.domain import Store
from app.db.seed import reset_database
from app.websocket.manager import manager
@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(engine);db=SessionLocal()
    try:
        if db.query(Store).count()==0:db.close();reset_database()
    finally:
        if db.is_active:db.close()
    yield
app=FastAPI(title='Niriksh Intelligence API',version='1.0.0',description='Privacy-first edge retail intelligence. Stores aggregate operational metadata only.',lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=get_settings().cors_list,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.include_router(router)
@app.get('/health',tags=['System'])
def health():return {'status':'ok','service':'niriksh-api'}
@app.websocket('/ws/stores/{store_id}')
async def websocket(store_id:str,ws:WebSocket):
    await manager.connect(store_id,ws)
    try:
        while True:await ws.receive_text()
    except WebSocketDisconnect:manager.disconnect(store_id,ws)
