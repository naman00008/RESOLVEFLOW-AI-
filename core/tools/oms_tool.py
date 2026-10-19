"""
Order Management System (OMS) and Carrier Logistics Tool
Simulates querying enterprise e-commerce databases and logistics carrier APIs.
"""

from typing import Dict, Any, Optional
from ..data.mock_database import ORDERS, CUSTOMERS, TRACKING_DATA

def lookup_order(order_id: str) -> Dict[str, Any]:
    """
    Retrieves full order specifications from the OMS database.
    """
    clean_id = order_id.strip().upper()
    if clean_id in ORDERS:
        order = ORDERS[clean_id].copy()
        # Attach customer info
        cust_id = order.get("customer_id")
        if cust_id and cust_id in CUSTOMERS:
            order["customer_profile"] = CUSTOMERS[cust_id]
        return {
            "found": True,
            "order": order
        }
    return {
        "found": False,
        "error": f"Order ID '{order_id}' was not found in the OMS database."
    }

def lookup_carrier_tracking(tracking_number: str) -> Dict[str, Any]:
    """
    Queries simulated carrier logistics tracking API (FedEx, DHL, UPS, BlueDart).
    """
    clean_num = tracking_number.strip().upper()
    if clean_num in TRACKING_DATA:
        return {
            "found": True,
            "tracking": TRACKING_DATA[clean_num]
        }
    return {
        "found": False,
        "error": f"Tracking number '{tracking_number}' not recognized by carrier gateway."
    }

def lookup_customer(customer_id: str) -> Dict[str, Any]:
    """
    Retrieves customer account history, tier, and lifetime stats.
    """
    clean_id = customer_id.strip().upper()
    if clean_id in CUSTOMERS:
        return {
            "found": True,
            "customer": CUSTOMERS[clean_id]
        }
    return {
        "found": False,
        "error": f"Customer ID '{customer_id}' not found."
    }
