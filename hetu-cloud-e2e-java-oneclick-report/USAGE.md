# hetu-cloud-e2e-java-oneclick-report 使用说明（给人看的）

这个 Skill 只服务于 `hetu-cloud` 仓库：把你在后端实现的某个功能，快速做成一套 **Java 21 + Maven** 的 E2E 测试工程，并且提供 `FullFlowOneClickTest`（一键全流程）在结束时生成 Markdown 测试报告：`target/full-flow-one-click-report.md`。

---

## 1) 怎么触发/怎么用

在对话里直接点名它（最稳）：  
“用 `hetu-cloud-e2e-java-oneclick-report`，为 XXX 功能生成/更新 E2E 测试项目……”

常见用法示例（你照着改就行）：

- “用 `hetu-cloud-e2e-java-oneclick-report`，参考现有 `company-feed-curve-e2e-java`，为公司级喂食方案生成一个新的 E2E 项目，覆盖这些 controller：……，并且 one-click 用例最终生成报告。”
- “用 `hetu-cloud-e2e-java-oneclick-report`，在已有 E2E 项目上新增一个 `FullFlowOneClickTest`，要求 finally 落盘 report，预期失败用 `requestAllowBusinessFail` 保留 msg。”

---

## 2) 你必须提供/确认的输入（必填项）

以下信息缺了，E2E 项目就很难“可跑且稳定”：

1. **目标范围（功能/模块名）**
   - 例如：公司级喂食方案、公司级曲线、设备下发等。

2. **接口清单（source of truth）**
   - 给 controller 类名或路径即可。
   - 默认忽略 `@Deprecated` 接口（除非你明确说要测）。

3. **环境可用的网关与账号**
   - `BASE_URL`
   - `LOGIN_USERNAME` / `LOGIN_PASSWORD`
   - 如有非默认：`LOGIN_PATH`、`RESOURCE_PREFIX`

4. **数据域/机构 ID（跟 hetu-cloud 强相关）**
   - `COMPANY_DEPT_ID`：公司侧主数据创建通常必需
   - `FARM_IDS`：下发/使用机构/锁定等链路通常必需（至少 1 个末级猪场/服务部）

---

## 3) E2E 工程里必须具备的东西（交付硬标准）

1. **配置加载**
   - `.env.example`（必须列出必填项和可选项）
   - `Settings` / `SettingsLoader`（环境变量 > .env > 默认值）

2. **HTTP 与认证**
   - 基于 Java `HttpClient` 的 `HttpExecutor`
   - `TokenManager`：缓存 token，401/403 自动重登并重试一次（可开关）

3. **Client 分层**
   - 每个 `@RequestMapping` 前缀一个 `*Client`（别把一堆接口糊到一个类里）
   - 对于“预期失败/拦截规则”，client 必须提供：
     - `requestAllowBusinessFail(...) -> HttpResult`
     - 用来拿到 `code/msg` 做断言（不要只用 `assertThrows` 把响应吞了）

4. **请求体集中管理**
   - 所有 JSON 构造放到 `*PayloadFactory`
   - 单测只“调用工厂 + 调接口 + 断言”，别在测试里散着拼 JSON

5. **一键全流程 + 报告落盘**
   - `FullFlowOneClickTest#shouldRunFullFlowOneClick`
   - `Stepper + RunReport` 分步记录
   - `finally` 里无论成功/失败都写 Markdown：
     - `target/full-flow-one-click-report.md`
   - 支持 `KEEP_DATA_ON_FAIL`：失败时可选择保留现场（打印 ids）

6. **最小验收命令**
   - `mvn -q -DskipTests test-compile` 必须能过（先保证能编译）

---

## 4) .env（必须项 vs 可选项）

通常这几个是“真正必填”的：

- `BASE_URL`
- `LOGIN_USERNAME`
- `LOGIN_PASSWORD`
- `COMPANY_DEPT_ID`
- `FARM_IDS`

常见可选项：

- `LOGIN_PATH`（默认 `/api/auth/login`）
- `RESOURCE_PREFIX`（默认 `/api/feeding`）
- `FARM_CURVE_ID`（某些 unify/import/addMain 链路需要 curveId，不配就用 Assumptions 跳过）
- `LOG_HTTP` / `LOG_HTTP_BODY`
- `KEEP_DATA_ON_FAIL`

---

## 5) 运行与产物位置

运行：

- `mvn -Dtest=FullFlowOneClickTest test`

报告：

- `target/full-flow-one-click-report.md`

如果你打开了 `LOG_HTTP=true`，Console 会打印请求/响应；报告会额外把每个 Step 的 request/out/error 固化下来，方便甩锅/复盘。

---

## 6) 模板校验（推荐）

你把 `PROMPT_TEMPLATE.md` 复制为 `PROMPT.md` 并填好值后，建议先跑一次校验脚本（避免漏填导致执行到一半才发现缺参数）：

```bash
python3 scripts/validate_prompt_md.py PROMPT.md
```

校验规则（简版）：
- 不能残留 `<your-...>` 占位符
- 不能有空的 `- 值：` 行
- `username/password` 不能空
- controller 清单至少要填 1 个 `XxxController`
