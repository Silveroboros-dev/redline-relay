# Codex Demo Prompts

These prompts make a Codex Desktop recording repeatable. They keep the phone call as a decision channel and the coding agent as the stateful worker.

## Opening Prompt

```text
Run the Redline Relay phone voice-escalation demo.

Read examples/mock-fast-eval-report.txt and apply skills/voice-escalation/SKILL.md. Show concise terminal evidence first, then prepare the decision packet for the Vocal Bridge Redline Relay agent.

Important constraints:
- This is a PSTN phone-call demo through Vocal Bridge.
- Do not run vb call, start a call, or dial anything until I type exactly: DIAL NOW.
- Do not claim Vocal Bridge is live-querying Codex during the call.
- Do not promote policy-2026-06-29-a unless I explicitly approve it by voice.
- If the phone call fails, is silent, or gives an unclear answer, use the safe default: do not promote.
- After I paste the completed Vocal Bridge session ID and selected decision, treat that decision as settled. Do not re-ask the same blocker.
- Do not print my personal phone number on screen.

Scenario:
- candidate: policy-2026-06-29-a
- decision options: A promote now, B reject, C run extended evals before deciding
- recommendation: C

What I need from you now:
1. Show the fast eval summary from examples/mock-fast-eval-report.txt.
2. State the decision packet in a form suitable for voice.
3. Set VOICE_ESCALATION_STATE with status=called, decision=none, and session=none.
4. Tell me you are ready and waiting for DIAL NOW before making the phone call.
```

## End-Of-Call Prompt

```text
Voice session completed.

Decision: C, run the extended eval suite and do not promote now.
Vocal Bridge session ID: <session_id>

Continue from the settled voice decision. Do not re-ask the policy decision. Show the updated VOICE_ESCALATION_STATE and the next action the coding agent will take.
```

## Expected Settled State

```text
Voice decision received: run extended eval suite; do not promote policy-2026-06-29-a.

VOICE_ESCALATION_STATE enabled=true stop_scope=none blocker=policy-2026-06-29-a status=settled decision=run_extended_evals session=<session_id>

Next action: keep policy-2026-06-29-a unpromoted and run the extended eval suite. I will not re-ask this settled blocker.
```
