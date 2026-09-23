"""Unit and E2E tests for Forge v0.2 CLI commands."""

from pathlib import Path
import pytest
from typer.testing import CliRunner
import yaml

from forge.cli import app

runner = CliRunner()


def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Forge: Personal software factory for solo engineering" in result.output
    assert "new" in result.output
    assert "skills" in result.output
    assert "context" in result.output
    assert "projects" in result.output
    assert "doctor" in result.output


def test_cli_skills():
    result = runner.invoke(app, ["skills"])
    assert result.exit_code == 0
    assert "Available Forge Skills" in result.output
    assert "implementation" in result.output
    assert "planning" in result.output
    assert "testing" in result.output


def test_cli_projects(tmp_path: Path):
    projects_dir = tmp_path / "test_projects"
    projects_dir.mkdir()

    # Empty
    res_empty = runner.invoke(app, ["projects", "--path", str(projects_dir)])
    assert res_empty.exit_code == 0
    assert "No Forge projects discovered" in res_empty.output

    # Populated
    proj_a = projects_dir / "app_a"
    proj_a.mkdir()
    (proj_a / ".forge").mkdir()
    (proj_a / ".forge" / "config.yaml").write_text(
        yaml.dump({"project": {"name": "app_a", "language": "rust"}}),
        encoding="utf-8",
    )

    res_pop = runner.invoke(app, ["projects", "--path", str(projects_dir)])
    assert res_pop.exit_code == 0
    assert "Discovered Forge Projects" in res_pop.output
    assert "app_a" in res_pop.output
    assert "rust" in res_pop.output


def test_cli_doctor():
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "Forge Environment Diagnostics" in result.output
    assert "PASS" in result.output


def test_cli_doctor_with_project(tmp_path: Path):
    proj_dir = tmp_path / "diag_project"
    proj_dir.mkdir()
    (proj_dir / ".forge").mkdir()
    (proj_dir / ".forge" / "config.yaml").write_text(
        yaml.dump({"project": {"name": "diag_project", "language": "python"}}),
        encoding="utf-8",
    )

    result = runner.invoke(app, ["doctor", "--path", str(proj_dir)])
    assert result.exit_code == 0
    assert "diag_project" in result.output


def test_cli_new_and_context_workflow(tmp_path: Path):
    target = tmp_path / "demo_app"

    # 1. forge new
    r_new = runner.invoke(app, ["new", "demo_app", "--template", "rust", "--path", str(target)])
    assert r_new.exit_code == 0
    assert "Created project 'demo_app'" in r_new.output
    assert (target / ".forge" / "config.yaml").exists()

    # 2. Add task file
    task_file = target / ".forge" / "tasks" / "TASK-001.md"
    task_file.write_text("# Build Feature\nStep 1: Write code.", encoding="utf-8")

    # 3. forge context
    r_ctx = runner.invoke(app, [
        "context",
        "--skill", "implementation",
        "--task", "TASK-001",
        "--path", str(target),
    ])
    assert r_ctx.exit_code == 0
    assert "# Forge Agent Context" in r_ctx.output
    assert "## 1. Global Rules" in r_ctx.output
    assert "## 2. Skill" in r_ctx.output
    assert "## 3. Project Context" in r_ctx.output
    assert "## 4. Task" in r_ctx.output
    assert "Step 1: Write code." in r_ctx.output
