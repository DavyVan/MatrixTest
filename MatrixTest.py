from typing import Dict, List, Callable, Any
import subprocess
import pandas as pd

COLOR_OK = "\033[92m"
COLOR_FAIL = "\033[91m"
COLOR_WARNING = "\033[93m"
COLOR_NORMAL = "\033[0m"


class MatrixTest:
    """
    MatrixTest is the all-in-one class to create a test suite with multi-dimensional test matrix.
    Please do not reuse one instance of this class for multiple tests.
    """

    def __cmd_format_checker(self) -> bool:
        """
        Check the format of command line template. Specifically:

        - Check if the braces can be matched in pairs

        :return: A boolean value indicating if they are matched.
        """

        # Check the '{' and '}' are matched in pairs
        print("Checking command line format...", end="")
        count = 0
        for i in self.__cmd:
            if i == "{":
                count += 1
            elif i == "}":
                count -= 1
        if count == 0:
            print(COLOR_OK + "OK" + COLOR_NORMAL + ".")
            return True
        elif count > 0:  # more "{"
            print(COLOR_WARNING + "WARNING" + COLOR_NORMAL + ": Braces do not match (more \"{\").")
            return False
        else:
            print(COLOR_WARNING + "WARNING" + COLOR_NORMAL + ": Braces do not match (more \"}\").")
            return False

    def __argument_matrix_checker(self, cmd: str) -> bool:
        """

        :param cmd:
        :return:
        """
        pass

    def __init__(self, cmd: str, matrix: Dict[str, List[str]], parser: Callable[[str], Any]):
        """

        :param cmd:
        :param matrix:
        :param parser:
        """
        self.__cmd = cmd
        self.__matrix = matrix
        self.__parser = parser

        # check the command format
        self.__cmd_format_checker()

        # check the matrix: if the tokens are identical with the command

    def run(self, repeat: int = 1) -> None:
        # initialize the result matrix
        pass
