# Demo Runbook

This runbook shows the official-style phone escalation loop: a coding agent prepares the decision packet, Vocal Bridge calls the human, and the coding agent resumes from the spoken decision.

## Preflight

```sh
export VOICE_ESCALATION_PHONE="+<verified destination number>"
export VOICE_ESCALATION_NAME="<name>"

command -v vb
vb auth login
vb agent list
vb agent use "Redline Relay"
vb config show
vb config set --outbound-enabled true --accept-outbound-tos
vb config set --background-enabled false --web-search-enabled false --debug-mode true --hangup-enabled true
```

Do not commit phone numbers or `.env` files.

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

## Not Used In This Demo

- AI Agent Integration.
- Custom API tools.
- Cloudflare tunnels.
- Live app-side advisor endpoints.

Those are useful future product integrations, but the challenge-style escalation loop does not require them.
