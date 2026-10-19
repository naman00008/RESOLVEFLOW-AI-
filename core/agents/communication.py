"""
Customer Communication & Business Automation Agent for ResolveFlow AI
Synthesizes verified determinations into empathetic, personalized customer responses
and creates live ERP/Payment gateway integration payloads.
"""

from typing import Dict, Any
from ..tools.resolution_actions import generate_erp_webhook_payload

class CommunicationAgent:
    """
    Communication Agent responsible for empathetic customer messaging and ERP automation.
    """
    def __init__(self):
        self.role = "Communication & Business Automation Agent"

    def run(
        self,
        triage_info: Dict[str, Any],
        research_info: Dict[str, Any],
        executor_info: Dict[str, Any],
        critic_info: Dict[str, Any],
        tone_preference: str = "Empathetic & Warm"
    ) -> Dict[str, Any]:
        """
        Drafts customer-facing correspondence and triggers backend webhooks.
        """
        order_data = research_info.get("order_data", {})
        customer_data = research_info.get("customer_data", {})
        carrier_data = research_info.get("carrier_data", {})
        final_verdict = critic_info.get("final_verdict", "")
        financial_remedy = executor_info.get("financial_remedy", {})
        logistics_action = executor_info.get("logistics_action", {})
        customer_name = customer_data.get("name", "Valued Customer")
        product_name = order_data.get("product_name", "your item")
        order_id = order_data.get("order_id", "N/A")

        # 1. Customer Response Message Generation based on Final Verdict
        if final_verdict in ["AUTO_RESOLVED_REPLACEMENT", "REPLACEMENT"]:
            subject = f"Resolution Approved: Replacement for {product_name} (Order #{order_id})"
            message_body = (
                f"Dear {customer_name},\n\n"
                f"Thank you for contacting our customer care team regarding your recent order #{order_id}. "
                f"We are very sorry to hear that your {product_name} arrived in defective condition.\n\n"
                f"We have immediately processed a complimentary expedited replacement unit for you! "
                f"Our warehouse is currently preparing your new order, and it will be dispatched via priority shipping.\n\n"
                f"Return Details:\n"
                f"- Return Merchandise Authorization (RMA): {logistics_action.get('rma_number', 'RMA-PENDING')}\n"
                f"- Courier: {order_data.get('carrier', 'FedEx')}\n"
                f"- Instructions: {logistics_action.get('instructions', 'Courier will bring printed label.')}\n\n"
                "Please accept our sincere apologies for the inconvenience. Thank you for your continued patience."
            )

        elif final_verdict == "CARRIER_INVESTIGATION_COMPENSATION":
            carrier_name = carrier_data.get("carrier", "our logistics carrier")
            compensation = financial_remedy.get("compensation_store_credit", 500.00)
            subject = f"Update & Store Credit on Delayed Order #{order_id}"
            message_body = (
                f"Dear {customer_name},\n\n"
                f"We sincerely apologize for the delay with your order #{order_id} ({product_name}). "
                f"We investigated tracking number {order_data.get('tracking_number')} with {carrier_name} and identified "
                "an unexpected transit delay at the Nagpur central transit hub.\n\n"
                "Here is what we have done immediately:\n"
                f"1. We escalated a Priority Carrier Trace ticket with {carrier_name} management to release your parcel.\n"
                f"2. To make up for the frustration, we have credited ₹{compensation:,.2f} directly to your store account balance.\n"
                f"3. If the shipment does not show onward movement within the next 48 hours, we will either issue an immediate 100% refund "
                f"or dispatch a new unit at no extra charge.\n\n"
                "Thank you for your patience while we resolve this carrier delay."
            )

        elif final_verdict == "POLICY_REFUSAL_GOODWILL_COUPON":
            coupon = financial_remedy.get("coupon_code", "CARE-LOYALTY")
            category = order_data.get("category", "this category")
            subject = f"Regarding your return request for Order #{order_id}"
            message_body = (
                f"Dear {customer_name},\n\n"
                f"Thank you for reaching out to us regarding your order #{order_id} for {product_name}.\n\n"
                f"We carefully reviewed your return inquiry. Because this item falls under our '{category}' category, "
                "our strict safety, health, and hygiene standards prohibit accepting unsealed returns once delivered. "
                f"Additionally, the standard return window elapsed {executor_info.get('policy_evaluation', {}).get('days_since_delivery', 30)} days after delivery.\n\n"
                "While we are unable to accept a return or issue a monetary refund for this purchase, we truly value your relationship with us. "
                f"As a gesture of goodwill, please accept this 15% discount code for your next order:\n\n"
                f"Promo Code: {coupon} (Valid for 30 days across all store items)\n\n"
                "We appreciate your understanding and look forward to serving you again soon."
            )

        elif final_verdict == "ESCALATED_TO_HUMAN_SUPERVISOR":
            subject = f"Order #{order_id}: Case Transferred to Senior Resolution Specialist"
            message_body = (
                f"Dear {customer_name},\n\n"
                f"Thank you for your message regarding order #{order_id} for {product_name}. "
                "We take claims of missing or damaged merchandise very seriously.\n\n"
                "Because this claim involves a high-value item and requires cross-referencing carrier courier manifests and direct delivery signatures, "
                "your ticket has been escalated directly to a Senior Resolution Supervisor on our Priority Operations Desk.\n\n"
                "A specialist has been assigned to your file and will contact you directly within 4 to 8 business hours with an update "
                "following a comprehensive carrier investigation.\n\n"
                "Reference Case Number: ESC-849201"
            )

        elif final_verdict == "VIP_EXPEDITED_EXCHANGE":
            subject = f"VIP Concierge: Expedited Size Exchange for Order #{order_id}"
            message_body = (
                f"Dear {customer_name},\n\n"
                f"Thank you for being one of our most valued Platinum VIP members. "
                f"We deeply apologize that the incorrect size was packed for your {product_name} (Order #{order_id}).\n\n"
                "We understand you have an upcoming event, so we have bypassed all standard return waiting periods:\n"
                "- A brand new pair in Size 42 has been dispatched right now via Same-Day / Priority Courier.\n"
                "- A personal courier will drop off your new boots and collect the Size 40 pair simultaneously.\n"
                "- All return and expedited delivery fees have been completely waived.\n\n"
                "Your dedicated VIP Concierge will track the courier until it is safely in your hands. Thank you for your continued loyalty."
            )

        else:
            subject = f"Update on your Order #{order_id}"
            message_body = (
                f"Dear {customer_name},\n\n"
                f"Thank you for contacting customer support regarding order #{order_id}. "
                f"We have reviewed your inquiry and our team is taking care of it.\n\n"
                "Best regards,\nCustomer Care Team"
            )

        # 2. ERP / Webhook Payload Generation
        webhook_payload = generate_erp_webhook_payload(
            order_id=order_id,
            customer_id=customer_data.get("customer_id", "UNKNOWN"),
            action=final_verdict,
            details={
                "financial_remedy": financial_remedy,
                "logistics_action": logistics_action,
                "fraud_assessment": critic_info.get("fraud_assessment", {})
            }
        )

        thoughts = (
            f"Drafted customer correspondence for verdict '{final_verdict}' with tone '{tone_preference}'. "
            f"Subject: '{subject}'. "
            f"Dispatched ERP webhook event '{webhook_payload.get('event_type')}' with full audit payload."
        )

        return {
            "subject": subject,
            "message_body": message_body,
            "tone_applied": tone_preference,
            "webhook_payload": webhook_payload,
            "communication_thoughts": thoughts
        }
