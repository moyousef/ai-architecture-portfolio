#!/usr/bin/env python3
"""Documentation guardrail for the Session 1 governance pack (NOT runtime compliance)."""
from pathlib import Path
from xml.etree import ElementTree as ET
import sys

BASE = Path(__file__).resolve().parents[1]
MD = BASE / 'docs/01-marketing-ai-governance-pack.md'
DIAGRAM = BASE / 'diagrams/marketing-ai-governance.drawio'
failures = []

if not MD.is_file() or not DIAGRAM.is_file():
    sys.exit('FAIL: governance wiki or draw.io file is missing')

text = MD.read_text(encoding='utf-8')
for label in ['**P1**', '**P2**', '**P3**', '**P4**',
              '**001 —', '**002 —', '**003 —',
              '**Security**', '**Privacy / Saudi PDPL**',
              '**Evals**', '**Cost**', '**Human oversight**',
              'CONDITIONAL / NOT YET APPROVED',
              'consent', 'opt-out', 'human approval']:
    if label.lower() not in text.lower():
        failures.append('Wiki missing: ' + label)

try:
    tree = ET.parse(DIAGRAM)
    labels = ' '.join(n.get('value', '') for n in tree.findall('.//mxCell')).lower()
    for phrase in ['human approval', 'send-time eligibility',
                   'llm egress gateway', 'policy + eval gate',
                   'crm / consent ledger', 'batch dispatcher']:
        if phrase not in labels:
            failures.append('Diagram missing gate: ' + phrase)
except ET.ParseError as exc:
    failures.append(f'Invalid draw.io XML: {exc}')

if failures:
    sys.exit('Governance check FAILED:\n- ' + '\n- '.join(failures))
print('Governance documentation guardrail: PASS')
