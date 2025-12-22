from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class PricingInput:
    membership_type: str        # standard | student | premium
    base_price: float           # > 0
    occupancy_rate: float       # 0.0 - 1.0
    start_time: datetime

def is_peak_hour(dt: datetime) -> bool:
    return 18 <= dt.hour <= 21

def price_for(p: PricingInput) -> float:
    factors = {
        "standard": 1.00,
        "student": 0.85,
        "premium": 0.90,
    }

    if p.membership_type not in factors:
        raise ValueError("invalid membership_type")

    if p.base_price <= 0:
        raise ValueError("base_price must be positive")

    if not (0.0 <= p.occupancy_rate <= 1.0):
        raise ValueError("occupancy_rate out of range")

    price = p.base_price * factors[p.membership_type]

    if is_peak_hour(p.start_time):
        price *= 1.10

    if p.occupancy_rate > 0.80:
        price *= 1.20

    return round(price, 2)
