from typing import Dict, List, Callable, Any
import subprocess
import pandas as pd


class MatrixTest:
    """
    MatrixTest is the all-in-one class to create a test suite with multi-dimensional test matrix.
    Please do not reuse one instance of this class for multiple tests.
    """

    def __init__(self, cmd: str, matrix: Dict[str, List[str]], parser: Callable[[str], Any]):
        """

        :param cmd:
        :param matrix:
        :param parser:
        """
        self.__cmd = cmd
        self.__matrix = matrix
        self.__parser = parser

        # check the command format: % in pairs

        # check the matrix: if the tokens are identical with the command

    def run(self, repeat: int = 1) -> None:
        # initialize the result matrix
        pass
