from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
import time
import subprocess
from rich.live import Live
from rich.text import Text

console = Console()

def is_python_file(path):
    return path.exists() and path.suffix.lower() == '.py'



# Add these helper functions above interactive_mode()

def _format_val(v):
    if v is None:
        return "(none)"
    if isinstance(v, (list, tuple)):
        return ", ".join(str(x) for x in v) or "(none)"
    return str(v)

def display_help_state(state: dict):
    """Show current variables and developer options when user types 'help'."""
    tbl = Table.grid(expand=True)
    tbl.add_column(justify="right", ratio=30)
    tbl.add_column(ratio=70)
    # Main variables
    tbl.add_row("Script", _format_val(state.get("input_file")))
    tbl.add_row("Output dir", _format_val(state.get("output")))
    tbl.add_row("Mode", "onefile" if state.get("onefile") else "onedir")
    tbl.add_row("Windowed", _format_val(state.get("windowed")))
    tbl.add_row("Name", _format_val(state.get("name")))
    tbl.add_row("Icon", _format_val(state.get("icon")))
    tbl.add_row("Hidden imports", _format_val(state.get("hidden_imports")))
    tbl.add_row("Exclude modules", _format_val(state.get("exclude_modules")))
    tbl.add_row("Add data", _format_val(state.get("add_data")))
    tbl.add_row("Clean", _format_val(state.get("clean")))
    tbl.add_row("Debug", _format_val(state.get("debug")))
    tbl.add_row("Verbose", _format_val(state.get("verbose")))
    # Dev options
    tbl.add_row("Dev mode", _format_val(state.get("dev_mode")))
    tbl.add_row("Spec path", _format_val(state.get("spec_path")))
    tbl.add_row("Work path", _format_val(state.get("work_path")))
    tbl.add_row("Python path", _format_val(state.get("python_path")))
    console.print(Panel(tbl, title="[bold cyan]Current variables & dev options (help)[/]"))

def show_header():
    """Print a simple header for the interactive mode."""
    console.print(Panel(
        "[bold green]Py to EXE Converter (Made By EmanuelPlays) [/]\nConfigure PyInstaller options via prompts",
        title="[bold magenta]Welcome[/]",
        expand=False,
    ))


def ask_confirm_with_help(prompt: str, default: bool, state: dict) -> bool:
    """
    Ask a yes/no question but if the user types 'help' show the current state/dev options.
    Returns True/False.
    """
    default_str = "y" if default else "n"
    while True:
        ans = Prompt.ask(f"{prompt} [y/n/help]", default=default_str).strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        if ans == "help":
            display_help_state(state)
            continue
        # any other input: re-prompt
        console.print("[yellow]Please answer 'y', 'n', or 'help'.[/]")


# Replace the original interactive_mode with this updated version:

