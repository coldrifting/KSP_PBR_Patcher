from typing import Any

from utils.info_status import InfoStatus
from utils.terminal_colors import TerminalColors


def header(msg: Any):
    print(TerminalColors.CYAN + str(msg) + TerminalColors.ENDC)


def info(msg: Any, status: InfoStatus = InfoStatus.NONE, rewrite: bool = True):
    match status:
        case InfoStatus.NONE:
            prefix = " " * 7
        case InfoStatus.DONE:
            prefix = f"  [{TerminalColors.GREEN}OK{TerminalColors.ENDC}] "
        case InfoStatus.WARN:
            prefix = f" [{TerminalColors.YELLOW}WRN{TerminalColors.ENDC}] "
        case InfoStatus.ERROR:
            prefix = f" [{TerminalColors.RED}ERR{TerminalColors.ENDC}] "

    rewrite_text = TerminalColors.UP + TerminalColors.REWRITE if rewrite else ""
    print(rewrite_text + prefix + str(msg), flush=True)


def warn(msg: Any, should_exit: bool = False):
    print(TerminalColors.YELLOW + "WARNING: " + str(msg) + TerminalColors.ENDC)
    if should_exit:
        exit(1)


def error(msg: Any, display_prefix: bool = True):
    print(TerminalColors.RED + ("ERROR: " if display_prefix else "") + str(msg) + TerminalColors.ENDC)
