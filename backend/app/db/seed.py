from datetime import datetime,timezone,timedelta
from app.db.session import Base,engine,SessionLocal
from app.models.domain import Store,Zone,Camera,Shelf,Queue,ShopperMetric,Alert,Prediction,Recommendation,ActionTask,Activity,EdgeState
STORE='store-hyd'
def reset_database():
    Base.metadata.drop_all(engine);Base.metadata.create_all(engine);db=SessionLocal()
    try:
        db.add(Store(id=STORE,name='Niriksh Demo Store',location='Hyderabad',status='online'))
        zones=[('zone-ent','Entrance','entrance'),('zone-gro','Grocery','retail'),('zone-pc','Personal Care','retail'),('zone-elec','Electronics','retail'),('zone-check','Checkout','checkout')]
        for i,(zid,name,ztype) in enumerate(zones):db.add(Zone(id=zid,store_id=STORE,name=name,type=ztype,status='normal',occupancy=[8,19,6,12,11][i],average_dwell_seconds=[42,306,192,258,252][i]))
        for i in range(1,7):
            zid=zones[min(i-1,4)][0];db.add(Camera(id=f'CAM-{i:02}',store_id=STORE,zone_id=zid,name=f'{zones[min(i-1,4)][1]} Camera {i}',status='online',stream_health='good',visibility_score=96-i,analytics_confidence=.96-i/100))
        products=['Coca-Cola 750ml','Amul Taaza Milk','Aashirvaad Atta','Dove Shampoo','Colgate MaxFresh','AA Batteries 4pk','Lay’s Classic','Tata Salt','Surf Excel','Maggi Noodles','Red Bull','Dettol Handwash','Nivea Lotion','USB-C Cable','LED Bulb','Britannia Bread','Fortune Oil','Cadbury Dairy Milk']
        for i,p in enumerate(products):
            code=f'{chr(65+i//3)}{i%3+1}';avail=42 if code=='A3' else [78,64,55,88,36,71][i%6];db.add(Shelf(id=f'shelf-{code.lower()}',store_id=STORE,zone_id='zone-gro' if i<10 else 'zone-pc' if i<14 else 'zone-elec',shelf_code=code,product_name=p,sku=f'SKU-{1000+i}',availability_percent=avail,status='normal' if avail>35 else 'attention',depletion_rate=.25+(i%4)*.15,confidence=.88+(i%8)/100))
        for i in range(1,5):db.add(Queue(id=f'queue-{i}',store_id=STORE,counter_name=f'Counter {i}',status='open' if i<4 else 'closed',current_length=[3,3,4,0][i-1],estimated_wait_minutes=[1.8,2.1,2.6,0][i-1],arrival_rate=[1.0,1.4,1.1,0][i-1],service_rate=[1.2,1.2,1.2,0][i-1],predicted_length=[2,4,3,0][i-1],prediction_window_minutes=7,congestion_risk='normal'))
        for h in range(8):
            for zid,_,_ in zones: db.add(ShopperMetric(store_id=STORE,zone_id=zid,timestamp_window=datetime.now(timezone.utc)-timedelta(hours=7-h),footfall=30+h*11,entries=18+h*5,exits=16+h*5,occupancy=8+h,average_dwell_seconds=180+h*8,peak_occupancy=15+h))
        db.add(Alert(id='ALT-201',store_id=STORE,source_type='shelf',source_id='shelf-b1',severity='warning',title='Shelf B1 trending low',message='Availability is declining faster than baseline.',status='open'))
        db.add_all([
            ActionTask(id='ACT-1042',store_id=STORE,recommendation_id=None,title='Replenish Shelf A3',description='Bring Coca-Cola stock from the backroom and replenish the shelf.',type='replenishment',priority='critical',location='Grocery · Aisle 2 · Shelf A3',status='assigned',assigned_to='Rahul'),
            ActionTask(id='ACT-1043',store_id=STORE,recommendation_id=None,title='Open Counter 4',description='Open Counter 4 to reduce expected waiting time.',type='queue',priority='high',location='Checkout',status='assigned',assigned_to='Rahul'),
            ActionTask(id='ACT-1044',store_id=STORE,recommendation_id=None,title='Check Camera 3',description='Check the lens, remove any obstruction and verify the camera angle.',type='camera',priority='warning',location='Electronics',status='assigned',assigned_to='Rahul'),
            ActionTask(id='ACT-1039',store_id=STORE,title='Replenish Shelf C7',description='Historical completed action',type='replenishment',priority='normal',location='Personal Care',status='completed',assigned_to='Amit',completed_at=datetime.now(timezone.utc)-timedelta(minutes=20))])
        db.add(Activity(store_id=STORE,event='system.seeded',message='Demo store initialised'))
        db.add(EdgeState(store_id=STORE));db.commit()
    finally:db.close()
if __name__=='__main__':reset_database();print('Niriksh demo database reset and seeded.')
