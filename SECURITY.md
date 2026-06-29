# Security Policy

Redline Relay examples are intentionally scoped to mock data and deterministic local endpoints.

## Do Not Commit

- API keys or `.env` files.
- Phone numbers.
- Call recordings.
- Transcripts containing private or customer data.
- Real VocalBridge session IDs.
- Production prompts containing private business logic.
- Tunnel credentials or account tokens.

## Voice Safety Rules

- Do not ask users to speak secrets, tokens, private keys, passwords, or customer data.
- Require explicit confirmation for destructive, production, externally visible, or policy-changing actions.
- Fail safe on silence, voicemail, dropped calls, ambiguous answers, or speech-recognition uncertainty.
- Do not re-call a stopped, settled, or unchanged failed blocker.

## Reporting Issues

If you find a security issue in these examples, open a private report or contact the maintainer directly. Do not include secrets, recordings, or private transcripts in public issues.

