"""Metric calculation helpers; supply ground-truth/prediction JSON from a licensed dataset."""
def mae(actual,predicted):return sum(abs(a-b) for a,b in zip(actual,predicted))/max(1,len(actual))
def count_error(actual,predicted):return mae(actual,predicted)
def privacy_audit(event_payloads):return {'raw_frames_transmitted':sum('frame' in p or 'image' in p for p in event_payloads),'persistent_shopper_identifiers':sum('track_id' in p or 'visitor_id' in p for p in event_payloads)}
