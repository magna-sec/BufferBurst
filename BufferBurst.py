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

    session = None
    if Session.exists():
        if Confirm.ask("[yellow]\\[?][/] Existing session found — resume?"):
            session = Session.load()
            _console.print(f"[green]\\[+][/] Resuming from stage: [bold]{session.stage}[/]")
        else:
            Session.delete()

    exploit = CreateExploit(target, DEBUGGERS[target.debugger], session=session)
    exploit.start()


if __name__ == "__main__":
    main()
