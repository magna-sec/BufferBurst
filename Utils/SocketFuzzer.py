import re
import socket
from time import sleep

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from Utils.Pattern import cyclic

_console = Console()


def _build_payload(data: str, prefix: str, template: str) -> str:
    if template:
        result = template.replace("*", data, 1)
        # Auto-update Content-Length after substitution
        sep = "\r\n\r\n"
        if sep in result:
            headers, body = result.split(sep, 1)
            body_len = len(body.encode("latin-1"))
            headers = re.sub(
                r"(Content-Length\s*:\s*)\d+",
                lambda m: m.group(1) + str(body_len),
                headers,
                flags=re.IGNORECASE,
            )
            result = headers + sep + body
        return result
    return prefix + data


def socket_fuzz(ip: str, port: int, fuzz_amount: int, prefix: str, template: str = "") -> int:
    if not fuzz_amount:
        fuzz_amount = 100
    amount = fuzz_amount

    with Progress(
        SpinnerColumn(),
        TextColumn("[cyan]Fuzzing[/]"),
        BarColumn(bar_width=30),
        TextColumn("[yellow]{task.description}[/]"),
        console=_console,
        transient=True,
    ) as progress:
        task = progress.add_task("starting...", total=None)

        while True:
            pattern = cyclic(min(amount, 456976)).decode("latin-1")
            payload = _build_payload(pattern, prefix, template)
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(5)
                    s.connect((ip, port))
                    s.recv(1024)
                    progress.update(task, description=f"{amount} bytes")
                    s.send(bytes(payload, "latin-1"))
                    s.recv(1024)
            except OSError:
                _console.print(f"[green]\\[I][/] Crashed at [yellow]{amount}[/] bytes")
                return amount

            amount += fuzz_amount
            sleep(0.5)
