from rich.console import Console
from rich.prompt import Confirm

from Utils.FancyPrint import show_target
from Utils.Usage import parse_args
from Utils.CreateExploit import CreateExploit
from Utils.Session import Session
from Templates.Debuggers import DEBUGGERS

_console = Console()


def main():
    target = parse_args()
    show_target(target.ip, target.port, target.type)

    existing = Session.load_for(target.ip, target.port)
    session = None
    if existing:
        if existing.stage == "done":
            _console.print(f"[dim]Exploit already generated for [cyan]{target.ip}:{target.port}[/][/]")
            if Confirm.ask("[yellow]\\[?][/] Regenerate payload with new LHOST/LPORT (skip to Stage 6)?"):
                existing.stage = "payload"
                session = existing
            else:
                existing.delete()
        else:
            _console.print(f"[dim]Session found: [cyan]{target.ip}:{target.port}[/] — stage [bold]{existing.stage}[/][/]")
            if Confirm.ask("[yellow]\\[?][/] Resume?"):
                session = existing
                _console.print(f"[green]\\[+][/] Resuming from stage: [bold]{session.stage}[/]")
            else:
                existing.delete()

    exploit = CreateExploit(target, DEBUGGERS[target.debugger], session=session)
    exploit.start()


if __name__ == "__main__":
    main()