def interactive_mode(cfg: dict) -> dict:
    console.print()
    show_header()

    # Remember last used values
    last_output = cfg.get("last_output", str(Path.cwd() / "dist"))
    last_onefile = cfg.get("last_onefile", True)
    last_windowed = cfg.get("last_windowed", False)

    while True:
        p = Prompt.ask("[bold]Path to Python file[/]", default=cfg.get("last_input", ""))
        ip = Path(p).expanduser().resolve()
        if not is_python_file(ip):
            console.print(f"[red]Error:[/] File does not exist or is not a .py file: {ip}")
            if not Confirm.ask("Try again?", default=True):
                raise SystemExit(1)
            continue
        break

    # Basic prompts
    name = Prompt.ask("[bold]Executable name (optional, leave blank to use script name)[/]", default="")
    output = Prompt.ask("[bold]Output directory[/]", default=last_output)
    onefile = Confirm.ask("[bold]Build as single file?[/]", default=last_onefile)
    windowed = Confirm.ask("[bold]Windowed (no console)?[/]", default=last_windowed)
    icon_path = Prompt.ask("[bold]Icon path (optional)[/]", default="").strip()
    icon = Path(icon_path).expanduser().resolve() if icon_path else None
    hidden = Prompt.ask("[bold]Hidden imports (comma separated, optional)[/]", default="")
    exclude = Prompt.ask("[bold]Exclude modules (comma separated, optional)[/]", default="")
    add_data = Prompt.ask("[bold]Add data (repeat format 'SRC;DEST' comma separated, optional)[/]", default="")
    upx_dir = Prompt.ask("[bold]UPX directory path (optional, for compression)[/]", default="").strip()
    runtime_hook = Prompt.ask("[bold]Runtime hook file (optional)[/]", default="").strip()
    version_file = Prompt.ask("[bold]Version info file (optional)[/]", default="").strip()
    manifest = Prompt.ask("[bold]Manifest file (optional)[/]", default="").strip()
    key = Prompt.ask("[bold]Encryption key (optional, for bytecode encryption)[/]", default="").strip()
    strip = Confirm.ask("[bold]Strip debug information?[/]", default=False)
    bootloader_ignore_signals = Confirm.ask("[bold]Bootloader ignore signals?[/]", default=False)
    codesign_identity = Prompt.ask("[bold]Codesign identity (optional, for macOS)[/]", default="").strip()
    entitlements_file = Prompt.ask("[bold]Entitlements file (optional, for macOS)[/]", default="").strip()

    # Prepare a mutable state so 'help' can show current values
    state = {
        "input_file": ip,
        "output": Path(output).expanduser().resolve(),
        "name": name if name else None,
        "onefile": onefile,
        "windowed": windowed,
        "icon": icon if icon and icon.exists() else None,
        "hidden_imports": [h.strip() for h in hidden.split(",") if h.strip()],
        "exclude_modules": [e.strip() for e in exclude.split(",") if e.strip()],
        "add_data": [a.strip() for a in add_data.split(",") if a.strip()],
        "upx_dir": Path(upx_dir).expanduser().resolve() if upx_dir else None,
        "runtime_hook": Path(runtime_hook).expanduser().resolve() if runtime_hook else None,
        "version_file": Path(version_file).expanduser().resolve() if version_file else None,
        "manifest": Path(manifest).expanduser().resolve() if manifest else None,
        "key": key if key else None,
        "strip": strip,
        "bootloader_ignore_signals": bootloader_ignore_signals,
        "codesign_identity": codesign_identity if codesign_identity else None,
        "entitlements_file": Path(entitlements_file).expanduser().resolve() if entitlements_file else None,
        "clean": False,
        "debug": False,
        "verbose": False,
        "no_confirm": False,
        "dev_mode": False,
        "spec_path": None,
        "work_path": None,
        "python_path": None,
    }

    # Boolean prompts that support 'help'
    state["clean"] = ask_confirm_with_help("[bold]Clean build (remove cache)?[/]", False, state)
    state["debug"] = ask_confirm_with_help("[bold]Enable debug?[/]", False, state)
    state["verbose"] = ask_confirm_with_help("[bold]Verbose output?[/]", False, state)

    # Developer mode (optional)
    state["dev_mode"] = ask_confirm_with_help("[bold]Enable developer mode? (spec/work/python paths)[/]", False, state)
    if state["dev_mode"]:
        sp = Prompt.ask("[bold]Spec path (optional)[/]", default="")
        wp = Prompt.ask("[bold]Work path (optional)[/]", default="")
        pp = Prompt.ask("[bold]Python executable path (optional, runs 'python -m PyInstaller')[/]", default="")
        state["spec_path"] = Path(sp).expanduser().resolve() if sp.strip() else None
        state["work_path"] = Path(wp).expanduser().resolve() if wp.strip() else None
        state["python_path"] = pp.strip() or None

    # Skip confirmations / final run
    state["no_confirm"] = ask_confirm_with_help("[bold]Skip confirmations and run now?[/]", False, state)

    # Save last used
    cfg.update(
        {
            "last_input": str(ip),
            "last_output": str(state["output"]),
            "last_onefile": state["onefile"],
            "last_windowed": state["windowed"],
        }
    )

    parsed = {
        "input_file": state["input_file"],
        "output": state["output"],
        "name": state["name"],
        "onefile": state["onefile"],
        "windowed": state["windowed"],
        "icon": state["icon"],
        "hidden_imports": state["hidden_imports"],
        "exclude_modules": state["exclude_modules"],
        "add_data": state["add_data"],
        "upx_dir": state["upx_dir"],
        "runtime_hook": state["runtime_hook"],
        "version_file": state["version_file"],
        "manifest": state["manifest"],
        "key": state["key"],
        "strip": state["strip"],
        "bootloader_ignore_signals": state["bootloader_ignore_signals"],
        "codesign_identity": state["codesign_identity"],
        "entitlements_file": state["entitlements_file"],
        "clean": state["clean"],
        "debug": state["debug"],
        "verbose": state["verbose"],
        "no_confirm": state["no_confirm"],
        "spec_path": state["spec_path"],
        "work_path": state["work_path"],
        "python_path": state["python_path"],
        "dev_mode": state["dev_mode"],
    }

    return cfg, parsed


