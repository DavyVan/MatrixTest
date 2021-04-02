import sys


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
