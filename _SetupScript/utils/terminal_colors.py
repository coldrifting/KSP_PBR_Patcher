from enum import Enum
from typing import Any


class TerminalColors:
    WHITE = '\033[1;37m'
    CYAN = '\033[1;36m'
    GREEN = '\033[1;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[91m'

    UP = '\033[F'
    ENDC = '\033[0m'
    REWRITE = '\033[K'

class InfoStatus(Enum):
    NONE = 0,
    DONE = 1,
    WARN = 2,
    ERROR = 3,

def header(msg: Any):
    print(TerminalColors.CYAN + str(msg) + TerminalColors.ENDC)


def info(msg: Any, status: InfoStatus = InfoStatus.NONE, rewrite: bool = True):
    prefix_none = " " * 9
    prefix_done = f"    [{TerminalColors.GREEN}OK{TerminalColors.ENDC}] "
    prefix_warn = f"  [{TerminalColors.YELLOW}WARN{TerminalColors.ENDC}] "
    prefix_error = f" [{TerminalColors.RED}ERROR{TerminalColors.ENDC}] "

    rewrite_text = TerminalColors.UP + TerminalColors.REWRITE if rewrite else ""

    match status:
        case InfoStatus.NONE:
            print(prefix_none + str(msg), flush=True)
        case InfoStatus.DONE:
            print(rewrite_text + prefix_done + str(msg), flush=True)
        case InfoStatus.WARN:
            print(rewrite_text + prefix_warn + str(msg), flush=True)
        case InfoStatus.ERROR:
            print(rewrite_text + prefix_error + str(msg), flush=True)


def warn(msg: Any, should_exit: bool = False):
    print(TerminalColors.YELLOW + "WARNING: " + str(msg) + TerminalColors.ENDC)
    if should_exit:
        exit(1)


def error(msg: Any, display_prefix: bool = True):
    print()
    print(TerminalColors.RED + ("ERROR: " if display_prefix else "") + str(msg) + TerminalColors.ENDC)
    exit(1)
