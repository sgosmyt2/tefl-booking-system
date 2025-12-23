from app.main import overlaps

def test_no_overlap():
    a = {"start": "2025-12-23T15:00:00Z", "end": "2025-12-23T16:00:00Z"}
    b = {"start": "2025-12-23T16:00:00Z", "end": "2025-12-23T17:00:00Z"}
    assert overlaps(a, b) is False

def test_partial_overlap():
    a = {"start": "2025-12-23T15:00:00Z", "end": "2025-12-23T16:00:00Z"}
    b = {"start": "2025-12-23T15:30:00Z", "end": "2025-12-23T16:30:00Z"}
    assert overlaps(a, b) is True

def test_inside_overlap():
    a = {"start": "2025-12-23T15:00:00Z", "end": "2025-12-23T17:00:00Z"}
    b = {"start": "2025-12-23T15:30:00Z", "end": "2025-12-23T16:00:00Z"}
    assert overlaps(a, b) is True