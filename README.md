# 代理分流规则 · Proxy Routing Rules

> 一份域名源头，多客户端通用。改规则只改仓库，客户端点一下更新即可。
> One source of domains, for many clients. Edit the repo, update in the client, done.

- 仓库 / Repo：`danxinavi/shadowrocket-rules`
- 规则思路 / Logic：国内直连，海外走代理，常见广告屏蔽，中国 IP 兜底直连，其他默认走代理。
  Domestic DIRECT, overseas PROXY, common ads REJECT, China IP DIRECT as fallback, everything else PROXY.
- 节点不在这个仓库里：节点用你自己的订阅，规则里的 PROXY 就是你当前选的节点。
  No nodes in this repo: use your own subscription; PROXY means your currently selected node.

---

## 中文说明

### 快速开始

| 客户端 | 用哪个文件 | 怎么更新 |
|---|---|---|
| Shadowrocket（iOS） | `shadowrocket.conf`（根目录，见下面链接） | 配置列表里点更新 |
| Surge（iOS / macOS） | `configs/surge.conf` | 更新这个配置 |
| Quantumult X（iOS） | `configs/quantumultx.conf` | 更新 filter_remote |
| Loon（iOS） | `ruleset/*.list` 做 RULE-SET 引入 | 更新配置 |
| Clash / Mihomo / Clash Verge / Mihomo Party / Stash / Egern | `configs/clash.yaml` | 更新配置或 rule-provider |
| sing-box / SFA / NekoBox（Android / 桌面） | `ruleset/sing-box/*.json` 做 rule-set 引入 | 更新 rule-set |
| v2rayNG / v2rayN / Hiddify | 先看 `docs/CLIENTS.md`，按里面的路由写法引入域名列表 | 更新配置 |

Shadowrocket 更新链接（以前给你的那个链接不变，照样能用）：

```
https://raw.githubusercontent.com/danxinavi/shadowrocket-rules/main/shadowrocket.conf
```

其他客户端的完整链接见 `docs/CLIENTS.md`，每个客户端一行，复制就能用。

### 规则顺序（从上到下，先命中先走）

1. 局域网、私有地址：直连
2. 广告、追踪域名：屏蔽（只列常见的，避免误伤）
3. 国内服务：直连（微信、淘宝、抖音、B站、12306、大麦、苹果中国等，另加所有 `.cn`）
4. 海外服务：走代理（Google、YouTube、GitHub、OpenAI、Claude、X、Instagram 等）
5. 中国 IP：直连（域名没列到的国内网站靠这条兜底）
6. 其他：默认走代理

### 怎么改规则（以后我们改，就这么改）

不要直接改生成出来的文件，那些文件是脚本生成的，改了下次会被覆盖：

1. 改 `domains/direct.txt`、`domains/proxy.txt` 或 `domains/reject.txt`，每行一个域名
2. 跑 `python3 scripts/build.py`，所有客户端的文件会一起重新生成
3. 提交到仓库，客户端点更新就拿到最新版

### 文件结构

```
domains/            域名源头（唯一需要手改的地方）
  direct.txt        直连域名（40 个）
  proxy.txt         走代理域名（49 个）
  reject.txt        屏蔽域名（10 个）
ruleset/            各客户端规则集（脚本生成，别手改）
  *.list            Shadowrocket / Surge / Loon 格式
  clash/*.yaml      Clash rule-provider 格式
  qx/*.list         Quantumult X 格式
  sing-box/*.json   sing-box rule-set 格式
configs/            各客户端配置模板（节点换成你自己的）
  shadowrocket.conf
  surge.conf
  clash.yaml
  quantumultx.conf
scripts/build.py    生成脚本
docs/CLIENTS.md     各客户端对照表（中英文）
shadowrocket.conf   根目录同款，供老链接继续使用
```

### 自动维护（每天自动跑，不用人工盯）

GitHub Action 每天早上 05:30（北京时间）自动跑一次 `scripts/check_and_clean.py` + `scripts/build.py`：
- 去重、删格式错误的域名、删 IP 地址，立即生效
- DNS 查域名：连续 3 天都解析不到的才删，避免一天网络抖动误删；删了的会在提交记录里写清楚，误删可以从历史里找回来
- 重新生成所有客户端文件，提交回仓库

