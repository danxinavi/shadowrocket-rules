#!/usr/bin/env python3
"""Daily maintenance for this repo (run by GitHub Actions, see .github/workflows/daily-check.yml).

What it does, in order:
1. Deterministic cleaning (safe, no false positives):
   - domains/*.txt: drop duplicates, drop invalid domains, drop IP literals.
   - shadowrocket.conf [MITM] hostname: drop duplicates, drop IP literals,
     drop mid-wildcards (only "*.domain" and "-*.domain" / "-domain" are valid).
2. Dead-domain tracking (conservative, avoids one-day network flapping):
   - DNS-resolve every domain in domains/*.txt and every MITM hostname
     (wildcards stripped to their base domain for the check).
   - A domain that returns NXDOMAIN / no address increments its counter in
     scripts/dead_tracker.json; any success resets it to 0.
   - Only a domain with counter >= 3 (i.e. dead 3 days in a row) is deleted.
   - Timeouts / other DNS errors do NOT increment the counter.
3. Regenerate all client files with scripts/build.py (build.py appends the
   cleaned MITM list from mitm-hostname.txt to shadowrocket.conf).

Deleted domains are listed in the commit message by the Action, and can be
restored from git history. Nothing here invents new domains: adding a new
service is still a human decision (edit domains/*.txt, or tell Ren).
"""
import json
import re
import socket
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRACKER = ROOT / "scripts" / "dead_tracker.json"
IP_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")
DOMAIN_RE = re.compile(r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63}(?<!-))*$")


def is_ip(s):
    return bool(IP_RE.match(s))


def valid_domain(s):
    return bool(DOMAIN_RE.match(s)) and "." in s


def clean_hostname_list(items):
    """Return (cleaned, removed) for a MITM hostname list."""
    seen, cleaned, removed = set(), [], []
    for raw in items:
        item = raw.strip()
        if not item:
            continue
        neg = item.startswith("-")
        core = item[1:] if neg else item
        key = item.lower()
        if key in seen:
            removed.append((item, "duplicate"))
            continue
        seen.add(key)
        if is_ip(core):
            removed.append((item, "ip-literal"))
            continue
        if "*" in core and not core.startswith("*."):
            removed.append((item, "mid-wildcard"))
            continue
        base = core[2:] if core.startswith("*.") else core
        if not valid_domain(base):
            removed.append((item, "invalid-domain"))
            continue
        cleaned.append(item)
    return cleaned, removed


def dns_dead(domain):
    """True only on a definite NXDOMAIN / no-address result, else False."""
    try:
        socket.getaddrinfo(domain, 80, proto=socket.IPPROTO_TCP)
        return False
    except socket.gaierror as e:
        # EAI_NONAME = name does not resolve. Anything else (timeout, temp
        # failure) is treated as "unknown", not dead.
        return e.errno == socket.EAI_NONAME
    except Exception:
        return False


def main():
    tracker = json.loads(TRACKER.read_text()) if TRACKER.exists() else {}
    removed_all = []

    # --- domains/*.txt ---
    for name in ("direct", "proxy", "reject"):
        path = ROOT / "domains" / f"{name}.txt"
        lines = path.read_text().splitlines()
        header = [l for l in lines if l.strip().startswith("#")]
        domains = [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]
        seen, kept = set(), []
        for d in domains:
            if d.lower() in seen or is_ip(d) or not valid_domain(d):
                removed_all.append((d, "domains-clean"))
                continue
            seen.add(d.lower())
            kept.append(d)
        # Dead tracking for the kept domains
        final = []
        for d in kept:
            if dns_dead(d):
                tracker[d] = tracker.get(d, 0) + 1
                if tracker[d] >= 3:
                    removed_all.append((d, f"dns-dead-{tracker[d]}d"))
                    tracker.pop(d, None)
                    continue
            else:
                tracker.pop(d, None)
            final.append(d)
        path.write_text("\n".join(header + final) + "\n")

    # --- MITM hostname in mitm-hostname.txt (build.py appends it to the conf) ---
    mitm_path = ROOT / "mitm-hostname.txt"
    if mitm_path.exists():
        items = [l.strip() for l in mitm_path.read_text().splitlines()
                 if l.strip() and not l.strip().startswith("#")]
        cleaned, removed = clean_hostname_list(items)
        removed_all.extend(removed)
        # Dead tracking for MITM hostnames (base domain only, wildcards kept as-is)
        final = []
        for item in cleaned:
            neg = item.startswith("-")
            core = item[1:] if neg else item
            base = core[2:] if core.startswith("*.") else core
            key = f"mitm:{base}"
            if dns_dead(base):
                tracker[key] = tracker.get(key, 0) + 1
                if tracker[key] >= 3:
                    removed_all.append((item, f"mitm-dns-dead-{tracker[key]}d"))
                    tracker.pop(key, None)
                    continue
            else:
                tracker.pop(key, None)
            final.append(item)
        mitm_path.write_text("\n".join(final) + "\n")

    TRACKER.write_text(json.dumps(tracker, indent=2, sort_keys=True) + "\n")
    print(f"removed={len(removed_all)}")
    for item, reason in removed_all:
        print(f"  - {item} ({reason})")
    print(f"tracker-pending={len(tracker)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
