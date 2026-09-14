import pytest
from app.intelligence import predict_shelf,predict_queue
def test_shelf_prediction():
    r=predict_shelf(17,.7);assert r.should_alert and r.prediction_value==25
def test_no_spam():assert not predict_shelf(30,.05).should_alert
def test_queue_prediction():
    r=predict_queue(6,2.1,1.4,7);assert r.prediction_value==11 and r.should_alert
def test_invalid():
    with pytest.raises(ValueError):predict_shelf(101,1)
    with pytest.raises(ValueError):predict_queue(-1,1,1)
