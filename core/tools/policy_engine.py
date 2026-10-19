"""
E-Commerce Policy Verification Engine
Deterministically validates customer requests against category return windows,
hygiene restrictions, and restocking rules.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from ..data.mock_database import POLICY_RULES, CURRENT_TIMESTAMP

def evaluate_return_policy(
    category: str,
    delivery_date_str: Optional[str],
    claimed_reason: str,
    custom_policy_matrix: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Evaluates whether a product is eligible for return, replacement, or refund
    based on institutional policy rules and delivery timestamp.
    """
    active_matrix = custom_policy_matrix if custom_policy_matrix is not None else POLICY_RULES
    rule = active_matrix.get(category, {
        "return_window_days": 14,
        "allow_refund": True,
        "allow_replacement": True,
        "free_reverse_pickup": True,
        "restocking_fee_pct": 0.0,
        "mandatory_photo_for_damage": False,
        "notes": "Standard default policy."
    })

    # If item has not been delivered yet (e.g. lost in transit)
    if not delivery_date_str:
        return {
            "eligible": False,
            "reason": "ITEM_NOT_YET_DELIVERED",
            "category": category,
            "days_since_delivery": None,
            "allowed_window_days": rule["return_window_days"],
            "allow_refund": True,  # Lost items can be refunded
            "allow_replacement": True,
            "restocking_fee_pct": 0.0,
            "free_reverse_pickup": False,
            "policy_notes": "Item is still in transit or stalled. Handled under Logistics Delay Policy."
        }

    try:
        delivery_date = datetime.strptime(delivery_date_str, "%Y-%m-%d")
        days_elapsed = (CURRENT_TIMESTAMP - delivery_date).days
    except Exception:
        days_elapsed = 0

    allowed_days = rule["return_window_days"]
    within_window = days_elapsed <= allowed_days

    # Category specific non-returnable checks (e.g. hygiene)
    if allowed_days == 0:
        return {
            "eligible": False,
            "reason": "CATEGORY_NON_RETURNABLE_HYGIENE",
            "category": category,
            "days_since_delivery": days_elapsed,
            "allowed_window_days": 0,
            "allow_refund": False,
            "allow_replacement": False,
            "restocking_fee_pct": 0.0,
            "free_reverse_pickup": False,
            "policy_notes": rule["notes"],
            "policy_violation_detail": (
                f"Products in '{category}' are strictly non-returnable due to health, "
                "sanitary and hygiene regulations once delivered."
            )
        }

    if not within_window:
        return {
            "eligible": False,
            "reason": "RETURN_WINDOW_EXPIRED",
            "category": category,
            "days_since_delivery": days_elapsed,
            "allowed_window_days": allowed_days,
            "allow_refund": False,
            "allow_replacement": False,
            "restocking_fee_pct": 0.0,
            "free_reverse_pickup": False,
            "policy_notes": rule["notes"],
            "policy_violation_detail": (
                f"Return window of {allowed_days} days expired {days_elapsed - allowed_days} days ago "
                f"({days_elapsed} days since delivery on {delivery_date_str})."
            )
        }

    # Within valid window
    is_damage_claim = any(w in claimed_reason.lower() for w in ["damage", "defect", "broken", "static", "not working", "cut out", "wrong size", "wrong item"])
    restocking_fee = 0.0 if is_damage_claim else rule.get("restocking_fee_pct", 0.0)

    return {
        "eligible": True,
        "reason": "VALID_RETURN_WINDOW",
        "category": category,
        "days_since_delivery": days_elapsed,
        "allowed_window_days": allowed_days,
        "allow_refund": rule["allow_refund"],
        "allow_replacement": rule["allow_replacement"],
        "free_reverse_pickup": rule["free_reverse_pickup"],
        "restocking_fee_pct": restocking_fee,
        "mandatory_photo_required": rule.get("mandatory_photo_for_damage", False) and is_damage_claim,
        "policy_notes": rule["notes"],
        "policy_violation_detail": None
    }
