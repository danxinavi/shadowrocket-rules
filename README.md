# 代理分流规则 · Proxy Routing Rules

> 单一域名源头，适配多款客户端。规则变更仅需在仓库中完成，客户端执行更新后即可生效。
> A single domain source, adapted for multiple clients. Rule changes are made in this repository only, and take effect after the client is updated.

- 仓库 / Repository：`danxinavi/shadowrocket-rules`
- 规则策略 / Routing Policy：国内流量直连，海外流量经代理，常见广告域名屏蔽，中国 IP 兜底直连，其余流量默认经代理。
  Domestic traffic DIRECT, overseas traffic PROXY, common advertising domains REJECT, China IP DIRECT as fallback, all other traffic PROXY.
- 节点配置 / Proxy Nodes：本仓库不包含任何节点信息。使用者应当使用自有订阅，规则中的 PROXY 指使用者当前所选的节点。
  This repository contains no proxy nodes. Users shall use their own subscriptions; PROXY in the rules refers to the node currently selected by the user.

---

## 中文说明

### 快速开始

| 客户端 | 使用文件 | 更新方式 |
|---|---|---|
| Shadowrocket（iOS） | `shadowrocket.conf`（仓库根目录，链接见下文） | 在配置列表中执行更新 |
| Surge（iOS / macOS） | `configs/surge.conf` | 更新该配置 |
| Quantumult X（iOS） | `configs/quantumultx.conf` | 更新 filter_remote |
| Loon（iOS） | 以 RULE-SET 方式引入 `ruleset/*.list` | 更新配置 |
| Clash / Mihomo / Clash Verge / Mihomo Party / Stash / Egern | `configs/clash.yaml` | 更新配置或 rule-provider |
| sing-box / SFA / NekoBox（Android / 桌面） | 以 rule-set 方式引入 `ruleset/sing-box/*.json` | 更新 rule-set |
| v2rayNG / v2rayN / Hiddify | 参见 `docs/CLIENTS.md` 中的路由配置说明，引入域名列表 | 更新配置 |

Shadowrocket 更新链接：

```
https://raw.githubusercontent.com/danxinavi/shadowrocket-rules/main/shadowrocket.conf
```

其他客户端的完整链接见 `docs/CLIENTS.md`，每个客户端一行，可直接复制使用。

### 规则顺序（自上而下，优先匹配先生效）

1. 局域网、私有地址：直连
2. 广告、追踪域名：屏蔽（仅列入常见域名，以避免误拦截正常服务）
3. 国内服务：直连（微信、淘宝、抖音、B站、12306、大麦、苹果中国等，另加所有 `.cn` 域名）
4. 海外服务：经代理（Google、YouTube、GitHub、OpenAI、Claude、X、Instagram 等）
5. 中国 IP：直连（未以域名列入的国内网站由本条兜底）
6. 其他流量：默认经代理

### 规则修改流程

生成文件由脚本自动生成，请勿直接修改。直接修改将在下一次生成时被覆盖。规则修改应当遵循以下流程：

1. 修改 `domains/direct.txt`、`domains/proxy.txt` 或 `domains/reject.txt`，每行一个域名；
2. 执行 `python3 scripts/build.py`，所有客户端的文件将随之重新生成；
3. 提交至仓库，客户端更新后即可获得最新规则。

### 文件结构

```
domains/            域名源头（唯一需要人工修改的部分）
  direct.txt        直连域名（40 个）
  proxy.txt         经代理域名（49 个）
  reject.txt        屏蔽域名（10 个）
ruleset/            各客户端规则集（由脚本生成，请勿人工修改）
  *.list            Shadowrocket / Surge / Loon 格式
  clash/*.yaml      Clash rule-provider 格式
  qx/*.list         Quantumult X 格式
  sing-box/*.json   sing-box rule-set 格式
configs/            各客户端配置模板（节点请替换为自有订阅）
  shadowrocket.conf
  surge.conf
  clash.yaml
  quantumultx.conf
scripts/build.py    生成脚本
docs/CLIENTS.md     各客户端对照表（中英文）
shadowrocket.conf   根目录版本，与上述更新链接所指向的文件一致
```

### 自动维护（每日自动执行，无须人工干预）

GitHub Action 每日 05:30（北京时间）自动执行 `scripts/check_and_clean.py` 与 `scripts/build.py`：
- 去重、删除格式错误的域名与 IP 地址，立即生效；
- DNS 检查：仅当某一域名连续 3 天均无法解析时才予删除，以避免单日网络波动导致误删；删除记录载于提交历史，误删可从历史记录中恢复；
- 重新生成所有客户端文件，并提交回仓库。

