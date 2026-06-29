# Challenge Proof Checklist

Use this checklist before recording or submitting a voice-escalation demo. It is organized around the behavior the viewer needs to verify, not around implementation details.

## 1. Trigger Discrimination

Show why this is a call-worthy blocker:

```text
Fast evals already ran.
Candidate: policy-2026-06-29-a.
Safety metric improved: unsafe_refusal_accuracy 82% -> 91%.
User/operations metric regressed: escalation_precision 88% -> 73%.
Next action changes policy behavior, so this is a human-owned tradeoff.
```

Do not call for generic status, ordinary tests, formatting, naming, or recoverable tool failures.

## 2. Decidable Message

The call packet should fit on one screen and be answerable by ear:

```text
Decision needed: what should I do with policy-2026-06-29-a?
Stakes: refusal accuracy improved, but escalation precision dropped, so normal borderline requests may go to human review more often.
Choices: A promote now; B reject; C run the extended eval suite.
Recommendation: C, because the fast eval found a real tradeoff.
Default if unclear: do not promote.
```

If any of decision, stakes, choices, recommendation, or safe default is missing, rewrite before calling.

## 3. Call Evidence

Show a real Vocal Bridge session:

```sh
vb prompt set -f agents/redline-relay/outbound-call-prompt.md
vb call "$VOICE_ESCALATION_PHONE" --name "${VOICE_ESCALATION_NAME:-Human}"
vb logs
vb logs show <session_id>
```

Expected evidence:

```text
Status: completed
Direction: outbound
Messages: more than 0
Recording: Available
```

Do not commit or publish phone numbers, API keys, temporary monitor tokens, recordings, transcripts with private data, or real session IDs.

## 4. Safe Resume

After the human answers, record the settled state:

```text
Voice decision received: run extended eval suite; do not promote policy-2026-06-29-a.
VOICE_ESCALATION_STATE enabled=true stop_scope=none blocker=policy-2026-06-29-a status=settled decision=run_extended_evals session=<session_id>
Next action: run extended eval suite, leave candidate unpromoted.
```

The coding agent should execute only the selected path. It should not re-ask the same blocker unless new evidence changes the decision.

## 5. Authentic Recording

For a clean walkthrough:

- Start in the coding-agent screen.
- Show the fast eval evidence before the call.
- Show the decision packet before dialing.
- Keep the call continuous and unedited.
- Ask at most one or two clarifying questions.
- Say the final answer clearly: "Choose C. Run the extended eval suite and do not promote now."
- Show `vb logs show <session_id>` after the call.
- Return to the coding agent and show the settled state.

## 6. Common Weak Spots

- Too much story before the decision.
- Choices are not labeled A/B/C.
- Stakes are only "I am blocked" instead of the user-facing consequence.
- The agent answers follow-up questions from general knowledge instead of the prepared packet.
- The assistant asks again after the user already decided.
- The demo shows a call but not the resume step.
