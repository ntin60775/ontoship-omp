"""Тесты нового поведения gitmark.py из плана command-inventory:
идемпотентность inventory, поимка рассинхрона --check, парсер .gitignore, I7.
Существующее поведение не покрывается (вне scope плана)."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

_GITMARK = Path(__file__).resolve().parent.parent / ".omp" / "skills" / "kb-search" / "gitmark.py"
_spec = importlib.util.spec_from_file_location("gitmark", _GITMARK)
gm = importlib.util.module_from_spec(_spec)
sys.modules["gitmark"] = gm
_spec.loader.exec_module(gm)


COMMAND = """---
description: Test command for the registry.
args: "<topic>"
drives: "test skill"
---

Run the test skill on: `$ARGUMENTS`.
"""

SKILL = """---
name: test-skill
description: A skill for the registry tests.
---

Body.
"""

REGISTRY = """---
node_type: reference
title: Test commands
---

# Test commands

## Summary

<!-- BEGIN inventory:commands -->
<!-- END inventory:commands -->

<!-- BEGIN inventory:skills -->
<!-- END inventory:skills -->

---

## `/foo` — test command

- **Definition:** `.omp/commands/foo.md`
"""


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """Минимальный репо: одна команда, один навык, реестр с маркерами."""
    (tmp_path / ".omp" / "commands").mkdir(parents=True)
    (tmp_path / ".omp" / "skills" / "test-skill").mkdir(parents=True)
    (tmp_path / "docs" / "reference").mkdir(parents=True)
    (tmp_path / ".omp" / "commands" / "foo.md").write_text(COMMAND, encoding="utf-8")
    (tmp_path / ".omp" / "skills" / "test-skill" / "SKILL.md").write_text(SKILL, encoding="utf-8")
    (tmp_path / "docs" / "reference" / "commands.md").write_text(REGISTRY, encoding="utf-8")
    return tmp_path


def _between(text: str, what: str) -> str:
    b, e = f"<!-- BEGIN inventory:{what} -->", f"<!-- END inventory:{what} -->"
    return text[text.find(b) + len(b):text.find(e)].strip("\n")


# ── парсер .gitignore ──────────────────────────────────────────────

def test_gitignore_excludes_dirs_and_files(repo: Path):
    (repo / ".gitignore").write_text(".scratch/\ndraft.md\n", encoding="utf-8")
    (repo / ".scratch").mkdir()
    (repo / ".scratch" / "report.md").write_text("ephemeral", encoding="utf-8")
    (repo / "draft.md").write_text("draft", encoding="utf-8")
    (repo / "keep.md").write_text("keep", encoding="utf-8")
    found = {p.name for p in gm.iter_md(repo)}
    assert "report.md" not in found
    assert "draft.md" not in found
    assert "keep.md" in found


def test_gitignore_wildcard(repo: Path):
    (repo / ".gitignore").write_text("*-map.html\n", encoding="utf-8")
    (repo / "notes.md").write_text("notes", encoding="utf-8")
    dir_pats, file_pats, path_pats, unsupported = gm.parse_gitignore(repo)
    assert dir_pats == [] and path_pats == [] and unsupported == []
    assert file_pats == ["*-map.html"]
    assert gm._wild_match("docs-map.html", "*-map.html")
    assert not gm._wild_match("notes.md", "*-map.html")


def test_gitignore_path_rules_are_not_dropped(repo: Path):
    """Репро баг-репорта 2026-09-15: правила с путём терялись молча.

    Правило с '/' и без хвостового слэша не попадало ни в один список, а шаблон
    каталога с путём не матчился никогда — индекс набирал мусор из бэкапов.
    """
    (repo / ".gitignore").write_text(
        "build/\n.omp/plugins/\n.omp/.backup-*\ndrafts/secret.md\n", encoding="utf-8")
    for rel in ("docs/live.md", ".omp/plugins/x.md", "drafts/secret.md", "build/b.md",
                ".omp/.backup-20260101-000000/rules/r.md"):
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("текст", encoding="utf-8")

    hidden = (".omp/plugins/x.md", "drafts/secret.md", "build/b.md",
              ".omp/.backup-20260101-000000/rules/r.md")
    for source in (gm.iter_md_fallback, gm.iter_md):
        found = {p.relative_to(repo).as_posix() for p in source(repo)}
        assert "docs/live.md" in found, f"{source.__name__}: живой документ потерян"
        for rel in hidden:
            assert rel not in found, f"{source.__name__}: {rel} попало в список"


def test_iter_md_takes_the_list_from_git(repo: Path):
    """Основной путь — git: он понимает и вложенные .gitignore, чего фолбэк не умеет."""
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / "docs" / "nested").mkdir()
    (repo / "docs" / "nested" / ".gitignore").write_text("hidden.md\n", encoding="utf-8")
    (repo / "docs" / "nested" / "hidden.md").write_text("скрытый", encoding="utf-8")
    (repo / "docs" / "nested" / "shown.md").write_text("видимый", encoding="utf-8")

    assert gm.git_md_files(repo) is not None, "в репозитории список обязан приходить от git"
    found = {p.relative_to(repo).as_posix() for p in gm.iter_md(repo)}
    assert "docs/nested/shown.md" in found
    assert "docs/nested/hidden.md" not in found


def test_unsupported_rules_warn_when_git_is_absent(repo: Path, monkeypatch):
    """Без git фолбэк не исполняет негативы и '**' — обязан сказать вслух."""
    (repo / ".gitignore").write_text("!keep.md\n**/generated\n", encoding="utf-8")
    monkeypatch.setattr(gm, "git_md_files", lambda root: None)

    warnings = gm.gitignore_warnings(repo)

    assert any("!keep.md" in w for w in warnings)
    assert any("**/generated" in w for w in warnings)


def test_no_gitignore_warnings_on_the_git_path(repo: Path):
    """На основном пути подмножество не задействовано — предупреждать не о чем."""
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / ".gitignore").write_text("!keep.md\n", encoding="utf-8")

    assert gm.gitignore_warnings(repo) == []


# ── inventory: генерация и идемпотентность ─────────────────────────

def test_inventory_generates_tables(repo: Path):
    r = gm.cmd_inventory(repo)
    assert set(r["changed"]) == {"commands", "skills"}
    text = (repo / "docs" / "reference" / "commands.md").read_text(encoding="utf-8")
    assert "| `/foo` |" in _between(text, "commands")
    assert "| `test-skill` |" in _between(text, "skills")
    # вне маркеров файл не тронут
    assert "## `/foo` — test command" in text


def test_inventory_idempotent(repo: Path):
    gm.cmd_inventory(repo)
    before = (repo / "docs" / "reference" / "commands.md").read_text(encoding="utf-8")
    r = gm.cmd_inventory(repo)
    assert r["changed"] == []
    assert (repo / "docs" / "reference" / "commands.md").read_text(encoding="utf-8") == before


# ── inventory --check: поимка рассинхрона ──────────────────────────

def test_check_clean_after_generate(repo: Path):
    gm.cmd_inventory(repo)
    assert gm.cmd_inventory(repo, check=True)["issues"] == []


def test_check_catches_missing_frontmatter_fields(repo: Path):
    gm.cmd_inventory(repo)
    # убираем args:/drives: у команды
    (repo / ".omp" / "commands" / "foo.md").write_text(
        "---\ndescription: Test command for the registry.\n---\n\nBody.\n", encoding="utf-8")
    issues = gm.cmd_inventory(repo, check=True)["issues"]
    msgs = " ".join(m for _, m in issues)
    assert "args:" in msgs and "drives:" in msgs


def test_check_catches_missing_section(repo: Path):
    gm.cmd_inventory(repo)
    reg = repo / "docs" / "reference" / "commands.md"
    reg.write_text(reg.read_text(encoding="utf-8").replace("## `/foo` — test command", "## `/bar`"),
                   encoding="utf-8")
    issues = gm.cmd_inventory(repo, check=True)["issues"]
    msgs = " ".join(m for _, m in issues)
    assert "/foo" in msgs and "/bar" in msgs


def test_check_catches_stale_table(repo: Path):
    gm.cmd_inventory(repo)
    reg = repo / "docs" / "reference" / "commands.md"
    reg.write_text(reg.read_text(encoding="utf-8").replace("| `/foo` |", "| `/foo` | STALE"),
                   encoding="utf-8")
    issues = gm.cmd_inventory(repo, check=True)["issues"]
    assert any("рассинхронизирована" in m for _, m in issues)


# ── I7 в lint ──────────────────────────────────────────────────────

def test_lint_reports_i7_on_desync(repo: Path):
    # маркеры пусты, секции нет → рассинхрон
    r = gm.cmd_lint(repo)
    i7 = [i for i in r["issues"] if i[1] == "I7"]
    assert i7 and all(lvl == "ERR" for lvl, *_ in i7)
    # после генерации реестр синхронен (секция `/foo` уже в шаблоне) → I7 чист
    gm.cmd_inventory(repo)
    r = gm.cmd_lint(repo)
    assert [i for i in r["issues"] if i[1] == "I7"] == []