客户端更新方式：
- Clash 系：rule-provider 的更新间隔已设置为 86400 秒（每日），将自动获取最新规则；
- Shadowrocket：在配置列表中执行更新即可获得最新版本；亦可在设置 → 订阅中开启“打开时更新”与后台自动更新（该选项作用于节点订阅，配置更新仍以手动更新为准）；
- 其他客户端：按照 `docs/CLIENTS.md` 中各自的更新方式执行，规则集更新后即行生效。

自动维护的范围仅限于清理与重新生成，不会新增域名。如需新增服务，应当将相应域名加入 `domains/*.txt`，下一次自动检查将随之生成至各客户端文件。

### 参考

- Johnshall/Shadowrocket-ADBlock-Rules-Forever（3.16 万星，每日重建）
- blackmatrix7/ios_rule_script（2.84 万星，规则集收录范围较广）

本仓库的规则系依据上述策略编写的精简版本，并非对上述项目的原样复制。

---

## English

### Quick Start

| Client | File | How to update |
|---|---|---|
| Shadowrocket (iOS) | `shadowrocket.conf` (repository root, link below) | Update the configuration in the app |
| Surge (iOS / macOS) | `configs/surge.conf` | Update the configuration |
| Quantumult X (iOS) | `configs/quantumultx.conf` | Update filter_remote |
| Loon (iOS) | `ruleset/*.list` as RULE-SET | Update the configuration |
| Clash / Mihomo / Clash Verge / Mihomo Party / Stash / Egern | `configs/clash.yaml` | Update the configuration or rule-providers |
| sing-box / SFA / NekoBox (Android / desktop) | `ruleset/sing-box/*.json` as rule-sets | Update the rule-sets |
| v2rayNG / v2rayN / Hiddify | See `docs/CLIENTS.md` for routing notes | Update the configuration |

Shadowrocket update link:

```
https://raw.githubusercontent.com/danxinavi/shadowrocket-rules/main/shadowrocket.conf
```

Full links for other clients are in `docs/CLIENTS.md`, one line per client, and may be copied directly.

### Rule Order (top-down, first match wins)

1. LAN / private addresses: DIRECT
2. Common advertising / tracking domains: REJECT (kept short to avoid breaking legitimate services)
3. Domestic services: DIRECT (WeChat, Taobao, Douyin, Bilibili, 12306, Damai, Apple China, plus all `.cn` domains)
4. Overseas services: PROXY (Google, YouTube, GitHub, OpenAI, Claude, X, Instagram, etc.)
5. China IP: DIRECT (fallback for domestic sites not listed by domain)
6. All other traffic: PROXY

### Modifying Rules

Generated files are produced by script and shall not be edited directly; any direct edit will be overwritten on the next build. Rule modifications shall follow this procedure:

1. Edit `domains/direct.txt`, `domains/proxy.txt`, or `domains/reject.txt` (one domain per line);
2. Run `python3 scripts/build.py` to regenerate all client files;
3. Commit to the repository; clients will receive the new rules on their next update.

### Automatic Maintenance (runs daily, without manual intervention)

A GitHub Action runs every day at 05:30 Asia/Shanghai, executing `scripts/check_and_clean.py` and `scripts/build.py`:
- Deduplication, removal of malformed domains and IP literals, effective immediately;
- DNS verification: a domain is deleted only after it fails to resolve for 3 consecutive days, so that a single day of network instability cannot cause an erroneous deletion; deletions are recorded in the commit history and may be restored;
- Regeneration of all client files, committed back to the repository.

Client update methods:
- Clash family: rule-providers refresh every 86400 seconds (daily) automatically;
- Shadowrocket: update the configuration in the app to obtain the latest version;
- Other clients: follow their respective update methods in `docs/CLIENTS.md`.

Automatic maintenance is limited to cleaning and regeneration; it does not introduce new domains. To add a new service, the corresponding domain shall be added to `domains/*.txt`, and the next automated run will generate it for all clients.

### References

- Johnshall/Shadowrocket-ADBlock-Rules-Forever (31.6k stars, rebuilt daily)
- blackmatrix7/ios_rule_script (28.4k stars, a broad rule-set collection)

These rules are a curated, lightweight rewrite following the same policy, not a verbatim copy.

## License

MIT
