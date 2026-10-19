"""
Mock Database Engine for ResolveFlow AI
Provides realistic Indian e-commerce backend entities:
- Customer records (with return histories and LTV in INR)
- Order records (items, payment status, delivery timestamps, INR pricing)
- Carrier tracking checkpoints (live logistics statuses across Indian transit hubs)
- Return & refund policy matrices
- Pre-configured benchmark complaint scenarios
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Reference "Current Date" for simulated time calculations
CURRENT_TIMESTAMP = datetime(2026, 10, 18, 14, 0, 0)

# 1. Product Return Policy Matrix
POLICY_RULES = {
    "Electronics": {
        "return_window_days": 7,
        "allow_refund": True,
        "allow_replacement": True,
        "free_reverse_pickup": True,
        "restocking_fee_pct": 0.0,
        "mandatory_photo_for_damage": True,
        "notes": "Must be reported within 7 days of delivery. Serial number verification required."
    },
    "Apparel": {
        "return_window_days": 30,
        "allow_refund": True,
        "allow_replacement": True,
        "free_reverse_pickup": True,
        "restocking_fee_pct": 0.0,
        "mandatory_photo_for_damage": False,
        "notes": "Must have original tags attached and be unworn. Free size exchange supported."
    },
    "Beauty & Personal Care": {
        "return_window_days": 0,
        "allow_refund": False,
        "allow_replacement": False,
        "free_reverse_pickup": False,
        "restocking_fee_pct": 0.0,
        "mandatory_photo_for_damage": False,
        "notes": "Non-returnable item due to hygiene and health regulations once delivered."
    },
    "Home & Kitchen": {
        "return_window_days": 15,
        "allow_refund": True,
        "allow_replacement": True,
        "free_reverse_pickup": True,
        "restocking_fee_pct": 0.10,  # 10% restocking fee if discretionary return
        "mandatory_photo_for_damage": True,
        "notes": "15 days return window. Free replacement for manufacturer defects."
    },
    "Computing": {
        "return_window_days": 14,
        "allow_refund": True,
        "allow_replacement": True,
        "free_reverse_pickup": True,
        "restocking_fee_pct": 0.0,
        "mandatory_photo_for_damage": True,
        "notes": "High-value asset policy. Claims of missing parcels over ₹25,000 require carrier investigation."
    }
}

# 2. Customer Profiles (Indian Demographics & INR LTV)
CUSTOMERS: Dict[str, Dict[str, Any]] = {
    "CUST-101": {
        "customer_id": "CUST-101",
        "name": "Aarav Sharma",
        "email": "aarav.sharma@example.in",
        "tier": "Standard",
        "account_age_months": 18,
        "total_orders": 4,
        "total_spend": 48500.00,
        "total_returns": 0,
        "claimed_missing_orders": 0,
        "return_rate_pct": 0.0,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-102": {
        "customer_id": "CUST-102",
        "name": "Rohan Mehta",
        "email": "rohan.mehta@example.in",
        "tier": "Silver",
        "account_age_months": 24,
        "total_orders": 9,
        "total_spend": 105000.00,
        "total_returns": 1,
        "claimed_missing_orders": 0,
        "return_rate_pct": 11.1,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-103": {
        "customer_id": "CUST-103",
        "name": "Meera Iyer",
        "email": "meera.iyer@example.in",
        "tier": "Standard",
        "account_age_months": 6,
        "total_orders": 2,
        "total_spend": 12500.00,
        "total_returns": 0,
        "claimed_missing_orders": 0,
        "return_rate_pct": 0.0,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-104": {
        "customer_id": "CUST-104",
        "name": "Vikram Verma",
        "email": "vikram.verma@example.in",
        "tier": "Standard",
        "account_age_months": 4,
        "total_orders": 12,
        "total_spend": 285000.00,
        "total_returns": 8,
        "claimed_missing_orders": 3,
        "return_rate_pct": 66.7,
        "fraud_risk_level": "HIGH",
        "vip_concierge": False
    },
    "CUST-105": {
        "customer_id": "CUST-105",
        "name": "Dr. Ananya Sen",
        "email": "dr.ananya.sen@example.in",
        "tier": "Platinum VIP",
        "account_age_months": 48,
        "total_orders": 38,
        "total_spend": 475000.00,
        "total_returns": 1,
        "claimed_missing_orders": 0,
        "return_rate_pct": 2.6,
        "fraud_risk_level": "VERY_LOW",
        "vip_concierge": True
    },
    "CUST-106": {
        "customer_id": "CUST-106",
        "name": "Aditya Patel",
        "email": "aditya.patel@example.in",
        "tier": "Gold",
        "account_age_months": 30,
        "total_orders": 16,
        "total_spend": 182000.00,
        "total_returns": 1,
        "claimed_missing_orders": 0,
        "return_rate_pct": 6.2,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-107": {
        "customer_id": "CUST-107",
        "name": "Sneha Reddy",
        "email": "sneha.reddy@example.in",
        "tier": "Standard",
        "account_age_months": 8,
        "total_orders": 3,
        "total_spend": 28400.00,
        "total_returns": 0,
        "claimed_missing_orders": 0,
        "return_rate_pct": 0.0,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-108": {
        "customer_id": "CUST-108",
        "name": "Manish Agarwal",
        "email": "manish.agarwal@example.in",
        "tier": "Silver",
        "account_age_months": 15,
        "total_orders": 7,
        "total_spend": 74500.00,
        "total_returns": 1,
        "claimed_missing_orders": 0,
        "return_rate_pct": 14.3,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-109": {
        "customer_id": "CUST-109",
        "name": "Kavita Rao",
        "email": "kavita.rao@example.in",
        "tier": "Standard",
        "account_age_months": 11,
        "total_orders": 5,
        "total_spend": 51900.00,
        "total_returns": 0,
        "claimed_missing_orders": 0,
        "return_rate_pct": 0.0,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-110": {
        "customer_id": "CUST-110",
        "name": "Devendra Joshi",
        "email": "devendra.j@example.in",
        "tier": "Standard",
        "account_age_months": 5,
        "total_orders": 2,
        "total_spend": 17800.00,
        "total_returns": 0,
        "claimed_missing_orders": 0,
        "return_rate_pct": 0.0,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-111": {
        "customer_id": "CUST-111",
        "name": "Pooja Banerjee",
        "email": "pooja.banerjee@example.in",
        "tier": "Gold",
        "account_age_months": 36,
        "total_orders": 22,
        "total_spend": 264000.00,
        "total_returns": 2,
        "claimed_missing_orders": 0,
        "return_rate_pct": 9.1,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-112": {
        "customer_id": "CUST-112",
        "name": "Mayank Kulkarni",
        "email": "m.kulkarni@example.in",
        "tier": "Gold",
        "account_age_months": 28,
        "total_orders": 19,
        "total_spend": 238000.00,
        "total_returns": 1,
        "claimed_missing_orders": 0,
        "return_rate_pct": 5.3,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-113": {
        "customer_id": "CUST-113",
        "name": "Sunita Deshmukh",
        "email": "sunita.d@example.in",
        "tier": "Platinum VIP",
        "account_age_months": 40,
        "total_orders": 31,
        "total_spend": 412000.00,
        "total_returns": 2,
        "claimed_missing_orders": 0,
        "return_rate_pct": 6.5,
        "fraud_risk_level": "VERY_LOW",
        "vip_concierge": True
    },
    "CUST-114": {
        "customer_id": "CUST-114",
        "name": "Deepak Gupta",
        "email": "deepak.gupta@example.in",
        "tier": "Silver",
        "account_age_months": 14,
        "total_orders": 8,
        "total_spend": 82000.00,
        "total_returns": 0,
        "claimed_missing_orders": 0,
        "return_rate_pct": 0.0,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-115": {
        "customer_id": "CUST-115",
        "name": "Priya Nair",
        "email": "priya.nair@example.in",
        "tier": "Gold",
        "account_age_months": 22,
        "total_orders": 14,
        "total_spend": 196000.00,
        "total_returns": 1,
        "claimed_missing_orders": 0,
        "return_rate_pct": 7.1,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-116": {
        "customer_id": "CUST-116",
        "name": "Sanya Malhotra",
        "email": "sanya.m@example.in",
        "tier": "Standard",
        "account_age_months": 9,
        "total_orders": 3,
        "total_spend": 25900.00,
        "total_returns": 0,
        "claimed_missing_orders": 0,
        "return_rate_pct": 0.0,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-117": {
        "customer_id": "CUST-117",
        "name": "Jatin Chawla",
        "email": "jatin.c@example.in",
        "tier": "Silver",
        "account_age_months": 18,
        "total_orders": 10,
        "total_spend": 118000.00,
        "total_returns": 1,
        "claimed_missing_orders": 0,
        "return_rate_pct": 10.0,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-118": {
        "customer_id": "CUST-118",
        "name": "Lakshya Singhania",
        "email": "lakshya.s@example.in",
        "tier": "Standard",
        "account_age_months": 7,
        "total_orders": 4,
        "total_spend": 38400.00,
        "total_returns": 0,
        "claimed_missing_orders": 0,
        "return_rate_pct": 0.0,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-119": {
        "customer_id": "CUST-119",
        "name": "Esha Mukherjee",
        "email": "esha.mukherjee@example.in",
        "tier": "Standard",
        "account_age_months": 12,
        "total_orders": 5,
        "total_spend": 48900.00,
        "total_returns": 1,
        "claimed_missing_orders": 0,
        "return_rate_pct": 20.0,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-120": {
        "customer_id": "CUST-120",
        "name": "Kunal Bhatia",
        "email": "kunal.b@example.in",
        "tier": "Gold",
        "account_age_months": 32,
        "total_orders": 25,
        "total_spend": 331000.00,
        "total_returns": 2,
        "claimed_missing_orders": 0,
        "return_rate_pct": 8.0,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    },
    "CUST-121": {
        "customer_id": "CUST-121",
        "name": "Farhan Siddiqui",
        "email": "farhan.s@example.in",
        "tier": "Standard",
        "account_age_months": 6,
        "total_orders": 2,
        "total_spend": 14700.00,
        "total_returns": 0,
        "claimed_missing_orders": 0,
        "return_rate_pct": 0.0,
        "fraud_risk_level": "LOW",
        "vip_concierge": False
    }
}

# 3. Order Management System (OMS) Data (INR Pricing, Indian Carriers & Gateways)
ORDERS: Dict[str, Dict[str, Any]] = {
    "ORD-9821": {
        "order_id": "ORD-9821",
        "customer_id": "CUST-101",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=5)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=2)).strftime("%Y-%m-%d"),
        "product_name": "AcousticPro Studio Noise-Cancelling Headphones",
        "sku": "ELEC-HP-901",
        "category": "Electronics",
        "price": 24999.00,
        "tax": 4500.00,
        "shipping_fee": 0.00,
        "total_paid": 29499.00,
        "payment_method": "UPI (Google Pay / SBI)",
        "order_status": "DELIVERED",
        "carrier": "BlueDart Express",
        "tracking_number": "TRK-BD-9821",
        "replacement_stock_available": 14
    },
    "ORD-7742": {
        "order_id": "ORD-7742",
        "customer_id": "CUST-102",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=10)).strftime("%Y-%m-%d"),
        "delivery_date": None,  # Not yet delivered
        "promised_delivery_date": (CURRENT_TIMESTAMP - timedelta(days=4)).strftime("%Y-%m-%d"),
        "product_name": "BaristaMaster Compact Espresso Machine",
        "sku": "HOME-ESP-420",
        "category": "Home & Kitchen",
        "price": 29999.00,
        "tax": 5400.00,
        "shipping_fee": 500.00,
        "total_paid": 35899.00,
        "payment_method": "NetBanking (HDFC Bank)",
        "order_status": "IN_TRANSIT",
        "carrier": "Delhivery Prime",
        "tracking_number": "TRK-DLV-7742",
        "replacement_stock_available": 6
    },
    "ORD-5190": {
        "order_id": "ORD-5190",
        "customer_id": "CUST-103",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=42)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=38)).strftime("%Y-%m-%d"),
        "product_name": "GlowBotanica Peptide Anti-Aging Serum Set (30ml)",
        "sku": "BEAUTY-SER-112",
        "category": "Beauty & Personal Care",
        "price": 7499.00,
        "tax": 1350.00,
        "shipping_fee": 150.00,
        "total_paid": 8999.00,
        "payment_method": "UPI (PhonePe)",
        "order_status": "DELIVERED",
        "carrier": "BlueDart Express",
        "tracking_number": "TRK-BD-5190",
        "replacement_stock_available": 25
    },
    "ORD-3319": {
        "order_id": "ORD-3319",
        "customer_id": "CUST-104",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=3)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=1)).strftime("%Y-%m-%d"),
        "product_name": "TitanV Pro 16-inch RTX 4080 Gaming Laptop",
        "sku": "COMP-LAP-880",
        "category": "Computing",
        "price": 149990.00,
        "tax": 26998.20,
        "shipping_fee": 0.00,
        "total_paid": 176988.20,
        "payment_method": "Credit Card (HDFC Regalia ending 9931)",
        "order_status": "DELIVERED",
        "carrier": "BlueDart Apex Express",
        "tracking_number": "TRK-BD-3319",
        "replacement_stock_available": 3
    },
    "ORD-6401": {
        "order_id": "ORD-6401",
        "customer_id": "CUST-105",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=6)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=3)).strftime("%Y-%m-%d"),
        "product_name": "Venezia Handcrafted Italian Leather Chelsea Boots (Size 42)",
        "sku": "APP-BOOT-042",
        "category": "Apparel",
        "price": 32000.00,
        "tax": 5760.00,
        "shipping_fee": 0.00,
        "total_paid": 37760.00,
        "payment_method": "Amex Platinum (ending 1004)",
        "order_status": "DELIVERED",
        "carrier": "Shadowfax VIP Priority",
        "tracking_number": "TRK-SFX-6401",
        "replacement_stock_available": 8
    },
    "ORD-1102": {
        "order_id": "ORD-1102",
        "customer_id": "CUST-106",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=6)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=4)).strftime("%Y-%m-%d"),
        "product_name": "ProView 32-inch 4K HDR IPS Designer Monitor",
        "sku": "ELEC-MON-320",
        "category": "Electronics",
        "price": 38990.00,
        "tax": 7018.20,
        "shipping_fee": 0.00,
        "total_paid": 46008.20,
        "payment_method": "UPI (Paytm / Axis Bank)",
        "order_status": "DELIVERED",
        "carrier": "Delhivery Prime",
        "tracking_number": "TRK-DLV-1102",
        "replacement_stock_available": 5
    },
    "ORD-2245": {
        "order_id": "ORD-2245",
        "customer_id": "CUST-107",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=16)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=12)).strftime("%Y-%m-%d"),
        "product_name": "SummitShield Waterproof Gore-Tex Alpine Parka",
        "sku": "APP-JCKT-108",
        "category": "Apparel",
        "price": 16500.00,
        "tax": 2970.00,
        "shipping_fee": 0.00,
        "total_paid": 19470.00,
        "payment_method": "Credit Card (ICICI Coral ending 1104)",
        "order_status": "DELIVERED",
        "carrier": "DTDC Air Cargo",
        "tracking_number": "TRK-DTDC-2245",
        "replacement_stock_available": 12
    },
    "ORD-8830": {
        "order_id": "ORD-8830",
        "customer_id": "CUST-108",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=26)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=22)).strftime("%Y-%m-%d"),
        "product_name": "RoboClean Smart Laser Mapping Vacuum & Mop",
        "sku": "HOME-VAC-900",
        "category": "Home & Kitchen",
        "price": 38500.00,
        "tax": 6930.00,
        "shipping_fee": 0.00,
        "total_paid": 45430.00,
        "payment_method": "NetBanking (State Bank of India)",
        "order_status": "DELIVERED",
        "carrier": "Delhivery Prime",
        "tracking_number": "TRK-DLV-8830",
        "replacement_stock_available": 4
    },
    "ORD-4491": {
        "order_id": "ORD-4491",
        "customer_id": "CUST-109",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=8)).strftime("%Y-%m-%d"),
        "delivery_date": None,
        "promised_delivery_date": (CURRENT_TIMESTAMP - timedelta(days=3)).strftime("%Y-%m-%d"),
        "product_name": "ErgoType Split Wireless Mechanical Keyboard",
        "sku": "COMP-KEY-301",
        "category": "Computing",
        "price": 14500.00,
        "tax": 2610.00,
        "shipping_fee": 350.00,
        "total_paid": 17460.00,
        "payment_method": "Credit Card (Axis Flipkart ending 5541)",
        "order_status": "IN_TRANSIT",
        "carrier": "BlueDart Express",
        "tracking_number": "TRK-BD-4491",
        "replacement_stock_available": 18
    },
    "ORD-7123": {
        "order_id": "ORD-7123",
        "customer_id": "CUST-110",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=8)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=5)).strftime("%Y-%m-%d"),
        "product_name": "AuraGlow Botanical Hair Repair Essential Oils (100ml)",
        "sku": "BEAUTY-OIL-404",
        "category": "Beauty & Personal Care",
        "price": 8900.00,
        "tax": 1602.00,
        "shipping_fee": 0.00,
        "total_paid": 10502.00,
        "payment_method": "UPI (Google Pay)",
        "order_status": "DELIVERED",
        "carrier": "BlueDart Express",
        "tracking_number": "TRK-BD-7123",
        "replacement_stock_available": 20
    },
    "ORD-9054": {
        "order_id": "ORD-9054",
        "customer_id": "CUST-101",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=3)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=1)).strftime("%Y-%m-%d"),
        "product_name": "PulseAir Active Noise-Cancelling Sport Earbuds",
        "sku": "ELEC-BUD-550",
        "category": "Electronics",
        "price": 11999.00,
        "tax": 2159.82,
        "shipping_fee": 0.00,
        "total_paid": 14158.82,
        "payment_method": "UPI (PhonePe / Kotak)",
        "order_status": "DELIVERED",
        "carrier": "Delhivery Prime",
        "tracking_number": "TRK-DLV-9054",
        "replacement_stock_available": 35
    },
    "ORD-3788": {
        "order_id": "ORD-3788",
        "customer_id": "CUST-102",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=5)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=3)).strftime("%Y-%m-%d"),
        "product_name": "HyperSpeed 2TB NVMe PCIe Gen4 M.2 Gaming SSD",
        "sku": "COMP-SSD-200",
        "category": "Computing",
        "price": 16999.00,
        "tax": 3059.82,
        "shipping_fee": 0.00,
        "total_paid": 20058.82,
        "payment_method": "NetBanking (HDFC Bank)",
        "order_status": "DELIVERED",
        "carrier": "DTDC Air Cargo",
        "tracking_number": "TRK-DTDC-3788",
        "replacement_stock_available": 15
    },
    "ORD-6210": {
        "order_id": "ORD-6210",
        "customer_id": "CUST-105",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=4)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=2)).strftime("%Y-%m-%d"),
        "product_name": "SavileRow Bespoke Merino Wool Long Trench Coat",
        "sku": "APP-COAT-501",
        "category": "Apparel",
        "price": 24500.00,
        "tax": 4410.00,
        "shipping_fee": 0.00,
        "total_paid": 28910.00,
        "payment_method": "Amex Platinum (ending 1004)",
        "order_status": "DELIVERED",
        "carrier": "Shadowfax VIP Priority",
        "tracking_number": "TRK-SFX-6210",
        "replacement_stock_available": 7
    },
    "ORD-8432": {
        "order_id": "ORD-8432",
        "customer_id": "CUST-111",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=12)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=8)).strftime("%Y-%m-%d"),
        "product_name": "LeArtisan Enameled Cast Iron Dutch Oven (6 Qt)",
        "sku": "HOME-POT-600",
        "category": "Home & Kitchen",
        "price": 11500.00,
        "tax": 2070.00,
        "shipping_fee": 0.00,
        "total_paid": 13570.00,
        "payment_method": "UPI (Google Pay)",
        "order_status": "DELIVERED",
        "carrier": "Delhivery Prime",
        "tracking_number": "TRK-DLV-8432",
        "replacement_stock_available": 9
    },
    "ORD-5509": {
        "order_id": "ORD-5509",
        "customer_id": "CUST-104",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=2)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=1)).strftime("%Y-%m-%d"),
        "product_name": "ClearStream 4K UltraHD Studio Streaming Webcam",
        "sku": "COMP-CAM-400",
        "category": "Computing",
        "price": 12900.00,
        "tax": 2322.00,
        "shipping_fee": 0.00,
        "total_paid": 15222.00,
        "payment_method": "Credit Card (HDFC Regalia ending 9931)",
        "order_status": "DELIVERED",
        "carrier": "DTDC Air Cargo",
        "tracking_number": "TRK-DTDC-5509",
        "replacement_stock_available": 11
    },
    "ORD-1290": {
        "order_id": "ORD-1290",
        "customer_id": "CUST-112",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=6)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=3)).strftime("%Y-%m-%d"),
        "product_name": "UltraFit GPS Multisport Rugged Smartwatch",
        "sku": "ELEC-WCH-810",
        "category": "Electronics",
        "price": 18499.00,
        "tax": 3329.82,
        "shipping_fee": 0.00,
        "total_paid": 21828.82,
        "payment_method": "Credit Card (SBI SimplyCLICK ending 3301)",
        "order_status": "DELIVERED",
        "carrier": "BlueDart Express",
        "tracking_number": "TRK-BD-1290",
        "replacement_stock_available": 16
    },
    "ORD-4821": {
        "order_id": "ORD-4821",
        "customer_id": "CUST-113",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=8)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=5)).strftime("%Y-%m-%d"),
        "product_name": "NordicPeak 800-Fill Goose Down Parka Coat (M)",
        "sku": "APP-DOWN-702",
        "category": "Apparel",
        "price": 21990.00,
        "tax": 3958.20,
        "shipping_fee": 0.00,
        "total_paid": 25948.20,
        "payment_method": "Amex Platinum (ending 4002)",
        "order_status": "DELIVERED",
        "carrier": "Shadowfax VIP Priority",
        "tracking_number": "TRK-SFX-4821",
        "replacement_stock_available": 8
    },
    "ORD-6734": {
        "order_id": "ORD-6734",
        "customer_id": "CUST-114",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=9)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=6)).strftime("%Y-%m-%d"),
        "product_name": "AeroChef Dual-Zone 10-Quart Air Fryer XL",
        "sku": "HOME-FRY-300",
        "category": "Home & Kitchen",
        "price": 14999.00,
        "tax": 2699.82,
        "shipping_fee": 0.00,
        "total_paid": 17698.82,
        "payment_method": "NetBanking (ICICI Bank)",
        "order_status": "DELIVERED",
        "carrier": "Delhivery Prime",
        "tracking_number": "TRK-DLV-6734",
        "replacement_stock_available": 12
    },
    "ORD-7890": {
        "order_id": "ORD-7890",
        "customer_id": "CUST-115",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=4)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=2)).strftime("%Y-%m-%d"),
        "product_name": "QuantumBook 14 3K OLED Ultraportable Laptop",
        "sku": "COMP-LAP-140",
        "category": "Computing",
        "price": 119990.00,
        "tax": 21598.20,
        "shipping_fee": 0.00,
        "total_paid": 141588.20,
        "payment_method": "Credit Card (Visa Signature ending 7741)",
        "order_status": "DELIVERED",
        "carrier": "BlueDart Express",
        "tracking_number": "TRK-BD-7890",
        "replacement_stock_available": 7
    },
    "ORD-2341": {
        "order_id": "ORD-2341",
        "customer_id": "CUST-116",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=7)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=4)).strftime("%Y-%m-%d"),
        "product_name": "LuminaSilk Ceramide Restorative Night Cream (50ml)",
        "sku": "BEAUTY-CRM-502",
        "category": "Beauty & Personal Care",
        "price": 6500.00,
        "tax": 1170.00,
        "shipping_fee": 0.00,
        "total_paid": 7670.00,
        "payment_method": "UPI (Google Pay)",
        "order_status": "DELIVERED",
        "carrier": "Delhivery Prime",
        "tracking_number": "TRK-DLV-2341",
        "replacement_stock_available": 22
    },
    "ORD-9128": {
        "order_id": "ORD-9128",
        "customer_id": "CUST-117",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=9)).strftime("%Y-%m-%d"),
        "delivery_date": None,
        "promised_delivery_date": (CURRENT_TIMESTAMP - timedelta(days=3)).strftime("%Y-%m-%d"),
        "product_name": "SoundWave Studio Subwoofer 12-inch Powered Bass",
        "sku": "ELEC-SUB-120",
        "category": "Electronics",
        "price": 28000.00,
        "tax": 5040.00,
        "shipping_fee": 850.00,
        "total_paid": 33890.00,
        "payment_method": "NetBanking (HDFC Bank)",
        "order_status": "IN_TRANSIT",
        "carrier": "DTDC Air Cargo",
        "tracking_number": "TRK-DTDC-9128",
        "replacement_stock_available": 5
    },
    "ORD-5672": {
        "order_id": "ORD-5672",
        "customer_id": "CUST-118",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=22)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=18)).strftime("%Y-%m-%d"),
        "product_name": "AlpinePro Vibram Grip Trail Running Shoes (Size 43)",
        "sku": "APP-SHOE-043",
        "category": "Apparel",
        "price": 12500.00,
        "tax": 2250.00,
        "shipping_fee": 0.00,
        "total_paid": 14750.00,
        "payment_method": "Credit Card (Mastercard ending 1209)",
        "order_status": "DELIVERED",
        "carrier": "BlueDart Express",
        "tracking_number": "TRK-BD-5672",
        "replacement_stock_available": 14
    },
    "ORD-3456": {
        "order_id": "ORD-3456",
        "customer_id": "CUST-119",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=25)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=20)).strftime("%Y-%m-%d"),
        "product_name": "SmartBrew Precision Thermal Carafe Coffee Maker",
        "sku": "HOME-COF-201",
        "category": "Home & Kitchen",
        "price": 9999.00,
        "tax": 1799.82,
        "shipping_fee": 0.00,
        "total_paid": 11798.82,
        "payment_method": "UPI (PhonePe)",
        "order_status": "DELIVERED",
        "carrier": "Delhivery Prime",
        "tracking_number": "TRK-DLV-3456",
        "replacement_stock_available": 9
    },
    "ORD-8901": {
        "order_id": "ORD-8901",
        "customer_id": "CUST-120",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=5)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=3)).strftime("%Y-%m-%d"),
        "product_name": "OmniHub Thunderbolt 4 12-Port Dual 4K Display Dock",
        "sku": "COMP-DCK-800",
        "category": "Computing",
        "price": 21990.00,
        "tax": 3958.20,
        "shipping_fee": 0.00,
        "total_paid": 25948.20,
        "payment_method": "Credit Card (Axis Flipkart ending 8031)",
        "order_status": "DELIVERED",
        "carrier": "DTDC Air Cargo",
        "tracking_number": "TRK-DTDC-8901",
        "replacement_stock_available": 20
    },
    "ORD-4312": {
        "order_id": "ORD-4312",
        "customer_id": "CUST-121",
        "order_date": (CURRENT_TIMESTAMP - timedelta(days=14)).strftime("%Y-%m-%d"),
        "delivery_date": (CURRENT_TIMESTAMP - timedelta(days=10)).strftime("%Y-%m-%d"),
        "product_name": "PureRadiance Bio-Active Vitamin C Antioxidant Mist",
        "sku": "BEAUTY-MST-101",
        "category": "Beauty & Personal Care",
        "price": 4500.00,
        "tax": 810.00,
        "shipping_fee": 0.00,
        "total_paid": 5310.00,
        "payment_method": "UPI (Paytm)",
        "order_status": "DELIVERED",
        "carrier": "BlueDart Express",
        "tracking_number": "TRK-BD-4312",
        "replacement_stock_available": 30
    }
}

# 4. Logistics & Carrier Tracking Events (Indian Hubs: Bhiwandi, Nagpur, Gurugram, Bengaluru, etc.)
TRACKING_DATA: Dict[str, Dict[str, Any]] = {
    "TRK-BD-9821": {
        "tracking_number": "TRK-BD-9821",
        "carrier": "BlueDart Express",
        "status": "DELIVERED",
        "signed_by": "A. Sharma",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=2)).strftime("%Y-%m-%d 14:22:00"),
        "checkpoints": [
            {"time": "Day -5 10:00", "location": "Fulfillment Hub, Bhiwandi, MH", "event": "Shipment picked up"},
            {"time": "Day -3 18:45", "location": "Sort Facility, Gurugram, HR", "event": "Departed transit hub"},
            {"time": "Day -2 08:30", "location": "Local Depot, Connaught Place, New Delhi", "event": "Out for delivery"},
            {"time": "Day -2 14:22", "location": "New Delhi, DL", "event": "Delivered - Handed to customer"}
        ]
    },
    "TRK-DLV-7742": {
        "tracking_number": "TRK-DLV-7742",
        "carrier": "Delhivery Prime",
        "status": "DELAYED_IN_TRANSIT",
        "signed_by": None,
        "delivery_timestamp": None,
        "checkpoints": [
            {"time": "Day -10 11:30", "location": "Distribution Center, Bhiwandi, MH", "event": "Package processed"},
            {"time": "Day -8 04:15", "location": "Central Freight Hub, Nagpur, MH", "event": "In transit to destination hub"},
            {"time": "Day -6 19:00", "location": "Nagpur Central Freight Hub, MH", "event": "Weather delay / Mechanical transport issue reported"},
            {"time": "Day -1 10:00", "location": "Nagpur Central Freight Hub, MH", "event": "Tracking stall: No movement scan for >120 hours"}
        ]
    },
    "TRK-BD-5190": {
        "tracking_number": "TRK-BD-5190",
        "carrier": "BlueDart Express",
        "status": "DELIVERED",
        "signed_by": "M. Iyer",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=38)).strftime("%Y-%m-%d 11:15:00"),
        "checkpoints": [
            {"time": "Day -41 09:00", "location": "Skincare Lab Hub, Bengaluru, KA", "event": "Dispatched from origin fulfillment center"},
            {"time": "Day -40 18:30", "location": "Whitefield Linehaul Sorting Depot, Bengaluru", "event": "Sorted & scanned onto regional linehaul transport"},
            {"time": "Day -38 08:30", "location": "East Bengaluru Delivery Hub", "event": "Loaded on courier delivery van - Out for delivery"},
            {"time": "Day -38 11:15", "location": "Customer Residence, Indiranagar, Bengaluru", "event": "Delivered successfully (Signed by M. Iyer)"}
        ]
    },
    "TRK-BD-3319": {
        "tracking_number": "TRK-BD-3319",
        "carrier": "BlueDart Apex Express",
        "status": "DELIVERED",
        "signed_by": "V. Verma (Direct Biometric Signature Verified)",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=1)).strftime("%Y-%m-%d 16:40:00"),
        "checkpoints": [
            {"time": "Day -3 15:00", "location": "Tech Logistics Hub, Navi Mumbai, MH", "event": "Origin scan (Weight: 4.8 kg recorded)"},
            {"time": "Day -2 22:30", "location": "Regional Hub, Gurugram, HR", "event": "En route via express air cargo"},
            {"time": "Day -1 09:00", "location": "South Delhi Local Depot", "event": "Loaded on security delivery van"},
            {"time": "Day -1 16:40", "location": "South Delhi, DL", "event": "Delivered: In-person biometric signature captured"}
        ]
    },
    "TRK-SFX-6401": {
        "tracking_number": "TRK-SFX-6401",
        "carrier": "Shadowfax VIP Priority",
        "status": "DELIVERED",
        "signed_by": "Dr. A. Sen (VIP Concierge Reception)",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=3)).strftime("%Y-%m-%d 13:05:00"),
        "checkpoints": [
            {"time": "Day -6 14:00", "location": "Customs Air Hub, Chhatrapati Shivaji Int'l Airport", "event": "Import release cleared & priority barcode attached"},
            {"time": "Day -5 20:00", "location": "Western Express Cargo Gateway, Mumbai", "event": "Processed through secured high-value transit locker"},
            {"time": "Day -4 08:30", "location": "South Mumbai VIP Hub, Nariman Point", "event": "Assigned to dedicated VIP concierge dispatch van"},
            {"time": "Day -3 13:05", "location": "Malabar Hill, Mumbai, MH", "event": "Delivered to private concierge desk (Dr. A. Sen)"}
        ]
    },
    "TRK-DLV-1102": {
        "tracking_number": "TRK-DLV-1102",
        "carrier": "Delhivery Prime",
        "status": "DELIVERED",
        "signed_by": "A. Patel (Direct Signature Verified)",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=4)).strftime("%Y-%m-%d 15:10:00"),
        "checkpoints": [
            {"time": "Day -6 09:00", "location": "Regional Electronics Hub, Hyderabad, TG", "event": "Shipment picked up & origin manifest barcode scanned"},
            {"time": "Day -5 18:30", "location": "Shamshabad Freight Sorting Depot, Hyderabad", "event": "Linehaul container sorted and routed to local center"},
            {"time": "Day -4 08:30", "location": "Gachibowli Local Dispatch Station, Hyderabad", "event": "Out for delivery via express courier van (Driver assigned)"},
            {"time": "Day -4 15:10", "location": "Gachibowli, Hyderabad", "event": "Delivered: In-person recipient handover signed by A. Patel"}
        ]
    },
    "TRK-DTDC-2245": {
        "tracking_number": "TRK-DTDC-2245",
        "carrier": "DTDC Air Cargo",
        "status": "DELIVERED",
        "signed_by": "S. Reddy",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=12)).strftime("%Y-%m-%d 11:30:00"),
        "checkpoints": [
            {"time": "Day -15 14:00", "location": "Apparel Sort Facility, Tiruppur, TN", "event": "Consignment packed and origin manifest logged"},
            {"time": "Day -14 06:30", "location": "Coimbatore Express Air Cargo Terminal, TN", "event": "Departed transit airport via linehaul cargo flight"},
            {"time": "Day -12 08:15", "location": "Hyderabad Central Sorting Terminal, TG", "event": "Loaded on courier delivery van - Out for delivery"},
            {"time": "Day -12 11:30", "location": "Banjara Hills, Hyderabad", "event": "Delivered successfully to customer (Signed by S. Reddy)"}
        ]
    },
    "TRK-DLV-8830": {
        "tracking_number": "TRK-DLV-8830",
        "carrier": "Delhivery Prime",
        "status": "DELIVERED",
        "signed_by": "M. Agarwal",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=22)).strftime("%Y-%m-%d 14:00:00"),
        "checkpoints": [
            {"time": "Day -25 10:00", "location": "Home Appliance Depot, Pune, MH", "event": "Dispatched from central manufacturing warehouse"},
            {"time": "Day -24 19:15", "location": "Chakan Automated Linehaul Hub, Pune", "event": "Processed via automated conveyor sort scanner"},
            {"time": "Day -22 08:45", "location": "Kothrud Local Dispatch Depot, Pune", "event": "Out for delivery on heavy-appliance cargo van"},
            {"time": "Day -22 14:00", "location": "Kothrud, Pune", "event": "Delivered and unboxed at residence (Signed by M. Agarwal)"}
        ]
    },
    "TRK-BD-4491": {
        "tracking_number": "TRK-BD-4491",
        "carrier": "BlueDart Express",
        "status": "DELAYED_IN_TRANSIT",
        "signed_by": None,
        "delivery_timestamp": None,
        "checkpoints": [
            {"time": "Day -8 11:00", "location": "Tech Hub, Bengaluru, KA", "event": "Shipment picked up & origin manifest barcode scanned"},
            {"time": "Day -7 18:30", "location": "Southern Linehaul Freight Terminal, Bengaluru", "event": "Departed regional facility via inter-state container"},
            {"time": "Day -5 20:00", "location": "Nagpur Central Freight Hub, MH", "event": "Sorting stalled: Adverse weather / road connection disruption"},
            {"time": "Day -1 10:00", "location": "Nagpur Central Freight Hub, MH", "event": "Transit exception: Automated tracer inquiry open with hub manager"}
        ]
    },
    "TRK-BD-7123": {
        "tracking_number": "TRK-BD-7123",
        "carrier": "BlueDart Express",
        "status": "DELIVERED",
        "signed_by": "D. Joshi",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=5)).strftime("%Y-%m-%d 16:15:00"),
        "checkpoints": [
            {"time": "Day -7 08:30", "location": "Cosmetic Fulfillment Center, Ahmedabad, GJ", "event": "Dispatched from climate-controlled warehouse"},
            {"time": "Day -6 17:45", "location": "Sanand Logistics Gateway Hub, GJ", "event": "Sorted and transferred to municipal delivery network"},
            {"time": "Day -5 09:00", "location": "Navrangpura Local Delivery Station, Ahmedabad", "event": "Out for delivery on courier vehicle"},
            {"time": "Day -5 16:15", "location": "Navrangpura, Ahmedabad", "event": "Delivered: Biometric proof-of-delivery signed by D. Joshi"}
        ]
    },
    "TRK-DLV-9054": {
        "tracking_number": "TRK-DLV-9054",
        "carrier": "Delhivery Prime",
        "status": "DELIVERED",
        "signed_by": "A. Sharma",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=1)).strftime("%Y-%m-%d 10:45:00"),
        "checkpoints": [
            {"time": "Day -3 12:00", "location": "Audio Fulfillment Hub, Noida, UP", "event": "Shipped from national audio warehouse"},
            {"time": "Day -2 20:15", "location": "Okhla Express Logistics Terminal, Delhi NCR", "event": "Processed through linehaul automated sorting belt"},
            {"time": "Day -1 08:30", "location": "South Delhi Local Delivery Center", "event": "Loaded on courier delivery van - Out for delivery"},
            {"time": "Day -1 10:45", "location": "Vasant Kunj, New Delhi", "event": "Delivered to recipient address (Signed by A. Sharma)"}
        ]
    },
    "TRK-DTDC-3788": {
        "tracking_number": "TRK-DTDC-3788",
        "carrier": "DTDC Air Cargo",
        "status": "DELIVERED",
        "signed_by": "R. Mehta",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=3)).strftime("%Y-%m-%d 17:20:00"),
        "checkpoints": [
            {"time": "Day -5 09:30", "location": "Memory Storage Center, Chennai, TN", "event": "Consignment packed and origin scan recorded"},
            {"time": "Day -4 21:00", "location": "Western Air Cargo Terminal, Mumbai, MH", "event": "Arrived at destination air cargo terminal"},
            {"time": "Day -3 08:45", "location": "Bandra Local Delivery Hub, Mumbai", "event": "Out for delivery on express delivery vehicle"},
            {"time": "Day -3 17:20", "location": "Bandra West, Mumbai", "event": "Delivered: Recipient sign-off recorded by R. Mehta"}
        ]
    },
    "TRK-SFX-6210": {
        "tracking_number": "TRK-SFX-6210",
        "carrier": "Shadowfax VIP Priority",
        "status": "DELIVERED",
        "signed_by": "Dr. A. Sen",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=2)).strftime("%Y-%m-%d 12:10:00"),
        "checkpoints": [
            {"time": "Day -4 14:00", "location": "Mumbai Airport Air Cargo", "event": "VIP consignment cleared & priority manifest printed"},
            {"time": "Day -3 18:00", "location": "South Mumbai Concierge Hub, Nariman Point", "event": "Secured in high-priority distribution locker"},
            {"time": "Day -2 09:30", "location": "South Mumbai Dispatch Depot", "event": "Out for delivery via white-glove courier van"},
            {"time": "Day -2 12:10", "location": "Cuffe Parade, Mumbai", "event": "Delivered to private concierge (Signed by Dr. A. Sen)"}
        ]
    },
    "TRK-DLV-8432": {
        "tracking_number": "TRK-DLV-8432",
        "carrier": "Delhivery Prime",
        "status": "DELIVERED",
        "signed_by": "P. Banerjee",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=8)).strftime("%Y-%m-%d 13:40:00"),
        "checkpoints": [
            {"time": "Day -11 08:00", "location": "Culinary Logistics Hub, Kolkata, WB", "event": "Dispatched from cookware central distribution center"},
            {"time": "Day -10 17:30", "location": "Dankuni Distribution Center, WB", "event": "Processed through linehaul sorting scanners"},
            {"time": "Day -8 08:45", "location": "Salt Lake Local Delivery Depot, Kolkata", "event": "Out for delivery on courier vehicle"},
            {"time": "Day -8 13:40", "location": "Salt Lake Sector V, Kolkata", "event": "Delivered: Handed to recipient (Signed by P. Banerjee)"}
        ]
    },
    "TRK-DTDC-5509": {
        "tracking_number": "TRK-DTDC-5509",
        "carrier": "DTDC Air Cargo",
        "status": "DELIVERED",
        "signed_by": "V. Verma (Direct Signature Captured)",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=1)).strftime("%Y-%m-%d 15:50:00"),
        "checkpoints": [
            {"time": "Day -2 10:00", "location": "Camera Warehouse, Gurugram, HR", "event": "Origin scan (Gross Weight: 0.9kg recorded)"},
            {"time": "Day -2 21:30", "location": "Dhaula Kuan Express Gateway, New Delhi", "event": "Transferred to municipal delivery network"},
            {"time": "Day -1 09:00", "location": "Rohini Local Distribution Center, Delhi", "event": "Loaded on courier delivery van - Out for delivery"},
            {"time": "Day -1 15:50", "location": "Rohini, Delhi", "event": "Delivered: Verified biometric signature of V. Verma"}
        ]
    },
    "TRK-BD-1290": {
        "tracking_number": "TRK-BD-1290",
        "carrier": "BlueDart Express",
        "status": "DELIVERED",
        "signed_by": "M. Kulkarni",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=3)).strftime("%Y-%m-%d 11:20:00"),
        "checkpoints": [
            {"time": "Day -5 08:00", "location": "Wearables Fulfillment Hub, Pune, MH", "event": "Picked up and origin manifest logged"},
            {"time": "Day -4 16:45", "location": "Hadapsar Linehaul Sort Facility, Pune", "event": "Linehaul sort completed & departed on local transfer"},
            {"time": "Day -3 08:15", "location": "Shivajinagar Local Station, Pune", "event": "Out for delivery on courier delivery van"},
            {"time": "Day -3 11:20", "location": "Shivajinagar, Pune", "event": "Delivered to customer address (Signed by M. Kulkarni)"}
        ]
    },
    "TRK-SFX-4821": {
        "tracking_number": "TRK-SFX-4821",
        "carrier": "Shadowfax VIP Priority",
        "status": "DELIVERED",
        "signed_by": "S. Deshmukh",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=5)).strftime("%Y-%m-%d 14:15:00"),
        "checkpoints": [
            {"time": "Day -7 11:00", "location": "Luxury Apparel Hub, Chandigarh, PB", "event": "Dispatched from high-fashion fulfillment center"},
            {"time": "Day -6 19:30", "location": "Mohali Linehaul Terminal, PB", "event": "Processed via priority laser sorting scanner"},
            {"time": "Day -5 09:00", "location": "Chandigarh Sector Delivery Depot", "event": "Out for delivery via priority courier vehicle"},
            {"time": "Day -5 14:15", "location": "Sector 9, Chandigarh", "event": "Delivered to recipient residence (Signed by S. Deshmukh)"}
        ]
    },
    "TRK-DLV-6734": {
        "tracking_number": "TRK-DLV-6734",
        "carrier": "Delhivery Prime",
        "status": "DELIVERED",
        "signed_by": "D. Gupta",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=6)).strftime("%Y-%m-%d 16:30:00"),
        "checkpoints": [
            {"time": "Day -8 13:00", "location": "Kitchen Depot Hub, Jaipur, RJ", "event": "Consignment packed and shipped from regional hub"},
            {"time": "Day -7 20:00", "location": "Sitapura Logistics Terminal, Jaipur", "event": "Linehaul container sorted and routed to local center"},
            {"time": "Day -6 08:30", "location": "Malviya Nagar Delivery Center, Jaipur", "event": "Loaded on courier delivery van - Out for delivery"},
            {"time": "Day -6 16:30", "location": "Malviya Nagar, Jaipur", "event": "Delivered: Handed over in person (Signed by D. Gupta)"}
        ]
    },
    "TRK-BD-7890": {
        "tracking_number": "TRK-BD-7890",
        "carrier": "BlueDart Express",
        "status": "DELIVERED",
        "signed_by": "P. Nair",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=2)).strftime("%Y-%m-%d 13:10:00"),
        "checkpoints": [
            {"time": "Day -4 09:30", "location": "Electronics Park Hub, Kochi, KL", "event": "Dispatched from technology distribution center"},
            {"time": "Day -3 18:00", "location": "Ernakulam Sort Depot, KL", "event": "Sorted and transferred to local delivery station"},
            {"time": "Day -2 08:45", "location": "Kakkanad Local Delivery Station, Kochi", "event": "Out for delivery on courier vehicle"},
            {"time": "Day -2 13:10", "location": "Kakkanad, Kochi", "event": "Delivered to recipient address (Signed by P. Nair)"}
        ]
    },
    "TRK-DLV-2341": {
        "tracking_number": "TRK-DLV-2341",
        "carrier": "Delhivery Prime",
        "status": "DELIVERED",
        "signed_by": "S. Malhotra",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=4)).strftime("%Y-%m-%d 10:50:00"),
        "checkpoints": [
            {"time": "Day -6 11:00", "location": "Skincare Lab Logistics, Lucknow, UP", "event": "Processed at origin cosmetics warehouse"},
            {"time": "Day -5 19:15", "location": "Transport Nagar Sort Hub, Lucknow", "event": "Departed sorting facility on local linehaul van"},
            {"time": "Day -4 08:30", "location": "Gomti Nagar Local Depot, Lucknow", "event": "Out for delivery on courier dispatch van"},
            {"time": "Day -4 10:50", "location": "Gomti Nagar, Lucknow", "event": "Delivered to customer residence (Signed by S. Malhotra)"}
        ]
    },
    "TRK-DTDC-9128": {
        "tracking_number": "TRK-DTDC-9128",
        "carrier": "DTDC Air Cargo",
        "status": "DELAYED_IN_TRANSIT",
        "signed_by": None,
        "delivery_timestamp": None,
        "checkpoints": [
            {"time": "Day -9 15:00", "location": "Audio Factory, Chennai, TN", "event": "Origin scan & freight manifest registered"},
            {"time": "Day -7 02:30", "location": "Central Linehaul Corridor Hub, Vijayawada, AP", "event": "En route via express linehaul container"},
            {"time": "Day -5 04:00", "location": "Nagpur Freight Depot, MH", "event": "Severe highway stall / weather disruption reported"},
            {"time": "Day -1 11:00", "location": "Nagpur Freight Depot, MH", "event": "Delayed in transit: Logistics escalation ticket active"}
        ]
    },
    "TRK-BD-5672": {
        "tracking_number": "TRK-BD-5672",
        "carrier": "BlueDart Express",
        "status": "DELIVERED",
        "signed_by": "L. Singhania",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=18)).strftime("%Y-%m-%d 12:40:00"),
        "checkpoints": [
            {"time": "Day -21 10:00", "location": "Footwear Hub, Agra, UP", "event": "Dispatched from regional footwear warehouse"},
            {"time": "Day -20 18:30", "location": "Kanpur Transit Cargo Terminal, UP", "event": "Transferred to eastern linehaul container"},
            {"time": "Day -18 08:15", "location": "South Kolkata Delivery Hub", "event": "Out for delivery on courier vehicle"},
            {"time": "Day -18 12:40", "location": "Alipore, Kolkata", "event": "Delivered: Physical signature recorded by L. Singhania"}
        ]
    },
    "TRK-DLV-3456": {
        "tracking_number": "TRK-DLV-3456",
        "carrier": "Delhivery Prime",
        "status": "DELIVERED",
        "signed_by": "E. Mukherjee",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=20)).strftime("%Y-%m-%d 15:25:00"),
        "checkpoints": [
            {"time": "Day -24 09:00", "location": "Appliance Center, Surat, GJ", "event": "Dispatched from consumer appliance hub"},
            {"time": "Day -22 22:00", "location": "Eastern India Gateway Hub, Howrah, WB", "event": "Inbound container sorted & cleared"},
            {"time": "Day -20 09:00", "location": "Ballygunge Local Depot, Kolkata", "event": "Loaded on courier delivery van - Out for delivery"},
            {"time": "Day -20 15:25", "location": "Ballygunge, Kolkata", "event": "Delivered: Biometric POD signed by E. Mukherjee"}
        ]
    },
    "TRK-DTDC-8901": {
        "tracking_number": "TRK-DTDC-8901",
        "carrier": "DTDC Air Cargo",
        "status": "DELIVERED",
        "signed_by": "K. Bhatia",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=3)).strftime("%Y-%m-%d 14:05:00"),
        "checkpoints": [
            {"time": "Day -5 14:00", "location": "Tech Hub, Electronic City Bengaluru", "event": "Shipped from hardware logistics depot"},
            {"time": "Day -4 20:00", "location": "Outer Ring Road Sort Facility, Bengaluru", "event": "Automated sorting scan complete"},
            {"time": "Day -3 08:30", "location": "Whitefield Delivery Station, Bengaluru", "event": "Out for delivery on courier van"},
            {"time": "Day -3 14:05", "location": "Whitefield, Bengaluru", "event": "Delivered: Handed to customer (Signed by K. Bhatia)"}
        ]
    },
    "TRK-BD-4312": {
        "tracking_number": "TRK-BD-4312",
        "carrier": "BlueDart Express",
        "status": "DELIVERED",
        "signed_by": "F. Siddiqui",
        "delivery_timestamp": (CURRENT_TIMESTAMP - timedelta(days=10)).strftime("%Y-%m-%d 11:35:00"),
        "checkpoints": [
            {"time": "Day -13 09:00", "location": "Beauty Fulfillment, Mumbai, MH", "event": "Dispatched from cosmetics fulfillment hub"},
            {"time": "Day -11 19:00", "location": "Begumpet Logistics Depot, Hyderabad", "event": "Arrived at destination transit terminal"},
            {"time": "Day -10 08:45", "location": "Banjara Hills Local Station, Hyderabad", "event": "Out for delivery on courier delivery van"},
            {"time": "Day -10 11:35", "location": "Banjara Hills, Hyderabad", "event": "Delivered: Verified signature captured by F. Siddiqui"}
        ]
    }
}

# 5. Pre-Loaded Realistic Benchmark Customer Complaints (Indian Localization & Rupee)
BENCHMARK_SCENARIOS = [
    {
        "id": "scenario_1",
        "title": "Scenario 1: Defective Product (Auto-Approved Return & Replacement)",
        "order_id": "ORD-9821",
        "customer_id": "CUST-101",
        "complaint_text": (
            "Hello Customer Support, I received order #ORD-9821 (AcousticPro Studio Noise-Cancelling Headphones) two days ago. "
            "Upon unboxing and connecting them to my audio interface, there is a persistent buzzing static in the right ear cup that cuts out audio completely. "
            "I tested with multiple auxiliary cables and across two different computers to confirm it is a hardware defect. "
            "The left ear cup functions normally, but the right audio channel fails repeatedly under any active sound output. "
            "As an audio professional with tight project deadlines this week, I am extremely disappointed by this out-of-box failure. "
            "Since this purchase is well within the 7-day return window, please issue an immediate prepaid replacement or a full refund. "
            "I have repacked all cables, adapters, and the retail packaging ready for immediate courier pickup."
        ),
        "expected_category": "Damaged / Defective Goods",
        "expected_urgency": "High",
        "expected_decision": "AUTO_RESOLVED_REPLACEMENT",
        "description": "Standard customer reporting defective audio within the 7-day electronics return window. Low risk. Auto-approve replacement with free reverse pickup label."
    },
    {
        "id": "scenario_2",
        "title": "Scenario 2: Logistics Stall & Delay (Carrier Investigation + ₹500 Credit)",
        "order_id": "ORD-7742",
        "customer_id": "CUST-102",
        "complaint_text": (
            "Dear Support Team, I am writing regarding order #ORD-7742 for the BaristaMaster Compact Espresso Machine placed 10 days ago. "
            "The guaranteed delivery date was 4 days ago, but the tracking status has remained completely frozen at the Nagpur central transit hub for over 120 hours with only a vague 'weather delay' tag. "
            "This equipment is urgently needed for our café opening in Pune this weekend, and the lack of communication is unacceptable. "
            "Where is my package, and when will it arrive? If it is lost or damaged in transit, please open an investigation immediately and provide delay compensation or a full refund. "
            "Our opening event cannot be rescheduled, so please contact Delhivery dispatch directly and expedite a trace today."
        ),
        "expected_category": "Logistics & Delivery Delay",
        "expected_urgency": "Critical",
        "expected_decision": "CARRIER_INVESTIGATION_COMPENSATION",
        "description": "Shipment stalled in transit past promised delivery date. Auto-triggers carrier trace ticket and offers ₹500 delay compensation + expedited priority delivery alert."
    },
    {
        "id": "scenario_3",
        "title": "Scenario 3: Policy-Ineligible Return Request (Polite Refusal + Goodwill Discount)",
        "order_id": "ORD-5190",
        "customer_id": "CUST-103",
        "complaint_text": (
            "Hello Customer Service, I am contacting you regarding order #ORD-5190 for the GlowBotanica Peptide Anti-Aging Serum Set delivered 38 days ago. "
            "I finally opened the outer box over the weekend to try the product, but after applying it once, I found the botanical fragrance irritating to my sensitive skin. "
            "The other bottles in the set remain completely unused and sealed in their original boxes. "
            "Since the package is virtually full, I would like to return the set for a full refund back to my PhonePe UPI account. Please email me the prepaid return label and shipping instructions. "
            "I understand there are product guidelines, but I hope your team can accommodate a flexible store credit solution."
        ),
        "expected_category": "Return & Refund Request",
        "expected_urgency": "Medium",
        "expected_decision": "POLICY_REFUSAL_GOODWILL_COUPON",
        "description": "Cosmetic item delivered 38 days ago. Exceeds return window AND violates health/hygiene non-returnable policy. Politely refuses refund, explains hygiene policy, and grants 15% goodwill store credit."
    },
    {
        "id": "scenario_4",
        "title": "Scenario 4: ₹1.76L Laptop Stolen Claim (Critic Flags Fraud -> Escalated to Supervisor)",
        "order_id": "ORD-3319",
        "customer_id": "CUST-104",
        "complaint_text": (
            "URGENT ATTENTION REQUIRED: I am furious and filing an immediate complaint regarding order #ORD-3319 for the TitanV Pro Gaming Laptop (₹1,76,988 total). "
            "The carrier marked the package delivered yesterday afternoon, but when I picked up the parcel from the doorstep, the outer box was unsealed and completely EMPTY! "
            "The delivery driver stole the laptop! This is blatant theft and unacceptable for an expensive asset. "
            "I demand an immediate full refund of ₹1,76,988 back to my HDFC credit card right now, or I will file a formal police report and instruct my lawyer to initiate fraud chargeback proceedings immediately! "
            "I have porch surveillance footage showing the package was lightweight on arrival and expect manager resolution today."
        ),
        "expected_category": "Stolen / Missing Package Claim",
        "expected_urgency": "Critical",
        "expected_decision": "ESCALATED_TO_HUMAN_SUPERVISOR",
        "description": "High-value ₹1,76,000+ item. Customer Vikram Verma has a 66.7% return rate and 3 prior stolen claims. Carrier logged 4.8kg package weight and verified signature. Critic Agent flags synthetic fraud risk (Score 88/100) and halts auto-refund, escalating to Senior Fraud Prevention Supervisor."
    },
    {
        "id": "scenario_5",
        "title": "Scenario 5: VIP Platinum Customer White-Glove Resolution (Wrong Size Apparel)",
        "order_id": "ORD-6401",
        "customer_id": "CUST-105",
        "complaint_text": (
            "Good morning Concierge Desk, I recently received my order #ORD-6401 for the Venezia Handcrafted Italian Leather Chelsea Boots. "
            "When I unboxed them today, I discovered that the warehouse sent me the wrong size — the shoes inside are Size 40 instead of Size 42. "
            "I have an important keynote presentation at an international trade conference in Mumbai this upcoming weekend and urgently require the proper Size 42 boots. "
            "As a longtime Platinum VIP member, could you please dispatch an expedited courier exchange with the correct Size 42 pair to my South Mumbai residence? "
            "I have the wrong pair sealed in the original dust bag ready to hand directly to the swap courier."
        ),
        "expected_category": "Wrong Item Shipped",
        "expected_urgency": "High",
        "expected_decision": "VIP_EXPEDITED_EXCHANGE",
        "description": "Warehouse packing error on a Platinum VIP customer (₹4,75,000+ LTV). Dispatches immediate courier exchange without waiting for return receipt, waives return fee, and assigns personal concierge follow-up."
    }
]

# 6. Realistic Inbound Complaint Templates for All 25 Orders
ORDER_SAMPLE_COMPLAINTS: Dict[str, str] = {
    "ORD-9821": (
        "Hello Customer Support, I received order #ORD-9821 (AcousticPro Studio Noise-Cancelling Headphones) two days ago. "
        "Upon unboxing and connecting them to my audio interface, there is a persistent buzzing static in the right ear cup that cuts out audio completely. "
        "I tested with multiple auxiliary cables and across two different computers to confirm it is a hardware defect. "
        "The left ear cup functions normally, but the right audio channel fails repeatedly under any active sound output. "
        "As an audio professional with tight project deadlines this week, I am extremely disappointed by this out-of-box failure. "
        "Since this purchase is well within the 7-day return window, please issue an immediate prepaid replacement or a full refund. "
        "I have repacked all cables, adapters, and the retail packaging ready for immediate courier pickup."
    ),
    "ORD-7742": (
        "Dear Support Team, I am writing regarding order #ORD-7742 for the BaristaMaster Compact Espresso Machine placed 10 days ago. "
        "The guaranteed delivery date was 4 days ago, but the tracking status has remained completely frozen at the Nagpur central transit hub for over 120 hours with only a vague 'weather delay' tag. "
        "This equipment is urgently needed for our café opening in Pune this weekend, and the lack of communication is unacceptable. "
        "Where is my package, and when will it arrive? If it is lost or damaged in transit, please open an investigation immediately and provide delay compensation or a full refund."
    ),
    "ORD-5190": (
        "Hello Customer Service, I am contacting you regarding order #ORD-5190 for the GlowBotanica Peptide Anti-Aging Serum Set delivered 38 days ago. "
        "I finally opened the outer box over the weekend to try the product, but after applying it once, I found the botanical fragrance irritating to my sensitive skin. "
        "The other bottles in the set remain completely unused and sealed in their original boxes. "
        "Since the package is virtually full, I would like to return the set for a full refund back to my PhonePe UPI account. Please email me the prepaid return label and shipping instructions."
    ),
    "ORD-3319": (
        "URGENT ATTENTION REQUIRED: I am furious and filing an immediate complaint regarding order #ORD-3319 for the TitanV Pro Gaming Laptop (₹1,76,988 total). "
        "The carrier marked the package delivered yesterday afternoon, but when I picked up the parcel from the doorstep, the outer box was unsealed and completely EMPTY! "
        "The delivery driver stole the laptop! This is blatant theft and unacceptable for an expensive asset. "
        "I demand an immediate full refund of ₹1,76,988 back to my HDFC credit card right now, or I will file a formal police report and instruct my lawyer to initiate fraud chargeback proceedings immediately!"
    ),
    "ORD-6401": (
        "Good morning Concierge Desk, I recently received my order #ORD-6401 for the Venezia Handcrafted Italian Leather Chelsea Boots. "
        "When I unboxed them today, I discovered that the warehouse sent me the wrong size — the shoes inside are Size 40 instead of Size 42. "
        "I have an important keynote presentation at an international trade conference in Mumbai this upcoming weekend and urgently require the proper Size 42 boots. "
        "As a longtime Platinum VIP member, could you please dispatch an expedited courier exchange with the correct Size 42 pair to my South Mumbai residence?"
    ),
    "ORD-1102": (
        "Hello Technical Support, I received order #ORD-1102 (ProView 32-inch 4K HDR IPS Designer Monitor) four days ago. "
        "After setting it up with DisplayPort, I noticed a prominent cluster of bright red dead pixels directly in the center of the display. "
        "For professional color grading and video production, this defect makes the monitor completely unusable. "
        "I have repackaged the unit in its original styrofoam and box. As this is within the 7-day electronics return window, please issue an immediate RMA return authorization and dispatch a replacement unit without display panel defects."
    ),
    "ORD-2245": (
        "Hi Customer Service, I ordered the SummitShield Waterproof Gore-Tex Alpine Parka (Order #ORD-2245) which arrived 12 days ago. "
        "While the weatherproofing is great, the main front two-way zipper continuously catches and jams on the interior storm flap fabric, making it very difficult to zip up or down. "
        "Since apparel items have a 30-day return policy and the tags are still attached, I would like to return this jacket for an exchange or refund. "
        "Please send me a prepaid return shipping barcode so I can hand it to the courier pickup executive."
    ),
    "ORD-8830": (
        "Hello Support, I am reaching out regarding my RoboClean Smart Laser Mapping Vacuum (Order #ORD-8830) delivered 22 days ago. "
        "The vacuum recently stopped suctioning and continuously beeps with error code E4 on the docking station. "
        "I have cleared the roller brushes and reset the sensors according to the troubleshooting manual, but the issue persists. "
        "Since Home & Kitchen has a 15-day return policy, I understand I may be outside the standard refund window, but I would like to know what warranty repair, replacement parts, or manufacturer service options are available."
    ),
    "ORD-4491": (
        "Dear Logistics Support, I placed order #ORD-4491 for an ErgoType Split Wireless Mechanical Keyboard 8 days ago. "
        "The scheduled delivery date was 3 days ago, but the tracking status has shown 'sorting stalled / flight delay' in Nagpur with zero status updates since. "
        "I work remotely and desperately need this ergonomic keyboard to alleviate severe wrist strain. "
        "Could you please check with BlueDart to locate the package and provide an updated delivery estimate? If the shipment is lost in transit, please send a replacement unit."
    ),
    "ORD-7123": (
        "Hello, I ordered the AuraGlow Botanical Hair Repair Essential Oils (Order #ORD-7123) 5 days ago and it was delivered over the weekend. "
        "I ended up receiving a similar ayurvedic hair treatment gift pack from a family member, so this bottle is completely unopened and still sealed in its original shrink-wrap. "
        "Since I haven't used the product at all, I would like to return it and receive a refund to my Google Pay UPI account. "
        "Please provide me with the return instructions and mailing address."
    ),
    "ORD-9054": (
        "Hi Support Team, I received the PulseAir Sport Earbuds (Order #ORD-9054) yesterday afternoon. "
        "I plugged the charging case into an official USB-C wall charger overnight, but the battery indicator continuously blinks red and neither earbud will charge or power on. "
        "I tested with multiple charging cables and confirmed the battery case itself is defective. "
        "Since this is within the 7-day electronics return period, please process an expedited replacement pair so I have working earbuds for my morning training."
    ),
    "ORD-3788": (
        "Hello Tech Support, I ordered the HyperSpeed 2TB NVMe PCIe Gen4 M.2 SSD (Order #ORD-3788) which arrived 3 days ago. "
        "I installed it into the primary M.2 slot of my motherboard, but the drive is completely undetected in the BIOS and Windows Disk Management across two separate motherboard test benches. "
        "The drive appears to be dead on arrival (DOA). As a computing component covered under the 14-day return policy, please generate an RMA return authorization and dispatch a replacement drive as soon as possible."
    ),
    "ORD-6210": (
        "Good afternoon Concierge Team, I received my SavileRow Bespoke Merino Wool Long Trench Coat (Order #ORD-6210) two days ago. "
        "The craftsmanship and fabric quality are magnificent, but the sleeve length and chest drape feel slightly too roomy for my tailored preferences. "
        "As an active Platinum VIP member with an upcoming business summit in Mumbai, I would love to arrange a white-glove size consultation or exchange for a slightly slimmer fit. "
        "Please let me know how we can coordinate this VIP courier exchange."
    ),
    "ORD-8432": (
        "Hello Customer Care, I received my LeArtisan Enameled Cast Iron Dutch Oven (Order #ORD-8432) 8 days ago. "
        "Upon carefully unboxing it from the bubble wrap, I noticed a distinct half-inch chip in the porcelain enamel coating right along the interior rim, exposing raw cast iron. "
        "Since this poses a food safety and rusting issue during cooking, I cannot use this pot. "
        "As this is within the 15-day Home & Kitchen policy window, please arrange a free reverse pickup and ship a replacement unit in pristine condition."
    ),
    "ORD-5509": (
        "Hello Support, I received order #ORD-5509 for the ClearStream 4K UltraHD Studio Streaming Webcam yesterday. "
        "When I connect the camera to my PC and open OBS Studio, the video feed exhibits severe purple vertical banding and heavy digital noise across the entire optical sensor. "
        "I tried multiple USB 3.0 ports and tested on a Mac and PC with the same result. The sensor is clearly defective. "
        "Please issue an immediate replacement unit under warranty so I can resume my live broadcast schedule."
    ),
    "ORD-1290": (
        "Hi Support Team, I am contacting you regarding order #ORD-1290 (UltraFit GPS Multisport Rugged Smartwatch) received 3 days ago. "
        "Whenever I begin an outdoor running workout and the GPS sensor initiates tracking, the watch freezes and enters a continuous reboot cycle. "
        "I performed a full factory reset and updated the firmware, but the issue persists. "
        "Since this is within the 7-day return window for electronics, please generate a return label and send me a functional replacement smartwatch."
    ),
    "ORD-4821": (
        "Good morning, I received order #ORD-4821 for the NordicPeak 800-Fill Goose Down Parka Coat in Size Medium 5 days ago. "
        "While the thermal insulation and design are extraordinary, the fit runs considerably larger than standard sizing and feels too bulky around the shoulders. "
        "The coat is completely unworn with all manufacturer tags intact. "
        "Could you please provide a complimentary exchange return label for a Size Small so I can swap it before traveling to Himachal?"
    ),
    "ORD-6734": (
        "Hello Customer Service, I ordered the AeroChef Dual-Zone 10-Quart Air Fryer XL (Order #ORD-6734) which was delivered 6 days ago. "
        "When attempting to cook in the left basket, the digital heating element fails to reach any temperature above 150°C regardless of the preset selected, leaving food undercooked. "
        "The right basket works fine, so the left heating thermostat appears defective. "
        "Since it is within the 15-day window, please issue a replacement unit or arrange a replacement basket."
    ),
    "ORD-7890": (
        "Dear Support Desk, I received my QuantumBook 14 3K OLED Laptop (Order #ORD-7890) two days ago. "
        "While the display panel is gorgeous, the physical haptic click mechanism on the right half of the trackpad is completely stiff and unresponsive, requiring excessive downward force to register clicks. "
        "For a premium computing device, this is a clear manufacturing defect. "
        "Please approve an expedited replacement unit and provide a prepaid courier return label for this unit."
    ),
    "ORD-2341": (
        "Hello Customer Care, I purchased the LuminaSilk Ceramide Restorative Night Cream (Order #ORD-2341) delivered 4 days ago. "
        "My dermatologist reviewed the ingredient profile yesterday and advised me to discontinue retinol products due to an acute skin sensitivity flare-up. "
        "The cosmetic jar remains completely sealed in its tamper-evident foil packaging. "
        "Since it has never been opened or exposed, I would like to inquire whether I can return this jar for store credit or refund."
    ),
    "ORD-9128": (
        "Dear Shipping Department, I ordered the SoundWave Studio Powered Subwoofer (Order #ORD-9128) 9 days ago. "
        "The guaranteed delivery window was 3 days ago, but the DTDC tracking number has shown 'severe weather stall in Nagpur' without any departure scans for nearly a week. "
        "I have an audio client recording session booked in Chennai this week and need this subwoofer. "
        "Can you please escalate with the carrier to track down the consignment, or ship an expedited replacement if the unit is stuck indefinitely?"
    ),
    "ORD-5672": (
        "Hi Support, I am writing regarding order #ORD-5672 for the AlpinePro Vibram Grip Trail Running Shoes in Size 43, delivered 18 days ago. "
        "After wearing them around the house on indoor carpet, the rigid heel cup causes painful rubbing against my Achilles tendon and does not fit my foot shape. "
        "The shoes are in mint condition with original packaging. "
        "Since apparel purchases have a 30-day return policy, please send me a prepaid return barcode to initiate a return and refund."
    ),
    "ORD-3456": (
        "Hello Support Team, I am contacting you about our SmartBrew Precision Thermal Carafe Coffee Maker (Order #ORD-3456) delivered 20 days ago. "
        "The internal heating plate stopped warming water yesterday morning, and the brew cycle automatically shuts off after 30 seconds with error code ERR-2. "
        "I understand this is past the initial 15-day store return window for kitchen appliances, but I would like to know how to file a warranty claim or obtain a replacement heating base."
    ),
    "ORD-8901": (
        "Hello Technical Support, I received order #ORD-8901 for the OmniHub Thunderbolt 4 12-Port Docking Station 3 days ago. "
        "When connecting dual 4K monitors to my laptop, the secondary HDMI port fails to output any video signal or handshake with the monitor, although the primary DisplayPort works fine. "
        "I verified with certified HDMI 2.1 cables and updated all Thunderbolt drivers. "
        "Since this is covered under the 14-day computing policy, please issue an RMA and replacement dock."
    ),
    "ORD-4312": (
        "Dear Customer Service, I received my package for order #ORD-4312 (PureRadiance Vitamin C Antioxidant Mist) 10 days ago. "
        "When I unboxed the package, the plastic spray nozzle was cracked in transit and roughly half of the liquid had leaked out into the cardboard packaging. "
        "Since the container arrived physically damaged upon delivery, I would appreciate it if customer support could dispatch an intact replacement bottle or issue a refund for the damaged product."
    )
}
