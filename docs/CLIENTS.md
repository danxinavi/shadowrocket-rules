# 客户端对照表 · Client Matrix

> 基础地址：`https://raw.githubusercontent.com/danxinavi/shadowrocket-rules/main/`
> Base URL: `https://raw.githubusercontent.com/danxinavi/shadowrocket-rules/main/`
> 下面每个链接 = 基础地址 + 文件路径。节点一律用你自己的订阅，本仓库不带节点。
> Each link below = base URL + file path. Nodes always come from your own subscription; this repo has none.

## iOS

### Shadowrocket（小火箭）
- 配置 / Config：`shadowrocket.conf`
- 链接 / Link：`https://raw.githubusercontent.com/danxinavi/shadowrocket-rules/main/shadowrocket.conf`
- 用法：配置 → + → 从 URL 添加 → 粘贴链接 → 选中配置，全局路由选「配置」
- 更新：配置列表里点更新
- Update: update the config in the app

### Surge
- 配置 / Config：`configs/surge.conf`
- 链接 / Link：`https://raw.githubusercontent.com/danxinavi/shadowrocket-rules/main/configs/surge.conf`
- 注意：模板里的节点是占位，请换成你自己的节点；规则集部分（RULE-SET）已就绪。
- Note: replace the placeholder proxy with your own nodes; the RULE-SET part is ready.

### Quantumult X
- 配置 / Config：`configs/quantumultx.conf`
- 链接 / Link：`https://raw.githubusercontent.com/danxinavi/shadowrocket-rules/main/configs/quantumultx.conf`
- 规则集也可以单独引入：`ruleset/qx/direct.list`、`ruleset/qx/proxy.list`、`ruleset/qx/reject.list`（filter_remote，force-policy 对应 direct / proxy / reject）
- Rule-sets can also be used separately as filter_remote with matching force-policy.

### Loon
- 规则集 / Rule-sets：`ruleset/direct.list`、`ruleset/proxy.list`、`ruleset/reject.list`
- 用法：在你的 Loon 配置里加三行 RULE-SET，策略分别对应 DIRECT / PROXY / REJECT，再加 `GEOIP,CN,DIRECT` 和 `FINAL,PROXY`。
- Usage: add three RULE-SET lines with policies DIRECT / PROXY / REJECT, plus `GEOIP,CN,DIRECT` and `FINAL,PROXY`.

### Stash / Egern（iOS，Clash 内核）
- 和 Clash 一样用 `configs/clash.yaml`，见下面 Clash 一节。
- Same as Clash: use `configs/clash.yaml` below.

## Android

### Clash Meta / Mihomo（Android）
- 配置 / Config：`configs/clash.yaml`
- 链接 / Link：`https://raw.githubusercontent.com/danxinavi/shadowrocket-rules/main/configs/clash.yaml`
- 规则集是远程 rule-provider，更新配置或 rule-provider 即可拿到最新规则。
- Rule-providers are remote; update the config or providers to get new rules.

### sing-box / SFA / NekoBox（Android）
- 规则集 / Rule-sets：
  - `ruleset/sing-box/direct.json`
  - `ruleset/sing-box/proxy.json`
  - `ruleset/sing-box/reject.json`
- 用法：在 sing-box 配置的 `route.rule_set` 里引用这三个文件，再在 `route.rules` 里按 rule-set 分配 outbound（direct / proxy / block）。
- Usage: reference them in `route.rule_set`, then map each to an outbound (direct / proxy / block) in `route.rules`.

### v2rayNG / Hiddify（Android）
- 这类客户端没有统一的远程规则集格式：建议用 sing-box 核心的版本，或在路由设置里按域名列表手动建三条规则（直连 / 代理 / 屏蔽），域名抄 `domains/*.txt`。
- No unified remote rule-set format here: prefer a sing-box-core client, or build three routing rules by hand from `domains/*.txt` (direct / proxy / block).

## Windows / macOS / Linux

### Clash Verge Rev / Mihomo Party / Clash for Windows（桌面 Clash 系）
- 配置 / Config：`configs/clash.yaml`，链接同 Android 的 Clash 一节。
- Same `configs/clash.yaml` as the Android Clash section.

### v2rayN（Windows）
- 和 v2rayNG 类似：路由设置里按 `domains/*.txt` 建三条规则，或用 sing-box 核心版本引入 `ruleset/sing-box/*.json`。
- Same as v2rayNG: build three routing rules from `domains/*.txt`, or use a sing-box-core build with `ruleset/sing-box/*.json`.

### Surge for Mac
- 同 iOS 的 Surge：`configs/surge.conf`。
- Same as Surge on iOS: `configs/surge.conf`.

## 通用说明 · General Notes

- 所有客户端共用同一套域名源头（`domains/*.txt`），改一处，各客户端下次更新一起生效。
  All clients share the same domain source (`domains/*.txt`); one edit takes effect on every client at its next update.
- 国内直连里包含苹果中国和 iCloud 中国；如果你在海外使用，建议把 `apple.com`、`icloud.com` 改回走代理。
  Apple / iCloud are DIRECT for China services; if you use this outside China, consider moving `apple.com` and `icloud.com` to PROXY.
- 屏蔽列表只列常见广告域名，刻意保持短，避免误伤正经服务。
  The reject list is intentionally short (common ads only) to avoid breaking services.
