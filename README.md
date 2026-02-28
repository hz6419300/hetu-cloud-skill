# hetu-cloud-skill

面向 `hetu-cloud` 场景的 Codex Skill 集合仓库，当前包含两个可直接使用的 Skill：

- `hetu-cloud-e2e-java-oneclick-report`：生成或维护 Java 21 + Maven 的 E2E 测试工程，并输出一键全流程测试报告。
- `hetu-cloud-proto-backend-spec`：把原始原型需求先做冲突澄清（Q&A），再整理成后端可落地的需求说明。

## 目录结构

```text
hetu-cloud-skill/
├── hetu-cloud-e2e-java-oneclick-report/
│   ├── SKILL.md
│   ├── USAGE.md
│   ├── PROMPT_TEMPLATE.md
│   ├── agents/
│   ├── references/
│   └── scripts/
├── hetu-cloud-proto-backend-spec/
│   ├── SKILL.md
│   ├── USAGE.md
│   ├── PROMPT_TEMPLATE.md
│   ├── agents/
│   └── references/
└── .gitignore
```

## Skill 一览

### 1) `hetu-cloud-e2e-java-oneclick-report`

- 目标：为 `hetu-cloud` 后端功能快速搭建可复用的 E2E 测试工程。
- 关键产物：`FullFlowOneClickTest` 与 `target/full-flow-one-click-report.md`。
- 典型能力：`HttpClient` 调用封装、token 自动重登、按 controller 拆分 client、`Stepper + RunReport` 分步记录。
- 文档入口：`hetu-cloud-e2e-java-oneclick-report/SKILL.md`、`hetu-cloud-e2e-java-oneclick-report/USAGE.md`。

### 2) `hetu-cloud-proto-backend-spec`

- 目标：将原始需求从“可讨论”收敛为“可开发、可验收”的后端需求说明。
- 两阶段流程：先输出《冲突说明（Q&A）》并等待回答，再输出最终《后端需求说明》。
- 典型能力：冲突识别、规则补齐、TBD 管理、Decision Log 汇总。
- 文档入口：`hetu-cloud-proto-backend-spec/SKILL.md`、`hetu-cloud-proto-backend-spec/USAGE.md`。

## 快速使用

1. 进入对应子目录，先看 `USAGE.md` 里的触发示例和输入要求。
2. 按需复制 `PROMPT_TEMPLATE.md` 并补齐业务上下文。
3. 在 Codex 对话中明确点名 Skill 名称，例如：
   - “用 `hetu-cloud-e2e-java-oneclick-report`，为 XXX 功能补一套 one-click E2E 测试。”
   - “用 `hetu-cloud-proto-backend-spec`，先生成冲突 Q&A，不要直接出最终后端需求说明。”

## 仓库维护建议

- 提交前先执行：`git status`，确认没有把 `.env` 等敏感文件纳入版本控制。
- 新增 Skill 时，建议至少补齐：`SKILL.md`、`USAGE.md`、`PROMPT_TEMPLATE.md` 与 `references/`。
- 需要对外共享时，优先在根目录更新本 README 的 Skill 列表与使用入口。
