"""Deterministic tools package for ResolveFlow AI."""
from .oms_tool import lookup_order, lookup_carrier_tracking, lookup_customer
from .policy_engine import evaluate_return_policy
from .fraud_detector import assess_fraud_risk
from .resolution_actions import (
    calculate_financial_remedy,
    generate_logistics_action,
    generate_erp_webhook_payload
)

__all__ = [
    "lookup_order",
    "lookup_carrier_tracking",
    "lookup_customer",
    "evaluate_return_policy",
    "assess_fraud_risk",
    "calculate_financial_remedy",
    "generate_logistics_action",
    "generate_erp_webhook_payload"
]
