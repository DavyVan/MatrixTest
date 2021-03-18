import sys

COLOR_OK = "\033[92m"
COLOR_FAIL = "\033[91m"
COLOR_WARNING = "\033[93m"
COLOR_NORMAL = "\033[0m"


def print_ok(msg: str = "OK."):
    print(COLOR_OK + msg + COLOR_NORMAL)


def print_warning(msg: str):
    print(COLOR_WARNING + "WARNING: " + COLOR_NORMAL + msg)


def print_error(msg: str):
    print(COLOR_FAIL + "ERROR: " + COLOR_NORMAL + msg)


def print_aborted():
    """
    This function will print and then abort.
    """
    print(COLOR_FAIL + "Aborted." + COLOR_NORMAL)
    exit(1)


def print_info(msg: str):
    print("INFO: " + msg)


def default_parser(stdout: str) -> str:
    return stdout


def removeprefix(long: str, prefix: str) -> str:
    major, minor, _, _, _ = sys.version_info
    if major >= 3 and minor >= 9:
        return long.removeprefix(prefix)
    else:
        if long.startswith(prefix):
            return long[len(prefix):]
        else:
            return long
