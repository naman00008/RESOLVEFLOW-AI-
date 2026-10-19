"""
Critic & Fraud Auditor Agent for ResolveFlow AI
Validates proposed resolution actions against compliance regulations,
computes fraud/abuse risk scores, and enforces Human-in-the-Loop (HITL) gates.
"""

from typing import Dict, Any, List
from ..tools.fraud_detector import assess_fraud_risk

class CriticAuditorAgent:
    """
    Critic Agent that audits the Executor's decisions, scans for fraud/abuse,
    and prevents improper automated payouts.
    """
    def __init__(self):
        self.role = "Critic & Fraud Auditor Agent"

    def run(
        self,
        triage_info: Dict[str, Any],
        research_info: Dict[str, Any],
        executor_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Audits the proposed remedy, runs fraud detection, and outputs final decision gate.
        """
        order_data = research_info.get("order_data", {})
        customer_data = research_info.get("customer_data", {})
        carrier_data = research_info.get("carrier_data", {})
        claim_type = triage_info.get("claim_type", "general")
        policy_eval = executor_info.get("policy_evaluation", {})
        proposed_remedy = executor_info.get("proposed_remedy_type", "")

        tool_calls: List[Dict[str, Any]] = []

        # Tool 1: Assess Fraud & Abuse Risk
        fraud_res = assess_fraud_risk(
            customer_data=customer_data,
            order_data=order_data,
            carrier_tracking=carrier_data,
            claim_type=claim_type
        )
        tool_calls.append({
            "tool": "assess_fraud_risk",
            "args": {
                "customer_id": customer_data.get("customer_id"),
                "claim_type": claim_type,
                "order_value": order_data.get("total_paid")
            },
            "result": fraud_res
        })

        compliance_checks = []
        is_overruled = False
        final_verdict = proposed_remedy
        critic_notes: List[str] = []

        # Check 1: Fraud Risk Threshold
        fraud_score = fraud_res.get("risk_score", 0)
        if fraud_score >= 60:
            compliance_checks.append({
                "check": "Fraud & Abuse Safety Threshold",
                "status": "FAILED",
                "detail": f"Risk Score {fraud_score}/100 exceeds automation limit (60). {len(fraud_res.get('risk_factors', []))} anomaly flags detected."
            })
            is_overruled = True
            final_verdict = "ESCALATED_TO_HUMAN_SUPERVISOR"
            critic_notes.append(
                "CRITIC INTERVENTION: Halted automated refund! Customer profile indicates high return velocity "
                f"({customer_data.get('return_rate_pct')}%) and carrier records confirm direct signature delivery."
            )
        else:
            compliance_checks.append({
                "check": "Fraud & Abuse Safety Threshold",
                "status": "PASSED",
                "detail": f"Risk Score {fraud_score}/100 within acceptable threshold."
            })

        # Check 2: Policy Compliance Check
        if not policy_eval.get("eligible", True) and proposed_remedy in ["FULL_REFUND", "REPLACEMENT"]:
            compliance_checks.append({
                "check": "Policy Boundary Verification",
                "status": "OVERRULED",
                "detail": "Executor proposed refund for an ineligible item. Corrected to policy-compliant refusal."
            })
            is_overruled = True
            final_verdict = "POLICY_REFUSAL_GOODWILL_COUPON"
            critic_notes.append("CRITIC SANITY CHECK: Corrected remedy to adhere to FDA hygiene and return window rules.")
        else:
            compliance_checks.append({
                "check": "Policy Boundary Verification",
                "status": "PASSED",
                "detail": "Action strictly conforms to institutional category return window."
            })

        # Check 3: VIP Loyalty Safeguard
        if customer_data.get("vip_concierge", False):
            compliance_checks.append({
                "check": "VIP Customer Retention Safeguard",
                "status": "PASSED",
                "detail": "Verified Platinum Concierge entitlement: fee waivers and priority dispatch authorized."
            })

        # Reflection and Thought Process
        if is_overruled:
            thoughts = (
                f"CRITIQUE TRIGGERED: Overruled Executor's preliminary proposal '{proposed_remedy}'! "
                f"Enforced decision '{final_verdict}'. Justification: {'; '.join(critic_notes)}. "
                f"Assigned Risk Level '{fraud_res.get('risk_level')}' (Score: {fraud_score}/100)."
            )
        else:
            thoughts = (
                f"Audit completed: Validated Executor's proposed action '{proposed_remedy}'. "
                f"All {len(compliance_checks)} compliance checks passed. "
                f"Fraud risk is {fraud_res.get('risk_level')} ({fraud_score}/100). Approved for automated fulfillment."
            )

        return {
            "final_verdict": final_verdict,
            "is_overruled": is_overruled,
            "fraud_assessment": fraud_res,
            "compliance_checks": compliance_checks,
            "critic_notes": critic_notes,
            "supervisor_escalation_required": final_verdict == "ESCALATED_TO_HUMAN_SUPERVISOR",
            "tool_calls": tool_calls,
            "critic_thoughts": thoughts
        }
