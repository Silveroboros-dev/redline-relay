# VocalBridge Integration Settings

These settings are intended for a demo caller that can delegate deeper questions to an app-side advisor endpoint.

## Direct Demo Mode

Choose:

```text
Custom API Tool
```

Use this mode when the voice agent should call a direct HTTP advisor endpoint.

## Important Distinction

AI Agent Integration is not a plain webhook URL. If the UI only gives you "When to delegate" and no URL field, do not paste the advisor URL there. AI Agent Integration expects an app connected through the Vocal Bridge SDK/data channel to receive `query_agent` and send `agent_response`.

For a direct hosted endpoint, use a Custom API Tool.

## Custom API Tool

Create:

```text
Name: ask_coding_advisor
Method: POST
URL: https://<temporary-tunnel-host>/query
Headers: Content-Type: application/json
Auth: none for this local demo
Request body: {"query":"{{query}}"}
Response field to speak: response
```

Tool instruction:

```text
When the developer asks a substantive follow-up about policy-2026-06-29-a, the eval metrics, tradeoff, recommendation, safe default, or what the coding assistant should do next, call ask_coding_advisor. Read the response verbatim. Do not call it for greetings, hearing checks, repeating A/B/C choices, final decision capture, confirmations, or call control.
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

Expose it through a temporary tunnel and configure the Custom API Tool URL:

```text
POST https://<temporary-tunnel-host>/query
```
