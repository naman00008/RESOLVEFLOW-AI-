"""
OMS & Research Agent for ResolveFlow AI
Collects ground-truth order, customer, and carrier logistics evidence from enterprise systems.
"""

from typing import Dict, Any
from ..tools.oms_tool import lookup_order, lookup_carrier_tracking, lookup_customer

class OMSResearchAgent:
    """
    Research Agent that queries enterprise databases and logistics gateways.
    """
    def __init__(self):
        self.role = "OMS & Research Agent"

    def run(self, order_id: str) -> Dict[str, Any]:
        """
        Executes order and carrier telemetry lookups.
        """
        tool_calls = []

        # Tool Call 1: Order Lookup
        order_res = lookup_order(order_id)
        tool_calls.append({
            "tool": "lookup_order",
            "args": {"order_id": order_id},
            "result_status": "SUCCESS" if order_res["found"] else "NOT_FOUND"
        })

        if not order_res["found"]:
            return {
                "success": False,
                "error": order_res.get("error", "Order not found"),
                "order_data": {},
                "customer_data": {},
                "carrier_data": {},
                "tool_calls": tool_calls,
                "researcher_thoughts": f"Queried OMS for {order_id}. Record does not exist in backend database."
            }

        order_data = order_res["order"]
        customer_id = order_data.get("customer_id", "")

        # Tool Call 2: Customer Lookup
        cust_res = lookup_customer(customer_id)
        tool_calls.append({
            "tool": "lookup_customer",
            "args": {"customer_id": customer_id},
            "result_status": "SUCCESS" if cust_res["found"] else "NOT_FOUND"
        })
        customer_data = cust_res.get("customer", {})

        # Tool Call 3: Carrier Tracking Lookup
        tracking_num = order_data.get("tracking_number", "")
        carrier_res = lookup_carrier_tracking(tracking_num)
        tool_calls.append({
            "tool": "lookup_carrier_tracking",
            "args": {"tracking_number": tracking_num},
            "result_status": "SUCCESS" if carrier_res["found"] else "NOT_FOUND"
        })
        carrier_data = carrier_res.get("tracking", {})

        # Synthesis & Reasoning
        product_name = order_data.get("product_name")
        price = order_data.get("price")
        carrier_status = carrier_data.get("status", "UNKNOWN")
        cust_tier = customer_data.get("tier", "Standard")
        return_rate = customer_data.get("return_rate_pct", 0.0)

        thoughts = (
            f"Verified Order '{order_id}': Product='{product_name}', Total=₹{order_data.get('total_paid', 0):,.2f}, "
            f"Category='{order_data.get('category')}'. "
            f"Carrier '{order_data.get('carrier')}' reports status: '{carrier_status}'. "
            f"Customer '{customer_data.get('name')}' (Tier: {cust_tier}, Lifetime Orders: {customer_data.get('total_orders')}, "
            f"Return Rate: {return_rate}%). Extracted all telemetry for policy engine."
        )

        return {
            "success": True,
            "order_data": order_data,
            "customer_data": customer_data,
            "carrier_data": carrier_data,
            "tool_calls": tool_calls,
            "researcher_thoughts": thoughts
        }
