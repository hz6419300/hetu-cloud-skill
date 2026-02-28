#!/usr/bin/env python3
import re
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1].strip() in {"-h", "--help"}:
        print("Usage: validate_prompt_md.py <PROMPT.md|PROMPT_TEMPLATE.md>")
        return 2

    path = Path(sys.argv[1]).expanduser().resolve()
    if not path.exists():
        print(f"[ERR] File not found: {path}")
        return 2

    raw = path.read_text(encoding="utf-8")
    lines = raw.splitlines()

    errors: list[str] = []
    warnings: list[str] = []

    # 1) 模板本体允许占位符；只有在真正执行时（通常是 PROMPT.md）才要求替换
    if path.name.upper() != "PROMPT_TEMPLATE.MD":
        if "<your-" in raw:
            errors.append("存在占位符 `<your-...>`，请替换为实际值。")

    # 2) 必填值行不能为空（模板中统一用 `- 值：`）
    empty_value_lines = [i + 1 for i, l in enumerate(lines) if re.match(r"^\s*-\s*值：\s*$", l)]
    if path.name.upper() != "PROMPT_TEMPLATE.MD":
        if empty_value_lines:
            errors.append(f"存在空的 `- 值：` 必填项（行号：{', '.join(map(str, empty_value_lines))}）。")

    # 3) username/password 不能为空（允许写在 bullet 或非 bullet）
    def has_empty_kv(prefix: str) -> bool:
        pattern = re.compile(rf"^\s*-?\s*{re.escape(prefix)}\s*$")
        return any(pattern.match(l) for l in lines)

    if path.name.upper() != "PROMPT_TEMPLATE.MD":
        if has_empty_kv("username："):
            errors.append("LOGIN_USERNAME 未填写（存在空的 `username：` 行）。")
        if has_empty_kv("password："):
            errors.append("LOGIN_PASSWORD 未填写（存在空的 `password：` 行）。")

    # 4) controller 清单至少要有 1 条非示例
    controller_section_start = None
    for idx, l in enumerate(lines):
        if "【必填】要覆盖的 controller 类名清单" in l:
            controller_section_start = idx
            break
    if controller_section_start is not None:
        items: list[str] = []
        for l in lines[controller_section_start + 1:]:
            if l.strip() == "":
                break
            if l.strip().startswith("## "):
                break
            if l.strip().startswith("- "):
                items.append(l.strip()[2:])

        actual = [x for x in items if "例：" not in x and "…" not in x and "你的值从这里开始" not in x and x.strip()]
        actual = [x for x in actual if "Controller" in x]
        if path.name.upper() != "PROMPT_TEMPLATE.MD":
            if not actual:
                errors.append("controller 清单为空：请在该段落下新增至少 1 行 `XxxController`。")
    else:
        warnings.append("未找到 controller 清单段落（模板结构可能被改动），建议检查。")

    if errors:
        print("[FAIL] Prompt template validation failed.")
        for e in errors:
            print(f"- {e}")
        if warnings:
            print("\n[WARN]")
            for w in warnings:
                print(f"- {w}")
        return 1

    print("[OK] Prompt template validation passed.")
    if warnings:
        print("\n[WARN]")
        for w in warnings:
            print(f"- {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
