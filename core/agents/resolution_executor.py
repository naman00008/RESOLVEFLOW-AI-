"""
Resolution Executor Agent for ResolveFlow AI
Executes deterministic business logic, calculates refunds, checks inventory,
and schedules reverse logistics workflows.
"""

from typing import Dict, Any, List, Optional
from ..tools.policy_engine import evaluate_return_policy
from ..tools.resolution_actions import (
    calculate_financial_remedy,
    generate_logistics_action
)

class ResolutionExecutorAgent:
    """
    Executor Agent that applies business rules and calculates financial adjustments.
    """
    def __init__(self):
        self.role = "Resolution Executor Agent"

    def run(
        self,
        triage_info: Dict[str, Any],
        research_info: Dict[str, Any],
        custom_policy_matrix: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes policy checks and generates proposed resolution actions.
        """
        order_data = research_info.get("order_data", {})
        customer_data = research_info.get("customer_data", {})
        carrier_data = research_info.get("carrier_data", {})

        category = order_data.get("category", "General")
        delivery_date = order_data.get("delivery_date")
        claim_type = triage_info.get("claim_type", "general")
        carrier_status = carrier_data.get("status", "UNKNOWN")
        stock_available = order_data.get("replacement_stock_available", 0)

        tool_calls: List[Dict[str, Any]] = []

        # Tool 1: Evaluate Policy
        policy_res = evaluate_return_policy(
            category,
            delivery_date,
            triage_info.get("category", ""),
            custom_policy_matrix=custom_policy_matrix
        )
        tool_calls.append({
            "tool": "evaluate_return_policy",
            "args": {"category": category, "delivery_date": delivery_date, "claim_type": claim_type},
            "result": policy_res
        })

        proposed_remedy_type = "UNKNOWN"
        financial_remedy = {}
        logistics_action = {}
        operational_summary = ""

        # Branch A: Logistics Stall / Delayed in transit
        if carrier_status in ["DELAYED_IN_TRANSIT", "IN_TRANSIT"] and not delivery_date:
            proposed_remedy_type = "DELAY_COMPENSATION"
            financial_remedy = calculate_financial_remedy(order_data, "DELAY_COMPENSATION", policy_res)
            tool_calls.append({
                "tool": "calculate_financial_remedy",
                "args": {"remedy_type": "DELAY_COMPENSATION"},
                "result": financial_remedy
            })
            operational_summary = (
                f"Package is delayed in transit ({carrier_data.get('carrier')}). "
                f"Proposed action: File carrier trace escalation, expedite tracking, and issue "
                f"₹{financial_remedy.get('compensation_store_credit', 0):,.2f} store credit."
            )

        # Branch B: Missing / Stolen Claim (Potentially High Risk)
        elif claim_type == "stolen_missing":
            proposed_remedy_type = "MISSING_PARCEL_CLAIM_REVIEW"
            # Provisional calculation, but will require strict Critic scrutiny
            financial_remedy = calculate_financial_remedy(order_data, "FULL_REFUND", policy_res)
            operational_summary = (
                f"Customer claims parcel was empty/stolen. Order value: ₹{order_data.get('total_paid', 0):,.2f}. "
                "Submitted provisional full refund calculation to Critic Agent for fraud/abuse evaluation."
            )

        # Branch C: Non-returnable or Expired Window
        elif not policy_res["eligible"]:
            proposed_remedy_type = "POLICY_REFUSAL_GOODWILL_COUPON"
            financial_remedy = calculate_financial_remedy(order_data, "POLICY_DENIAL_GOODWILL", policy_res)
            tool_calls.append({
                "tool": "calculate_financial_remedy",
                "args": {"remedy_type": "POLICY_DENIAL_GOODWILL"},
                "result": financial_remedy
            })
            operational_summary = (
                f"Item ineligible for standard return ({policy_res.get('reason')}). "
                f"Proposed action: Enforce policy, deny cash refund, and issue 15% goodwill coupon "
                f"({financial_remedy.get('coupon_code')})."
            )

        # Branch D: Defective / Damaged Item within valid window
        elif claim_type in ["damaged_defect", "wrong_item"]:
            if customer_data.get("vip_concierge", False) and claim_type == "wrong_item":
                proposed_remedy_type = "VIP_EXPEDITED_EXCHANGE"
                financial_remedy = calculate_financial_remedy(order_data, "SIZE_EXCHANGE", policy_res)
                logistics_action = generate_logistics_action(order_data.get("order_id", ""), "CONCIERGE_SWAP", "Priority Courier")
                operational_summary = (
                    "VIP Platinum customer received wrong size. Immediate courier exchange initiated "
                    "with zero return friction and waived fees."
                )
            elif stock_available > 0:
                proposed_remedy_type = "REPLACEMENT"
                financial_remedy = calculate_financial_remedy(order_data, "REPLACEMENT", policy_res)
                logistics_action = generate_logistics_action(order_data.get("order_id", ""), "REVERSE_PICKUP_LABEL", order_data.get("carrier", "FedEx"))
                operational_summary = (
                    f"Defective item reported within {policy_res.get('days_since_delivery')} days (Limit: {policy_res.get('allowed_window_days')} days). "
                    f"Replacement stock verified ({stock_available} units). Generated reverse pickup RMA '{logistics_action.get('rma_number')}'."
                )
            else:
                proposed_remedy_type = "FULL_REFUND"
                financial_remedy = calculate_financial_remedy(order_data, "FULL_REFUND", policy_res)
                logistics_action = generate_logistics_action(order_data.get("order_id", ""), "RETURN_AND_REFUND", order_data.get("carrier", "FedEx"))
                operational_summary = "Defective item; replacement out of stock. Full refund + reverse pickup initiated."

            tool_calls.append({
                "tool": "calculate_financial_remedy",
                "args": {"remedy_type": proposed_remedy_type},
                "result": financial_remedy
            })
            if logistics_action:
                tool_calls.append({
                    "tool": "generate_logistics_action",
                    "args": {"order_id": order_data.get("order_id"), "action": proposed_remedy_type},
                    "result": logistics_action
                })

        # Branch E: General return
        else:
            proposed_remedy_type = "RETURN_AND_REFUND"
            financial_remedy = calculate_financial_remedy(order_data, "RETURN_AND_REFUND", policy_res)
            logistics_action = generate_logistics_action(order_data.get("order_id", ""), "RETURN_LABEL", order_data.get("carrier", "FedEx"))
            operational_summary = f"Standard return authorized within policy window. Restocking fee: {policy_res.get('restocking_fee_pct')*100}%."

        thoughts = (
            f"Policy evaluation completed: Category='{category}', Eligible={policy_res.get('eligible')}. "
            f"Formulated proposed remedy: '{proposed_remedy_type}'. "
            f"Financial impact: {financial_remedy.get('remedy_type', 'N/A')}. "
            "Forwarding complete proposal to Critic & Auditor Agent for risk assessment."
        )

        return {
            "proposed_remedy_type": proposed_remedy_type,
            "policy_evaluation": policy_res,
            "financial_remedy": financial_remedy,
            "logistics_action": logistics_action,
            "operational_summary": operational_summary,
            "tool_calls": tool_calls,
            "executor_thoughts": thoughts
        }
