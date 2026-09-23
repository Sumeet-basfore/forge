"""Pytest fixtures for Forge tests."""

from pathlib import Path
import subprocess
import tempfile
import pytest


@pytest.fixture
def temp_dir():
    """Provides a clean temporary directory."""
    with tempfile.TemporaryDirectory(prefix="forge-test-") as td:
        yield Path(td)


@pytest.fixture
def git_repo(temp_dir):
    """Provides a clean git repository initialized with an initial commit."""
    repo_path = temp_dir / "test_repo"
    repo_path.mkdir(parents=True, exist_ok=True)

    subprocess.run(["git", "init"], cwd=repo_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Forge Test"], cwd=repo_path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "test@forge.local"], cwd=repo_path, check=True, capture_output=True)

    # Initial file and commit
    readme = repo_path / "README.md"
    readme.write_text("# Test Repo\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo_path, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True, capture_output=True)

    return repo_path
