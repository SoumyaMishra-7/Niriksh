def test_overview(client):assert client.get('/api/v1/stores/store-hyd/overview').status_code==200
def test_ack(client):assert client.post('/api/v1/alerts/ALT-201/acknowledge').json()['status']=='acknowledged'
def test_transition(client):assert client.post('/api/v1/actions/ACT-1039/start').status_code==409
def test_invalid_observation(client):
    body={'event_id':'test-event-1','event_type':'shelf.observation','timestamp':'2026-01-01T00:00:00Z','payload':{'shelf_id':'shelf-a3','availability_percent':120,'confidence':.9}}
    assert client.post('/api/v1/edge/events',json=body).status_code==422
def test_offline_and_reset(client):
    r=client.post('/api/v1/demo/connectivity',json={'online':False}).json();assert r['metadata_sync_status']=='paused' and r['analytics_running'];assert client.post('/api/v1/demo/reset').json()['reset']
def test_duplicate_edge_event_is_idempotent(client):
    body={'event_id':'duplicate-event','event_type':'shelf.observation','timestamp':'2026-01-01T00:00:00Z','payload':{'shelf_id':'shelf-a3','availability_percent':18,'confidence':.9}}
    assert client.post('/api/v1/edge/events',json=body).json()['duplicate'] is False
    assert client.post('/api/v1/edge/events',json=body).json()['duplicate'] is True
