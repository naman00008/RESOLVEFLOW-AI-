# ResolveFlow AI: 5-Minute Presentation Script (CA-3 Evaluation)

> **Format**: Maximum 5 minutes.  
> **Structure**: Designed for either a **Solo Presenter** or a **Pair (Presenter 1 & Presenter 2)**.  
> **Visual Reference**: Follows slides in `ResolveFlow_AI_Presentation.pptx`.

---

## Slide 1: Title & Introduction (0:00 - 0:40)
- **Presenter 1**:
  > *"Good morning respected faculty and peers. Today, we are proud to present **ResolveFlow AI: A Multi-Agent AI System for E-Commerce Customer Complaint Triage and Autonomous Resolution** for Continuous Assessment 3 (CA-3).*  
  > *In today's presentation, we will demonstrate how moving from traditional single-turn chatbots to an orchestrated multi-agent architecture transforms customer support from a costly 48-hour backlog into a secure, policy-compliant, sub-second resolution pipeline."*

---

## Slide 2: The Real-World Business Challenge (0:40 - 1:20)
- **Presenter 1** (or Presenter 2 if presenting as a pair):
  > *"Let's look at the current industry problem. Modern e-commerce platforms like Amazon, Flipkart, and Shopify process thousands of complex complaints every single day—damaged shipments, logistics delays, wrong sizes, and refund disputes.*  
  > *Existing solutions suffer from three fatal inefficiencies:*  
  > *1. **Slow Human Triage**: Response times average 12 to 48 hours, causing customer churn.*  
  > *2. **Static Chatbots Fail**: Rule-based or generic LLM chatbots cannot query backend Order Management Systems (OMS), check real-time carrier GPS logs, calculate restocking fees, or generate reverse pickup shipping labels.*  
  > *3. **The ₹8,000 Crore+ Fraud Crisis**: Retailers lose over ₹8,000 Crores annually in India to return fraud and false 'empty package' claims because human agents lack real-time abuse scoring and carrier signature cross-checks."*

---

## Slide 3: Domain Justification & Agentic Solution (1:20 - 2:00)
- **Presenter 2**:
  > *"Why did we choose E-Commerce Operations? Because resolving a customer complaint is fundamentally a multi-step, deterministic, and compliance-driven task. A simple text-generating chatbot can hallucinate refund promises that violate company policy or health regulations.*  
  > *ResolveFlow AI solves this by introducing **Agentic AI**: an autonomous system where specialized agents plan, gather telemetry, execute mathematical business tools, perform self-critique, and trigger downstream enterprise webhooks without human intervention—while safely escalating edge cases."*

---

## Slide 4: Multi-Agent Architecture (2:00 - 2:45)
- **Presenter 1**:
  > *"Our system coordinates five distinct cognitive agents alongside a deterministic tool layer:*  
  > *1. The **Triage & Planner Agent** deconstructs incoming customer messages, identifies the order ID, assesses emotional sentiment and urgency, and outlines a dynamic 4-step milestone plan.*  
  > *2. The **OMS & Research Agent** pulls ground-truth telemetry from the Order Management System, customer purchase history, and live carrier tracking APIs (BlueDart, Delhivery, DTDC, Shadowfax).*  
  > *3. The **Resolution Executor Agent** applies deterministic business rules: verifying category return windows, calculating refunds or restocking fees, and checking replacement inventory.*  
  > *4. The **Critic & Fraud Auditor Agent** acts as an internal reflection gate. It calculates a multi-factor abuse score (0 to 100) and cross-checks the executor's proposal against institutional policies.*  
  > *5. The **Communication & Automation Agent** drafts empathetic, personalized messages and emits transactional webhooks to Stripe and warehouse ERPs."*

---

## Slide 5: Orchestration & Human-in-the-Loop Governance (2:45 - 3:30)
- **Presenter 2**:
  > *"Here is how these agents collaborate in our orchestration state machine.*  
  > *Notice the critical innovation: **The Critic Reflection Gate**.*  
  > *If an executor attempts to refund an unsealed cosmetic item that violates health regulations, the Critic Agent overrules the decision and converts it to a polite policy refusal with a goodwill coupon.*  
  > *Even more importantly, if a customer with a high return velocity claims a ₹1.76L laptop was stolen despite carrier direct-signature verification, the Critic Agent detects a Critical Risk Score (88/100), halts automated payout, and routes the dossier to a Human Fraud Supervisor. This provides 100% enterprise trust."*

---

## Slide 6: Live PoC Demonstration & Benchmark Results (3:30 - 4:15)
- **Presenter 1**:
  > *[Demonstrate live Streamlit UI or point to slide]*  
  > *"We validated our PoC across five diverse benchmark scenarios:*  
  > *- In **Scenario 1**, a legitimate defective headphone within the 7-day window receives an auto-approved replacement with an instant reverse pickup RMA label.*  
  > *- In **Scenario 2**, a delayed espresso machine triggers a carrier trace and automated ₹500 store compensation credit.*  
  > *- In **Scenario 3**, an unsealed cosmetic returned after 38 days is politely refused under FDA hygiene rules, but rewarded with a 15% goodwill coupon.*  
  > *- In **Scenario 4**, our Critic Agent catches a serial returner anomaly, preventing a ₹1,76,988 improper payout.*  
  > *- In **Scenario 5**, our Platinum VIP customer receives white-glove courier exchange with zero friction.*  
  > *All of this runs in under 100 milliseconds locally with zero paid API overhead."*

---

## Slide 7 & 8: Limitations, Future Scope & Conclusion (4:15 - 5:00)
- **Presenter 2**:
  > *"To ensure academic rigor, we acknowledge our current limitations: future iterations will integrate Computer Vision for automated damaged parcel inspection and Model Context Protocol (MCP) bridges for live warehouse robotics.*  
  > *In conclusion, ResolveFlow AI proves how multi-agent collaboration replaces frustrating chatbots and slow human queues with an autonomous, secure, and delightful customer support experience.*  
  > *Thank you, and we now welcome any questions from the panel!"*
