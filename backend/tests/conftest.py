import os,sys
from pathlib import Path
os.environ['NIRIKSH_DATABASE_URL']='sqlite:///./test_niriksh.db'
sys.path.insert(0,str(Path(__file__).parents[1]))
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.seed import reset_database
@pytest.fixture(autouse=True)
def seed():reset_database()
@pytest.fixture
def client():
    with TestClient(app) as c:yield c
