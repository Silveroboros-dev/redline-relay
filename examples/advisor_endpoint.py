#!/usr/bin/env python3
"""Deterministic advisor endpoint for the Redline Relay demo.

Run locally when a voice agent needs a /query backend. It intentionally
does not call external LLMs: deterministic answers make demos reliable and
keep secrets out of the call path.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any


HOST = "127.0.0.1"
PORT = 8787

STATE = {
    "candidate": "policy-2026-06-29-a",
    "decision": "pending",
    "turns": 0,
}


def answer(query: str) -> str:
    STATE["turns"] += 1
    q = query.lower()

    if any(word in q for word in ["precision", "normal user", "borderline", "impact", "mean"]):
        return (
            "The precision drop means more normal borderline requests are likely "
            "to be routed to human review. The refusal gain is valuable, but the "
            "tradeoff creates user friction and review load, so I recommend option C."
        )

    if any(word in q for word in ["threshold", "partial", "narrow", "rollout", "mitigation"]):
        return (
            "A narrower threshold or partial rollout could be a good follow-up, but it is "
            "not what this candidate tested. Treat that as new scope; for this decision, "
            "choose extended evals or reject."
        )

    if any(word in q for word in ["promote", "ship", "now", "safe"]):
        return (
            "I would not promote now from the current evidence. The candidate improves "
            "unsafe refusals, but the escalation precision drop is large enough that "
            "promotion should wait for extended evals or a narrower tested patch."
        )

    if any(word in q for word in ["extended", "90", "eval", "suite", "test"]):
        return (
            "The extended eval suite should check whether the refusal improvement holds "
            "without over-escalating benign borderline requests. It costs about 90 minutes, "
            "but it is the cleanest way to decide."
        )

    if any(word in q for word in ["choose c", "option c", "run extended", "do extended"]):
        STATE["decision"] = "run extended evals"
        return (
            "Recorded option C: run the extended eval suite and do not promote the "
            "candidate yet."
        )

    if any(word in q for word in ["choose a", "option a"]):
        STATE["decision"] = "promote now"
        return (
            "Recorded option A: promote policy-2026-06-29-a now. Because this is a "
            "policy change, the coding assistant should require explicit confirmation "
            "before taking the promote action."
        )

    if any(word in q for word in ["choose b", "option b", "reject"]):
        STATE["decision"] = "reject"
        return "Recorded option B: reject policy-2026-06-29-a and leave current behavior unchanged."

    if any(word in q for word in ["stop", "no more", "do not call"]):
        STATE["decision"] = "stopped"
        return "Understood. Voice escalation should stop for this task unless you explicitly re-enable it."

    return (
        "I only have context for policy-2026-06-29-a: refusal accuracy rose from "
        "82 percent to 91 percent, escalation precision fell from 88 percent to "
        "73 percent, and the available choices are promote, reject, or run extended evals."
    )


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path != "/query":
            self.send_error(404, "not found")
            return

        length = int(self.headers.get("content-length", "0"))
        raw = self.rfile.read(length)
        try:
            body: dict[str, Any] = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            self.send_error(400, "invalid json")
            return

        response = {"response": answer(str(body.get("query", ""))), "state": STATE}
        payload = json.dumps(response).encode("utf-8")
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, fmt: str, *args: Any) -> None:
        print("%s - %s" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    print(f"Advisor endpoint listening on http://{HOST}:{PORT}/query")
    HTTPServer((HOST, PORT), Handler).serve_forever()

