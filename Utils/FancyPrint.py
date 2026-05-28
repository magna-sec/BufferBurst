from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

_console = Console()


def show_target(ip: str, port, trgt_type: str):
    t = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    t.add_column(style="blue bold")
    t.add_column(style="yellow")
    t.add_row("IP", str(ip))
    t.add_row("Port", str(port))
    t.add_row("Type", trgt_type)
    _console.print(Panel(t, title="[bold]Target[/]", border_style="cyan"))


def print_stage(title: str):
    _console.print()
    _console.rule(f"[bold cyan]{title}[/]")


def print_info(message: str, detail: str = ""):
    if detail:
        _console.print(f"[green]\\[I][/] {message}[dim]: [/][yellow]{detail}[/]")
    else:
        _console.print(f"[green]\\[I][/] {message}")


def print_warning(message: str):
    _console.print(f"[bold red]\\[!][/] {message}")


def print_success(message: str):
    _console.print(f"[bold green]\\[+][/] {message}")


def show_bad_bytes_grid(bad_bytes: list[str], remaining: str):
    remaining_set = {f"{ord(c):02x}" for c in remaining}
    bad_set = set(bad_bytes)

    t = Table(box=box.SIMPLE_HEAD, show_header=True, padding=(0, 1))
    t.add_column("  ", style="dim", min_width=3)
    for col in range(16):
        t.add_column(f"+{col:x}", justify="center", min_width=3)

    for row in range(16):
        cells = []
        for col in range(16):
            hx = f"{row * 16 + col:02x}"
            if hx in bad_set:
                cells.append(f"[bold red]{hx}[/]")
            elif hx in remaining_set:
                cells.append(f"[green]{hx}[/]")
            else:
                cells.append(f"[dim]{hx}[/]")
        t.add_row(f"{row:x}0", *cells)

    _console.print(Panel(
        t,
        title="[bold]Byte Grid[/]  [dim green]green=testing  [red]red=bad[/]  dim=removed[/]",
        border_style="yellow",
    ))
