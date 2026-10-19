"""
Automated Pipeline Verification Test Suite
Tests all 5 benchmark scenarios through the Multi-Agent Orchestrator.
"""

import unittest
from core.orchestrator import ResolveFlowOrchestrator
from core.data.mock_database import BENCHMARK_SCENARIOS

class TestResolveFlowPipeline(unittest.TestCase):
    def setUp(self):
        self.orchestrator = ResolveFlowOrchestrator()

    def test_scenario_1_defective_headphones(self):
        scenario = BENCHMARK_SCENARIOS[0]
        result = self.orchestrator.run_pipeline(scenario["complaint_text"], scenario["order_id"])
        self.assertTrue(result["success"])
        self.assertEqual(result["final_verdict"], "REPLACEMENT")
        self.assertFalse(result["supervisor_escalated"])
        self.assertEqual(result["fraud_level"], "LOW")
        self.assertEqual(len(result["trace_steps"]), 5)
        # Check RMA was created
        logistics = result["executor_info"].get("logistics_action", {})
        self.assertTrue(logistics.get("rma_number", "").startswith("RMA-"))

    def test_scenario_2_logistics_delay(self):
        scenario = BENCHMARK_SCENARIOS[1]
        result = self.orchestrator.run_pipeline(scenario["complaint_text"], scenario["order_id"])
        self.assertTrue(result["success"])
        self.assertEqual(result["final_verdict"], "DELAY_COMPENSATION")
        self.assertFalse(result["supervisor_escalated"])
        # Check compensation was awarded
        remedy = result["executor_info"].get("financial_remedy", {})
        self.assertGreater(remedy.get("compensation_store_credit", 0), 0)

    def test_scenario_3_policy_ineligible_cosmetics(self):
        scenario = BENCHMARK_SCENARIOS[2]
        result = self.orchestrator.run_pipeline(scenario["complaint_text"], scenario["order_id"])
        self.assertTrue(result["success"])
        self.assertEqual(result["final_verdict"], "POLICY_REFUSAL_GOODWILL_COUPON")
        self.assertFalse(result["supervisor_escalated"])
        # Check goodwill coupon was generated
        remedy = result["executor_info"].get("financial_remedy", {})
        self.assertTrue(remedy.get("coupon_code", "").startswith("CARE-"))

    def test_scenario_4_fraud_serial_returner_escalation(self):
        scenario = BENCHMARK_SCENARIOS[3]
        result = self.orchestrator.run_pipeline(scenario["complaint_text"], scenario["order_id"])
        self.assertTrue(result["success"])
        # Critic must overrule automatic refund and escalate to supervisor
        self.assertEqual(result["final_verdict"], "ESCALATED_TO_HUMAN_SUPERVISOR")
        self.assertTrue(result["supervisor_escalated"])
        self.assertGreaterEqual(result["fraud_score"], 60)
        self.assertTrue(result["critic_info"]["is_overruled"])

    def test_scenario_5_vip_concierge_exchange(self):
        scenario = BENCHMARK_SCENARIOS[4]
        result = self.orchestrator.run_pipeline(scenario["complaint_text"], scenario["order_id"])
        self.assertTrue(result["success"])
        self.assertEqual(result["final_verdict"], "VIP_EXPEDITED_EXCHANGE")
        self.assertFalse(result["supervisor_escalated"])
        self.assertIn("Platinum VIP", result["research_info"]["customer_data"]["tier"])

if __name__ == "__main__":
    unittest.main()
