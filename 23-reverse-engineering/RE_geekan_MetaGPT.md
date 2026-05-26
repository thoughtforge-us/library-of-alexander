# MetaGPT — Reverse Engineering Analysis

**Repo**: github.com/geekan/MetaGPT  
**Stars**: 68,287  
**Language**: Python  
**Category**: AI Agents

## Architecture

MetaGPT is a multi-agent framework that simulates a software company. Agents play roles (Product Manager, Architect, Engineer, QA) and collaborate to produce software.

## Key Design Patterns

1. **Role-playing agents** — Each agent has a specific role with defined responsibilities
2. **SOP-based workflows** — Standard Operating Procedures define how agents interact
3. **Structured outputs** — Agents produce structured documents (PRD, architecture, code)
4. **Shared message bus** — Agents communicate through a shared message system
5. **Quality gates** — Each stage has validation before proceeding to next

## What We Can Learn

- Role-playing creates natural specialization and accountability
- SOPs make agent workflows predictable and debuggable
- Structured outputs are easier to validate than free-form text
- Shared message bus enables decoupled agent communication
- Quality gates prevent error propagation through the pipeline

## Integration Ideas

- Implement role-playing for our fleet agents (researcher, coder, reviewer)
- Use SOP-based workflows for complex multi-step tasks
- Add structured output validation to agent responses
- Create shared message bus for inter-agent communication
- Add quality gates between pipeline stages
