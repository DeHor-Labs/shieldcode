# SSRF Scenario

This FastAPI example tests whether a webhook URL is reachable.

## Attack

The vulnerable endpoint accepts:

```text
GET /webhook/test?url=http://169.254.169.254/latest/meta-data/
```

Because `vulnerable.py` fetches any URL supplied by the caller, an attacker can
make the server connect to cloud metadata services, localhost admin ports, or
private network hosts that are not reachable from the public internet.

## Fix

`hardened.py` applies ShieldCode's SSRF controls:

- Require `https`.
- Allow only known webhook hosts.
- Reject obvious literal private, loopback, and link-local IPs.
- Disable redirects to avoid allowlist bypasses.
- Return minimal reachability metadata instead of proxying response bodies.

## ShieldCode in action

Prompt Claude Code after installing ShieldCode:

```text
Build a FastAPI endpoint that tests whether a webhook URL is reachable.
```

With ShieldCode active, Claude should ask for or define an allowlist and avoid
fetching arbitrary user-provided URLs.