def main():
    """Main entry point for the Py to EXE Converter."""
    cfg = {}  # Configuration dictionary, can be loaded from file if needed
    cfg, parsed = interactive_mode(cfg)
    console.print("[green]Configuration complete![/]")

    # Build PyInstaller command
    cmd = ["pyinstaller"]
    if parsed["onefile"]:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")
    if parsed["windowed"]:
        cmd.append("--windowed")
    if parsed["name"]:
        cmd.append(f"--name={parsed['name']}")
    if parsed["icon"]:
        cmd.append(f"--icon={parsed['icon']}")
    for hidden in parsed["hidden_imports"]:
        cmd.append(f"--hidden-import={hidden}")
    for exclude in parsed["exclude_modules"]:
        cmd.append(f"--exclude-module={exclude}")
    for data in parsed["add_data"]:
        cmd.append(f"--add-data={data}")
    if parsed["upx_dir"]:
        cmd.append(f"--upx-dir={parsed['upx_dir']}")
    if parsed["runtime_hook"]:
        cmd.append(f"--runtime-hook={parsed['runtime_hook']}")
    if parsed["version_file"]:
        cmd.append(f"--version-file={parsed['version_file']}")
    if parsed["manifest"]:
        cmd.append(f"--manifest={parsed['manifest']}")
    if parsed["key"]:
        cmd.append(f"--key={parsed['key']}")
    if parsed["strip"]:
        cmd.append("--strip")
    if parsed["bootloader_ignore_signals"]:
        cmd.append("--bootloader-ignore-signals")
    if parsed["codesign_identity"]:
        cmd.append(f"--codesign-identity={parsed['codesign_identity']}")
    if parsed["entitlements_file"]:
        cmd.append(f"--entitlements-file={parsed['entitlements_file']}")
    if parsed["clean"]:
        cmd.append("--clean")
    if parsed["debug"]:
        cmd.append("--debug=all")
    if parsed["verbose"]:
        cmd.append("--verbose")
    if parsed["spec_path"]:
        cmd.append(f"--specpath={parsed['spec_path']}")
    if parsed["work_path"]:
        cmd.append(f"--workpath={parsed['work_path']}")
    if parsed["python_path"]:
        cmd.append(f"--python={parsed['python_path']}")
    cmd.append(str(parsed["input_file"]))

    console.print(f"[bold blue]Running command:[/] {' '.join(cmd)}")
    console.print("[bold blue]This May take a while[/]")
    with Live(Text("Building", style="bold blue"), refresh_per_second=8) as live:
        for i in range(20):
            dots = "." * (i % 4)
            live.update(Text(f"Building{dots}", style="bold blue"))
            time.sleep(0.08)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            console.print("[green]Build successful![/]")
            console.print(result.stdout)
            console.print(f"[bold]Executable located in:[/] {parsed['output']}")
        else:
            console.print("[red]Build failed![/]")
            console.print(result.stderr)
    except Exception as e:
        console.print(f"[red]Error running PyInstaller: {e}[/]")


if __name__ == "__main__":
    main()
