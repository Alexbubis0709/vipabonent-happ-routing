#!/usr/bin/env python3
import argparse
import base64
import json
import time
from pathlib import Path


def read_lines(path: str, prefix: str | None = None) -> list[str]:
    p = Path(path)
    if not p.exists():
        return []
    out: list[str] = []
    for raw in p.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if prefix and ":" not in line:
            line = prefix + line
        out.append(line)
    return out


def dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", default="config/routing-template.json")
    ap.add_argument("--outdir", default="HAPP")
    ap.add_argument("--last-updated", default=str(int(time.time())))
    args = ap.parse_args()

    cfg = json.loads(Path(args.template).read_text(encoding="utf-8"))
    cfg["LastUpdated"] = str(args.last_updated)

    cfg["DirectSites"] = dedupe(cfg.get("DirectSites", []) + read_lines("custom/direct-domains.txt", "domain:"))
    cfg["DirectIp"] = dedupe(cfg.get("DirectIp", []) + read_lines("custom/direct-cidr.txt"))
    cfg["ProxySites"] = dedupe(cfg.get("ProxySites", []) + read_lines("custom/proxy-domains.txt", "domain:"))
    cfg["ProxyIp"] = dedupe(cfg.get("ProxyIp", []) + read_lines("custom/proxy-cidr.txt"))

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    pretty = json.dumps(cfg, ensure_ascii=False, indent=2) + "\n"
    compact = json.dumps(cfg, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    payload = base64.b64encode(compact).decode("ascii")

    (outdir / "ROUTING.JSON").write_text(pretty, encoding="utf-8")
    (outdir / "ROUTING.DEEPLINK").write_text(f"happ://routing/add/{payload}\n", encoding="utf-8")
    (outdir / "ROUTING.ONADD.DEEPLINK").write_text(f"happ://routing/onadd/{payload}\n", encoding="utf-8")

    print(f"Built profile: {cfg['Name']}")
    print(f"GeoIP: {cfg['Geoipurl']}")
    print(f"GeoSite: {cfg['Geositeurl']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
