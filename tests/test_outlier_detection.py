from app.analysis.outlier_detection import iso_duration_to_seconds

def test_duration_parser():
    assert iso_duration_to_seconds("PT1H2M3S") == 3723
    assert iso_duration_to_seconds("PT45S") == 45
    assert iso_duration_to_seconds("PT10M") == 600
