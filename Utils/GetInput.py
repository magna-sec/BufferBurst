import socket
import time
from ipaddress import ip_address

from rich.console import Console
from rich.prompt import Prompt, Confirm

_console = Console()


def wait_for_service(ip: str, port: int, timeout: int = 120) -> bool:
    """Poll TCP until the service is reachable again. Shows a spinner."""
    with _console.status("[yellow]Waiting for service to come back up...[/]"):
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    s.connect((ip, port))
                    _console.print("[green]\\[+][/] Service is back up.")
                    return True
            except OSError:
                time.sleep(1)
    _console.print("[red]\\[!][/] Timed out waiting for service.")
    return False


def get_eip() -> str:
    return Prompt.ask("[yellow]\\[?][/] EIP value from debugger [dim](hex, e.g. 64636261)[/]")


def get_jmpesp() -> str:
    return Prompt.ask("[yellow]\\[?][/] JMP ESP address [dim](e.g. 625011af)[/]")


def get_bad_bytes_input() -> list[str]:
    raw = Prompt.ask("[yellow]\\[?][/] Bad bytes found [dim](e.g. 0a 0d) — blank if none[/]")
    if not raw.strip():
        return []
    return [b.strip().lower().zfill(2) for b in raw.split() if b.strip()]


def get_ip() -> str:
    while True:
        val = Prompt.ask("[yellow]\\[?][/] LHOST [dim](your attacker IP)[/]")
        try:
            ip_address(val)
            return val
        except ValueError:
            _console.print("[red]\\[!][/] Invalid IP format.")


def get_port() -> int:
    while True:
        val = Prompt.ask("[yellow]\\[?][/] LPORT [dim](your listener port)[/]")
        try:
            p = int(val)
            if 0 <= p <= 65535:
                return p
            _console.print("[red]\\[!][/] Port must be 0–65535.")
        except ValueError:
            _console.print("[red]\\[!][/] Enter a number.")


def confirm(message: str) -> bool:
    return Confirm.ask(f"[yellow]\\[?][/] {message}")


def prompt_service_restart():
    """Ask the user to restart the service manually and wait for them to confirm."""
    _console.print("[yellow]\\[?][/] Restart the service / relaunch in your debugger, then press Enter to continue...", end="")
    input()
