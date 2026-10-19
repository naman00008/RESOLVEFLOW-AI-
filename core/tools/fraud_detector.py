"""
Fraud and Policy Abuse Risk Detector
Analyzes customer claim velocity, return rates, carrier discrepancies,
and transaction value to generate an explainable fraud risk score.
"""

from typing import Dict, Any, List, Optional

def assess_fraud_risk(
    customer_data: Dict[str, Any],
    order_data: Dict[str, Any],
    carrier_tracking: Optional[Dict[str, Any]] = None,
    claim_type: str = "general"
) -> Dict[str, Any]:
    """
    Computes a composite fraud & abuse risk score (0-100) and identifies
    anomalous risk indicators.
    """
    score = 0
    risk_factors: List[str] = []
    
    total_orders = customer_data.get("total_orders", 1)
    total_returns = customer_data.get("total_returns", 0)
    return_rate = (total_returns / total_orders * 100.0) if total_orders > 0 else 0.0
    missing_claims = customer_data.get("claimed_missing_orders", 0)
    account_age = customer_data.get("account_age_months", 12)
    is_vip = customer_data.get("vip_concierge", False)
    item_price = order_data.get("total_paid", order_data.get("price", 0.0))

    # Signal 1: Transaction Financial Exposure
    if item_price > 100000.0:
        score += 12
        risk_factors.append(f"High financial exposure order: ₹{item_price:,.2f}")
    elif item_price > 25000.0:
        score += 8
    elif item_price > 5000.0:
        score += 4
    else:
        score += 2

    # Signal 2: Return Frequency & Velocity
    if return_rate > 50.0:
        score += 26
        risk_factors.append(f"Abnormally high lifetime return rate ({return_rate:.1f}% across {total_orders} orders)")
    elif return_rate > 25.0:
        score += 18
        risk_factors.append(f"Elevated return rate ({return_rate:.1f}%)")
    elif return_rate > 8.0:
        score += 6
        risk_factors.append(f"Non-zero return history ({return_rate:.1f}%)")

    # Signal 3: Historical Missing Package Claims
    if missing_claims >= 2:
        score += 20
        risk_factors.append(f"Repeat missing/stolen parcel history ({missing_claims} previous claims on record)")
    elif missing_claims == 1:
        score += 10
        risk_factors.append("One previous missing package claim recorded")

    # Signal 4: High Value + Missing / Stolen Claim
    is_missing_claim = "stolen" in claim_type.lower() or "empty" in claim_type.lower() or "missing" in claim_type.lower()
    if is_missing_claim and item_price > 25000.0:
        score += 15
        risk_factors.append(f"High-value asset missing claim (₹{item_price:,.2f})")

    # Signal 5: Carrier Logistics Discrepancy (e.g. Direct Signature vs Denial)
    if carrier_tracking and is_missing_claim:
        tracking_status = carrier_tracking.get("status", "")
        signed_by = carrier_tracking.get("signed_by", "")
        if tracking_status == "DELIVERED" and signed_by:
            score += 15
            risk_factors.append(
                f"Direct conflict with carrier physical delivery proof (Carrier logged signature: '{signed_by}')"
            )

    # Signal 6: Category Hygiene & Return Policy Deviation
    if order_data.get("category") == "Beauty & Personal Care" or "hygiene" in claim_type.lower() or "ineligible" in claim_type.lower():
        score += 24
        risk_factors.append("Policy deviation: Hygiene-restricted item or return window exceeded")

    # Mitigating Factor: VIP Platinum Loyalty
    if is_vip:
        score = max(5, score - 20)
        risk_factors.append("Mitigating: Account holds VIP Platinum Concierge status with verified high LTV")

    # Cap score at 100
    final_score = min(100, max(0, score))

    if final_score >= 70:
        level = "CRITICAL"
        action = "HALT_AUTOMATION_ESCALATE_SUPERVISOR"
    elif final_score >= 50:
        level = "HIGH"
        action = "REQUIRE_ADDITIONAL_VERIFICATION"
    elif final_score >= 25:
        level = "MEDIUM"
        action = "STANDARD_AUDIT"
    else:
        level = "LOW"
        action = "AUTO_APPROVE_ELIGIBLE"

    return {
        "risk_score": final_score,
        "risk_level": level,
        "recommended_action": action,
        "risk_factors": risk_factors,
        "customer_return_rate_pct": round(return_rate, 1),
        "total_prior_claims": missing_claims,
        "supervisor_escalation_required": final_score >= 60
    }
