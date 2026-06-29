# Architecture

Redline Relay separates the voice layer from the product brain.

```text
Coding/product agent
  -> detects human-owned decision
  -> prepares decision packet
  -> sets voice-agent prompt
  -> starts outbound call

Voice agent
  -> states the decision, stakes, choices, recommendation, and safe default
  -> captures A/B/C or a short instruction
  -> delegates substantive follow-up questions to /query
  -> confirms the final decision

Advisor endpoint
  -> answers domain questions from current task context
  -> does not mutate production systems
  -> returns concise responses for speech

Coding/product agent
  -> records settled state
  -> executes only the selected path
```

## Boundaries

The voice agent should be the mouth and ears. The product agent or backend advisor should own domain reasoning, repo state, metrics, and current task context.

The advisor endpoint in this repo is deterministic on purpose. In production, it can be replaced with a retrieval-backed or LLM-backed service, but the interface should stay narrow:

```http
POST /query
Content-Type: application/json

{"query":"What does the precision drop mean for normal users?"}
```

```json
{"response":"Short answer for the voice agent to speak."}
```

## Non-Goals

- No direct deployment, database mutation, billing action, or credential handling from the voice layer.
- No spoken secrets.
- No open-ended browsing during critical decisions unless the workflow explicitly requires it.

