# Stepper + RunReport（One-Click）模式参考

目标：让 `FullFlowOneClickTest#shouldRunFullFlowOneClick` 在结束时**无论成功/失败**都生成 Markdown 报告到：

`target/full-flow-one-click-report.md`

## 关键点

1. **Step 颗粒度固定**：每步只有一件事，方便定位失败点（create / save detail / add useDept / verify / denied）。
2. **日志结构固定**：每步记录：
   - Requests：`METHOD path | summary`
   - Outputs：产物（id/name/flags）与关键断言结果
   - Warnings：skip/assumption 信息
3. **预期失败**不要 `assertThrows` 吞响应：
   - client 增加 `requestAllowBusinessFail(...)` 返回 `HttpResult`
   - 断言 `HTTP 2xx` 且 `body.code != 200`，并校验 `msg` 包含关键词
4. **报告生成在 finally**：
   - `report.finish(failure, ctx)`
   - `Files.writeString(reportPath, report.toMarkdown(), UTF_8)`
5. **清理策略**：
   - `KEEP_DATA_ON_FAIL=true` 且失败：保留现场（打印 id）
   - 否则清理：`use_dept -> company entity`（必要时再兜底删本地 entity）

## 最小骨架（伪码）

```java
RunReport report = new RunReport("FullFlowOneClickTest#shouldRunFullFlowOneClick");
Stepper stepper = new Stepper(report);
Throwable failure = null;
try {
  stepper.run(ENV, ctx, "...", step -> { ... });
  stepper.run(AUTH, ctx, "...", step -> { ... });
  stepper.run(CREATE, ctx, "...", step -> { ... });
  ...
} catch (Throwable t) {
  failure = t;
  throw t;
} finally {
  if (ctx.keepDataOnFail && failure != null) { ... } else { cleanupQuietly(ctx); }
  report.finish(failure, ctx);
  Files.writeString(Path.of("target","full-flow-one-click-report.md"), report.toMarkdown(), UTF_8);
}
```

