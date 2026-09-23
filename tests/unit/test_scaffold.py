"""Unit tests for Forge v0.2 project scaffolding and template standardization."""

import os
from pathlib import Path
import pytest
from typer.testing import CliRunner
import yaml

from forge.cli import app
from forge.scaffold import create_project, list_templates

runner = CliRunner()


def test_list_templates():
    templates = list_templates()
    assert "rust" in templates
    assert "python" in templates
    assert "typescript" in templates
    assert "android" in templates


@pytest.mark.parametrize("template_name", ["rust", "python", "typescript", "android"])
def test_create_project_all_templates(tmp_path: Path, template_name: str):
    target = tmp_path / f"test_{template_name}_proj"
    res_path = create_project(name=f"test_{template_name}_proj", template=template_name, target_dir=target)

    assert res_path == target.resolve()
    assert (target / ".forge" / "config.yaml").is_file()
    assert (target / ".forge" / "tasks").is_dir()
    assert (target / "AGENTS.md").is_file()
    assert (target / "README.md").is_file()
    assert (target / "docs" / "architecture.md").is_file()
    assert (target / "docs" / "contributing.md").is_file()

    # Invariant: No state, evidence, or decision artifacts
    assert not (target / ".forge" / "state.yaml").exists()
    assert not (target / ".forge" / "evidence").exists()
    assert not (target / ".forge" / "decisions").exists()
    assert not (target / ".forge" / "reviews").exists()

    # Check config content and schema
    config_content = (target / ".forge" / "config.yaml").read_text(encoding="utf-8")
    config = yaml.safe_load(config_content)
    assert config["name"] == f"test_{template_name}_proj"
    assert config["language"] == template_name
    assert config["template"] == template_name
    assert "toolchain" in config
    assert "build" in config["toolchain"]
    assert "test" in config["toolchain"]
    assert "lint" in config["toolchain"]
    assert "format" in config["toolchain"]

    # Verify all text files have resolved placeholders
    for root, _dirs, files in os.walk(target):
        for file in files:
            file_path = Path(root) / file
            try:
                text = file_path.read_text(encoding="utf-8")
                assert "{{ project_name }}" not in text, f"Unresolved placeholder in {file_path}"
            except UnicodeDecodeError:
                pass


def test_invalid_template_fails(tmp_path: Path):
    with pytest.raises(ValueError, match="Unknown template"):
        create_project(name="invalid_proj", template="nonexistent_lang", target_dir=tmp_path / "inv")


def test_empty_project_name_fails(tmp_path: Path):
    with pytest.raises(ValueError, match="Project name cannot be empty"):
        create_project(name="   ", template="rust", target_dir=tmp_path / "empty")


def test_existing_directory_conflict_safety(tmp_path: Path):
    target = tmp_path / "existing_dir"
    target.mkdir()
    (target / "some_file.txt").write_text("critical user content", encoding="utf-8")

    # Hard Invariant: Must fail without force and preserve user content
    with pytest.raises(FileExistsError, match="already exists and is not empty"):
        create_project(name="existing_dir", template="rust", target_dir=target, force=False)

    assert (target / "some_file.txt").read_text(encoding="utf-8") == "critical user content"
    assert not (target / ".forge" / "config.yaml").exists()

    # Should succeed with force and keep existing non-conflicting files
    res = create_project(name="existing_dir", template="rust", target_dir=target, force=True)
    assert (res / ".forge" / "config.yaml").exists()
    assert (res / "some_file.txt").read_text(encoding="utf-8") == "critical user content"


def test_existing_forge_conflict_safety(tmp_path: Path):
    target = tmp_path / "forge_proj"
    target.mkdir()
    (target / ".forge").mkdir()
    (target / ".forge" / "config.yaml").write_text("existing: true\n", encoding="utf-8")

    # Hard Invariant: Must fail without force and never overwrite .forge/config.yaml
    with pytest.raises(FileExistsError, match="already contains .forge metadata"):
        create_project(name="forge_proj", template="rust", target_dir=target, force=False)

    # Original .forge/config.yaml strictly preserved
    assert "existing: true" in (target / ".forge" / "config.yaml").read_text(encoding="utf-8")

    # Should succeed with force
    create_project(name="forge_proj", template="rust", target_dir=target, force=True)
    assert "language: \"rust\"" in (target / ".forge" / "config.yaml").read_text(encoding="utf-8")


def test_binary_file_scaffold_safety(tmp_path: Path):
    # Create custom template with binary file
    templates_dir = tmp_path / "templates"
    tpl_dir = templates_dir / "binary_tpl"
    (tpl_dir / ".forge").mkdir(parents=True)
    (tpl_dir / ".forge" / "config.yaml").write_text("name: \"{{ project_name }}\"\nlanguage: \"bin\"\n", encoding="utf-8")

    # Write a binary file with invalid UTF-8 bytes
    binary_data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\xff\xff\x00\x00"
    (tpl_dir / "sample.png").write_bytes(binary_data)

    target = tmp_path / "binary_proj"
    create_project(
        name="binary_proj",
        template="binary_tpl",
        target_dir=target,
        templates_dir=templates_dir,
    )

    copied_binary = (target / "sample.png").read_bytes()
    assert copied_binary == binary_data


def test_cli_new_project_success(tmp_path: Path):
    target = tmp_path / "cli_rust_app"
    result = runner.invoke(app, ["new", "cli_rust_app", "--template", "rust", "--path", str(target)])
    assert result.exit_code == 0
    assert "Created project 'cli_rust_app'" in result.output
    assert (target / ".forge" / "config.yaml").exists()


def test_cli_new_project_conflict_safety(tmp_path: Path):
    target = tmp_path / "conflict_app"
    target.mkdir()
    (target / "file.txt").write_text("content", encoding="utf-8")

    # Fails without force
    result = runner.invoke(app, ["new", "conflict_app", "--template", "python", "--path", str(target)])
    assert result.exit_code == 1
    assert "already exists and is not empty" in result.output

    # Original file preserved
    assert (target / "file.txt").read_text(encoding="utf-8") == "content"
    assert not (target / ".forge").exists()

    # Succeeds with --force
    result_forced = runner.invoke(app, ["new", "conflict_app", "--template", "python", "--path", str(target), "--force"])
    assert result_forced.exit_code == 0
    assert (target / ".forge" / "config.yaml").exists()
