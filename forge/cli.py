"""Forge command-line interface.

Minimal, deterministic developer tool CLI for Forge v0.2.
"""

from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
import typer

from forge.context import assemble_context
from forge.discovery import discover_projects, discover_skills
from forge.doctor import CheckStatus, run_doctor
from forge.scaffold import create_project

app = typer.Typer(
    name="forge",
    help="Forge: Personal software factory for solo engineering",
    add_completion=False,
)
console = Console()


@app.command(name="new")
def new_project(
    name: str = typer.Argument(..., help="Project name"),
    template: str = typer.Option("rust", "--template", "-t", help="Project template (rust, python, typescript, android)"),
    path: Optional[Path] = typer.Option(None, "--path", "-p", help="Target directory path"),
    force: bool = typer.Option(False, "--force", "-f", help="Force overwrite if target directory exists"),
):
    """Create a new project scaffold from a template."""
    try:
        dest = create_project(name=name, template=template, target_dir=path, force=force)
        console.print(
            f"[bold green]✔[/bold green] Created project '[bold cyan]{name}[/bold cyan]' "
            f"at [green]{dest}[/green] using template '[magenta]{template}[/magenta]'"
        )
    except Exception as ex:
        console.print(f"[bold red]✖[/bold red] {ex}")
        raise typer.Exit(code=1)


@app.command(name="skills")
def list_skills():
    """List available Forge skills."""
    skills = discover_skills()
    if not skills:
        console.print("[yellow]No Forge skills discovered in skills directory.[/yellow]")
        return

    table = Table(title="Available Forge Skills", show_header=True, header_style="bold cyan")
    table.add_column("Skill", style="bold green", no_wrap=True)
    table.add_column("Purpose", style="white")
    table.add_column("Location", style="dim")

    for s in skills:
        table.add_row(s.name, s.purpose, str(s.path))

    console.print(table)


@app.command(name="projects")
def list_projects(
    path: Optional[Path] = typer.Option(None, "--path", "-p", help="Projects directory path to scan"),
):
    """Discover Forge projects."""
    projects = discover_projects(projects_dir=path)
    if not projects:
        console.print("[yellow]No Forge projects discovered.[/yellow]")
        return

    table = Table(title="Discovered Forge Projects", show_header=True, header_style="bold cyan")
    table.add_column("Project", style="bold green", no_wrap=True)
    table.add_column("Language", style="magenta")
    table.add_column("Path", style="white")
    table.add_column("Status", style="dim")

    for p in projects:
        status = "[red]Error[/red]" if p.error else "[green]Ready[/green]"
        lang = p.language or "[dim]unspecified[/dim]"
        table.add_row(p.name, lang, str(p.path), status)

    console.print(table)

    # Show errors if any
    for p in projects:
        if p.error:
            console.print(f"[red]Warning ({p.name}):[/red] {p.error}")


@app.command(name="doctor")
def doctor_cmd(
    path: Optional[Path] = typer.Option(None, "--path", "-p", help="Optional project directory to diagnose"),
):
    """Diagnose Forge environment, runtime, and project health."""
    report = run_doctor(project_path=path)

    table = Table(title="Forge Environment Diagnostics", show_header=True, header_style="bold cyan")
    table.add_column("Category", style="bold magenta", no_wrap=True)
    table.add_column("Check", style="white", no_wrap=True)
    table.add_column("Status", justify="center", no_wrap=True)
    table.add_column("Message", style="dim")

    for check in report.checks:
        if check.status == CheckStatus.PASS:
            status_badge = "[bold green]PASS[/bold green]"
        elif check.status == CheckStatus.WARN:
            status_badge = "[bold yellow]WARN[/bold yellow]"
        else:
            status_badge = "[bold red]FAIL[/bold red]"

        table.add_row(check.category, check.name, status_badge, check.message)

    console.print(table)

    if report.overall_status == CheckStatus.FAIL:
        console.print("\n[bold red]✖ Forge diagnostics failed. Resolve failures above.[/bold red]")
        raise typer.Exit(code=1)
    elif report.overall_status == CheckStatus.WARN:
        console.print("\n[bold yellow]⚠ Forge diagnostics passed with warnings.[/bold yellow]")
    else:
        console.print("\n[bold green]✔ All Forge diagnostics passed.[/bold green]")


@app.command(name="context")
def generate_context(
    skill: Optional[str] = typer.Option(None, "--skill", "-s", help="Skill to attach (e.g. implementation, testing, planning)"),
    task: Optional[str] = typer.Option(None, "--task", "-t", help="Task ID, file path, or specification text"),
    path: Path = typer.Option(Path("."), "--path", "-p", help="Target project directory path"),
):
    """Assemble deterministic context for a coding agent."""
    try:
        ctx = assemble_context(skill=skill, task=task, project_dir=path)
        print(ctx)
    except Exception as ex:
        console.print(f"[bold red]✖[/bold red] {ex}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
