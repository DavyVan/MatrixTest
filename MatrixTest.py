from typing import Dict, List, Callable, Any, get_type_hints
import subprocess
import pandas as pd
import colorama
import string

from Utils import *


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
        count = 0
        for i in self.__cmd:
            if i == "{":
                count += 1
            elif i == "}":
                count -= 1
        if count == 0:
            return True
        elif count > 0:  # more "{"
            return False
        else:
            return False

    def __argument_matrix_checker(self) -> bool:
        """
        Check if the changeable fields in command line match the keys in the matrix

        :return:    A boolean
        """
        # get the fields from cmd
        formatter = string.Formatter()
        fields_cmd = []
        it = formatter.parse(self.__cmd)
        for x in it:
            if x[1] is not None:
                fields_cmd.append(x[1])

        # get the fields from matrix
        fields_matrix = []
        for key in self.__matrix:
            fields_matrix.append(key)

        # check if they are matched
        fields_matrix.sort()
        fields_cmd.sort()
        return fields_matrix == fields_cmd

    def __init__(self, cmd: str, matrix: Dict[str, List[str]], parser: Callable[[str], Any]):
        """

        :param cmd:
        :param matrix:
        :param parser:
        """
        colorama.init()  # enable ANSI support on Windows for colored output

        self.__cmd = cmd
        self.__matrix = matrix
        self.__parser = parser

        # check the command format
        print("Checking command line format...", end="")
        if self.__cmd_format_checker():
            print_ok()
        else:
            print_warning("Braces do not match.")

        # check the matrix: if the tokens are identical with the command
        print("Checking argument keys...", end="")
        if self.__argument_matrix_checker():
            print_ok()
            self.__nargs = len(self.__matrix)
            self.__arg_keys = []
            for key in self.__matrix:
                self.__arg_keys.append(key)
        else:
            print_error("Keys in the command line do not match those in the matrix.")
            print_aborted()
            exit(1)

    def run(self, repeat: int = 1) -> None:
        # initialize the result matrix
        results_columns = ["cmd_full"]
        results_columns += self.__arg_keys
        # TODO: remove data type inference
        # for i in range(repeat):
        #     results_columns.append("attempt" + str(i+1))
        results = pd.DataFrame(columns=results_columns)
        #
        # # infer the result type from parser type hint
        # parser_type_hints = get_type_hints(self.__parser)
        # if "return" in parser_type_hints:
        #     parser_return_type = parser_type_hints["return"]
        #     df_type_str = ""
        #     if issubclass(parser_return_type, int):
        #         df_type_str = "int64"
        #     elif issubclass(parser_return_type, str):
        #         df_type_str = "string"
        #     elif issubclass(parser_return_type, float):
        #         df_type_str = "float64"
        #
        #     if df_type_str != "":
        #         print_info("Result data type has been inferred as " + df_type_str)
        #         new_types = {}
        #         for i in range(repeat):
        #             new_types["attempt" + str(i + 1)] = df_type_str
        #         results.astype(new_types)
        # else:
        #     print_info("Result data type will be inferred automatically by pandas")

        # configure the arg fields and run
        # init
        key_index = [0] * self.__nargs
        key_len = [0] * self.__nargs
        for i, key in enumerate(self.__arg_keys):
            key_len[i] = len(self.__matrix[key])
        args = {}

        while True:
            for i in range(self.__nargs):
                args[self.__arg_keys[i]] = self.__matrix[self.__arg_keys[i]][key_index[i]]

            current_cmd = self.__cmd.format_map(args)
            print("Running: " + current_cmd + "...")

            # run
            record = {"cmd_full": current_cmd}
            record.update(args)
            for attempt in range(repeat):
                print("Attempt " + str(attempt + 1) + "...", end="")
                current_result = subprocess.run(current_cmd, stdout=subprocess.PIPE, text=True, shell=True)
                if current_result.returncode != 0:
                    print_warning("Return code is " + str(current_result.returncode))
                else:
                    print_ok("Success")
                # print(current_result.stdout)

                # parse the result
                current_result_parsed = self.__parser(str(current_result.stdout))

                # record the result
                if isinstance(current_result_parsed, dict):  # if the parser function returns a dict (multiple results)
                    for key in current_result_parsed:
                        record["attempt" + str(attempt + 1) + "_" + key] = current_result_parsed[key]
                else:       # single result
                    record["attempt" + str(attempt + 1)] = current_result_parsed
            results = results.append(record, ignore_index=True)

            # get the next or break
            i = self.__nargs - 1
            while i >= 0:
                key_index[i] += 1
                if key_index[i] == key_len[i]:
                    key_index[i] = 0
                    i -= 1
                else:
                    break
            if i == -1:  # finished all test cases
                break
        print("All done.")
        # exit(0)
        # print(results)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
            print(results)
