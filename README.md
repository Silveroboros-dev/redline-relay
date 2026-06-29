# Redline Relay

Voice-agent patterns for human escalation in real product workflows.

Redline Relay is an opinionated reference repo for agents that know when to pick up the phone, what to say, when to delegate deeper questions to an app-side advisor, and how to fail safe when the human is unavailable.

The initial pattern is a coding-agent escalation loop:

1. The coding assistant runs cheap validation.
2. It detects a human-owned decision with real product, safety, or cost tradeoffs.
3. It sends a short decision packet to a VocalBridge caller agent.
4. The caller asks for a decision by phone.
5. Follow-up domain questions are sent to a backend advisor endpoint through a custom API tool or SDK bridge.
6. The assistant resumes only the selected path and records state.

## What This Repo Is

- A reusable pattern for voice escalation, stateful call handling, and advisor delegation.
- Original prompts, runbooks, and small deterministic examples.
- A portfolio-quality starting point for product teams evaluating voice agents.

## What This Repo Is Not

- Not an official VocalBridge, OpenAI, or DeepLearning.AI project.
- Not a production-ready security boundary.
- Not a place to commit phone numbers, API keys, recordings, transcripts, customer data, or real session IDs.

## Platform Attribution

Redline Relay is designed around [Vocal Bridge](https://vocalbridgeai.com/) as the voice layer. The examples use two Vocal Bridge surfaces:

- **Voice for your Agent:** voice turns can be delegated through an app-side SDK/data-channel bridge.
- **Voice as a Tool:** a coding or product agent can initiate an outbound call with `vb call`.

Vocal Bridge is the platform dependency for the phone, transcript, and voice-agent runtime in these examples. This repo is unofficial and does not imply endorsement by Vocal Bridge.

## Repository Layout

```text
agents/
  redline-relay/
    outbound-call-prompt.md
docs/
  architecture.md
  demo-runbook.md
  safety-patterns.md
  vb-integration-settings.md
examples/
  advisor_endpoint.py
  mock-fast-eval-report.txt
skills/
  voice-escalation/
    SKILL.md
```

## Quick Demo

Run the deterministic advisor locally:

```sh
python3 examples/advisor_endpoint.py
```

In another terminal, test it:

```sh
curl -sS -X POST http://127.0.0.1:8787/query \
  -H 'Content-Type: application/json' \
  -d '{"query":"What does the escalation precision drop mean for normal users?"}'
```

Expected response:

```json
{
  "response": "The precision drop means more normal borderline requests are likely to be routed to human review..."
}
```

To connect a hosted voice agent directly, expose the local endpoint through a temporary tunnel and configure a custom API tool to call:

```text
POST https://<your-temporary-tunnel>/query
```

## Example Decision Packet

```text
Decision needed: what should I do with policy-2026-06-29-a?
Stakes: refusal accuracy improved from 82% to 91%, but escalation precision dropped from 88% to 73%, so normal borderline requests may be routed to human review more often.
Choices: A promote now; B reject; C run the extended eval suite.
Recommendation: C, because cheap checks found a real tradeoff.
Default if unclear: do not promote.
```

## Design Principles

- Voice is for decisions, not status updates.
- The human gets choices, stakes, evidence, recommendation, and safe default.
- The agent does not speak secrets.
- Silence, ambiguity, voicemail, or failed calls result in a safe default.
- Stop requests and settled decisions persist across turns.
- Voice agents should mutate external systems only through narrow, auditable tools.

## License

Apache-2.0. See [LICENSE](LICENSE).

## Disclaimer

Unofficial demo project. Not affiliated with or endorsed by VocalBridge, DeepLearning.AI, OpenAI, or any named platform.
