---
name: hetu-cloud-e2e-java-oneclick-report
description: "Scaffold and maintain Java 21 Maven E2E test projects for the hetu-cloud repository. Use when you need to quickly create repeatable E2E coverage for a hetu-cloud backend feature with many endpoints/controllers: generate HttpClient-based API clients, request payload factories, smoke/endpoint/fullchain tests, a Stepper + RunReport one-click flow, and always write a Markdown report (target/full-flow-one-click-report.md) on completion."
---

# E2E Java One-Click Report

## Goal

Create or update a Java 21 Maven E2E test project that:
- Loads settings from `.env` (baseUrl, auth, ids)
- Uses `HttpClient` + Bearer token with auto re-login
- Provides `SmokeTest` + `EndpointTest` + `FullChainTest`
- Provides `FullFlowOneClickTest` using `Stepper + RunReport`
- Always writes a Markdown report to `target/full-flow-one-click-report.md` (success or failure)
- Uses `KEEP_DATA_ON_FAIL` to decide cleanup strategy
- Targets the `hetu-cloud` codebase conventions and controller patterns (e.g., `@RequestMapping`, `@SaCheckPermission`, `R` response wrapper)

## Workflow

### 1) Discover endpoints (source of truth = controller annotations)

- List controllers and methods (exclude `@Deprecated` by default).
- Record: `@RequestMapping` prefix + method mapping + request method + request body type + auth notes (`@SaCheckPermission`).
- Identify which endpoints are needed for:
  - **Create main** (create primary entity)
  - **Update details** (per feed type / per detail type)
  - **Query info** (page/getById/info)
  - **Downstream verify** (optional: query generated local entities)
  - **Deletion rules** (expected denied path)
  - **Cleanup** (cascade deletes in correct order)

### 2) Create/extend E2E project structure

- `src/main/java/...`
  - `config/Settings`, `config/SettingsLoader`
  - `http/HttpExecutor`, `http/HttpResult`
  - `client/*Client` (one per controller prefix)
  - `fixture/*PayloadFactory` (all JSON request bodies centralized here)
- `src/test/java/...`
  - `BaseE2ETest` (wires Settings/Http/Token/Clients)
  - `company/*` and `farm/*` packages (or by bounded context)
  - `FullFlowOneClickTest` (one-click runner + report generation)

### 3) Implement tests

- **SmokeTest**: login + 401/403 without token + `page` with token.
- **EndpointTest**: cover main endpoints in a stable order; tolerate empty pages.
- **FullChainTest per detail type**: create → save detail → info → copy → add useDept → verify local entity → delete denied.
- **FullFlowOneClickTest**: minimal happy path + denied path + always emit report.

### 4) Make the report deterministic

- Write Markdown to `target/full-flow-one-click-report.md` in `finally`.
- Capture for each step:
  - Requests (`METHOD path | summary`)
  - Outputs (key ids, names, flags)
  - Warnings (skip reasons)
  - Errors + stacktrace

### 5) Validate quickly

- Compile check: `mvn -q -DskipTests test-compile`
- Run a single test: `mvn -Dtest=FullFlowOneClickTest test`

## Minimal conventions

- Prefer `requestAllowBusinessFail(...)` in clients for “expected denied” assertions (avoid `assertThrows` swallowing response msg).
- Keep request payload construction in `*PayloadFactory`.
- Cleanup order:
  - delete use_dept (cascades local) → delete company entity
  - if unify import: delete company use_dept first, then farm entity as fallback
- Always gate optional chains with JUnit `Assumptions` (`FARM_CURVE_ID` etc).

## References

- For the detailed Stepper/RunReport pattern, read `references/oneclick-report-pattern.md`.
- For the project scaffolding checklist, read `references/e2e-project-checklist.md`.

## Scripts

Run `scripts/scaffold-e2e-java-from-existing.sh` to copy an existing E2E project as a starting point and rename it (artifactId, project name, paths).
