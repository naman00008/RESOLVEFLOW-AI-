"""
Multi-Agent Orchestrator for ResolveFlow AI
Coordinates agent execution, manages shared state, streams live trace logs,
and enforces error boundaries.
"""

import time
from datetime import datetime
from typing import Dict, Any, Generator, List, Optional
from .agents.triage_planner import TriagePlannerAgent
from .agents.oms_researcher import OMSResearchAgent
from .agents.resolution_executor import ResolutionExecutorAgent
from .agents.critic_auditor import CriticAuditorAgent
from .agents.communication import CommunicationAgent

class ResolveFlowOrchestrator:
    """
    Central Orchestrator implementing the collaborative Multi-Agent state machine.
    """
    def __init__(self):
        self.planner = TriagePlannerAgent()
        self.researcher = OMSResearchAgent()
        self.executor = ResolutionExecutorAgent()
        self.critic = CriticAuditorAgent()
        self.communicator = CommunicationAgent()

    def run_pipeline(
        self,
        complaint_text: str,
        order_id: str = "",
        tone_preference: str = "Empathetic & Warm",
        custom_policy_matrix: Optional[Dict[str, Any]] = None,
        acoustic_telemetry: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes the entire multi-agent pipeline synchronously and returns complete state.
        """
        trace_steps: List[Dict[str, Any]] = []
        start_time = time.time()

        # Step 1: Triage & Planning
        t1 = time.time()
        triage_info = self.planner.run(complaint_text, explicit_order_id=order_id, acoustic_telemetry=acoustic_telemetry)
        resolved_order_id = triage_info.get("order_id") or order_id
        triage_duration = round((time.time() - t1) * 1000, 1)
        step1_summary = f"Classified as '{triage_info.get('category')}' with {triage_info.get('urgency')} urgency."
        if acoustic_telemetry:
            step1_summary += f" [IVR Voice Stress: {acoustic_telemetry.get('stress_score')}/100 ({acoustic_telemetry.get('stress_label')})]"
        trace_steps.append({
            "step_number": 1,
            "agent_name": "Triage & Planner Agent",
            "role": "Intent Classification & Milestone Planning",
            "status": "COMPLETED",
            "duration_ms": triage_duration,
            "summary": step1_summary,
            "thoughts": triage_info.get("planner_thoughts"),
            "data": triage_info,
            "tool_calls": []
        })

        # Step 2: OMS & Carrier Research
        t2 = time.time()
        research_info = self.researcher.run(resolved_order_id)
        research_duration = round((time.time() - t2) * 1000, 1)
        trace_steps.append({
            "step_number": 2,
            "agent_name": "OMS & Research Agent",
            "role": "Order & Carrier Logistics Telemetry Retrieval",
            "status": "COMPLETED" if research_info.get("success") else "FAILED",
            "duration_ms": research_duration,
            "summary": f"Fetched order details for {resolved_order_id} ({research_info.get('order_data', {}).get('carrier', 'Carrier')}).",
            "thoughts": research_info.get("researcher_thoughts"),
            "data": research_info,
            "tool_calls": research_info.get("tool_calls", [])
        })

        if not research_info.get("success"):
            return {
                "success": False,
                "error": research_info.get("error"),
                "trace_steps": trace_steps,
                "total_duration_ms": round((time.time() - start_time) * 1000, 1)
            }

        # Step 3: Resolution Execution
        t3 = time.time()
        executor_info = self.executor.run(triage_info, research_info, custom_policy_matrix=custom_policy_matrix)
        executor_duration = round((time.time() - t3) * 1000, 1)
        trace_steps.append({
            "step_number": 3,
            "agent_name": "Resolution Executor Agent",
            "role": "Deterministic Policy Evaluation & Remedy Calculation",
            "status": "COMPLETED",
            "duration_ms": executor_duration,
            "summary": f"Proposed remedy: '{executor_info.get('proposed_remedy_type')}'.",
            "thoughts": executor_info.get("executor_thoughts"),
            "data": executor_info,
            "tool_calls": executor_info.get("tool_calls", [])
        })

        # Step 4: Critic & Fraud Audit
        t4 = time.time()
        critic_info = self.critic.run(triage_info, research_info, executor_info)
        critic_duration = round((time.time() - t4) * 1000, 1)
        trace_steps.append({
            "step_number": 4,
            "agent_name": "Critic & Fraud Auditor Agent",
            "role": "Policy Self-Correction, Fraud Scoring & HITL Enforcer",
            "status": "COMPLETED",
            "duration_ms": critic_duration,
            "summary": f"Final verdict: '{critic_info.get('final_verdict')}' (Overruled: {critic_info.get('is_overruled')}).",
            "thoughts": critic_info.get("critic_thoughts"),
            "data": critic_info,
            "tool_calls": critic_info.get("tool_calls", [])
        })

        # Step 5: Customer Communication & ERP Automation
        t5 = time.time()
        comm_info = self.communicator.run(
            triage_info,
            research_info,
            executor_info,
            critic_info,
            tone_preference=tone_preference
        )
        comm_duration = round((time.time() - t5) * 1000, 1)
        trace_steps.append({
            "step_number": 5,
            "agent_name": "Communication & Automation Agent",
            "role": "Customer Response Drafting & ERP Webhook Dispatch",
            "status": "COMPLETED",
            "duration_ms": comm_duration,
            "summary": f"Generated customer response letter and dispatched ERP webhook '{comm_info.get('webhook_payload', {}).get('event_type')}'.",
            "thoughts": comm_info.get("communication_thoughts"),
            "data": comm_info,
            "tool_calls": []
        })

        total_duration = round((time.time() - start_time) * 1000, 1)

        return {
            "success": True,
            "complaint_text": complaint_text,
            "order_id": resolved_order_id,
            "triage_info": triage_info,
            "research_info": research_info,
            "executor_info": executor_info,
            "critic_info": critic_info,
            "communication_info": comm_info,
            "trace_steps": trace_steps,
            "final_verdict": critic_info.get("final_verdict"),
            "supervisor_escalated": critic_info.get("supervisor_escalation_required"),
            "fraud_score": critic_info.get("fraud_assessment", {}).get("risk_score", 0),
            "fraud_level": critic_info.get("fraud_assessment", {}).get("risk_level", "LOW"),
            "total_duration_ms": total_duration,
            "timestamp": datetime.now().isoformat()
        }

    def stream_execution(
        self,
        complaint_text: str,
        order_id: str = "",
        tone_preference: str = "Empathetic & Warm",
        custom_policy_matrix: Optional[Dict[str, Any]] = None
    ) -> Generator[Dict[str, Any], None, Dict[str, Any]]:
        """
        Yields incremental step updates for real-time visual progress rendering in Streamlit.
        """
        trace_steps = []
        start_time = time.time()

        # Step 1
        t1 = time.time()
        triage_info = self.planner.run(complaint_text, explicit_order_id=order_id)
        resolved_order_id = triage_info.get("order_id") or order_id
        step1 = {
            "step_number": 1,
            "agent_name": "Triage & Planner Agent",
            "role": "Intent Classification & Milestone Planning",
            "status": "COMPLETED",
            "duration_ms": round((time.time() - t1) * 1000, 1),
            "summary": f"Classified as '{triage_info.get('category')}' with {triage_info.get('urgency')} urgency.",
            "thoughts": triage_info.get("planner_thoughts"),
            "data": triage_info,
            "tool_calls": []
        }
        trace_steps.append(step1)
        yield {"step": 1, "step_data": step1, "all_steps": trace_steps, "pipeline_complete": False}

        # Step 2
        t2 = time.time()
        research_info = self.researcher.run(resolved_order_id)
        step2 = {
            "step_number": 2,
            "agent_name": "OMS & Research Agent",
            "role": "Order & Carrier Logistics Telemetry Retrieval",
            "status": "COMPLETED" if research_info.get("success") else "FAILED",
            "duration_ms": round((time.time() - t2) * 1000, 1),
            "summary": f"Fetched order details for {resolved_order_id} ({research_info.get('order_data', {}).get('carrier', 'Carrier')}).",
            "thoughts": research_info.get("researcher_thoughts"),
            "data": research_info,
            "tool_calls": research_info.get("tool_calls", [])
        }
        trace_steps.append(step2)
        yield {"step": 2, "step_data": step2, "all_steps": trace_steps, "pipeline_complete": False}

        if not research_info.get("success"):
            yield {
                "step": 2,
                "pipeline_complete": True,
                "error": research_info.get("error"),
                "all_steps": trace_steps
            }
            return

        # Step 3
        t3 = time.time()
        executor_info = self.executor.run(triage_info, research_info, custom_policy_matrix=custom_policy_matrix)
        step3 = {
            "step_number": 3,
            "agent_name": "Resolution Executor Agent",
            "role": "Deterministic Policy Evaluation & Remedy Calculation",
            "status": "COMPLETED",
            "duration_ms": round((time.time() - t3) * 1000, 1),
            "summary": f"Proposed remedy: '{executor_info.get('proposed_remedy_type')}'.",
            "thoughts": executor_info.get("executor_thoughts"),
            "data": executor_info,
            "tool_calls": executor_info.get("tool_calls", [])
        }
        trace_steps.append(step3)
        yield {"step": 3, "step_data": step3, "all_steps": trace_steps, "pipeline_complete": False}

        # Step 4
        t4 = time.time()
        critic_info = self.critic.run(triage_info, research_info, executor_info)
        step4 = {
            "step_number": 4,
            "agent_name": "Critic & Fraud Auditor Agent",
            "role": "Policy Self-Correction, Fraud Scoring & HITL Enforcer",
            "status": "COMPLETED",
            "duration_ms": round((time.time() - t4) * 1000, 1),
            "summary": f"Final verdict: '{critic_info.get('final_verdict')}' (Overruled: {critic_info.get('is_overruled')}).",
            "thoughts": critic_info.get("critic_thoughts"),
            "data": critic_info,
            "tool_calls": critic_info.get("tool_calls", [])
        }
        trace_steps.append(step4)
        yield {"step": 4, "step_data": step4, "all_steps": trace_steps, "pipeline_complete": False}

        # Step 5
        t5 = time.time()
        comm_info = self.communicator.run(
            triage_info,
            research_info,
            executor_info,
            critic_info,
            tone_preference=tone_preference
        )
        step5 = {
            "step_number": 5,
            "agent_name": "Communication & Automation Agent",
            "role": "Customer Response Drafting & ERP Webhook Dispatch",
            "status": "COMPLETED",
            "duration_ms": round((time.time() - t5) * 1000, 1),
            "summary": f"Generated customer response letter and dispatched ERP webhook.",
            "thoughts": comm_info.get("communication_thoughts"),
            "data": comm_info,
            "tool_calls": []
        }
        trace_steps.append(step5)

        total_duration = round((time.time() - start_time) * 1000, 1)
        complete_result = {
            "success": True,
            "complaint_text": complaint_text,
            "order_id": resolved_order_id,
            "triage_info": triage_info,
            "research_info": research_info,
            "executor_info": executor_info,
            "critic_info": critic_info,
            "communication_info": comm_info,
            "trace_steps": trace_steps,
            "final_verdict": critic_info.get("final_verdict"),
            "supervisor_escalated": critic_info.get("supervisor_escalation_required"),
            "fraud_score": critic_info.get("fraud_assessment", {}).get("risk_score", 0),
            "fraud_level": critic_info.get("fraud_assessment", {}).get("risk_level", "LOW"),
            "total_duration_ms": total_duration,
            "timestamp": datetime.now().isoformat()
        }

        yield {
            "step": 5,
            "step_data": step5,
            "all_steps": trace_steps,
            "pipeline_complete": True,
            "final_result": complete_result
        }
        return complete_result
