---
name: voice-escalation
description: Use this skill when an async coding assistant is blocked on a genuine human-owned decision and should escalate by phone through Vocal Bridge using `vb call`. It defines when to call, when not to call, how to construct the spoken decision packet, how to parse the voice response, and how to fail safely on no-answer, timeout, or ambiguity.
---

# Voice Escalation

Use Vocal Bridge as a decision channel, not as a status channel. Your job is to keep building independently until a decision is genuinely owned by the human. Call only when the work is blocked and continuing without the human would be unsafe, irreversible, out of scope, or based on a product/business tradeoff you cannot infer from the repo or task.

## State First

Before considering any call, reconstruct voice-escalation state from the current conversation, terminal notes, and prior call logs. Do not rely on memory alone.

Track this compact ledger:

- `enabled`: `true` unless the user has asked to stop voice escalation.
- `stop_scope`: `none`, `current_blocker`, `current_task`, or `session`.
- `called_blockers`: normalized blocker fingerprints already called about.
- `settled_decisions`: blocker fingerprints with the user's decision.
- `failed_blockers`: blocker fingerprints where the last call was no-answer, timeout, ambiguous, failed, or voicemail.
- `last_session_id`: latest Vocal Bridge call session ID, if known.

After every call, stop request, failed call, or clear decision, write a compact state note in the terminal or final response:

```text
VOICE_ESCALATION_STATE enabled=<true|false> stop_scope=<scope> blocker=<fingerprint> status=<called|settled|failed|stopped> decision=<short decision or none> session=<id or none>
```

At the start of the next turn, parse the latest `VOICE_ESCALATION_STATE` note before acting. If state is missing, reconstruct it from the conversation: user stop requests, prior questions, prior answers, and call outcomes still count.

## Stop And Settled-Question Rules

Make a stop request stick. If the user says "stop calling", "do not call me", "no more calls", "use terminal only", or equivalent, set `enabled=false` for the current task or broader stated scope. Do not call again until the user explicitly re-enables voice escalation with language like "you may call again" or "resume voice escalation."

Never re-ask a settled question. If the human already chose, rejected, approved, or deferred a blocker, record it in `settled_decisions` and continue on that path. Do not ask again unless there is a material change: new stakes, new evidence, new options, or the user explicitly reopens the decision.

Never re-call an unchanged failed blocker. If a blocker is in `failed_blockers`, report the safe default and continue only with reversible work unless the user explicitly asks for another call.

## Core Rule

Before calling, ask:

1. Is there a concrete decision that blocks the next action?
2. Is the decision owned by the human rather than recoverable from repo context, tests, docs, or ordinary engineering judgment?
3. Would proceeding without the answer create meaningful risk, irreversible change, wasted work, external cost, credential exposure, or scope drift?
4. Have I already tried the cheap local validation or recovery steps?
5. Is voice escalation still enabled for this task?
6. Is this blocker absent from `called_blockers`, `settled_decisions`, and `failed_blockers` unless materially changed?

Call only if all six answers are yes.

## Call Immediately For

- Destructive or hard-to-reverse operations: deleting data, force pushing, rewriting published history, running migrations against shared/prod data, disabling auth, rotating credentials, or deploying without rollback.
- Product or architecture tradeoffs where two or more valid paths have materially different user, cost, latency, reliability, privacy, or maintenance consequences.
- Eval, policy, or guardrail changes where one metric improves but another user-facing, safety, escalation, or operational metric regresses, after the cheap/local evals have already run.
- Plan approval before committing to a broad multi-file change when the user's request does not already authorize that plan.
- Scope expansion: a required plan change that exceeds the user's original request, budget, deadline, or blast radius.
- Missing human-owned credentials or access when the task explicitly depends on them. Do not ask the user to speak secrets. Ask whether to pause, use a mock/offline path, or wait for them to set the credential in the terminal.
- Legal, privacy, security, or compliance choices that need user acceptance.
- Repeated blocker after local recovery has failed and the remaining options have different user-visible tradeoffs.

## Do Not Call For

