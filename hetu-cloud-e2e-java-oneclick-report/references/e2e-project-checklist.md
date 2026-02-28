# Java E2E 项目脚手架清单（可复用）

## 目录结构

- `pom.xml`
  - Java 21
  - JUnit 5
  - Jackson
  - dotenv（.env）
- `.env.example` + `.gitignore`（忽略 `.env` / `target` / token cache）
- `src/main/java/...`
  - `config/Settings`, `SettingsLoader`
  - `http/HttpExecutor`, `HttpResult`
  - `client/*Client`
  - `fixture/*PayloadFactory`
  - `util/Jsons`（ObjectMapper 单例）
  - `client/TokenManager`（token 缓存 + 自动重登）
- `src/test/java/...`
  - `BaseE2ETest`：初始化 settings/http/clients
  - `company/*SmokeTest`：登录 + 401/403 + page
  - `company/*EndpointTest`：逐接口覆盖
  - `company/*FullChainTest`：主干链路
  - `FullFlowOneClickTest`：Stepper + RunReport + 落盘报告

## 生成/维护流程

1. 从 controller 注解收集 endpoints（过滤 `@Deprecated`）
2. 每个 controller prefix 一个 `*Client`，方法命名与 endpoint 对齐
3. 把请求体 JSON 全塞进 `*PayloadFactory`（别在 test 里散着拼）
4. 用 `Assumptions` 控制可选链路（比如需要 FARM_CURVE_ID）
5. 用 `requestAllowBusinessFail` 覆盖预期失败接口（不要只用 assertThrows）
6. `mvn -q -DskipTests test-compile` 做最小验收

## 常见坑

- `DELETE + body`：HTTP 客户端需要显式发送 body（Java HttpClient 默认 noBody）
- 401/403：client 需要自动重登重试一次（可开关）
- 数据域/权限：companyDeptId/farmIds 必须在账号可见范围，否则“业务失败”不是代码问题
- 清理顺序：先删 use_dept（可能级联删本地），再删主表，最后兜底删本地表

