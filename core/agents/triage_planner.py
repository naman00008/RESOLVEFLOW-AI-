"""
Triage & Planner Agent for ResolveFlow AI
Deconstructs incoming customer messages into structured intent, sentiment,
urgency, order references, and formulates a milestone execution roadmap.
"""

import re
from typing import Dict, Any, List, Optional

class TriagePlannerAgent:
    """
    Planner Agent responsible for triage classification and task decomposition.
    """
    def __init__(self):
        self.role = "Triage & Planner Agent"

    def run(
        self,
        complaint_text: str,
        explicit_order_id: str = "",
        acoustic_telemetry: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyzes the complaint text and produces a triage assessment + execution plan.
        """
        # 1. Order ID extraction
        order_id = explicit_order_id.strip() if explicit_order_id else ""
        if not order_id:
            match = re.search(r"ORD-\d{4}", complaint_text, re.IGNORECASE)
            if match:
                order_id = match.group(0).upper()

        text_lower = complaint_text.lower()

        # 2. Sentiment Analysis
        if any(w in text_lower for w in ["stole", "lawyer", "police", "empty", "furious", "unacceptable", "disaster"]):
            sentiment = "Critical / Hostile"
            urgency = "Critical"
        elif any(w in text_lower for w in ["disappointed", "broken", "static", "delay", "haven't updated", "stalled", "wrong"]):
            sentiment = "Frustrated / Urgent"
            urgency = "High"
        elif any(w in text_lower for w in ["can i return", "changed mind", "don't really like", "wondering"]):
            sentiment = "Inquiring / Mild"
            urgency = "Medium"
        else:
            sentiment = "Neutral"
            urgency = "Medium"

        # 3. Category Classification
        if any(w in text_lower for w in ["empty", "stole", "stolen", "missing box", "didn't receive"]):
            category = "Stolen / Missing Package Claim"
            claim_type = "stolen_missing"
        elif any(w in text_lower for w in ["static", "broken", "defect", "damaged", "cut out", "not working"]):
            category = "Damaged / Defective Goods"
            claim_type = "damaged_defect"
        elif any(w in text_lower for w in ["haven't updated", "weather delay", "where is my", "stalled", "stuck", "tracking hasn't"]):
            category = "Logistics & Delivery Delay"
            claim_type = "shipping_delay"
        elif any(w in text_lower for w in ["wrong size", "wrong item", "sent me", "unboxed them today"]):
            category = "Wrong Item Shipped"
            claim_type = "wrong_item"
        elif any(w in text_lower for w in ["return", "refund", "changed mind", "don't like"]):
            category = "Return & Refund Request"
            claim_type = "discretionary_return"
        else:
            category = "General Order Inquiry"
            claim_type = "general"

        # 4. Milestone Task Planning
        execution_plan: List[Dict[str, str]] = [
            {
                "step": 1,
                "agent": "OMSResearchAgent",
                "milestone": "Retrieve Order & Carrier Logistics Records",
                "objective": f"Query OMS for order {order_id or '[Auto-Detect]'} and verify carrier tracking status."
            },
            {
                "step": 2,
                "agent": "ResolutionExecutorAgent",
                "milestone": "Evaluate Policy Eligibility & Calculate Remedy",
                "objective": f"Check category return windows and inventory availability for {category}."
            },
            {
                "step": 3,
                "agent": "CriticAuditorAgent",
                "milestone": "Audit Fraud Risk & Enforce Compliance",
                "objective": "Cross-check customer return velocity and verify carrier delivery proof to decide auto-approval vs human escalation."
            },
            {
                "step": 4,
                "agent": "CommunicationAgent",
                "milestone": "Draft Customer Response & Dispatch ERP Webhook",
                "objective": "Synthesize final determination into empathetic customer communication and trigger backend webhook."
            }
        ]

        thoughts = (
            f"Detected complaint intent: Category='{category}', Urgency='{urgency}', Sentiment='{sentiment}'. "
            f"Target order identified: '{order_id}'. "
            "Decomposed problem into 4 structured agent milestones with strict compliance and fraud review checkpoints."
        )

        if acoustic_telemetry:
            stress_score = acoustic_telemetry.get("stress_score", 0)
            stress_label = acoustic_telemetry.get("stress_label", "Normal")
            pitch_hz = acoustic_telemetry.get("pitch_hz", 180)
            prosody = acoustic_telemetry.get("prosody_notes", "")
            
            if stress_score >= 70:
                urgency = "Critical"
                sentiment = f"Critical Distress / High Agitation ({stress_score}/100)"
                thoughts += (
                    f" Acoustic Telemetry Stream Integrated: Severe agitation index {stress_score}/100 ({stress_label}) "
                    f"detected via SIP telephony trunk (Pitch: {pitch_hz}Hz, Prosody: '{prosody}'). "
                    f"Acoustic stress elevated triage prioritization to Critical."
                )
            elif stress_score >= 50:
                if urgency == "Medium":
                    urgency = "High"
                thoughts += (
                    f" Acoustic Telemetry Stream Integrated: Moderate vocal tension {stress_score}/100 ({stress_label}) "
                    f"recorded via telephony audio stream. Factored into prioritization."
                )
            else:
                thoughts += (
                    f" Acoustic Telemetry Stream Integrated: Composed vocal cadence {stress_score}/100 ({stress_label}) "
                    f"confirmed via SIP telephony stream."
                )

        return {
            "order_id": order_id,
            "category": category,
            "claim_type": claim_type,
            "sentiment": sentiment,
            "urgency": urgency,
            "execution_plan": execution_plan,
            "planner_thoughts": thoughts,
            "acoustic_telemetry": acoustic_telemetry
        }
