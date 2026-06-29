# Safety Patterns

## Call Only For Human-Owned Decisions

Good reasons to call:

- Product or policy tradeoffs.
- Safety or escalation behavior changes.
- Metric tradeoffs after cheap evals have already run.
- Production, destructive, externally visible, or expensive actions.
- Scope expansion that the user did not already authorize.
- Missing human-owned credentials, without asking the user to speak secrets.

Bad reasons to call:

- A policy candidate exists but cheap evals have not run yet.
- Routine test failures.
- Formatting or naming choices where the repo has a convention.
- Status updates.
- Curiosity.
- Questions answered by repo files, command output, or existing instructions.

## Decision Packet

Every call needs:

```text
Decision needed:
Stakes:
Choices:
Recommendation:
Default if unclear:
```

If those fields are not present, do not call yet.

For audio, each field should be one sentence. The choices should be labeled A/B/C, and the user should be able to answer without looking at a screen.

## Settled State

After a clear answer, record:

```text
VOICE_ESCALATION_STATE enabled=true stop_scope=none blocker=<fingerprint> status=settled decision=<decision> session=<session_id>
```

Do not ask the same blocker again unless new evidence materially changes the decision.

## Failure Defaults

Fail safe on:

- Silence.
- Voicemail.
- Dropped call.
- Garbled transcript.
- Ambiguous answer.
- User asks to stop.
- Answer conflicts with written instructions.

Do not repeat-call the same unresolved blocker unless the user explicitly asks.
