from typing import Dict, List, Callable, Any, get_type_hints, Union
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

    def __init__(self, cmd: str, matrix: Dict[str, List[str]], parser: Callable[[str], Any] = None):
        """

        :param cmd:
        :param matrix:
        :param parser:
        """
        colorama.init()  # enable ANSI support on Windows for colored output

        self.__cmd = cmd
        self.__matrix = matrix
        if parser is None:
            print_warning(
                "No parser function received. The outputs of commands will be stored as string without parsing.")
            self.__parser = default_parser
        else:
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

        # declare variables for a single run
        self.__last_result = None
        self.__last_repeat = 0

    def run(self, repeat: int = 1) -> None:
        if repeat < 1:
            print_error("repeat must be at least 1.")
            print_aborted()
        self.__last_repeat = repeat

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
            print("Running: " + current_cmd)

            # run
            record = {"cmd_full": current_cmd}
            record.update(args)
            for attempt in range(repeat):
                print("Attempt " + str(attempt + 1) + "...", end="")
                current_result = subprocess.run(current_cmd, stdout=subprocess.PIPE, text=True, shell=True)
                if current_result.returncode != 0:
                    print_error("Return code is " + str(current_result.returncode))
                    print_error("STDERR:" + str(current_result.stderr))
                    print_error("STDOUT:" + str(current_result.stdout))
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

        self.__last_result = results
        print("All done.")

    def get_last_result(self) -> pd.DataFrame:
        """

        :return: pandas.DataFrame. Return the internal dataframe storing the final results.
        """
        return self.__last_result

    def average(self, column: Union[str, List[str]]) -> None:
        """
        This function compute the arithmetic mean of selected columns.
        The results will store in the same dataframe with names of "avg_*".

        :param column: str or List of str. Name(s) of selected column(s). If any column does not exist in the result, the
                    calculation will be skipped. Generally, this should be a subset of the keys returned by the parser function.
        """

        # convert the str to List[str]. Will use List anyway in the following
        if isinstance(column, str):
            column = [column]

        # check column
        columns = self.__last_result.columns
        for item in column:
            t = "attempt1_" + item      # only check one of them
            found = False
            for col in columns:
                if t == col:
                    found = True
                    break
            if not found:
                print_warning("The calculation of mean is skipped for %s is skipped because we cannot find it in the last result" % item)
                column.remove(item)

        # calculate start
        dtypes = self.__last_result.dtypes
        for item in column:
            # construct column names
            columns_in_result = []
            for i in range(self.__last_repeat):
                columns_in_result.append("attempt%d_%s" % (i+1, item))

            # check data types
            for col in columns_in_result:
                if not pd.api.types.is_numeric_dtype(self.__last_result[col]):
                    print_warning("The column %s is not in numeric type, may produce unexpected results." % col)

            # execute calculation
            self.__last_result["avg_"+item] = self.__last_result[columns_in_result].mean(axis=1, numeric_only=True)