- Routine test failures, lint warnings, type errors, formatting choices, naming choices, merge conflicts you can resolve safely, or dependency issues with obvious local fixes.
- Eval or policy changes where the next step is an obvious cheap validation run. Run the fast evals first; call only when the remaining decision is promote/reject/spend time on extended evals, or when metric tradeoffs are genuinely human-owned.
- Package install or network failures until you have tried the normal cheap recovery path: retry once, inspect the error, check the lockfile/package manager, try the repo's documented install command, and look for an offline or cached path. Call only if the remaining choices require credentials, paid services, scope changes, or a user-visible tradeoff.
- Status updates, progress reports, logs, curiosity, or "just checking in."
- Questions answered by existing repo files, command output, official docs already available in context, or the user's original instructions.
- Preference choices with low consequence where the repo has a convention. Follow the convention and continue.
- A failed call, garbled answer, or timeout for the same blocker. Report the unresolved blocker in the terminal and stop or continue only along a reversible safe path.
- Situations where there is no concrete action you would take immediately after the answer.

## Pre-Call Packet

Construct a decision packet before invoking `vb call`. Keep it short enough to speak in 25 to 40 seconds. If you cannot state the decision, stakes, and options, do not call yet.

Required fields:

- `decision`: the exact decision needed, in one sentence.
- `blocker`: one sentence describing why work cannot safely continue.
- `stakes`: the practical consequence of choosing wrong.
- `evidence`: the shortest concrete evidence available, such as command output, changed files, candidate ID, or eval deltas.
- `options`: two or three labeled options with tradeoffs.
- `recommendation`: your default recommendation, if you have one, with one reason.
- `question`: one explicit question the human can answer by saying the option label or a short phrase.
- `safe_default`: what you will do if the call fails or the answer is unclear. Usually "do not proceed with the risky action."

The packet must be answerable from audio alone. Lead with the decision, then stakes, then choices. Include only facts needed to decide. Do not include secrets, tokens, customer data, private keys, full stack traces, or long diffs in the spoken packet. Avoid filler such as background history, apologies, progress narration, or "just checking in."

## Communication Contract

Every voice escalation, including the terminal pre-call note and spoken call, must have this shape:

```text
Decision needed: <one sentence>
Stakes: <one sentence explaining what goes wrong if the choice is wrong>
Choices: A <action + tradeoff>; B <action + tradeoff>; optional C <action + tradeoff>
Recommendation: <option label + one reason, or "none">
Default if unclear: <safe default>
```

This is a hard requirement. If any of `Decision needed`, `Stakes`, or `Choices` is missing, rewrite the packet before calling. If the choices are not labeled, label them before calling. If the stakes are only "I am blocked" or "the task cannot continue", they are not stakes; state the practical consequence for users, safety, cost, time, or scope.

Keep each field to one sentence. Prefer concrete nouns, candidate IDs, metric deltas, file names, and command names over narrative. Do not mention that you are "checking in", "making progress", "almost done", or "calling with an update."

## Calling Procedure

Assume the Vocal Bridge CLI is already installed, authenticated, and configured with a caller agent. Prefer a configured phone number in `VOICE_ESCALATION_PHONE`; if it is absent, check `VOCAL_BRIDGE_ESCALATION_PHONE`. If neither is set, do not invent a number. Print the decision packet and ask for terminal input instead.

1. Create a temporary prompt file outside the repo, for example `/tmp/voice_escalation_call.md`.
2. Put the decision packet in the prompt using the call script below.
3. Run `vb prompt set -f /tmp/voice_escalation_call.md` so the selected Vocal Bridge caller agent has the current context.
4. Resolve the phone number with `phone="${VOICE_ESCALATION_PHONE:-${VOCAL_BRIDGE_ESCALATION_PHONE:-}}"`.
5. If `$phone` is empty, do not run `vb call`. Print the decision packet and ask for terminal input.
6. Run `vb call "$phone" --name "${VOICE_ESCALATION_NAME:-Human}" --json`.
7. Stream or inspect the call with `vb debug` or `vb logs` until the session ends or times out.
8. Parse the human's answer from the transcript or structured call output.
9. Record the session ID in the terminal if available, because the challenge submission verifies the demo call by session ID.

If a command fails due to missing CLI auth, missing phone config, network failure, or Vocal Bridge error, do not retry repeatedly. Report the exact failure and use the safe default.

## Call Script

Use this structure for the caller prompt. Do not add extra background outside this structure:

