# Project Report: ResolveFlow AI
## A Multi-Agent AI System for E-Commerce Customer Complaint Triage and Autonomous Resolution
**Continuous Assessment 3 (CA-3) • Domain-Specific Agentic AI Proof of Concept**  
**Authors**: Naman Vyas ([@naman00008](https://github.com/naman00008)) & Akshita Mishra ([@amakshita0506-dot](https://github.com/amakshita0506-dot))

---

### Executive Summary
Customer support in modern e-commerce enterprises is bottlenecked by manual triage backlogs, rigid rule-based FAQ chatbots, and rampant return/refund policy fraud. **ResolveFlow AI** is a domain-specific multi-agent system designed to automate customer complaint triage, policy validation, fraud anomaly detection, and resolution execution. 

Unlike single-turn conversational chatbots that merely generate text, ResolveFlow AI coordinates five specialized agents (**Triage & Planner**, **OMS & Research**, **Resolution Executor**, **Critic & Fraud Auditor**, and **Communication & Automation**) backed by a deterministic pure-Python tool layer. The system reduces resolution turnaround time from 24–48 hours to under 100 milliseconds, prevents improper automated payouts via active self-critique, and generates audit-ready ERP and payment gateway webhook payloads.

---

### 1. Problem Statement & Domain Justification

#### 1.1 The Domain: E-Commerce & Retail Operations
E-commerce retail platforms (e.g., Amazon, Flipkart, Shopify direct-to-consumer merchants) process millions of customer support interactions annually. The operational domain involves a tightly coupled intersection of:
- **Customer Relationship Management (CRM)**: Sentiment management, churn reduction, loyalty tiers.
- **Order Management Systems (OMS)**: Transaction history, SKU specifications, payment records.
- **Logistics & Third-Party Carriers**: Carrier tracking milestones (FedEx, DHL, UPS, BlueDart).
- **Institutional Compliance**: Category-specific return policies, sanitary/health laws (FDA non-returnable hygiene rules), and financial restocking deductions.

#### 1.2 The Existing Business Challenge
Current e-commerce customer service workflows suffer from four major inefficiencies:
1. **Prolonged Support Backlogs**: Tier-1 human customer support queues experience average response times of 12 to 48 hours. Long resolution cycles directly drive customer dissatisfaction and negative social media sentiment.
2. **The Frustration of Static Chatbots**: Existing rule-based or basic RAG chatbots provide canned responses. They lack the autonomous agency to query backend order databases, inspect carrier GPS tracking logs, compute prorated refunds, or schedule reverse pickups.
3. **Inconsistent Policy Application**: Human support agents frequently misapply return window rules, either granting unapproved refunds (causing company financial leakage) or improperly denying legitimate claims (damaging customer retention).
4. **The \$100 Billion Return & Policy Fraud Crisis**: Organized retail abuse—such as serial returners, wardrobing, and false "Item Not Received" (INR) claims—causes retailers over \$100 billion in annual losses. Manual agents lack instantaneous behavioral scoring models to catch repeat offenders.

#### 1.3 The Proposed Solution: ResolveFlow AI
ResolveFlow AI replaces passive conversational chatbots with an autonomous, collaborative multi-agent architecture. The system:
- Ingests raw customer complaint text and decomposes the task into dynamic execution milestones.
- Queries enterprise order databases and live carrier logistics gateways.
- Executes deterministic business tools to calculate mathematically verified financial remedies and reverse logistics labels.
- Implements an explicit **Critic & Fraud Auditor Agent** that reflects on preliminary proposals, scores abuse risk, and enforces Human-in-the-Loop (HITL) supervisor escalation for suspicious cases.
- Formulates empathetic, customer-ready correspondence and emits standardized JSON webhook payloads for automated ERP and Stripe payment fulfillment.

---

### 2. Multi-Agent System Architecture & Specialization

ResolveFlow AI adopts a decentralized, role-based multi-agent architecture where agents communicate through a stateful orchestrator.

```
+----------------------------------------------------------------------------------------------------+
|                                    ResolveFlow Multi-Agent System                                  |
+----------------------------------------------------------------------------------------------------+
|                                                                                                    |
|   [Customer Complaint]                                                                             |
|            |                                                                                       |
|            v                                                                                       |
|   +-----------------------+           +-----------------------+          +-----------------------+ |
|   | 1. Triage & Planner   |  ----->   | 2. OMS & Research     |  ----->  | 3. Resolution Executor| |
|   | Agent                 |           | Agent                 |          | Agent                 | |
|   +-----------------------+           +-----------------------+          +-----------------------+ |
|      - Intent Extraction                 - Order Telemetry                  - Policy Windows       |
|      - Sentiment & Urgency               - Carrier Tracking                 - Financial Remedy     |
|      - Milestone Roadmap                 - Customer Profile                 - Reverse Pickup RMA   |
|                                                                                      |             |
|                                                                                      v             |
|   +-----------------------+           +-----------------------+          +-----------------------+ |
|   | 5. Communication &    |  <-----   | Decision & Risk Gate  |  <-----  | 4. Critic & Fraud     | |
|   | Automation Agent      |           | (Auto vs Supervisor)  |          | Auditor Agent         | |
|   +-----------------------+           +-----------------------+          +-----------------------+ |
|      - Empathetic Letter                 - Risk < 60: Auto                  - Policy Audit         |
|      - ERP Webhook JSON                  - Risk >= 60: HITL                 - Abuse Score (0-100)  |
|                                                                             - Self-Correction Gate |
+----------------------------------------------------------------------------------------------------+
```

#### 2.1 Agent Roles and Responsibilities

| Agent Name | Primary Responsibility | Input Artifacts | Output Artifacts | Deterministic Tools |
| :--- | :--- | :--- | :--- | :--- |
| **1. Triage & Planner Agent** | Analyzes complaint text, extracts order IDs, classifies emotional sentiment, detects urgency, and plans milestones. | Raw customer complaint text | Structured triage metadata & 4-step execution roadmap | Regex parser, sentiment tokenizer, milestone generator |
| **2. OMS & Research Agent** | Gathers authoritative ground-truth data from the Order Management System and logistics carrier gateways. | Order ID | Structured order, customer, and carrier tracking telemetry | `lookup_order`, `lookup_carrier_tracking`, `lookup_customer` |
| **3. Resolution Executor Agent** | Applies deterministic business rules, verifies category return eligibility, and calculates financial adjustments. | Triage metadata, order telemetry | Preliminary resolution proposal, refund/credit math, RMA logistics | `evaluate_return_policy`, `calculate_financial_remedy`, `generate_logistics_action` |
| **4. Critic & Fraud Auditor Agent** | Acts as an internal reflection gate. Evaluates proposed remedies against policies and computes fraud/abuse risk scores. | Executor proposal, customer return history, carrier signature | Validated final determination, overrule flags, HITL escalation notice | `assess_fraud_risk`, policy compliance checklist |
| **5. Communication Agent** | Drafts empathetic, context-aware customer responses and outputs transactional ERP / payment gateway webhook payloads. | Critic verdict, order details, financial calculations | Customer letter, subject line, and JSON webhook event | `generate_erp_webhook_payload`, tone adaptation engine |

---

### 3. Orchestration Workflow & Decision-Making Logic

The multi-agent state machine executes sequentially with conditional reflection:

1. **Phase 1: Ingestion & Milestone Decomposition**
   - The user's message is parsed for order references.
   - Sentiment is classified into `Critical / Hostile`, `Frustrated / Urgent`, or `Inquiring / Mild`.
   - Category is mapped to specific business workflows: *Damaged Goods*, *Logistics Delay*, *Policy-Ineligible Return*, *Stolen Claim*, or *Wrong Item*.

2. **Phase 2: Telemetry Binding**
   - The Research Agent binds external ground-truth state into the working context.
   - For example, in *Scenario 4*, the carrier's physical tracking manifest shows a recorded weight of 4.8 kg and direct signature receipt from the customer.

3. **Phase 3: Deterministic Tool Execution**
   - The Executor Agent executes mathematical business tools:
     - Verifies category-specific return windows (e.g., Electronics: 7 days, Apparel: 30 days, Cosmetics: 0 days).
     - Checks replacement unit stock availability.
     - Calculates prorated refunds, tax adjustments, and restocking deductions.

4. **Phase 4: The Critic Reflection Gate (Self-Correction & Fraud Guard)**
   - The Critic Agent evaluates:
     - **Policy Sanity**: If the Executor proposes a refund for an unsealed cosmetic product, the Critic overrules the proposal to enforce health regulations.
     - **Fraud Risk Score**: Computes a multi-factor risk score ($0 \le \text{Risk} \le 100$) based on customer return rate, past missing item claims, claim value, and carrier signature conflicts.
     - **Human-in-the-Loop Threshold**: If $\text{Risk} \ge 60$, the Critic halts automated payout and escalates the dossier to a Human Fraud Supervisor.

5. **Phase 5: Automated Fulfillment**
   - The Communication Agent compiles the customer correspondence and generates an event-driven JSON webhook payload formatted for Stripe and SAP ERP integration.

---

### 4. Empirical Evaluation: 5 Benchmark Scenarios

The system was evaluated against five representative e-commerce edge cases:

| Scenario # | Test Case Description | Customer Tier | Order Value | Fraud Risk | Final System Verdict | Action Executed |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Scenario 1** | Defective audio on headphones delivered 2 days ago (within 7-day window). | Standard (`CUST-101`) | \$269.99 | Low (10/100) | `REPLACEMENT` | Auto-approved replacement; generated reverse pickup RMA label. |
| **Scenario 2** | Espresso machine stalled in transit with DHL for 6 days past promised date. | Silver (`CUST-102`) | \$360.59 | Low (15/100) | `DELAY_COMPENSATION` | Expedited carrier trace opened; \$25 store compensation credit awarded. |
| **Scenario 3** | Unsealed anti-aging serum returned after 38 days (non-returnable hygiene item). | Standard (`CUST-103`) | \$101.66 | Low (5/100) | `POLICY_REFUSAL_GOODWILL_COUPON` | Cash refund refused per FDA policy; 15% goodwill store credit coupon issued. |
| **Scenario 4** | \$1,600 laptop claimed stolen / box empty. Customer has 66.7% return rate; carrier verified signature. | High Risk (`CUST-104`) | \$1,618.92 | Critical (88/100) | `ESCALATED_TO_HUMAN_SUPERVISOR` | **CRITIC OVERRULED**: Automated refund halted; case escalated to Senior Fraud Desk. |
| **Scenario 5** | Platinum VIP customer shipped wrong shoe size (EU 40 instead of EU 42). | Platinum VIP (`CUST-105`) | \$410.40 | Very Low (0/100) | `VIP_EXPEDITED_EXCHANGE` | White-glove concierge courier exchange; all return fees waived. |

---

### 5. Technical Stack & Local Execution

ResolveFlow AI was intentionally engineered to run **100% locally with zero paid API requirements**:
- **Programming Language**: Python 3.12+
- **User Interface**: Streamlit (Zinc minimal high-tech design, responsive card layouts)
- **Data Visualization**: Plotly & Pandas
- **Presentation Engine**: `python-pptx` (programmatic 16:9 widescreen slide generation)
- **Execution Engine**: Stateful Multi-Agent Orchestrator with streaming generators for real-time UI animation.

---

### 6. Limitations, Ethical Safeguards & Future Scope

#### 6.1 Ethical Safeguards & Fair Treatment
- **Algorithmic Transparency**: Every decision is accompanied by an explainable audit trail detailing exact policy clauses and risk factors.
- **Demographic Neutrality**: Fraud scores rely exclusively on objective transactional telemetry (return velocity, signature mismatches), eliminating subjective bias.
- **High-Stakes Safety**: The system enforces human supervisor approval on all high-risk claims, preventing irreversible erroneous decisions.

#### 6.2 Current Limitations
1. **Multimodal Damage Verification**: Currently, photo evidence submission is verified programmatically; production deployment will incorporate Vision-Language Models (VLMs) to inspect item crack/water damage severity.
2. **Synthetic Data Dependency**: Uses a mock OMS and simulated carrier API gateway; production deployment requires enterprise REST/GraphQL middleware.

#### 6.3 Future Scope
- **Model Context Protocol (MCP) Integration**: Connecting agents directly to external ERP inventory microservices and warehouse robotics via standardized MCP tool servers.
- **Multi-Turn Negotiation Memory**: Enabling conversational bargaining where customers can choose between immediate store credit discounts or delayed physical replacements.

---

### 7. Conclusion
ResolveFlow AI demonstrates that Agentic AI provides a fundamental leap over traditional chatbots in customer operations. By combining autonomous milestone planning, authoritative telemetry research, deterministic business tools, and self-correcting critic reflection, ResolveFlow AI delivers an enterprise-grade Proof of Concept that drastically cuts operational costs while enhancing customer trust and satisfaction.
