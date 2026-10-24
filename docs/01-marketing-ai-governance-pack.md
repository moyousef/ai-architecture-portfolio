# Marketing Automation with AI & Agents — Governance Pack

**Session 1 mini-project | Architecture baseline v1.0 | Status: Proposed (ARB review required)**  
**Scope:** Saudi-based marketing team; agents plan campaigns, retrieve approved brand content, draft messages, and prepare audience segments. CRM owns customer records and consent. **Agents may draft but never autonomously send.** Proposed goals and controls below are design targets, not verified implementation claims.

## Business goals & architecture principles

| ID | Principle (mandatory design rule) | Linked business goal | Evidence |
|---|---|---|---|
| **P1** | **Privacy and consent by design:** minimize PII; exclude sensitive data from marketing; check recorded consent and suppression **at send time**. | **G1** Earn customer trust and avoid unauthorized outreach. | Consent receipts, opt-out tests, data inventory. |
| **P2** | **Human accountability:** an authorized marketer approves every outbound campaign; approval is scoped to content, audience, channel and expiry. | **G2** Protect brand reputation and reduce campaign errors. | Approval record and reject/rollback test. |
| **P3** | **Least-privilege agents:** isolate tools behind an API gateway, allowlist actions, and block unapproved external data transfers. | **G3** Scale automation without widening security exposure. | Threat model, tool permissions, egress review. |
| **P4** | **Measurable quality and spend:** evaluate generated content and enforce per-campaign usage budgets before release. | **G4** Reduce campaign lead time while controlling ROI and AI costs. | Eval report, usage dashboard, budget alerts. |

## Architecture Decision Records (ADRs)

| ADR | Options & trade-offs | Decision and consequences |
|---|---|---|
| **001 — LLM hosting** | **Managed API:** faster setup and model upgrades; vendor dependency and transfer risk. **Self-hosted:** higher data control; GPU, operations and model-maintenance burden. | **Choose managed API for sanitized, non-personal campaign drafts only**, behind a PII-filtering gateway, **conditional on** vendor due diligence, contracts and lawful transfer assessment. If not approved, self-host within approved boundary or block that feature. |
| **002 — Retrieval store** | **PostgreSQL + pgvector:** simple reuse and low operational cost; weaker scaling for very large vector workloads. **Dedicated vector DB:** specialized scale/features; more complexity and cost. | **Choose PostgreSQL + pgvector** for approved brand documents only (no customer profiles in embeddings); revisit if measured retrieval latency/scale fails targets. |
| **003 — Execution pattern** | **Real-time:** responsive to events; higher coupling, monitoring load and incident risk. **Scheduled batch:** predictable reviews/cost; less immediate personalization. | **Choose scheduled batch campaigns**, with mandatory human approval and **live consent/suppression recheck immediately before each send**. Real-time triggers are deferred. |

## ARB pre-production checklist — all items must pass

| Domain | Required evidence / pass criterion |
|---|---|
| **Security** | Threat model; SSO/RBAC; secrets vault; isolated agent tools; prompt-injection defenses; signed API actions; audit logging; incident kill switch. |
| **Privacy / Saudi PDPL** | Document processing purpose and notice; verify **prior direct-marketing consent** and accessible opt-out; respect withdrawal/deletion; no sensitive-data marketing; retention plan; review any overseas transfers and vendor safeguards. |
| **Evals** | Versioned test set for brand fidelity, factual claims, harmful output, PII leakage and prompt injection; defined acceptance thresholds and human-reviewed failures. |
| **Cost** | Approved model/channel spend caps, token metering, alerts, retry limits and rollback plan. |
| **Human oversight** | Named approver, three-step publish control (**approve → verify eligibility → send**), approval expiry, override logging and stop/resume procedure. |

**ARB decision:** **CONDITIONAL / NOT YET APPROVED FOR PRODUCTION.** Security, Privacy/DPO, Marketing Owner and Architecture must sign off on the evidence above. Any failed privacy/consent or human-approval gate means **NO GO**.

**Optional automated guardrail:** `.github/workflows/governance-review.yml` runs `scripts/check_governance.py` on pull requests to verify that all four principles, three ADRs, five ARB categories, and the human/consent gates appear in the design artifacts. **It checks documentation completeness, not legal or operational compliance.**

**Regulatory references:** [Saudi PDPL (SDAIA)](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PDPL) · [PDPL Implementing Regulation — arts. 28–29](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/PDPL2) · [Cross-border data transfer regulation](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter/details/RegulationonPersonalDataTransferOutsidetheKingdom).
