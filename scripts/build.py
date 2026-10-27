#!/usr/bin/env python3
"""Build all client rule files from one source of truth.

Source: domains/{direct,proxy,reject}.txt (one domain per line, # = comment)
Outputs (all generated, do not edit by hand):
  ruleset/*.list            Shadowrocket / Surge / Loon RULE-SET format
  ruleset/clash/*.yaml      Clash / Mihomo rule-provider format (payload)
  ruleset/qx/*.list         Quantumult X filter format
  ruleset/sing-box/*.json   sing-box rule-set format (version 3)
  configs/shadowrocket.conf Shadowrocket full config (also kept at repo root)
  configs/surge.conf        Surge config template (replace nodes with your own)
  configs/clash.yaml        Clash / Mihomo config template (replace nodes)
  configs/quantumultx.conf  Quantumult X remote-filter template

Usage: python3 scripts/build.py
Rule order everywhere: REJECT -> DIRECT -> PROXY -> GEOIP CN DIRECT -> FINAL PROXY.
Only the domain lists are edited by hand; everything else is regenerated.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://raw.githubusercontent.com/danxinavi/shadowrocket-rules/main"
CATEGORIES = [("reject", "REJECT"), ("direct", "DIRECT"), ("proxy", "PROXY")]

def load(name):
    out = []
    for line in (ROOT / "domains" / f"{name}.txt").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out

def main():
    domains = {name: load(name) for name, _ in CATEGORIES}
    # Overlap check: a domain must not be in two categories.
    seen = {}
    for name, lst in domains.items():
        for d in lst:
            assert d not in seen, f"domain {d} in both {seen[d]} and {name}"
            seen[d] = name

    (ROOT / "ruleset").mkdir(exist_ok=True)
    (ROOT / "ruleset" / "clash").mkdir(exist_ok=True)
    (ROOT / "ruleset" / "qx").mkdir(exist_ok=True)
    (ROOT / "ruleset" / "sing-box").mkdir(exist_ok=True)
    (ROOT / "configs").mkdir(exist_ok=True)

    for name, _policy in CATEGORIES:
        lst = domains[name]
        # Shadowrocket / Surge / Loon: RULE-SET entries, policy is given in the main config.
        (ROOT / "ruleset" / f"{name}.list").write_text(
            "".join(f"DOMAIN-SUFFIX,{d}\n" for d in lst), encoding="utf-8")
        # Clash rule-provider
        (ROOT / "ruleset" / "clash" / f"{name}.yaml").write_text(
            "payload:\n" + "".join(f"  - DOMAIN-SUFFIX,{d}\n" for d in lst), encoding="utf-8")
        # Quantumult X filter
        policy = {"reject": "reject", "direct": "direct", "proxy": "proxy"}[name]
        (ROOT / "ruleset" / "qx" / f"{name}.list").write_text(
            "".join(f"host-suffix,{d},{policy}\n" for d in lst), encoding="utf-8")
        # sing-box rule-set
        (ROOT / "ruleset" / "sing-box" / f"{name}.json").write_text(
            json.dumps({"version": 3, "rules": [{"domain_suffix": lst}]},
                       ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Shadowrocket full config (also copied to repo root for the old update link)
    sr = f"""# Shadowrocket 分流规则 · danxinavi 自用版
# 更新方式：小火箭里添加这个配置的远程链接，之后改规则只改仓库，
# 客户端点一下配置更新即可，不用再进小火箭逐条改。
# 规则顺序从上到下，先命中先走。节点不在这个文件里，用你自己的订阅，
# 规则里的 PROXY 就是你当前选的节点。域名列表见 ruleset/*.list，
# 改域名只改 domains/*.txt，再跑 scripts/build.py 重新生成。

[General]
dns-server = system,223.5.5.5,114.114.114.114
bypass-system = true
skip-proxy = 192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,localhost,*.local

[Rule]
IP-CIDR,192.168.0.0/16,DIRECT,no-resolve
IP-CIDR,10.0.0.0/8,DIRECT,no-resolve
IP-CIDR,172.16.0.0/12,DIRECT,no-resolve
IP-CIDR,127.0.0.0/8,DIRECT,no-resolve
DOMAIN-SUFFIX,local,DIRECT
DOMAIN-SUFFIX,lan,DIRECT
RULE-SET,{BASE}/ruleset/reject.list,REJECT
RULE-SET,{BASE}/ruleset/direct.list,DIRECT
RULE-SET,{BASE}/ruleset/proxy.list,PROXY
DOMAIN-SUFFIX,cn,DIRECT
GEOIP,CN,DIRECT
FINAL,PROXY