客户端那边：
- Clash 系：rule-provider 的更新间隔已设为 86400 秒（每天），会自动拉最新规则
- 小火箭：配置列表里点一下更新，就拿到最新版；也可以在设置 → 订阅里打开“打开时更新”和后台自动更新（这是管节点订阅的，配置还是以点更新为准）
- 其他客户端：按 `docs/CLIENTS.md` 里各自的更新方式，规则集更新后都会生效

这个自动维护只做清理和重新生成，不会凭空发明新域名。想加一个新服务（比如新出的 AI 工具、新 App），还是跟我说域名，我加到 `domains/*.txt` 里，下次自动检查就会一起生成。

### 参考

- Johnshall/Shadowrocket-ADBlock-Rules-Forever（3.16 万星，每日重建）
- blackmatrix7/ios_rule_script（2.84 万星，规则集最全）

本仓库的规则是按上面思路自己写的精简版，不是原样照搬，目标是好用、好维护、不臃肿。

---

## English

### Quick Start

| Client | File | How to update |
|---|---|---|
| Shadowrocket (iOS) | `shadowrocket.conf` (repo root, link below) | Update the config in the app |
| Surge (iOS / macOS) | `configs/surge.conf` | Update the config |
| Quantumult X (iOS) | `configs/quantumultx.conf` | Update filter_remote |
| Loon (iOS) | `ruleset/*.list` as RULE-SET | Update the config |
| Clash / Mihomo / Clash Verge / Mihomo Party / Stash / Egern | `configs/clash.yaml` | Update the config or rule-providers |
| sing-box / SFA / NekoBox (Android / desktop) | `ruleset/sing-box/*.json` as rule-sets | Update the rule-sets |
| v2rayNG / v2rayN / Hiddify | See `docs/CLIENTS.md` for routing notes | Update the config |

Shadowrocket update link (the old link still works, unchanged):

```
https://raw.githubusercontent.com/danxinavi/shadowrocket-rules/main/shadowrocket.conf
```

Full links for other clients are in `docs/CLIENTS.md`, one line per client, copy and paste.

### Rule Order (top-down, first match wins)

1. LAN / private addresses: DIRECT
2. Common ads / tracking domains: REJECT (kept short to avoid breaking services)
3. Domestic services: DIRECT (WeChat, Taobao, Douyin, Bilibili, 12306, Damai, Apple China, plus all `.cn`)
4. Overseas services: PROXY (Google, YouTube, GitHub, OpenAI, Claude, X, Instagram, etc.)
5. China IP: DIRECT (fallback for domestic sites not listed by domain)
6. Everything else: PROXY

### How to Change Rules

Do not edit generated files by hand; they are overwritten on the next build:

1. Edit `domains/direct.txt`, `domains/proxy.txt`, or `domains/reject.txt` (one domain per line)
2. Run `python3 scripts/build.py` to regenerate all client files
3. Commit to the repo; clients get the new rules on their next update

### Automatic Maintenance (runs daily, no manual watching)

A GitHub Action runs every day at 05:30 Asia/Shanghai, running `scripts/check_and_clean.py` + `scripts/build.py`:
- Deduplicate, drop malformed domains and IP literals, immediately
- DNS-check domains: only a domain dead 3 days in a row is deleted, so a one-day network blip cannot delete a good domain; deletions are listed in the commit history and can be restored
- Regenerate all client files and commit back to the repo

On the client side:
- Clash family: rule-providers refresh every 86400 seconds (daily) automatically
- Shadowrocket: tap update on the config to get the latest version
- Other clients: follow their update method in `docs/CLIENTS.md`

Automatic maintenance only cleans and regenerates; it never invents new domains. To add a new service, tell Ren the domain, it goes into `domains/*.txt`, and the next daily run generates it everywhere.

### References

- Johnshall/Shadowrocket-ADBlock-Rules-Forever (31.6k stars, rebuilt daily)
- blackmatrix7/ios_rule_script (28.4k stars, the most complete rule-set collection)

These rules are a curated, lightweight rewrite following the same idea, not a copy.

## License

MIT
