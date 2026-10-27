# Shadowrocket 分流规则

自用 Shadowrocket 分流规则：国内直连、海外走代理、常见广告屏蔽。

## 更新链接（小火箭里用这一个）

```
https://raw.githubusercontent.com/danxinavi/shadowrocket-rules/main/shadowrocket.conf
```

## 小火箭里怎么用

1. 打开 Shadowrocket，点「配置」，右上角 +，选从 URL 添加，粘贴上面这个链接，下载。
2. 选中这个配置，全局路由选「配置」，不要长期选全局代理。
3. 节点用你自己的订阅，这个文件里不带节点，规则里的 PROXY 就是你当前选的节点。

## 以后怎么更新

仓库里改了规则，不用再进小火箭逐条改：

在配置列表里找到这个配置，点更新，拉到的就是最新版。

## 规则思路

顺序从上到下，先命中先走：

1. 局域网、私有地址：直连
2. 常见广告、追踪域名：屏蔽
3. 国内服务（微信、淘宝、抖音、B站、12306、大麦、苹果中国等）：直连
4. 海外服务（Google、YouTube、GitHub、OpenAI、Claude、X、Instagram 等）：走代理
5. 中国 IP：直连（兜底）
6. 其他：默认走代理

## 参考

- Johnshall/Shadowrocket-ADBlock-Rules-Forever（3.16 万星，每日重建）
- blackmatrix7/ios_rule_script（2.84 万星，规则集最全）

本仓库的规则是按上面思路自己写的精简版，不是原样照搬。
