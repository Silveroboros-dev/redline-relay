# Safety Patterns

## Call Only For Human-Owned Decisions

Good reasons to call:

- Product or policy tradeoffs.
- Safety or escalation behavior changes.
- Production, destructive, externally visible, or expensive actions.
- Scope expansion that the user did not already authorize.
- Missing human-owned credentials, without asking the user to speak secrets.

Bad reasons to call:

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

