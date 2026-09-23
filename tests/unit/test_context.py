"""Unit tests for Forge v0.2 deterministic context assembly."""

from pathlib import Path
import pytest
from typer.testing import CliRunner

from forge.cli import app
from forge.context import (
    assemble_context,
    list_available_skills,
    load_global_rules,
    load_project_context,
    load_skill,
    load_task,
)
from forge.scaffold import create_project

runner = CliRunner()


# -----------------------------------------------------------------------------
# 1. Rules Tests
# -----------------------------------------------------------------------------

def test_load_global_rules_deterministic():
    rules_text = load_global_rules()
    assert "## 1. Global Rules" in rules_text
    assert "### rules/agents.md" in rules_text
    assert "### rules/engineering.md" in rules_text
    assert "### rules/git.md" in rules_text
    assert "### rules/safety.md" in rules_text

    # Verify strict alphabetical ordering: agents -> engineering -> git -> safety
    idx_agents = rules_text.find("### rules/agents.md")
    idx_eng = rules_text.find("### rules/engineering.md")
    idx_git = rules_text.find("### rules/git.md")
    idx_safety = rules_text.find("### rules/safety.md")
    assert idx_agents < idx_eng < idx_git < idx_safety


def test_load_global_rules_missing_dir(tmp_path: Path):
    missing_dir = tmp_path / "nonexistent_rules"
    with pytest.raises(FileNotFoundError, match="Global rules directory not found"):
        load_global_rules(missing_dir)


def test_load_global_rules_empty_dir(tmp_path: Path):
    empty_dir = tmp_path / "empty_rules"
    empty_dir.mkdir()
    res = load_global_rules(empty_dir)
    assert "No global rule files found" in res


def test_load_global_rules_content_preservation(tmp_path: Path):
    custom_rules = tmp_path / "custom_rules"
    custom_rules.mkdir()
    (custom_rules / "01_test.md").write_text("# Rule 01\nExact content line.", encoding="utf-8")

    res = load_global_rules(custom_rules)
    assert "### rules/01_test.md" in res
    assert "Exact content line." in res


# -----------------------------------------------------------------------------
# 2. Skills Tests
# -----------------------------------------------------------------------------

def test_list_available_skills():
    skills = list_available_skills()
    expected = [
        "architecture",
        "code-review",
        "documentation",
        "implementation",
        "planning",
        "project-init",
        "release",
        "research",
        "specification",
        "testing",
    ]
    for exp in expected:
        assert exp in skills


def test_load_valid_skill():
    skill_text = load_skill("implementation")
    assert "## 2. Skill" in skill_text
    assert "### implementation" in skill_text
    assert "## Purpose" in skill_text
    assert "Execute precise" in skill_text


def test_load_invalid_skill_raises():
    with pytest.raises(ValueError, match="Unknown skill 'nonexistent'"):
        load_skill("nonexistent")


def test_load_skill_empty_raises():
    with pytest.raises(ValueError, match="Skill name cannot be empty"):
        load_skill("   ")


@pytest.mark.parametrize("traversal", ["../../secret", "../skills", "/etc/passwd", ".."])
def test_load_skill_traversal_protection(traversal: str):
    with pytest.raises(ValueError, match="(Path traversal detected|Unknown skill)"):
        load_skill(traversal)


def test_load_skill_missing_skills_dir(tmp_path: Path):
    missing_dir = tmp_path / "missing_skills"
    with pytest.raises(FileNotFoundError, match="Skills directory not found"):
        load_skill("implementation", skills_dir=missing_dir)


# -----------------------------------------------------------------------------
# 3. Project Context Tests
# -----------------------------------------------------------------------------

def test_load_project_context_populated(tmp_path: Path):
    proj_dir = create_project("test_proj", template="rust", target_dir=tmp_path / "test_proj")
    ctx = load_project_context(proj_dir)

    assert "## 3. Project Context" in ctx
    assert "### .forge/config.yaml" in ctx
    assert "cargo check" in ctx
    assert "### AGENTS.md" in ctx
    assert "### docs/architecture.md" in ctx


def test_load_project_context_partial(tmp_path: Path):
    proj_dir = tmp_path / "partial_proj"
    proj_dir.mkdir()
    (proj_dir / "AGENTS.md").write_text("# Agents file only", encoding="utf-8")

    ctx = load_project_context(proj_dir)
    assert "## 3. Project Context" in ctx
    assert "### AGENTS.md" in ctx
    assert "### .forge/config.yaml" not in ctx
    assert "### docs/architecture.md" not in ctx


