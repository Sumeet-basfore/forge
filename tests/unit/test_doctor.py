"""Unit tests for Forge v0.2 doctor and diagnostic checks."""

from pathlib import Path
import pytest
import yaml

from forge.doctor import CheckStatus, DoctorReport, run_doctor


def test_doctor_healthy_environment():
    report = run_doctor()
    assert report.overall_status in {CheckStatus.PASS, CheckStatus.WARN}

    cat_map = {c.name: c for c in report.checks}
    assert "Python Version" in cat_map
    assert cat_map["Python Version"].status == CheckStatus.PASS

    assert "Skills Directory" in cat_map
    assert cat_map["Skills Directory"].status == CheckStatus.PASS

    assert "Rules Directory" in cat_map
    assert cat_map["Rules Directory"].status == CheckStatus.PASS

    assert "Templates Directory" in cat_map
    assert cat_map["Templates Directory"].status == CheckStatus.PASS


def test_doctor_missing_forge_directories(tmp_path: Path):
    empty_root = tmp_path / "empty_forge"
    empty_root.mkdir()

    report = run_doctor(forge_root=empty_root)
    assert report.overall_status == CheckStatus.FAIL

    failed_checks = [c.name for c in report.checks if c.status == CheckStatus.FAIL]
    assert "Skills Directory" in failed_checks
    assert "Rules Directory" in failed_checks
    assert "Templates Directory" in failed_checks


def test_doctor_with_valid_project(tmp_path: Path):
    proj_dir = tmp_path / "valid_project"
    proj_dir.mkdir()
    (proj_dir / ".forge").mkdir()
    (proj_dir / ".forge" / "config.yaml").write_text(
        yaml.dump({"project": {"name": "valid_app", "language": "rust"}}),
        encoding="utf-8",
    )

    report = run_doctor(project_path=proj_dir)
    cfg_check = next((c for c in report.checks if c.name == "Project Configuration"), None)
    assert cfg_check is not None
    assert cfg_check.status == CheckStatus.PASS
    assert "valid_app" in cfg_check.message


def test_doctor_with_invalid_project_config(tmp_path: Path):
    proj_dir = tmp_path / "bad_project"
    proj_dir.mkdir()
    (proj_dir / ".forge").mkdir()
    (proj_dir / ".forge" / "config.yaml").write_text("invalid_syntax: [unclosed bracket", encoding="utf-8")

    report = run_doctor(project_path=proj_dir)
    assert report.overall_status == CheckStatus.FAIL

    cfg_check = next((c for c in report.checks if c.name == "Project Configuration"), None)
    assert cfg_check is not None
    assert cfg_check.status == CheckStatus.FAIL
    assert "Failed to parse" in cfg_check.message


def test_doctor_with_missing_project_config(tmp_path: Path):
    proj_dir = tmp_path / "no_config_proj"
    proj_dir.mkdir()

    report = run_doctor(project_path=proj_dir)
    assert report.overall_status == CheckStatus.FAIL

    cfg_check = next((c for c in report.checks if c.name == "Project Configuration"), None)
    assert cfg_check is not None
    assert cfg_check.status == CheckStatus.FAIL
    assert "Missing .forge/config.yaml" in cfg_check.message
