import pytest
from datetime import datetime
from app.domain.pricing import PricingInput, price_for

def test_student_offpeak_low_occupancy():
    p = PricingInput("student", 200.0, 0.5, datetime(2025, 12, 1, 10, 0))
    assert price_for(p) == 170.0

def test_peak_and_surge():
    p = PricingInput("standard", 100.0, 0.81, datetime(2025, 12, 1, 19, 0))
    assert price_for(p) == 132.0

def test_invalid_membership():
    p = PricingInput("vip", 100.0, 0.3, datetime(2025, 12, 1, 12, 0))
    with pytest.raises(ValueError):
        price_for(p)
