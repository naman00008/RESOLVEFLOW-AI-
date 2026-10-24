# ResolveFlow AI: Multi-Agent Customer Complaint Triage & Resolution

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red.svg)](https://streamlit.io/)
[![Assessment](https://img.shields.io/badge/Assessment-CA--3%20Agentic%20AI%20PoC-green.svg)]()
[![Zero Paid API](https://img.shields.io/badge/API%20Requirement-Zero%20Paid%20Keys-brightgreen.svg)]()

> **Continuous Assessment 3 (CA-3) Submission**  
> An enterprise-grade Proof of Concept (PoC) demonstrating how autonomous, collaborative AI agents transform slow, error-prone e-commerce customer complaint handling into an instant, policy-compliant, and fraud-resistant workflow.

---

## Quickstart (1-Click Run)

To run the entire system (including test verification, presentation generation, and launching the Streamlit PoC):

```bash
chmod +x run.sh
./run.sh
```

Or run manually using your virtual environment:

```bash
# 1. Activate environment
source .venv/bin/activate

# 2. Run automated verification tests
python -m unittest tests/test_pipeline.py

# 3. Generate PowerPoint presentation (.pptx)
python scripts/generate_presentation.py

# 4. Launch Streamlit UI
streamlit run app.py
```

Open your browser to `http://localhost:8501`.

---

## The Real-World Problem & Domain Justification

- **Domain**: E-Commerce & Retail Operations (Customer Complaint Triage & Resolution).
- **Existing Challenge**:
  - Human customer support backlogs average **12 to 48 hours**.
  - Traditional rule-based chatbots cannot query backend Order Management Systems (OMS), inspect real-time carrier tracking (BlueDart, Delhivery, DTDC), or calculate prorated refunds and restocking fees.
  - Return fraud and false "Item Not Received" (INR) claims cost retailers over **₹8,000 Crores annually** due to lack of real-time abuse scoring.
- **Agentic AI Solution**:
  - ResolveFlow AI coordinates **5 specialized agents** with a deterministic Python tool layer.
  - Slashes resolution turnaround from **2 days to <100 milliseconds**.
  - Features an active **Critic Agent** that audits preliminary proposals, scores fraud risk, and enforces Human-in-the-Loop (HITL) supervisor escalation on suspicious cases.

---

## Multi-Agent Architecture

```
[Customer Complaint]
        |
        v
1. Triage & Planner Agent (Extracts intent, urgency, order ID; formulates 4-step milestones)
        |
        v
2. OMS & Research Agent (Queries order telemetry, customer tier, carrier GPS logs)
        |
        v
3. Resolution Executor Agent (Checks category return windows, inventory, calculates refund/RMA)
        |
        v
4. Critic & Fraud Auditor Agent (Audits compliance, scores abuse risk 0-100, enforces HITL gate)
        |
   +----+---------------------------+
   v                                v
[Risk < 60: Auto-Approved]     [Risk >= 60: Human Supervisor Escalation]
   |                                |
   +---------------+----------------+
                   v
5. Communication & Automation Agent (Empathetic customer letter + Stripe/ERP JSON webhook)
```

### Deterministic Tool Layer
- `lookup_order`: Fetches items, prices, delivery dates, and SKU details from OMS.
- `lookup_carrier_tracking`: Interrogates live carrier checkpoints and delivery signatures.
- `evaluate_return_policy`: Mathematically checks return windows and sanitary hygiene restrictions.
- `assess_fraud_risk`: Multi-factor risk engine evaluating return rate, stolen claims, and signature conflicts.
- `calculate_financial_remedy`: Computes exact refunds, restocking deductions, or delay compensations.
- `generate_logistics_action`: Issues Reverse Merchandise Authorization (RMA) barcodes.
- `generate_erp_webhook_payload`: Formats standardized JSON payloads for payment gateways.

---

## 5 Realistic Benchmark Evaluation Scenarios

| Scenario | Case Description | Risk Score | Expected Verdict | Action Executed |
| :--- | :--- | :--- | :--- | :--- |
| **1** | Defective Headphones within 7-day window | 10/100 (Low) | `REPLACEMENT` | Auto-approved replacement with free reverse pickup RMA label |
| **2** | Espresso Machine delayed in transit with Delhivery | 15/100 (Low) | `DELAY_COMPENSATION` | Expedited carrier trace opened + ₹500 store delay credit |
| **3** | Unsealed cosmetic serum returned after 38 days | 5/100 (Low) | `POLICY_REFUSAL_GOODWILL_COUPON` | Cash refund refused per hygiene rules; 15% goodwill voucher issued |
| **4** | ₹1.76L laptop claimed stolen by serial returner | 88/100 (Critical) | `ESCALATED_TO_HUMAN_SUPERVISOR` | **Critic Overruled**: Automated refund halted; escalated to Fraud Desk |
| **5** | Platinum VIP customer shipped wrong shoe size | 0/100 (Very Low) | `VIP_EXPEDITED_EXCHANGE` | White-glove concierge courier exchange; all return fees waived |

---

## Project Deliverables Checklist (CA-3 Rubric)

- [x] **Clear Problem Statement & Domain Justification**: Documented in `PROJECT_REPORT.md` and UI.
- [x] **Agent Roles, Responsibilities & Orchestration**: 5 modular agents under `core/agents/`.
- [x] **Architecture Diagram**: Mermaid and graphical diagrams in `docs/` and Streamlit.
- [x] **Working Streamlit PoC**: Interactive web dashboard (`app.py`) with live agent traces.
- [x] **Output Validation & Test Suite**: Unit tests passing 10/10 in `tests/test_pipeline.py` (covering multi-agent pipeline, provider credentials, and LLM studio).
- [x] **PowerPoint Presentation Deck**: Programmatically generated 8-slide deck (`ResolveFlow_AI_Presentation.pptx`).
- [x] **5-Minute Timed Presentation Script**: Full speaker script in `docs/presentation_script.md`.
- [x] **Zero Paid API Requirement**: Runs 100% locally and reliably out-of-the-box (with optional live Google Gemini and Groq Cloud connections).
- [x] **Multi-Provider LLM Studio**: Dedicated LLM Intelligence tab featuring Supervisor Copilot, Dynamic Intent & Tone Synthesis, and Adversarial Prompt Defense.

---

## Authors / Team
- **Course**: Continuous Assessment 3 (CA-3) • Agentic AI
- **Date**: October 2026
- **Team Members**:
  - **Naman Vyas** ([@naman00008](https://github.com/naman00008))
  - **Akshita Mishra** ([@amakshita0506-dot](https://github.com/amakshita0506-dot))
