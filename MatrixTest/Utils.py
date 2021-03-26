import sys

COLOR_OK = "\033[92m"
COLOR_FAIL = "\033[91m"
COLOR_WARNING = "\033[93m"
COLOR_NORMAL = "\033[0m"


def print_ok(msg: str = "OK.") -> None:
    """
    Print in ``green`` color (ASCII code = ``\033[92m``) color. The color will be recovered to normal before this function returns.

    :param msg: The message to be printed.
    :return: None
    """
    print(COLOR_OK + msg + COLOR_NORMAL)


def print_warning(msg: str):
    """
    Print in ``yellow`` color (ASCII code = ``\033[93m``). The color will be recovered to normal before this function returns.

    :param msg: The message to be printed.
    :return: None
    """
    print(COLOR_WARNING + "WARNING: " + COLOR_NORMAL + msg)


def print_error(msg: str):
    """
    Print in ``red`` color (ASCII code = ``\033[91m``). The color will be recovered to normal before this function returns.

    :param msg: The message to be printed.
    :return: None
    """
    print(COLOR_FAIL + "ERROR: " + COLOR_NORMAL + msg)


def print_aborted():
    """
    Print in ``red`` color (ASCII code = ``\033[91m``) and exit with return code 1.
    The color will be recovered to normal before this function returns.

    """
    print(COLOR_FAIL + "Aborted." + COLOR_NORMAL)
    exit(1)


def print_info(msg: str):
    """
    Print with prefix ``INFO:``

    :param msg: The message to be printed.
    :return:
    """
    print("INFO: " + msg)


def default_parser(stdout: str) -> str:
    """
    This is the default parser function that can be used to instantiate :class:`MatrixTestRunner`.
    This function basically do nothing and return what is input.

    :param stdout: Text from ``stdout``.
    :return: Same as input.
    """
    return stdout


def removeprefix(long: str, prefix: str) -> str:
    """
    Simply remove the prefix from a string.

    :param long: The basic string from where this function will remove the prefix.
    :param prefix: The prefix to be removed.
    :return: The result string without prefix.
    """
    major, minor, _, _, _ = sys.version_info
    if major >= 3 and minor >= 9:
        return long.removeprefix(prefix)
    else:
        if long.startswith(prefix):
            return long[len(prefix):]
        else:
            return long