```text
You are a Vocal Bridge voice escalation agent calling the developer because their coding assistant is blocked on a decision.

Be concise, calm, and explicit. Do not sound like a status update. The goal is one decision.

Say:
"Hi, this is your coding assistant.
Decision needed: {decision}
I cannot safely continue because {blocker}
Stakes: {stakes}
Evidence: {evidence}
Choices: A: {option_a}. B: {option_b}. {optional_option_c}
Recommendation: {recommendation}.
Please answer A, B, C, or a short instruction. If unclear, I will {safe_default}."

After the human answers, confirm the interpreted decision in one sentence and end the call. If the human asks for details, answer briefly from the packet only. If the answer is unclear, ask once for clarification. If it is still unclear, say you will not proceed and end the call.
```

## Response Handling

Treat the voice answer as valid only when it maps clearly to one option or to an explicit instruction that is safe and within scope.

Valid response examples:

- "A", "option A", "use the lock", "go sequential", "do not deploy", "pause and wait for me."
- A direct approval for a named risky action: "approve the migration against staging" or "promote candidate policy-2026-06-29-a." For production, destructive, externally visible, or policy/guardrail changes, require the action name and target to be spoken or otherwise unambiguous.

Invalid or unsafe response examples:

- "Whatever you think", when the point of the call is a human-owned tradeoff.
- Silence, voicemail, transcript missing, dropped call, no recording, or speech recognition uncertainty.
- Any answer that introduces a new out-of-scope task, asks for secret handling by voice, or conflicts with the user's written instructions.

For destructive, production, externally visible, or policy/guardrail actions, require a specific approval that names the action and target. If the answer is "yes" but the action or target is ambiguous, ask once for confirmation. If it remains ambiguous, fail safe.

After a valid answer:

1. Write a terminal note: `Voice decision received: <decision>. Proceeding with <next action>.`
2. Update `VOICE_ESCALATION_STATE` with `status=settled` and the blocker fingerprint.
3. Execute only the selected path. Do not broaden scope.
4. Add tests or verification proportional to the risk.
5. If the decision affects architecture, data, deployment, or security, leave a short implementation note in the final response.

After an invalid, missing, or ambiguous answer:

1. Write a terminal note with the call status and safe default.
2. Update `VOICE_ESCALATION_STATE` with `status=failed` and the blocker fingerprint.
3. Do not take destructive, irreversible, costly, or scope-expanding action.
4. Do not call again for the same blocker unless the user explicitly asks.
5. Continue only with reversible investigation or stop and wait for terminal input.

## Examples

Call:

- "Decision needed: whether to remove the legacy export column. Stakes: removing it may break a customer-facing export, while preserving it adds compatibility code. Choices: A preserve compatibility; B remove it now. Recommendation: A because the breakage is user-visible. Default if unclear: keep the column."
- "Decision needed: choose the concurrency design. Stakes: the wrong choice either adds lock latency or risks duplicate processing. Choices: A distributed lock with latency overhead; B sequential processing with lower throughput. Recommendation: A if correctness matters more than throughput. Default if unclear: do not change concurrency."
- "Decision needed: how to handle missing production verification. Stakes: speaking or guessing credentials is unsafe, but skipping live verification leaves deployment risk. Choices: A pause for terminal credential setup; B use a mock path; C continue with local tests only. Recommendation: A for a production path. Default if unclear: pause."
- "Decision needed: whether to expand the requested rewrite. Stakes: the full plan touches auth, billing, and data export, increasing review and regression risk. Choices: A proceed with full multi-file plan; B narrow to the original scope. Recommendation: B unless the user explicitly accepts the blast radius. Default if unclear: narrow scope."
- "Decision needed: what to do with policy-2026-06-29-a. Stakes: it improves unsafe-request refusal from 82% to 91% but drops escalation precision from 88% to 73%, which may over-escalate normal users. Choices: A promote now; B reject; C spend 90 minutes on extended evals. Recommendation: C because cheap checks already found a real tradeoff. Default if unclear: do not promote."

Do not call:

- "Three lint warnings remain." Fix them or document if irrelevant.
- "`npm install` failed once." Try the normal local recovery path.
- "A policy candidate exists but fast evals have not run." Run the cheap eval first.
- "Tabs or spaces?" Follow the repo convention.
- "I finished half the work." Keep working or report at the end.