def test_load_project_context_empty_dir(tmp_path: Path):
    empty_dir = tmp_path / "empty_dir"
    empty_dir.mkdir()
    ctx = load_project_context(empty_dir)
    assert "## 3. Project Context" in ctx
    assert "No project context files found" in ctx


def test_load_project_context_missing_dir(tmp_path: Path):
    missing = tmp_path / "nonexistent_dir"
    with pytest.raises(FileNotFoundError, match="Project directory not found"):
        load_project_context(missing)


# -----------------------------------------------------------------------------
# 4. Task Tests
# -----------------------------------------------------------------------------

def test_load_task_direct_text():
    res = load_task("Implement a fast cache with LRU eviction")
    assert "## 4. Task" in res
    assert "Implement a fast cache with LRU eviction" in res


def test_load_task_file_resolution(tmp_path: Path):
    proj_dir = tmp_path / "proj"
    tasks_dir = proj_dir / ".forge" / "tasks"
    tasks_dir.mkdir(parents=True)
    task_file = tasks_dir / "TASK-001.md"
    task_file.write_text("# Task 001: Sample Objective\nDetails here.", encoding="utf-8")

    # Resolve by ID without extension
    res1 = load_task("TASK-001", proj_dir)
    assert "## 4. Task" in res1
    assert "### TASK-001" in res1
    assert "Sample Objective" in res1

    # Resolve by file name with extension
    res2 = load_task("TASK-001.md", proj_dir)
    assert "Sample Objective" in res2


def test_load_task_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError, match="Task file for 'TASK-999' not found"):
        load_task("TASK-999", tmp_path)


# -----------------------------------------------------------------------------
# 5. Determinism & Composition Tests
# -----------------------------------------------------------------------------

def test_assemble_context_composition_and_order(tmp_path: Path):
    proj_dir = create_project("full_proj", template="python", target_dir=tmp_path / "full_proj")
    task_file = proj_dir / ".forge" / "tasks" / "TASK-010.md"
    task_file.write_text("# Implement Feature X\nDetailed steps.", encoding="utf-8")

    full_context = assemble_context(
        skill="implementation",
        task="TASK-010",
        project_dir=proj_dir,
    )

    # Verify the 4 main sections in exact order
    assert "# Forge Agent Context" in full_context
    assert "## 1. Global Rules" in full_context
    assert "## 2. Skill" in full_context
    assert "## 3. Project Context" in full_context
    assert "## 4. Task" in full_context

    idx_rules = full_context.find("## 1. Global Rules")
    idx_skill = full_context.find("## 2. Skill")
    idx_proj = full_context.find("## 3. Project Context")
    idx_task = full_context.find("## 4. Task")

    assert idx_rules < idx_skill < idx_proj < idx_task


def test_assemble_context_strict_determinism(tmp_path: Path):
    proj_dir = create_project("det_proj", template="typescript", target_dir=tmp_path / "det_proj")
    task_file = proj_dir / ".forge" / "tasks" / "TASK-001.md"
    task_file.write_text("# Determinism Test\nByte-for-byte equivalence.", encoding="utf-8")

    ctx1 = assemble_context(skill="testing", task="TASK-001", project_dir=proj_dir)
    ctx2 = assemble_context(skill="testing", task="TASK-001", project_dir=proj_dir)

    # Byte-for-byte equivalence
    assert ctx1 == ctx2
    assert len(ctx1) > 0


def test_cli_context_command(tmp_path: Path):
    proj_dir = create_project("cli_proj", template="rust", target_dir=tmp_path / "cli_proj")
    task_file = proj_dir / ".forge" / "tasks" / "TASK-005.md"
    task_file.write_text("# CLI Context Test\nVerification steps.", encoding="utf-8")

    result = runner.invoke(app, [
        "context",
        "--skill", "testing",
        "--task", "TASK-005",
        "--path", str(proj_dir),
    ])

    assert result.exit_code == 0
    assert "# Forge Agent Context" in result.output
    assert "## 1. Global Rules" in result.output
    assert "## 2. Skill" in result.output
    assert "## 3. Project Context" in result.output
    assert "## 4. Task" in result.output
    assert "CLI Context Test" in result.output
