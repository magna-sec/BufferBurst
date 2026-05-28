import re
import socket
from time import sleep

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from Utils.Pattern import cyclic

_console = Console()


def _apply_template(template: str, data: str) -> str:
    """
    Substitute the fuzz payload into the template.
    POST: replaces * in the body (avoids */* wildcards in Accept headers).
    GET:  replaces * in the request line only.
    Content-Length is recalculated after substitution.
    """
    sep = "\r\n\r\n"
    if sep not in template:
        return template.replace("*", data, 1)

    headers, body = template.split(sep, 1)

    if "*" in body:
        # POST-style: payload is in the body
        new_body = body.replace("*", data, 1)
        new_headers = headers
    else:
        # GET-style: payload is in the request line (first header line)
        lines = headers.split("\r\n")
        lines[0] = lines[0].replace("*", data, 1)
        new_headers = "\r\n".join(lines)
        new_body = body

    # Recalculate Content-Length for requests that carry a body
    new_headers = re.sub(
        r"(Content-Length\s*:\s*)\d+",
        lambda m: m.group(1) + str(len(new_body.encode("latin-1"))),
        new_headers,
        flags=re.IGNORECASE,
    )

    return new_headers + sep + new_body


def _build_payload(data: str, prefix: str, template: str) -> str:
    if template:
        return _apply_template(template, data)
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
                    if not template:
                        s.recv(1024)  # consume socket server banner (e.g. vulnserver)
                    progress.update(task, description=f"{amount} bytes")
                    s.send(bytes(payload, "latin-1"))
                    s.recv(4096 if template else 1024)
            except OSError:
                _console.print(f"[green]\\[I][/] Crashed at [yellow]{amount}[/] bytes")
                return amount

            amount += fuzz_amount
            sleep(0.5)
