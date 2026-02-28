# hetu-cloud E2E One-Click Skill｜提示词模板（可编辑后直接驱动执行）

用途：当你想使用 `hetu-cloud-e2e-java-oneclick-report` 这个 skill 时，**只需要改这份模板**，然后对我说：  
“读取该模板文件，按模板内容执行 skill（生成/更新 E2E 项目）”。

> 约定：标注为 `【必填】` 的字段缺失，我会直接让你补齐；标注为 `【可选】` 的字段缺失，我会自动跳过对应链路（用 JUnit Assumptions）。

---

## A. 任务总述

【必填】功能/模块名称（人类可读）：
- 例如：公司级喂食方案 / 公司级曲线 / 设备下发 / 报表统计
- 值：

【必填】目标：你希望 E2E 验证什么（1~3 句话）：
- 例如：创建主表、保存详情、下发生成本地数据、删除规则拦截、锁定拦截等
- 值：

【可选】是否新建 E2E 项目：
- 是 / 否（如果“否”，请在下面给出要更新的项目路径）
- 值：

---

## B. 代码仓与参考样板

【必填】目标仓库（hetu-cloud）路径：
- 默认：`/home/hz/work/project/gitea/hetu-cloud`
- 值：

【必填】参考 E2E 项目路径（作为结构样板）：
- 例如：`/home/hz/work/version/2.5.2/company/company-feed-curve-e2e-java`
- 例如：`/home/hz/work/version/2.5.2/company/company-feed-scheme-e2e-java`
- 值：

【必填】输出 E2E 项目路径（生成到哪里）：
- 例如：`/home/hz/work/version/2.5.2/company/<your-feature>-e2e-java`
- 值：

【必填】新项目 Maven 坐标（如果是新建）：
- groupId：`com.hetu.e2e`
- artifactId：`<your-artifact-id>`
- name：`<your-project-name>`
- description：一句话描述

---

## C. 接口范围（以 Controller 为准）

【必填】要覆盖的 controller 类名清单（逐行）：
- 例：`CompanyFeedSchemeController`
- 例：`CompanyFeedSchemeGeneralDetailController`
- …
- 你的值从这里开始逐行追加：

【可选】需要忽略的接口/说明（逐行）：
- 例：忽略所有 `@Deprecated`
- 例：忽略 xxx（原因：已废弃/无网关暴露/本期不测）

【可选】强制覆盖的接口（即使 `@Deprecated` 也要测，逐行）：
- 例：`POST /xxx/yyy`

---

## D. 链路与用例要求（你勾啥我测啥）

### D1. 必跑链路（默认全开）

- [x] Smoke：登录 + 401/403 + page
- [x] Endpoint：逐接口覆盖（按 @Order 顺序）
- [x] FullChain：每种详情类型的完整链路（create → save detail → info → copy → useDept → verify local → delete denied → cleanup）
- [x] OneClick：`FullFlowOneClickTest`（**finally 落盘报告**）

### D2. 可选链路（需要环境参数）

- [ ] unify/importFromCompany（需要 `FARM_CURVE_ID` 或其它 id）
- [ ] PLAN_TYPE 锁定回归（需要 lock 权限 + `FARM_CURVE_ID`）
- [ ] 其它（你自定义说明）：

---

## E. 测试数据与环境变量（.env）

【必填】BASE_URL：
- 例：`http://127.0.0.1:8080`
- 值：

【必填】LOGIN_USERNAME / LOGIN_PASSWORD：
- username：
- password：

【必填】COMPANY_DEPT_ID（公司机构 ID）：
- 值：

【必填】FARM_IDS（末级猪场/服务部 ID，逗号分隔）：
- 值：

【可选】FARM_CURVE_ID（统一入口/锁定链路需要）：
- 值：

【可选】RESOURCE_PREFIX / LOGIN_PATH（非默认才填）：
- RESOURCE_PREFIX：默认 `/api/feeding`
- LOGIN_PATH：默认 `/api/auth/login`

【可选】调试开关（建议默认）：
- LOG_HTTP：true/false
- LOG_HTTP_BODY：true/false
- KEEP_DATA_ON_FAIL：true/false（失败是否保留现场）

---

## F. 产物与验收标准（写死，别扯皮）

【必填】报告文件要求（OneClick 结束后）：
- 必须生成：`target/full-flow-one-click-report.md`
- 报告必须包含：
  - 环境信息（baseUrl/resourcePrefix/companyDeptId/farmId）
  - 产物 ID（主表 id、useDept ids、本地 id 等）
  - 每个 Step 的请求/输出/耗时/错误

【必填】最小验收命令：
- `mvn -q -DskipTests test-compile` 必须通过

【可选】你希望额外生成的文档：
- `README.md`（运行方式）
- `FULL_TEST_FLOW.md`（逐接口清单）

---

## G. 约束（防止我瞎改）

【必填】约束：
- 只允许新增/修改 E2E 项目代码；不改业务代码（除非你明确要求）
- 预期失败断言必须保留后端 `msg`（用 `requestAllowBusinessFail`，不要只用 `assertThrows`）
- Payload 构造必须集中在 `*PayloadFactory`
