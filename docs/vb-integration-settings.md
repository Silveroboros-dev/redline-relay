# VocalBridge Integration Settings

These settings are intended for a demo caller that can delegate deeper questions to an app-side advisor endpoint.

## Integration Mode

Choose:

```text
An AI agent
```

Use this mode when the voice agent should delegate domain questions to a backend endpoint.

## When To Delegate

Use:

```text
Delegate substantive questions about policy-2026-06-29-a, fast eval metrics, repo/task state, changed files, command output, decision packet, tradeoffs, recommendation, safe default, or what the coding assistant should do next. Do not delegate greetings, hearing checks, repeating A/B/C choices, capturing the final A/B/C decision, confirmations, or call control. If asked for secrets, credentials, private data, or unrelated topics, refuse briefly and return to the A/B/C decision.
```

## Speech

- Speak responses verbatim: on.
- Thinking sound: off for recordings.
- Ambient sound: off.
- Continuous speech: off.
- Silence duration: around 600 ms for natural phone pauses.
- Max call duration: 5 to 10 minutes for demos.

## Backend

Run:

```sh
python3 examples/advisor_endpoint.py
```

Expose it through a temporary tunnel and configure:

```text
POST https://<temporary-tunnel-host>/query
```

