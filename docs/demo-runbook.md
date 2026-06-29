# Demo Runbook

This runbook shows a phone escalation loop for a coding-agent policy decision.

## Preflight

```sh
export VOICE_ESCALATION_PHONE="+<verified destination number>"
export VOICE_ESCALATION_NAME="<name>"

command -v vb
vb auth login
vb agent list
vb agent use <caller-agent-id>
vb config show
vb config set --outbound-enabled true --accept-outbound-tos
```

Do not commit phone numbers or `.env` files.

## Advisor Endpoint

```sh
python3 examples/advisor_endpoint.py
```

For hosted voice platforms that need a public URL, expose the local endpoint through a temporary tunnel and configure:

```text
POST https://<temporary-tunnel-host>/query
```

## Evidence

Show:

```sh
sed -n '1,80p' examples/mock-fast-eval-report.txt
```

The decision packet:

```text
Decision needed: what should I do with policy-2026-06-29-a?
Stakes: refusal accuracy improved from 82% to 91%, but escalation precision dropped from 88% to 73%, so normal borderline requests may be routed to human review more often.
Choices: A promote now; B reject; C run the extended eval suite.
Recommendation: C, because cheap checks found a real tradeoff.
Default if unclear: do not promote.
```

## Call

```sh
vb prompt set -f agents/redline-relay/outbound-call-prompt.md
vb call "$VOICE_ESCALATION_PHONE" --name "${VOICE_ESCALATION_NAME:-Human}" --json
vb logs
```

## Suggested Human Questions

```text
Before I choose, what does the escalation precision drop mean for normal users?
```

```text
Could we promote it now with a narrower threshold instead?
```

Then decide:

```text
Choose C. Run the extended eval suite and do not promote now.
```

## After The Call

Record:

```text
Voice decision received: run extended eval suite; do not promote policy-2026-06-29-a.
VOICE_ESCALATION_STATE enabled=true stop_scope=none blocker=policy-2026-06-29-a status=settled decision=run_extended_evals session=<session_id>
Next action: run extended eval suite, leave candidate unpromoted.
```

Do not fake call IDs or session IDs in production demos.

