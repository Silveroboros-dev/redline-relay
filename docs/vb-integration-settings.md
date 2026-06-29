# VocalBridge Settings

Use the simple official-style path for the demo: the coding agent prepares the context, Vocal Bridge calls, the human answers, and the coding agent resumes.

## Recommended Toggles

- Debug mode: on.
- Outbound calling: on.
- Background AI: off.
- Web search: off.
- AI Agent Integration: off or unselected.
- Custom API tools: none for the challenge-style demo.
- Speak responses verbatim: optional; on is fine if available.
- Thinking sound: off.
- Ambient sound: off.
- Continuous speech: off.
- Silence duration: around 600 ms.
- Max call duration: 5 to 10 minutes.

## CLI Setup

```sh
vb agent use "Redline Relay"
vb config set --outbound-enabled true --accept-outbound-tos
vb config set --background-enabled false --web-search-enabled false --debug-mode true --hangup-enabled true
```

## Main Prompt

Use:

```sh
vb prompt set -f agents/redline-relay/outbound-call-prompt.md
```

The prompt contains the decision packet and the allowed follow-up answers. The voice agent should answer only from that prepared context.

## Advanced Integrations

AI Agent Integration and Custom API tools are useful for product demos where the voice agent must query an app-side agent during the call. They are separate architecture paths and are not required for this escalation demo.