[Host]
*.apple.com = server:system
*.icloud.com = server:system
localhost = 127.0.0.1

[URL Rewrite]
^https?://(www.)?g.cn https://www.google.com 302
^https?://(www.)?google.cn https://www.google.com 302
"""
    (ROOT / "configs" / "shadowrocket.conf").write_text(sr, encoding="utf-8")
    (ROOT / "shadowrocket.conf").write_text(sr, encoding="utf-8")

    # Surge config template
    surge = f"""# Surge 配置模板 · 规则部分已就绪，节点部分请换成你自己的
# Surge Template: rules are ready, replace the proxy section with your own nodes.
# 远程规则集（更新方式：Surge 里更新这个配置即可）

[General]
dns-server = system,223.5.5.5,114.114.114.114
skip-proxy = 192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,localhost,*.local

[Proxy]
# 把下面这一行换成你自己的节点，Surge 里节点名要和下面 ProxyGroup 里对应
# Replace with your own proxies, e.g. Proxy = vmess, example.com, 443, username=xxx
Proxy = direct

[ProxyGroup]
PROXY = select, Proxy

[Rule]
RULE-SET,{BASE}/ruleset/reject.list,REJECT
RULE-SET,{BASE}/ruleset/direct.list,DIRECT
RULE-SET,{BASE}/ruleset/proxy.list,PROXY
DOMAIN-SUFFIX,cn,DIRECT
GEOIP,CN,DIRECT
FINAL,PROXY
"""
    (ROOT / "configs" / "surge.conf").write_text(surge, encoding="utf-8")

    # Clash / Mihomo config template
    clash = f"""# Clash / Mihomo 配置模板 · 规则部分已就绪，节点部分请换成你自己的
# Clash Template: rules are ready, replace proxies with your own subscription.
# 规则集用远程 rule-provider，更新方式：Clash 里更新 rule-provider / 配置即可。
mixed-port: 7890
allow-lan: true
mode: rule
log-level: info
dns:
  enable: true
  nameserver:
    - 223.5.5.5
    - 114.114.114.114
proxies:
  # 把下面换成你自己的节点（订阅或手动节点），名字要和 proxy-groups 里对应
  # Replace with your own proxies.
  - name: "MyNode"
    type: socks5
    server: 127.0.0.1
    port: 1080
proxy-groups:
  - name: PROXY
    type: select
    proxies:
      - MyNode
rule-providers:
  reject:
    type: http
    behavior: domain
    url: "{BASE}/ruleset/clash/reject.yaml"
    path: ./ruleset/reject.yaml
    interval: 86400
  direct:
    type: http
    behavior: domain
    url: "{BASE}/ruleset/clash/direct.yaml"
    path: ./ruleset/direct.yaml
    interval: 86400
  proxy:
    type: http
    behavior: domain
    url: "{BASE}/ruleset/clash/proxy.yaml"
    path: ./ruleset/proxy.yaml
    interval: 86400
rules:
  - RULE-SET,reject,REJECT
  - RULE-SET,direct,DIRECT
  - RULE-SET,proxy,PROXY
  - DOMAIN-SUFFIX,cn,DIRECT
  - GEOIP,CN,DIRECT,no-resolve
  - MATCH,PROXY
"""
    (ROOT / "configs" / "clash.yaml").write_text(clash, encoding="utf-8")

    # Quantumult X remote-filter template
    qx = f"""# Quantumult X 配置模板 · 远程规则集，更新方式：QX 里更新 filter_remote 即可
# Quantumult X Template: remote filters, update in QX to get the latest rules.
# 节点请用你自己的订阅，本文件只管规则。

[general]
server_check_url = http://www.gstatic.com/generate_204

[filter_remote]
{BASE}/ruleset/qx/reject.list, tag=Reject, force-policy=reject, enabled=true
{BASE}/ruleset/qx/direct.list, tag=Direct, force-policy=direct, enabled=true
{BASE}/ruleset/qx/proxy.list, tag=Proxy, force-policy=proxy, enabled=true

[filter_local]
# 本地兜底：局域网直连，中国 IP 直连，其他走代理
ip-cidr,192.168.0.0/16,direct
ip-cidr,10.0.0.0/8,direct
ip-cidr,172.16.0.0/12,direct
geoip,cn,direct
final,proxy
"""
    (ROOT / "configs" / "quantumultx.conf").write_text(qx, encoding="utf-8")

    counts = {k: len(v) for k, v in domains.items()}
    print(f"direct={counts['direct']} proxy={counts['proxy']} reject={counts['reject']} total={sum(counts.values())}")

if __name__ == "__main__":
    main()
